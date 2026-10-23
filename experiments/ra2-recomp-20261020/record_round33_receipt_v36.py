"""Bind new native fragments to production, probes and exact reconstruction recipes."""
from pathlib import Path
import hashlib,json,subprocess
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v36'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
results={}
for exe,args,name in [('overlap_probe.exe',['12'],'destination-copy-probe'),('objects_probe.exe',['7'],'enemy-contact-probe'),('overlap_probe.exe',['14'],'following-service-probe')]:
    p=subprocess.run([str(S/exe),str(R/'ra2/game/game.exe'),*args],cwd=R,check=True,capture_output=True,text=True)
    value=json.loads(p.stdout);assert value['passed'] and value.get('cases',value.get('object_cases'))==65536
    if name=='enemy-contact-probe':assert all(value['outcomes'][i]>0 for i in [2,6])
    if name=='following-service-probe':assert value['ordered_callback_values']==425984
    (S/(name+'-verified-01.json')).write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8');results[name]=value
paths=[Path(__file__)]+[R/n for n in ['integrate_template_v36.py','integrate_objects_v36.py','integrate_returns_v36.py','audit_destination_copies_v36.py','extend_objects_probe_v36.py','extend_exit_probe_v36.py','build-overlap-probe-v36.ps1','build-objects-probe-v36.ps1']]
paths += [S/n for n in ['overlap_probe.c','objects_probe.c','native_probe_host.h','remaining_return_cases.h']]
paths += [R/'ra2/src'/n for n in ['runtime/ground_overlap_bridge.c','runtime/ground_joint_bridge.c','runtime/ground_allied_bridge.c','gameplay/ground_allied.c','gameplay/ground_moving_tail.h','gameplay/ground_allied_relation.h','gameplay/ground_enemy_contact.h','gameplay/ground_objects.c','runtime/ground_objects_bridge.c','recomp/gen_game/recomp_0010.c','recomp/gen_game/recomp_0046.c']]
value=dict(passed=True,total_cases=196608,results=results,destination_copy_continuation_contract_verified=True,mutable_contact_relationship_verified=True,
    callback_updated_owner_and_saved_registers_verified=True,original_sha256=sha(R/'ra2/game/game.exe'),
    probe_executables=[dict(path=(S/n).relative_to(R).as_posix(),sha256=sha(S/n)) for n in ['overlap_probe.exe','objects_probe.exe']],
    inputs=[dict(path=p.relative_to(R).as_posix(),sha256=sha(p)) for p in paths])
(S/'native-round33-identity.json').write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(passed=True,new_cases=196608)))
