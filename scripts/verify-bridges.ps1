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
if (-not $ReportDirectory) { $ReportDirectory = Join-Path $root ('reports\bridges-' + [DateTime]::UtcNow.ToString('yyyyMMdd-HHmmss')) }
New-Item -ItemType Directory -Force -Path $ReportDirectory | Out-Null
$previous = Get-Content -Raw -LiteralPath (Join-Path $root 'reports\latest-layers.json') | ConvertFrom-Json
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
$checks = 0
$samples = @()
$native = @()
$tests = @('ra2tests','ra2rulestests','ra2assettests','ra2voxeltests','ra2maptests','ra2battletests','ra2combattests','ra2missiontests','ra2physicstests','ra2locomotortests','ra2layerstests','ra2bridgetests')
try {
    if (-not $SkipBuild) { & (Join-Path $root 'build.ps1') > (Join-Path $ReportDirectory 'build.log') 2>&1 }
    if ($AddressSanitizer -and -not $SkipBuild) { & (Join-Path $root 'build.ps1') -AddressSanitizer > (Join-Path $ReportDirectory 'asan-build.log') 2>&1 }
    foreach ($variant in @('normal','asan')) {
        if ($variant -eq 'asan' -and -not $AddressSanitizer) { continue }
        $binary = Join-Path $root $(if ($variant -eq 'asan') { 'build\asan' } else { 'build' })
        $directory = Join-Path $ReportDirectory $variant
        New-Item -ItemType Directory -Force -Path $directory | Out-Null
        $sum = 0
        foreach ($name in $tests) {
            Run (Join-Path $binary ($name+'.exe')) @() (Join-Path $directory ($name+'.json'))
            $sum += (ReadJson ($variant+'\'+$name+'.json')).checks
        }
        if ($variant -eq 'normal') { $checks = $sum }
        elseif ($sum -ne $checks) { throw 'ASAN 检查数不一致。' }
        foreach ($reference in @('numbers','physics','locomotor','layers','bridges')) {
            Run 'E:\Program Files\Python\python.exe' @('-B',(Join-Path $PSScriptRoot ('reference-'+$reference+'.py')),(Join-Path $binary 'ra2calibrationcheck.exe'),(Join-Path $directory ('native-'+$reference+'.json'))) (Join-Path $directory ($reference+'-comparison.json'))
        }
        foreach ($map in @('MP06T2.map','MP18S3.map','MP33U4.map')) {
            $short = [IO.Path]::GetFileNameWithoutExtension($map)
            $sampleDirectory = Join-Path $directory $short
            New-Item -ItemType Directory -Force -Path $sampleDirectory | Out-Null
            $arguments = @('--original',$Baseline,'--map',$map,'--bridge-life')
            if ($variant -eq 'asan') { $arguments += @('--steps','600') }
            Run (Join-Path $binary 'ra2battlecheck.exe') ($arguments + @('--output',(Join-Path $sampleDirectory 'lifecycle.rpl'))) (Join-Path $sampleDirectory 'record.json')
            Run (Join-Path $binary 'ra2battlecheck.exe') ($arguments + @('--replay',(Join-Path $sampleDirectory 'lifecycle.rpl'))) (Join-Path $sampleDirectory 'replay.json')
            $record = Get-Content -Raw -LiteralPath (Join-Path $sampleDirectory 'record.json') | ConvertFrom-Json
            $played = Get-Content -Raw -LiteralPath (Join-Path $sampleDirectory 'replay.json') | ConvertFrom-Json
            if (-not $played.replay_verified -or $record.sha1 -cne $played.sha1 -or $record.trace_sha1 -cne $played.trace_sha1 -or $record.bridge_falls -ne 1 -or $record.units[0].cell -ne $record.units[0].goal -or -not $record.units[0].health -or $record.units[1].health -or -not $record.repaired_segments) { throw ('桥梁生命周期回放失败：'+$variant+' '+$map) }
            if ($variant -eq 'normal') {
                Run (Join-Path $binary 'ra2battlecheck.exe') ($arguments+@('--steps','600')) (Join-Path $sampleDirectory 'short-normal.json')
            } else {
                $short=ReadJson ('normal\'+$short+'\short-normal.json')
                if ($short.sha1 -cne $record.sha1 -or $short.trace_sha1 -cne $record.trace_sha1) { throw '正常版与 ASAN 的前 600 步状态链不一致。' }
            }
            $samples += [ordered]@{variant=$variant;map=$map;mode='bridge_life';record=$record;replay=$played}
        }
        $arguments = @('--original',$Baseline,'--map','MP09DU.map','--bridge-repair')
        Run (Join-Path $binary 'ra2battlecheck.exe') ($arguments+@('--output',(Join-Path $directory 'broken.rpl'))) (Join-Path $directory 'broken-record.json')
        Run (Join-Path $binary 'ra2battlecheck.exe') ($arguments+@('--replay',(Join-Path $directory 'broken.rpl'))) (Join-Path $directory 'broken-replay.json')
        $record = ReadJson ($variant+'\broken-record.json')
        $played = ReadJson ($variant+'\broken-replay.json')
        if (-not $played.replay_verified -or $record.sha1 -cne $played.sha1 -or $record.trace_sha1 -cne $played.trace_sha1 -or $record.repaired_segments -lt 3) { throw '原始断桥修复回放失败。' }
        $samples += [ordered]@{variant=$variant;map='MP09DU.map';mode='original_broken_bridge';record=$record;replay=$played}
        Run (Join-Path $binary 'ra2bridgemapcheck.exe') @((Join-Path $directory 'broken-crossing.rpl')) (Join-Path $directory 'broken-crossing.json')
        $crossing = ReadJson ($variant+'\broken-crossing.json')
        if ($crossing.failures -or -not $crossing.crossed_original_gap -or $crossing.missing_segments -ne 7 -or $crossing.repaired_segments -ne 9) { throw '原始断桥修复后穿越检查失败。' }
        foreach ($mode in @('standard','bridge')) {
            $windowDirectory = Join-Path $directory ('window-'+$mode)
            New-Item -ItemType Directory -Force -Path $windowDirectory | Out-Null
            $arguments = @('--original',$Baseline)
            if ($mode -eq 'bridge') { $arguments += @('--map','MP06T2.map','--self-test-bridges',$windowDirectory) }
            else { $arguments += @('--self-test',$windowDirectory) }
            Run (Join-Path $binary 'ra2battle.exe') $arguments (Join-Path $windowDirectory 'native.json')
            $result = Get-Content -Raw -LiteralPath (Join-Path $windowDirectory 'native.json') | ConvertFrom-Json
            if ($result.failures -or $result.simulation_version -ne 7) { throw '战场窗口验证失败。' }
            $native += [ordered]@{variant=$variant;mode=$mode;result=$result}
        }
    }
    foreach ($map in @('MP05MW.map','MP13DU.map','MP29U2.map')) {
        $short=[IO.Path]::GetFileNameWithoutExtension($map)
        $directory=Join-Path $ReportDirectory $short
        New-Item -ItemType Directory -Force -Path $directory | Out-Null
        $arguments=@('--original',$Baseline,'--map',$map)
        Run (Join-Path $root 'build\ra2battlecheck.exe') ($arguments+@('--missions','--output',(Join-Path $directory 'missions.rpl'))) (Join-Path $directory 'record.json')
        Run (Join-Path $root 'build\ra2battlecheck.exe') ($arguments+@('--trace','--replay',(Join-Path $directory 'missions.rpl'))) (Join-Path $directory 'replay.json')
        $record=Get-Content -Raw -LiteralPath (Join-Path $directory 'record.json') | ConvertFrom-Json
        $played=Get-Content -Raw -LiteralPath (Join-Path $directory 'replay.json') | ConvertFrom-Json
        if (-not $played.replay_verified -or $record.sha1 -cne $played.sha1 -or $record.trace_sha1 -cne $played.trace_sha1) { throw '既有任务回放回归失败。' }
        $samples += [ordered]@{variant='normal';map=$map;mode='missions';record=$record;replay=$played}
    }
    Run 'E:\Program Files\Python\python.exe' @('-B',(Join-Path $PSScriptRoot 'reference-motion.py'),(Join-Path $Baseline 'game.exe'),(Join-Path $ReportDirectory 'native-motion.json'),(Join-Path $root 'build\ra2motioncheck.exe')) (Join-Path $ReportDirectory 'motion-comparison.json')
    Run (Join-Path $root 'build\ra2battlecheck.exe') @('--original',$Baseline,'--corpus') (Join-Path $ReportDirectory 'map-corpus.json')
    $corpus=ReadJson 'map-corpus.json'
    $oldCorpus=Get-Content -Raw -LiteralPath (Join-Path $previous.directory 'map-corpus.json') | ConvertFrom-Json
    if ($corpus.maps -ne $oldCorpus.maps -or $corpus.cells -ne $oldCorpus.cells -or $corpus.missing -ne $oldCorpus.missing) { throw '历史地图语料缺失情况发生变化。' }
    $oldReplay=Join-Path $previous.directory 'bridge-MP06T2\reference.rpl'
    & (Join-Path $root 'build\ra2battlecheck.exe') --original $Baseline --map MP06T2.map --layers --replay $oldReplay > (Join-Path $ReportDirectory 'v6-rejection.json') 2> (Join-Path $ReportDirectory 'v6-rejection.stderr.txt')
    if ($LASTEXITCODE -ne 1 -or -not (Select-String -LiteralPath (Join-Path $ReportDirectory 'v6-rejection.stderr.txt') -SimpleMatch 'unsupported replay format or simulation version' -Quiet)) { throw '版本 6 回放未被明确拒绝。' }
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

$receipt=[ordered]@{
    passed=($null -eq $problem);error=$problem;simulation_version=7;replay_magic='RA2RPL9';unit_checks=$checks;asan_requested=[bool]$AddressSanitizer
    samples=$samples;native_windows=$native;source_unchanged=$sourceUnchanged;inputs_unchanged=$inputsUnchanged;input_count=$after.Count
    old_project_preserved=$oldPreserved;old_project_unchanged=($differences.Count -eq 0);old_files=$oldAfter.Count;concurrent_design_files=$paths
    scope='高桥与低桥损坏、移除、修复、坦克坠桥和动态占格；场景事件与武器撞击均进入固定步。工程师/维修屋交互与原版实机校准待验。'
    original_live_scene_acceptance='pending_user_has_no_capture';v6_rejected=($null -eq $problem)
    corpus=$(if (-not $problem) { [ordered]@{maps=$corpus.maps;cells=$corpus.cells;missing=$corpus.missing;bridge_parts=($corpus.navigation | Measure-Object bridge_parts -Sum).Sum;missing_spans=($corpus.navigation | Measure-Object missing_spans -Sum).Sum;damaged_parts=($corpus.navigation | Measure-Object damaged_parts -Sum).Sum;pending_bridge_cells=($corpus.navigation | Measure-Object pending_bridges -Sum).Sum} })
    native_bridges=$(if (-not $problem) { ReadJson 'normal\native-bridges.json' });native_bridges_asan=$(if (-not $problem -and $AddressSanitizer) { ReadJson 'asan\native-bridges.json' })
    cmake=$(if (-not $problem) { ReadJson 'cmake.json' });executable_sha256=(Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $root 'build\ra2battle.exe')).Hash.ToLowerInvariant()
}
$receipt | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath (Join-Path $ReportDirectory 'validation.json') -Encoding utf8
if ($problem) { throw $problem }
foreach ($name in @('latest-bridges.json','latest-battle.json')) {
    [ordered]@{validation=(Join-Path $ReportDirectory 'validation.json');directory=$ReportDirectory} | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $root ('reports\'+$name)) -Encoding utf8
}
$receipt | ConvertTo-Json -Depth 12

