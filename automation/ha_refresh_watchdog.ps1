[CmdletBinding()]
param(
    [ValidateSet('Install','Check','Test','Receipt')][string]$Action = 'Check',
    [string]$ResultPath
)
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$local = Get-Content -Raw (Join-Path $RepoRoot 'automation/runs/home-assistant-notification.local.json') | ConvertFrom-Json
$secret = Get-Content -Raw (Join-Path $RepoRoot $local.homeAssistantSecretPath) | ConvertFrom-Json
$api = $secret.home_assistant.api_base_url.TrimEnd('/')
$headers = @{Authorization=('Bearer ' + $secret.home_assistant.long_lived_access_tokens.health_auto_export.raw_token)}
$receiptId = 'fh6_refresh_receipt'
$watchId = 'fh6_refresh_watchdog'
function Request([string]$Method,[string]$Path,$Data=$null) {
    $params = @{Method=$Method;Uri="$api/$Path";Headers=$headers;TimeoutSec=30}
    if ($null -ne $Data) { $params.ContentType='application/json; charset=utf-8'; $params.Body=($Data | ConvertTo-Json -Depth 40 -Compress) }
    Invoke-RestMethod @params
}
function Entity([string]$Id) {
    $allStates = Request GET 'states'
    $matches = @($allStates | Where-Object { $_.entity_id -like 'automation.*' -and $_.attributes.PSObject.Properties['id'] -and $_.attributes.id -eq $Id })
    if ($matches.Count -ne 1) {throw "Expected exactly one HA automation with id $Id"}
    return $matches[0]
}
function TimePoint($Value) {
    # Invoke-RestMethod may already deserialize an ISO date into DateTime.
    # Converting it to a culture-dependent string can swap month/day in ru-RU.
    if ($Value -is [DateTimeOffset]) { return $Value }
    if ($Value -is [DateTime]) { return [DateTimeOffset]$Value }
    return [DateTimeOffset]::Parse([string]$Value,[Globalization.CultureInfo]::InvariantCulture)
}
$config = Request GET 'config'
if ($config.time_zone -ne 'Asia/Krasnoyarsk') {throw 'HA timezone differs from agreed Asia/Krasnoyarsk; install aborted.'}

if ($Action -eq 'Install') {
    # Back up only the exact two configurations before any mutation. No secrets in backups.
    $backupDir = Join-Path $RepoRoot ('automation/runs/watchdog-backup-' + (Get-Date -Format 'yyyyMMdd-HHmmss'))
    New-Item -ItemType Directory -Path $backupDir | Out-Null
    foreach ($id in @($receiptId,$watchId)) {
        $old=$null
        try {$old=Request GET "config/automation/config/$id"} catch {
            if ([int]$_.Exception.Response.StatusCode -ne 404) {throw}
        }
        [IO.File]::WriteAllText((Join-Path $backupDir "$id.json"), ($old | ConvertTo-Json -Depth 40), [Text.UTF8Encoding]::new($false))
    }
    $receipt = @{
        id=$receiptId; alias='FH6: получение итогового статуса'; description='Подтверждение итогового результата FH6 после проверенного уведомления. Событие приходит через авторизованный REST API. last_triggered сохраняет дату получения для независимого контроля.'
        triggers=@(@{trigger='event';event_type='fh6_refresh_finished'})
        conditions=@(@{condition='template';value_template="{{ trigger.event.data.get('project') == 'fh6' and trigger.event.data.get('schemaVersion') == 1 and trigger.event.data.get('runDate') == now().strftime('%Y-%m-%d') and trigger.event.data.get('status') in ['COMPLETED','BLOCKED','PENDING_CONFIRMATION'] and trigger.event.data.get('notification') in ['SENT','ALREADY_SENT'] and (trigger.event.data.get('runId','') | length) > 5 and as_timestamp(trigger.event.data.get('completedAt'), 0) >= as_timestamp(today_at('06:00')) and as_timestamp(trigger.event.data.get('completedAt'), 0) <= as_timestamp(now()) + 30 }}"})
        actions=@(@{variables=@{received_run_id='{{ trigger.event.data.runId }}';received_status='{{ trigger.event.data.status }}'}})
        mode='queued';max=5
    }
    $null=Request POST "config/automation/config/$receiptId" $receipt
    $receiptEntity=(Entity $receiptId).entity_id
    $check = "{% set receipt = state_attr('$receiptEntity', 'last_triggered') %}{% set last_alert = this.attributes.get('last_triggered') %}{{ now() >= today_at('06:30') and (receipt is none or as_timestamp(receipt, 0) < as_timestamp(today_at('06:00'))) and (last_alert is none or as_timestamp(last_alert, 0) < as_timestamp(today_at('00:00'))) }}"
    $watch = @{
        id=$watchId;alias='FH6: контроль ежедневного обновления';description='Ежедневно в 06:30 Красноярск и после восстановления HA (контроль каждые 5 минут). Одно предупреждение в день, если нет подтверждённого итогового результата FH6. Не зависит от Codex и его компьютера.'
        triggers=@(@{trigger='time';at='06:30:00'},@{trigger='time_pattern';minutes='/5'})
        conditions=@(@{condition='template';value_template=$check})
        actions=@(@{action=$local.notifyService;data=@{title='FH6 — нет результата обновления';message='Сегодня не получен подтверждённый итог ежедневного обновления FH6. Возможно, компьютер выключен или выполнение прервалось. Откройте чат «Сводка сезона».';data=@{tag='fh6-refresh-watchdog';group='fh6-season-guide';url='https://knsk45.github.io/fh6-season-guide/reports/current-week.html'}}})
        mode='single'
    }
    $null=Request POST "config/automation/config/$watchId" $watch
    foreach ($pair in @(@($receiptId,$receipt),@($watchId,$watch))) {
        $saved=Request GET "config/automation/config/$($pair[0])"
        if ($saved.alias -ne $pair[1].alias -or @($saved.actions).Count -ne @($pair[1].actions).Count) {throw 'Saved HA config verification failed'}
        $null=Request POST 'services/automation/turn_on' @{entity_id=(Entity $pair[0]).entity_id}
    }
    $checkConfig=Request POST 'config/core/check_config' @{}
    if ($checkConfig.result -ne 'valid') {throw 'HA check_config did not return valid; inspect backed-up target configs before further changes.'}
    Write-Host "HA_WATCHDOG_BACKUP=$backupDir"
    Write-Host 'HA_CONFIG_CHECK=valid'
}

if ($Action -eq 'Receipt') {
    $result=Get-Content -Raw -LiteralPath $ResultPath | ConvertFrom-Json
    $active=Get-Content -Raw (Join-Path $RepoRoot 'automation/runs/refresh/active.json') | ConvertFrom-Json
    if ($result.runId -ne $active.runId -or $active.notification -notin @('SENT','ALREADY_SENT')) {throw 'Run result is not associated with a sent final notification.'}
    if ((Get-FileHash -LiteralPath $ResultPath -Algorithm SHA256).Hash.ToLowerInvariant() -ne $active.resultSha256) {throw 'Result fingerprint mismatch'}
    if ($result.status -notin @('COMPLETED','BLOCKED','PENDING_CONFIRMATION')) {throw 'Invalid final status'}
    $before=[DateTimeOffset]::UtcNow.AddSeconds(-1)
    $payload=@{schemaVersion=1;project='fh6';runId=$result.runId;runDate=$result.runDate;status=$result.status;notification=$active.notification;completedAt=[DateTimeOffset]::Now.ToString('o')}
    $null=Request POST 'events/fh6_refresh_finished' $payload
    for($i=0;$i -lt 8;$i++) {
        $entity=Entity $receiptId
        if ($entity.attributes.last_triggered -and (TimePoint $entity.attributes.last_triggered) -ge $before) {
            Write-Host 'HA_RECEIPT_STATUS=CONFIRMED'
            Write-Host "HA_RECEIPT_ENTITY=$($entity.entity_id)"
            exit 0
        }
        Start-Sleep -Seconds 1
    }
    throw 'HA did not confirm the receipt event; do not mark the run completed.'
}

if ($Action -eq 'Test') {
    $sample=[DateTimeOffset]::Parse('2026-09-03T07:04:11.401021+07:00',[Globalization.CultureInfo]::InvariantCulture)
    foreach($value in @($sample,$sample.LocalDateTime,$sample.ToString('o'))) {
        if ((TimePoint $value) -ne $sample) {throw 'HA receipt date conversion regression'}
    }
    Write-Host 'HA_RECEIPT_DATE_TEST=PASS'
    # Exercise HA's real Jinja evaluator without triggering notifications or altering receipt state.
    $saved=Request GET "config/automation/config/$watchId"
    $expr=$saved.conditions[0].value_template
    $cases=@(
        @{name='before_deadline';hour=6;minute=20;receipt=-1;alert=-1;expected='False'},
        @{name='missing_result';hour=6;minute=30;receipt=-1;alert=-1;expected='True'},
        @{name='result_received';hour=6;minute=30;receipt=6.2;alert=-1;expected='False'},
        @{name='duplicate_suppressed';hour=7;minute=0;receipt=-1;alert=6.5;expected='False'},
        @{name='restart_catchup';hour=8;minute=0;receipt=-1;alert=-1;expected='True'}
    )
    foreach($case in $cases) {
        $testExpr=$expr -replace "state_attr\('[^']+', 'last_triggered'\)", 'fake_receipt'
        $testExpr=$testExpr.Replace("this.attributes.get('last_triggered')",'fake_alert').Replace('now() >=', 'fake_now >=')
        $prefix="{% set fake_now = today_at('$($case.hour):$($case.minute.ToString('00'))') %}"
        $prefix+='{% set fake_receipt = ' + $(if($case.receipt -lt 0){'none'}else{"today_at('00:00') + timedelta(hours=$($case.receipt))"}) + ' %}'
        $prefix+='{% set fake_alert = ' + $(if($case.alert -lt 0){'none'}else{"today_at('00:00') + timedelta(hours=$($case.alert))"}) + ' %}'
        $actual=[string](Request POST 'template' @{template=($prefix+$testExpr)})
        if ($actual.Trim() -ne $case.expected) {throw "Watchdog test failed: $($case.name), got $actual"}
        Write-Host "HA_WATCHDOG_TEST=$($case.name):PASS"
    }
}
foreach($id in @($receiptId,$watchId)) {
    $e=Entity $id
    if ($e.state -ne 'on') {throw "HA automation $id is not enabled"}
    Write-Host "HA_AUTOMATION=$id ON entity=$($e.entity_id)"
}
Write-Host 'HA_WATCHDOG_STATUS=READY'
