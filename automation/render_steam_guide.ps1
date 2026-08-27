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

function ConvertTo-CompactSteamText {
    param([AllowEmptyString()][string]$Text)

    if ([string]::IsNullOrWhiteSpace($Text)) { return '' }

    $Compact = $Text
    $Compact = $Compact -replace '\s*\(свежий код сообщества; не подтверждён в игре\)', ''
    $Compact = $Compact -replace '\s*\(один свежий код сообщества для всех трёх PR Stunts; не подтверждён в игре\)', ''
    $Compact = $Compact -replace '^Специальный автомобиль или тюнинг не нужен\.$', ''
    $Compact = $Compact -replace '^Подойдёт любой Cult Car; тюнинг не требуется\.$', ''
    $Compact = $Compact -replace '^Подойдёт любой автомобиль; тюнинг не требуется\.$', ''
    $Compact = $Compact -replace '^Используйте удобный дрифт-кар; специального сезонного кода не требуется\.$', ''
    $Compact = $Compact -replace '^Выберите универсальную машину из гаража; специальный тюнинг не требуется\.$', ''
    $Compact = [regex]::Replace($Compact, '[ \t]+', ' ')
    return $Compact.Trim()
}

$State = Get-Content -LiteralPath $StatePath -Raw -Encoding UTF8 | ConvertFrom-Json -DateKind String
$Project = Get-Content -LiteralPath $ProjectPath -Raw -Encoding UTF8 | ConvertFrom-Json -DateKind String

if (-not $Project.steamGuide.enabled) {
    throw 'Steam guide output is disabled in data/project.json.'
}

$Season = $State.season
$GuideUrl = [string]$Project.steamGuide.publicGuideUrl
if ($State.activities.Count -ne [int]$Season.expectedCardCount) {
    throw "Steam output card count mismatch: $($State.activities.Count), expected $($Season.expectedCardCount)."
}
$Deadline = [DateTimeOffset]::Parse([string]$Season.endAt).ToString('dd.MM.yyyy HH:mm')
$Lines = [Collections.Generic.List[string]]::new()

$Lines.Add('[h1]РУССКАЯ ЕЖЕНЕДЕЛЬНАЯ СВОДКА FH6[/h1]')
$Lines.Add('[b]Регулярно обновляется после смены сезона и по мере появления новых решений.[/b]')
$Lines.Add('')
$Lines.Add("[quote][url=$GuideUrl][b]ОТКРЫТЬ ПОЛНУЮ АКТУАЛЬНУЮ СВОДКУ С КАРТАМИ И ИЗОБРАЖЕНИЯМИ[/b][/url][/quote]")
$Lines.Add('')
$Lines.Add("[h1]Series $($Season.seriesNumber) «$($Season.seriesName)» — $($Season.seasonDisplay)[/h1]")
$Lines.Add("[b]До:[/b] $Deadline (Красноярск) · [b]Активностей:[/b] $($Season.expectedCardCount)")
$Lines.Add("[b]$($Project.steamGuide.freshnessNote)[/b]")
$Lines.Add('[i]Коды тюнингов собраны по свежим материалам сообщества и не проверены автором руководства в игре.[/i]')

foreach ($Activity in $State.activities) {
    $Lines.Add('')
    $Lines.Add("[h2]$($Activity.number). $($Activity.kind) — $($Activity.title) · $($Activity.points)[/h2]")

    $Condition = ConvertTo-CompactSteamText (ConvertFrom-CardHtml ([string]$Activity.conditionHtml))
    $Tune = ConvertTo-CompactSteamText (ConvertFrom-CardHtml ([string]$Activity.tuneHtml))

    if ($Condition) {
        $Lines.Add($Condition)
    }
    if ($Tune) {
        $Lines.Add("[b]Авто:[/b] $Tune")
    }
}

$Lines.Add('')
$Lines.Add('[h1]Карты, скриншоты и уточнения[/h1]')
$Lines.Add("[url=$GuideUrl][b]ОТКРЫТЬ ПОЛНУЮ РУССКОЯЗЫЧНУЮ СВОДКУ FH6[/b][/url]")
$Lines.Add('[b]Добавьте руководство Steam в избранное:[/b] оно регулярно обновляется вместе с Festival Playlist.')

$OutputDirectory = Split-Path -Parent $OutputPath
if (-not (Test-Path -LiteralPath $OutputDirectory)) {
    New-Item -ItemType Directory -Path $OutputDirectory | Out-Null
}
$RenderedText = ($Lines -join "`r`n") + "`r`n"
$SteamCharacterCount = ($RenderedText -replace "`r`n", "`n").Length
$SteamSafeCharacterLimit = 4800
if ($SteamCharacterCount -gt $SteamSafeCharacterLimit) {
    throw "Steam subsection is too long: $SteamCharacterCount characters; project safe limit is $SteamSafeCharacterLimit. Compact the generated mirror before publication."
}
[IO.File]::WriteAllText($OutputPath, $RenderedText, [Text.UTF8Encoding]::new($false))

Write-Host "STEAM_GUIDE_OUTPUT=$OutputPath"
Write-Host "STEAM_GUIDE_CARDS=$($State.activities.Count)"
Write-Host "STEAM_GUIDE_CHARACTERS=$SteamCharacterCount"
Write-Host "STEAM_GUIDE_MAX_CHARACTERS=$SteamSafeCharacterLimit"
