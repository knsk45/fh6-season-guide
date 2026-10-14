Set-StrictMode -Version Latest
$ErrorActionPreference='Stop'
. (Join-Path $PSScriptRoot 'notification_text.ps1')
function Assert-True($Value,$Message) { if (-not $Value) { throw $Message } }
$metrics=[pscustomobject]@{baselineCreated=$false;steam=[pscustomobject]@{viewsAdded=3;favoritesAdded=-1};github=[pscustomobject]@{viewsAdded=2}}
$result=[pscustomobject]@{message='Сводка актуальна, содержательных изменений не требуется; дата проверки обновлена. HTML: 101980 байт. GitHub-коммит: PRIVATE_SECRET'}
foreach ($status in @('UpToDate','UpdateRequired','CheckBlocked')) {
    $n=Get-Fh6NotificationText -Status $status -CheckedResult $result -Metrics $metrics
    Assert-True ($n.message.Length -le 200) 'Push too long'
    Assert-True (-not $n.message.Contains('PRIVATE_SECRET') -and -not $n.message.Contains('HTML:')) 'Detailed result leaked'
    Assert-True ($n.message.Contains('Steam +3') -and $n.message.Contains('сайт +2') -and $n.message.Contains('избранное -1')) 'Deltas missing'
}
$n=Get-Fh6NotificationText -Status UpToDate -CheckedResult $result
Assert-True ($n.message.Contains('Новых данных нет') -and $n.message.Contains('Дата проверки обновлена')) 'Unchanged run unclear'
$n=Get-Fh6NotificationText -Status CheckBlocked
Assert-True (-not $n.message.Contains('актуальны')) 'Blocked run presented as success'
$metrics.baselineCreated=$true
$n=Get-Fh6NotificationText -Status UpToDate -Metrics $metrics
Assert-True ($n.message.Contains('первый замер') -and -not $n.message.Contains('Steam +3')) 'Baseline counted as growth'
Write-Output 'NOTIFICATION_TEXT_TESTS=PASSED'
