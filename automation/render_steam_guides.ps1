[CmdletBinding()]
param()

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

foreach ($Language in @('ru','en')) {
    & (Join-Path $PSScriptRoot 'render_steam_guide.ps1') -Language $Language
    if (-not $?) { throw "Steam renderer failed for $Language." }
}
Write-Host 'STEAM_GUIDES_RENDERED=ru,en'
