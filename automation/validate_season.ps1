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
$ProjectConfigPath = Join-Path $RepoRoot 'data\project.json'
$errors = [Collections.Generic.List[string]]::new()
$warnings = [Collections.Generic.List[string]]::new()

function Add-ValidationError([string]$Message) { $errors.Add($Message) }
function Add-ValidationWarning([string]$Message) { $warnings.Add($Message) }
function Get-FullProjectPath([string]$RelativePath) { [IO.Path]::GetFullPath((Join-Path $RepoRoot $RelativePath)) }

try {
    $state = Get-Content -LiteralPath $StatePath -Raw -Encoding UTF8 | ConvertFrom-Json -DateKind String
}
catch {
    Add-ValidationError "Cannot parse season state: $($_.Exception.Message)"
    $state = $null
}

try {
    $project = Get-Content -LiteralPath $ProjectConfigPath -Raw -Encoding UTF8 | ConvertFrom-Json -DateKind String
}
catch {
    Add-ValidationError "Cannot parse project config: $($_.Exception.Message)"
    $project = $null
}

$branding = $null
$support = $null
$analytics = $null
$requiredSources = @()
if ($project) {
    if ($project.schemaVersion -ne 1) { Add-ValidationError 'project schemaVersion must be 1' }
    $branding = $project.branding
    foreach ($name in @('faviconPng','appleTouchIcon','themeColor')) {
        if ($null -eq $branding.$name -or [string]::IsNullOrWhiteSpace([string]$branding.$name)) { Add-ValidationError "project.branding.$name is required" }
    }
    if ([string]$branding.themeColor -notmatch '^#[0-9A-Fa-f]{6}$') { Add-ValidationError 'project.branding.themeColor must be a six-digit hex color' }
    $projectAssetsRoot = Get-FullProjectPath 'reports/assets/project'
    foreach ($assetName in @('faviconPng','appleTouchIcon')) {
        if (-not [string]::IsNullOrWhiteSpace([string]$branding.$assetName)) {
            if ([string]$branding.$assetName -notmatch '^reports/assets/project/[^/]+\.(svg|png)$') { Add-ValidationError "project.branding.$assetName must be a direct SVG or PNG file under reports/assets/project/" }
            $brandingAssetPath = Get-FullProjectPath ([string]$branding.$assetName)
            if (-not $brandingAssetPath.StartsWith($projectAssetsRoot, [StringComparison]::OrdinalIgnoreCase)) { Add-ValidationError "project.branding.$assetName must stay under reports/assets/project/" }
            elseif (-not (Test-Path -LiteralPath $brandingAssetPath)) { Add-ValidationError "project.branding.$assetName is missing: $brandingAssetPath" }
        }
    }
    $support = $project.support
    if ($support.enabled -ne $true) { Add-ValidationError 'project support block must remain enabled' }
    foreach ($name in @('title','description','url','buttonLabel','qrAsset','buttonAsset')) {
        if ($null -eq $support.$name -or [string]::IsNullOrWhiteSpace([string]$support.$name)) { Add-ValidationError "project.support.$name is required" }
    }
    if ([string]$support.url -notmatch '^https://www\.sberbank\.com/') { Add-ValidationError 'project.support.url must use the configured Sberbank HTTPS host' }
    foreach ($assetName in @('qrAsset','buttonAsset')) {
        if (-not [string]::IsNullOrWhiteSpace([string]$support.$assetName)) {
            $supportAssetPath = Get-FullProjectPath ([string]$support.$assetName)
            if (-not $supportAssetPath.StartsWith($projectAssetsRoot, [StringComparison]::OrdinalIgnoreCase)) { Add-ValidationError "project.support.$assetName must stay under reports/assets/project/" }
            elseif (-not (Test-Path -LiteralPath $supportAssetPath)) { Add-ValidationError "project.support.$assetName is missing: $supportAssetPath" }
        }
    }
    $analytics = $project.analytics
    if ($analytics.enabled -ne $true) { Add-ValidationError 'project analytics must remain enabled' }
    foreach ($name in @('provider','title','description','counterImageUrl','dashboardUrl')) {
        if ($null -eq $analytics.$name -or [string]::IsNullOrWhiteSpace([string]$analytics.$name)) { Add-ValidationError "project.analytics.$name is required" }
    }
    if ([string]$analytics.provider -ne 'hits.sh') { Add-ValidationError 'project.analytics.provider must be hits.sh' }
    if ([string]$analytics.counterImageUrl -notmatch '^https://hits\.sh/.+\.svg(?:\?.*)?$') { Add-ValidationError 'project.analytics.counterImageUrl must be a hits.sh HTTPS SVG URL' }
    if ([string]$analytics.dashboardUrl -notmatch '^https://hits\.sh/.+/$') { Add-ValidationError 'project.analytics.dashboardUrl must be a hits.sh HTTPS dashboard URL' }
    $notifications = $project.notifications
    if ($notifications.enabled -ne $true) { Add-ValidationError 'project notifications must remain enabled' }
    if ([string]$notifications.provider -ne 'home-assistant') { Add-ValidationError 'project.notifications.provider must be home-assistant' }
    if ([string]::IsNullOrWhiteSpace([string]$notifications.localConfigPath)) { Add-ValidationError 'project.notifications.localConfigPath is required' }
    else {
        $notificationConfigPath = Get-FullProjectPath ([string]$notifications.localConfigPath)
        $notificationRunsRoot = Get-FullProjectPath 'automation/runs'
        if (-not $notificationConfigPath.StartsWith($notificationRunsRoot, [StringComparison]::OrdinalIgnoreCase)) { Add-ValidationError 'project.notifications.localConfigPath must stay under ignored automation/runs/' }
        elseif (-not (Test-Path -LiteralPath $notificationConfigPath)) { Add-ValidationError 'Home Assistant notification local config is missing' }
    }
    foreach ($messageName in @('updateRequired','upToDate','checkBlocked')) {
        foreach ($fieldName in @('title','message')) {
            if ([string]::IsNullOrWhiteSpace([string]$notifications.messages.$messageName.$fieldName)) { Add-ValidationError "project.notifications.messages.$messageName.$fieldName is required" }
        }
    }
    foreach ($scriptName in @('send_home_assistant_notification.ps1','mark_steam_guide_published.ps1','check_steam_guide.ps1')) {
        if (-not (Test-Path -LiteralPath (Join-Path $PSScriptRoot $scriptName))) { Add-ValidationError "Notification/publication script is missing: $scriptName" }
    }
    $publicationStatePath = Get-FullProjectPath 'automation/runs/steam-publication-state.json'
    if (-not (Test-Path -LiteralPath $publicationStatePath)) { Add-ValidationWarning 'Verified Steam publication fingerprint is missing; next checker run will require confirmation' }
    $requiredSources = @($project.requiredSources)
    $mandatorySourceIds = @('fandom_series_category','fandom_current','forza_playlist','forza_news','forza_support_release_notes','forza_support_known_issues','forza_forums_official','reddit_forzahorizon','reddit_forzahorizon6','reddit_forza','reddit_forzatune','forza_horizon_hub','forza_labs_collector','forza_labs_map','escorenews_fh6','dungg_playlist')
    $configuredSourceIds = @($requiredSources | ForEach-Object { [string]$_.id })
    if ($requiredSources.Count -lt $mandatorySourceIds.Count) { Add-ValidationError "project.requiredSources must contain at least $($mandatorySourceIds.Count) entries" }
    if (@($configuredSourceIds | Sort-Object -Unique).Count -ne $configuredSourceIds.Count) { Add-ValidationError 'project.requiredSources ids must be unique' }
    foreach ($sourceId in $mandatorySourceIds) {
        if ($configuredSourceIds -notcontains $sourceId) { Add-ValidationError "project.requiredSources is missing mandatory source: $sourceId" }
    }
    foreach ($source in $requiredSources) {
        foreach ($name in @('id','label','url','purpose')) {
            if ([string]::IsNullOrWhiteSpace([string]$source.$name)) { Add-ValidationError "project.requiredSources contains an empty $name" }
        }
        if ([string]$source.url -notmatch '^https://') { Add-ValidationError "project.requiredSources URL must use HTTPS: $($source.id)" }
    }
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
    $piPattern = '(?<![A-Za-z0-9])(?:S1|S2|[DCBARX])\s*[0-9]{3}(?![0-9])'
    $expectedPiBadges = 0
    foreach ($activity in $activities) {
        foreach ($fieldName in @('conditionHtml','howHtml','tuneHtml')) {
            $expectedPiBadges += ([regex]::Matches([string]$activity.$fieldName, $piPattern, 'IgnoreCase')).Count
        }
    }
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
        foreach ($contentField in @('conditionHtml','howHtml','tuneHtml')) {
            if ([string]$card.$contentField -match '<a\b') { Add-ValidationError "$($card.id).$contentField contains a link; move it to sourceHtml" }
        }
        foreach ($linkMatch in [regex]::Matches([string]$card.sourceHtml, '<a\b[^>]*>', 'IgnoreCase')) {
            if ($linkMatch.Value -notmatch 'target\s*=\s*["'']_blank["'']') { Add-ValidationError "$($card.id).sourceHtml has a link without target=_blank" }
            if ($linkMatch.Value -notmatch 'rel\s*=\s*["''][^"'']*noopener[^"'']*noreferrer[^"'']*["'']') { Add-ValidationError "$($card.id).sourceHtml has a link without rel=noopener noreferrer" }
        }
        if ([string]$card.tuneHtml -match '<b\b') { Add-ValidationError "$($card.id).tuneHtml contains bold attribution; publish codes without tuner names" }
        $vehicleAndTuneHtml = ([string]$card.conditionHtml) + ' ' + ([string]$card.tuneHtml)
        foreach ($codeMatch in [regex]::Matches($vehicleAndTuneHtml, '<code>[0-9]{3} [0-9]{3} [0-9]{3}</code>')) {
            $prefixStart = [Math]::Max(0, $codeMatch.Index - 140)
            $codePrefix = $vehicleAndTuneHtml.Substring($prefixStart, $codeMatch.Index - $prefixStart)
            if ($codePrefix -notmatch '(?:19|20)[0-9]{2}') { Add-ValidationError "$($card.id) has a tune code without a nearby four-digit vehicle year: $($codeMatch.Value)" }
            if ($codePrefix -match '<b>[^<]+</b>\s*,?\s*$') { Add-ValidationError "$($card.id) exposes a tuner name before $($codeMatch.Value)" }
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
        $readmePath = Join-Path $RepoRoot 'README.md'
        foreach ($path in @($archivePath, $artifactPath, $htmlPath, $currentWeekPath, $readmePath)) {
            if (-not (Test-Path -LiteralPath $path)) { Add-ValidationError "Generated output is missing: $path" }
        }

        if (Test-Path -LiteralPath $artifactPath) {
            $artifact = Get-Content -LiteralPath $artifactPath -Raw -Encoding UTF8 | ConvertFrom-Json -DateKind String
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
            foreach ($cardBlock in [regex]::Matches($html, '<section class="activity-block"[\s\S]*?</section>', 'IgnoreCase')) {
                foreach ($linkMatch in [regex]::Matches($cardBlock.Value, '<a\b[^>]*>', 'IgnoreCase')) {
                    if ($linkMatch.Value -notmatch 'target\s*=\s*["'']_blank["'']') { Add-ValidationError 'Public HTML contains an activity-card link that does not open in a new tab' }
                    if ($linkMatch.Value -notmatch 'rel\s*=\s*["''][^"'']*noopener[^"'']*noreferrer[^"'']*["'']') { Add-ValidationError 'Public HTML contains an unsafe activity-card external link' }
                }
            }
            $actualPiBadges = ([regex]::Matches($html, 'class="pi-badge pi-(?:d|c|b|a|s1|s2|r|x)"')).Count
            if ($actualPiBadges -ne $expectedPiBadges) { Add-ValidationError "Public HTML contains $actualPiBadges PI badges, expected $expectedPiBadges from season state" }
            foreach ($forbidden in @('Проверка полноты','Общие ловушки','Что ещё требует проверки','Ограничения источников')) {
                if ($html.Contains($forbidden)) { Add-ValidationError "Public HTML contains forbidden section: $forbidden" }
            }
            foreach ($match in [regex]::Matches($html, 'src="(assets/[^"]+)"')) {
                $assetPath = Join-Path (Join-Path $RepoRoot 'reports') ($match.Groups[1].Value -replace '/', '\')
                if (-not (Test-Path -LiteralPath $assetPath)) { Add-ValidationError "Public HTML references missing asset: $($match.Groups[1].Value)" }
            }
            if ($project -and $branding) {
                $faviconPngSrc = ([string]$branding.faviconPng) -replace '^reports/', ''
                $appleTouchIconSrc = ([string]$branding.appleTouchIcon) -replace '^reports/', ''
                foreach ($expectedAsset in @($faviconPngSrc,$appleTouchIconSrc)) {
                    if (-not $html.Contains($expectedAsset)) { Add-ValidationError "Public HTML is missing branding asset: $expectedAsset" }
                }
                if (([regex]::Matches($html, '<link rel="icon"')).Count -ne 1) { Add-ValidationError 'Public HTML must contain exactly one PNG favicon link' }
                if (([regex]::Matches($html, '<link rel="apple-touch-icon"')).Count -ne 1) { Add-ValidationError 'Public HTML must contain exactly one Apple Touch Icon link' }
                if (-not $html.Contains("<meta name=`"theme-color`" content=`"$($branding.themeColor)`">")) { Add-ValidationError 'Public HTML theme-color differs from project config' }
            }
            if ($support) {
                $supportQrSrc = ([string]$support.qrAsset) -replace '^reports/', ''
                if (([regex]::Matches($html, 'data-support-block')).Count -ne 1) { Add-ValidationError 'Public HTML must contain exactly one support block' }
                if (-not $html.Contains([string]$support.title)) { Add-ValidationError 'Public HTML support title differs from project config' }
                if (-not $html.Contains([string]$support.url)) { Add-ValidationError 'Public HTML support URL differs from project config' }
                if (-not $html.Contains($supportQrSrc)) { Add-ValidationError 'Public HTML support QR differs from project config' }
                $supportIndex = $html.IndexOf('data-support-block', [StringComparison]::Ordinal)
                $lastCardIndex = $html.LastIndexOf('data-activity-block', [StringComparison]::Ordinal)
                if ($supportIndex -lt $lastCardIndex) { Add-ValidationError 'Public HTML support block must follow all activity cards' }
            }
            if ($analytics) {
                if (([regex]::Matches($html, 'data-visit-stats')).Count -ne 1) { Add-ValidationError 'Public HTML must contain exactly one visit statistics block' }
                if (-not $html.Contains([string]$analytics.title)) { Add-ValidationError 'Public HTML visit statistics title differs from project config' }
                $counterImageUrlHtml = [Net.WebUtility]::HtmlEncode([string]$analytics.counterImageUrl)
                $dashboardUrlHtml = [Net.WebUtility]::HtmlEncode([string]$analytics.dashboardUrl)
                if (-not $html.Contains($counterImageUrlHtml)) { Add-ValidationError 'Public HTML visit counter URL differs from project config' }
                if (-not $html.Contains($dashboardUrlHtml)) { Add-ValidationError 'Public HTML visit dashboard URL differs from project config' }
                if (-not $html.Contains("img-src 'self' https://hits.sh")) { Add-ValidationError 'Public HTML CSP must allow only the configured external counter image host' }
                $analyticsIndex = $html.IndexOf('data-visit-stats', [StringComparison]::Ordinal)
                $supportIndex = $html.IndexOf('data-support-block', [StringComparison]::Ordinal)
                if ($analyticsIndex -lt $supportIndex) { Add-ValidationError 'Public HTML visit statistics must stay inside the final support block' }
            }
        }

        if (Test-Path -LiteralPath $currentWeekPath) {
            $currentWeek = Get-Content -LiteralPath $currentWeekPath -Raw -Encoding UTF8
            if (-not $currentWeek.Contains(($season.archiveFile -replace '\\','/'))) { Add-ValidationError 'CURRENT_WEEK.md does not point to archiveFile' }
        }

        if ($support -and (Test-Path -LiteralPath $readmePath)) {
            $readme = Get-Content -LiteralPath $readmePath -Raw -Encoding UTF8
            $headingPattern = '(?m)^## ' + [regex]::Escape([string]$support.title) + '\s*$'
            if (([regex]::Matches($readme, $headingPattern)).Count -ne 1) { Add-ValidationError 'README must contain exactly one configured support heading' }
            foreach ($expected in @([string]$support.url, [string]$support.qrAsset, [string]$support.buttonAsset)) {
                if (-not $readme.Contains($expected)) { Add-ValidationError "README support block is missing: $expected" }
            }
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
