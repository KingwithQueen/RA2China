$ErrorActionPreference = 'Stop'
$taskVs = 'E:\Program Files\Microsoft Visual Studio\18\Community'
Import-Module (Join-Path $taskVs 'Common7\Tools\Microsoft.VisualStudio.DevShell.dll')
Enter-VsDevShell -VsInstallPath $taskVs -SkipAutomaticLocation -DevCmdArguments '-arch=x86 -host_arch=x64' | Out-Null
$env:TEMP = Join-Path $PSScriptRoot 'temp'
$env:TMP = $env:TEMP
Push-Location (Join-Path $PSScriptRoot 'evidence\movement-state-v35')
try {
 & cl /nologo /O2 /W4 /WX /std:c17 /utf-8 /DRECOMP_FLAT_MEMORY /DRECOMP_RETADDR=0u /I ..\..\ra2\src\gameplay /I ..\..\ra2\src\runtime /I ..\..\ra2\src\compat /I ..\..\pcrecomp\runtime\recomp32 overlap_probe.c ..\..\ra2\src\gameplay\ground_sampling_shared.c ..\..\ra2\src\gameplay\ground_template.c ..\..\ra2\src\runtime\ground_overlap_bridge.c ..\..\ra2\src\gameplay\ground_template_transition.c ..\..\ra2\src\gameplay\ground_object_chain.c ..\..\ra2\src\runtime\ground_joint_bridge.c ..\..\ra2\src\gameplay\ground_template_entry.c ..\..\ra2\src\gameplay\ground_passage_entry.c ..\..\ra2\src\gameplay\ground_return_plan.c /Fe:overlap_probe.exe /link /BASE:0x60000000 /DYNAMICBASE:NO
 if($LASTEXITCODE){throw 'Progress probe build failed'}
} finally {Pop-Location}
