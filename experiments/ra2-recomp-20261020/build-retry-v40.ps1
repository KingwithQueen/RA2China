$ErrorActionPreference='Stop'
$taskVs='E:\Program Files\Microsoft Visual Studio\18\Community'
Import-Module (Join-Path $taskVs 'Common7\Tools\Microsoft.VisualStudio.DevShell.dll')
Enter-VsDevShell -VsInstallPath $taskVs -SkipAutomaticLocation -DevCmdArguments '-arch=x86 -host_arch=x64' | Out-Null
$env:TEMP=Join-Path $PSScriptRoot 'temp';$env:TMP=$env:TEMP
$taskCmake=Join-Path $taskVs 'Common7\IDE\CommonExtensions\Microsoft\CMake\CMake\bin\cmake.exe'
$taskBuild=Join-Path $PSScriptRoot 'ra2\build-original-c'
$taskCompile=Get-Content -LiteralPath (Join-Path $taskBuild 'compile_commands.json') -Raw | ConvertFrom-Json
$taskSources=@($taskCompile | ForEach-Object {[IO.Path]::GetFullPath($_.file,$_.directory)} | Sort-Object -Unique)
$taskHeaders=@(Get-ChildItem -LiteralPath (Join-Path $PSScriptRoot 'ra2\src'),(Join-Path $PSScriptRoot 'pcrecomp\runtime\recomp32') -Recurse -File -Filter '*.h' | Select-Object -ExpandProperty FullName)
$taskHashes=@{}
foreach($taskPath in (@($taskSources)+@($taskHeaders) | Sort-Object -Unique)){$taskHashes[$taskPath]=(Get-FileHash -LiteralPath $taskPath -Algorithm SHA256).Hash.ToLowerInvariant()}
if($taskSources.Count -ne 172 -or $taskHashes.Count -ne 294){throw 'Unexpected compile inputs'}
# 上次所有编译任务已完成，只有重名导致链接失败。Ninja按已记录的依赖重编译改名后的源和头，不伪造成功收据。
& $taskCmake --build $taskBuild --parallel 4
if($LASTEXITCODE){throw 'Retry compile/link failed'}
foreach($taskPath in $taskHashes.Keys){if((Get-FileHash -LiteralPath $taskPath -Algorithm SHA256).Hash.ToLowerInvariant() -ne $taskHashes[$taskPath]){throw 'Input changed during retry'}}
$taskExe=Join-Path $taskBuild 'ra2.exe'
@{inputs=$taskHashes;source_count=$taskSources.Count;refreshed_count=0;executable_was_replaced=$true;executable_sha256=(Get-FileHash -LiteralPath $taskExe -Algorithm SHA256).Hash.ToLowerInvariant();recovered_link_failure='movement-state-v40/investigations/build-link-01';ninja_dependency_graph_verified=$true} | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $taskBuild 'source-content-receipt.json') -Encoding utf8NoBOM
