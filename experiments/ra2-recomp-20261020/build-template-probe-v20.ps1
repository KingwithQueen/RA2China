$ErrorActionPreference = 'Stop'
$taskVs = 'E:\Program Files\Microsoft Visual Studio\18\Community'
Import-Module (Join-Path $taskVs 'Common7\Tools\Microsoft.VisualStudio.DevShell.dll')
Enter-VsDevShell -VsInstallPath $taskVs -SkipAutomaticLocation -DevCmdArguments '-arch=x86 -host_arch=x64' | Out-Null
$env:TEMP = Join-Path $PSScriptRoot 'temp'
$env:TMP = $env:TEMP
Push-Location (Join-Path $PSScriptRoot 'evidence\movement-state-v20')
try
{
    & cl /nologo /O2 /W4 /WX /std:c17 /utf-8 /DRECOMP_FLAT_MEMORY /DRECOMP_RETADDR=0u /I ..\..\ra2\src\gameplay /I ..\..\ra2\src\runtime /I ..\..\ra2\src\compat /I ..\..\pcrecomp\runtime\recomp32 template_probe.c ..\..\ra2\src\runtime\ground_prepare_bridge.c ..\..\ra2\src\gameplay\ground_prepare.c ..\..\ra2\src\gameplay\ground_obstacle.c ..\..\ra2\src\gameplay\ground_segment.c ..\..\ra2\src\gameplay\ground_wait.c ..\..\ra2\src\gameplay\ground_reaction.c ..\..\ra2\src\gameplay\unit_movement.c ..\..\ra2\src\compat\x87_arithmetic.c ..\..\ra2\src\gameplay\ground_special.c ..\..\ra2\src\gameplay\ground_template.c /Fe:template_probe.exe /link /BASE:0x60000000 /DYNAMICBASE:NO
    if ($LASTEXITCODE -ne 0) { throw 'Obstacle probe build failed' }
}
finally
{
    Pop-Location
}
