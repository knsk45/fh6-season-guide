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
    $Visual = $Activity.visual
    $Image = [string]$Visual.image
    $SourceImage = [string]$Visual.sourceImage
    $HasPreparedTile = -not [string]::IsNullOrWhiteSpace($Image) -and (Test-Path -LiteralPath (Join-Path $AssetRoot $Image))
    $HasOriginalEvidence = -not [string]::IsNullOrWhiteSpace($SourceImage) -and (Test-Path -LiteralPath (Join-Path $AssetRoot $SourceImage))
    $ExactTileClaim = [string]$Visual.sourceLabel -match 'Точная игровая плитка|пользовательск.*скриншот.*точн'
    $Completeness = [string]$Activity.completeness.visual

    $Reason = $null
    if ($Completeness -in @('missing','preliminary')) {
        $Reason = 'В state уже указан незавершённый визуал.'
    }
    elseif (-not $HasPreparedTile -or -not $HasOriginalEvidence) {
        $Reason = 'Нет подготовленной точной плитки или сохранённого исходного доказательства.'
    }
    elseif (-not $ExactTileClaim) {
        $Reason = 'Источник не подтверждает, что файл является точной внутриигровой плиткой текущей недели.'
    }

    if ($Reason) {
        $Queue.Add([ordered]@{
            activityId = [string]$Activity.id
            number = [string]$Activity.number
            title = [string]$Activity.title
            orientation = [string]$Visual.orientation
            reason = $Reason
            request = 'Нужен неизменённый игровой скриншот с полностью видимой плиткой. Оригинал будет сохранён как sourceImage, затем из него без ретуши вырежется только граница плитки.'
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
