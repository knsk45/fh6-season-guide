[CmdletBinding()]
param(
    [string]$StatePath,
    [string]$ProjectPath
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

if (-not $StatePath) { $StatePath = Join-Path $PSScriptRoot '..\data\current-season.json' }
if (-not $ProjectPath) { $ProjectPath = Join-Path $PSScriptRoot '..\data\project.json' }

$State = Get-Content -LiteralPath $StatePath -Raw -Encoding UTF8 | ConvertFrom-Json
$Project = Get-Content -LiteralPath $ProjectPath -Raw -Encoding UTF8 | ConvertFrom-Json
$Steam = $Project.steamGuide

if (-not $Steam.enabled) {
    Write-Host 'STEAM_STATUS=DISABLED'
    exit 0
}

try {
    $Response = Invoke-WebRequest -UseBasicParsing -Uri ([string]$Steam.url) -TimeoutSec 30
}
catch {
    Write-Host 'STEAM_STATUS=CHECK_FAILED'
    Write-Host "STEAM_ERROR=$($_.Exception.Message)"
    exit 2
}

if ($Response.StatusCode -ne 200 -or $Response.RawContentLength -le 0) {
    Write-Host 'STEAM_STATUS=CHECK_FAILED'
    Write-Host "STEAM_ERROR=HTTP $($Response.StatusCode) or empty response"
    exit 2
}

$Html = [Net.WebUtility]::HtmlDecode([string]$Response.Content)
$Reasons = [Collections.Generic.List[string]]::new()

function Require-Text {
    param(
        [Parameter(Mandatory = $true)][string]$Label,
        [Parameter(Mandatory = $true)][string]$Value
    )

    if (-not $Html.Contains($Value)) {
        $Reasons.Add("missing $Label")
    }
}

Require-Text 'guide title' ([string]$Steam.title)
Require-Text 'current section title' ([string]$Steam.sectionTitle)
Require-Text 'series name' ([string]$State.season.seriesName)
Require-Text 'season display' ([string]$State.season.seasonDisplay)

$CheckedAt = [DateTimeOffset]::Parse([string]$State.lastContentUpdate).ToString('dd.MM.yyyy HH:mm')
Require-Text 'last successful audit time' $CheckedAt

foreach ($Activity in $State.activities) {
    Require-Text "activity $($Activity.number) title" ([string]$Activity.title)
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
    if (-not $Html.Contains("requiredtags%5B%5D=$EncodedTag")) {
        $Reasons.Add("missing tag $Tag")
    }
}

if ($Reasons.Count -eq 0) {
    Write-Host 'STEAM_STATUS=UP_TO_DATE'
    Write-Host "STEAM_GUIDE_URL=$($Steam.url)"
    Write-Host "STEAM_CARDS=$RenderedCardCount"
    exit 0
}

Write-Host 'STEAM_STATUS=UPDATE_REQUIRED'
foreach ($Reason in $Reasons) {
    Write-Host "STEAM_REASON=$Reason"
}
Write-Host "STEAM_GUIDE_URL=$($Steam.url)"
exit 0
