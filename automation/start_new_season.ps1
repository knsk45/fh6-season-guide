[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$InputPath,
    [switch]$ValidateOnly
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$InputPath = [IO.Path]::GetFullPath($InputPath)
$CurrentStatePath = Join-Path $RepoRoot 'data\current-season.json'
$Validator = Join-Path $PSScriptRoot 'validate_season.ps1'
$Renderer = Join-Path $PSScriptRoot 'render_season_markdown.ps1'

if (-not (Test-Path -LiteralPath $InputPath)) { throw "New-season input was not found: $InputPath" }
$validationOutput = & $Validator -StatePath $InputPath -SkipOutputs
$validationSucceeded = $?
$validationOutput | Write-Output
if (-not $validationSucceeded) { throw 'New-season input failed validation' }

$newState = Get-Content -LiteralPath $InputPath -Raw -Encoding UTF8 | ConvertFrom-Json
$newArchivePath = [IO.Path]::GetFullPath((Join-Path $RepoRoot $newState.season.archiveFile))
$assetsPath = [IO.Path]::GetFullPath((Join-Path $RepoRoot $newState.season.assetsDirectory))

if ($ValidateOnly) {
    Write-Output "ROLLOVER_INPUT_OK archive=$($newState.season.archiveFile) cards=$(@($newState.activities).Count)"
    exit 0
}

if (Test-Path -LiteralPath $CurrentStatePath) {
    $oldState = Get-Content -LiteralPath $CurrentStatePath -Raw -Encoding UTF8 | ConvertFrom-Json
    if ($oldState.season.archiveFile -eq $newState.season.archiveFile) {
        throw "Refusing rollover to the same archive: $($newState.season.archiveFile)"
    }
    $historyRoot = Join-Path $RepoRoot 'data\history'
    [IO.Directory]::CreateDirectory($historyRoot) | Out-Null
    $oldBase = [IO.Path]::GetFileNameWithoutExtension([string]$oldState.season.archiveFile)
    $historyPath = Join-Path $historyRoot "$oldBase.json"
    if (-not (Test-Path -LiteralPath $historyPath)) {
        Copy-Item -LiteralPath $CurrentStatePath -Destination $historyPath
    }
}

if (Test-Path -LiteralPath $newArchivePath) {
    throw "Refusing to overwrite an existing season archive during rollover: $newArchivePath"
}

[IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName($CurrentStatePath)) | Out-Null
[IO.Directory]::CreateDirectory($assetsPath) | Out-Null
$normalized = $newState | ConvertTo-Json -Depth 30
[IO.File]::WriteAllText($CurrentStatePath, $normalized, [Text.UTF8Encoding]::new($false))
$renderOutput = & $Renderer -StatePath $CurrentStatePath
$renderSucceeded = $?
$renderOutput | Write-Output
if (-not $renderSucceeded) { throw 'Failed to render the new season Markdown' }

Write-Output "ROLLOVER_OK archive=$($newState.season.archiveFile) cards=$(@($newState.activities).Count)"
