from pathlib import Path
import shutil
ROOT=Path(__file__).resolve().parent;OLD=ROOT/'evidence/movement-state-v8';NEW=ROOT/'evidence/movement-state-v9'
names=['movement_probe','original_movement_probe','path_fragment_probe','drive_process_probe','collision_probe',
    'arrival_probe','prepare_probe','recovery_probe','barrier_probe','obstacle_probe','segment_probe','speed_ramp_probe',
    'wait_probe','terrain_probe','reaction_probe','special_probe','template_probe','followup_probe','turn_probe','audit_noop','advance_probe','entry_probe']
for name in names: shutil.copy2(OLD/(name+'.c'),NEW/(name+'.c'))
for name in ('movement-probe','state-probes','prepare-probes','obstacle-probe','segment-probe','speed-ramp-probe',
    'wait-probe','terrain-probe','reaction-probe','special-probe','template-probe','followup-probe','turn-probe','advance-probe','entry-probe'):
    text=(ROOT/('build-'+name+'-v8.ps1')).read_text(encoding='utf-8').replace('movement-state-v8','movement-state-v9')
    (ROOT/('build-'+name+'-v9.ps1')).write_text(text,encoding='utf-8',newline='\n')
p=ROOT/'run_regressions_v9.ps1'
t=(ROOT/'run_regressions_v8.ps1').read_text(encoding='utf-8').replace('movement-state-v8','movement-state-v9').replace('-v8.ps1','-v9.ps1')
t=t.replace("'followup-probe','turn-probe'","'followup-probe','turn-probe','advance-probe','entry-probe','continuation-probe','objects-probe'")
t=t.replace("'speed_ramp_probe','terrain_probe'","'speed_ramp_probe','terrain_probe','advance_probe','entry_probe','continuation_probe'")
needle='}\nfinally { Pop-Location }'
if needle not in t: needle='}\nfinally\n{\n    Pop-Location\n}'
assert needle in t
t=t.replace(needle,'''    foreach ($taskPhase in 0..3)
    {
        & '.\\evidence\\movement-state-v9\\objects_probe.exe' '.\\ra2\\game\\game.exe' $taskPhase *> ('.\\evidence\\movement-state-v9\\objects_probe-' + $taskPhase + '-verified-' + $RunId + '.json')
        if ($LASTEXITCODE) { throw 'Objects probe failed' }
    }
'''+needle)
p.write_text(t,encoding='utf-8',newline='\n')
for old,new in [('run_movement_v8_matrix.py','run_movement_v9_matrix.py'),('run_scenes_v8.py','run_scenes_v9.py'),
                ('run_movement_v8_auxiliary.py','run_movement_v9_auxiliary.py')]:
    t=(ROOT/old).read_text(encoding='utf-8').replace('movement-state-v8','movement-state-v9').replace('第八批','第九批')
    if old=='run_scenes_v8.py':
        t=t.replace("prefix=sys.argv[1] if len(sys.argv)>1 else 'd-'",'''cases += [
    ('long','dynamic-far-base.MAP','0:1500',['--order','5:1022579:2:100:114']),
    ('second-failure','dynamic-far-base.MAP','0:650',['--order','5:1022579:2:100:114','--unit-ring','398:1022579:2'])]
prefix=sys.argv[1] if len(sys.argv)>1 else 'i-' ''')
    (ROOT/new).write_text(t,encoding='utf-8',newline='\n')
(NEW/'fixtures').mkdir(exist_ok=True)
for p in (OLD/'fixtures').glob('*'):
    if p.is_file(): shutil.copy2(p,NEW/'fixtures'/p.name)
