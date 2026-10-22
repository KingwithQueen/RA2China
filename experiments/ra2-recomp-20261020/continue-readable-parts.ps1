$ErrorActionPreference = 'Stop'
$python = 'E:\Program Files\Python\python.exe'
Push-Location $PSScriptRoot
try
{
    $previous = 'fraction'
    foreach ($part in @('interpolation', 'transform', 'arrival'))
    {
        $report = Get-Content -LiteralPath ".\evidence\movement-readable-v1\runs\$previous\comparison.json" -Raw | ConvertFrom-Json
        if (-not $report.passed) { throw "Previous stage did not pass: $previous" }
        & $python -B .\extract_readable_movement.py $part
        if ($LASTEXITCODE -ne 0) { throw "Extraction failed: $part" }
        & .\build-faithful.ps1 -Parallel 4 *> ".\evidence\movement-readable-v1\build-$part.log"
        if ($LASTEXITCODE -ne 0) { throw "Build failed: $part" }
        & $python -B .\run_state_comparison.py --evidence-stage movement-readable-v1 --tag $part --range 0:2350 --detail-id 1032341 *> ".\evidence\movement-readable-v1\$part.log"
        if ($LASTEXITCODE -ne 0) { throw "Original comparison failed: $part" }
        Write-Output "Verified: $part"
        $previous = $part
    }
}
finally
{
    Pop-Location
}
