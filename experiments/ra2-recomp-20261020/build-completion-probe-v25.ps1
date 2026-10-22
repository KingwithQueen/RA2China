$ErrorActionPreference = 'Stop'
$taskVs = 'E:\Program Files\Microsoft Visual Studio\18\Community'
Import-Module (Join-Path $taskVs 'Common7\Tools\Microsoft.VisualStudio.DevShell.dll')
Enter-VsDevShell -VsInstallPath $taskVs -SkipAutomaticLocation -DevCmdArguments '-arch=x86 -host_arch=x64' | Out-Null
$env:TEMP = Join-Path $PSScriptRoot 'temp'
$env:TMP = $env:TEMP
Push-Location (Join-Path $PSScriptRoot 'evidence\movement-state-v25')
try {
    & cl /nologo /O2 /W4 /WX /std:c17 /utf-8 /DRECOMP_FLAT_MEMORY /DRECOMP_RETADDR=0u /I ..\..\ra2\src\gameplay /I ..\..\ra2\src\runtime /I ..\..\pcrecomp\runtime\recomp32 arrival_complete_probe.c ..\..\ra2\src\runtime\ground_arrival_bridge.c ..\..\ra2\src\gameplay\ground_arrival.c /Fe:arrival_complete_probe.exe ..\..\ra2\src\runtime\ground_completion_bridge.c ..\..\ra2\src\gameplay\ground_completion.c ..\..\ra2\src\gameplay\ground_passage.c ..\..\ra2\src\gameplay\ground_cell_services.c ..\..\ra2\src\gameplay\unit_movement.c ..\..\ra2\src\compat\x87_arithmetic.c /I ..\..\ra2\src\compat /link /BASE:0x60000000 /DYNAMICBASE:NO
 if($LASTEXITCODE){throw 'Arrival completion probe build failed'}
    & cl /nologo /O2 /W4 /WX /std:c17 /utf-8 /DRECOMP_FLAT_MEMORY /DRECOMP_RETADDR=0u /I ..\..\ra2\src\gameplay /I ..\..\ra2\src\runtime /I ..\..\pcrecomp\runtime\recomp32 completion_services_probe.c ..\..\ra2\src\runtime\ground_arrival_bridge.c ..\..\ra2\src\gameplay\ground_arrival.c /Fe:completion_services_probe.exe ..\..\ra2\src\runtime\ground_completion_bridge.c ..\..\ra2\src\gameplay\ground_completion.c ..\..\ra2\src\gameplay\ground_passage.c ..\..\ra2\src\gameplay\ground_cell_services.c ..\..\ra2\src\gameplay\unit_movement.c ..\..\ra2\src\compat\x87_arithmetic.c /I ..\..\ra2\src\compat /link /BASE:0x60000000 /DYNAMICBASE:NO
 if($LASTEXITCODE){throw 'Completion services probe build failed'}
} finally {Pop-Location}
