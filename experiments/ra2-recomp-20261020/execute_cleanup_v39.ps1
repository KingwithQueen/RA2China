$ErrorActionPreference='Stop'
$taskStage=Join-Path $PSScriptRoot 'evidence\movement-state-v39'
$taskPlanPath=Join-Path $taskStage 'cleanup-plan.json'
$taskPlan=Get-Content -LiteralPath $taskPlanPath -Raw | ConvertFrom-Json
$taskExpected=@((Join-Path $PSScriptRoot 'evidence\movement-state-v38'),$taskStage)
foreach($taskRoot in $taskExpected){
    $taskPath=[IO.Path]::GetFullPath($taskRoot)
    while($taskPath){
        $taskInfo=Get-Item -LiteralPath $taskPath
        if($taskInfo.Attributes -band [IO.FileAttributes]::ReparsePoint){throw 'Reparse point refused'}
        if($taskPath -eq [IO.Path]::GetFullPath($PSScriptRoot)){break}
        $taskPath=[IO.Path]::GetDirectoryName($taskPath)
    }
}
foreach($taskFile in $taskPlan.candidates){
    $taskAbsolute=[IO.Path]::GetFullPath($taskFile.path)
    if([IO.Path]::GetDirectoryName($taskAbsolute) -notin $taskExpected -or [IO.Path]::GetExtension($taskAbsolute) -ne '.obj'){throw 'Candidate outside exact roots'}
    $taskInfo=Get-Item -LiteralPath $taskAbsolute
    if($taskInfo.PSIsContainer -or ($taskInfo.Attributes -band [IO.FileAttributes]::ReparsePoint) -or $taskInfo.Length -ne $taskFile.bytes){throw 'Candidate changed'}
    if((Get-FileHash -LiteralPath $taskAbsolute -Algorithm SHA256).Hash.ToLowerInvariant() -ne $taskFile.sha256){throw 'Candidate hash changed'}
}
foreach($taskFile in $taskPlan.protected){if((Get-FileHash -LiteralPath $taskFile.path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $taskFile.sha256){throw 'Protected file changed before cleanup'}}
foreach($taskFile in $taskPlan.candidates){Remove-Item -LiteralPath $taskFile.path}
foreach($taskFile in $taskPlan.candidates){if(Test-Path -LiteralPath $taskFile.path){throw 'Candidate remains'}}
foreach($taskFile in $taskPlan.protected){if((Get-FileHash -LiteralPath $taskFile.path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $taskFile.sha256){throw 'Protected file changed after cleanup'}}
@{passed=$true;deleted_files=$taskPlan.files;deleted_bytes=$taskPlan.bytes;protected_files=$taskPlan.protected.Count;protected_files_unchanged=$true;plan_sha256=(Get-FileHash -LiteralPath $taskPlanPath -Algorithm SHA256).Hash.ToLowerInvariant();method='Literal allowlist, hash checked, no force, no recursion'} | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $taskStage 'cleanup.json') -Encoding utf8NoBOM
Write-Output "Deleted $($taskPlan.files) reproducible object files."
