$ErrorActionPreference='Stop'
$taskVs='E:\Program Files\Microsoft Visual Studio\18\Community'
Import-Module (Join-Path $taskVs 'Common7\Tools\Microsoft.VisualStudio.DevShell.dll')
Enter-VsDevShell -VsInstallPath $taskVs -SkipAutomaticLocation -DevCmdArguments '-arch=x86 -host_arch=x64' | Out-Null
$env:TEMP=Join-Path $PSScriptRoot 'temp';$env:TMP=$env:TEMP
Push-Location (Join-Path $PSScriptRoot 'evidence\combat-state-v4')
try {
 & cl /nologo /O2 /W4 /WX /std:c17 /utf-8 /DRECOMP_FLAT_MEMORY /DRECOMP_RETADDR=0u /I ..\..\ra2\src\gameplay /I ..\..\ra2\src\runtime /I ..\..\ra2\src\compat /I ..\..\pcrecomp\runtime\recomp32 lifecycle_probe_initial_frame.c ..\..\ra2\src\gameplay\combat_lifecycle.c ..\..\ra2\src\runtime\combat_lifecycle_bridge.c /Fe:lifecycle_probe_initial_frame.exe /link /BASE:0x60000000 /DYNAMICBASE:NO
 if($LASTEXITCODE){throw 'Death probe compile failed'}
} finally {Pop-Location}
