$ErrorActionPreference='Stop'
$taskPwsh=(Get-Process -Id $PID).Path
& $taskPwsh -NoProfile -File (Join-Path $PSScriptRoot 'run_regressions_v18.ps1') -RunId 01
if($LASTEXITCODE){throw 'Prior 38 regression groups failed'}
foreach($taskPair in @(
    @('round-probe','round_probe'),@('path-cost-probe','path_cost_probe'),
    @('walk-probe','walk_probe'),@('path-cache-probe','path_cache_probe'),
    @('path-heap-probe','path_heap_probe'),@('path-nodes-probe','path_nodes_probe'),
    @('path-distance-probe','path_distance_probe'),@('path-search-probe','path_search_probe')))
{
    $taskTool=$taskPair[0];$taskExe=$taskPair[1]
    & $taskPwsh -NoProfile -File (Join-Path $PSScriptRoot ('build-'+$taskTool+'-v18.ps1')) *> (Join-Path $PSScriptRoot ('evidence\movement-state-v18\final-build-'+$taskTool+'.log'))
    if($LASTEXITCODE){throw ($taskTool+' build failed')}
    Push-Location $PSScriptRoot
    try {
        & ('.\evidence\movement-state-v18\'+$taskExe+'.exe') '.\ra2\game\game.exe' *> ('.\evidence\movement-state-v18\'+$taskTool+'-verified-01.json')
        if($LASTEXITCODE){throw ($taskTool+' original fragment comparison failed')}
    } finally {Pop-Location}
}
& $taskPwsh -NoProfile -File (Join-Path $PSScriptRoot 'build-path-lifecycle-probe-v18.ps1') *> (Join-Path $PSScriptRoot 'evidence\movement-state-v18\final-build-lifecycle.log')
if($LASTEXITCODE){throw 'Lifecycle probe build failed'}
$taskNames=@('path-prepare-probe','region-route-probe','path-rebuild-probe')
foreach($taskPhase in 0..2){
    Push-Location $PSScriptRoot
    try {
        & '.\evidence\movement-state-v18\path_lifecycle_probe.exe' '.\ra2\game\game.exe' $taskPhase *> ('.\evidence\movement-state-v18\'+$taskNames[$taskPhase]+'-verified-01.json')
        if($LASTEXITCODE){throw 'Lifecycle original comparison failed'}
    } finally {Pop-Location}
}

& $taskPwsh -NoProfile -File (Join-Path $PSScriptRoot 'build-region-search-probe-v18.ps1') *> (Join-Path $PSScriptRoot 'evidence\movement-state-v18\final-build-region-search.log')
if($LASTEXITCODE){throw 'Region build failed'}
& (Join-Path $PSScriptRoot 'evidence\movement-state-v18\region_search_probe.exe') (Join-Path $PSScriptRoot 'ra2\game\game.exe') *> (Join-Path $PSScriptRoot 'evidence\movement-state-v18\region-search-probe-verified-01.json')
if($LASTEXITCODE){throw 'Region original comparison failed'}
& $taskPwsh -NoProfile -File (Join-Path $PSScriptRoot 'build-path-optimize-probe-v18.ps1') *> (Join-Path $PSScriptRoot 'evidence\movement-state-v18\final-build-optimize.log')
if($LASTEXITCODE){throw 'Optimization build failed'}
$taskOptimizeNames=@('path-smoothing-probe','path-postprocess-probe')
foreach($taskPhase in 0..1){
 & (Join-Path $PSScriptRoot 'evidence\movement-state-v18\path_optimize_probe.exe') (Join-Path $PSScriptRoot 'ra2\game\game.exe') $taskPhase *> (Join-Path $PSScriptRoot ('evidence\movement-state-v18\'+$taskOptimizeNames[$taskPhase]+'-verified-01.json'))
 if($LASTEXITCODE){throw 'Optimization original comparison failed'}
}

& $taskPwsh -NoProfile -File (Join-Path $PSScriptRoot 'build-path-local-probe-v18.ps1') *> (Join-Path $PSScriptRoot 'evidence\movement-state-v18\final-build-local.log')
if($LASTEXITCODE){throw 'Local path build failed'}
$taskLocalNames=@('path-anchor-probe','path-turn-rewrite-probe','path-segment-rewrite-probe','path-completion-probe')
foreach($taskPhase in 0..3){
 & (Join-Path $PSScriptRoot 'evidence\movement-state-v18\path_local_probe.exe') (Join-Path $PSScriptRoot 'ra2\game\game.exe') $taskPhase *> (Join-Path $PSScriptRoot ('evidence\movement-state-v18\'+$taskLocalNames[$taskPhase]+'-verified-01.json'))
 if($LASTEXITCODE){throw 'Local path original comparison failed'}
}

& $taskPwsh -NoProfile -File (Join-Path $PSScriptRoot 'build-ground-services-probe-v18.ps1') *> (Join-Path $PSScriptRoot 'evidence\movement-state-v18\final-build-services.log')
if($LASTEXITCODE){throw 'Ground services build failed'}
$taskServiceNames=@('advance-interpolation-probe','prepare-shared-probe','cell-services-probe')
foreach($taskPhase in 0..2){
 & (Join-Path $PSScriptRoot 'evidence\movement-state-v18\ground_services_probe.exe') (Join-Path $PSScriptRoot 'ra2\game\game.exe') $taskPhase *> (Join-Path $PSScriptRoot ('evidence\movement-state-v18\'+$taskServiceNames[$taskPhase]+'-verified-01.json'))
 if($LASTEXITCODE){throw 'Ground services original comparison failed'}
}
