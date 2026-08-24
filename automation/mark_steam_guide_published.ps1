[CmdletBinding()]
param(
    [string]$GuidePath,
    [string]$StatePath,
    [string]$ProjectPath,
    [string]$PublicationStatePath,
    [string]$Evidence = 'Public Steam guide verified'
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
if (-not $GuidePath) { $GuidePath = Join-Path $RepoRoot 'reports\steam-guide-current.txt' }
if (-not $StatePath) { $StatePath = Join-Path $RepoRoot 'data\current-season.json' }
if (-not $ProjectPath) { $ProjectPath = Join-Path $RepoRoot 'data\project.json' }
if (-not $PublicationStatePath) { $PublicationStatePath = Join-Path $RepoRoot 'automation\runs\steam-publication-state.json' }

function Get-SubstantiveSteamHash {
    param([Parameter(Mandatory = $true)][string]$Path)

    $Text = Get-Content -LiteralPath $Path -Raw -Encoding UTF8
    $Text = [regex]::Replace($Text, '(?m)^\[b\]Последняя проверка данных:\[/b\][^\r\n]*(\r?\n)?', '')
    $Text = $Text -replace "`r`n", "`n"
    $Bytes = [Text.Encoding]::UTF8.GetBytes($Text.Trim())
    $Hasher = [Security.Cryptography.SHA256]::Create()
    try { return ([BitConverter]::ToString($Hasher.ComputeHash($Bytes))).Replace('-', '').ToLowerInvariant() }
    finally { $Hasher.Dispose() }
}

foreach ($RequiredPath in @($GuidePath, $StatePath, $ProjectPath)) {
    if (-not (Test-Path -LiteralPath $RequiredPath)) { throw "Required file not found: $RequiredPath" }
}

$State = Get-Content -LiteralPath $StatePath -Raw -Encoding UTF8 | ConvertFrom-Json
$Project = Get-Content -LiteralPath $ProjectPath -Raw -Encoding UTF8 | ConvertFrom-Json
$Hash = Get-SubstantiveSteamHash -Path $GuidePath
$Directory = Split-Path -Parent $PublicationStatePath
if (-not (Test-Path -LiteralPath $Directory)) { New-Item -ItemType Directory -Path $Directory | Out-Null }

$Payload = [ordered]@{
    schemaVersion = 1
    contentHash = $Hash
    publishedAt = [DateTimeOffset]::Now.ToString('o')
    sourceAuditAt = [string]$State.lastContentUpdate
    steamGuideUrl = [string]$Project.steamGuide.url
    evidence = $Evidence
}
[IO.File]::WriteAllText($PublicationStatePath, ($Payload | ConvertTo-Json -Depth 5) + "`r`n", [Text.UTF8Encoding]::new($false))

Write-Host 'STEAM_PUBLICATION_STATE=RECORDED'
Write-Host "STEAM_CONTENT_HASH=$Hash"
Write-Host "STEAM_PUBLICATION_STATE_PATH=$PublicationStatePath"
