[CmdletBinding()]
param(
    [string]$StatePath,
    [string]$ProjectPath,
    [string]$GuidePath,
    [string]$PublicationStatePath
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
if (-not $StatePath) { $StatePath = Join-Path $RepoRoot 'data\current-season.json' }
if (-not $ProjectPath) { $ProjectPath = Join-Path $RepoRoot 'data\project.json' }
if (-not $GuidePath) { $GuidePath = Join-Path $RepoRoot 'reports\steam-guide-current.txt' }
if (-not $PublicationStatePath) { $PublicationStatePath = Join-Path $RepoRoot 'automation\runs\steam-publication-state.json' }

function Get-SubstantiveSteamHash {
    param([Parameter(Mandatory = $true)][string]$Path)

    $Text = Get-Content -LiteralPath $Path -Raw -Encoding UTF8
    # Compatibility with the former daily timestamp line: time alone is not a Steam edit.
    $Text = [regex]::Replace($Text, '(?m)^\[b\]Последняя проверка данных:\[/b\][^\r\n]*(\r?\n)?', '')
    $Text = $Text -replace "`r`n", "`n"
    $Bytes = [Text.Encoding]::UTF8.GetBytes($Text.Trim())
    $Hasher = [Security.Cryptography.SHA256]::Create()
    try { return ([BitConverter]::ToString($Hasher.ComputeHash($Bytes))).Replace('-', '').ToLowerInvariant() }
    finally { $Hasher.Dispose() }
}

function ConvertFrom-CardHtml {
    param([AllowEmptyString()][string]$Value)

    if ([string]::IsNullOrWhiteSpace($Value)) { return '' }
    $Text = [regex]::Replace($Value, '(?i)<li[^>]*>', ' ')
    $Text = [regex]::Replace($Text, '(?i)</?(ol|ul|li|strong|em|code)[^>]*>', ' ')
    $Text = [regex]::Replace($Text, '(?i)<br\s*/?>', ' ')
    $Text = [regex]::Replace($Text, '<[^>]+>', ' ')
    return [Net.WebUtility]::HtmlDecode($Text)
}

function Normalize-Text {
    param([AllowEmptyString()][string]$Value)

    if ([string]::IsNullOrWhiteSpace($Value)) { return '' }
    $Text = [Net.WebUtility]::HtmlDecode($Value)
    $Text = [regex]::Replace($Text, '(?i)<(br|/div|/p|/li|/h[1-6])[^>]*>', ' ')
    $Text = [regex]::Replace($Text, '<[^>]+>', ' ')
    $Text = $Text -replace '[•·]', ' '
    return ([regex]::Replace($Text, '\s+', ' ')).Trim()
}

$State = Get-Content -LiteralPath $StatePath -Raw -Encoding UTF8 | ConvertFrom-Json
$Project = Get-Content -LiteralPath $ProjectPath -Raw -Encoding UTF8 | ConvertFrom-Json
$Steam = $Project.steamGuide

if (-not $Steam.enabled) {
    Write-Host 'STEAM_STATUS=DISABLED'
    exit 0
}
if (-not (Test-Path -LiteralPath $GuidePath)) { throw "Steam mirror not found: $GuidePath" }

$DesiredHash = Get-SubstantiveSteamHash -Path $GuidePath
$PublishedHash = ''
if (Test-Path -LiteralPath $PublicationStatePath) {
    try {
        $PublicationState = Get-Content -LiteralPath $PublicationStatePath -Raw -Encoding UTF8 | ConvertFrom-Json
        $PublishedHash = [string]$PublicationState.contentHash
    }
    catch { Write-Verbose "Publication state is unreadable: $($_.Exception.Message)" }
}

if ([string]::IsNullOrWhiteSpace($PublishedHash) -or $PublishedHash -ne $DesiredHash) {
    Write-Host 'STEAM_STATUS=UPDATE_REQUIRED'
    if ([string]::IsNullOrWhiteSpace($PublishedHash)) {
        Write-Host 'STEAM_REASON=verified publication baseline is missing'
    }
    else {
        Write-Host 'STEAM_REASON=substantive Steam content differs from the last verified publication'
    }
    Write-Host "STEAM_CONTENT_HASH=$DesiredHash"
    Write-Host "STEAM_GUIDE_URL=$($Steam.url)"
    exit 0
}

$Response = $null
$FetchError = ''
try {
    $Response = Invoke-WebRequest -UseBasicParsing -Uri ([string]$Steam.url) -TimeoutSec 30
}
catch { $FetchError = $_.Exception.Message }

if (-not $Response -or $Response.StatusCode -ne 200 -or $Response.RawContentLength -le 0) {
    Write-Host 'STEAM_STATUS=UP_TO_DATE'
    Write-Host 'STEAM_VERIFICATION=LOCAL_VERIFIED_BASELINE'
    Write-Host "STEAM_WARNING=public endpoint unavailable: $FetchError"
    Write-Host "STEAM_CONTENT_HASH=$DesiredHash"
    Write-Host "STEAM_GUIDE_URL=$($Steam.url)"
    exit 0
}

$Html = [Net.WebUtility]::HtmlDecode([string]$Response.Content)
if (-not $Html.Contains([string]$Steam.title)) {
    Write-Host 'STEAM_STATUS=UP_TO_DATE'
    Write-Host 'STEAM_VERIFICATION=LOCAL_VERIFIED_BASELINE'
    Write-Host 'STEAM_WARNING=Steam returned a non-guide page; substantive content is unchanged since the last verified publication'
    Write-Host "STEAM_CONTENT_HASH=$DesiredHash"
    Write-Host "STEAM_GUIDE_URL=$($Steam.url)"
    exit 0
}

$VisibleText = Normalize-Text $Html
$Reasons = [Collections.Generic.List[string]]::new()

function Require-PublicText {
    param(
        [Parameter(Mandatory = $true)][string]$Label,
        [Parameter(Mandatory = $true)][string]$Value
    )
    $Expected = Normalize-Text $Value
    if ($Expected -and -not $VisibleText.Contains($Expected)) { $Reasons.Add("missing $Label") }
}

Require-PublicText 'guide title' ([string]$Steam.title)
Require-PublicText 'current section title' ([string]$Steam.sectionTitle)
Require-PublicText 'series name' ([string]$State.season.seriesName)
Require-PublicText 'season display' ([string]$State.season.seasonDisplay)
Require-PublicText 'daily freshness link note' ([string]$Steam.freshnessNote)

foreach ($Activity in $State.activities) {
    Require-PublicText "activity $($Activity.number) title" ([string]$Activity.title)
    Require-PublicText "activity $($Activity.number) condition" (ConvertFrom-CardHtml ([string]$Activity.conditionHtml))
    Require-PublicText "activity $($Activity.number) tune" (ConvertFrom-CardHtml ([string]$Activity.tuneHtml))
}

$RenderedCardCount = ([regex]::Matches($Html, '<div class="bb_h2">')).Count
if ($RenderedCardCount -ne [int]$State.season.expectedCardCount) {
    $Reasons.Add("rendered card count $RenderedCardCount, expected $($State.season.expectedCardCount)")
}

$EncodedGuidePath = 'fh6-season-guide%2Freports%2Fcurrent-week.html'
if (-not $Html.Contains([string]$Steam.publicGuideUrl) -and -not $Html.Contains($EncodedGuidePath)) {
    $Reasons.Add('missing public guide link')
}
if (-not [regex]::IsMatch($Html, '<meta property="og:image" content="https://images\.steamusercontent\.com/')) {
    $Reasons.Add('missing Steam cover image')
}
foreach ($Tag in @($Steam.tags)) {
    $EncodedTag = [Uri]::EscapeDataString([string]$Tag).Replace('%20', '+')
    if (-not $Html.Contains("requiredtags%5B%5D=$EncodedTag")) { $Reasons.Add("missing tag $Tag") }
}

if ($Reasons.Count -eq 0) {
    Write-Host 'STEAM_STATUS=UP_TO_DATE'
    Write-Host 'STEAM_VERIFICATION=PUBLIC_AND_LOCAL'
    Write-Host "STEAM_GUIDE_URL=$($Steam.url)"
    Write-Host "STEAM_CARDS=$RenderedCardCount"
    Write-Host "STEAM_CONTENT_HASH=$DesiredHash"
    exit 0
}

Write-Host 'STEAM_STATUS=UPDATE_REQUIRED'
foreach ($Reason in $Reasons) { Write-Host "STEAM_REASON=$Reason" }
Write-Host "STEAM_CONTENT_HASH=$DesiredHash"
Write-Host "STEAM_GUIDE_URL=$($Steam.url)"
exit 0
