$ErrorActionPreference = 'Stop'
$taskVs = 'E:\Program Files\Microsoft Visual Studio\18\Community'
Import-Module (Join-Path $taskVs 'Common7\Tools\Microsoft.VisualStudio.DevShell.dll')
Enter-VsDevShell -VsInstallPath $taskVs -SkipAutomaticLocation -DevCmdArguments '-arch=x86 -host_arch=x64' | Out-Null
$env:TEMP = Join-Path $PSScriptRoot 'temp'
$env:TMP = $env:TEMP
Push-Location (Join-Path $PSScriptRoot 'evidence\movement-state-v62')
try
{
    & cl /nologo /O2 /W4 /WX /std:c17 /utf-8 /DRECOMP_FLAT_MEMORY /DRECOMP_RETADDR=0u /I ..\..\ra2\src\gameplay /I ..\..\ra2\src\runtime /I ..\..\pcrecomp\runtime\recomp32 drive_process_probe.c ..\..\ra2\src\runtime\ground_drive_bridge.c ..\..\ra2\src\gameplay\ground_drive.c ..\..\ra2\src\gameplay\ground_failure_transition.c ..\..\ra2\src\gameplay\ground_owner_boundary.c /Fe:drive_process_probe.exe /link /BASE:0x60000000 /DYNAMICBASE:NO
    if ($LASTEXITCODE) { throw 'Native state probe failed' }
} finally { Pop-Location }
