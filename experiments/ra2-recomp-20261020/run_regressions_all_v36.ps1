$ErrorActionPreference='Stop'
$taskPwsh=(Get-Process -Id $PID).Path
& $taskPwsh -NoProfile -File (Join-Path $PSScriptRoot 'run_regressions_v36.ps1') -RunId 01
if($LASTEXITCODE){throw 'Prior 38 regression groups failed'}
foreach($taskPair in @(
    @('round-probe','round_probe'),@('path-cost-probe','path_cost_probe'),
    @('walk-probe','walk_probe'),@('path-cache-probe','path_cache_probe'),
    @('path-heap-probe','path_heap_probe'),@('path-nodes-probe','path_nodes_probe'),
    @('path-distance-probe','path_distance_probe'),@('path-search-probe','path_search_probe')))
{
    $taskTool=$taskPair[0];$taskExe=$taskPair[1]
    & $taskPwsh -NoProfile -File (Join-Path $PSScriptRoot ('build-'+$taskTool+'-v36.ps1')) *> (Join-Path $PSScriptRoot ('evidence\movement-state-v36\final-build-'+$taskTool+'.log'))
    if($LASTEXITCODE){throw ($taskTool+' build failed')}
    Push-Location $PSScriptRoot
    try {
        & ('.\evidence\movement-state-v36\'+$taskExe+'.exe') '.\ra2\game\game.exe' *> ('.\evidence\movement-state-v36\'+$taskTool+'-verified-01.json')
        if($LASTEXITCODE){throw ($taskTool+' original fragment comparison failed')}
    } finally {Pop-Location}
}
& $taskPwsh -NoProfile -File (Join-Path $PSScriptRoot 'build-path-lifecycle-probe-v36.ps1') *> (Join-Path $PSScriptRoot 'evidence\movement-state-v36\final-build-lifecycle.log')
if($LASTEXITCODE){throw 'Lifecycle probe build failed'}
$taskNames=@('path-prepare-probe','region-route-probe','path-rebuild-probe')
foreach($taskPhase in 0..2){
    Push-Location $PSScriptRoot
    try {
        & '.\evidence\movement-state-v36\path_lifecycle_probe.exe' '.\ra2\game\game.exe' $taskPhase *> ('.\evidence\movement-state-v36\'+$taskNames[$taskPhase]+'-verified-01.json')
        if($LASTEXITCODE){throw 'Lifecycle original comparison failed'}
    } finally {Pop-Location}
}

& $taskPwsh -NoProfile -File (Join-Path $PSScriptRoot 'build-region-search-probe-v36.ps1') *> (Join-Path $PSScriptRoot 'evidence\movement-state-v36\final-build-region-search.log')
if($LASTEXITCODE){throw 'Region build failed'}
& (Join-Path $PSScriptRoot 'evidence\movement-state-v36\region_search_probe.exe') (Join-Path $PSScriptRoot 'ra2\game\game.exe') *> (Join-Path $PSScriptRoot 'evidence\movement-state-v36\region-search-probe-verified-01.json')
if($LASTEXITCODE){throw 'Region original comparison failed'}
& $taskPwsh -NoProfile -File (Join-Path $PSScriptRoot 'build-path-optimize-probe-v36.ps1') *> (Join-Path $PSScriptRoot 'evidence\movement-state-v36\final-build-optimize.log')
if($LASTEXITCODE){throw 'Optimization build failed'}
$taskOptimizeNames=@('path-smoothing-probe','path-postprocess-probe')
foreach($taskPhase in 0..1){
 & (Join-Path $PSScriptRoot 'evidence\movement-state-v36\path_optimize_probe.exe') (Join-Path $PSScriptRoot 'ra2\game\game.exe') $taskPhase *> (Join-Path $PSScriptRoot ('evidence\movement-state-v36\'+$taskOptimizeNames[$taskPhase]+'-verified-01.json'))
 if($LASTEXITCODE){throw 'Optimization original comparison failed'}
}

& $taskPwsh -NoProfile -File (Join-Path $PSScriptRoot 'build-path-local-probe-v36.ps1') *> (Join-Path $PSScriptRoot 'evidence\movement-state-v36\final-build-local.log')
if($LASTEXITCODE){throw 'Local path build failed'}
$taskLocalNames=@('path-anchor-probe','path-turn-rewrite-probe','path-segment-rewrite-probe','path-completion-probe')
foreach($taskPhase in 0..3){
 & (Join-Path $PSScriptRoot 'evidence\movement-state-v36\path_local_probe.exe') (Join-Path $PSScriptRoot 'ra2\game\game.exe') $taskPhase *> (Join-Path $PSScriptRoot ('evidence\movement-state-v36\'+$taskLocalNames[$taskPhase]+'-verified-01.json'))
 if($LASTEXITCODE){throw 'Local path original comparison failed'}
}

& $taskPwsh -NoProfile -File (Join-Path $PSScriptRoot 'build-ground-services-probe-v36.ps1') *> (Join-Path $PSScriptRoot 'evidence\movement-state-v36\final-build-services.log')
if($LASTEXITCODE){throw 'Ground services build failed'}
$taskServiceNames=@('advance-interpolation-probe','prepare-shared-probe','cell-services-probe')
foreach($taskPhase in 0..2){
 & (Join-Path $PSScriptRoot 'evidence\movement-state-v36\ground_services_probe.exe') (Join-Path $PSScriptRoot 'ra2\game\game.exe') $taskPhase *> (Join-Path $PSScriptRoot ('evidence\movement-state-v36\'+$taskServiceNames[$taskPhase]+'-verified-01.json'))
 if($LASTEXITCODE){throw 'Ground services original comparison failed'}
}

& $taskPwsh -NoProfile -File (Join-Path $PSScriptRoot 'build-dispatch-probe-v36.ps1') *> (Join-Path $PSScriptRoot 'evidence\movement-state-v36\final-build-dispatch.log')
if($LASTEXITCODE){throw 'Route control probe build failed'}
$taskRouteNames=@('advance-sampling-probe','prepare-exits-probe','object-terrain-services-probe')
foreach($taskPhase in 0..2){
 & (Join-Path $PSScriptRoot 'evidence\movement-state-v36\route_control_probe.exe') (Join-Path $PSScriptRoot 'ra2\game\game.exe') $taskPhase *> (Join-Path $PSScriptRoot ('evidence\movement-state-v36\'+$taskRouteNames[$taskPhase]+'-verified-01.json'))
 if($LASTEXITCODE){throw 'Route control original comparison failed'}
}

& $taskPwsh -NoProfile -File (Join-Path $PSScriptRoot 'build-completion-probe-v36.ps1') *> (Join-Path $PSScriptRoot 'evidence\movement-state-v36\final-build-completion.log')
if($LASTEXITCODE){throw 'Completion probe build failed'}
& (Join-Path $PSScriptRoot 'evidence\movement-state-v36\arrival_complete_probe.exe') (Join-Path $PSScriptRoot 'ra2\game\game.exe') *> (Join-Path $PSScriptRoot 'evidence\movement-state-v36\advance-arrival-completion-probe-verified-01.json')
if($LASTEXITCODE){throw 'Arrival completion comparison failed'}
$taskCompletionNames=@('prepare-target-cleanup-probe','base-passage-probe','ground-height-entry-probe')
foreach($taskPhase in 0..2){
 & (Join-Path $PSScriptRoot 'evidence\movement-state-v36\completion_services_probe.exe') (Join-Path $PSScriptRoot 'ra2\game\game.exe') $taskPhase *> (Join-Path $PSScriptRoot ('evidence\movement-state-v36\'+$taskCompletionNames[$taskPhase]+'-verified-01.json'))
 if($LASTEXITCODE){throw 'Completion service comparison failed'}
}

& $taskPwsh -NoProfile -File (Join-Path $PSScriptRoot 'build-remainder-probe-v36.ps1') *> (Join-Path $PSScriptRoot 'evidence\movement-state-v36\final-build-remainder.log')
if($LASTEXITCODE){throw 'Remainder probe build failed'}
$taskRemainderNames=@('advance-landing-probe','prepare-failure-tails-probe','slope-height-probe')
foreach($taskPhase in 0..2){
 & (Join-Path $PSScriptRoot 'evidence\movement-state-v36\remainder_probe.exe') (Join-Path $PSScriptRoot 'ra2\game\game.exe') $taskPhase *> (Join-Path $PSScriptRoot ('evidence\movement-state-v36\'+$taskRemainderNames[$taskPhase]+'-verified-01.json'))
 if($LASTEXITCODE){throw 'Remainder original comparison failed'}
}

& $taskPwsh -NoProfile -File (Join-Path $PSScriptRoot 'build-internal-probe-v36.ps1') *> (Join-Path $PSScriptRoot 'evidence\movement-state-v36\final-build-internal.log')
if($LASTEXITCODE){throw 'Internal probe build failed'}
$taskInternalNames=@('advance-shared-sampling-probe','prepare-internal-probe')
foreach($taskPhase in 0..1){
 & (Join-Path $PSScriptRoot 'evidence\movement-state-v36\internal_probe.exe') (Join-Path $PSScriptRoot 'ra2\game\game.exe') $taskPhase *> (Join-Path $PSScriptRoot ('evidence\movement-state-v36\'+$taskInternalNames[$taskPhase]+'-verified-01.json'))
 if($LASTEXITCODE){throw 'Internal original comparison failed'}
}

& $taskPwsh -NoProfile -File (Join-Path $PSScriptRoot 'build-connection-numeric-probe-v36.ps1') *> (Join-Path $PSScriptRoot 'evidence\movement-state-v36\final-build-connection-numeric.log')
if($LASTEXITCODE){throw 'Connection numeric build failed'}
& (Join-Path $PSScriptRoot 'evidence\movement-state-v36\connection_numeric_probe.exe') (Join-Path $PSScriptRoot 'ra2\game\game.exe') *> (Join-Path $PSScriptRoot 'evidence\movement-state-v36\connection-numeric-probe-verified-01.json')
if($LASTEXITCODE){throw 'Connection numeric comparison failed'}

& $taskPwsh -NoProfile -File (Join-Path $PSScriptRoot 'build-tube-state-probe-v36.ps1') *> (Join-Path $PSScriptRoot 'evidence\movement-state-v36\final-build-tube-state.log')
if($LASTEXITCODE){throw 'Tube state probe build failed'}
$taskTubeNames=@('tube-exit-probe','movement-handoff-probe','surface-class-probe','tube-waypoint-probe')
foreach($taskPhase in 0..3){
 & (Join-Path $PSScriptRoot 'evidence\movement-state-v36\tube_state_probe.exe') (Join-Path $PSScriptRoot 'ra2\game\game.exe') $taskPhase *> (Join-Path $PSScriptRoot ('evidence\movement-state-v36\'+$taskTubeNames[$taskPhase]+'-verified-01.json'))
 if($LASTEXITCODE){throw 'Tube state original comparison failed'}
}

& $taskPwsh -NoProfile -File (Join-Path $PSScriptRoot 'build-progress-probe-v36.ps1') *> (Join-Path $PSScriptRoot 'evidence\movement-state-v36\final-build-progress.log')
if($LASTEXITCODE){throw 'Progress native build failed'}
$taskProgressNames=@('tube-approach-probe','tube-height-progress-probe','movement-internal-next-probe','object-passage-finish-probe')
foreach($taskPhase in 0..3){
 & (Join-Path $PSScriptRoot 'evidence\movement-state-v36\progress_probe.exe') (Join-Path $PSScriptRoot 'ra2\game\game.exe') $taskPhase *> (Join-Path $PSScriptRoot ('evidence\movement-state-v36\'+$taskProgressNames[$taskPhase]+'-verified-01.json'))
 if($LASTEXITCODE){throw 'Progress original comparison failed'}
}

& $taskPwsh -NoProfile -File (Join-Path $PSScriptRoot 'build-travel-probe-v36.ps1') *> (Join-Path $PSScriptRoot 'evidence\movement-state-v36\final-build-travel.log')
if($LASTEXITCODE){throw 'Travel probe build failed'}
$taskTravelNames=@('tube-entry-preparation-probe','tube-remaining-horizontal-probe','tube-regular-horizontal-probe','movement-next-template-probe','neighbor-passage-probe')
foreach($taskPhase in 0..4){
 & (Join-Path $PSScriptRoot 'evidence\movement-state-v36\travel_probe.exe') (Join-Path $PSScriptRoot 'ra2\game\game.exe') $taskPhase *> (Join-Path $PSScriptRoot ('evidence\movement-state-v36\'+$taskTravelNames[$taskPhase]+'-verified-01.json'))
 if($LASTEXITCODE){throw 'Travel original comparison failed'}
}
