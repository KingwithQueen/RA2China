$ErrorActionPreference = 'Stop'
$taskVs = 'E:\Program Files\Microsoft Visual Studio\18\Community'
Import-Module (Join-Path $taskVs 'Common7\Tools\Microsoft.VisualStudio.DevShell.dll')
Enter-VsDevShell -VsInstallPath $taskVs -SkipAutomaticLocation -DevCmdArguments '-arch=x86 -host_arch=x64' | Out-Null
$env:TEMP = Join-Path $PSScriptRoot 'temp'
$env:TMP = $env:TEMP
Push-Location (Join-Path $PSScriptRoot 'evidence\movement-state-v20')
try
{
    & cl /nologo /O2 /W4 /WX /std:c17 /utf-8 /DRECOMP_FLAT_MEMORY /I ..\..\ra2\src\gameplay /I ..\..\ra2\src\runtime /I ..\..\pcrecomp\runtime\recomp32 path_fragment_probe.c ..\..\ra2\src\runtime\ground_path_bridge.c ..\..\ra2\src\gameplay\ground_path.c /Fe:path_fragment_probe.exe /link /BASE:0x60000000 /DYNAMICBASE:NO
    if ($LASTEXITCODE -ne 0) { throw 'Path probe build failed' }
    & cl /nologo /O2 /W4 /WX /std:c17 /utf-8 /DRECOMP_FLAT_MEMORY /DRECOMP_RETADDR=0u /I ..\..\ra2\src\gameplay /I ..\..\ra2\src\runtime /I ..\..\pcrecomp\runtime\recomp32 drive_process_probe.c ..\..\ra2\src\runtime\ground_drive_bridge.c ..\..\ra2\src\gameplay\ground_drive.c /Fe:drive_process_probe.exe /link /BASE:0x60000000 /DYNAMICBASE:NO
    if ($LASTEXITCODE -ne 0) { throw 'Drive process probe build failed' }
    & cl /nologo /O2 /W4 /WX /std:c17 /utf-8 /DRECOMP_FLAT_MEMORY /DRECOMP_RETADDR=0u /I ..\..\ra2\src\gameplay /I ..\..\ra2\src\runtime /I ..\..\pcrecomp\runtime\recomp32 collision_probe.c ..\..\ra2\src\runtime\ground_collision_bridge.c ..\..\ra2\src\gameplay\ground_collision.c ..\..\ra2\src\gameplay\ground_terrain.c audit_noop.c /Fe:collision_probe.exe /link /BASE:0x60000000 /DYNAMICBASE:NO
    if ($LASTEXITCODE -ne 0) { throw 'Collision probe build failed' }
    & cl /nologo /O2 /W4 /WX /std:c17 /utf-8 /DRECOMP_FLAT_MEMORY /DRECOMP_RETADDR=0u /I ..\..\ra2\src\gameplay /I ..\..\ra2\src\runtime /I ..\..\pcrecomp\runtime\recomp32 arrival_probe.c ..\..\ra2\src\runtime\ground_arrival_bridge.c ..\..\ra2\src\gameplay\ground_arrival.c /Fe:arrival_probe.exe /link /BASE:0x60000000 /DYNAMICBASE:NO
    if ($LASTEXITCODE -ne 0) { throw 'Arrival probe build failed' }
}
finally
{
    Pop-Location
}
