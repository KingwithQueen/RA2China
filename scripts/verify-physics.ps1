param(
    [string]$Baseline = 'H:\开发\运行版本\原版1.006',
    [string]$OldProject = 'H:\开发',
    [string]$ReportDirectory,
    [string]$ConcurrentDesignDirectory,
    [switch]$SkipBuild,
    [switch]$AddressSanitizer
)
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot
if (-not $ReportDirectory) { $ReportDirectory = Join-Path $root ('reports\physics-' + [DateTime]::UtcNow.ToString('yyyyMMdd-HHmmss')) }
New-Item -ItemType Directory -Force -Path $ReportDirectory | Out-Null
$previous = Get-Content -Raw -LiteralPath (Join-Path $root 'reports\latest-missions.json') | ConvertFrom-Json
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
$beforeFile = Join-Path $ReportDirectory 'inputs-before.json'
$oldFile = Join-Path $ReportDirectory 'old-before.tsv'
if (-not (Test-Path -LiteralPath $beforeFile)) { Fingerprints | ConvertTo-Json | Set-Content -LiteralPath $beforeFile -Encoding utf8 }
if (-not (Test-Path -LiteralPath $oldFile)) { Inventory | Set-Content -LiteralPath $oldFile -Encoding utf8 }
$problem = $null
$samples = @()
$checks = 0
try {
    if (-not $SkipBuild) { & (Join-Path $root 'build.ps1') > (Join-Path $ReportDirectory 'build.log') }
    foreach ($name in @('ra2tests','ra2rulestests','ra2assettests','ra2voxeltests','ra2maptests','ra2battletests','ra2combattests','ra2missiontests','ra2physicstests')) {
        Run (Join-Path $root ('build\' + $name + '.exe')) @() (Join-Path $ReportDirectory ($name + '.json'))
        $checks += (ReadJson ($name + '.json')).checks
    }
    Run 'E:\Program Files\Python\python.exe' @('-B',(Join-Path $root 'scripts\reference-motion.py'),(Join-Path $Baseline 'game.exe'),(Join-Path $ReportDirectory 'native-motion.json'),(Join-Path $root 'build\ra2motioncheck.exe')) (Join-Path $ReportDirectory 'motion-comparison.json')
    Run 'E:\Program Files\Python\python.exe' @('-B',(Join-Path $root 'scripts\reference-numbers.py'),(Join-Path $root 'build\ra2calibrationcheck.exe'),(Join-Path $ReportDirectory 'numbers.json')) (Join-Path $ReportDirectory 'numbers-comparison.json')
    Run 'E:\Program Files\Python\python.exe' @('-B',(Join-Path $root 'scripts\reference-physics.py'),(Join-Path $root 'build\ra2calibrationcheck.exe'),(Join-Path $ReportDirectory 'native-physics.json')) (Join-Path $ReportDirectory 'physics-comparison.json')
    foreach ($map in @('MP05MW.map','MP13DU.map','MP29U2.map')) {
        $short = [IO.Path]::GetFileNameWithoutExtension($map)
        $directory = Join-Path $ReportDirectory $short
        New-Item -ItemType Directory -Force -Path $directory | Out-Null
        $arguments = @('--original',$Baseline,'--map',$map)
        Run (Join-Path $root 'build\ra2battle.exe') ($arguments + @('--self-test',$directory)) (Join-Path $directory 'native.json')
        $native = ReadJson ($short + '\native.json')
        if ($native.failures -or -not $native.missions -or $native.simulation_version -ne 4 -or $native.hotkeys_from_original -ne 89) { throw '战场任务窗口验证未通过。' }
        Run (Join-Path $root 'build\ra2battlecheck.exe') ($arguments + @('--missions','--output',(Join-Path $directory 'reference.rpl'))) (Join-Path $directory 'record.json')
        Run (Join-Path $root 'build\ra2battlecheck.exe') ($arguments + @('--trace','--replay',(Join-Path $directory 'reference.rpl'))) (Join-Path $directory 'replay.json')
        $record = ReadJson ($short + '\record.json')
        $played = ReadJson ($short + '\replay.json')
        if (-not $played.replay_verified -or $played.sha1 -cne $record.sha1 -or -not $played.trace_enabled -or $played.trace_sha1 -cne $record.trace_sha1 -or $record.commands -ne 8 -or $record.dropped_shots) { throw '新任务回放摘要不一致。' }
        $oldDirectory = Join-Path $previous.directory $short
        & (Join-Path $root 'build\ra2battlecheck.exe') @arguments --replay (Join-Path $oldDirectory 'reference.rpl') > (Join-Path $directory 'v3-rejection.json') 2> (Join-Path $directory 'v3-rejection.stderr.txt')
        if ($LASTEXITCODE -ne 1 -or -not (Select-String -LiteralPath (Join-Path $directory 'v3-rejection.stderr.txt') -SimpleMatch 'unsupported replay format or simulation version' -Quiet)) { throw '旧协议未被明确拒绝。' }
        $samples += [ordered]@{map=$map;native=$native;record=$record;replay=$played;v3_rejected=$true}

    }
    if ($AddressSanitizer) {
        & (Join-Path $root 'build.ps1') -AddressSanitizer > (Join-Path $ReportDirectory 'asan-build.log')
        foreach ($name in @('ra2tests','ra2rulestests','ra2assettests','ra2voxeltests','ra2maptests','ra2battletests','ra2combattests','ra2missiontests','ra2physicstests')) {
            Run (Join-Path $root ('build\asan\' + $name + '.exe')) @() (Join-Path $ReportDirectory ($name + '-asan.json'))
        }
        Run 'E:\Program Files\Python\python.exe' @('-B',(Join-Path $root 'scripts\reference-numbers.py'),(Join-Path $root 'build\asan\ra2calibrationcheck.exe'),(Join-Path $ReportDirectory 'numbers-asan.json')) (Join-Path $ReportDirectory 'numbers-asan-comparison.json')
        Run 'E:\Program Files\Python\python.exe' @('-B',(Join-Path $root 'scripts\reference-physics.py'),(Join-Path $root 'build\asan\ra2calibrationcheck.exe'),(Join-Path $ReportDirectory 'native-physics-asan.json')) (Join-Path $ReportDirectory 'physics-asan-comparison.json')
        $directory = Join-Path $ReportDirectory 'asan-native'
        New-Item -ItemType Directory -Force -Path $directory | Out-Null
        Run (Join-Path $root 'build\asan\ra2battle.exe') @('--original',$Baseline,'--self-test',$directory) (Join-Path $directory 'native.json')
        if ((ReadJson 'asan-native\native.json').failures) { throw '操作窗口内存检查未通过。' }
    }
} catch { $problem = $_.Exception.Message }
finally {
    $after = Fingerprints
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
$receipt = [ordered]@{
    passed=($null -eq $problem);error=$problem;scope='连续停靠与加减速、重复改向、20种坡面、无制导炮弹初始化与离散推进、索敌范围；原版完整曲线运动与威胁排序未完成'
    unit_checks=$checks;samples=$samples;asan_requested=[bool]$AddressSanitizer
    asan=$(if ($AddressSanitizer -and -not $problem) { ReadJson 'asan-native\native.json' })
    inputs_unchanged=$inputsUnchanged;input_count=$after.Count;old_project_unchanged=($differences.Count -eq 0);old_project_preserved=$oldPreserved
    old_files=$oldAfter.Count;concurrent_design_directory=$ConcurrentDesignDirectory;concurrent_design_files=$paths
    previous_missions_validation=$previous.validation
    simulation_version=4;native_physics=$(if (-not $problem) { ReadJson 'physics-comparison.json' });numbers=$(if (-not $problem) { ReadJson 'numbers-comparison.json' })
    executable_sha256=(Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $root 'build\ra2battle.exe')).Hash.ToLowerInvariant()
}
$receipt | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath (Join-Path $ReportDirectory 'validation.json') -Encoding utf8
if ($problem) { throw $problem }
foreach ($name in @('latest-physics.json','latest-battle.json')) {
    [ordered]@{validation=(Join-Path $ReportDirectory 'validation.json');directory=$ReportDirectory} | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $root ('reports\' + $name)) -Encoding utf8
}
$receipt | ConvertTo-Json -Depth 12
