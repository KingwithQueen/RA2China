"""Bind the three newly exercised native entries to the exact current implementation."""
from pathlib import Path
import hashlib,json,subprocess
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v37';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();results={}
for exe,phase,name in [('tube_state_probe',4,'register-sample'),('objects_probe',8,'enemy-weapon'),('overlap_probe',15,'owner-stop')]:
    v=json.loads(subprocess.check_output([str(S/(exe+'.exe')),str(R/'ra2/game/game.exe'),str(phase)],cwd=R,text=True));assert v['passed'] and v.get('cases',v.get('object_cases'))==65536
    if phase==8:assert v['outcomes'][2]>0 and v['outcomes'][6]>0
    (S/(name+'-probe-verified-01.json')).write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8');results[name]=v
sources=[Path(__file__)]+[R/(n+'_v37.py') for n in ['integrate_template','integrate_objects','integrate_returns','extend_register_probe','extend_objects_probe','extend_exit_probe','audit_recipe_replay']]
sources += [S/n for n in ['tube_state_probe.c','objects_probe.c','overlap_probe.c','native_probe_host.h']]
sources += [R/'ra2/src'/n for n in ['runtime/ground_tube_state_bridge.c','runtime/ground_joint_bridge.c','runtime/ground_objects_bridge.c','gameplay/ground_objects.c','gameplay/ground_enemy_contact.h','recomp/gen_game/recomp_0010.c','recomp/gen_game/recomp_0046.c']]
value=dict(passed=True,total_cases=196608,results=results,register_index_differs_from_cache=True,weapon_callback_mutates_train_property=True,incoming_stop_owner_differs_from_drive_owner=True,original_sha256=sha(R/'ra2/game/game.exe'),inputs=[dict(path=p.relative_to(R).as_posix(),sha256=sha(p)) for p in sources],probe_executables=[dict(path=(S/n).relative_to(R).as_posix(),sha256=sha(S/n)) for n in ['tube_state_probe.exe','objects_probe.exe','overlap_probe.exe']])
(S/'native-round34-identity.json').write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8');print(dict(passed=True,new_cases=196608))
