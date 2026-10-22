param(
    [string]$Baseline = 'H:\开发\运行版本\原版1.006',
    [string]$Mod = 'H:\开发\运行版本\中国开局验证',
    [switch]$SkipBuild,
    [switch]$AddressSanitizer
)
$ErrorActionPreference = 'Stop'
$PSNativeCommandUseErrorActionPreference = $false
$root = Split-Path $PSScriptRoot
$reportDirectory = Join-Path $root ('reports\voxels-' + [DateTime]::UtcNow.ToString('yyyyMMdd-HHmmss'))
New-Item -ItemType Directory -Path $reportDirectory -Force | Out-Null
$env:TEMP = Join-Path $root 'build'
$env:TMP = $env:TEMP
$env:PYTHONIOENCODING = 'utf-8'
$inputs = @((Join-Path $Baseline 'ra2.mix'), (Join-Path $Baseline 'LANGUAGE.MIX'))
$inputs += @('ecache91.mix','rules.ini','art.ini','ra2.csf') | ForEach-Object { Join-Path $Mod $_ }

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
if (-not $SkipBuild) { & (Join-Path $root 'build.ps1') > (Join-Path $reportDirectory 'build.log') }
foreach ($test in @('ra2tests','ra2rulestests','ra2assettests','ra2voxeltests')) {
    InvokeChecked (Join-Path $root ('build\' + $test + '.exe')) @() (Join-Path $reportDirectory ($test + '.json'))
}
$originalFile = Join-Path $reportDirectory 'original.json'
$chinaFile = Join-Path $reportDirectory 'china.json'
InvokeChecked (Join-Path $root 'build\ra2voxelcheck.exe') @($Baseline,'--samples') $originalFile
InvokeChecked (Join-Path $root 'build\ra2voxelcheck.exe') @($Baseline,$Mod,'--samples') $chinaFile
InvokeChecked 'python.exe' @((Join-Path $PSScriptRoot 'reference-voxels.py'),$originalFile,$chinaFile) (Join-Path $reportDirectory 'independent-reference.json')
InvokeChecked (Join-Path $root 'build\ra2voxelviewer.exe') @('--original',$Baseline,'--mod',$Mod,'--self-test',$reportDirectory) (Join-Path $reportDirectory 'viewer-tests.json')
$original = Get-Content -LiteralPath $originalFile -Raw | ConvertFrom-Json
$china = Get-Content -LiteralPath $chinaFile -Raw | ConvertFrom-Json
$viewer = Get-Content -LiteralPath (Join-Path $reportDirectory 'viewer-tests.json') -Raw | ConvertFrom-Json
$originalIssues = @($original.resources | Where-Object binding_issue | Select-Object name,binding_issue)
$chinaIssues = @($china.resources | Where-Object binding_issue | Select-Object name,binding_issue)
if (($originalIssues | ConvertTo-Json -Compress) -cne ($chinaIssues | ConvertTo-Json -Compress)) { throw '中国预设出现不同的体素配对问题，请检查报告。' }
$compatibility = @('# 体素资源配对与兼容信息','','以下信息来自本次实际输入，原始文件未修补。','','## 无法连接的 VXL/HVA','')
foreach ($entry in $originalIssues) { $compatibility += '- `' + $entry.name + '`：' + $entry.binding_issue }
$compatibility += @('','## 单节名称差异','','仅在 VXL 与 HVA 都只有一节时，预览按顺序连接，并在窗口标注。多节名称仍按名称映射，不猜测缺失关系。','')
foreach ($entry in @($original.resources | Where-Object binding_by_index)) { $compatibility += '- `' + $entry.name + '`' }
$unmapped = @($original.resources | ForEach-Object { $_.limbs } | Measure-Object -Property unmapped_normals -Sum)[0].Sum
$compatibility += @('','## 未定义法线编号','',('原版共 {0} 个体素的法线编号不在方向表内；解析保留编号，预览使用统一向上方向，不越界访问方向表。' -f $unmapped))
$compatibility | Set-Content -LiteralPath (Join-Path $reportDirectory '资源配对与兼容信息.md') -Encoding utf8
$asan = $null
if ($AddressSanitizer) {
    $asanDirectory = Join-Path $reportDirectory 'asan'
    New-Item -ItemType Directory -Path $asanDirectory -Force | Out-Null
    & (Join-Path $root 'build.ps1') -AddressSanitizer > (Join-Path $asanDirectory 'build.log')
    InvokeChecked (Join-Path $root 'build\asan\ra2voxeltests.exe') @() (Join-Path $asanDirectory 'unit-tests.json')
    InvokeChecked (Join-Path $root 'build\asan\ra2voxelcheck.exe') @($Baseline,$Mod) (Join-Path $asanDirectory 'china.json')
    InvokeChecked (Join-Path $root 'build\asan\ra2voxelviewer.exe') @('--original',$Baseline,'--mod',$Mod,'--self-test',$asanDirectory) (Join-Path $asanDirectory 'viewer-tests.json')
    $asan = [ordered]@{
        unit = (Get-Content -LiteralPath (Join-Path $asanDirectory 'unit-tests.json') -Raw | ConvertFrom-Json)
        corpus = (Get-Content -LiteralPath (Join-Path $asanDirectory 'china.json') -Raw | ConvertFrom-Json).summary
        viewer = (Get-Content -LiteralPath (Join-Path $asanDirectory 'viewer-tests.json') -Raw | ConvertFrom-Json)
    }
}
$after = Fingerprints
$unchanged = ($before | ConvertTo-Json -Depth 5 -Compress) -ceq ($after | ConvertTo-Json -Depth 5 -Compress)
if (-not $unchanged) { throw '输入指纹发生变化，请检查报告。' }
$receipt = [ordered]@{
    passed = $true
    scope = 'VXL/HVA/VPL 解析、软件体素预览与真实 HVA 帧；不代表游戏运行或多核性能验收'
    original = $original.summary
    china = $china.summary
    original_scenes = $original.scenes
    china_scenes = $china.scenes
    viewer = $viewer
    asan = $asan
    binding_issues = $originalIssues
    unmapped_normals = $unmapped
    input_unchanged = $unchanged
    inputs_before = $before
    inputs_after = $after
    viewer_sha256 = (Get-FileHash -LiteralPath (Join-Path $root 'build\ra2voxelviewer.exe') -Algorithm SHA256).Hash.ToLowerInvariant()
}
$receipt | ConvertTo-Json -Depth 15 | Set-Content -LiteralPath (Join-Path $reportDirectory 'validation.json') -Encoding utf8
@{directory=$reportDirectory;validation=(Join-Path $reportDirectory 'validation.json')} | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $root 'reports\latest-voxels.json') -Encoding utf8
[pscustomobject]$receipt | Select-Object passed,original,china,viewer,input_unchanged | ConvertTo-Json -Depth 6
Write-Output $reportDirectory
