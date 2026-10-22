$ErrorActionPreference = 'Stop'
$taskVs = 'E:\Program Files\Microsoft Visual Studio\18\Community'
Import-Module (Join-Path $taskVs 'Common7\Tools\Microsoft.VisualStudio.DevShell.dll')
Enter-VsDevShell -VsInstallPath $taskVs -SkipAutomaticLocation -DevCmdArguments '-arch=x86 -host_arch=x64' | Out-Null
$env:TEMP = Join-Path $PSScriptRoot 'temp'
$env:TMP = $env:TEMP
Push-Location (Join-Path $PSScriptRoot 'evidence\movement-state-v24')
try {
 & cl /nologo /O2 /W4 /WX /std:c17 /utf-8 /I ..\..\ra2\src\gameplay /I ..\..\ra2\src\compat connection_numeric_probe.c ..\..\ra2\src\gameplay\ground_connection_numeric.c ..\..\ra2\src\compat\x87_arithmetic.c /Fe:connection_numeric_probe.exe /link /BASE:0x60000000 /DYNAMICBASE:NO
 if($LASTEXITCODE){throw 'Remainder probe build failed'}
} finally {Pop-Location}
