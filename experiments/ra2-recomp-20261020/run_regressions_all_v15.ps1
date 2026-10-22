$ErrorActionPreference='Stop'
$taskPwsh=(Get-Process -Id $PID).Path
& $taskPwsh -NoProfile -File (Join-Path $PSScriptRoot 'run_regressions_v15.ps1') -RunId 01
if($LASTEXITCODE){throw 'Prior 38 regression groups failed'}
foreach($taskPair in @(
    @('round-probe','round_probe'),@('path-cost-probe','path_cost_probe'),
    @('walk-probe','walk_probe'),@('path-cache-probe','path_cache_probe'),
    @('path-heap-probe','path_heap_probe'),@('path-nodes-probe','path_nodes_probe'),
    @('path-distance-probe','path_distance_probe'),@('path-search-probe','path_search_probe')))
{
    $taskTool=$taskPair[0];$taskExe=$taskPair[1]
    & $taskPwsh -NoProfile -File (Join-Path $PSScriptRoot ('build-'+$taskTool+'-v15.ps1')) *> (Join-Path $PSScriptRoot ('evidence\movement-state-v15\final-build-'+$taskTool+'.log'))
    if($LASTEXITCODE){throw ($taskTool+' build failed')}
    Push-Location $PSScriptRoot
    try {
        & ('.\evidence\movement-state-v15\'+$taskExe+'.exe') '.\ra2\game\game.exe' *> ('.\evidence\movement-state-v15\'+$taskTool+'-verified-01.json')
        if($LASTEXITCODE){throw ($taskTool+' original fragment comparison failed')}
    } finally {Pop-Location}
}
& $taskPwsh -NoProfile -File (Join-Path $PSScriptRoot 'build-path-lifecycle-probe-v15.ps1') *> (Join-Path $PSScriptRoot 'evidence\movement-state-v15\final-build-lifecycle.log')
if($LASTEXITCODE){throw 'Lifecycle probe build failed'}
$taskNames=@('path-prepare-probe','region-route-probe','path-rebuild-probe')
foreach($taskPhase in 0..2){
    Push-Location $PSScriptRoot
    try {
        & '.\evidence\movement-state-v15\path_lifecycle_probe.exe' '.\ra2\game\game.exe' $taskPhase *> ('.\evidence\movement-state-v15\'+$taskNames[$taskPhase]+'-verified-01.json')
        if($LASTEXITCODE){throw 'Lifecycle original comparison failed'}
    } finally {Pop-Location}
}
