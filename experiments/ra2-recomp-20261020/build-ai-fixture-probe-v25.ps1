$ErrorActionPreference='Stop'
$taskVs='E:\Program Files\Microsoft Visual Studio\18\Community'
Import-Module (Join-Path $taskVs 'Common7\Tools\Microsoft.VisualStudio.DevShell.dll')
Enter-VsDevShell -VsInstallPath $taskVs -SkipAutomaticLocation -DevCmdArguments '-arch=x86 -host_arch=x64' | Out-Null
$env:TEMP=Join-Path $PSScriptRoot 'temp';$env:TMP=$env:TEMP
$taskArguments=Get-Content -LiteralPath (Join-Path $PSScriptRoot 'evidence\movement-state-v25\ai-fixture-build-arguments.json') -Raw | ConvertFrom-Json
$taskExe=Join-Path $PSScriptRoot 'ra2\build-original-c\ra2.exe'
$taskBefore=(Get-FileHash -LiteralPath $taskExe -Algorithm SHA256).Hash
Push-Location (Join-Path $PSScriptRoot 'ra2\build-original-c')
try {
    $taskCompile=@($taskArguments.compile);& cl @taskCompile
    if($LASTEXITCODE){throw 'AI fixture compile failed'}
    $taskLink=@($taskArguments.link);& link @taskLink
    if($LASTEXITCODE){throw 'AI fixture link failed'}
} finally {Pop-Location}
if((Get-FileHash -LiteralPath $taskExe -Algorithm SHA256).Hash -ne $taskBefore){throw 'Production executable changed'}
