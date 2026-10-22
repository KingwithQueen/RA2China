from pathlib import Path
import shutil
ROOT=Path(__file__).resolve().parent
OLD=ROOT/'evidence/movement-state-v5'
NEW=ROOT/'evidence/movement-state-v6'
names=['movement_probe','original_movement_probe','path_fragment_probe','drive_process_probe','collision_probe',
    'arrival_probe','prepare_probe','recovery_probe','barrier_probe','obstacle_probe','segment_probe','speed_ramp_probe',
    'wait_probe','terrain_probe','reaction_probe']
for name in names:
    shutil.copy2(OLD/(name+'.c'),NEW/(name+'.c'))
shutil.copy2(OLD/'audit_noop.c',NEW/'audit_noop.c')
for name in ('movement-probe','state-probes','prepare-probes','obstacle-probe','segment-probe','speed-ramp-probe',
             'wait-probe','terrain-probe','reaction-probe'):
    text=(ROOT/('build-'+name+'-v5.ps1')).read_text(encoding='utf-8').replace('movement-state-v5','movement-state-v6')
    lines=text.splitlines()
    for i,line in enumerate(lines):
        if '& cl ' in line and 'ground_prepare_bridge.c' in line:
            line=line.replace(' /Fe:',' ..\\..\\ra2\\src\\gameplay\\ground_special.c ..\\..\\ra2\\src\\gameplay\\ground_template.c /Fe:')
        lines[i]=line
    (ROOT/('build-'+name+'-v6.ps1')).write_text('\n'.join(lines)+'\n',encoding='utf-8',newline='\n')
path=ROOT/'build-special-probe-v6.ps1'
text=path.read_text(encoding='utf-8')
if 'ground_template.c' not in text:
    text=text.replace(' /Fe:',' ..\\..\\ra2\\src\\gameplay\\ground_template.c /Fe:')
path.write_text(text,encoding='utf-8',newline='\n')
