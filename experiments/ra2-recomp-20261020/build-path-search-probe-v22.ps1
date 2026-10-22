$ErrorActionPreference='Stop'
$taskVs='E:\Program Files\Microsoft Visual Studio\18\Community'
Import-Module (Join-Path $taskVs 'Common7\Tools\Microsoft.VisualStudio.DevShell.dll')
Enter-VsDevShell -VsInstallPath $taskVs -SkipAutomaticLocation -DevCmdArguments '-arch=x86 -host_arch=x64' | Out-Null
$env:TEMP=Join-Path $PSScriptRoot 'temp';$env:TMP=$env:TEMP
Push-Location (Join-Path $PSScriptRoot 'evidence\movement-state-v22')
try {
    & cl /nologo /O2 /W4 /WX /std:c17 /utf-8 /I ..\..\ra2\src\gameplay /I ..\..\ra2\src\compat path_search_probe.c ..\..\ra2\src\gameplay\ground_path_search.c ..\..\ra2\src\gameplay\ground_path_distance.c ..\..\ra2\src\gameplay\ground_path_nodes.c ..\..\ra2\src\gameplay\ground_path_heap.c ..\..\ra2\src\gameplay\ground_path_cache.c ..\..\ra2\src\gameplay\ground_path_cost.c ..\..\ra2\src\compat\x87_arithmetic.c /Fe:path_search_probe.exe /link /BASE:0x60000000 /DYNAMICBASE:NO
    if($LASTEXITCODE){throw 'Search probe build failed'}
} finally {Pop-Location}
