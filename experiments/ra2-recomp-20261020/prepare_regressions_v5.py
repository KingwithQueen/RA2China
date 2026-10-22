from pathlib import Path
import shutil
ROOT = Path(__file__).resolve().parent
OLD = ROOT/'evidence/movement-state-v4'
NEW = ROOT/'evidence/movement-state-v5'
names = ['movement_probe','original_movement_probe','path_fragment_probe','drive_process_probe',
         'collision_probe','arrival_probe','prepare_probe','recovery_probe','barrier_probe','obstacle_probe','segment_probe','speed_ramp_probe']
for name in names:
    shutil.copy2(OLD/(name+'.c'), NEW/(name+'.c'))
(NEW/'audit_noop.c').write_text('#include <stdint.h>\nvoid ra2_state_movement_audit(uint32_t a, uint32_t b, uint32_t c, uint32_t d)\n{ (void)a; (void)b; (void)c; (void)d; }\n', encoding='utf-8')
for old, new in [('build-movement-probe-v4','build-movement-probe-v5'),
        ('build-state-probes-v4','build-state-probes-v5'),('build-prepare-probes-v4','build-prepare-probes-v5'),
        ('build-obstacle-probe','build-obstacle-probe-v5'),('build-segment-probe','build-segment-probe-v5'),
        ('build-speed-ramp-probe','build-speed-ramp-probe-v5')]:
    text = (ROOT/(old+'.ps1')).read_text(encoding='utf-8').replace('movement-state-v4','movement-state-v5')
    lines = text.splitlines()
    for i,line in enumerate(lines):
        if '& cl ' not in line:
            continue
        segment = '..\\..\\ra2\\src\\gameplay\\ground_segment.c '
        if segment+segment in line:
            line = line.replace(segment+segment, segment)
        if 'ground_prepare_bridge.c' in line:
            line = line.replace(' /Fe:', ' ..\\..\\ra2\\src\\gameplay\\ground_wait.c ..\\..\\ra2\\src\\gameplay\\ground_reaction.c /Fe:')
        if 'ground_collision_bridge.c' in line:
            line = line.replace(' /Fe:', ' ..\\..\\ra2\\src\\gameplay\\ground_terrain.c audit_noop.c /Fe:')
        lines[i] = line
    (ROOT/(new+'.ps1')).write_text('\n'.join(lines)+'\n',encoding='utf-8',newline='\n')
path = ROOT/'build-wait-probe-v5.ps1'
text = path.read_text(encoding='utf-8')
if 'ground_reaction.c' not in text:
    text = text.replace(' /Fe:', ' ..\\..\\ra2\\src\\gameplay\\ground_reaction.c /Fe:')
path.write_text(text,encoding='utf-8',newline='\n')
path = ROOT/'build-terrain-probe-v5.ps1'
text = path.read_text(encoding='utf-8')
if 'audit_noop.c' not in text:
    text = text.replace(' /Fe:', ' audit_noop.c /Fe:')
path.write_text(text,encoding='utf-8',newline='\n')
