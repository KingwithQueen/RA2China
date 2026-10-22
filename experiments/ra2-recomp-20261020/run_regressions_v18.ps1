param([string]$RunId = '01')
$ErrorActionPreference = 'Stop'
$taskPwsh = (Get-Process -Id $PID).Path
foreach ($taskBuild in @('movement-probe','state-probes','prepare-probes','obstacle-probe','segment-probe','speed-ramp-probe','wait-probe','terrain-probe','reaction-probe','special-probe','template-probe','followup-probe','turn-probe','advance-probe','entry-probe','continuation-probe','objects-probe','allied-probe','tail-probe'))
{
    & $taskPwsh -NoProfile -File (Join-Path $PSScriptRoot ('build-' + $taskBuild + '-v18.ps1')) *> (Join-Path $PSScriptRoot ('evidence\movement-state-v18\regression-' + $RunId + '-build-' + $taskBuild + '.log'))
    if ($LASTEXITCODE) { throw ($taskBuild + ' build failed') }
}
Push-Location $PSScriptRoot
try
{
    foreach ($taskProbe in @('movement_probe','original_movement_probe','path_fragment_probe','drive_process_probe','collision_probe','arrival_probe','prepare_probe','recovery_probe','barrier_probe','obstacle_probe','segment_probe','speed_ramp_probe','terrain_probe','advance_probe','entry_probe','continuation_probe','allied_probe','tail_probe'))
    {
        & ('.\evidence\movement-state-v18\' + $taskProbe + '.exe') '.\ra2\game\game.exe' *> ('.\evidence\movement-state-v18\' + $taskProbe + '-verified-' + $RunId + '.json')
        if ($LASTEXITCODE) { throw ($taskProbe + ' failed') }
    }
    foreach ($taskProbe in @('wait_probe','reaction_probe','special_probe','template_probe','followup_probe','turn_probe'))
    {
        $taskMaxPhase = if ($taskProbe -eq 'reaction_probe') { 3 } elseif ($taskProbe -eq 'special_probe') { 0 } elseif ($taskProbe -eq 'template_probe') { 4 } elseif ($taskProbe -eq 'followup_probe') { 1 } elseif ($taskProbe -eq 'turn_probe') { 0 } else { 2 }
        foreach ($taskPhase in 0..$taskMaxPhase)
        {
            & ('.\evidence\movement-state-v18\' + $taskProbe + '.exe') '.\ra2\game\game.exe' $taskPhase *> ('.\evidence\movement-state-v18\' + $taskProbe + '-' + $taskPhase + '-verified-' + $RunId + '.json')
            if ($LASTEXITCODE) { throw ($taskProbe + ' failed') }
        }
    }
    foreach ($taskPhase in 0..3)
    {
        & '.\evidence\movement-state-v18\objects_probe.exe' '.\ra2\game\game.exe' $taskPhase *> ('.\evidence\movement-state-v18\objects_probe-' + $taskPhase + '-verified-' + $RunId + '.json')
        if ($LASTEXITCODE) { throw 'Objects probe failed' }
    }
}
finally { Pop-Location }
