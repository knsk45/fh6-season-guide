[CmdletBinding()]
param(
    [string]$ProjectPath,
    [string]$OutputPath
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
if (-not $ProjectPath) { $ProjectPath = Join-Path $RepoRoot 'data\project.json' }
if (-not $OutputPath) { $OutputPath = Join-Path $RepoRoot 'reports\steam-guide-description.txt' }

$Project = Get-Content -LiteralPath $ProjectPath -Raw -Encoding UTF8 | ConvertFrom-Json
$Guide = $Project.steamGuide
if ($Guide.enabled -ne $true -or [string]::IsNullOrWhiteSpace([string]$Guide.safeDescription)) {
    throw 'steamGuide.safeDescription is required when the Steam guide is enabled.'
}

$Text = ([string]$Guide.safeDescription).Trim() + "`r`n"
$LinkTags = [regex]::Matches($Text, '(?i)\[url=([^\]]+)\]')
if ($LinkTags.Count -ne 1 -or $LinkTags[0].Groups[1].Value -ne [string]$Guide.publicGuideUrl -or
    ([regex]::Matches($Text, '(?i)https?://')).Count -ne 1 -or $Text -notmatch '(?i)\[/url\]' -or
    $Text -match '\{ССЫЛКА УДАЛЕНА\}|discord\.gg|bit\.ly|tinyurl') {
    throw 'Steam main description must contain exactly one direct link to the configured GitHub report, and no other links or removed-link markers.'
}
if ($Text.Length -gt 3000) { throw 'Steam main description exceeds the conservative 3000-character limit.' }
if ($Text -notmatch 'русск') { throw 'Steam main description must state that the guide is Russian.' }
if ($Text -notmatch 'English') { throw 'Steam main description must state that an English section is available.' }
if ($Text -notmatch 'обновля') { throw 'Steam main description must state that the guide is regularly updated.' }

$Directory = Split-Path -Parent $OutputPath
if (-not (Test-Path -LiteralPath $Directory)) { New-Item -ItemType Directory -Path $Directory | Out-Null }
[IO.File]::WriteAllText($OutputPath, $Text, [Text.UTF8Encoding]::new($false))
Write-Host "STEAM_MAIN_DESCRIPTION_CHARACTERS=$($Text.TrimEnd().Length)"
Write-Host 'STEAM_MAIN_DESCRIPTION=READY'
