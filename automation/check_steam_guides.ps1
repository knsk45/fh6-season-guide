[CmdletBinding()]
param()

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$AllUpToDate = $true
foreach ($Language in @('ru','en')) {
    $Output = & (Join-Path $PSScriptRoot 'check_steam_guide.ps1') -Language $Language 2>&1
    $Output | ForEach-Object { Write-Host $_ }
    if (-not $?) { throw "Steam checker failed for $Language." }
    if (-not (($Output -join "`n") -match 'STEAM_STATUS=UP_TO_DATE')) { $AllUpToDate = $false }
}
if ($AllUpToDate) { Write-Host 'STEAM_GUIDES_STATUS=UP_TO_DATE' }
else { Write-Host 'STEAM_GUIDES_STATUS=UPDATE_REQUIRED' }
