from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent
OLD = ROOT/'evidence/movement-state-v6'
NEW = ROOT/'evidence/movement-state-v7'
names = ['movement_probe','original_movement_probe','path_fragment_probe','drive_process_probe','collision_probe',
    'arrival_probe','prepare_probe','recovery_probe','barrier_probe','obstacle_probe','segment_probe','speed_ramp_probe',
    'wait_probe','terrain_probe','reaction_probe','special_probe','template_probe','audit_noop']
for name in names:
    shutil.copy2(OLD/(name+'.c'),NEW/(name+'.c'))
for name in ('movement-probe','state-probes','prepare-probes','obstacle-probe','segment-probe','speed-ramp-probe',
             'wait-probe','terrain-probe','reaction-probe','special-probe','template-probe'):
    text = (ROOT/('build-'+name+'-v6.ps1')).read_text(encoding='utf-8').replace('movement-state-v6','movement-state-v7')
    (ROOT/('build-'+name+'-v7.ps1')).write_text(text,encoding='utf-8',newline='\n')
text = (ROOT/'run_regressions_v6.ps1').read_text(encoding='utf-8')
text = text.replace('movement-state-v6','movement-state-v7').replace("'-v6.ps1'","'-v7.ps1'")
text = text.replace("'special-probe','template-probe'", "'special-probe','template-probe','followup-probe','turn-probe'")
text = text.replace("'special_probe','template_probe'", "'special_probe','template_probe','followup_probe','turn_probe'")
text = text.replace("elseif ($taskProbe -eq 'template_probe') { 4 } else", "elseif ($taskProbe -eq 'template_probe') { 4 } elseif ($taskProbe -eq 'followup_probe') { 1 } elseif ($taskProbe -eq 'turn_probe') { 0 } else")
(ROOT/'run_regressions_v7.ps1').write_text(text,encoding='utf-8',newline='\n')
text = (ROOT/'run_movement_v6_matrix.py').read_text(encoding='utf-8').replace('movement-state-v6','movement-state-v7')
text = text.replace('"""第五批：','"""第七批：')
if not (ROOT/'run_movement_v7_matrix.py').exists():
    (ROOT/'run_movement_v7_matrix.py').write_text(text,encoding='utf-8',newline='\n')
text = (ROOT/'run_movement_v6_auxiliary.py').read_text(encoding='utf-8').replace('movement-state-v6','movement-state-v7')
if not (ROOT/'run_movement_v7_auxiliary.py').exists():
    (ROOT/'run_movement_v7_auxiliary.py').write_text(text,encoding='utf-8',newline='\n')
for name in ('cloaked-corridor.MAP','restricted-clear.MAP','restricted-rock.MAP'):
    target = NEW/'fixtures'/name
    target.parent.mkdir(exist_ok=True)
    shutil.copy2(OLD/'fixtures'/name,target)
