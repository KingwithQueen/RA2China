param(
    [string]$Baseline = 'H:\开发\运行版本\原版1.006',
    [string]$ReportDirectory,
    [switch]$SkipBuild,
    [switch]$Resume,
    [switch]$AddressSanitizer
)
$ErrorActionPreference = 'Stop'
$env:PYTHONIOENCODING = 'utf-8'
$root = Split-Path $PSScriptRoot
if (-not $ReportDirectory) { $ReportDirectory = Join-Path $root ('reports\rendering-' + [DateTime]::UtcNow.ToString('yyyyMMdd-HHmmss')) }
$ReportDirectory = [IO.Path]::GetFullPath($ReportDirectory)
New-Item -ItemType Directory -Force -Path $ReportDirectory | Out-Null
function Run([string]$Program, [string[]]$Arguments, [string]$Log) {
    if ($Resume -and (Test-Path -LiteralPath $Log) -and (Get-Item -LiteralPath $Log).Length -gt 0) {
        $saved = Get-Content -LiteralPath $Log -Raw | ConvertFrom-Json
        if (($saved.PSObject.Properties.Name -contains 'failures') -and $saved.failures -ne 0) { throw "不能复用失败记录：$Log" }
        if (($saved.PSObject.Properties.Name -contains 'passed') -and -not $saved.passed) { throw "不能复用失败记录：$Log" }
        return
    }
    & $Program @Arguments > $Log 2> ($Log + '.stderr.txt')
    if ($LASTEXITCODE) { throw "验证失败：$Program，详见 $Log" }
}
function Sources {
    @(Get-ChildItem -LiteralPath (Join-Path $root 'src'),(Join-Path $root 'include'),(Join-Path $root 'tests'),(Join-Path $root 'scripts') -File -Recurse | ForEach-Object { Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256 }) +
    @(Get-FileHash -LiteralPath (Join-Path $root 'build.ps1'),(Join-Path $root 'CMakeLists.txt') -Algorithm SHA256)
}
function Inputs {
    @(foreach ($name in @('game.exe','ra2.mix','LANGUAGE.MIX','MULTI.MIX','MAPS01.MIX','MAPS02.MIX','RA2.INI')) { Get-FileHash -LiteralPath (Join-Path $Baseline $name) -Algorithm SHA256 })
}
function Inventory {
    @(Get-ChildItem -LiteralPath 'H:\开发' -Recurse -File -Force | Sort-Object FullName | ForEach-Object { '{0}`t{1}`t{2}' -f $_.FullName,$_.Length,$_.LastWriteTimeUtc.Ticks })
}
$sourceBefore = Sources
if ($Resume) {
    if (-not $SkipBuild) { throw '续验必须使用 SkipBuild，不能改变已验程序。' }
    $prefixSources = Get-Content -LiteralPath (Join-Path $ReportDirectory 'source-prefix.json') -Raw | ConvertFrom-Json
    $changedSources = @(Compare-Object $prefixSources $sourceBefore -Property Path,Hash | Where-Object { $_.Path -ne $PSCommandPath })
    if ($changedSources.Count) { throw '前段验证之后产品源码或其他验证工具已变化，不能续验。' }
    $prefixProducts = Get-Content -LiteralPath (Join-Path $ReportDirectory 'products-prefix.json') -Raw | ConvertFrom-Json
    foreach ($product in $prefixProducts) {
        if ((Get-FileHash -LiteralPath $product.Path -Algorithm SHA256).Hash -ne $product.Hash) { throw "前段程序已变化：$($product.Path)" }
    }
}
$sourceBefore | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $ReportDirectory 'source-before.json') -Encoding utf8
if (-not (Test-Path -LiteralPath (Join-Path $ReportDirectory 'inputs-before.json'))) { Inputs | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $ReportDirectory 'inputs-before.json') -Encoding utf8 }
if (-not (Test-Path -LiteralPath (Join-Path $ReportDirectory 'old-before.tsv'))) { Inventory | Set-Content -LiteralPath (Join-Path $ReportDirectory 'old-before.tsv') -Encoding utf8 }
$previous = Get-Content -LiteralPath (Join-Path $root 'reports\latest-bridges.json') -Raw | ConvertFrom-Json
$previousValidation = Get-Content -LiteralPath $previous.validation -Raw | ConvertFrom-Json
$tests = @('ra2tests','ra2rulestests','ra2assettests','ra2voxeltests','ra2maptests','ra2battletests','ra2combattests','ra2missiontests','ra2physicstests','ra2locomotortests','ra2layerstests','ra2bridgetests','ra2rendertests')
$problem = $null
$units = @()
$replays = @()
$windows = @()
try {
    if (-not $SkipBuild) {
        & (Join-Path $root 'build.ps1') > (Join-Path $ReportDirectory 'build.log') 2>&1
        if ($AddressSanitizer) { & (Join-Path $root 'build.ps1') -AddressSanitizer > (Join-Path $ReportDirectory 'asan-build.log') 2>&1 }
    }
    foreach ($variant in @('normal','asan')) {
        if ($variant -eq 'asan' -and -not $AddressSanitizer) { continue }
        $binary = Join-Path $root $(if ($variant -eq 'normal') { 'build' } else { 'build\asan' })
        $directory = Join-Path $ReportDirectory $variant
        New-Item -ItemType Directory -Force -Path $directory | Out-Null
        $sum = 0
        foreach ($name in $tests) {
            $log = Join-Path $directory ($name + '.json')
            Run (Join-Path $binary ($name + '.exe')) @() $log
            $sum += (Get-Content -LiteralPath $log -Raw | ConvertFrom-Json).checks
        }
        $units += [ordered]@{variant=$variant;suites=$tests.Count;checks=$sum}
        Run (Join-Path $binary 'ra2rendertests.exe') @($Baseline,$directory) (Join-Path $directory 'original-render.json')
        Run 'E:\Program Files\Python\python.exe' @('-B',(Join-Path $PSScriptRoot 'reference-rendering.py'),(Join-Path $binary 'ra2rendertests.exe'),(Join-Path $directory 'native-rendering.json')) (Join-Path $directory 'native-reference.log')
        $bridgeMaps = if ($variant -eq 'normal') { @('MP06T2','MP18S3','MP33U4') } else { @('MP06T2') }
        foreach ($map in $bridgeMaps) {
            $arguments = @('--original',$Baseline,'--map',($map+'.map'),'--trace','--bridge-life','--replay',(Join-Path $previous.directory ('normal\'+$map+'\lifecycle.rpl')))
            $log = Join-Path $directory ('old-'+$map+'.json')
            Run (Join-Path $binary 'ra2battlecheck.exe') $arguments $log
            $actual = Get-Content -LiteralPath $log -Raw | ConvertFrom-Json
            $expected = @($previousValidation.samples | Where-Object { $_.variant -eq 'normal' -and $_.map -eq ($map+'.map') -and $_.mode -eq 'bridge_life' })[0].record
            if (-not $actual.replay_verified -or $actual.sha1 -cne $expected.sha1 -or $actual.trace_sha1 -cne $expected.trace_sha1) { throw "旧回放不一致：$variant/$map" }
            $replays += [ordered]@{variant=$variant;map=$map;mode='old_bridge';ticks=$actual.tick;sha1=$actual.sha1;trace_sha1=$actual.trace_sha1}
        }
        $missionMaps = if ($variant -eq 'normal') { @('MP05MW','MP13DU','MP29U2') } else { @() }
        foreach ($map in $missionMaps) {
            $arguments = @('--original',$Baseline,'--map',($map+'.map'),'--missions')
            $file = Join-Path $directory ($map+'.rpl')
            Run (Join-Path $binary 'ra2battlecheck.exe') ($arguments + @('--output',$file)) (Join-Path $directory ($map+'-record.json'))
            Run (Join-Path $binary 'ra2battlecheck.exe') ($arguments + @('--replay',$file)) (Join-Path $directory ($map+'-replay.json'))
            $record = Get-Content -LiteralPath (Join-Path $directory ($map+'-record.json')) -Raw | ConvertFrom-Json
            $played = Get-Content -LiteralPath (Join-Path $directory ($map+'-replay.json')) -Raw | ConvertFrom-Json
            if (-not $played.replay_verified -or $record.sha1 -cne $played.sha1 -or $record.trace_sha1 -cne $played.trace_sha1) { throw "新回放不一致：$variant/$map" }
            $replays += [ordered]@{variant=$variant;map=$map;mode='new_missions';ticks=$played.tick;sha1=$played.sha1;trace_sha1=$played.trace_sha1}
        }
        $bridgeWindows = if ($variant -eq 'normal') { @('MP06T2','MP18S3','MP23MW') } else { @('MP23MW') }
        foreach ($map in $bridgeWindows) {
            $window = Join-Path $directory ('bridge-'+$map)
            New-Item -ItemType Directory -Force -Path $window | Out-Null
            $log = Join-Path $window 'window.json'
            Run (Join-Path $binary 'ra2battle.exe') @('--original',$Baseline,'--map',($map+'.map'),'--self-test-bridges',$window) $log
            $windows += [ordered]@{variant=$variant;map=$map;mode='bridge';result=(Get-Content -LiteralPath $log -Raw | ConvertFrom-Json)}
        }
        $maps = if ($variant -eq 'normal') { @('MP05MW','MP13DU','MP29U2') } else { @('MP13DU') }
        foreach ($map in $maps) {
            $window = Join-Path $directory ('window-'+$map)
            New-Item -ItemType Directory -Force -Path $window | Out-Null
            $log = Join-Path $window 'window.json'
            Run (Join-Path $binary 'ra2battle.exe') @('--original',$Baseline,'--map',($map+'.map'),'--self-test',$window) $log
            $windows += [ordered]@{variant=$variant;map=$map;mode='input';result=(Get-Content -LiteralPath $log -Raw | ConvertFrom-Json)}
        }
        $window = Join-Path $directory 'window-slopes'
        New-Item -ItemType Directory -Force -Path $window | Out-Null
        Run (Join-Path $binary 'ra2battle.exe') @('--original',$Baseline,'--map','MP06T2.map','--self-test-layers',$window) (Join-Path $window 'window.json')
        $windows += [ordered]@{variant=$variant;mode='slopes';result=(Get-Content -LiteralPath (Join-Path $window 'window.json') -Raw | ConvertFrom-Json)}
    }
    Run (Join-Path $root 'build\ra2battlecheck.exe') @('--original',$Baseline,'--corpus') (Join-Path $ReportDirectory 'map-corpus.json')
    $corpus = Get-Content -LiteralPath (Join-Path $ReportDirectory 'map-corpus.json') -Raw | ConvertFrom-Json
    $oldCorpus = Get-Content -LiteralPath (Join-Path $previous.directory 'map-corpus.json') -Raw | ConvertFrom-Json
    if ($corpus.maps -ne $oldCorpus.maps -or $corpus.cells -ne $oldCorpus.cells -or $corpus.missing -ne $oldCorpus.missing) { throw '原版地图语料发生变化。' }
    & (Join-Path $PSScriptRoot 'verify-cmake.ps1') -ReportDirectory $ReportDirectory
} catch { $problem = $_.Exception.Message }
$sourceAfter = Sources
$sourceAfter | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $ReportDirectory 'source-after.json') -Encoding utf8
$sourceUnchanged = @(Compare-Object $sourceBefore $sourceAfter -Property Path,Hash).Count -eq 0
$inputsBefore = Get-Content -LiteralPath (Join-Path $ReportDirectory 'inputs-before.json') -Raw | ConvertFrom-Json
$inputsAfter = Inputs
$inputsAfter | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $ReportDirectory 'inputs-after.json') -Encoding utf8
$inputsUnchanged = @(Compare-Object $inputsBefore $inputsAfter -Property Path,Hash).Count -eq 0
$oldBefore = @(Get-Content -LiteralPath (Join-Path $ReportDirectory 'old-before.tsv'))
$oldAfter = Inventory
$oldAfter | Set-Content -LiteralPath (Join-Path $ReportDirectory 'old-after.tsv') -Encoding utf8
$changes = @(Compare-Object $oldBefore $oldAfter)
$changedPaths = @($changes | ForEach-Object { ($_.InputObject -split '`t')[0] } | Sort-Object -Unique)
$unexpected = @($changedPaths | Where-Object { -not ($_.StartsWith('H:\开发\研究资料\中国阵营重设计\',[StringComparison]::OrdinalIgnoreCase) -and [IO.Path]::GetExtension($_) -eq '.md') })
$validation = [ordered]@{
    passed=($null -eq $problem -and $sourceUnchanged -and $inputsUnchanged -and $unexpected.Count -eq 0)
    error=$problem;unit_results=$units;replays=$replays;native_windows=$windows
    simulation_version=7;replay_magic='RA2RPL9';source_unchanged=$sourceUnchanged;inputs_unchanged=$inputsUnchanged
    original_input_count=$inputsAfter.Count;old_files=$oldAfter.Count;old_project_preserved=($unexpected.Count -eq 0);concurrent_design_changes=$changedPaths
    resumed=[bool]$Resume;resumed_product_fingerprints_verified=[bool]$Resume
    executable_sha256=(Get-FileHash -LiteralPath (Join-Path $root 'build\ra2battle.exe') -Algorithm SHA256).Hash.ToLowerInvariant()
    scope='桥梁锚点、固定比例与原点、统一车身/炮塔/坡面方向、三剧场单位调色板；不宣称完整原版光照、阴影及栏杆逐像素遮挡一致。'
}
$validation | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath (Join-Path $ReportDirectory 'validation.json') -Encoding utf8
if (-not $validation.passed) { throw "渲染验证未通过：$problem；源码=$sourceUnchanged，输入=$inputsUnchanged，旧项目意外变化=$($unexpected.Count)" }
$pointer = [ordered]@{validation=(Join-Path $ReportDirectory 'validation.json');directory=$ReportDirectory}
foreach ($name in @('latest-rendering.json','latest-battle.json')) { $pointer | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $root ('reports\'+$name)) -Encoding utf8 }
$validation | ConvertTo-Json -Depth 10
