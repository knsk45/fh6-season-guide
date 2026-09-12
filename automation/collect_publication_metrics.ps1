[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$RunId,
    [string]$ProjectPath,
    [string]$MetricsStatePath,
    [string]$HistoryPath,
    [long]$SteamViews = -1,
    [long]$SteamFavorites = -1
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
if (-not $ProjectPath) { $ProjectPath = Join-Path $RepoRoot 'data\project.json' }
if (-not $MetricsStatePath) { $MetricsStatePath = Join-Path $RepoRoot 'automation\runs\publication-metrics-state.json' }
if (-not $HistoryPath) { $HistoryPath = Join-Path $RepoRoot 'data\publication-metrics-history.json' }

function ConvertTo-MetricInteger {
    param(
        [Parameter(Mandatory = $true)][string]$Value,
        [Parameter(Mandatory = $true)][string]$Name
    )

    $Digits = $Value -replace '[^0-9-]', ''
    $Parsed = 0L
    if ([string]::IsNullOrWhiteSpace($Digits) -or -not [long]::TryParse($Digits, [ref]$Parsed)) {
        throw "Unable to parse $Name metric from '$Value'."
    }
    return $Parsed
}

function Get-SteamTableMetric {
    param(
        [Parameter(Mandatory = $true)][string]$Html,
        [Parameter(Mandatory = $true)][string]$Label
    )

    $Pattern = '<tr[^>]*>\s*<td[^>]*>\s*([^<]+?)\s*</td>\s*<td[^>]*>\s*' + [regex]::Escape($Label) + '\s*</td>\s*</tr>'
    $Match = [regex]::Match($Html, $Pattern, [Text.RegularExpressions.RegexOptions]::IgnoreCase)
    if (-not $Match.Success) { throw "Steam metric '$Label' was not found on the public guide page." }
    return ConvertTo-MetricInteger -Value ([Net.WebUtility]::HtmlDecode($Match.Groups[1].Value)) -Name $Label
}

function Write-MetricOutput {
    param([Parameter(Mandatory = $true)]$Snapshot)

    Write-Host 'PUBLIC_METRICS_STATUS=OK'
    Write-Host "PUBLIC_METRICS_RUN_ID=$($Snapshot.runId)"
    Write-Host "PUBLIC_METRICS_BASELINE=$($Snapshot.baselineCreated.ToString().ToUpperInvariant())"
    Write-Host "STEAM_VIEWS=$($Snapshot.steam.views)"
    Write-Host "STEAM_VIEWS_ADDED=$($Snapshot.steam.viewsAdded)"
    Write-Host "STEAM_FAVORITES=$($Snapshot.steam.favorites)"
    Write-Host "STEAM_FAVORITES_ADDED=$($Snapshot.steam.favoritesAdded)"
    Write-Host "GITHUB_VIEWS_TOTAL=$($Snapshot.github.viewsTotal)"
    Write-Host "GITHUB_VIEWS_TODAY=$($Snapshot.github.viewsToday)"
    Write-Host "GITHUB_VIEWS_ADDED=$($Snapshot.github.viewsAdded)"
}

function Update-PublicHistory {
    param(
        [Parameter(Mandatory = $true)]$Snapshot,
        [Parameter(Mandatory = $true)][string]$Path
    )

    if (-not (Test-Path -LiteralPath $Path)) { throw "Publication metrics history is missing: $Path" }
    $History = Get-Content -LiteralPath $Path -Raw -Encoding UTF8 | ConvertFrom-Json -DateKind String
    if ($History.schemaVersion -ne 1 -or $null -eq $History.snapshots -or $null -eq $History.source) {
        throw 'Publication metrics history has an unsupported schema.'
    }

    $Entry = [ordered]@{
        runId = [string]$Snapshot.runId
        collectedAt = [string]$Snapshot.collectedAt
        steamViews = [long]$Snapshot.steam.views
        steamFavorites = [long]$Snapshot.steam.favorites
        githubViews = [long]$Snapshot.github.viewsTotal
    }
    $Existing = @($History.snapshots | Where-Object { [string]$_.runId -ne [string]$Snapshot.runId })
    $History.snapshots = @($Existing + [pscustomobject]$Entry | Sort-Object { [DateTimeOffset]::Parse([string]$_.collectedAt, [Globalization.CultureInfo]::InvariantCulture, [Globalization.DateTimeStyles]::RoundtripKind) } | Select-Object -Last 60)
    $History | Add-Member -NotePropertyName updatedAt -NotePropertyValue ([DateTimeOffset]::Now.ToString('o')) -Force

    $Directory = Split-Path -Parent $Path
    if (-not (Test-Path -LiteralPath $Directory)) { New-Item -ItemType Directory -Path $Directory | Out-Null }
    $TemporaryPath = "$Path.tmp"
    [IO.File]::WriteAllText($TemporaryPath, ($History | ConvertTo-Json -Depth 12) + "`r`n", [Text.UTF8Encoding]::new($false))
    Move-Item -LiteralPath $TemporaryPath -Destination $Path -Force
    Write-Host "PUBLIC_METRICS_HISTORY=UPDATED"
    Write-Host "PUBLIC_METRICS_HISTORY_POINTS=$(@($History.snapshots).Count)"
}

if ([string]::IsNullOrWhiteSpace($RunId)) { throw 'RunId cannot be empty.' }
$Project = Get-Content -LiteralPath $ProjectPath -Raw -Encoding UTF8 | ConvertFrom-Json
if (-not $Project.steamGuide.enabled) { throw 'Steam guide metrics are disabled in data/project.json.' }
if (-not $Project.analytics.enabled) { throw 'GitHub Pages analytics are disabled in data/project.json.' }
if ([string]::IsNullOrWhiteSpace([string]$Project.analytics.statsApiUrl)) { throw 'project.analytics.statsApiUrl is required.' }

$Previous = $null
if (Test-Path -LiteralPath $MetricsStatePath) {
    try { $Previous = Get-Content -LiteralPath $MetricsStatePath -Raw -Encoding UTF8 | ConvertFrom-Json }
    catch { throw "Publication metrics state is unreadable: $($_.Exception.Message)" }

    if ([string]$Previous.runId -eq $RunId) {
        Write-MetricOutput -Snapshot $Previous
        exit 0
    }
}

if (($SteamViews -ge 0) -xor ($SteamFavorites -ge 0)) {
    throw 'Provide both -SteamViews and -SteamFavorites, or neither.'
}

$SteamMetricsSource = 'public-page'
if ($SteamViews -lt 0) {
    $SteamResponse = Invoke-WebRequest -UseBasicParsing -Uri ([string]$Project.steamGuide.url) -TimeoutSec 30
    if ($SteamResponse.StatusCode -ne 200) { throw "Steam guide returned HTTP $($SteamResponse.StatusCode)." }
    $SteamViews = Get-SteamTableMetric -Html $SteamResponse.Content -Label 'Unique Visitors'
    $SteamFavorites = Get-SteamTableMetric -Html $SteamResponse.Content -Label 'Current Favorites'
} else {
    $SteamMetricsSource = 'browser-verified-owner-view'
}

$HitsResponse = Invoke-RestMethod -Method Get -Uri ([string]$Project.analytics.statsApiUrl) -TimeoutSec 30
$GitHubTotal = [long]$HitsResponse.total
$TodayKey = [DateTimeOffset]::Now.ToOffset([TimeSpan]::FromHours(7)).ToString('yyyy-MM-dd')
$GitHubToday = 0L
foreach ($Bucket in @($HitsResponse.items)) {
    foreach ($Day in @($Bucket.data)) {
        if ([string]$Day.day -eq $TodayKey) { $GitHubToday = [long]$Day.value; break }
    }
}

$BaselineCreated = $null -eq $Previous
$SteamViewsAdded = if ($BaselineCreated) { 0L } else { $SteamViews - [long]$Previous.steam.views }
$SteamFavoritesAdded = if ($BaselineCreated) { 0L } else { $SteamFavorites - [long]$Previous.steam.favorites }
$GitHubViewsAdded = if ($BaselineCreated) { 0L } else { $GitHubTotal - [long]$Previous.github.viewsTotal }

$Snapshot = [ordered]@{
    schemaVersion = 1
    runId = $RunId
    collectedAt = [DateTimeOffset]::Now.ToString('o')
    baselineCreated = $BaselineCreated
    steam = [ordered]@{
        views = $SteamViews
        viewsAdded = $SteamViewsAdded
        favorites = $SteamFavorites
        favoritesAdded = $SteamFavoritesAdded
    }
    github = [ordered]@{
        viewsTotal = $GitHubTotal
        viewsToday = $GitHubToday
        viewsAdded = $GitHubViewsAdded
    }
    steamMetricsSource = $SteamMetricsSource
}

$StateDirectory = Split-Path -Parent $MetricsStatePath
if (-not (Test-Path -LiteralPath $StateDirectory)) { New-Item -ItemType Directory -Path $StateDirectory | Out-Null }
$TemporaryPath = "$MetricsStatePath.tmp"
[IO.File]::WriteAllText($TemporaryPath, ($Snapshot | ConvertTo-Json -Depth 8) + "`r`n", [Text.UTF8Encoding]::new($false))
Move-Item -LiteralPath $TemporaryPath -Destination $MetricsStatePath -Force

Update-PublicHistory -Snapshot $Snapshot -Path $HistoryPath

Write-MetricOutput -Snapshot $Snapshot
