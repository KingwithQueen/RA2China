$ErrorActionPreference = 'Stop'
$taskVs = 'E:\Program Files\Microsoft Visual Studio\18\Community'
Import-Module (Join-Path $taskVs 'Common7\Tools\Microsoft.VisualStudio.DevShell.dll')
Enter-VsDevShell -VsInstallPath $taskVs -SkipAutomaticLocation -DevCmdArguments '-arch=x64 -host_arch=x64' | Out-Null
$env:TEMP = Join-Path $PSScriptRoot 'temp'
$env:TMP = $env:TEMP
Push-Location (Join-Path $PSScriptRoot 'evidence\movement-state-v4')
try
{
    & cl /nologo /O2 /W4 /WX /std:c17 /utf-8 /MT /D_CRT_SECURE_NO_WARNINGS /I 'D:\Program\红色警戒2\include' extract_resource.c 'D:\Program\红色警戒2\build\ra2resources.lib' /Fe:extract_resource.exe /link user32.lib
    if ($LASTEXITCODE) { throw 'Resource extractor build failed' }
}
finally
{
    Pop-Location
}
