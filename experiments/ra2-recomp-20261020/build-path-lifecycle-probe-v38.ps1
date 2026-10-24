$ErrorActionPreference='Stop'
$taskVs='E:\Program Files\Microsoft Visual Studio\18\Community'
Import-Module (Join-Path $taskVs 'Common7\Tools\Microsoft.VisualStudio.DevShell.dll')
Enter-VsDevShell -VsInstallPath $taskVs -SkipAutomaticLocation -DevCmdArguments '-arch=x86 -host_arch=x64' | Out-Null
$env:TEMP=Join-Path $PSScriptRoot 'temp';$env:TMP=$env:TEMP
Push-Location (Join-Path $PSScriptRoot 'evidence\movement-state-v38')
try {
 & cl /nologo /O2 /W4 /WX /std:c17 /utf-8 /I ..\..\ra2\src\gameplay /I ..\..\ra2\src\compat path_lifecycle_probe.c ..\..\ra2\src\gameplay\ground_path_prepare.c ..\..\ra2\src\gameplay\ground_region_route.c ..\..\ra2\src\gameplay\ground_path_rebuild.c ..\..\ra2\src\gameplay\ground_path_nodes.c ..\..\ra2\src\gameplay\ground_path_heap.c ..\..\ra2\src\gameplay\ground_path_cost.c ..\..\ra2\src\compat\x87_arithmetic.c /Fe:path_lifecycle_probe.exe /link /BASE:0x60000000 /DYNAMICBASE:NO
 if($LASTEXITCODE){throw 'Lifecycle probe build failed'}
} finally {Pop-Location}
