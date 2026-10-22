$ErrorActionPreference = 'Stop'
$taskPwsh = (Get-Process -Id $PID).Path
foreach ($taskBuild in @('movement-probe','state-probes','prepare-probes','obstacle-probe','segment-probe','speed-ramp-probe','wait-probe','terrain-probe','reaction-probe'))
{
    & $taskPwsh -NoProfile -File (Join-Path $PSScriptRoot ('build-' + $taskBuild + '-v5.ps1')) *> (Join-Path $PSScriptRoot ('evidence\movement-state-v5\regression-build-' + $taskBuild + '-isolated.log'))
    if ($LASTEXITCODE) { throw ($taskBuild + ' build failed') }
}
Push-Location $PSScriptRoot
try
{
    foreach ($taskProbe in @('movement_probe','original_movement_probe','path_fragment_probe','drive_process_probe','collision_probe','arrival_probe','prepare_probe','recovery_probe','barrier_probe','obstacle_probe','segment_probe','speed_ramp_probe','terrain_probe'))
    {
        & ('.\evidence\movement-state-v5\' + $taskProbe + '.exe') '.\ra2\game\game.exe' *> ('.\evidence\movement-state-v5\' + $taskProbe + '-verified.json')
        if ($LASTEXITCODE) { throw ($taskProbe + ' failed') }
    }
    foreach ($taskPhase in 0..2)
    {
        & '.\evidence\movement-state-v5\wait_probe.exe' '.\ra2\game\game.exe' $taskPhase *> ('.\evidence\movement-state-v5\wait_probe-' + $taskPhase + '-verified.json')
        if ($LASTEXITCODE) { throw 'Wait probe failed' }
    }
    foreach ($taskPhase in 0..3)
    {
        & '.\evidence\movement-state-v5\reaction_probe.exe' '.\ra2\game\game.exe' $taskPhase *> ('.\evidence\movement-state-v5\reaction_probe-' + $taskPhase + '-verified.json')
        if ($LASTEXITCODE) { throw 'Reaction probe failed' }
    }
}
finally
{
    Pop-Location
}
