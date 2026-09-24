[CmdletBinding()]
param(
    [string]$StatePath,
    [string]$OutputPath
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
if (-not $StatePath) { $StatePath = Join-Path $RepoRoot 'data\current-season.json' }
if (-not $OutputPath) { $OutputPath = Join-Path $RepoRoot 'automation\runs\visual-evidence-queue.json' }

$State = Get-Content -LiteralPath $StatePath -Raw -Encoding UTF8 | ConvertFrom-Json
$AssetRoot = Join-Path $RepoRoot ([string]$State.season.assetsDirectory)
$Queue = [System.Collections.Generic.List[object]]::new()

foreach ($Activity in @($State.activities)) {
    # Daily is intentionally a text-only aggregate and never needs a public tile.
    if ([string]$Activity.kind -eq 'daily') { continue }
    $Visual = $Activity.visual
    $Image = [string]$Visual.image
    $SourceImage = [string]$Visual.sourceImage
    $HasPreparedTile = -not [string]::IsNullOrWhiteSpace($Image) -and (Test-Path -LiteralPath (Join-Path $AssetRoot $Image))
    $HasOriginalEvidence = -not [string]::IsNullOrWhiteSpace($SourceImage) -and (Test-Path -LiteralPath (Join-Path $AssetRoot $SourceImage))
    $Completeness = [string]$Activity.completeness.visual
    $Reason = $null
    if ($Completeness -in @('missing','preliminary')) {
        $Reason = 'The state marks this visual as unresolved.'
    }
    elseif (-not $HasPreparedTile -or -not $HasOriginalEvidence) {
        $Reason = 'The prepared exact tile or the original evidence file is missing.'
    }
    if ($Reason) {
        $Queue.Add([ordered]@{
            activityId = [string]$Activity.id
            number = [string]$Activity.number
            title = [string]$Activity.title
            orientation = [string]$Visual.orientation
            reason = $Reason
            request = 'Need an unedited in-game screenshot with the full tile visible. Save it as sourceImage and crop only the tile boundary without retouching.'
            status = 'screenshot_required'
        })
    }
}

$Payload = [ordered]@{
    schemaVersion = 1
    checkedAt = [DateTimeOffset]::Now.ToString('o')
    series = "Series $($State.season.seriesNumber) $($State.season.seasonDisplay)"
    checkedCards = @($State.activities).Count
    screenshotsRequired = @($Queue).Count
    items = @($Queue)
}
$Directory = Split-Path -Parent $OutputPath
if (-not (Test-Path -LiteralPath $Directory)) { New-Item -ItemType Directory -Path $Directory | Out-Null }
[IO.File]::WriteAllText($OutputPath, ($Payload | ConvertTo-Json -Depth 10) + "`r`n", [Text.UTF8Encoding]::new($false))

if ($Queue.Count -eq 0) {
    Write-Host 'VISUAL_QUEUE_STATUS=READY'
}
else {
    Write-Host 'VISUAL_QUEUE_STATUS=SCREENSHOTS_REQUIRED'
    Write-Host "VISUAL_QUEUE_ITEMS=$($Queue.activityId -join ',')"
}
Write-Host "VISUAL_QUEUE_PATH=$OutputPath"
