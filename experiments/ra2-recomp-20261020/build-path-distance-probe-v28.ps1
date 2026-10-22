$ErrorActionPreference='Stop'
$taskVs='E:\Program Files\Microsoft Visual Studio\18\Community'
Import-Module (Join-Path $taskVs 'Common7\Tools\Microsoft.VisualStudio.DevShell.dll')
Enter-VsDevShell -VsInstallPath $taskVs -SkipAutomaticLocation -DevCmdArguments '-arch=x86 -host_arch=x64' | Out-Null
$env:TEMP=Join-Path $PSScriptRoot 'temp';$env:TMP=$env:TEMP
Push-Location (Join-Path $PSScriptRoot 'evidence\movement-state-v28')
try {
    & cl /nologo /O2 /W4 /WX /std:c17 /utf-8 /I ..\..\ra2\src\gameplay path_distance_probe.c ..\..\ra2\src\gameplay\ground_path_distance.c /Fe:path_distance_probe.exe /link /BASE:0x60000000 /DYNAMICBASE:NO
    if($LASTEXITCODE){throw 'Distance probe build failed'}
    & .\path_distance_probe.exe ..\..\ra2\game\game.exe | Set-Content -LiteralPath path-distance-native.json -Encoding utf8NoBOM
    if($LASTEXITCODE){throw 'Distance probe failed'}
    Get-Content -LiteralPath path-distance-native.json
} finally {Pop-Location}
