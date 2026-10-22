param([switch]$SkipBuild, [switch]$AddressSanitizer, [string]$ReportDirectory = 'reports\economy-20261020')
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot
Set-Location -LiteralPath $root
$report = [IO.Path]::GetFullPath($ReportDirectory)
New-Item -ItemType Directory -Path $report -Force | Out-Null
if (-not (Test-Path -LiteralPath (Join-Path $report 'inputs-before.json'))) {
    $inputs = @(foreach ($name in @('game.exe','ra2.mix','LANGUAGE.MIX','MULTI.MIX','MAPS01.MIX','MAPS02.MIX','RA2.INI')) { Get-FileHash -LiteralPath (Join-Path 'H:\开发\运行版本\原版1.006' $name) })
    $inputs | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $report 'inputs-before.json') -Encoding utf8
}
if (-not (Test-Path -LiteralPath (Join-Path $report 'old-before.tsv'))) {
    Get-ChildItem -LiteralPath 'H:\开发' -Recurse -File -Force | Sort-Object FullName | ForEach-Object { '{0}`t{1}`t{2}' -f $_.FullName,$_.Length,$_.LastWriteTimeUtc.Ticks } | Set-Content -LiteralPath (Join-Path $report 'old-before.tsv') -Encoding utf8
}
function Run([string]$Program, [string[]]$Arguments, [string]$Log) {
    & $Program @Arguments > $Log 2> ($Log + '.stderr.txt')
    if ($LASTEXITCODE) { throw "验证失败：$Program；详见 $Log" }
    $result = Get-Content -LiteralPath $Log -Raw | ConvertFrom-Json
    if (($result.PSObject.Properties.Name -contains 'failures') -and $result.failures -ne 0) { throw "检查失败：$Log" }
    if (($result.PSObject.Properties.Name -contains 'passed') -and -not $result.passed) { throw "检查失败：$Log" }
}
function Sources {
    @(Get-ChildItem -LiteralPath src,include,tests,scripts -Recurse -File | Where-Object { $_.Extension -ne '.pyc' } | Sort-Object FullName | ForEach-Object { Get-FileHash -LiteralPath $_.FullName }) + @(Get-FileHash build.ps1,CMakeLists.txt)
}
$before = Sources
$before | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $report 'sources-before.json') -Encoding utf8
if (-not $SkipBuild) { & .\build.ps1 > (Join-Path $report 'build.log') 2>&1 }
if ($AddressSanitizer) { & .\build.ps1 -AddressSanitizer > (Join-Path $report 'asan-build.log') 2>&1 }
$suites = @('ra2tests','ra2rulestests','ra2assettests','ra2voxeltests','ra2maptests','ra2battletests','ra2combattests','ra2missiontests','ra2physicstests','ra2locomotortests','ra2layerstests','ra2bridgetests','ra2rendertests','ra2structuretests','ra2economytests')
$units = @(); $windows = @()
foreach ($variant in @('normal','asan')) {
    if ($variant -eq 'asan' -and -not $AddressSanitizer) { continue }
    $binary = Join-Path $root $(if ($variant -eq 'normal') { 'build' } else { 'build\asan' })
    $dir = Join-Path $report $variant
    New-Item -ItemType Directory -Path $dir -Force | Out-Null
    $checks = 0
    foreach ($name in $suites) {
        $log = Join-Path $dir ($name + '.json')
        Run (Join-Path $binary ($name + '.exe')) @() $log
        $checks += (Get-Content -LiteralPath $log -Raw | ConvertFrom-Json).checks
    }
    $units += [ordered]@{variant=$variant;suites=$suites.Count;checks=$checks}
    if ($variant -eq 'normal') {
        foreach ($spec in @(@{name='bridge-regression';flag='--self-test-layers';map='MP06T2.map'},@{name='campaign-regression';flag='--self-test-scenario';map='all01t.map'})) {
            $window = Join-Path $dir $spec.name
            New-Item -ItemType Directory -Path $window -Force | Out-Null
            Run (Join-Path $binary 'ra2battle.exe') @($spec.flag,$window,'--map',$spec.map) (Join-Path $window 'window.json')
        }
    }
    foreach ($side in @('soviet','allied')) {
        $window = Join-Path $dir $side
        New-Item -ItemType Directory -Path $window -Force | Out-Null
        $arguments = @('--self-test-economy',$window,'--map',$(if ($side -eq 'soviet') { 'MP17T6.map' } else { 'MP32S8.map' }))
        if ($side -eq 'allied') { $arguments += '--allied' }
        $log = Join-Path $window 'window.json'
        Run (Join-Path $binary 'ra2battle.exe') $arguments $log
        $result = Get-Content -LiteralPath $log -Raw | ConvertFrom-Json
        if ($result.built -ne 6 -or $result.produced -lt 2 -or $result.earned -eq 0 -or $result.paired_steps -lt 6000 -or $result.version -ne 9 -or $result.complete_game) { throw '经济场景验收内容不足。' }
        $windows += [ordered]@{variant=$variant;side=$side;result=$result;path=$log}
        Run 'E:\Program Files\Python\python.exe' @('-B','scripts/verify-economy-data.py',(Join-Path $window 'economy-rules.json'),'reports/structures-20261020/sources') (Join-Path $window 'independent.json')
    }
}
if ($AddressSanitizer) {
    foreach ($side in @('soviet','allied')) {
        foreach ($name in @('economy.rpl','economy-rules.json')) {
            if ((Get-FileHash (Join-Path $report ('normal\'+$side+'\'+$name))).Hash -ne (Get-FileHash (Join-Path $report ('asan\'+$side+'\'+$name))).Hash) { throw "普通版与内存检查版不一致：$side/$name" }
        }
    }
}
$after = Sources
$after | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $report 'sources-after.json') -Encoding utf8
if (Compare-Object $before $after -Property Path,Hash) { throw '验收期间源码发生变化。' }
$inputs = @(foreach ($name in @('game.exe','ra2.mix','LANGUAGE.MIX','MULTI.MIX','MAPS01.MIX','MAPS02.MIX','RA2.INI')) { Get-FileHash -LiteralPath (Join-Path 'H:\开发\运行版本\原版1.006' $name) })
$inputs | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $report 'inputs-after.json') -Encoding utf8
if (Compare-Object (Get-Content (Join-Path $report 'inputs-before.json') -Raw | ConvertFrom-Json) $inputs -Property Path,Hash) { throw '原始资源发生变化。' }
$inventory = @(Get-ChildItem -LiteralPath 'H:\开发' -Recurse -File -Force | Sort-Object FullName | ForEach-Object { '{0}`t{1}`t{2}' -f $_.FullName,$_.Length,$_.LastWriteTimeUtc.Ticks })
$inventory | Set-Content -LiteralPath (Join-Path $report 'old-after.tsv') -Encoding utf8
$changes = @(Compare-Object (Get-Content (Join-Path $report 'old-before.tsv')) $inventory)
$changes | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $report 'old-changes.json') -Encoding utf8
foreach ($change in $changes) {
    if ($change.InputObject -notmatch '^H:\\开发\\研究资料\\中国阵营重设计\\.*\.md`t') { throw '旧项目有预期外变动。' }
}
$result = [ordered]@{passed=$true;simulation=9;replay='RA2RPL11';units=$units;windows=$windows;inputs_unchanged=$true;old_project_changed_entries=$changes.Count;complete_game=$false;original_runtime_calibration=$false;exe=(Join-Path $root 'build\ra2battle.exe');exe_sha256=(Get-FileHash build\ra2battle.exe).Hash;rollback='build/economy-preserved'}
$result | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath (Join-Path $report 'validation.json') -Encoding utf8
$result | ConvertTo-Json -Depth 12
