[CmdletBinding()]
param(
    [string]$StatePath,
    [switch]$SkipOutputs,
    [switch]$AsJson
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
if (-not $StatePath) { $StatePath = Join-Path $RepoRoot 'data\current-season.json' }
$StatePath = [IO.Path]::GetFullPath($StatePath)
$errors = [Collections.Generic.List[string]]::new()
$warnings = [Collections.Generic.List[string]]::new()

function Add-ValidationError([string]$Message) { $errors.Add($Message) }
function Add-ValidationWarning([string]$Message) { $warnings.Add($Message) }
function Get-FullProjectPath([string]$RelativePath) { [IO.Path]::GetFullPath((Join-Path $RepoRoot $RelativePath)) }

try {
    $state = Get-Content -LiteralPath $StatePath -Raw -Encoding UTF8 | ConvertFrom-Json
}
catch {
    Add-ValidationError "Cannot parse season state: $($_.Exception.Message)"
    $state = $null
}

if ($state) {
    if ($state.schemaVersion -ne 1) { Add-ValidationError "schemaVersion must be 1" }
    $season = $state.season
    $activities = @($state.activities)
    $openItems = @($state.openItems)
    $allowedCompleteness = @('confirmed', 'community', 'preliminary', 'missing', 'not_applicable')
    $allowedMissingFields = @('condition', 'solution', 'vehicleTune', 'visual')

    foreach ($name in @('seriesNumber','seriesSlug','seriesName','season','seasonDisplay','startAt','endAt','reportTitle','archiveFile','assetsDirectory','fandomUrl','officialPlaylistUrl','expectedCardCount','expectedDailyItems','maxPublicHtmlBytes')) {
        if ($null -eq $season.$name -or [string]::IsNullOrWhiteSpace([string]$season.$name)) { Add-ValidationError "season.$name is required" }
    }

    try { $startAt = [DateTimeOffset]::Parse($season.startAt) } catch { Add-ValidationError 'season.startAt is not a valid timestamp'; $startAt = $null }
    try { $endAt = [DateTimeOffset]::Parse($season.endAt) } catch { Add-ValidationError 'season.endAt is not a valid timestamp'; $endAt = $null }
    try { $contentAt = [DateTimeOffset]::Parse($state.lastContentUpdate) } catch { Add-ValidationError 'lastContentUpdate is not a valid timestamp'; $contentAt = $null }
    if ($startAt -and $endAt -and $endAt -le $startAt) { Add-ValidationError 'season.endAt must be later than startAt' }
    if ($endAt -and [DateTimeOffset]::Now -gt $endAt) { Add-ValidationWarning 'Stored season deadline has passed; confirm whether a rollover is due' }

    $archivePath = Get-FullProjectPath $season.archiveFile
    $seasonRoot = Get-FullProjectPath 'seasons'
    if (-not $archivePath.StartsWith($seasonRoot, [StringComparison]::OrdinalIgnoreCase)) { Add-ValidationError 'archiveFile must stay under seasons/' }
    $assetRoot = Get-FullProjectPath $season.assetsDirectory
    $reportsAssetsRoot = Get-FullProjectPath 'reports/assets'
    if (-not $assetRoot.StartsWith($reportsAssetsRoot, [StringComparison]::OrdinalIgnoreCase)) { Add-ValidationError 'assetsDirectory must stay under reports/assets/' }

    $expectedCount = [int]$season.expectedCardCount
    if ($activities.Count -ne $expectedCount) { Add-ValidationError "Expected $expectedCount activities, found $($activities.Count)" }
    $ids = @($activities | ForEach-Object { $_.id })
    if (@($ids | Sort-Object -Unique).Count -ne $ids.Count) { Add-ValidationError 'Activity ids must be unique' }

    $openKeys = @{}
    foreach ($item in $openItems) {
        $key = "$($item.activityId)|$($item.field)"
        if ($openKeys.ContainsKey($key)) { Add-ValidationError "Duplicate openItems entry: $key" } else { $openKeys[$key] = $true }
        if ($ids -notcontains $item.activityId) { Add-ValidationError "openItems references unknown activity: $($item.activityId)" }
        if ($allowedMissingFields -notcontains $item.field) { Add-ValidationError "Invalid openItems field: $($item.field)" }
        foreach ($required in @('reason','nextCheck','status')) {
            if ([string]::IsNullOrWhiteSpace([string]$item.$required)) { Add-ValidationError "openItems $key has empty $required" }
        }
    }

    for ($i = 0; $i -lt $activities.Count; $i++) {
        $card = $activities[$i]
        $expectedNumber = '{0:D2}' -f ($i + 1)
        if ($card.number -ne $expectedNumber) { Add-ValidationError "$($card.id) has number $($card.number), expected $expectedNumber" }
        if ($card.id -notmatch '^activity_[0-9]{2}_[a-z0-9_]+$') { Add-ValidationError "Invalid activity id: $($card.id)" }
        foreach ($required in @('kind','title','points','sourceHtml')) {
            if ([string]::IsNullOrWhiteSpace([string]$card.$required)) { Add-ValidationError "$($card.id).$required is empty" }
        }

        $missing = @($card.missingFields)
        foreach ($field in $missing) {
            if ($allowedMissingFields -notcontains $field) { Add-ValidationError "$($card.id) has invalid missing field $field" }
            if (-not $openKeys.ContainsKey("$($card.id)|$field")) { Add-ValidationError "$($card.id).$field is missing but has no openItems entry" }
        }
        foreach ($field in $allowedMissingFields) {
            $status = [string]$card.completeness.$field
            if ($allowedCompleteness -notcontains $status) { Add-ValidationError "$($card.id).completeness.$field has invalid status '$status'" }
            if ($status -in @('missing','preliminary') -and $missing -notcontains $field) { Add-ValidationError "$($card.id).$field is $status but absent from missingFields" }
        }

        $fieldValues = @{
            condition = [string]$card.conditionHtml
            solution = [string]$card.howHtml
            vehicleTune = [string]$card.tuneHtml
        }
        foreach ($field in $fieldValues.Keys) {
            if ([string]::IsNullOrWhiteSpace($fieldValues[$field]) -and $missing -notcontains $field) { Add-ValidationError "$($card.id).$field is empty without missingFields" }
        }
        if ([string]::IsNullOrWhiteSpace([string]$card.visual.image) -or [string]::IsNullOrWhiteSpace([string]$card.visual.icon)) {
            if ($missing -notcontains 'visual') { Add-ValidationError "$($card.id).visual is empty without missingFields" }
        }
        else {
            foreach ($asset in @($card.visual.image, $card.visual.icon)) {
                $assetPath = Join-Path $assetRoot $asset
                if (-not (Test-Path -LiteralPath $assetPath)) { Add-ValidationError "$($card.id) references missing asset: $assetPath" }
            }
        }
    }

    foreach ($card in $activities) {
        foreach ($field in @($card.missingFields)) {
            if (-not $openKeys.ContainsKey("$($card.id)|$field")) { Add-ValidationError "Missing open item for $($card.id)|$field" }
        }
    }

    $dailyCards = @($activities | Where-Object { $_.kind -match 'Daily' })
    if ($dailyCards.Count -ne 1) { Add-ValidationError "Expected one Daily card, found $($dailyCards.Count)" }
    elseif (([regex]::Matches([string]$dailyCards[0].conditionHtml, '<li\b', 'IgnoreCase')).Count -ne [int]$season.expectedDailyItems) {
        Add-ValidationError "Daily card must contain $($season.expectedDailyItems) list items"
    }

    if (-not $SkipOutputs) {
        $artifactPath = Join-Path $RepoRoot 'reports\artifact.json'
        $htmlPath = Join-Path $RepoRoot 'reports\current-week.html'
        $currentWeekPath = Join-Path $RepoRoot 'CURRENT_WEEK.md'
        foreach ($path in @($archivePath, $artifactPath, $htmlPath, $currentWeekPath)) {
            if (-not (Test-Path -LiteralPath $path)) { Add-ValidationError "Generated output is missing: $path" }
        }

        if (Test-Path -LiteralPath $artifactPath) {
            $artifact = Get-Content -LiteralPath $artifactPath -Raw -Encoding UTF8 | ConvertFrom-Json
            $artifactBlocks = @($artifact.manifest.blocks)
            if ($artifact.manifest.title -ne $season.reportTitle) { Add-ValidationError 'artifact title does not match season state' }
            if ($artifactBlocks.Count -ne $expectedCount) { Add-ValidationError "artifact contains $($artifactBlocks.Count) blocks, expected $expectedCount" }
            if (($artifactBlocks.id -join '|') -ne ($ids -join '|')) { Add-ValidationError 'artifact block order differs from season state' }
            if ([DateTimeOffset]::Parse($artifact.snapshot.generatedAt) -ne $contentAt) { Add-ValidationError 'artifact generatedAt differs from lastContentUpdate' }
        }

        if (Test-Path -LiteralPath $htmlPath) {
            $html = Get-Content -LiteralPath $htmlPath -Raw -Encoding UTF8
            $htmlBytes = (Get-Item -LiteralPath $htmlPath).Length
            if ($htmlBytes -gt [int]$season.maxPublicHtmlBytes) { Add-ValidationError "Public HTML is too large: $htmlBytes bytes" }
            if ($html -match '<iframe|data:image/|data-analytics-portable-reader') { Add-ValidationError 'Public HTML contains a heavy or embedded runtime' }
            $htmlIds = @([regex]::Matches($html, '<section class="activity-block" id="([^"]+)" data-activity-block>') | ForEach-Object { $_.Groups[1].Value })
            if (($htmlIds -join '|') -ne ($ids -join '|')) { Add-ValidationError 'Public HTML card order differs from season state' }
            foreach ($forbidden in @('Проверка полноты','Общие ловушки','Что ещё требует проверки','Ограничения источников')) {
                if ($html.Contains($forbidden)) { Add-ValidationError "Public HTML contains forbidden section: $forbidden" }
            }
            foreach ($match in [regex]::Matches($html, 'src="(assets/[^"]+)"')) {
                $assetPath = Join-Path (Join-Path $RepoRoot 'reports') ($match.Groups[1].Value -replace '/', '\')
                if (-not (Test-Path -LiteralPath $assetPath)) { Add-ValidationError "Public HTML references missing asset: $($match.Groups[1].Value)" }
            }
        }

        if (Test-Path -LiteralPath $currentWeekPath) {
            $currentWeek = Get-Content -LiteralPath $currentWeekPath -Raw -Encoding UTF8
            if (-not $currentWeek.Contains(($season.archiveFile -replace '\\','/'))) { Add-ValidationError 'CURRENT_WEEK.md does not point to archiveFile' }
        }
    }
}

$result = [ordered]@{
    ok = ($errors.Count -eq 0)
    state = $StatePath
    cards = if ($state) { @($state.activities).Count } else { 0 }
    openItems = if ($state) { @($state.openItems).Count } else { 0 }
    errors = @($errors)
    warnings = @($warnings)
}

if ($AsJson) {
    $result | ConvertTo-Json -Depth 10
}
else {
    foreach ($warning in $warnings) { Write-Warning $warning }
    foreach ($errorMessage in $errors) { Write-Error $errorMessage -ErrorAction Continue }
    if ($errors.Count -eq 0) {
        Write-Output "STRUCTURE_OK cards=$($result.cards) open_items=$($result.openItems)"
    }
    else {
        Write-Output "STRUCTURE_FAILED errors=$($errors.Count)"
    }
}

if ($errors.Count -gt 0) { exit 1 }

