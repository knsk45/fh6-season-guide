param(
    [string]$StatePath
)

$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
if (-not $StatePath) {
    $StatePath = Join-Path $projectRoot 'data\current-season.json'
}
$StatePath = [IO.Path]::GetFullPath($StatePath)
$artifactPath = Join-Path $PSScriptRoot 'artifact.json'

if (-not (Test-Path -LiteralPath $StatePath)) {
    throw "Season state was not found: $StatePath"
}

$state = Get-Content -LiteralPath $StatePath -Raw -Encoding UTF8 | ConvertFrom-Json
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

function Get-AssetDataUri([string]$FileName) {
    $path = Join-Path $assetRoot $FileName
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

function New-CardHtml($card) {
    $visual = $card.visual
    if (-not $visual -or -not $visual.image -or -not $visual.icon) {
        throw "No visual mapping for $($card.id)"
    }
    $cardImage = Get-AssetDataUri $visual.image
    $cardIcon = Get-AssetDataUri $visual.icon
    $imagePosition = if ($visual.position) { $visual.position } else { '50% 50%' }
    $imageSourceUrl = if ($visual.sourceUrl) { $visual.sourceUrl } else { $season.fandomUrl }
    $imageSourceLabel = if ($visual.sourceLabel) { $visual.sourceLabel } else { 'изображение и иконка: Forza Wiki' }
    $seasonAlt = "Series $($season.seriesNumber) $($season.seasonDisplay)"
    $conditionHtml = Add-PerformanceIndexBadges ([string]$card.conditionHtml)
    $howHtml = Add-PerformanceIndexBadges ([string]$card.howHtml)
    $tuneHtml = Add-PerformanceIndexBadges ([string]$card.tuneHtml)
    @"
<style>
  :root{color-scheme:dark}*{box-sizing:border-box}body{margin:0;background:#071014;color:#eef6f5;font-family:Inter,Segoe UI,Arial,sans-serif}.card{overflow:hidden;border:1px solid #29434b;border-radius:18px;background:linear-gradient(145deg,#111c21,#081014);box-shadow:0 18px 40px #0008}.wrap{display:grid;grid-template-columns:230px 1fr;gap:0}.visual{position:relative;width:190px;height:190px;align-self:start;margin:20px;background:#111;overflow:hidden;border-radius:14px}.visual>img{display:block;width:190px;height:190px;object-fit:cover;object-position:center;filter:saturate(.96) contrast(1.04) brightness(.78)}.visual:after{content:'';position:absolute;inset:0;background:linear-gradient(180deg,transparent 38%,#061014dd)}.activity-icon{position:absolute;z-index:2;left:16px;top:16px;display:grid;place-items:center;width:56px;height:56px;border:3px solid #d9ff00;border-radius:14px;background:#142329;box-shadow:0 8px 24px #0008,inset 0 0 0 1px #ffffff1f}.activity-icon img{position:relative;z-index:1;width:40px;height:40px;object-fit:contain;filter:drop-shadow(0 1px 2px #000)}.number{position:absolute;z-index:2;left:16px;bottom:14px;font-weight:900;font-size:36px;letter-spacing:-1px}.content{padding:20px 24px 20px 0}.eyebrow{display:flex;gap:10px;align-items:center;flex-wrap:wrap;color:#b8ccd1;font-size:12px;font-weight:800;text-transform:uppercase;letter-spacing:.08em}.points{border-radius:999px;background:#e4007f;color:white;padding:5px 9px;letter-spacing:0;text-transform:none}h2{margin:7px 0 13px;font-size:26px;line-height:1.05;color:#fff}p{margin:9px 0;line-height:1.48}.label{color:#d9ff00;font-weight:800}.tune{padding:10px 12px;border-left:3px solid #d9ff00;background:#0e2025;border-radius:0 9px 9px 0}code{white-space:nowrap;background:#1d3238;border:1px solid #36515a;border-radius:6px;padding:2px 6px;color:#fff}.sources{margin-top:14px;padding-top:10px;border-top:1px solid #29434b;color:#8ea8ae;font-size:12px}.sources a{color:#9fd7ff}.days{margin:8px 0;padding-left:20px}.days li{margin:7px 0;line-height:1.42}@media(max-width:650px){.wrap{grid-template-columns:1fr}.visual{width:170px;height:170px;margin:18px auto 0}.visual>img{width:170px;height:170px}.content{padding:18px}h2{font-size:23px}}
  .pi-badge{--pi-color:#5d6871;display:inline-grid;grid-template-columns:auto auto;align-items:stretch;min-width:62px;height:1.2em;margin:0 .12em;overflow:hidden;border:1px solid #ffffff40;border-radius:3px;background:#f3f6f7;color:#0a1013;font-size:.82em;font-weight:950;line-height:1;vertical-align:.02em;box-shadow:0 2px 6px #0007;transform:skew(-7deg)}.pi-badge>span{display:grid;place-items:center;transform:skew(7deg)}.pi-class{min-width:26px;padding:0 5px;background:var(--pi-color);color:#fff;text-shadow:0 1px 2px #0009}.pi-score{min-width:34px;padding:0 6px;font-variant-numeric:tabular-nums}.pi-d{--pi-color:#626b72}.pi-c{--pi-color:#b49b25}.pi-b{--pi-color:#df6b20}.pi-a{--pi-color:#d52e59}.pi-s1{--pi-color:#ad2ea9}.pi-s2{--pi-color:#3b65d9}.pi-r{--pi-color:#009c9b}.pi-x{--pi-color:#171c20}
</style>
<article class="card">
  <div class="wrap">
    <div class="visual"><img src="$cardImage" data-local-src="$assetWebRoot/$($visual.image)" loading="lazy" decoding="async" style="object-position:$imagePosition" alt="Игровая карточка $($card.title) из $seasonAlt"><span class="activity-icon"><img src="$cardIcon" data-local-src="$assetWebRoot/$($visual.icon)" loading="lazy" decoding="async" alt="Иконка $($card.kind)"></span><span class="number">$($card.number)</span></div>
    <div class="content">
      <div class="eyebrow"><span>$($card.kind)</span><span class="points">$($card.points)</span></div>
      <h2>$($card.title)</h2>
      <p><span class="label">Условие:</span> $conditionHtml</p>
      <p><span class="label">Как выполнить:</span> $howHtml</p>
      <p class="tune"><span class="label">Автомобиль и тюнинг:</span> $tuneHtml</p>
      <div class="sources">$($card.sourceHtml) · <a href='$imageSourceUrl'>$imageSourceLabel</a></div>
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

$artifact = [ordered]@{
    surface = 'dashboard'
    manifest = [ordered]@{
        version = 1
        surface = 'dashboard'
        title = $season.reportTitle
        description = "Сезон действует до $($season.endAt)"
        generatedAt = $generatedAt.ToString('o')
        blocks = @($blocks)
        charts = @()
        sources = @()
    }
    snapshot = [ordered]@{
        version = 1
        status = if (@($state.openItems).Count -eq 0) { 'ready' } else { 'partial' }
        generatedAt = $generatedAt.ToString('o')
        datasets = [ordered]@{}
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
[IO.File]::WriteAllText($artifactPath, $json, [Text.UTF8Encoding]::new($false))
Write-Output "Wrote $artifactPath from data/current-season.json with $($blocks.Count) activity blocks"
