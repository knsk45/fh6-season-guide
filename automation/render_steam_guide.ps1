[CmdletBinding()]
param(
    [string]$StatePath,
    [string]$ProjectPath,
    [string]$OutputPath
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

if (-not $StatePath) { $StatePath = Join-Path $PSScriptRoot '..\data\current-season.json' }
if (-not $ProjectPath) { $ProjectPath = Join-Path $PSScriptRoot '..\data\project.json' }
if (-not $OutputPath) { $OutputPath = Join-Path $PSScriptRoot '..\reports\steam-guide-current.txt' }

function ConvertFrom-CardHtml {
    param([AllowEmptyString()][string]$Html)

    if ([string]::IsNullOrWhiteSpace($Html)) { return '' }

    $Text = $Html
    $Text = [regex]::Replace($Text, '(?i)<li[^>]*>', "`n• ")
    $Text = [regex]::Replace($Text, '(?i)</li>', '')
    $Text = [regex]::Replace($Text, '(?i)</(ol|ul)>', "`n")
    $Text = [regex]::Replace($Text, '(?i)<br\s*/?>', "`n")
    $Text = [regex]::Replace($Text, '(?i)<(ol|ul)[^>]*>', '')
    $Text = [regex]::Replace($Text, '(?i)</?(strong|em|code)[^>]*>', '')
    $Text = [regex]::Replace($Text, '<[^>]+>', '')
    $Text = [Net.WebUtility]::HtmlDecode($Text)
    $Text = $Text -replace '\s*\([^)]*в игре проектом не проверен[^)]*\)', ' (совет сообщества)'
    $Text = [regex]::Replace($Text, '[ \t]+', ' ')
    $Text = [regex]::Replace($Text, "(`r?`n){3,}", "`r`n`r`n")
    return $Text.Trim()
}

$State = Get-Content -LiteralPath $StatePath -Raw -Encoding UTF8 | ConvertFrom-Json
$Project = Get-Content -LiteralPath $ProjectPath -Raw -Encoding UTF8 | ConvertFrom-Json

if (-not $Project.steamGuide.enabled) {
    throw 'Steam guide output is disabled in data/project.json.'
}

$Season = $State.season
$GuideUrl = [string]$Project.steamGuide.publicGuideUrl
if ($State.activities.Count -ne [int]$Season.expectedCardCount) {
    throw "Steam output card count mismatch: $($State.activities.Count), expected $($Season.expectedCardCount)."
}
$Deadline = [DateTimeOffset]::Parse([string]$Season.endAt).ToString('dd.MM.yyyy HH:mm')
$CheckedAt = [DateTimeOffset]::Parse([string]$State.lastContentUpdate).ToString('dd.MM.yyyy HH:mm')
$Lines = [Collections.Generic.List[string]]::new()

$Lines.Add('[h1]РУССКОЯЗЫЧНАЯ ЕЖЕНЕДЕЛЬНАЯ СВОДКА FH6[/h1]')
$Lines.Add('[b]Руководство обновляется регулярно: после смены сезона и затем ежедневно по мере появления решений, карт и актуальных кодов тюнингов.[/b]')
$Lines.Add('')
$Lines.Add('[quote]Полная версия с изображениями карточек, прямыми ссылками на карты и источники, живым таймером и всеми уточнениями:')
$Lines.Add("[url=$GuideUrl][b]ОТКРЫТЬ АКТУАЛЬНУЮ СВОДКУ FESTIVAL PLAYLIST[/b][/url][/quote]")
$Lines.Add('')
$Lines.Add("[h1]Series $($Season.seriesNumber) «$($Season.seriesName)» — $($Season.seasonDisplay)[/h1]")
$Lines.Add("[b]Сезон активен до:[/b] $Deadline (Красноярск)")
$Lines.Add("[b]Последняя проверка данных:[/b] $CheckedAt (Красноярск)")
$Lines.Add("[b]Активностей в текущей неделе:[/b] $($Season.expectedCardCount)")

foreach ($Activity in $State.activities) {
    $Lines.Add('')
    $Lines.Add("[h2]$($Activity.number). $($Activity.kind) — $($Activity.title) · $($Activity.points)[/h2]")

    $Condition = ConvertFrom-CardHtml ([string]$Activity.conditionHtml)
    $Tune = ConvertFrom-CardHtml ([string]$Activity.tuneHtml)

    if ($Condition) {
        $Lines.Add('[b]Условие:[/b]')
        $Lines.Add($Condition)
    }
    if ($Tune) {
        $Lines.Add('[b]Автомобиль / тюнинг:[/b]')
        $Lines.Add($Tune)
    }
}

$Lines.Add('')
$Lines.Add('[h1]Всегда актуальная версия[/h1]')
$Lines.Add('Steam-страница содержит компактный список всех активностей недели. Пошаговые способы прохождения, карты, скриншоты, изображения карточек, источники и последующие исправления публикуются в основной русскоязычной сводке:')
$Lines.Add("[url=$GuideUrl][b]ОТКРЫТЬ ЕЖЕНЕДЕЛЬНУЮ СВОДКУ FH6[/b][/url]")
$Lines.Add('')
$Lines.Add('[b]Добавьте это руководство Steam в избранное:[/b] оно обновляется вместе со сменой Festival Playlist.')

$OutputDirectory = Split-Path -Parent $OutputPath
if (-not (Test-Path -LiteralPath $OutputDirectory)) {
    New-Item -ItemType Directory -Path $OutputDirectory | Out-Null
}
[IO.File]::WriteAllText($OutputPath, ($Lines -join "`r`n") + "`r`n", [Text.UTF8Encoding]::new($false))

Write-Host "STEAM_GUIDE_OUTPUT=$OutputPath"
Write-Host "STEAM_GUIDE_CARDS=$($State.activities.Count)"
