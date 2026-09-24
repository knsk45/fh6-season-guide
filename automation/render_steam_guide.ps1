[CmdletBinding()]
param(
    [string]$StatePath,
    [string]$ProjectPath,
    [string]$OutputPath,
    [ValidateSet('ru','en')]
    [string]$Language = 'ru'
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'json_compat.ps1')

if (-not $StatePath) { $StatePath = Join-Path $PSScriptRoot '..\data\current-season.json' }
if (-not $ProjectPath) { $ProjectPath = Join-Path $PSScriptRoot '..\data\project.json' }

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

$State = ConvertFrom-Fh6Json -Json (Get-Content -LiteralPath $StatePath -Raw -Encoding UTF8)
$Project = ConvertFrom-Fh6Json -Json (Get-Content -LiteralPath $ProjectPath -Raw -Encoding UTF8)

if (-not $Project.steamGuide.enabled) {
    throw 'Steam guide output is disabled in data/project.json.'
}

$SteamSection = $Project.steamGuide.sections.$Language
if ($null -eq $SteamSection -or [string]::IsNullOrWhiteSpace([string]$SteamSection.title) -or [string]::IsNullOrWhiteSpace([string]$SteamSection.outputPath)) {
    throw "steamGuide.sections.$Language requires title and outputPath."
}
if (-not $OutputPath) { $OutputPath = Join-Path $PSScriptRoot ("..\\" + [string]$SteamSection.outputPath) }
$IsEnglish = $Language -eq 'en'
$Locale = if ($IsEnglish) { $State.locales.en } else { $null }
if ($IsEnglish -and $null -eq $Locale) { throw 'current-season.json is missing locales.en for the English Steam section.' }

$Season = $State.season
$GuideUrl = [string]$Project.steamGuide.publicGuideUrl
if ($State.activities.Count -ne [int]$Season.expectedCardCount) {
    throw "Steam output card count mismatch: $($State.activities.Count), expected $($Season.expectedCardCount)."
}
$Deadline = [DateTimeOffset]::Parse([string]$Season.endAt).ToString('dd.MM.yyyy HH:mm')
$Lines = [Collections.Generic.List[string]]::new()

$Lines.Add($(if ($IsEnglish) { '[h1]FH6 WEEKLY GUIDE — ENGLISH[/h1]' } else { '[h1]РУССКАЯ ЕЖЕНЕДЕЛЬНАЯ СВОДКА FH6[/h1]' }))
$Lines.Add($(if ($IsEnglish) { '[b]Updated after each season change and whenever verified solutions appear.[/b]' } else { '[b]Регулярно обновляется после смены сезона и по мере появления новых решений.[/b]' }))
$Lines.Add('')
$Lines.Add($(if ($IsEnglish) { "[quote][url=$GuideUrl][b]OPEN THE FULL ENGLISH REPORT WITH MAPS AND IMAGES[/b][/url][/quote]" } else { "[quote][url=$GuideUrl][b]ОТКРЫТЬ ПОЛНУЮ АКТУАЛЬНУЮ СВОДКУ С КАРТАМИ И ИЗОБРАЖЕНИЯМИ[/b][/url][/quote]" }))
$Lines.Add('')
$SeasonDisplay = if ($IsEnglish) { [string]$Locale.seasonDisplay } else { [string]$Season.seasonDisplay }
$Lines.Add("[h1]Series $($Season.seriesNumber) '$($Season.seriesName)' — $SeasonDisplay[/h1]")
$Lines.Add($(if ($IsEnglish) { "[b]Ends:[/b] $Deadline (Krasnoyarsk) · [b]Activities:[/b] $($Season.expectedCardCount)" } else { "[b]До:[/b] $Deadline (Красноярск) · [b]Активностей:[/b] $($Season.expectedCardCount)" }))
$Lines.Add($(if ($IsEnglish) { '[b]The full report is checked daily; see the link above for the exact verification time.[/b]' } else { "[b]$($Project.steamGuide.freshnessNote)[/b]" }))
$Lines.Add($(if ($IsEnglish) { '[i]Tune codes come from current community material and have not been tested in-game by this guide author.[/i]' } else { '[i]Коды тюнингов собраны по свежим материалам сообщества и не проверены автором руководства в игре.[/i]' }))
$SteamLocations = [Collections.Generic.List[string]]::new()

foreach ($Activity in $State.activities) {
    $Localized = if ($IsEnglish) { $Locale.activities.($Activity.id) } else { $null }
    if ($IsEnglish -and $null -eq $Localized) { throw "English localization missing for $($Activity.id)." }
    $ActivityTitle = if ($IsEnglish) { [string]$Localized.title } else { [string]$Activity.title }
    $ActivityPoints = if ($IsEnglish) { [string]$Localized.points } else { [string]$Activity.points }
    $ConditionHtml = if ($IsEnglish) { [string]$Localized.conditionHtml } else { [string]$Activity.conditionHtml }
    $TuneHtml = if ($IsEnglish) { [string]$Localized.tuneHtml } else { [string]$Activity.tuneHtml }
    $Lines.Add('')
    $Lines.Add("[h2]$($Activity.number). $($Activity.kind) — $ActivityTitle · $ActivityPoints[/h2]")

    $Condition = ConvertTo-CompactSteamText (ConvertFrom-CardHtml $ConditionHtml)
    $Tune = ConvertTo-CompactSteamText (ConvertFrom-CardHtml $TuneHtml)

    if ($Condition) {
        $Lines.Add($Condition)
    }
    $LocationMatches = [regex]::Matches([string]$Activity.sourceHtml, '(?is)<a\s+href="([^"]+)"[^>]*>([^<]*(?:Локация|Карта|Location|Map)[^<]*)</a>')
    foreach ($LocationMatch in $LocationMatches) {
        $SteamLocations.Add("[url=$($LocationMatch.Groups[1].Value)]$($LocationMatch.Groups[2].Value.Trim())[/url]")
    }
    if ($Tune) {
        $Lines.Add("[b]$(if ($IsEnglish) { 'Car' } else { 'Авто' }):[/b] $Tune")
    }
}

$Lines.Add('')
$Lines.Add($(if ($IsEnglish) { '[h1]Maps, screenshots and updates[/h1]' } else { '[h1]Карты, скриншоты и уточнения[/h1]' }))
$Lines.Add($(if ($IsEnglish) { "[url=$GuideUrl][b]OPEN THE FULL ENGLISH FH6 REPORT[/b][/url]" } else { "[url=$GuideUrl][b]ОТКРЫТЬ ПОЛНУЮ РУССКОЯЗЫЧНУЮ СВОДКУ FH6[/b][/url]" }))
$Lines.Add($(if ($IsEnglish) { '[b]Add this Steam guide to favourites:[/b] it is updated together with the Festival Playlist.' } else { '[b]Добавьте руководство Steam в избранное:[/b] оно регулярно обновляется вместе с Festival Playlist.' }))
if ($SteamLocations.Count -gt 0) {
    $Lines.Add('')
    $Lines.Add($(if ($IsEnglish) { '[h2]Short location links[/h2]' } else { '[h2]Короткие ссылки на локации[/h2]' }))
    foreach ($Location in ($SteamLocations | Select-Object -Unique)) { $Lines.Add($Location) }
}

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

Write-Host "STEAM_GUIDE_LANGUAGE=$Language"
Write-Host "STEAM_GUIDE_OUTPUT=$OutputPath"
Write-Host "STEAM_GUIDE_CARDS=$($State.activities.Count)"
Write-Host "STEAM_GUIDE_CHARACTERS=$SteamCharacterCount"
Write-Host "STEAM_GUIDE_MAX_CHARACTERS=$SteamSafeCharacterLimit"
