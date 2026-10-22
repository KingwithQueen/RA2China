param(
    [string]$Baseline = 'H:\开发\运行版本\原版1.006',
    [string]$Mod = 'H:\开发\运行版本\中国开局验证',
    [switch]$SkipBuild
)
$ErrorActionPreference = 'Stop'
$PSNativeCommandUseErrorActionPreference = $false
$root = Split-Path $PSScriptRoot
$reportDirectory = Join-Path $root ('reports\assets-' + [DateTime]::UtcNow.ToString('yyyyMMdd-HHmmss'))
New-Item -ItemType Directory -Path $reportDirectory -Force | Out-Null
$env:TEMP = Join-Path $root 'build'
$env:TMP = $env:TEMP
$env:PYTHONIOENCODING = 'utf-8'

# 对本阶段实际读取的包、覆盖资源和目录清单保存前后指纹。
$inputs = @((Join-Path $Baseline 'ra2.mix'), (Join-Path $Baseline 'LANGUAGE.MIX'))
$inputs += @('ecache91.mix','ra2.csf','ls640cnpr.shp','ls800cnpr.shp') | ForEach-Object { Join-Path $Mod $_ }
function Fingerprints {
    @(foreach ($path in $inputs) {
        $file = Get-Item -LiteralPath $path
        [pscustomobject]@{path=$file.FullName; bytes=$file.Length; write_ticks=$file.LastWriteTimeUtc.Ticks; sha256=(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()}
    })
}
function InvokeChecked([string]$Program, [string[]]$Arguments, [string]$Log) {
    & $Program @Arguments > $Log
    if ($LASTEXITCODE) { throw "验证失败：$Program，退出码 $LASTEXITCODE，报告 $Log" }
}
$before = Fingerprints
if (-not $SkipBuild) { & (Join-Path $root 'build.ps1') }
InvokeChecked (Join-Path $root 'build\ra2tests.exe') @() (Join-Path $reportDirectory 'base-tests.log')
InvokeChecked (Join-Path $root 'build\ra2rulestests.exe') @() (Join-Path $reportDirectory 'rule-tests.log')
InvokeChecked (Join-Path $root 'build\ra2assettests.exe') @() (Join-Path $reportDirectory 'asset-tests.json')
$originalReport = Join-Path $reportDirectory 'original.json'
$chinaReport = Join-Path $reportDirectory 'china.json'
InvokeChecked (Join-Path $root 'build\ra2assetcheck.exe') @($Baseline,'--samples') $originalReport
InvokeChecked (Join-Path $root 'build\ra2assetcheck.exe') @($Baseline,$Mod,'--samples') $chinaReport
InvokeChecked 'python.exe' @((Join-Path $PSScriptRoot 'reference-assets.py'), $originalReport, $chinaReport) (Join-Path $reportDirectory 'independent-reference.json')
InvokeChecked (Join-Path $root 'build\ra2viewer.exe') @('--original',$Baseline,'--mod',$Mod,'--self-test',$reportDirectory) (Join-Path $reportDirectory 'viewer-tests.json')
$after = Fingerprints
$unchanged = ($before | ConvertTo-Json -Depth 5 -Compress) -ceq ($after | ConvertTo-Json -Depth 5 -Compress)
if (-not $unchanged) { throw '输入指纹发生变化，请检查验证报告。' }
$original = Get-Content -LiteralPath $originalReport -Raw | ConvertFrom-Json
$china = Get-Content -LiteralPath $chinaReport -Raw | ConvertFrom-Json
$viewer = Get-Content -LiteralPath (Join-Path $reportDirectory 'viewer-tests.json') -Raw | ConvertFrom-Json
$receipt = [ordered]@{
    passed = $true
    scope = 'PAL/SHP/CSF 解析、原生窗口交互与截图；不代表游戏运行验收'
    original = $original.summary
    original_csf_labels = $original.csf.labels
    china = $china.summary
    china_csf_labels = $china.csf.labels
    viewer = $viewer
    input_unchanged = $unchanged
    inputs_before = $before
    inputs_after = $after
    viewer_sha256 = (Get-FileHash -LiteralPath (Join-Path $root 'build\ra2viewer.exe') -Algorithm SHA256).Hash.ToLowerInvariant()
}
$receipt | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath (Join-Path $reportDirectory 'validation.json') -Encoding utf8
@{directory=$reportDirectory; validation=(Join-Path $reportDirectory 'validation.json')} | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $root 'reports\latest-assets.json') -Encoding utf8
[pscustomobject]$receipt | Select-Object passed,original,original_csf_labels,china,china_csf_labels,input_unchanged | ConvertTo-Json -Depth 5
Write-Output $reportDirectory
