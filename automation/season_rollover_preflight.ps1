[CmdletBinding()]
param(
    [string]$StatePath,
    [string]$ProjectPath,
    [string]$HistoryPath,
    [string]$OutputPath
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
if (-not $StatePath) { $StatePath = Join-Path $RepoRoot 'data\current-season.json' }
if (-not $ProjectPath) { $ProjectPath = Join-Path $RepoRoot 'data\project.json' }
if (-not $HistoryPath) { $HistoryPath = Join-Path $RepoRoot 'data\publication-metrics-history.json' }
if (-not $OutputPath) { $OutputPath = Join-Path $RepoRoot 'automation\runs\rollover-preflight\last.json' }

function Require-File {
    param([string]$Path, [string]$Label)
    if (-not (Test-Path -LiteralPath $Path)) { throw "$Label is missing: $Path" }
}

Require-File $StatePath 'Season state'
Require-File $ProjectPath 'Project config'
Require-File $HistoryPath 'Publication metrics history'

$State = Get-Content -LiteralPath $StatePath -Raw -Encoding UTF8 | ConvertFrom-Json
$Project = Get-Content -LiteralPath $ProjectPath -Raw -Encoding UTF8 | ConvertFrom-Json
$History = Get-Content -LiteralPath $HistoryPath -Raw -Encoding UTF8 | ConvertFrom-Json
$ExpectedCards = [int]$State.season.expectedCardCount
$ExpectedDaily = [int]$State.season.expectedDailyItems

if ($ExpectedCards -lt 1 -or @($State.activities).Count -ne $ExpectedCards) { throw 'Card count is not driven by current season state.' }
if ($ExpectedDaily -lt 1 -or @($State.activities | Where-Object { $_.kind -match 'Daily' }).Count -ne 1) { throw 'Current season must contain exactly one Daily card.' }
$seasonEndAt = [DateTimeOffset]::Parse(
    [string]$State.season.endAt,
    [Globalization.CultureInfo]::InvariantCulture,
    [Globalization.DateTimeStyles]::AssumeLocal
)
if ($seasonEndAt -le [DateTimeOffset]::Now) { throw 'Stored season has already ended; do not roll over without live Playlist confirmation.' }
if ($History.schemaVersion -ne 1 -or @($History.snapshots).Count -lt 2) { throw 'Metrics history needs at least two verified snapshots before a trend can be rendered.' }
if (-not $Project.steamGuide.enabled -or -not $Project.analytics.enabled) { throw 'Steam guide and public analytics must stay enabled for rollover readiness.' }

$MissingAssets = [System.Collections.Generic.List[string]]::new()
$VisualQueue = [System.Collections.Generic.List[string]]::new()
foreach ($Activity in @($State.activities)) {
    $Visual = $Activity.visual
    $VisualIsUnresolved = [string]$Activity.completeness.visual -in @('missing','preliminary')
    if ($VisualIsUnresolved -and ([string]::IsNullOrWhiteSpace([string]$Visual.image) -or [string]::IsNullOrWhiteSpace([string]$Visual.sourceImage))) {
        $VisualQueue.Add([string]$Activity.id)
        continue
    }
    foreach ($Name in @([string]$Visual.image, [string]$Visual.sourceImage)) {
        if ([string]::IsNullOrWhiteSpace($Name) -or -not (Test-Path -LiteralPath (Join-Path $RepoRoot (Join-Path $State.season.assetsDirectory $Name)))) {
            $MissingAssets.Add("$($Activity.id):$Name")
        }
    }
    if ($VisualIsUnresolved) { $VisualQueue.Add([string]$Activity.id) }
}
if ($MissingAssets.Count -gt 0) { throw "Current-season visual asset check failed: $($MissingAssets -join '; ')" }

$null = & (Join-Path $PSScriptRoot 'render_steam_guide.ps1')
$SteamRendered = $?
if (-not $SteamRendered) { throw 'Steam mirror renderer failed during rollover preflight.' }
$SteamOutputPath = Join-Path $RepoRoot 'reports\steam-guide-current.txt'
Require-File $SteamOutputPath 'Generated Steam subsection'
$SteamCharacters = ((Get-Content -LiteralPath $SteamOutputPath -Raw -Encoding UTF8) -replace "`r`n", "`n").Length
if ($SteamCharacters -gt 4800) { throw 'Steam subsection is not safely below the 4800-character ceiling.' }

$Payload = [ordered]@{
    schemaVersion = 1
    checkedAt = [DateTimeOffset]::Now.ToString('o')
    status = 'READY'
    series = "Series $($State.season.seriesNumber) $($State.season.seriesName)"
    currentSeasonEndAt = [string]$State.season.endAt
    expectedCardCount = $ExpectedCards
    expectedDailyItems = $ExpectedDaily
    steamCharacters = $SteamCharacters
    metricSnapshots = @($History.snapshots).Count
    unresolvedVisuals = @($VisualQueue)
}
$OutputDirectory = Split-Path -Parent $OutputPath
if (-not (Test-Path -LiteralPath $OutputDirectory)) { New-Item -ItemType Directory -Path $OutputDirectory | Out-Null }
[IO.File]::WriteAllText($OutputPath, ($Payload | ConvertTo-Json -Depth 8) + "`r`n", [Text.UTF8Encoding]::new($false))

Write-Host 'SEASON_PREFLIGHT=READY'
Write-Host "SEASON_PREFLIGHT_CARDS=$ExpectedCards"
Write-Host "SEASON_PREFLIGHT_DAILY=$ExpectedDaily"
Write-Host "SEASON_PREFLIGHT_STEAM_CHARACTERS=$SteamCharacters"
Write-Host "SEASON_PREFLIGHT_METRIC_SNAPSHOTS=$(@($History.snapshots).Count)"
if ($VisualQueue.Count -gt 0) { Write-Host "SEASON_PREFLIGHT_UNRESOLVED_VISUALS=$($VisualQueue -join ',')" }
