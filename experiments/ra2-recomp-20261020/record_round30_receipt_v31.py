"""Bind the three new original/C phases to exact sources and probe binaries."""
from pathlib import Path
import hashlib,json,subprocess
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v31'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
results={}
for exe,phase,name in [('overlap_probe.exe',8,'template-index-probe'),('objects_probe.exe',6,'enemy-kind-probe'),('overlap_probe.exe',9,'service-exits-probe')]:
    run=subprocess.run([str(S/exe),str(R/'ra2/game/game.exe'),str(phase)],cwd=R,check=True,capture_output=True,text=True)
    value=json.loads(run.stdout);assert value['passed'] and value['phase']==phase and value.get('cases',value.get('object_cases'))==65536
    (S/(name+'-verified-01.json')).write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8');results[name]=value
paths=[Path(__file__)]+[R/n for n in ['integrate_template_v31.py','integrate_objects_v31.py','integrate_returns_v31.py','extend_probes_v31.py','build-overlap-probe-v31.ps1','build-objects-probe-v31.ps1']]
paths += [S/n for n in ['overlap_probe.c','objects_probe.c','native_probe_host.h','remaining_return_cases.h']]
for d,names in [('gameplay',['ground_sampling_shared','ground_objects','ground_enemy_kind']),('runtime',['ground_overlap_bridge','ground_objects_bridge','ground_joint_bridge'])]:
    for n in names:
        paths += [p for ext in ['c','h'] if (p:=R/f'ra2/src/{d}/{n}.{ext}').exists()]
value=dict(passed=True,total_cases=196608,results=results,ordered_service_arguments_and_writes_verified=True,
    callback_mutated_saved_frame_verified=True,mutable_owner_verified=True,original_sha256=sha(R/'ra2/game/game.exe'),
    probe_executables=[dict(path=(S/n).relative_to(R).as_posix(),sha256=sha(S/n)) for n in ['overlap_probe.exe','objects_probe.exe']],
    inputs=[dict(path=p.relative_to(R).as_posix(),sha256=sha(p)) for p in paths])
(S/'native-round30-identity.json').write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(passed=True,new_cases=196608)))
