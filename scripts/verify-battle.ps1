param(
    [string]$Baseline = 'H:\开发\运行版本\原版1.006',
    [string]$OldProject = 'H:\开发',
    [string]$ReportDirectory,
    [switch]$SkipBuild,
    [switch]$AddressSanitizer
)
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot
if (-not $ReportDirectory) { $ReportDirectory = Join-Path $root ('reports\battle-' + [DateTime]::UtcNow.ToString('yyyyMMdd-HHmmss')) }
New-Item -ItemType Directory -Force -Path $ReportDirectory | Out-Null
$env:TEMP = Join-Path $root 'build'
$env:TMP = $env:TEMP
function Fingerprints {
    @(foreach ($name in @('ra2.mix','LANGUAGE.MIX','MULTI.MIX','MAPS01.MIX','MAPS02.MIX')) {
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
# 同目录续验保留最初的只读边界记录，不能在最后一次检查时覆盖初始证据。
if (-not (Test-Path -LiteralPath $beforeFile)) { Fingerprints | ConvertTo-Json | Set-Content -LiteralPath $beforeFile -Encoding utf8 }
if (-not (Test-Path -LiteralPath $oldFile)) { Inventory | Set-Content -LiteralPath $oldFile -Encoding utf8 }
$problem = $null
$samples = @()
try {
    if (-not $SkipBuild) { & (Join-Path $root 'build.ps1') > (Join-Path $ReportDirectory 'build.log') }
    foreach ($test in @('ra2tests','ra2rulestests','ra2assettests','ra2voxeltests','ra2maptests','ra2battletests')) {
        Run (Join-Path $root ('build\' + $test + '.exe')) @() (Join-Path $ReportDirectory ($test + '.json'))
    }
    Run (Join-Path $root 'build\ra2battlecheck.exe') @('--original',$Baseline,'--corpus') (Join-Path $ReportDirectory 'navigation.json')
    foreach ($map in @('MP05MW.map','MP13DU.map','MP29U2.map')) {
        $directory = Join-Path $ReportDirectory ([IO.Path]::GetFileNameWithoutExtension($map))
        New-Item -ItemType Directory -Force -Path $directory | Out-Null
        $replay = Join-Path $directory 'reference.rpl'
        $arguments = @('--original',$Baseline,'--map',$map)
        Run (Join-Path $root 'build\ra2battlecheck.exe') ($arguments + @('--output',$replay)) (Join-Path $directory 'record.json')
        Run (Join-Path $root 'build\ra2battlecheck.exe') ($arguments + @('--replay',$replay)) (Join-Path $directory 'fresh-replay.json')
        $record = Get-Content -Raw -LiteralPath (Join-Path $directory 'record.json') | ConvertFrom-Json
        $played = Get-Content -Raw -LiteralPath (Join-Path $directory 'fresh-replay.json') | ConvertFrom-Json
        if ($record.sha1 -cne $played.sha1 -or -not $played.replay_verified) { throw '独立进程回放摘要不一致。' }
        Run (Join-Path $root 'build\ra2battle.exe') ($arguments + @('--self-test',$directory)) (Join-Path $directory 'native.json')
        $native = Get-Content -Raw -LiteralPath (Join-Path $directory 'native.json') | ConvertFrom-Json
        if ($native.failures) { throw '原生窗口验证失败。' }
        $samples += [ordered]@{map=$map;record=$record;replay=$played;native=$native}
    }
    if ($AddressSanitizer) {
        & (Join-Path $root 'build.ps1') -AddressSanitizer > (Join-Path $ReportDirectory 'asan-build.log')
        Run (Join-Path $root 'build\asan\ra2battletests.exe') @() (Join-Path $ReportDirectory 'asan-unit.json')
        Run (Join-Path $root 'build\asan\ra2battlecheck.exe') @('--original',$Baseline,'--corpus') (Join-Path $ReportDirectory 'asan-navigation.json')
        foreach ($sample in $samples) {
            $directory = Join-Path $ReportDirectory ([IO.Path]::GetFileNameWithoutExtension($sample.map))
            $arguments = @('--original',$Baseline,'--map',$sample.map)
            Run (Join-Path $root 'build\asan\ra2battlecheck.exe') ($arguments + @('--replay',(Join-Path $directory 'reference.rpl'))) (Join-Path $directory 'asan-replay.json')
        }
        $directory = Join-Path $ReportDirectory 'asan-native'
        New-Item -ItemType Directory -Force -Path $directory | Out-Null
        Run (Join-Path $root 'build\asan\ra2battle.exe') @('--original',$Baseline,'--self-test',$directory) (Join-Path $directory 'native.json')
    }
} catch { $problem = $_.Exception.Message }
finally {
    $after = Fingerprints
    $oldAfter = Inventory
    $after | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $ReportDirectory 'inputs-after.json') -Encoding utf8
    $oldAfter | Set-Content -LiteralPath (Join-Path $ReportDirectory 'old-after.tsv') -Encoding utf8
    $before = Get-Content -LiteralPath $beforeFile -Raw | ConvertFrom-Json
    $unchanged = ($before | ConvertTo-Json -Compress) -ceq ($after | ConvertTo-Json -Compress)
    $oldUnchanged = ((Get-Content -LiteralPath $oldFile) -join "`n") -ceq ($oldAfter -join "`n")
}
if (-not $unchanged -or -not $oldUnchanged) { $problem = '原版输入或旧项目清单发生变化。' }
$receipt = [ordered]@{
    passed=($null -eq $problem); error=$problem
    scope='原版资源最小战场、整数单线程固定步、移动与回放；尚未完成原版运动学对照或多核性能验收'
    navigation=$(if (Test-Path (Join-Path $ReportDirectory 'navigation.json')) { $j=ReadJson 'navigation.json'; [ordered]@{maps=$j.maps;cells=$j.cells;missing=$j.missing} })
    unit=$(if (Test-Path (Join-Path $ReportDirectory 'ra2battletests.json')) { ReadJson 'ra2battletests.json' })
    samples=$samples; asan_requested=[bool]$AddressSanitizer
    asan=$(if ($AddressSanitizer -and -not $problem) {
        $j=ReadJson 'asan-navigation.json'
        [ordered]@{unit=(ReadJson 'asan-unit.json');navigation=[ordered]@{maps=$j.maps;cells=$j.cells;missing=$j.missing};native=(ReadJson 'asan-native\native.json')}
    })
    inputs_unchanged=$unchanged; old_project_unchanged=$oldUnchanged; old_files=$oldAfter.Count
    executable_sha256=(Get-FileHash -LiteralPath (Join-Path $root 'build\ra2battle.exe') -Algorithm SHA256).Hash.ToLowerInvariant()
}
$receipt | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath (Join-Path $ReportDirectory 'validation.json') -Encoding utf8
if ($problem) { throw $problem }
[ordered]@{validation=(Join-Path $ReportDirectory 'validation.json');directory=$ReportDirectory} |
    ConvertTo-Json | Set-Content -LiteralPath (Join-Path $root 'reports\latest-battle.json') -Encoding utf8
$receipt | ConvertTo-Json -Depth 12
