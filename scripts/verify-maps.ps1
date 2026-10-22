param(
    [string]$Baseline = 'H:\开发\运行版本\原版1.006',
    [string]$Mod = 'H:\开发\运行版本\中国开局验证',
    [string]$OldProject = 'H:\开发',
    [switch]$SkipBuild,
    [switch]$AddressSanitizer
)
$ErrorActionPreference = 'Stop'
$PSNativeCommandUseErrorActionPreference = $false
$root = Split-Path $PSScriptRoot
$reportDirectory = Join-Path $root ('reports\maps-' + [DateTime]::UtcNow.ToString('yyyyMMdd-HHmmss'))
New-Item -ItemType Directory -Path $reportDirectory -Force | Out-Null
$env:TEMP = Join-Path $root 'build'
$env:TMP = $env:TEMP
$env:PYTHONIOENCODING = 'utf-8'
$inputs = @(foreach ($directory in @($Baseline,$Mod)) {
    foreach ($name in @('ra2.mix','LANGUAGE.MIX','MULTI.MIX','MAPS01.MIX','MAPS02.MIX')) { Join-Path $directory $name }
})
$inputs += @('ecache91.mix','rules.ini','art.ini','ra2.csf') | ForEach-Object { Join-Path $Mod $_ }

function Fingerprints {
    @(foreach ($path in $inputs) {
        $file = Get-Item -LiteralPath $path
        [pscustomobject]@{path=$file.FullName;bytes=$file.Length;write_ticks=$file.LastWriteTimeUtc.Ticks;sha256=(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()}
    })
}
function OldInventory {
    @(Get-ChildItem -LiteralPath $OldProject -File -Recurse -Force | Sort-Object FullName |
        ForEach-Object { "{0}`t{1}`t{2}" -f $_.FullName,$_.Length,$_.LastWriteTimeUtc.Ticks })
}
function InvokeChecked([string]$Program, [string[]]$Arguments, [string]$Log, [int]$Expected = 0) {
    & $Program @Arguments > $Log 2> ($Log + '.stderr.txt')
    if ($LASTEXITCODE -ne $Expected) { throw "验证失败：$Program，退出码 $LASTEXITCODE，预期 $Expected，报告 $Log" }
}

$before = Fingerprints
$inventoryBefore = OldInventory
$before | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $reportDirectory 'inputs-before.json') -Encoding utf8
$inventoryBefore | Set-Content -LiteralPath (Join-Path $reportDirectory 'old-project-before.tsv') -Encoding utf8
$problem = $null
$asan = $null
try {
    if (-not $SkipBuild) { & (Join-Path $root 'build.ps1') > (Join-Path $reportDirectory 'build.log') }
    foreach ($test in @('ra2tests','ra2rulestests','ra2assettests','ra2voxeltests','ra2maptests')) {
        InvokeChecked (Join-Path $root ('build\' + $test + '.exe')) @() (Join-Path $reportDirectory ($test + '.json'))
    }
    $originalFile = Join-Path $reportDirectory 'original.json'
    $chinaFile = Join-Path $reportDirectory 'china.json'
    InvokeChecked (Join-Path $root 'build\ra2mapcheck.exe') @($Baseline) $originalFile
    InvokeChecked (Join-Path $root 'build\ra2mapcheck.exe') @($Baseline,$Mod) $chinaFile
    InvokeChecked 'python.exe' @((Join-Path $PSScriptRoot 'reference-maps.py'),$originalFile,$chinaFile,$Baseline,$Mod) (Join-Path $reportDirectory 'independent-reference.json')
    $original = Get-Content -LiteralPath $originalFile -Raw | ConvertFrom-Json
    $china = Get-Content -LiteralPath $chinaFile -Raw | ConvertFrom-Json
    $known = Get-Content -LiteralPath (Join-Path $root 'tests\known-map-issues.json') -Raw | ConvertFrom-Json
    foreach ($profile in @($original,$china)) {
        $actual = @($profile.maps | Where-Object missing -gt 0 | ForEach-Object { [pscustomobject]@{name=$_.name;sha1=$_.sha1;missing=$_.missing;archive=(($_.source -split '[\\/]' | Select-Object -Last 1) -split '\|')[0]} })
        if (($actual | ConvertTo-Json -Compress) -cne ($known | ConvertTo-Json -Compress)) { throw '地图引用问题与已确认的输入清单不符。' }
    }
    InvokeChecked (Join-Path $root 'build\ra2mapviewer.exe') @('--original',$Baseline,'--mod',$Mod,'--self-test',$reportDirectory) (Join-Path $reportDirectory 'viewer-tests.json')
    $issues = @('# 地图引用与兼容信息','','原始文件未修补；实际缺失格在查看器中显示为洋红色。','')
    foreach ($map in @($original.maps | Where-Object missing -gt 0)) {
        $issues += @('## ' + $map.name,'',('- 来源：`' + $map.source + '`'),('- 文件 SHA-1：`' + $map.sha1 + '`'),('- 缺失格数：' + $map.missing),'')
        foreach ($group in @($map.issues | Group-Object reason | Sort-Object Count -Descending)) { $issues += '- ' + $group.Count + ' 格：' + $group.Name }
        $issues += ''
    }
    $issues += @('## 地形 INI 中声明但无文件的条目','','不将编辑器用的空置条目全部当作地图损坏；只有实际地图引用到它们才计入缺失引用。','')
    foreach ($theater in $original.theaters) { $issues += '- 剧场 ' + $theater.id + '：' + $theater.absent + ' 个，详见 original.json 的 absent_names。' }
    $issues += @('','## 保留与兼容','','- TN01T2.map 的节外参数保存在 __RA2_Map_Preamble；诊断行号恢复为原始行号。','- 负坐标和图外路径点保留并计数。','- MP25MW.map 的 5 个未存储地形格补为零高度普通地表。','- 未建模的触发、任务脚本、地图规则和光照定义保留在地图 INI 中。')
    $issues | Set-Content -LiteralPath (Join-Path $reportDirectory '地图引用与兼容信息.md') -Encoding utf8
    if ($AddressSanitizer) {
        $asanDirectory = Join-Path $reportDirectory 'asan'
        New-Item -ItemType Directory -Path $asanDirectory -Force | Out-Null
        & (Join-Path $root 'build.ps1') -AddressSanitizer > (Join-Path $asanDirectory 'build.log')
        InvokeChecked (Join-Path $root 'build\asan\ra2maptests.exe') @() (Join-Path $asanDirectory 'unit-tests.json')
        InvokeChecked (Join-Path $root 'build\asan\ra2mapcheck.exe') @($Baseline,$Mod,'--strict') (Join-Path $asanDirectory 'china.json') 2
        InvokeChecked (Join-Path $root 'build\asan\ra2mapviewer.exe') @('--original',$Baseline,'--mod',$Mod,'--self-test',$asanDirectory) (Join-Path $asanDirectory 'viewer-tests.json')
        $asan = [ordered]@{
            unit=(Get-Content -LiteralPath (Join-Path $asanDirectory 'unit-tests.json') -Raw | ConvertFrom-Json)
            corpus=(Get-Content -LiteralPath (Join-Path $asanDirectory 'china.json') -Raw | ConvertFrom-Json).summary
            viewer=(Get-Content -LiteralPath (Join-Path $asanDirectory 'viewer-tests.json') -Raw | ConvertFrom-Json)
            strict_exit=2
        }
    }
} catch { $problem = $_.Exception.Message }
finally {
    $after = Fingerprints
    $inventoryAfter = OldInventory
    $after | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $reportDirectory 'inputs-after.json') -Encoding utf8
    $inventoryAfter | Set-Content -LiteralPath (Join-Path $reportDirectory 'old-project-after.tsv') -Encoding utf8
    $unchanged = ($before | ConvertTo-Json -Compress) -ceq ($after | ConvertTo-Json -Compress)
    $oldUnchanged = ($inventoryBefore -join "`n") -ceq ($inventoryAfter -join "`n")
}
if (-not $unchanged -or -not $oldUnchanged) { $problem = '输入指纹或旧项目清单发生变化，请检查前后记录。' }
$receipt = [ordered]@{
    passed=($null -eq $problem)
    scope='TMP、地图数据与地形预览；对象和覆盖物以位置标记显示；不代表模拟或原版逐像素重现'
    error=$problem
    original=$original.summary
    china=$china.summary
    viewer=$(if (Test-Path -LiteralPath (Join-Path $reportDirectory 'viewer-tests.json')) { Get-Content -LiteralPath (Join-Path $reportDirectory 'viewer-tests.json') -Raw | ConvertFrom-Json })
    asan=$asan
    known_reference_issues=$known
    input_unchanged=$unchanged
    old_project_unchanged=$oldUnchanged
    old_project_files=$inventoryBefore.Count
    shared_archive_hashes_equal=@(foreach ($name in @('ra2.mix','LANGUAGE.MIX','MULTI.MIX','MAPS01.MIX','MAPS02.MIX')) {
        $pair=@($before | Where-Object { (Split-Path $_.path -Leaf) -ieq $name })
        [pscustomobject]@{name=$name;equal=($pair[0].sha256 -ceq $pair[1].sha256)}
    })
    inputs_before=$before
    inputs_after=$after
    viewer_sha256=(Get-FileHash -LiteralPath (Join-Path $root 'build\ra2mapviewer.exe') -Algorithm SHA256).Hash.ToLowerInvariant()
}
$receipt | ConvertTo-Json -Depth 15 | Set-Content -LiteralPath (Join-Path $reportDirectory 'validation.json') -Encoding utf8
if ($problem) { throw "$problem 报告：$reportDirectory" }
@{directory=$reportDirectory;validation=(Join-Path $reportDirectory 'validation.json')} | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $root 'reports\latest-maps.json') -Encoding utf8
$receipt | ConvertTo-Json -Depth 6
Write-Output $reportDirectory
