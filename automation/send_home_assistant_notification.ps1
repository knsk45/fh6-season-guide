[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet('UpdateRequired', 'UpToDate', 'CheckBlocked')]
    [string]$Status,
    [string]$RunId,
    [string]$ProjectPath,
    [string]$LocalConfigPath,
    [string]$DeliveryStatePath,
    [string]$MetricsStatePath
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
if (-not $ProjectPath) { $ProjectPath = Join-Path $RepoRoot 'data\project.json' }
$Project = Get-Content -LiteralPath $ProjectPath -Raw -Encoding UTF8 | ConvertFrom-Json
$Notifications = $Project.notifications

if (-not $Notifications.enabled) {
    Write-Host 'HA_NOTIFICATION_STATUS=DISABLED'
    exit 0
}
if ([string]$Notifications.provider -ne 'home-assistant') { throw "Unsupported notification provider: $($Notifications.provider)" }
if (-not $LocalConfigPath) { $LocalConfigPath = Join-Path $RepoRoot ([string]$Notifications.localConfigPath) }
if (-not $DeliveryStatePath) { $DeliveryStatePath = Join-Path $RepoRoot 'automation\runs\home-assistant-notification-state.json' }
if (-not $MetricsStatePath) { $MetricsStatePath = Join-Path $RepoRoot 'automation\runs\publication-metrics-state.json' }
if (-not $RunId) { $RunId = [DateTimeOffset]::Now.ToString('yyyyMMdd-HHmmsszzz') }

if (-not (Test-Path -LiteralPath $LocalConfigPath)) {
    Write-Host 'HA_NOTIFICATION_STATUS=BLOCKED'
    Write-Host "HA_NOTIFICATION_ERROR=local config not found: $LocalConfigPath"
    exit 2
}
$LocalConfig = Get-Content -LiteralPath $LocalConfigPath -Raw -Encoding UTF8 | ConvertFrom-Json
$SecretPath = [IO.Path]::GetFullPath((Join-Path $RepoRoot ([string]$LocalConfig.homeAssistantSecretPath)))
if (-not (Test-Path -LiteralPath $SecretPath)) {
    Write-Host 'HA_NOTIFICATION_STATUS=BLOCKED'
    Write-Host 'HA_NOTIFICATION_ERROR=Home Assistant secret file not found'
    exit 2
}

$Service = [string]$LocalConfig.notifyService
if ($Service -notmatch '^notify\.(?<name>[a-z0-9_]+)$') { throw "Invalid Home Assistant notify service: $Service" }
$ServiceName = $Matches.name
$Secret = Get-Content -LiteralPath $SecretPath -Raw -Encoding UTF8 | ConvertFrom-Json
$ApiBase = ([string]$Secret.home_assistant.api_base_url).TrimEnd('/')
$Token = [string]$Secret.home_assistant.long_lived_access_tokens.health_auto_export.raw_token
if ([string]::IsNullOrWhiteSpace($ApiBase) -or [string]::IsNullOrWhiteSpace($Token)) {
    Write-Host 'HA_NOTIFICATION_STATUS=BLOCKED'
    Write-Host 'HA_NOTIFICATION_ERROR=Home Assistant API URL or token is missing'
    exit 2
}

if (Test-Path -LiteralPath $DeliveryStatePath) {
    try {
        $Previous = Get-Content -LiteralPath $DeliveryStatePath -Raw -Encoding UTF8 | ConvertFrom-Json
        if ([string]$Previous.runId -eq $RunId -and [string]$Previous.status -eq $Status) {
            Write-Host 'HA_NOTIFICATION_STATUS=ALREADY_SENT'
            Write-Host "HA_NOTIFICATION_RUN_ID=$RunId"
            exit 0
        }
    }
    catch { Write-Verbose "Ignoring unreadable delivery state: $($_.Exception.Message)" }
}

$MessageKey = switch ($Status) {
    'UpdateRequired' { 'updateRequired' }
    'UpToDate' { 'upToDate' }
    'CheckBlocked' { 'checkBlocked' }
}
$Content = $Notifications.messages.$MessageKey
if (-not $Content -or [string]::IsNullOrWhiteSpace([string]$Content.title) -or [string]::IsNullOrWhiteSpace([string]$Content.message)) {
    throw "Notification text is not configured for status $Status."
}

$MetricsMessage = 'Статистика публикаций недоступна для этого запуска.'
if (Test-Path -LiteralPath $MetricsStatePath) {
    try {
        $Metrics = Get-Content -LiteralPath $MetricsStatePath -Raw -Encoding UTF8 | ConvertFrom-Json
        if ([string]$Metrics.runId -eq $RunId) {
            if ($Metrics.baselineCreated -eq $true) {
                $MetricsMessage = "Статистика: создан начальный снимок. Steam — $($Metrics.steam.views) просмотров, $($Metrics.steam.favorites) в избранном; GitHub-сводка — $($Metrics.github.viewsTotal) просмотров."
            }
            else {
                $SteamViewsAdded = '{0:+0;-0;0}' -f [long]$Metrics.steam.viewsAdded
                $SteamFavoritesAdded = '{0:+0;-0;0}' -f [long]$Metrics.steam.favoritesAdded
                $GitHubViewsAdded = '{0:+0;-0;0}' -f [long]$Metrics.github.viewsAdded
                $MetricsMessage = "С прошлого успешного запуска: Steam — просмотры $SteamViewsAdded (всего $($Metrics.steam.views)), избранное $SteamFavoritesAdded (всего $($Metrics.steam.favorites)); GitHub-сводка — просмотры $GitHubViewsAdded (всего $($Metrics.github.viewsTotal))."
            }
        }
    }
    catch { Write-Verbose "Ignoring unreadable publication metrics state: $($_.Exception.Message)" }
}

$Body = [ordered]@{
    title = $Content.title
    message = "$($Content.message)`n`n$MetricsMessage"
    data = [ordered]@{
        tag = 'fh6-season-status'
        group = 'fh6-season-guide'
        url = [string]$Project.steamGuide.publicGuideUrl
    }
}
$Headers = @{ Authorization = "Bearer $Token" }
$Uri = "$ApiBase/services/notify/$ServiceName"

try {
    $Response = Invoke-RestMethod -Method Post -Uri $Uri -Headers $Headers -ContentType 'application/json; charset=utf-8' -Body ($Body | ConvertTo-Json -Depth 8 -Compress) -TimeoutSec 20
}
catch {
    Write-Host 'HA_NOTIFICATION_STATUS=BLOCKED'
    Write-Host "HA_NOTIFICATION_ERROR=$($_.Exception.Message)"
    exit 2
}

$Directory = Split-Path -Parent $DeliveryStatePath
if (-not (Test-Path -LiteralPath $Directory)) { New-Item -ItemType Directory -Path $Directory | Out-Null }
$Delivery = [ordered]@{
    schemaVersion = 1
    runId = $RunId
    status = $Status
    service = $Service
    sentAt = [DateTimeOffset]::Now.ToString('o')
}
[IO.File]::WriteAllText($DeliveryStatePath, ($Delivery | ConvertTo-Json -Depth 5) + "`r`n", [Text.UTF8Encoding]::new($false))

Write-Host 'HA_NOTIFICATION_STATUS=SENT'
Write-Host "HA_NOTIFICATION_TYPE=$Status"
Write-Host "HA_NOTIFICATION_RUN_ID=$RunId"
