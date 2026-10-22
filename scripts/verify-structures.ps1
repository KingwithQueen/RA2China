param(
    [string]$Baseline = 'H:\开发\运行版本\原版1.006',
    [string]$ReportDirectory,
    [switch]$SkipBuild,
    [switch]$AddressSanitizer
)
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot
if (-not $ReportDirectory) { $ReportDirectory = Join-Path $root ('reports\structures-' + [DateTime]::UtcNow.ToString('yyyyMMdd-HHmmss')) }
$ReportDirectory = [IO.Path]::GetFullPath($ReportDirectory)
New-Item -ItemType Directory -Path $ReportDirectory -Force | Out-Null
function Inputs {
    @(foreach ($name in @('game.exe','ra2.mix','LANGUAGE.MIX','MULTI.MIX','MAPS01.MIX','MAPS02.MIX','RA2.INI')) { Get-FileHash -LiteralPath (Join-Path $Baseline $name) -Algorithm SHA256 })
}
function Sources {
    @(Get-ChildItem -LiteralPath (Join-Path $root 'src'),(Join-Path $root 'include'),(Join-Path $root 'tests'),(Join-Path $root 'scripts') -Recurse -File | ForEach-Object { Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256 }) +
    @(Get-FileHash -LiteralPath (Join-Path $root 'build.ps1'),(Join-Path $root 'CMakeLists.txt') -Algorithm SHA256)
}
function Inventory {
    @(Get-ChildItem -LiteralPath 'H:\开发' -Recurse -File -Force | Sort-Object FullName | ForEach-Object { '{0}`t{1}`t{2}' -f $_.FullName,$_.Length,$_.LastWriteTimeUtc.Ticks })
}
function Run([string]$Program, [string[]]$Arguments, [string]$Log) {
    & $Program @Arguments > $Log 2> ($Log + '.stderr.txt')
    if ($LASTEXITCODE) { throw "验证失败：$Program，详见 $Log" }
    $result = Get-Content -LiteralPath $Log -Raw | ConvertFrom-Json
    if (($result.PSObject.Properties.Name -contains 'failures') -and $result.failures -ne 0) { throw "检查失败：$Log" }
    if (($result.PSObject.Properties.Name -contains 'passed') -and -not $result.passed) { throw "检查失败：$Log" }
}
if (-not (Test-Path -LiteralPath (Join-Path $ReportDirectory 'inputs-before.json'))) { Inputs | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $ReportDirectory 'inputs-before.json') -Encoding utf8 }
if (-not (Test-Path -LiteralPath (Join-Path $ReportDirectory 'old-before.tsv'))) { Inventory | Set-Content -LiteralPath (Join-Path $ReportDirectory 'old-before.tsv') -Encoding utf8 }
$before = Sources
$before | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $ReportDirectory 'sources-before.json') -Encoding utf8
$problem = $null
$units = @()
$windows = @()
$corpusSummary = @()
$sourceDirectory = Join-Path $ReportDirectory 'sources'
New-Item -ItemType Directory -Path $sourceDirectory -Force | Out-Null
try {
    if (-not $SkipBuild) { & (Join-Path $root 'build.ps1') > (Join-Path $ReportDirectory 'build.log') 2>&1 }
    if ($AddressSanitizer) { & (Join-Path $root 'build.ps1') -AddressSanitizer > (Join-Path $ReportDirectory 'asan-build.log') 2>&1 }
    foreach ($variant in @('normal','asan')) {
        if ($variant -eq 'asan' -and -not $AddressSanitizer) { continue }
        $binary = Join-Path $root $(if ($variant -eq 'normal') { 'build' } else { 'build\asan' })
        $directory = Join-Path $ReportDirectory $variant
        New-Item -ItemType Directory -Path $directory -Force | Out-Null
        $tests = @('ra2tests','ra2rulestests','ra2assettests','ra2voxeltests','ra2maptests','ra2battletests','ra2combattests','ra2missiontests','ra2physicstests','ra2locomotortests','ra2layerstests','ra2bridgetests','ra2rendertests','ra2structuretests')
        $sum = 0
        foreach ($name in $tests) {
            $log = Join-Path $directory ($name+'.json')
            Run (Join-Path $binary ($name+'.exe')) @() $log
            $sum += (Get-Content -LiteralPath $log -Raw | ConvertFrom-Json).checks
        }
        $units += [ordered]@{variant=$variant;suites=$tests.Count;checks=$sum}
        $log = Join-Path $directory 'corpus.json'
        Run (Join-Path $binary 'ra2structurecheck.exe') @('--original',$Baseline,'--corpus','--validate-images','--sources',$sourceDirectory) $log
        $data = Get-Content -LiteralPath $log -Raw | ConvertFrom-Json
        if ($data.map_count -ne 131 -or $data.complete_game) { throw '原版场景数量或完成状态错误。' }
        $corpusSummary += [ordered]@{variant=$variant;maps=$data.map_count;structures=($data.maps | Measure-Object -Property structures -Sum).Sum;tanks=($data.maps | Measure-Object -Property tanks -Sum).Sum;pending_objects=@($data.maps.pending_objects).Count;missing_visuals=($data.maps | Measure-Object -Property missing_visuals -Sum).Sum;missing_layers=($data.maps | Measure-Object -Property missing_layers -Sum).Sum}
        $specifications = @(@{map='MP05MW.map';kind='structures';argument='--self-test-structures'})
        if ($variant -eq 'normal') {
            $specifications += @(@{map='all01t.map';kind='campaign-allied';argument='--self-test-scenario'},@{map='sov01t.map';kind='campaign-soviet';argument='--self-test-scenario'},@{map='all02s.map';kind='campaign-snow';argument='--self-test-scenario'},@{map='MP06T2.map';kind='bridge-regression';argument='--self-test-layers'})
        } else { $specifications += @{map='all01t.map';kind='campaign-allied';argument='--self-test-scenario'} }
        foreach ($spec in $specifications) {
            $window = Join-Path $directory $spec.kind
            New-Item -ItemType Directory -Path $window -Force | Out-Null
            $log = Join-Path $window 'window.json'
            Run (Join-Path $binary 'ra2battle.exe') @('--original',$Baseline,'--map',$spec.map,$spec.argument,$window) $log
            $windows += [ordered]@{variant=$variant;map=$spec.map;kind=$spec.kind;result=(Get-Content -LiteralPath $log -Raw | ConvertFrom-Json)}
        }
        if ($variant -eq 'normal') {
            Run (Join-Path $binary 'ra2rendertests.exe') @($Baseline,$directory) (Join-Path $directory 'original-render.json')
        }
    }
    if ($AddressSanitizer) {
        foreach ($relative in @('corpus.json','structures\building-combat.rpl','campaign-allied\scenario-native.rpl')) {
            $normal = Get-FileHash -LiteralPath (Join-Path $ReportDirectory ('normal\'+$relative)) -Algorithm SHA256
            $asan = Get-FileHash -LiteralPath (Join-Path $ReportDirectory ('asan\'+$relative)) -Algorithm SHA256
            if ($normal.Hash -ne $asan.Hash) { throw "普通版和 ASAN 输出不同：$relative" }
        }
    }
    Run 'E:\Program Files\Python\python.exe' @('-B',(Join-Path $PSScriptRoot 'verify-scenario-data.py'),(Join-Path $ReportDirectory 'normal\corpus.json'),(Join-Path $ReportDirectory 'independent-data.json')) (Join-Path $ReportDirectory 'independent-data.log')
    # 新协议改变摘要，但原有桥梁与坦克的实际数值不得改变。
    $log = Join-Path $ReportDirectory 'bridge-scalar.json'
    Run (Join-Path $root 'build\ra2battlecheck.exe') @('--original',$Baseline,'--map','MP06T2.map','--bridge-life') $log
    $old = Get-Content -LiteralPath (Join-Path $root 'reports\destination-render-20261019\old-replay.json') -Raw | ConvertFrom-Json
    $actual = Get-Content -LiteralPath $log -Raw | ConvertFrom-Json
    foreach ($key in @('tick','commands','fired','impacts','kills','dropped_shots','bridge_parts','bridge_hits','destroyed_segments','repaired_segments','bridge_falls')) {
        if ($old.$key -ne $actual.$key) { throw "旧场景实际数值变化：$key" }
    }
    if (($old.units | ConvertTo-Json -Depth 4 -Compress) -cne ($actual.units | ConvertTo-Json -Depth 4 -Compress)) { throw '旧桥梁场景单位状态变化。' }
    & (Join-Path $PSScriptRoot 'verify-cmake.ps1') -ReportDirectory (Join-Path $ReportDirectory 'cmake') > (Join-Path $ReportDirectory 'cmake.log') 2>&1
    $after = Sources
    if (@(Compare-Object $before $after -Property Path,Hash).Count) { throw '验证期间产品源码发生变化。' }
    $inputsAfter = Inputs
    $inputsAfter | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $ReportDirectory 'inputs-after.json') -Encoding utf8
    $inputsBefore = Get-Content -LiteralPath (Join-Path $ReportDirectory 'inputs-before.json') -Raw | ConvertFrom-Json
    if (@(Compare-Object $inputsBefore $inputsAfter -Property Path,Hash).Count) { throw '原始输入发生变化。' }
    $oldAfter = Inventory
    $oldAfter | Set-Content -LiteralPath (Join-Path $ReportDirectory 'old-after.tsv') -Encoding utf8
    $oldBefore = Get-Content -LiteralPath (Join-Path $ReportDirectory 'old-before.tsv') -Encoding utf8
    $changes = @(Compare-Object $oldBefore $oldAfter)
    $paths = @($changes | ForEach-Object { [regex]::Split($_.InputObject, [regex]::Escape('`t'))[0] } | Sort-Object -Unique)
    $unexpected = @($paths | Where-Object { -not $_.StartsWith('H:\开发\研究资料\中国阵营重设计\', [StringComparison]::OrdinalIgnoreCase) -or [IO.Path]::GetExtension($_) -ne '.md' })
    $changes | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $ReportDirectory 'old-changes.json') -Encoding utf8
    if ($unexpected.Count) { throw '旧目录出现设计 Markdown 之外的变化。' }
    $protection = [ordered]@{files_before=$oldBefore.Count;files_after=$oldAfter.Count;concurrent_design_files=$paths;unexpected_changes=$unexpected.Count;original_inputs_unchanged=7}
} catch { $problem = $_.Exception.Message }
$record = [ordered]@{passed=($null -eq $problem);error=$problem;unit_results=$units;windows=$windows;corpus=$corpusSummary;protection=$protection;simulation_version=8;replay_format='RA2RPL10';campaign_runtime=$false;complete_skirmish=$false;binary=(Get-FileHash -LiteralPath (Join-Path $root 'build\ra2battle.exe') -Algorithm SHA256)}
$record | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath (Join-Path $ReportDirectory 'validation.json') -Encoding utf8
if ($problem) { throw $problem }
Write-Output '建筑、原始场景对象、回放、窗口和资源保护验证通过。'
