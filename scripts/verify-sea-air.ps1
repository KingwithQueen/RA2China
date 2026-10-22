param([switch]$AddressSanitizer, [switch]$SkipBuild, [string]$ReportDirectory = 'D:\Program\红色警戒2\reports\naval-air-20261020\final')
$ErrorActionPreference = 'Stop'
$root = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$original = 'H:\开发\运行版本\原版1.006'
New-Item -ItemType Directory -Path $ReportDirectory -Force | Out-Null
function Invoke-Checked([string]$Exe, [string[]]$Arguments, [string]$Log) {
    & $Exe @Arguments *> $Log
    if ($LASTEXITCODE) { throw ('验证失败：' + $Exe + '，日志：' + $Log) }
}
function Source-Hashes {
    Get-ChildItem -LiteralPath (Join-Path $root 'src'),(Join-Path $root 'include'),(Join-Path $root 'tests') -Recurse -File |
        Get-FileHash -Algorithm SHA256 | Select-Object Path,Hash
}
if (-not $SkipBuild) {
    & (Join-Path $root 'build.ps1') *> (Join-Path $ReportDirectory 'build.log')
    if ($LASTEXITCODE) { throw '普通构建失败' }
    if ($AddressSanitizer) {
        & (Join-Path $root 'build.ps1') -AddressSanitizer *> (Join-Path $ReportDirectory 'build-asan.log')
        if ($LASTEXITCODE) { throw '内存检查构建失败' }
    }
}
$before = @(Source-Hashes)
$before | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $ReportDirectory 'sources-before.json') -Encoding utf8
$names = @('ra2tests','ra2rulestests','ra2assettests','ra2voxeltests','ra2maptests','ra2battletests','ra2combattests','ra2missiontests','ra2physicstests','ra2locomotortests','ra2layerstests','ra2bridgetests','ra2rendertests','ra2structuretests','ra2economytests','ra2campaigntests','ra2seaairtests')
$variants = @('normal')
if ($AddressSanitizer) { $variants += 'asan' }
$records = @()
foreach ($label in $variants) {
    $bin = if ($label -eq 'normal') { Join-Path $root 'build' } else { Join-Path $root 'build\asan' }
    $out = Join-Path $ReportDirectory $label
    New-Item -ItemType Directory -Path $out -Force | Out-Null
    foreach ($name in $names) {
        $log = Join-Path $out ($name + '.log')
        Invoke-Checked (Join-Path $bin ($name + '.exe')) @() $log
        $records += [ordered]@{variant=$label;name=$name;passed=$true;result=(Get-Content -LiteralPath $log -Raw).Trim()}
    }
    Write-Output ($label + '：17 组 C 测试通过')
    $mission = Join-Path $out 'first-mission'
    New-Item -ItemType Directory -Path $mission -Force | Out-Null
    $arguments = @($original,$mission)
    if ($label -eq 'asan') { $arguments += '--probe' }
    Invoke-Checked (Join-Path $bin 'ra2firstmissioncheck.exe') $arguments (Join-Path $out 'first-mission.log')
    $result = Get-Content -LiteralPath (Join-Path $mission 'first-mission.json') -Raw | ConvertFrom-Json
    if ($result.outcome -ne 1 -or $result.mismatches -ne 0 -or ($label -eq 'normal' -and $result.paired_steps -ne $result.ticks)) { throw '首关胜负或逐步回放不一致' }
    Write-Output ($label + '：原始胜利触发器成立，固定步 ' + $result.ticks)
    $native = Join-Path $out 'native-campaign'
    New-Item -ItemType Directory -Path $native -Force | Out-Null
    $arguments = @('--self-test-campaign',$native,'--original',$original)
    if ($label -eq 'asan') { $arguments += '--probe' }
    Invoke-Checked (Join-Path $bin 'ra2battle.exe') $arguments (Join-Path $out 'native-campaign.log')
    Invoke-Checked (Join-Path $bin 'ra2seaaircheck.exe') @($original,$out) (Join-Path $out 'sea-air-assets.log')
    Invoke-Checked (Join-Path $bin 'ra2rendertests.exe') @($original,$out) (Join-Path $out 'original-render.log')
}
$normal = Get-Content -LiteralPath (Join-Path $ReportDirectory 'normal\first-mission\first-mission.json') -Raw | ConvertFrom-Json
if ($AddressSanitizer) {
    $asan = Get-Content -LiteralPath (Join-Path $ReportDirectory 'asan\first-mission\first-mission.json') -Raw | ConvertFrom-Json
    if ($normal.state_sha1 -ne $asan.state_sha1 -or $normal.ticks -ne $asan.ticks) { throw '普通与内存检查首关状态不同' }
}
$after = @(Source-Hashes)
$after | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $ReportDirectory 'sources-after.json') -Encoding utf8
if (Compare-Object $before $after -Property Path,Hash) { throw '验证期间源码变化，结果不能作为交付依据' }
$validation = [ordered]@{
    passed=$true;simulation=11;replay='RA2RPL13';hz=15;suites=$records;first_mission=$normal
    asan_profile=if($AddressSanitizer){'unit paired replay; original full mission final-state comparison; native opening final-state comparison'}else{$null}
    original_runtime_calibration=$false;complete_original_campaign=$false;china_enabled=$false
    executable=(Get-FileHash -LiteralPath (Join-Path $root 'build\ra2battle.exe') -Algorithm SHA256 | Select-Object Path,Hash)
}
$validation | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath (Join-Path $ReportDirectory 'validation.json') -Encoding utf8
Write-Output ('正式验证完成：' + (Join-Path $ReportDirectory 'validation.json'))
