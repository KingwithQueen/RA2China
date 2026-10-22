param(
    [string]$Baseline = 'H:\开发\运行版本\原版1.006',
    [string]$OldProject = 'H:\开发',
    [string]$ReportDirectory,
    [string]$Python = 'E:\Program Files\Python\python.exe',
    [string[]]$ConcurrentDesignFiles = @(),
    [string]$ConcurrentDesignDirectory,
    [switch]$SkipBuild,
    [switch]$AddressSanitizer
)
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot
if (-not $ReportDirectory) { $ReportDirectory = Join-Path $root ('reports\combat-' + [DateTime]::UtcNow.ToString('yyyyMMdd-HHmmss')) }
New-Item -ItemType Directory -Force -Path $ReportDirectory | Out-Null
$env:TEMP = Join-Path $root 'build'
$env:TMP = $env:TEMP
$env:PYTHONDONTWRITEBYTECODE = '1'
function Fingerprints {
    @(foreach ($name in @('game.exe','ra2.mix','LANGUAGE.MIX','MULTI.MIX','MAPS01.MIX','MAPS02.MIX')) {
        Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $Baseline $name)
    })
}
function Inventory {
    @(Get-ChildItem -LiteralPath $OldProject -File -Recurse -Force | Sort-Object FullName |
        ForEach-Object { '{0}`t{1}`t{2}' -f $_.FullName,$_.Length,$_.LastWriteTimeUtc.Ticks })
}
function Run([string]$Program, [string[]]$Arguments, [string]$Log) {
    & $Program @Arguments > $Log 2> ($Log + '.stderr.txt')
    if ($LASTEXITCODE) { throw "验证失败：$Program，退出码 $LASTEXITCODE，详见 $Log" }
}
function ReadJson([string]$Name) { Get-Content -LiteralPath (Join-Path $ReportDirectory $Name) -Raw | ConvertFrom-Json }
$beforeFile = Join-Path $ReportDirectory 'inputs-before.json'
$oldFile = Join-Path $ReportDirectory 'old-before.tsv'
# 同目录续验保留最早边界记录，重试不能覆盖初始证据。
if (-not (Test-Path -LiteralPath $beforeFile)) { Fingerprints | ConvertTo-Json | Set-Content -LiteralPath $beforeFile -Encoding utf8 }
if (-not (Test-Path -LiteralPath $oldFile)) { Inventory | Set-Content -LiteralPath $oldFile -Encoding utf8 }
$problem = $null
$functionalPassed = $false
$samples = @()
try {
    if (-not $SkipBuild) { & (Join-Path $root 'build.ps1') > (Join-Path $ReportDirectory 'build.log') }
    foreach ($test in @('ra2tests','ra2rulestests','ra2assettests','ra2voxeltests','ra2maptests','ra2battletests','ra2combattests')) {
        Run (Join-Path $root ('build\' + $test + '.exe')) @() (Join-Path $ReportDirectory ($test + '.json'))
    }
    Run $Python @('-B',(Join-Path $PSScriptRoot 'reference-motion.py'),(Join-Path $Baseline 'game.exe'),(Join-Path $ReportDirectory 'native-motion.json'),(Join-Path $root 'build\ra2motioncheck.exe')) (Join-Path $ReportDirectory 'motion-comparison.json')
    Run (Join-Path $root 'build\ra2battlecheck.exe') @('--original',$Baseline,'--corpus') (Join-Path $ReportDirectory 'navigation.json')
    foreach ($map in @('MP05MW.map','MP13DU.map','MP29U2.map')) {
        $directory = Join-Path $ReportDirectory ([IO.Path]::GetFileNameWithoutExtension($map))
        New-Item -ItemType Directory -Force -Path $directory | Out-Null
        $replay = Join-Path $directory 'reference.rpl'
        $arguments = @('--original',$Baseline,'--map',$map)
        Run (Join-Path $root 'build\ra2battlecheck.exe') ($arguments + @('--combat','--output',$replay)) (Join-Path $directory 'record.json')
        Run (Join-Path $root 'build\ra2battlecheck.exe') ($arguments + @('--replay',$replay)) (Join-Path $directory 'fresh-replay.json')
        $record = ReadJson (([IO.Path]::GetFileNameWithoutExtension($map)) + '\record.json')
        $played = ReadJson (([IO.Path]::GetFileNameWithoutExtension($map)) + '\fresh-replay.json')
        if ($record.sha1 -cne $played.sha1 -or -not $played.replay_verified -or -not $record.kills -or $record.dropped_shots) { throw '独立进程战斗回放或摧毁验证失败。' }
        Run (Join-Path $root 'build\ra2battle.exe') ($arguments + @('--self-test',$directory)) (Join-Path $directory 'native.json')
        $native = ReadJson (([IO.Path]::GetFileNameWithoutExtension($map)) + '\native.json')
        if ($native.failures -or -not $native.mouse_attack -or -not $native.combat_replay) { throw '原生战斗窗口验证失败。' }
        $samples += [ordered]@{map=$map;record=$record;replay=$played;native=$native}
    }
    if ($AddressSanitizer) {
        & (Join-Path $root 'build.ps1') -AddressSanitizer > (Join-Path $ReportDirectory 'asan-build.log')
        foreach ($test in @('ra2battletests','ra2combattests')) {
            Run (Join-Path $root ('build\asan\' + $test + '.exe')) @() (Join-Path $ReportDirectory ('asan-' + $test + '.json'))
        }
        foreach ($sample in $samples) {
            $directory = Join-Path $ReportDirectory ([IO.Path]::GetFileNameWithoutExtension($sample.map))
            Run (Join-Path $root 'build\asan\ra2battlecheck.exe') @('--original',$Baseline,'--map',$sample.map,'--replay',(Join-Path $directory 'reference.rpl')) (Join-Path $directory 'asan-replay.json')
            $played = ReadJson (([IO.Path]::GetFileNameWithoutExtension($sample.map)) + '\asan-replay.json')
            if ($played.sha1 -cne $sample.record.sha1 -or -not $played.replay_verified) { throw '内存检查构建的回放摘要不同。' }
        }
        $directory = Join-Path $ReportDirectory 'asan-native'
        New-Item -ItemType Directory -Force -Path $directory | Out-Null
        Run (Join-Path $root 'build\asan\ra2battle.exe') @('--original',$Baseline,'--self-test',$directory) (Join-Path $directory 'native.json')
        if ((ReadJson 'asan-native\native.json').failures) { throw '内存检查构建的窗口验证失败。' }
    }
    $functionalPassed = $true
} catch { $problem = $_.Exception.Message }
finally {
    $after = Fingerprints
    $oldAfter = Inventory
    $after | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $ReportDirectory 'inputs-after.json') -Encoding utf8
    $oldAfter | Set-Content -LiteralPath (Join-Path $ReportDirectory 'old-after.tsv') -Encoding utf8
    $before = Get-Content -LiteralPath $beforeFile -Raw | ConvertFrom-Json
    $unchanged = ($before | ConvertTo-Json -Compress) -ceq ($after | ConvertTo-Json -Compress)
    $oldBefore = Get-Content -LiteralPath $oldFile
    $oldUnchanged = ($oldBefore -join "`n") -ceq ($oldAfter -join "`n")
    $accepted = [Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
    foreach ($file in $ConcurrentDesignFiles) { [void]$accepted.Add([IO.Path]::GetFullPath($file)) }
    $differences = @(Compare-Object -ReferenceObject $oldBefore -DifferenceObject $oldAfter)
    $changedFiles = @($differences | ForEach-Object { ($_.InputObject -split [regex]::Escape('`t'))[0] } | Sort-Object -Unique)
    # 仅在用户明确确认并行设计时，允许指定目录中的 Markdown 文档变化；不放宽资源或代码边界。
    $designRoot = if ($ConcurrentDesignDirectory) { [IO.Path]::GetFullPath($ConcurrentDesignDirectory).TrimEnd('\') } else { $null }
    $unaccepted = @($differences | Where-Object {
        $path = ($_.InputObject -split [regex]::Escape('`t'))[0]
        -not $accepted.Contains($path) -and -not ($designRoot -and [IO.Path]::GetDirectoryName($path) -ieq $designRoot -and [IO.Path]::GetExtension($path) -ieq '.md')
    })
    $oldPreserved = $unaccepted.Count -eq 0
    $differences | Select-Object InputObject,SideIndicator | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath (Join-Path $ReportDirectory 'concurrent-design-changes.json') -Encoding utf8
}
if (-not $unchanged -or -not $oldPreserved) { $problem = '原版输入或用户确认的并行设计文档之外的旧项目文件发生变化。' }
$receipt = [ordered]@{
    passed=($null -eq $problem); error=$problem; functional_passed=$functionalPassed
    scope='原版窄指令运动学对照、最小炮战、纯 C 整数固定步与独立进程回放；不是完整原版行走/弹道或多核性能验收'
    motion=$(if (Test-Path (Join-Path $ReportDirectory 'motion-comparison.json')) { ReadJson 'motion-comparison.json' })
    navigation=$(if (Test-Path (Join-Path $ReportDirectory 'navigation.json')) { $j=ReadJson 'navigation.json'; [ordered]@{maps=$j.maps;cells=$j.cells;missing=$j.missing} })
    unit=$(if (Test-Path (Join-Path $ReportDirectory 'ra2combattests.json')) { ReadJson 'ra2combattests.json' })
    movement_unit=$(if (Test-Path (Join-Path $ReportDirectory 'ra2battletests.json')) { ReadJson 'ra2battletests.json' })
    samples=$samples; asan_requested=[bool]$AddressSanitizer
    asan=$(if ($AddressSanitizer -and $functionalPassed) { [ordered]@{combat=(ReadJson 'asan-ra2combattests.json');movement=(ReadJson 'asan-ra2battletests.json');native=(ReadJson 'asan-native\native.json');replays=3} })
    inputs_unchanged=$unchanged; input_count=$after.Count; old_project_unchanged=$oldUnchanged; old_files=$oldAfter.Count
    old_project_preserved=$oldPreserved; concurrent_design_files=$ConcurrentDesignFiles; concurrent_changed_files=$changedFiles.Count
    concurrent_design_directory=$ConcurrentDesignDirectory
    executable_sha256=(Get-FileHash -LiteralPath (Join-Path $root 'build\ra2battle.exe') -Algorithm SHA256).Hash.ToLowerInvariant()
}
$receipt | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath (Join-Path $ReportDirectory 'validation.json') -Encoding utf8
if ($problem) { throw $problem }
foreach ($name in @('latest-combat.json','latest-battle.json')) {
    [ordered]@{validation=(Join-Path $ReportDirectory 'validation.json');directory=$ReportDirectory} | ConvertTo-Json |
        Set-Content -LiteralPath (Join-Path $root ('reports\' + $name)) -Encoding utf8
}
$receipt | ConvertTo-Json -Depth 12
