param([switch]$AddressSanitizer, [switch]$SkipBuild, [string]$ReportDirectory = 'D:\Program\红色警戒2\reports\campaign-20261020')
$ErrorActionPreference = 'Stop'
$root = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$original = 'H:\开发\运行版本\原版1.006'
New-Item -ItemType Directory -Path $ReportDirectory -Force | Out-Null
$names = @('ra2tests','ra2rulestests','ra2assettests','ra2voxeltests','ra2maptests','ra2battletests','ra2combattests','ra2missiontests','ra2physicstests','ra2locomotortests','ra2layerstests','ra2bridgetests','ra2rendertests','ra2structuretests','ra2economytests','ra2campaigntests')
function Invoke-Checked([string]$Exe, [string[]]$Arguments, [string]$Log) {
    & $Exe @Arguments *> $Log
    if ($LASTEXITCODE) { throw ('验证未通过：' + $Exe + '，日志：' + $Log) }
}
if (-not $SkipBuild) {
    & (Join-Path $root 'build.ps1') *> (Join-Path $ReportDirectory 'build.log')
    if ($LASTEXITCODE) { throw '普通构建失败' }
    if ($AddressSanitizer) {
        & (Join-Path $root 'build.ps1') -AddressSanitizer *> (Join-Path $ReportDirectory 'build-asan.log')
        if ($LASTEXITCODE) { throw '内存检查构建失败' }
    }
}
$sourceHashes = Get-ChildItem -LiteralPath (Join-Path $root 'src'),(Join-Path $root 'include'),(Join-Path $root 'tests') -File -Recurse | Get-FileHash -Algorithm SHA256 | Select-Object Path,Hash
$sourceHashes | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $ReportDirectory 'sources-before.json') -Encoding utf8
$normal = Join-Path $root 'build'
$variants = @($normal)
if ($AddressSanitizer) { $variants += (Join-Path $root 'build\asan') }
$testRecords = @()
foreach ($variant in $variants) {
    $label = if ($variant -eq $normal) { 'normal' } else { 'asan' }
    $out = Join-Path $ReportDirectory $label
    New-Item -ItemType Directory -Path $out -Force | Out-Null
    foreach ($name in $names) {
        $log = Join-Path $out ($name + '.log')
        Invoke-Checked (Join-Path $variant ($name + '.exe')) @() $log
        $text = Get-Content -LiteralPath $log -Raw
        $testRecords += [ordered]@{variant=$label;name=$name;passed=$true;result=$text.Trim()}
    }
    foreach ($kind in @('campaign','mcv')) {
        $dir = Join-Path $out ('native-' + $kind)
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        $arguments = @(('--self-test-' + $kind),$dir)
        if ($label -eq 'asan' -and $kind -eq 'campaign') { $arguments += '--probe' }
        Invoke-Checked (Join-Path $variant 'ra2battle.exe') $arguments (Join-Path $out ($kind + '.log'))
    }
    Write-Output ($label + ' C 测试和原生窗口检查通过')
}
Invoke-Checked (Join-Path $normal 'ra2infantrycheck.exe') @($original,$ReportDirectory) (Join-Path $ReportDirectory 'infantry-assets.log')
Invoke-Checked (Join-Path $normal 'ra2campaigncheck.exe') @($original,'sov01t.map',(Join-Path $ReportDirectory 'soviet.json'),'180') (Join-Path $ReportDirectory 'soviet.log')
$normalWindow = (Get-Content (Join-Path $ReportDirectory 'normal/campaign.log') | Select-Object -Last 1) | ConvertFrom-Json
if ($normalWindow.paired_steps -ne 960 -or $normalWindow.failures) { throw '盟军首关逐步回放未通过' }
if ($AddressSanitizer) {
    $asanWindow = (Get-Content (Join-Path $ReportDirectory 'asan/campaign.log') | Select-Object -Last 1) | ConvertFrom-Json
    if ($asanWindow.paired_steps -ne 0 -or $asanWindow.state_sha1 -ne $normalWindow.state_sha1) { throw '普通与内存检查构建的首关最终状态不一致' }
}
$renderOut = Join-Path $ReportDirectory 'render'
New-Item -ItemType Directory -Path $renderOut -Force | Out-Null
Invoke-Checked (Join-Path $normal 'ra2rendertests.exe') @($original,$renderOut) (Join-Path $ReportDirectory 'render.log')
if ($AddressSanitizer) {
    $renderAsan = Join-Path $ReportDirectory 'render-asan'
    New-Item -ItemType Directory -Path $renderAsan -Force | Out-Null
    Invoke-Checked (Join-Path $root 'build/asan/ra2rendertests.exe') @($original,$renderAsan) (Join-Path $ReportDirectory 'render-asan.log')
}
$afterHashes = Get-ChildItem -LiteralPath (Join-Path $root 'src'),(Join-Path $root 'include'),(Join-Path $root 'tests') -File -Recurse | Get-FileHash -Algorithm SHA256 | Select-Object Path,Hash
if (Compare-Object ($sourceHashes | ConvertTo-Json -Compress) ($afterHashes | ConvertTo-Json -Compress)) { throw '验证期间源代码发生变化' }
[ordered]@{passed=$true;simulation=10;replay='RA2RPL12';unit_suites=16;address_sanitizer=[bool]$AddressSanitizer;allied_paired_steps=960;soviet_paired_steps=180;asan_native_campaign_mode='final_state_only';complete_original_mission=$false;original_runtime_calibration=$false;tests=$testRecords} | ConvertTo-Json -Depth 6 | Set-Content (Join-Path $ReportDirectory 'validation.json') -Encoding utf8
