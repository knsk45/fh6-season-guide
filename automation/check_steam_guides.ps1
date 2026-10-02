[CmdletBinding()]
param()

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$AllUpToDate = $true
foreach ($Language in @('ru','en')) {
    # Child checker reports status with Write-Host, which is the Information
    # stream in PowerShell 7; merge all streams so the wrapper can actually
    # inspect the authoritative status instead of falsely returning UPDATE_REQUIRED.
    $Output = & (Join-Path $PSScriptRoot 'check_steam_guide.ps1') -Language $Language *>&1
    $Output | ForEach-Object { Write-Host $_ }
    if (-not $?) { throw "Steam checker failed for $Language." }
    if (-not (($Output -join "`n") -match 'STEAM_STATUS=UP_TO_DATE')) { $AllUpToDate = $false }
}
if ($AllUpToDate) { Write-Host 'STEAM_GUIDES_STATUS=UP_TO_DATE' }
else { Write-Host 'STEAM_GUIDES_STATUS=UPDATE_REQUIRED' }
