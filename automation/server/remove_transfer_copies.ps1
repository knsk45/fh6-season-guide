# Remove only the transport copies created by this migration, never source runs/assets.
$ErrorActionPreference='Stop'
$root=(Resolve-Path (Join-Path $PSScriptRoot '../..')).Path
$runRoot=[IO.Path]::GetFullPath((Join-Path $root 'automation/runs'))
$names=@('server-export','server-transfer','fh6-server-source.tar','fh6-server-state.tar','fh6-server-active-state.tar','fh6-server-state-ready.tar','fh6-server-patch-ready.tar','fh6-server-patch.tar','fh6-server-final.tar')
foreach($name in $names){
    $target=[IO.Path]::GetFullPath((Join-Path $runRoot $name))
    if([IO.Path]::GetDirectoryName($target) -ne $runRoot){throw 'Unsafe cleanup path'}
    if(Test-Path -LiteralPath $target){Remove-Item -LiteralPath $target -Recurse -Force}
}
Write-Output 'LOCAL_TRANSPORT_COPIES_REMOVED=YES'
