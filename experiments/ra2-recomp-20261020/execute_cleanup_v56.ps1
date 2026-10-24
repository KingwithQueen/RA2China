$ErrorActionPreference='Stop'
$taskStage=Join-Path $PSScriptRoot 'evidence\movement-state-v56'
$taskPlanPath=Join-Path $taskStage 'cleanup-plan.json'
$taskPlan=Get-Content -LiteralPath $taskPlanPath -Raw | ConvertFrom-Json
$taskWorkspace=[IO.Path]::GetFullPath($PSScriptRoot)
if($taskPlan.workspace -ne $taskWorkspace){throw 'Unexpected workspace'}
function Confirm-TaskPath([string]$taskInput){
    $taskAbsolute=[IO.Path]::GetFullPath($taskInput)
    if(-not $taskAbsolute.StartsWith($taskWorkspace+[IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase)){throw 'Path outside workspace'}
    $taskWalk=$taskAbsolute
    while($taskWalk -ne $taskWorkspace){
        $taskInfo=Get-Item -LiteralPath $taskWalk
        if($taskInfo.Attributes -band [IO.FileAttributes]::ReparsePoint){throw 'Reparse point refused'}
        $taskWalk=[IO.Path]::GetDirectoryName($taskWalk)
    }
    if((Get-Item -LiteralPath $taskWorkspace).Attributes -band [IO.FileAttributes]::ReparsePoint){throw 'Workspace reparse refused'}
    return $taskAbsolute
}
foreach($taskFile in $taskPlan.candidates){
    $taskAbsolute=Confirm-TaskPath $taskFile.path
    if([IO.Path]::GetDirectoryName($taskAbsolute) -notin $taskPlan.roots){throw 'Root mismatch'}
    $taskInfo=Get-Item -LiteralPath $taskAbsolute
    if($taskInfo.PSIsContainer -or $taskInfo.Length -ne $taskFile.bytes){throw 'Candidate changed'}
    switch($taskFile.kind){
        'reproducible-root-probe-object' {if([IO.Path]::GetExtension($taskAbsolute) -ne '.obj'){throw 'Wrong object suffix'}}
        'python-bytecode-cache' {if([IO.Path]::GetExtension($taskAbsolute) -ne '.pyc'){throw 'Wrong cache suffix'}}
        'scratch-difftest-with-retained-source' {if([IO.Path]::GetFileName($taskAbsolute) -ne 'difftest.exe' -or -not (Test-Path -LiteralPath ([IO.Path]::ChangeExtension($taskAbsolute,'.c')))){throw 'Scratch source absent'}}
        'redundant-private-copy-of-preserved-original-save' {if($taskAbsolute -ne (Join-Path $taskWorkspace 'temp\storage-probe-copy.sav')){throw 'Wrong private save'}}
        default {throw 'Unknown candidate kind'}
    }
    if((Get-FileHash -LiteralPath $taskAbsolute -Algorithm SHA256).Hash.ToLowerInvariant() -ne $taskFile.sha256){throw 'Candidate hash changed'}
}
foreach($taskFile in $taskPlan.protected){if((Get-FileHash -LiteralPath $taskFile.path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $taskFile.sha256){throw 'Protected file changed before cleanup'}}
foreach($taskFile in $taskPlan.candidates){Remove-Item -LiteralPath $taskFile.path}
foreach($taskDirectory in $taskPlan.empty_cache_directories){
    $taskAbsolute=Confirm-TaskPath $taskDirectory
    if(@(Get-ChildItem -LiteralPath $taskAbsolute).Count -eq 0){Remove-Item -LiteralPath $taskAbsolute}
}
foreach($taskFile in $taskPlan.candidates){if(Test-Path -LiteralPath $taskFile.path){throw 'Candidate remains'}}
foreach($taskFile in $taskPlan.protected){if((Get-FileHash -LiteralPath $taskFile.path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $taskFile.sha256){throw 'Protected file changed after cleanup'}}
@{passed=$true;deleted_files=$taskPlan.files;deleted_bytes=$taskPlan.bytes;protected_files=$taskPlan.protected.Count;protected_files_unchanged=$true;plan_sha256=(Get-FileHash -LiteralPath $taskPlanPath -Algorithm SHA256).Hash.ToLowerInvariant();method='Literal exact allowlist; no force or recursion';types=@($taskPlan.candidates | Group-Object kind | Select-Object Name,Count)} | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath (Join-Path $taskStage 'cleanup.json') -Encoding utf8NoBOM
Write-Output "Cleaned $($taskPlan.files) inactive scratch/cache files."
