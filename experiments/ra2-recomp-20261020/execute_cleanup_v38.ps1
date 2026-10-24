$ErrorActionPreference='Stop'
$taskRoot=[IO.Path]::GetFullPath($PSScriptRoot)
$taskStage=Join-Path $taskRoot 'evidence\movement-state-v38'
$taskPlanPath=Join-Path $taskStage 'cleanup-plan.json'
$taskPlan=Get-Content -LiteralPath $taskPlanPath -Raw | ConvertFrom-Json
if(-not $taskPlan.passed -or -not $taskPlan.authorized_by_current_user_cleanup_request){throw 'Invalid cleanup authority'}
$taskTargets=@()
foreach($taskEntry in $taskPlan.files){
 $taskTarget=[IO.Path]::GetFullPath((Join-Path $taskRoot $taskEntry.path))
 $taskAllowed=@((Join-Path $taskRoot 'evidence\movement-state-v36'),(Join-Path $taskRoot 'evidence\movement-state-v37'))
 if([IO.Path]::GetDirectoryName($taskTarget) -notin $taskAllowed -or [IO.Path]::GetExtension($taskTarget) -ne '.obj'){throw 'Cleanup path outside allowlist'}
 $taskItem=Get-Item -LiteralPath $taskTarget
 foreach($taskAncestor in @($taskItem,$taskItem.Directory,$taskItem.Directory.Parent,$taskItem.Directory.Parent.Parent)){
  if($taskAncestor.Attributes -band [IO.FileAttributes]::ReparsePoint){throw 'Reparse point prohibited'}
 }
 if($taskItem.Length -ne $taskEntry.bytes -or (Get-FileHash -LiteralPath $taskTarget -Algorithm SHA256).Hash.ToLowerInvariant() -ne $taskEntry.sha256){throw 'Cleanup input changed'}
 $taskTargets+=$taskTarget
}
foreach($taskTarget in $taskTargets){Remove-Item -LiteralPath $taskTarget}
foreach($taskTarget in $taskTargets){if(Test-Path -LiteralPath $taskTarget){throw 'Cleanup incomplete'}}
foreach($taskEntry in $taskPlan.protected_files){
 $taskTarget=Join-Path $taskRoot $taskEntry.path
 if((Get-FileHash -LiteralPath $taskTarget -Algorithm SHA256).Hash.ToLowerInvariant() -ne $taskEntry.sha256){throw 'Protected file changed'}
}
$taskReceipt=@{passed=$true;deleted_files=$taskTargets.Count;deleted_bytes=$taskPlan.total_bytes;protected_files=$taskPlan.protected_files.Count;protected_files_unchanged=$true;plan_sha256=(Get-FileHash -LiteralPath $taskPlanPath -Algorithm SHA256).Hash.ToLowerInvariant();method='Hash-checked literal file deletion; no force, no recursion';authorized_by_current_user_cleanup_request=$true}
$taskReceipt | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $taskStage 'cleanup.json') -Encoding utf8
$taskReceipt | ConvertTo-Json -Compress
