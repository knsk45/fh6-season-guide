param(
    [string]$StatePath
)

$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
. (Join-Path $projectRoot 'automation\json_compat.ps1')
if (-not $StatePath) {
    $StatePath = Join-Path $projectRoot 'data\current-season.json'
}
$StatePath = [IO.Path]::GetFullPath($StatePath)
$artifactPath = Join-Path $PSScriptRoot 'artifact.json'
$ProjectConfigPath = Join-Path $projectRoot 'data\project.json'

if (-not (Test-Path -LiteralPath $StatePath)) {
    throw "Season state was not found: $StatePath"
}

$state = ConvertFrom-Fh6Json -Json (Get-Content -LiteralPath $StatePath -Raw -Encoding UTF8)
$project = ConvertFrom-Fh6Json -Json (Get-Content -LiteralPath $ProjectConfigPath -Raw -Encoding UTF8)
$season = $state.season
$activities = @($state.activities)
$expectedCardCount = [int]$season.expectedCardCount

if ($state.schemaVersion -ne 1) { throw "Unsupported season state schema: $($state.schemaVersion)" }
if (-not $season.reportTitle -or -not $season.assetsDirectory -or -not $season.endAt) {
    throw 'Season state must contain reportTitle, assetsDirectory and endAt'
}
if ($activities.Count -ne $expectedCardCount) {
    throw "Season state expects $expectedCardCount cards but contains $($activities.Count)"
}
if (@($activities.id | Sort-Object -Unique).Count -ne $activities.Count) {
    throw 'Activity ids must be unique'
}

$generatedAt = [DateTimeOffset]::Parse($state.lastContentUpdate)
$assetRoot = [IO.Path]::GetFullPath((Join-Path $projectRoot $season.assetsDirectory))
$reportsAssetsRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot 'assets'))
if (-not $assetRoot.StartsWith($reportsAssetsRoot, [StringComparison]::OrdinalIgnoreCase)) {
    throw "assetsDirectory must stay inside reports/assets: $assetRoot"
}
$assetWebRoot = (($season.assetsDirectory -replace '\\', '/') -replace '^reports/', '').TrimEnd('/')
$activityIconLibrary = $project.activityIconLibrary
if ($null -eq $activityIconLibrary) { throw 'data/project.json must contain activityIconLibrary' }
$metricsHistoryPath = Join-Path $projectRoot 'data\publication-metrics-history.json'
if (-not (Test-Path -LiteralPath $metricsHistoryPath)) { throw 'Publication metrics history is required for the public trend chart' }
$metricsHistory = ConvertFrom-Fh6Json -Json (Get-Content -LiteralPath $metricsHistoryPath -Raw -Encoding UTF8)
if ($metricsHistory.schemaVersion -ne 1 -or @($metricsHistory.snapshots).Count -lt 2) { throw 'Publication metrics history requires at least two snapshots' }

function Get-ImageDataUri([string]$Path) {
    if (-not (Test-Path -LiteralPath $path)) {
        throw "Missing report asset: $path"
    }
    $extension = [IO.Path]::GetExtension($path).TrimStart('.').ToLowerInvariant()
    $mime = switch ($extension) {
        'jpg' { 'image/jpeg' }
        'jpeg' { 'image/jpeg' }
        'png' { 'image/png' }
        'webp' { 'image/webp' }
        default { throw "Unsupported image type: $path" }
    }
    $base64 = [Convert]::ToBase64String([IO.File]::ReadAllBytes($path))
    return "data:$mime;base64,$base64"
}

function Get-AssetDataUri([string]$FileName) {
    $path = Join-Path $assetRoot $FileName
    return Get-ImageDataUri $path
}

function Get-TypeIconDataUri([string]$TypeIconKey) {
    $property = $activityIconLibrary.PSObject.Properties[$TypeIconKey]
    if ($null -eq $property -or [string]::IsNullOrWhiteSpace([string]$property.Value)) {
        throw "Unknown activity type icon key: $TypeIconKey"
    }
    $relativePath = ([string]$property.Value) -replace '\\', '/'
    if ($relativePath -notmatch '^reports/assets/activity-icons/[A-Za-z0-9._-]+\.png$') {
        throw "Activity type icon must be a direct PNG in reports/assets/activity-icons/: $relativePath"
    }
    $path = [IO.Path]::GetFullPath((Join-Path $projectRoot $relativePath))
    $libraryRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot 'assets\activity-icons'))
    if (-not $path.StartsWith($libraryRoot, [StringComparison]::OrdinalIgnoreCase)) {
        throw "Activity type icon escapes the local library: $relativePath"
    }
    return [ordered]@{ dataUri = (Get-ImageDataUri $path); webPath = ($relativePath -replace '^reports/', '') }
}

function Add-PerformanceIndexBadges([string]$Html) {
    if ([string]::IsNullOrWhiteSpace($Html)) { return $Html }
    $parts = [regex]::Split($Html, '(<[^>]+>)')
    $pattern = '(?<![A-Za-z0-9])(?<class>S1|S2|[DCBARX])\s*(?<score>[0-9]{3})(?![0-9])'
    for ($i = 0; $i -lt $parts.Count; $i++) {
        if ($parts[$i].StartsWith('<')) { continue }
        $parts[$i] = [regex]::Replace($parts[$i], $pattern, {
            param($match)
            $classLabel = $match.Groups['class'].Value.ToUpperInvariant()
            $classKey = $classLabel.ToLowerInvariant()
            $score = $match.Groups['score'].Value
            return "<span class=`"pi-badge pi-$classKey`" title=`"Класс $classLabel, PI $score`"><span class=`"pi-class`">$classLabel</span><span class=`"pi-score`">$score</span></span>"
        }, [Text.RegularExpressions.RegexOptions]::IgnoreCase)
    }
    return ($parts -join '')
}

function Add-ShareCodeControls([string]$Html) {
    if ([string]::IsNullOrWhiteSpace($Html)) { return $Html }
    return [regex]::Replace($Html, '<code>(?<code>[0-9]{3} [0-9]{3} [0-9]{3})</code>', {
        param($match)
        $code = $match.Groups['code'].Value
        return "<span class=`"share-code`"><code>$code</code><button class=`"copy-code`" type=`"button`" data-copy-code=`"$code`" aria-label=`"Копировать код $code`"></button></span>"
    })
}

function Get-ProvenanceMarkup($card) {
    $chips = [System.Collections.Generic.List[string]]::new()
    if ([string]$card.completeness.condition -eq 'confirmed') { $chips.Add('<span class="provenance-chip provenance-official">Условия: Forza</span>') }
    if ([string]$card.completeness.solution -in @('community','preliminary')) { $chips.Add('<span class="provenance-chip provenance-community">Решение: сообщество</span>') }
    if ([string]$card.completeness.vehicleTune -in @('community','preliminary')) { $chips.Add('<span class="provenance-chip provenance-community">Тюнинг: сообщество</span>') }
    if ([string]$card.completeness.visual -in @('missing','preliminary')) { $chips.Add('<span class="provenance-chip provenance-missing">Плитка: нужен скриншот</span>') }
    if ($chips.Count -eq 0) { return '' }
    return "<div class=`"provenance`" data-provenance>$($chips -join '')</div>"
}

function New-CardHtml($card) {
    $visual = $card.visual
    if (-not $visual -or -not $visual.orientation) {
        throw "No visual mapping for $($card.id)"
    }
    $hasTile = -not [string]::IsNullOrWhiteSpace([string]$visual.image) -and -not [string]::IsNullOrWhiteSpace([string]$visual.sourceImage)
    if (-not $hasTile -and [string]$card.completeness.visual -notin @('missing','preliminary')) {
        throw "Missing tile for a completed visual: $($card.id)"
    }
    $cardImage = if ($hasTile) { Get-AssetDataUri $visual.image } else { '' }
    $typeIconMarkup = ''
    if ($null -ne $visual.typeIconKey -and -not [string]::IsNullOrWhiteSpace([string]$visual.typeIconKey)) {
        $typeIcon = Get-TypeIconDataUri ([string]$visual.typeIconKey)
        $typeIconMarkup = "<span class=`"type-icon`" data-type-icon=`"$($visual.typeIconKey)`"><img src=`"$($typeIcon.dataUri)`" data-local-src=`"$($typeIcon.webPath)`" loading=`"lazy`" decoding=`"async`" alt=`"Иконка $($card.kind)`"></span>"
    }
    $imageSourceUrl = if ($visual.sourceUrl) { $visual.sourceUrl } else { $season.fandomUrl }
    $imageSourceLabel = if ($visual.sourceLabel) { $visual.sourceLabel } else { 'изображение и иконка: Forza Wiki' }
    $seasonAlt = "Series $($season.seriesNumber) $($season.seasonDisplay)"
    $conditionHtml = Add-PerformanceIndexBadges ([string]$card.conditionHtml)
    $howHtml = Add-PerformanceIndexBadges ([string]$card.howHtml)
    $tuneHtml = Add-ShareCodeControls (Add-PerformanceIndexBadges ([string]$card.tuneHtml))
    $provenanceMarkup = Get-ProvenanceMarkup $card
    $tileMarkup = if ($hasTile) { "<div class=`"game-tile game-tile-$($visual.orientation)`"><img src=`"$cardImage`" data-local-src=`"$assetWebRoot/$($visual.image)`" loading=`"lazy`" decoding=`"async`" alt=`"Игровая карточка $($card.title) из $seasonAlt`"></div>" } else { '' }
    $cardClass = if ($hasTile) { "card-$($visual.orientation)" } else { 'card-no-tile' }
    @"
<style>
  :root{color-scheme:dark}*{box-sizing:border-box}body{margin:0;background:#071014;color:#eef6f5;font-family:Inter,Segoe UI,Arial,sans-serif}.card{overflow:hidden;border:1px solid #29434b;border-radius:18px;background:linear-gradient(145deg,#111c21,#081014);box-shadow:0 18px 40px #0008}.wrap{display:grid;grid-template-columns:minmax(210px,360px) minmax(0,1fr);gap:0;align-items:start}.card-vertical .wrap{grid-template-columns:minmax(210px,280px) minmax(0,1fr)}.card-vertical .content{padding-left:12px}.card-no-tile .wrap{grid-template-columns:minmax(0,1fr)}.card-no-tile .content{padding-left:24px}.game-tile{align-self:start;margin:20px 0 20px 20px;background:transparent}.game-tile-horizontal{width:min(100%,340px)}.game-tile-vertical{width:min(100%,215px)}.game-tile>img{display:block;width:100%;height:auto;max-height:none;object-fit:contain;filter:none;border-radius:11px}.content{min-width:0;padding:20px 24px 20px 18px}.eyebrow{display:flex;gap:9px;align-items:center;flex-wrap:wrap;color:#b8ccd1;font-size:12px;font-weight:800;text-transform:uppercase;letter-spacing:.08em}.kind-line{display:inline-flex;align-items:center;gap:7px;min-height:24px}.type-icon{display:inline-flex;flex:0 0 24px;width:24px;height:24px;align-items:center;justify-content:center;line-height:1}.type-icon img{display:block;width:24px;height:24px;object-fit:contain;filter:drop-shadow(0 1px 2px #0009)}.points{border-radius:999px;background:#e4007f;color:white;padding:5px 9px;letter-spacing:0;text-transform:none}.number{display:inline-flex;align-items:center;justify-content:center;min-width:31px;height:24px;margin-right:8px;padding:0 6px;border:1px solid #d9ff0070;border-left:3px solid #d9ff00;border-radius:5px;background:#102126;color:#d9ff00;font-variant-numeric:tabular-nums;font-weight:950;font-size:14px;line-height:1;vertical-align:.12em}h2{margin:7px 0 13px;font-size:26px;line-height:1.05;color:#fff}p{margin:9px 0;line-height:1.48}.label{color:#d9ff00;font-weight:800}.tune{padding:10px 12px;border-left:3px solid #d9ff00;background:#0e2025;border-radius:0 9px 9px 0}code{white-space:nowrap;background:#1d3238;border:1px solid #36515a;border-radius:6px;padding:2px 6px;color:#fff}.share-code{display:inline-flex;align-items:baseline;gap:6px}.copy-code,.completion-toggle{appearance:none;border:0;background:transparent;color:#9fd7ff;font:inherit;font-size:12px;font-weight:800;cursor:pointer}.copy-code:after{content:'Копировать'}.copy-code:hover,.copy-code:focus-visible{color:#d9ff00;text-decoration:underline}.completion-toggle{margin-left:10px;padding:3px 7px;border:1px solid #36515a;border-radius:999px;color:#b8ccd1;vertical-align:middle}.completion-toggle:after{content:'Отметить выполненным'}.completion-toggle[aria-pressed=true]{border-color:#d9ff00;color:#d9ff00}.completion-toggle[aria-pressed=true]:after{content:'Выполнено'}.provenance{display:flex;flex-wrap:wrap;gap:6px;margin-top:10px}.provenance-chip{display:inline-flex;padding:3px 7px;border-radius:999px;border:1px solid #36515a;font-size:11px;line-height:1.25}.provenance-official{color:#d9ff00}.provenance-community{color:#9fd7ff}.provenance-missing{color:#ffc36b;border-color:#8a5b2d}.sources{margin-top:14px;padding-top:10px;border-top:1px solid #29434b;color:#8ea8ae;font-size:12px}.sources a{color:#9fd7ff}.days{margin:8px 0;padding-left:20px}.days li{margin:7px 0;line-height:1.42}@media(max-width:650px){.wrap{grid-template-columns:1fr}.card-no-tile .content{padding-left:18px}.game-tile{margin:18px auto 0}.game-tile-horizontal{width:min(100% - 36px,420px)}.game-tile-vertical{width:min(100% - 36px,250px)}.content{padding:18px}h2{font-size:23px}}
  .pi-badge{--pi-color:#5d6871;display:inline-grid;grid-template-columns:auto auto;align-items:stretch;min-width:62px;height:1.2em;margin:0 .12em;overflow:hidden;border:1px solid #ffffff40;border-radius:3px;background:#f3f6f7;color:#0a1013;font-size:.82em;font-weight:950;line-height:1;vertical-align:.02em;box-shadow:0 2px 6px #0007;transform:skew(-7deg)}.pi-badge>span{display:grid;place-items:center;transform:skew(7deg)}.pi-class{min-width:26px;padding:0 5px;background:var(--pi-color);color:#fff;text-shadow:0 1px 2px #0009}.pi-score{min-width:34px;padding:0 6px;font-variant-numeric:tabular-nums}.pi-d{--pi-color:#626b72}.pi-c{--pi-color:#b49b25}.pi-b{--pi-color:#df6b20}.pi-a{--pi-color:#d52e59}.pi-s1{--pi-color:#ad2ea9}.pi-s2{--pi-color:#3b65d9}.pi-r{--pi-color:#009c9b}.pi-x{--pi-color:#171c20}
</style>
<article class="card $cardClass" data-activity-id="$($card.id)">
  <div class="wrap">
    $tileMarkup
    <div class="content">
      <div class="eyebrow"><span class="kind-line">$typeIconMarkup<span>$($card.kind)</span></span><span class="points">$($card.points)</span></div>
      <h2><span class="number">$($card.number)</span>$($card.title)<button class="completion-toggle" type="button" data-completion-toggle aria-pressed="false" aria-label="Отметить активность $($card.number) выполненной"></button></h2>
      <p><span class="label">Условие:</span> $conditionHtml</p>
      <p><span class="label">Как выполнить:</span> $howHtml</p>
      <p class="tune"><span class="label">Автомобиль и тюнинг:</span> $tuneHtml</p>
      <div class="sources">$provenanceMarkup$($card.sourceHtml) · <a href='$imageSourceUrl' target='_blank' rel='noopener noreferrer'>$imageSourceLabel</a></div>
    </div>
  </div>
</article>
"@
}

$blocks = foreach ($card in $activities) {
    [ordered]@{
        id = $card.id
        type = 'html'
        layout = 'full'
        body = New-CardHtml -card $card
    }
}

$metricRows = @($metricsHistory.snapshots | Sort-Object { [DateTimeOffset]::Parse([string]$_.collectedAt) } | Select-Object -Last 30 | ForEach-Object {
    [ordered]@{
        runId = [string]$_.runId
        collectedAt = [string]$_.collectedAt
        steamViews = [long]$_.steamViews
        steamFavorites = [long]$_.steamFavorites
        githubViews = [long]$_.githubViews
    }
})
$metricDataset = [ordered]@{
    title = [string]$metricsHistory.title
    source = $metricsHistory.source
    description = [string]$metricsHistory.description
    rows = $metricRows
}
$metricChart = [ordered]@{
    id = 'publication-history'
    type = 'line'
    title = [string]$metricsHistory.title
    subtitle = 'Последние успешные публичные замеры: Steam — уникальные посетители, GitHub — просмотры сводки.'
    dataset = 'publicationMetrics'
    x = 'collectedAt'
    series = @('steamViews','githubViews')
    palette = [ordered]@{ steamViews = '#ff2f92'; githubViews = '#d9ff00' }
}

$artifact = [ordered]@{
    surface = 'dashboard'
    manifest = [ordered]@{
        version = 1
        surface = 'dashboard'
        title = $season.reportTitle
        description = "Сезон действует до $($season.endAt)"
        generatedAt = $generatedAt.ToString('o')
        blocks = @($blocks)
        charts = @($metricChart)
        sources = @()
    }
    snapshot = [ordered]@{
        version = 1
        status = if (@($state.openItems).Count -eq 0) { 'ready' } else { 'partial' }
        generatedAt = $generatedAt.ToString('o')
        datasets = [ordered]@{ publicationMetrics = $metricDataset }
        accessIssues = @($state.openItems)
    }
    sources = @()
    package_info = [ordered]@{
        generated_at = $generatedAt.ToString('o')
        workflow = 'fh6-season-maintainer'
        state_file = 'data/current-season.json'
    }
}

$json = $artifact | ConvertTo-Json -Depth 100
# A report consumer can keep the old JSON memory-mapped on Windows.  Replace it
# atomically so a transient reader never turns a valid artifact into a truncated
# file, and retry the Windows sharing violation without touching the old copy.
$artifactTempPath = "$artifactPath.$PID.tmp"
[IO.File]::WriteAllText($artifactTempPath, $json, [Text.UTF8Encoding]::new($false))
$artifactWritten = $false
for ($attempt = 0; $attempt -lt 12; $attempt++) {
    try {
        [IO.File]::Move($artifactTempPath, $artifactPath, $true)
        $artifactWritten = $true
        break
    }
    catch [IO.IOException] {
        if ($attempt -eq 11) { throw }
        Start-Sleep -Milliseconds ([Math]::Min(100 * ($attempt + 1), 500))
    }
}
if (-not $artifactWritten) { throw 'Artifact replacement did not complete.' }
Write-Output "Wrote $artifactPath from data/current-season.json with $($blocks.Count) activity blocks"
