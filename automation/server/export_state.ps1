[CmdletBinding()]
param([Parameter(Mandatory=$true)][string]$Destination)
$ErrorActionPreference='Stop'
$root=(Resolve-Path (Join-Path $PSScriptRoot '../..')).Path
New-Item -ItemType Directory -Path $Destination -Force | Out-Null
$runs=Join-Path $root 'automation/runs'
$active=Get-Content -Raw (Join-Path $runs 'refresh/active.json') | ConvertFrom-Json
$names=@('steam-publication-state.json','steam-publication-state-en.json','publication-metrics-state.json','home-assistant-notification-state.json')
foreach($name in $names){
    $file=Join-Path $runs $name
    if(Test-Path -LiteralPath $file){Copy-Item -LiteralPath $file -Destination (Join-Path $Destination $name)}
}
$refresh=Join-Path $Destination 'refresh'
New-Item -ItemType Directory -Path $refresh -Force | Out-Null
Copy-Item -LiteralPath (Join-Path $runs 'refresh/active.json') -Destination (Join-Path $refresh 'active.json')
Copy-Item -LiteralPath (Join-Path $runs ('refresh/'+$active.runId)) -Destination (Join-Path $refresh $active.runId) -Recurse
# Copy ONLY the HA token already used by this project, never unrelated secrets.
$local=Get-Content -Raw (Join-Path $runs 'home-assistant-notification.local.json') | ConvertFrom-Json
$secret=Get-Content -Raw (Join-Path $root $local.homeAssistantSecretPath) | ConvertFrom-Json
$minimal=@{home_assistant=@{api_base_url='http://192.168.1.95:8123/api';long_lived_access_tokens=@{health_auto_export=@{raw_token=$secret.home_assistant.long_lived_access_tokens.health_auto_export.raw_token}}}}
[IO.File]::WriteAllText((Join-Path $Destination 'home-assistant.json'),($minimal|ConvertTo-Json -Depth 10),[Text.UTF8Encoding]::new($false))
$manifest=@{sourceRoot=$root;runId=$active.runId;files=@{}}
Get-ChildItem -LiteralPath $Destination -Recurse -File | ForEach-Object {
    $relative=[IO.Path]::GetRelativePath($Destination,$_.FullName).Replace('\','/')
    $manifest.files[$relative]=(Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
}
[IO.File]::WriteAllText((Join-Path $Destination 'manifest.json'),($manifest|ConvertTo-Json -Depth 10),[Text.UTF8Encoding]::new($false))
Write-Output "STATE_EXPORT_FILES=$($manifest.files.Count)"
Write-Output "STATE_EXPORT_RUN_ID=$($active.runId)"
