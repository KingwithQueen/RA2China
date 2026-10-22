param([string]$ReportDirectory)
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot
if (-not $ReportDirectory) { $ReportDirectory = Join-Path $root 'reports\cmake-locomotor' }
$out = Join-Path $root 'build\cmake-ninja-locomotor'
New-Item -ItemType Directory -Force $out,$ReportDirectory | Out-Null
$vswhere = Join-Path ${env:ProgramFiles(x86)} 'Microsoft Visual Studio\Installer\vswhere.exe'
$installation = & $vswhere -latest -products * -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationPath
if (-not $installation) { throw '找不到 MSVC。' }
$vcvars = Join-Path $installation 'VC\Auxiliary\Build\vcvars64.bat'
$environment = & $env:ComSpec /d /s /c ('"' + $vcvars + '" >nul && set')
if ($LASTEXITCODE) { throw '无法加载编译环境。' }
foreach ($line in $environment) {
    if ($line -match '^([^=]+)=(.*)$') { [Environment]::SetEnvironmentVariable($matches[1],$matches[2],'Process') }
}
# 请求英文诊断；只有中文资源的安装会回退，因此还须实测本机提示前缀。
$env:VSLANG = '1033'
$env:TEMP = $out
$env:TMP = $out
$cmake = Join-Path $installation 'Common7\IDE\CommonExtensions\Microsoft\CMake\CMake\bin\cmake.exe'
$ctest = Join-Path (Split-Path $cmake) 'ctest.exe'
$ninja = Join-Path $installation 'Common7\IDE\CommonExtensions\Microsoft\CMake\Ninja\ninja.exe'
$header = Join-Path $out 'prefix_probe.h'
$probe = Join-Path $out 'prefix_probe.c'
Set-Content -LiteralPath $header -Value '/* dependency probe */' -Encoding utf8
Set-Content -LiteralPath $probe -Value ('#include "' + $header + '"' + [Environment]::NewLine + 'int probe(void) { return 0; }') -Encoding utf8
$lines = & cl.exe /nologo /TC /utf-8 /c /showIncludes ('/Fo' + (Join-Path $out 'prefix_probe.obj')) $probe
if ($LASTEXITCODE) { throw '无法读取编译器头文件提示。' }
$lines | Set-Content -LiteralPath (Join-Path $ReportDirectory 'cmake-prefix-probe.log') -Encoding utf8
$prefix = $null
foreach ($line in $lines) {
    if ($line -match '^(.*?)[A-Za-z]:[/\\].*prefix_probe\.h$') { $prefix = $matches[1]; break }
}
if (-not $prefix) { throw '无法识别头文件提示前缀。' }
# 在 project 启用语言后覆盖缓存中可能乱码的前缀；只修改当前构建目录。
$include = Join-Path $out 'msvc-prefix.cmake'
Set-Content -LiteralPath $include -Value ('set(CMAKE_CL_SHOWINCLUDES_PREFIX [==[' + $prefix + ']==])') -Encoding utf8
& $cmake -S $root -B $out -G Ninja ('-DCMAKE_PROJECT_INCLUDE=' + $include) ('-DCMAKE_MAKE_PROGRAM=' + $ninja) -DCMAKE_BUILD_TYPE=Release -DCMAKE_POLICY_DEFAULT_CMP0141=NEW -DCMAKE_MSVC_DEBUG_INFORMATION_FORMAT=Embedded > (Join-Path $ReportDirectory 'cmake-configure.log') 2>&1
if ($LASTEXITCODE) { throw 'CMake 配置失败。' }
& $cmake --build $out --clean-first --parallel 2 > (Join-Path $ReportDirectory 'cmake-build.log') 2>&1
if ($LASTEXITCODE) { throw 'CMake 编译失败。' }
& $ninja -C $out -t deps 'CMakeFiles/ra2missiontests.dir/tests/missions_test.c.obj' > (Join-Path $ReportDirectory 'cmake-header-deps.txt')
if ($LASTEXITCODE -or -not (Select-String -LiteralPath (Join-Path $ReportDirectory 'cmake-header-deps.txt') -Pattern '[/\\]battle\.h$' -Quiet)) { throw 'CMake 没有记录战场头文件依赖。' }
& $ctest --test-dir $out --output-on-failure > (Join-Path $ReportDirectory 'ctest.log') 2>&1
if ($LASTEXITCODE) { throw 'CTest 验证失败。' }
$testDefinitions = & $ctest --test-dir $out --show-only=json-v1 | ConvertFrom-Json
if ($LASTEXITCODE) { throw '无法读取 CTest 测试清单。' }
[ordered]@{passed=$true;tests=$testDefinitions.tests.Count;requested_compiler_language='1033';actual_include_prefix=$prefix;clean_build=$true;battle_header_dependency=$true;directory=$out} | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $ReportDirectory 'cmake.json') -Encoding utf8
