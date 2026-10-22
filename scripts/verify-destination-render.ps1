param(
    [string]$Baseline = 'H:\开发\运行版本\原版1.006',
    [string]$ReportDirectory,
    [switch]$SkipBuild,
    [switch]$AddressSanitizer
)
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot
if (-not $ReportDirectory) { $ReportDirectory = Join-Path $root ('reports\destination-render-' + [DateTime]::UtcNow.ToString('yyyyMMdd-HHmmss')) }
$ReportDirectory = [IO.Path]::GetFullPath($ReportDirectory)
New-Item -ItemType Directory -Path $ReportDirectory -Force | Out-Null
function Inputs {
    @(foreach ($name in @('game.exe','ra2.mix','LANGUAGE.MIX','MULTI.MIX','MAPS01.MIX','MAPS02.MIX','RA2.INI')) { Get-FileHash -LiteralPath (Join-Path $Baseline $name) -Algorithm SHA256 })
}
function Sources {
    @(Get-ChildItem -LiteralPath (Join-Path $root 'src'),(Join-Path $root 'include'),(Join-Path $root 'tests'),(Join-Path $root 'scripts') -Recurse -File | ForEach-Object { Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256 })
}
function Run([string]$Program, [string[]]$Arguments, [string]$Log) {
    & $Program @Arguments > $Log 2> ($Log + '.stderr.txt')
    if ($LASTEXITCODE) { throw "验证失败：$Program，详见 $Log" }
    $record = Get-Content -LiteralPath $Log -Raw | ConvertFrom-Json
    if (($record.PSObject.Properties.Name -contains 'failures') -and $record.failures) { throw "检查未通过：$Log" }
}
if (-not (Test-Path -LiteralPath (Join-Path $ReportDirectory 'inputs-before.json'))) { Inputs | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $ReportDirectory 'inputs-before.json') -Encoding utf8 }
$sourceBefore = Sources
$sourceBefore | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $ReportDirectory 'sources-before.json') -Encoding utf8
$unitResults = @()
$windows = @()
$problem = $null
try {
    if (-not $SkipBuild) { & (Join-Path $root 'build.ps1') > (Join-Path $ReportDirectory 'build.log') 2>&1 }
    if ($AddressSanitizer) { & (Join-Path $root 'build.ps1') -AddressSanitizer > (Join-Path $ReportDirectory 'asan-build.log') 2>&1 }
    foreach ($variant in @('normal','asan')) {
        if ($variant -eq 'asan' -and -not $AddressSanitizer) { continue }
        $directory = Join-Path $ReportDirectory $variant
        $binary = Join-Path $root $(if ($variant -eq 'normal') { 'build' } else { 'build\asan' })
        New-Item -ItemType Directory -Path $directory -Force | Out-Null
        $sum = 0
        $tests = @('ra2tests','ra2rulestests','ra2assettests','ra2voxeltests','ra2maptests','ra2battletests','ra2combattests','ra2missiontests','ra2physicstests','ra2locomotortests','ra2layerstests','ra2bridgetests','ra2rendertests')
        foreach ($name in $tests) {
            $log = Join-Path $directory ($name + '.json')
            Run (Join-Path $binary ($name + '.exe')) @() $log
            $sum += (Get-Content -LiteralPath $log -Raw | ConvertFrom-Json).checks
        }
        $unitResults += [ordered]@{variant=$variant;suites=$tests.Count;checks=$sum}
        $maps = if ($variant -eq 'normal') { @('MP06T2','MP23MW') } else { @('MP23MW') }
        foreach ($map in $maps) {
            $window = Join-Path $directory ('layers-'+$map)
            New-Item -ItemType Directory -Path $window -Force | Out-Null
            $log = Join-Path $window 'window.json'
            Run (Join-Path $binary 'ra2battle.exe') @('--original',$Baseline,'--map',($map+'.map'),'--self-test-layers',$window) $log
            $pixels = Get-Content -LiteralPath (Join-Path $window 'pixel-visibility.json') -Raw | ConvertFrom-Json
            if ($pixels.after.visible -ne $pixels.after.expected -or $pixels.returned.visible -ne $pixels.returned.expected -or $pixels.shore_poses -ne 96 -or -not $pixels.simulation_unchanged) { throw '桥口完整模型检查未通过。' }
            $windows += [ordered]@{variant=$variant;map=$map;mode='layers';result=(Get-Content -LiteralPath $log -Raw | ConvertFrom-Json);pixels=$pixels}
        }
        if ($variant -eq 'normal') {
            $window = Join-Path $directory 'bridge-MP06T2'
            New-Item -ItemType Directory -Path $window -Force | Out-Null
            $log = Join-Path $window 'window.json'
            Run (Join-Path $binary 'ra2battle.exe') @('--original',$Baseline,'--map','MP06T2.map','--self-test-bridges',$window) $log
            $windows += [ordered]@{variant=$variant;map='MP06T2';mode='bridge_lifecycle';result=(Get-Content -LiteralPath $log -Raw | ConvertFrom-Json)}
            Run (Join-Path $binary 'ra2rendertests.exe') @($Baseline,$directory) (Join-Path $directory 'original-render.json')
        }
    }
    # 旧回放的终态和逐步摘要链同时核对，显示修改不得改变固定步模拟。
    $previous = Get-Content -LiteralPath (Join-Path $root 'reports\rendering-20261019\validation.json') -Raw | ConvertFrom-Json
    $old = Get-Content -LiteralPath (Join-Path $root 'reports\latest-bridges.json') -Raw | ConvertFrom-Json
    $replay = Join-Path $old.directory 'normal\MP06T2\lifecycle.rpl'
    $log = Join-Path $ReportDirectory 'old-replay.json'
    Run (Join-Path $root 'build\ra2battlecheck.exe') @('--original',$Baseline,'--map','MP06T2.map','--trace','--bridge-life','--replay',$replay) $log
    $actual = Get-Content -LiteralPath $log -Raw | ConvertFrom-Json
    $expected = @($previous.replays | Where-Object { $_.variant -eq 'normal' -and $_.map -eq 'MP06T2' -and $_.mode -eq 'old_bridge' })[0]
    if (-not $actual.replay_verified -or $actual.sha1 -cne $expected.sha1 -or $actual.trace_sha1 -cne $expected.trace_sha1) { throw '旧回放或逐步摘要链发生变化。' }
    & (Join-Path $PSScriptRoot 'verify-cmake.ps1') -ReportDirectory (Join-Path $ReportDirectory 'cmake') > (Join-Path $ReportDirectory 'cmake.log') 2>&1
    $audit = @(foreach ($name in @('battle','battle_layers','battle_bridges','battle_matrix','battle_motion','battle_tracks','battle_target','battle_number','battle_ballistics','battle_rules','battle_missions','battle_combat','battle_replay')) {
        $current = Get-FileHash -LiteralPath (Join-Path $root ('src\'+$name+'.c')) -Algorithm SHA256
        $saved = Get-FileHash -LiteralPath (Join-Path $root ('build\destination-render-preserved\src\'+$name+'.c')) -Algorithm SHA256
        if ($current.Hash -ne $saved.Hash) { throw "模拟核心发生变化：$name" }
        [ordered]@{file=$name+'.c';unchanged=$true;sha256=$current.Hash}
    })
    $audit | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $ReportDirectory 'simulation-source-audit.json') -Encoding utf8
    $sourceAfter = Sources
    if (@(Compare-Object $sourceBefore $sourceAfter -Property Path,Hash).Count) { throw '验证期间源码发生变化。' }
    $inputsAfter = Inputs
    $inputsAfter | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $ReportDirectory 'inputs-after.json') -Encoding utf8
    $inputsBefore = Get-Content -LiteralPath (Join-Path $ReportDirectory 'inputs-before.json') -Raw | ConvertFrom-Json
    if (@(Compare-Object $inputsBefore $inputsAfter -Property Path,Hash).Count) { throw '原始游戏输入指纹发生变化。' }
    if ($AddressSanitizer) {
        $normal = Get-Content -LiteralPath (Join-Path $ReportDirectory 'normal\layers-MP23MW\pixel-visibility.json') -Raw
        $asan = Get-Content -LiteralPath (Join-Path $ReportDirectory 'asan\layers-MP23MW\pixel-visibility.json') -Raw
        if ($normal -cne $asan) { throw '正常版与 ASAN 的显示像素统计不同。' }
    }
} catch { $problem = $_.Exception.Message }
$binaryHash = Get-FileHash -LiteralPath (Join-Path $root 'build\ra2battle.exe') -Algorithm SHA256
$record = [ordered]@{passed=($null -eq $problem);error=$problem;unit_results=$unitResults;windows=$windows;binary=$binaryHash;simulation_version=7;replay_format='RA2RPL9';old_replay=$actual}
$record | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath (Join-Path $ReportDirectory 'validation.json') -Encoding utf8
if ($problem) { throw $problem }
Write-Output '终点模型、双向桥口、桥下遮挡、回放和内存检查已通过。'
