from pathlib import Path
import shutil
ROOT=Path(__file__).resolve().parent
OLD=ROOT/'evidence/movement-state-v7'; NEW=ROOT/'evidence/movement-state-v8'
for name in ('movement_probe','original_movement_probe','path_fragment_probe','drive_process_probe','collision_probe',
    'arrival_probe','prepare_probe','recovery_probe','barrier_probe','obstacle_probe','segment_probe','speed_ramp_probe',
    'wait_probe','terrain_probe','reaction_probe','special_probe','template_probe','followup_probe','turn_probe','audit_noop'):
    shutil.copy2(OLD/(name+'.c'),NEW/(name+'.c'))
for name in ('movement-probe','state-probes','prepare-probes','obstacle-probe','segment-probe','speed-ramp-probe',
             'wait-probe','terrain-probe','reaction-probe','special-probe','template-probe','followup-probe','turn-probe'):
    text=(ROOT/('build-'+name+'-v7.ps1')).read_text(encoding='utf-8').replace('movement-state-v7','movement-state-v8')
    (ROOT/('build-'+name+'-v8.ps1')).write_text(text,encoding='utf-8',newline='\n')
for name in ('run_regressions','run_movement_matrix','run_movement_auxiliary'):
    old_name={'run_regressions':'run_regressions_v7.ps1','run_movement_matrix':'run_movement_v7_matrix.py','run_movement_auxiliary':'run_movement_v7_auxiliary.py'}[name]
    text=(ROOT/old_name).read_text(encoding='utf-8').replace('movement-state-v7','movement-state-v8').replace('-v7.ps1','-v8.ps1').replace('第七批','第八批')
    (ROOT/old_name.replace('v7','v8')).write_text(text,encoding='utf-8',newline='\n')
(NEW/'fixtures').mkdir(exist_ok=True)
for p in (OLD/'fixtures').glob('*'):
    if p.is_file(): shutil.copy2(p,NEW/'fixtures'/p.name)
p=NEW/'advance_probe.c'; t=p.read_text(encoding='utf-8')
if 'void ra2_state_movement_audit' not in t:
    t+='\nvoid ra2_state_movement_audit(uint32_t stage,uint32_t actor,uint32_t cell,uint32_t object)\n{ (void)stage; (void)actor; (void)cell; (void)object; }\n'
    p.write_text(t,encoding='utf-8',newline='\n')
