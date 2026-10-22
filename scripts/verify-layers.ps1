param(
    [string]$Baseline = 'H:\开发\运行版本\原版1.006',
    [string]$OldProject = 'H:\开发',
    [string]$ReportDirectory,
    [string]$ConcurrentDesignDirectory,
    [switch]$SkipBuild,
    [switch]$AddressSanitizer
)
$ErrorActionPreference = 'Stop'
$env:PYTHONIOENCODING = 'utf-8'
$root = Split-Path $PSScriptRoot
if (-not $ReportDirectory) { $ReportDirectory = Join-Path $root ('reports\layers-' + [DateTime]::UtcNow.ToString('yyyyMMdd-HHmmss')) }
New-Item -ItemType Directory -Force -Path $ReportDirectory | Out-Null
$previous = Get-Content -Raw -LiteralPath (Join-Path $root 'reports\latest-locomotor.json') | ConvertFrom-Json
function Fingerprints {
    @(foreach ($name in @('game.exe','ra2.mix','LANGUAGE.MIX','MULTI.MIX','MAPS01.MIX','MAPS02.MIX','RA2.INI')) { Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $Baseline $name) })
}
function Inventory {
    @(Get-ChildItem -LiteralPath $OldProject -File -Recurse -Force | Sort-Object FullName | ForEach-Object { '{0}`t{1}`t{2}' -f $_.FullName,$_.Length,$_.LastWriteTimeUtc.Ticks })
}
function Run([string]$Program, [string[]]$Arguments, [string]$Log) {
    # 让重定向直接创建日志，避免先创建再立即重开产生临时共享冲突。
    & $Program @Arguments > $Log 2> ($Log + '.stderr.txt')
    if ($LASTEXITCODE) { throw "验证失败：$Program，详见 $Log" }
}
function ReadJson([string]$Name) { Get-Content -Raw -LiteralPath (Join-Path $ReportDirectory $Name) | ConvertFrom-Json }
function Sources {
    @(Get-ChildItem -LiteralPath (Join-Path $root 'src'),(Join-Path $root 'include'),(Join-Path $root 'tests'),(Join-Path $root 'scripts') -File -Recurse | Sort-Object FullName | ForEach-Object { Get-FileHash -Algorithm SHA256 -LiteralPath $_.FullName }) +
    @(Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $root 'build.ps1'),(Join-Path $root 'CMakeLists.txt'))
}
$sourceBefore = Sources
$sourceBefore | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $ReportDirectory 'source-before.json') -Encoding utf8
$beforeFile = Join-Path $ReportDirectory 'inputs-before.json'
$oldFile = Join-Path $ReportDirectory 'old-before.tsv'
if (-not (Test-Path -LiteralPath $beforeFile)) { Fingerprints | ConvertTo-Json | Set-Content -LiteralPath $beforeFile -Encoding utf8 }
if (-not (Test-Path -LiteralPath $oldFile)) { Inventory | Set-Content -LiteralPath $oldFile -Encoding utf8 }
$problem = $null
$samples = @()
$checks = 0
try {
    if (-not $SkipBuild) { & (Join-Path $root 'build.ps1') > (Join-Path $ReportDirectory 'build.log') }
    foreach ($name in @('ra2tests','ra2rulestests','ra2assettests','ra2voxeltests','ra2maptests','ra2battletests','ra2combattests','ra2missiontests','ra2physicstests','ra2locomotortests','ra2layerstests')) {
        Run (Join-Path $root ('build\' + $name + '.exe')) @() (Join-Path $ReportDirectory ($name + '.json'))
        $checks += (ReadJson ($name + '.json')).checks
    }
    Run 'E:\Program Files\Python\python.exe' @('-B',(Join-Path $root 'scripts\reference-motion.py'),(Join-Path $Baseline 'game.exe'),(Join-Path $ReportDirectory 'native-motion.json'),(Join-Path $root 'build\ra2motioncheck.exe')) (Join-Path $ReportDirectory 'motion-comparison.json')
    Run 'E:\Program Files\Python\python.exe' @('-B',(Join-Path $root 'scripts\reference-numbers.py'),(Join-Path $root 'build\ra2calibrationcheck.exe'),(Join-Path $ReportDirectory 'numbers.json')) (Join-Path $ReportDirectory 'numbers-comparison.json')
    Run 'E:\Program Files\Python\python.exe' @('-B',(Join-Path $root 'scripts\reference-physics.py'),(Join-Path $root 'build\ra2calibrationcheck.exe'),(Join-Path $ReportDirectory 'native-physics.json')) (Join-Path $ReportDirectory 'physics-comparison.json')
    Run 'E:\Program Files\Python\python.exe' @('-B',(Join-Path $root 'scripts\reference-locomotor.py'),(Join-Path $root 'build\ra2calibrationcheck.exe'),(Join-Path $ReportDirectory 'native-locomotor.json')) (Join-Path $ReportDirectory 'locomotor-comparison.json')
    Run 'E:\Program Files\Python\python.exe' @('-B',(Join-Path $root 'scripts\reference-layers.py'),(Join-Path $root 'build\ra2calibrationcheck.exe'),(Join-Path $ReportDirectory 'native-layers.json')) (Join-Path $ReportDirectory 'layers-comparison.json')
    foreach ($map in @('MP05MW.map','MP13DU.map','MP29U2.map')) {
        $short = [IO.Path]::GetFileNameWithoutExtension($map)
        $directory = Join-Path $ReportDirectory $short
        New-Item -ItemType Directory -Force -Path $directory | Out-Null
        $arguments = @('--original',$Baseline,'--map',$map)
        Run (Join-Path $root 'build\ra2battle.exe') ($arguments + @('--self-test',$directory)) (Join-Path $directory 'native.json')
        $native = ReadJson ($short + '\native.json')
        if ($native.failures -or -not $native.missions -or $native.simulation_version -ne 6 -or $native.hotkeys_from_original -ne 89) { throw '战场任务窗口验证未通过。' }
        Run (Join-Path $root 'build\ra2battlecheck.exe') ($arguments + @('--missions','--output',(Join-Path $directory 'reference.rpl'))) (Join-Path $directory 'record.json')
        Run (Join-Path $root 'build\ra2battlecheck.exe') ($arguments + @('--trace','--replay',(Join-Path $directory 'reference.rpl'))) (Join-Path $directory 'replay.json')
        $record = ReadJson ($short + '\record.json')
        $played = ReadJson ($short + '\replay.json')
        if (-not $played.replay_verified -or $played.sha1 -cne $record.sha1 -or -not $played.trace_enabled -or $played.trace_sha1 -cne $record.trace_sha1 -or $record.commands -ne 8 -or $record.dropped_shots) { throw '新任务回放摘要不一致。' }
        $oldDirectory = Join-Path $previous.directory $short
        & (Join-Path $root 'build\ra2battlecheck.exe') @arguments --replay (Join-Path $oldDirectory 'reference.rpl') > (Join-Path $directory 'v5-rejection.json') 2> (Join-Path $directory 'v5-rejection.stderr.txt')
        if ($LASTEXITCODE -ne 1 -or -not (Select-String -LiteralPath (Join-Path $directory 'v5-rejection.stderr.txt') -SimpleMatch 'unsupported replay format or simulation version' -Quiet)) { throw '旧协议未被明确拒绝。' }
        $samples += [ordered]@{map=$map;native=$native;record=$record;replay=$played;v5_rejected=$true}

    }
    $bridgeSamples = @()
    foreach ($map in @('MP06T2.map','MP18S3.map','MP33U4.map')) {
        $short = 'bridge-' + [IO.Path]::GetFileNameWithoutExtension($map)
        $directory = Join-Path $ReportDirectory $short
        New-Item -ItemType Directory -Force -Path $directory | Out-Null
        $arguments = @('--original',$Baseline,'--map',$map,'--layers')
        Run (Join-Path $root 'build\ra2battlecheck.exe') ($arguments + @('--output',(Join-Path $directory 'reference.rpl'))) (Join-Path $directory 'record.json')
        Run (Join-Path $root 'build\ra2battlecheck.exe') ($arguments + @('--replay',(Join-Path $directory 'reference.rpl'))) (Join-Path $directory 'replay.json')
        $record = ReadJson ($short + '\record.json')
        $played = ReadJson ($short + '\replay.json')
        if (-not $played.replay_verified -or $record.sha1 -cne $played.sha1 -or $record.trace_sha1 -cne $played.trace_sha1 -or $record.units[0].cell -ne $record.units[0].goal) { throw '实际桥梁地图回放或抵岸检查失败。' }
        $bridgeSamples += [ordered]@{map=$map;record=$record;replay=$played}
    }
    $directory = Join-Path $ReportDirectory 'bridge-native'
    New-Item -ItemType Directory -Force -Path $directory | Out-Null
    Run (Join-Path $root 'build\ra2battle.exe') @('--original',$Baseline,'--map','MP06T2.map','--self-test-layers',$directory) (Join-Path $directory 'native.json')
    if ((ReadJson 'bridge-native\native.json').failures) { throw '桥层窗口验证失败。' }
    Run (Join-Path $root 'build\ra2battlecheck.exe') @('--original',$Baseline,'--corpus') (Join-Path $ReportDirectory 'map-corpus.json')
    if ($AddressSanitizer) {
        & (Join-Path $root 'build.ps1') -AddressSanitizer > (Join-Path $ReportDirectory 'asan-build.log')
        foreach ($name in @('ra2tests','ra2rulestests','ra2assettests','ra2voxeltests','ra2maptests','ra2battletests','ra2combattests','ra2missiontests','ra2physicstests','ra2locomotortests','ra2layerstests')) {
            Run (Join-Path $root ('build\asan\' + $name + '.exe')) @() (Join-Path $ReportDirectory ($name + '-asan.json'))
            if ((ReadJson ($name + '.json')).checks -ne (ReadJson ($name + '-asan.json')).checks) { throw '正常版与内存检查版的检查数量不一致。' }
        }
        Run 'E:\Program Files\Python\python.exe' @('-B',(Join-Path $root 'scripts\reference-numbers.py'),(Join-Path $root 'build\asan\ra2calibrationcheck.exe'),(Join-Path $ReportDirectory 'numbers-asan.json')) (Join-Path $ReportDirectory 'numbers-asan-comparison.json')
        Run 'E:\Program Files\Python\python.exe' @('-B',(Join-Path $root 'scripts\reference-physics.py'),(Join-Path $root 'build\asan\ra2calibrationcheck.exe'),(Join-Path $ReportDirectory 'native-physics-asan.json')) (Join-Path $ReportDirectory 'physics-asan-comparison.json')
        Run 'E:\Program Files\Python\python.exe' @('-B',(Join-Path $root 'scripts\reference-locomotor.py'),(Join-Path $root 'build\asan\ra2calibrationcheck.exe'),(Join-Path $ReportDirectory 'native-locomotor-asan.json')) (Join-Path $ReportDirectory 'locomotor-asan-comparison.json')
        Run 'E:\Program Files\Python\python.exe' @('-B',(Join-Path $root 'scripts\reference-layers.py'),(Join-Path $root 'build\asan\ra2calibrationcheck.exe'),(Join-Path $ReportDirectory 'native-layers-asan.json')) (Join-Path $ReportDirectory 'layers-asan-comparison.json')
        $directory = Join-Path $ReportDirectory 'asan-native'
        New-Item -ItemType Directory -Force -Path $directory | Out-Null
        Run (Join-Path $root 'build\asan\ra2battle.exe') @('--original',$Baseline,'--self-test',$directory) (Join-Path $directory 'native.json')
        if ((ReadJson 'asan-native\native.json').failures) { throw '操作窗口内存检查未通过。' }
        $directory = Join-Path $ReportDirectory 'asan-bridge-native'
        New-Item -ItemType Directory -Force -Path $directory | Out-Null
        Run (Join-Path $root 'build\asan\ra2battle.exe') @('--original',$Baseline,'--map','MP06T2.map','--self-test-layers',$directory) (Join-Path $directory 'native.json')
        if ((ReadJson 'asan-bridge-native\native.json').failures) { throw '桥层窗口内存检查未通过。' }
    }
    & (Join-Path $PSScriptRoot 'verify-cmake.ps1') -ReportDirectory $ReportDirectory
} catch { $problem = $_.Exception.Message }
finally {
    $after = Fingerprints
    $sourceAfter = Sources
    $sourceAfter | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $ReportDirectory 'source-after.json') -Encoding utf8
    $sourceUnchanged = ($sourceBefore | ConvertTo-Json -Compress) -ceq ($sourceAfter | ConvertTo-Json -Compress)
    $oldAfter = Inventory
    $after | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $ReportDirectory 'inputs-after.json') -Encoding utf8
    $oldAfter | Set-Content -LiteralPath (Join-Path $ReportDirectory 'old-after.tsv') -Encoding utf8
    $before = Get-Content -Raw -LiteralPath $beforeFile | ConvertFrom-Json
    $inputsUnchanged = ($before | ConvertTo-Json -Compress) -ceq ($after | ConvertTo-Json -Compress)
    $oldBefore = Get-Content -LiteralPath $oldFile
    $differences = @(Compare-Object -ReferenceObject $oldBefore -DifferenceObject $oldAfter)
    $paths = @($differences | ForEach-Object { ($_.InputObject -split [regex]::Escape('`t'))[0] } | Sort-Object -Unique)
    $unaccepted = @($paths | Where-Object { -not $ConcurrentDesignDirectory -or [IO.Path]::GetDirectoryName($_) -ine $ConcurrentDesignDirectory -or [IO.Path]::GetExtension($_) -ine '.md' })
    $oldPreserved = $unaccepted.Count -eq 0
    $differences | Select-Object InputObject,SideIndicator | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $ReportDirectory 'concurrent-design-changes.json') -Encoding utf8
}
if (-not $inputsUnchanged -or -not $oldPreserved) { $problem = '原始输入或已确认的并行设计文档之外的旧文件发生变化。' }
if (-not $sourceUnchanged) { $problem = '验证期间源码发生变化，需要统一重建后重新验证。' }
$receipt = [ordered]@{
    passed=($null -eq $problem);error=$problem;scope='普通坦克的桥上桥下占格和桥口通行、静态坡面底盘与炮口、常规炮弹碰撞退场、基础候选过滤；隔离指令对照不替代原版整局验收'
    unit_checks=$checks;samples=$samples;bridge_samples=$bridgeSamples;bridge_native=$(if (-not $problem) { ReadJson 'bridge-native\native.json' });asan_requested=[bool]$AddressSanitizer;source_unchanged=$sourceUnchanged
    asan=$(if ($AddressSanitizer -and -not $problem) { ReadJson 'asan-native\native.json' })
    inputs_unchanged=$inputsUnchanged;input_count=$after.Count;old_project_unchanged=($differences.Count -eq 0);old_project_preserved=$oldPreserved
    old_files=$oldAfter.Count;concurrent_design_directory=$ConcurrentDesignDirectory;concurrent_design_files=$paths
    previous_locomotor_validation=$previous.validation
    native_layers=$(if (-not $problem) { ReadJson 'native-layers.json' });native_layers_asan=$(if ($AddressSanitizer -and -not $problem) { ReadJson 'native-layers-asan.json' })
    cmake=$(if (-not $problem) { ReadJson 'cmake.json' });corpus=$(if (-not $problem) { $c=ReadJson 'map-corpus.json'; [ordered]@{maps=$c.maps;cells=$c.cells;missing=$c.missing;deck_cells=($c.navigation | Measure-Object decks -Sum).Sum;low_bridge_cells=($c.navigation | Measure-Object low_bridges -Sum).Sum;pending_bridge_cells=($c.navigation | Measure-Object pending_bridges -Sum).Sum} })
    native_locomotor=$(if (-not $problem) { ReadJson 'native-locomotor.json' });native_locomotor_asan=$(if ($AddressSanitizer -and -not $problem) { ReadJson 'native-locomotor-asan.json' })
    simulation_version=6;native_physics=$(if (-not $problem) { ReadJson 'physics-comparison.json' });numbers=$(if (-not $problem) { ReadJson 'numbers-comparison.json' })
    executable_sha256=(Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $root 'build\ra2battle.exe')).Hash.ToLowerInvariant()
}
$receipt | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath (Join-Path $ReportDirectory 'validation.json') -Encoding utf8
if ($problem) { throw $problem }
foreach ($name in @('latest-layers.json','latest-battle.json')) {
    [ordered]@{validation=(Join-Path $ReportDirectory 'validation.json');directory=$ReportDirectory} | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $root ('reports\' + $name)) -Encoding utf8
}
$receipt | ConvertTo-Json -Depth 12
