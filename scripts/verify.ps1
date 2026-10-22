param(
    [string]$Baseline = 'H:\开发\运行版本\原版1.006',
    [string]$Mod = 'H:\开发\运行版本\中国开局验证',
    [string]$Extracted = 'H:\开发\研究资料\提取\原版\ra2.mix_files\local.mix_files',
    [string]$OldProject = 'H:\开发',
    [string]$ToolDirectory,
    [switch]$SkipBuild,
    [string]$ReportLabel = 'release'
)
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot
if ($ReportLabel -notmatch '^[a-zA-Z0-9_-]+$') { throw 'Invalid report label.' }
$report = Join-Path $root ('reports\' + [DateTime]::UtcNow.ToString('yyyyMMdd-HHmmss') + '-' + $ReportLabel)
New-Item -ItemType Directory -Path $report -Force | Out-Null
if (-not $ToolDirectory) { $ToolDirectory = Join-Path $root 'build' }
$env:TEMP = Join-Path $root 'build'
$env:TMP = $env:TEMP
if (-not $SkipBuild) {
    & (Join-Path $root 'build.ps1') *> (Join-Path $report 'build.log')
    if ($LASTEXITCODE) { throw 'Build failed; see build.log.' }
}
$tool = Join-Path $ToolDirectory 'ra2tool.exe'
$tests = Join-Path $ToolDirectory 'ra2tests.exe'
if (-not (Test-Path -LiteralPath $tool) -or -not (Test-Path -LiteralPath $tests)) { throw 'Build tools missing.' }

function OldInventory {
    @(Get-ChildItem -LiteralPath $OldProject -File -Recurse -Force | Sort-Object FullName |
        ForEach-Object { "{0}`t{1}`t{2}" -f $_.FullName, $_.Length, $_.LastWriteTimeUtc.Ticks })
}
function FileHashes([string[]]$Paths) {
    @(foreach ($path in $Paths) {
        $file = Get-Item -LiteralPath $path
        [pscustomobject]@{ path = $file.FullName; bytes = $file.Length; sha256 = (Get-FileHash -LiteralPath $file.FullName -Algorithm SHA256).Hash.ToLowerInvariant() }
    })
}
function RunTool([string[]]$Arguments) {
    $output = & $tool @Arguments 2> (Join-Path $report 'last-tool-error.log')
    if ($LASTEXITCODE) {
        $detail = Get-Content -LiteralPath (Join-Path $report 'last-tool-error.log') -Raw
        throw "Resource tool failed ($($Arguments -join ' ')): $detail"
    }
    $output | ConvertFrom-Json
}

$archives = @(Get-ChildItem -LiteralPath $Baseline -File | Where-Object Extension -eq '.mix' | Sort-Object Name)
$nestedRoot = Split-Path $Extracted
$nested = @(Get-ChildItem -LiteralPath $nestedRoot -File -Filter '*.mix' | Sort-Object Name)
$iniFiles = @(Get-ChildItem -LiteralPath $Extracted -File -Filter '*.ini' | Sort-Object Name)
$modFiles = @(Get-ChildItem -LiteralPath $Mod -File | Where-Object { $_.Extension -in '.ini','.mix','.csf' })
$inputs = @(@($archives.FullName) + @($nested.FullName) + @($iniFiles.FullName) + @($modFiles.FullName) | Sort-Object -Unique)
Write-Host 'Recording read-only source baseline...'
$inventoryBefore = OldInventory
$inventoryBefore | Set-Content -LiteralPath (Join-Path $report 'old-project-before.tsv') -Encoding utf8
$hashBefore = FileHashes $inputs
$hashBefore | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath (Join-Path $report 'inputs-before.json') -Encoding utf8

$passed = $false
$problem = $null
$unitResult = $null
$archiveResults = @()
$expectedRejections = @()
$knownIssues = @(Get-Content -LiteralPath (Join-Path $root 'tests\known-input-issues.json') -Raw -Encoding utf8 | ConvertFrom-Json)
$indexChecks = @()
$iniResults = @()
$queries = @()
try {
    Write-Host 'Running C tests and byte-for-byte corpus comparisons...'
    $output = @(& $tests $Baseline $Mod $Extracted 2>&1)
    $exitCode = $LASTEXITCODE
    $output | Set-Content -LiteralPath (Join-Path $report 'tests.log') -Encoding utf8
    if ($exitCode) { throw "C tests failed with exit code $exitCode." }
    $unitResult = $output[-1] | ConvertFrom-Json
    if ($unitResult.failures -ne 0) { throw 'C test failures reported.' }

    Write-Host 'Verifying original and nested MIX archives...'
    foreach ($file in @($archives) + @($nested) + @($modFiles | Where-Object Extension -eq '.mix')) {
        $inputHash = ($hashBefore | Where-Object path -eq $file.FullName).sha256
        $issue = @($knownIssues | Where-Object { $_.name -ieq $file.Name -and $_.sha256 -eq $inputHash })
        if ($issue.Count) {
            $errorPath = Join-Path $report ('expected-rejection-' + $expectedRejections.Count + '.json')
            $null = & $tool mix $file.FullName 2> $errorPath
            $rejectCode = $LASTEXITCODE
            $diagnostic = Get-Content -LiteralPath $errorPath -Raw -Encoding utf8 | ConvertFrom-Json
            if ($rejectCode -ne 1 -or $diagnostic.error -ne 'format' -or $diagnostic.message -ne $issue[0].expected_error) {
                throw 'Known invalid input was not rejected with the expected integrity error.'
            }
            $expectedRejections += [pscustomobject]@{ source = $file.FullName; sha256 = $inputHash; error = $diagnostic; reason = $issue[0].reason }
            continue
        }
        $result = RunTool @('mix', $file.FullName)
        if ($result.checksum_present -and -not $result.checksum_verified) { throw 'Unverified MIX checksum.' }
        $archiveResults += $result | Select-Object source,count,flags,encrypted,checksum_present,checksum_verified,data_offset,data_size
        $reference = $null
        if ($file.DirectoryName -eq $nestedRoot) { $reference = Join-Path $nestedRoot ($file.Name.ToLowerInvariant() + '_files\index.json') }
        elseif ($file.Name -ieq 'ra2.mix') { $reference = Join-Path $nestedRoot 'index.json' }
        elseif ($file.Name -ieq 'language.mix') { $reference = Join-Path (Split-Path $nestedRoot) 'language.mix_files\index.json' }
        if ($reference -and (Test-Path -LiteralPath $reference)) {
            $expected = @(Get-Content -LiteralPath $reference -Raw -Encoding utf8 | ConvertFrom-Json)
            if ($expected.Count -ne $result.count) { throw "MIX count differs from existing reference: $($file.Name)" }
            $byId = @{}
            foreach ($entry in $result.entries) { $byId[$entry.id] = $entry }
            foreach ($entry in $expected) {
                if (-not $byId.ContainsKey($entry.id) -or $byId[$entry.id].size -ne $entry.size) { throw "MIX entry differs from existing reference: $($entry.id)" }
            }
            $indexChecks += [pscustomobject]@{ source = $file.FullName; reference = $reference; entries_compared = $expected.Count }
        }
    }

    foreach ($file in @($iniFiles) + @($modFiles | Where-Object Extension -eq '.ini')) {
        $iniResults += RunTool @('ini', $file.FullName)
    }
    $spec = (Join-Path $Baseline 'ra2.mix') + '|local.mix'
    $queries += RunTool @('query','rules.ini','CNLTNK','Strength','--mix','10',$spec,'--dir','100',$Mod)
    if ($queries[-1].value -ne '400' -or $queries[-1].priority -ne 100) { throw 'MOD override failed.' }
    $queries += RunTool @('query','rules.ini','CNAPOC','Primary','--mix','10',$spec,'--dir','100',$Mod)
    $queries += RunTool @('resolve','ai.ini','--mix','10',$spec,'--dir','100',$Mod)
    if ($queries[-1].priority -ne 10) { throw 'Base fallback failed.' }
    $passed = $true
} catch {
    $problem = $_.Exception.Message
} finally {
    Write-Host 'Checking source preservation...'
    $hashAfter = FileHashes $inputs
    $inventoryAfter = OldInventory
    $hashAfter | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath (Join-Path $report 'inputs-after.json') -Encoding utf8
    $inventoryAfter | Set-Content -LiteralPath (Join-Path $report 'old-project-after.tsv') -Encoding utf8
    $hashChanges = @(Compare-Object $hashBefore $hashAfter -Property path,bytes,sha256)
    $metadataChanges = @(Compare-Object $inventoryBefore $inventoryAfter)
    if ($hashChanges.Count -or $metadataChanges.Count) { $passed = $false; $problem = 'Source inventory or input hashes changed during validation.' }
    $codePaths = @(Get-ChildItem -LiteralPath (Join-Path $root 'src'),(Join-Path $root 'include'),(Join-Path $root 'tests') -File -Recurse | Where-Object { $_.Extension -in '.c','.h' } | Select-Object -ExpandProperty FullName)
    $result = [ordered]@{
        created_utc = [DateTime]::UtcNow.ToString('o')
        passed = $passed
        problem = $problem
        project = $root
        tool_directory = $ToolDirectory
        c_standard = 'C17'
        c_tests = $unitResult
        archives = $archiveResults
        expected_input_rejections = $expectedRejections
        existing_index_checks = $indexChecks
        ini_files = $iniResults
        resource_queries = $queries
        preservation = [ordered]@{
            old_project = $OldProject
            inventory_files = $inventoryBefore.Count
            inventory_changes = $metadataChanges.Count
            hashed_inputs = $hashBefore.Count
            hash_changes = $hashChanges.Count
            scope = 'File names, lengths and write times for the old project; SHA-256 for the listed validation inputs. Comparison covers this validation run.'
        }
        sources = (FileHashes $codePaths)
        artifacts = (FileHashes @($tool,$tests,(Join-Path $ToolDirectory 'ra2resources.lib')))
        limitations = @('File/format validation only; no game simulation, rendering, runtime gameplay or performance acceptance.','INI compatibility behavior is documented reader behavior; not complete RA2 engine semantic equivalence.','Pre-existing MOVIES01.MIX integrity failure is a recorded rejection, not a successful asset validation.','CMake verification is recorded separately; non-Windows builds are not verified.')
    }
    $result | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath (Join-Path $report 'validation.json') -Encoding utf8
    [ordered]@{ report = (Join-Path $report 'validation.json'); passed = $passed } | ConvertTo-Json |
        Set-Content -LiteralPath (Join-Path $root ('reports\latest-' + $ReportLabel + '.json')) -Encoding utf8
}
Write-Host "Validation report: $report"
if (-not $passed) { throw $problem }
Write-Host "PASS: $($unitResult.checks) checks; $($archiveResults.Count) MIX archives accepted; $($expectedRejections.Count) known invalid inputs rejected; $($iniResults.Count) INI files; sources preserved."
