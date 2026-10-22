param(
    [string]$Baseline = 'H:\开发\运行版本\原版1.006',
    [string]$OriginalExtracted = 'H:\开发\研究资料\提取\原版\ra2.mix_files\local.mix_files',
    [string]$Mod = 'H:\开发\运行版本\中国开局验证',
    [switch]$SkipBuild
)
$ErrorActionPreference = 'Stop'
$PSNativeCommandUseErrorActionPreference = $false
$root = Split-Path $PSScriptRoot
$reportDirectory = Join-Path $root ('reports\rules-' + [DateTime]::UtcNow.ToString('yyyyMMdd-HHmmss'))
New-Item -ItemType Directory -Path $reportDirectory -Force | Out-Null
$env:TEMP = Join-Path $root 'build'
$env:TMP = $env:TEMP
$tool = Join-Path $root 'build\ra2tool.exe'
$ruleTests = Join-Path $root 'build\ra2rulestests.exe'
$originalRules = Join-Path $OriginalExtracted 'rules.ini'
$originalArt = Join-Path $OriginalExtracted 'art.ini'
$chinaRules = Join-Path $Mod 'rules.ini'
$chinaArt = Join-Path $Mod 'art.ini'
$archive = Join-Path $Baseline 'ra2.mix'
$inputs = @($archive, $originalRules, $originalArt, $chinaRules, $chinaArt)

function HashFiles([string[]]$Paths) {
    @(foreach ($path in $Paths) {
        $file = Get-Item -LiteralPath $path
        [pscustomobject]@{
            path = $file.FullName
            bytes = $file.Length
            write_ticks = $file.LastWriteTimeUtc.Ticks
            sha256 = (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()
        }
    })
}

function MarkdownCell($Value) {
    ([string]$Value).Replace('|', '\|').Replace("`r", '').Replace("`n", '<br>')
}

function ReferenceKey($Reference) {
    '{0}|{1}|{2}|{3}|{4}' -f $Reference.target_domain, $Reference.section, $Reference.key, $Reference.target_id, $Reference.status
}

function WriteProfile($Profile, [string]$Label) {
    $missing = [System.Collections.Generic.List[string]]::new()
    $missing.Add('# ' + $Label + '：引用检查')
    $missing.Add('')
    $missing.Add('规则来源：`' + $Profile.rules_source + '`。')
    $missing.Add('美术来源：`' + $Profile.art_source + '`。')
    $missing.Add('')
    $missing.Add('以下是已建模字段的静态检查，不代表原版所有默认行为或真实对局结果。美术文件本身尚未检查。')
    foreach ($status in @('missing', 'declared_without_definition', 'wrong_type')) {
        $title = switch ($status) {
            'missing' { '明确缺失的目标' }
            'declared_without_definition' { '类型表声明但没有规则定义' }
            'wrong_type' { '与当前模型类型不符的目标' }
        }
        $items = @($Profile.missing_references | Where-Object status -eq $status)
        $missing.Add('')
        $missing.Add('## ' + $title + '：' + $items.Count + ' 项')
        $missing.Add('')
        if ($status -eq 'declared_without_definition') {
            $missing.Add('此类包含遗留占位类型，可能使用原版内建默认值；单独列出，不直接判为游戏故障。')
            $missing.Add('')
        }
        $missing.Add('| 节 | 字段 | 目标 | 命名空间 | 行号 |')
        $missing.Add('|---|---|---|---|---:|')
        foreach ($item in $items) {
            $missing.Add(('| {0} | {1} | {2} | {3} | {4} |' -f (MarkdownCell $item.section), (MarkdownCell $item.key), (MarkdownCell $item.target_id), $item.target_domain, $item.line))
        }
    }
    $missing.Add('')
    $missing.Add('## 标量字段取值异常：' + $Profile.invalid_fields.Count + ' 项')
    $missing.Add('')
    foreach ($item in $Profile.invalid_fields) {
        $missing.Add(('- [{0}] {1}={2}，第 {3} 行。' -f (MarkdownCell $item.section), (MarkdownCell $item.key), (MarkdownCell $item.value), $item.line))
    }
    $missing | Set-Content -LiteralPath (Join-Path $reportDirectory ($Label + '-缺失引用.md')) -Encoding utf8

    $gaps = [System.Collections.Generic.List[string]]::new()
    $gaps.Add('# ' + $Label + '：尚未实现的字段')
    $gaps.Add('')
    $gaps.Add('当前未实现任何字段对应的游戏运行逻辑。数值转换和引用检查属于数据层支持，不计为移动、战斗、生产或绘制功能已经完成。')
    $gaps.Add('类型总表和通用前置成员作为结构资料单独处理，不列为游戏运行字段。其余字段按命名空间及字段名分组，所有出现位置保存在完整 JSON 的 fields 数组。')
    $gaps.Add('')
    $gaps.Add('| 命名空间 | 字段 | 次数 | 仅原文 | 已转换标量 | 已检查引用 | 首个对象 | 行号 |')
    $gaps.Add('|---|---|---:|---:|---:|---:|---|---:|')
    foreach ($gap in ($Profile.unimplemented_fields | Sort-Object @{Expression='raw_only';Descending=$true}, domain, key)) {
        $first = $Profile.fields[$gap.first_field]
        $gaps.Add(('| {0} | {1} | {2} | {3} | {4} | {5} | {6} | {7} |' -f $gap.domain, (MarkdownCell $gap.key), $gap.occurrences, $gap.raw_only, $gap.typed, $gap.reference_checked, (MarkdownCell $first.section), $first.line))
    }
    $gaps | Set-Content -LiteralPath (Join-Path $reportDirectory ($Label + '-未实现字段.md')) -Encoding utf8
}

Write-Host '记录规则输入的只读基线……'
$before = HashFiles $inputs
$before | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath (Join-Path $reportDirectory 'inputs-before.json') -Encoding utf8
$passed = $false
$problem = $null
$profiles = @{}
$strictResults = @{}
$testResult = $null
$baseResult = $null
$newMissing = @()
$newGaps = @()
try {
    if (-not $SkipBuild) {
        & (Join-Path $root 'build.ps1') *> (Join-Path $reportDirectory 'build.log')
        if ($LASTEXITCODE) { throw 'C17 编译失败。' }
    }
    $baseLog = @(& (Join-Path $root 'build\ra2tests.exe') 2>&1)
    $baseExit = $LASTEXITCODE
    $baseLog | Set-Content -LiteralPath (Join-Path $reportDirectory 'base-tests.log') -Encoding utf8
    if ($baseExit) { throw '资源基础回归测试失败。' }
    $baseResult = $baseLog[-1] | ConvertFrom-Json
    $testLog = @(& $ruleTests $originalRules $originalArt $chinaRules $chinaArt 2>&1)
    $testExit = $LASTEXITCODE
    $testLog | Set-Content -LiteralPath (Join-Path $reportDirectory 'rules-tests.log') -Encoding utf8
    if ($testExit) { throw '规则 C 测试失败。' }
    $testResult = $testLog[-1] | ConvertFrom-Json

    $spec = $archive + '|local.mix'
    foreach ($name in @('original', 'china')) {
        $arguments = @('rules-check', '--mix', '10', $spec)
        if ($name -eq 'china') { $arguments += @('--dir', '100', $Mod) }
        $jsonPath = Join-Path $reportDirectory ($name + '.json')
        & $tool @arguments > $jsonPath 2> (Join-Path $reportDirectory ($name + '-error.log'))
        if ($LASTEXITCODE) { throw "无法生成 $name 规则报告。" }
        $profile = Get-Content -LiteralPath $jsonPath -Raw -Encoding utf8 | ConvertFrom-Json
        if ($profile.fields.Count -ne $profile.summary.fields -or $profile.references.Count -ne $profile.summary.references) { throw '报告数量不一致。' }
        if ($profile.summary.runtime_fields_implemented -ne 0) { throw '报告错误地宣称游戏字段已经运行实现。' }
        if ($profile.summary.invalid_values -ne 0) { throw '真实规则出现标量取值异常，需检查模型或源文件。' }
        $profiles[$name] = $profile
        & $tool @arguments --strict > $null 2> (Join-Path $reportDirectory ($name + '-strict-error.log'))
        $strictResults[$name] = $LASTEXITCODE
        $expectedExit = if ($profile.has_reference_or_value_errors) { 2 } else { 0 }
        if ($strictResults[$name] -ne $expectedExit) { throw '严格模式未返回预期退出码。' }
        $label = if ($name -eq 'original') { '原版1.006' } else { '中国MOD' }
        WriteProfile $profile $label
    }

    # 差异比较忽略来源路径和整体行号偏移，防止把原版遗留条目误报成中国新增问题。
    $knownMissing = [System.Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
    foreach ($reference in $profiles.original.missing_references) { $null = $knownMissing.Add((ReferenceKey $reference)) }
    $newMissing = @($profiles.china.missing_references | Where-Object { -not $knownMissing.Contains((ReferenceKey $_)) })
    $knownGaps = [System.Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
    foreach ($gap in $profiles.original.unimplemented_fields) { $null = $knownGaps.Add(($gap.domain + '|' + $gap.key)) }
    $newGaps = @($profiles.china.unimplemented_fields | Where-Object { -not $knownGaps.Contains(($_.domain + '|' + $_.key)) })
    $newMissing | ConvertTo-Json -Depth 6 -AsArray | Set-Content -LiteralPath (Join-Path $reportDirectory 'china-additional-missing.json') -Encoding utf8
    $newGaps | ConvertTo-Json -Depth 6 -AsArray | Set-Content -LiteralPath (Join-Path $reportDirectory 'china-additional-fields.json') -Encoding utf8
    $passed = $true
} catch {
    $problem = $_.Exception.Message
} finally {
    $after = HashFiles $inputs
    $after | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath (Join-Path $reportDirectory 'inputs-after.json') -Encoding utf8
    $changes = @(Compare-Object $before $after -Property path,bytes,write_ticks,sha256)
    if ($changes.Count) {
        $passed = $false
        $problem = '验证期间源规则或原始包发生变化。'
    }
    $sourcePaths = @(Get-ChildItem -LiteralPath (Join-Path $root 'src'), (Join-Path $root 'include'), (Join-Path $root 'tests') -File -Recurse |
        Where-Object Extension -in '.c','.h' | Select-Object -ExpandProperty FullName)
    $sourcePaths += @((Join-Path $root 'build.ps1'), (Join-Path $root 'CMakeLists.txt'), $PSCommandPath)
    $artifactPaths = @($tool, $ruleTests, (Join-Path $root 'build\ra2resources.lib'))
    $receipt = [ordered]@{
        created_utc = [DateTime]::UtcNow.ToString('o')
        passed = $passed
        problem = $problem
        stage = 'rule_model_and_static_references'
        base_tests = $baseResult
        rule_tests = $testResult
        original = $profiles.original.summary
        china = $profiles.china.summary
        strict_exit_codes = $strictResults
        china_additional_missing = $newMissing.Count
        china_additional_field_groups = $newGaps.Count
        preservation = @{ hashed_inputs = $inputs.Count; changes = $changes.Count; scope = '读取的 4 份 INI 与原版 ra2.mix 的大小、修改时间及 SHA-256 前后对照；所有输出位于新项目。' }
        sources = (HashFiles $sourcePaths)
        artifacts = (HashFiles $artifactPaths)
        limitations = @('仅覆盖明确建模的字段引用与标量类型，未实现游戏运行逻辑。','声明但无定义的旧条目与待检查的美术资源单独列出，不自动判定原版游戏故障。','未检查战役、地图覆盖、声音/文字标签、资源文件内容、科技树可达性或联机行为。')
    }
    $receipt | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $reportDirectory 'validation.json') -Encoding utf8
    @{ report = (Join-Path $reportDirectory 'validation.json'); passed = $passed } | ConvertTo-Json |
        Set-Content -LiteralPath (Join-Path $root 'reports\latest-rules.json') -Encoding utf8
}
Write-Host "报告目录：$reportDirectory"
if (-not $passed) { throw $problem }
Write-Host "通过：规则 $($testResult.checks) 项检查，基础回归 $($baseResult.checks) 项；源输入哈希保持一致。"
exit 0
