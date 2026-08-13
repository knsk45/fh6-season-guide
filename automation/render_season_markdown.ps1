[CmdletBinding()]
param(
    [string]$StatePath
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
if (-not $StatePath) { $StatePath = Join-Path $RepoRoot 'data\current-season.json' }
$StatePath = [IO.Path]::GetFullPath($StatePath)
$state = Get-Content -LiteralPath $StatePath -Raw -Encoding UTF8 | ConvertFrom-Json
$season = $state.season

$archivePath = [IO.Path]::GetFullPath((Join-Path $RepoRoot $season.archiveFile))
$seasonRoot = [IO.Path]::GetFullPath((Join-Path $RepoRoot 'seasons'))
if (-not $archivePath.StartsWith($seasonRoot, [StringComparison]::OrdinalIgnoreCase)) {
    throw "archiveFile must stay inside seasons/: $archivePath"
}

$start = [DateTimeOffset]::Parse($season.startAt)
$end = [DateTimeOffset]::Parse($season.endAt)
$updated = [DateTimeOffset]::Parse($state.lastContentUpdate)
$status = if (@($state.openItems).Count -eq 0) { 'подтверждено' } else { "предварительно; открытых полей: $(@($state.openItems).Count)" }

$lines = [Collections.Generic.List[string]]::new()
$lines.Add("# $($season.reportTitle)")
$lines.Add('')
$lines.Add("> Статус: $status")
$lines.Add("> Период: $($start.ToString('dd.MM.yyyy HH:mm')) — $($end.ToString('dd.MM.yyyy HH:mm')) (Asia/Krasnoyarsk)")
$lines.Add("> Обновлено: $($updated.ToString('dd.MM.yyyy HH:mm'))")
$lines.Add("> В отчёте: $($season.expectedCardCount) карточек; Daily объединены в одну карточку.")
$lines.Add('')

foreach ($card in @($state.activities)) {
    $lines.Add("## $($card.number). $($card.kind) — $($card.title) · $($card.points)")
    $lines.Add('')
    $lines.Add("- **Условие:** $($card.conditionHtml)")
    $lines.Add("- **Как выполнить:** $($card.howHtml)")
    $lines.Add("- **Автомобиль и тюнинг:** $($card.tuneHtml)")
    $lines.Add("- **Источники:** $($card.sourceHtml) · <a href='$($card.visual.sourceUrl)' target='_blank' rel='noopener noreferrer'>$($card.visual.sourceLabel)</a>")
    $lines.Add('')
}

$archiveText = ($lines -join "`n").TrimEnd() + "`n"
[IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName($archivePath)) | Out-Null
[IO.File]::WriteAllText($archivePath, $archiveText, [Text.UTF8Encoding]::new($false))

$archiveWebPath = $season.archiveFile -replace '\\', '/'
$currentWeek = @"
# Текущая неделя

Актуальная сводка: [$($season.reportTitle)]($archiveWebPath).

Интерактивная автономная версия: [reports/current-week.html](reports/current-week.html).

Дедлайн: **$($end.ToString('dd MMMM yyyy, HH:mm', [Globalization.CultureInfo]::GetCultureInfo('ru-RU'))) Asia/Krasnoyarsk**.
"@
[IO.File]::WriteAllText((Join-Path $RepoRoot 'CURRENT_WEEK.md'), $currentWeek.TrimEnd() + "`n", [Text.UTF8Encoding]::new($false))

Write-Output "Rendered $($season.archiveFile) and CURRENT_WEEK.md from data/current-season.json"
