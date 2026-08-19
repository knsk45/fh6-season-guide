[CmdletBinding()]
param(
    [string]$StatePath,
    [string]$Timestamp
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
if (-not $StatePath) {
    $StatePath = Join-Path $RepoRoot 'data\current-season.json'
}
$StatePath = [IO.Path]::GetFullPath($StatePath)

$KrasnoyarskTimeZone = [TimeZoneInfo]::FindSystemTimeZoneById('North Asia Standard Time')
if ($Timestamp) {
    $parsedTimestamp = [DateTimeOffset]::Parse($Timestamp, [Globalization.CultureInfo]::InvariantCulture)
    $verifiedAt = [TimeZoneInfo]::ConvertTime($parsedTimestamp, $KrasnoyarskTimeZone)
}
else {
    $verifiedAt = [TimeZoneInfo]::ConvertTime([DateTimeOffset]::UtcNow, $KrasnoyarskTimeZone)
}
$formattedTimestamp = $verifiedAt.ToString("yyyy-MM-dd'T'HH:mm:sszzz", [Globalization.CultureInfo]::InvariantCulture)

$rawState = [IO.File]::ReadAllText($StatePath, [Text.Encoding]::UTF8)
$null = $rawState | ConvertFrom-Json

$pattern = '(?m)("lastContentUpdate"\s*:\s*")[^"]*(")'
$matches = [Text.RegularExpressions.Regex]::Matches($rawState, $pattern)
if ($matches.Count -ne 1) {
    throw "Expected exactly one lastContentUpdate field in $StatePath; found $($matches.Count)."
}

$updatedState = [Text.RegularExpressions.Regex]::Replace(
    $rawState,
    $pattern,
    ('${1}' + $formattedTimestamp + '${2}'),
    1
)
$null = $updatedState | ConvertFrom-Json

$tempPath = Join-Path ([IO.Path]::GetDirectoryName($StatePath)) ('.current-season-' + [Guid]::NewGuid().ToString('N') + '.tmp')
try {
    [IO.File]::WriteAllText($tempPath, $updatedState, [Text.UTF8Encoding]::new($false))
    Move-Item -LiteralPath $tempPath -Destination $StatePath -Force
}
finally {
    if (Test-Path -LiteralPath $tempPath) {
        Remove-Item -LiteralPath $tempPath -Force
    }
}

Write-Output "LAST_CONTENT_UPDATE=$formattedTimestamp"
