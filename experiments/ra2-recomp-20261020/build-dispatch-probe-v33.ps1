$ErrorActionPreference='Stop'
$taskVs='E:\Program Files\Microsoft Visual Studio\18\Community'
Import-Module (Join-Path $taskVs 'Common7\Tools\Microsoft.VisualStudio.DevShell.dll')
Enter-VsDevShell -VsInstallPath $taskVs -SkipAutomaticLocation -DevCmdArguments '-arch=x86 -host_arch=x64' | Out-Null
$env:TEMP=Join-Path $PSScriptRoot 'temp';$env:TMP=$env:TEMP
Push-Location (Join-Path $PSScriptRoot 'evidence/movement-state-v33')
try {
 & cl /nologo /O2 /W4 /WX /std:c17 /utf-8 /I ..\..\ra2\src\gameplay /I ..\..\ra2\src\compat dispatch_probe.c ..\..\ra2\src\gameplay\ground_sampling.c ..\..\ra2\src\gameplay\ground_path.c ..\..\ra2\src\gameplay\ground_prepare_exit.c ..\..\ra2\src\gameplay\ground_object_services.c ..\..\ra2\src\gameplay\unit_movement.c ..\..\ra2\src\compat\x87_arithmetic.c /Fe:route_control_probe.exe /link /BASE:0x60000000 /DYNAMICBASE:NO
 if($LASTEXITCODE){throw 'Dispatch probe build failed'}
} finally {Pop-Location}
