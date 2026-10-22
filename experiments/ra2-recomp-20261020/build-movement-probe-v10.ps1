$ErrorActionPreference = 'Stop'
$experiment = $PSScriptRoot
$vsInstall = 'E:\Program Files\Microsoft Visual Studio\18\Community'
Import-Module (Join-Path $vsInstall 'Common7\Tools\Microsoft.VisualStudio.DevShell.dll')
Enter-VsDevShell -VsInstallPath $vsInstall -SkipAutomaticLocation -DevCmdArguments '-arch=x86 -host_arch=x64'
$env:TEMP = Join-Path $experiment 'temp'
$env:TMP = $env:TEMP
$probeDirectory = Join-Path $experiment 'evidence\movement-state-v10'
Push-Location $probeDirectory
try
{
    & cl /nologo /O2 /W4 /WX /std:c17 /utf-8 /I ..\..\ra2\src\compat /I ..\..\ra2\src\gameplay movement_probe.c ..\..\ra2\src\compat\x87_arithmetic.c ..\..\ra2\src\gameplay\unit_movement.c /Fe:movement_probe.exe
    if ($LASTEXITCODE -ne 0) { throw 'Movement probe compile failed' }
    & .\movement_probe.exe
    if ($LASTEXITCODE -ne 0) { throw 'Movement probe mismatch' }
    & cl /nologo /O2 /W4 /WX /std:c17 /utf-8 /DRECOMP_FLAT_MEMORY /I ..\..\ra2\src\compat /I ..\..\ra2\src\gameplay /I ..\..\ra2\src\runtime /I ..\..\pcrecomp\runtime\recomp32 original_movement_probe.c ..\..\ra2\src\runtime\movement_bridge.c ..\..\ra2\src\compat\x87_arithmetic.c ..\..\ra2\src\gameplay\unit_movement.c /Fe:original_movement_probe.exe /link /BASE:0x60000000 /DYNAMICBASE:NO
    if ($LASTEXITCODE -ne 0) { throw 'Original movement probe compile failed' }
}
finally
{
    Pop-Location
}
