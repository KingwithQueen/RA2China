param([int]$Parallel = 4)
$ErrorActionPreference = 'Stop'
$taskRoot = $PSScriptRoot
$taskVs = 'E:\Program Files\Microsoft Visual Studio\18\Community'
$taskCmake = Join-Path $taskVs 'Common7\IDE\CommonExtensions\Microsoft\CMake\CMake\bin\cmake.exe'
$taskNinja = Join-Path $taskVs 'Common7\IDE\CommonExtensions\Microsoft\CMake\Ninja\ninja.exe'
# 使用已安装的 x86 C 编译工具；构建、临时文件和日志仅进入实验目录。
New-Item -ItemType Directory -Path (Join-Path $taskRoot 'temp') -Force | Out-Null
Import-Module (Join-Path $taskVs 'Common7\Tools\Microsoft.VisualStudio.DevShell.dll')
Enter-VsDevShell -VsInstallPath $taskVs -SkipAutomaticLocation -DevCmdArguments '-arch=x86 -host_arch=x64' | Out-Null
$env:TEMP = Join-Path $taskRoot 'temp'
$env:TMP = $env:TEMP
Push-Location (Join-Path $taskRoot 'ra2')
try {
    # Release 探测避免调用冲突的调试数据库服务；需要的函数地址另存于索引和调用轨迹。
    & $taskCmake -S . -B build-original-c -G Ninja "-DCMAKE_MAKE_PROGRAM=$taskNinja" -DCMAKE_BUILD_TYPE=Release -DCMAKE_TRY_COMPILE_CONFIGURATION=Release -DCMAKE_C_STANDARD=17 '-DCMAKE_C_FLAGS_DEBUG=/Z7 /Ob0 /Od /RTC1' -DRA2_TARGET=game -DRA2_TRACE=ON -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
    if ($LASTEXITCODE) { throw 'CMake 配置失败。' }
    # 对象数增加后 Ninja 会改用响应文件；MSVC 需要 BOM 才能识别其中的 UTF-8 中文路径。
    $taskRulesPath = Join-Path $taskRoot 'ra2\build-original-c\CMakeFiles\rules.ninja'
    $taskRulesText = [IO.File]::ReadAllText($taskRulesPath)
    $taskRspOld = 'rspfile_content = $in_newline $LINK_PATH $LINK_LIBRARIES'
    $taskRspNew = 'rspfile_content = ' + [char]0xFEFF + '$in_newline $LINK_PATH $LINK_LIBRARIES'
    if ($taskRulesText.Contains($taskRspOld)) {
        [IO.File]::WriteAllText($taskRulesPath, $taskRulesText.Replace($taskRspOld, $taskRspNew), [Text.UTF8Encoding]::new($false))
    }
    # 归档恢复会保留旧时间戳。以内容确认输入变化，防止 Ninja 沿用诊断版本对象。
    $taskReceipt = Join-Path $taskRoot 'ra2\build-original-c\source-content-receipt.json'
    $taskCompile = Get-Content -LiteralPath 'build-original-c\compile_commands.json' -Raw | ConvertFrom-Json
    $taskSources = @($taskCompile | ForEach-Object {
        [IO.Path]::GetFullPath($_.file, $_.directory)
    } | Sort-Object -Unique)
    $taskInputPaths = @($taskSources) + @(Get-ChildItem -LiteralPath 'src', '..\pcrecomp\runtime\recomp32' -Recurse -File -Filter '*.h' | Select-Object -ExpandProperty FullName)
    $taskHashes = @{}
    foreach ($taskPath in ($taskInputPaths | Sort-Object -Unique)) {
        $taskAbsolute = [IO.Path]::GetFullPath($taskPath)
        if (-not $taskAbsolute.StartsWith($taskRoot + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) { throw "构建输入越出实验目录：$taskAbsolute" }
        $taskHashes[$taskAbsolute] = (Get-FileHash -LiteralPath $taskAbsolute -Algorithm SHA256).Hash.ToLowerInvariant()
    }
    $taskPrevious = @{}
    $taskOldReceipt = $null
    if (Test-Path -LiteralPath $taskReceipt) {
        $taskOldReceipt = Get-Content -LiteralPath $taskReceipt -Raw | ConvertFrom-Json -AsHashtable
        $taskPrevious = $taskOldReceipt.inputs
    }
    $taskHeadersChanged = $taskPrevious.Count -eq 0
    foreach ($taskPath in $taskHashes.Keys) {
        # 新头文件由新增/修改的源文件和 Ninja 依赖处理；已存在头文件恢复旧时间戳时刷新全部源。
        if ([IO.Path]::GetExtension($taskPath) -eq '.h' -and $taskPrevious.ContainsKey($taskPath) -and $taskPrevious[$taskPath] -ne $taskHashes[$taskPath]) { $taskHeadersChanged = $true }
    }
    $taskForced = @($taskSources | Where-Object { $taskHeadersChanged -or $taskPrevious[$_] -ne $taskHashes[$_] })
    $taskArtifactChanged = -not (Test-Path -LiteralPath 'build-original-c\ra2.exe')
    if (-not $taskArtifactChanged -and $taskOldReceipt) {
        $taskArtifactChanged = (Get-FileHash -LiteralPath 'build-original-c\ra2.exe' -Algorithm SHA256).Hash.ToLowerInvariant() -ne $taskOldReceipt.executable_sha256
    }
    # 正式 EXE 单独回退后，下次构建也必须重新链接当前源对应的对象。
    if ($taskArtifactChanged -and -not $taskForced.Count) { $taskForced = @($taskSources[0]) }
    foreach ($taskPath in $taskForced) { [IO.File]::SetLastWriteTimeUtc($taskPath, [DateTime]::UtcNow) }
    Write-Output ("按内容检查构建输入：{0} 项；强制刷新：{1} 个源文件。" -f $taskHashes.Count, $taskForced.Count)
    & $taskCmake --build build-original-c --parallel $Parallel
    if ($LASTEXITCODE) { throw 'C 编译或链接失败。' }
    foreach ($taskPath in $taskHashes.Keys) {
        if ((Get-FileHash -LiteralPath $taskPath -Algorithm SHA256).Hash.ToLowerInvariant() -ne $taskHashes[$taskPath]) { throw "构建期间输入发生变化：$taskPath" }
    }
    @{ inputs = $taskHashes; source_count = $taskSources.Count; refreshed_count = $taskForced.Count; executable_was_replaced = $taskArtifactChanged;
       executable_sha256 = (Get-FileHash -LiteralPath 'build-original-c\ra2.exe' -Algorithm SHA256).Hash.ToLowerInvariant()
    } | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $taskReceipt -Encoding utf8NoBOM
} finally {
    Pop-Location
}
