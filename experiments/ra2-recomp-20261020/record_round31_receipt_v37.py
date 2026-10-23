"""Bind new native fragments to production, probes and exact reconstruction recipes."""
from pathlib import Path
import hashlib,json,subprocess
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v37'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
results={}
for exe,args,name in [('overlap_probe.exe',['10'],'sample-anchor-probe'),('allied_probe.exe',['tail'],'moving-tail-probe'),('overlap_probe.exe',['11'],'advance-service-probe')]:
    p=subprocess.run([str(S/exe),str(R/'ra2/game/game.exe'),*args],cwd=R,check=True,capture_output=True,text=True)
    value=json.loads(p.stdout);assert value['passed'] and value.get('cases',value.get('moving_tail_cases'))==65536
    if name=='advance-service-probe':assert value['primary_fallthrough_cases']==16384 and value['secondary_service_cases']==49152 and value['alive_continuations']==12288
    (S/(name+'-verified-01.json')).write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8');results[name]=value
paths=[Path(__file__)]+[R/n for n in ['integrate_template_v37.py','integrate_objects_v37.py','integrate_returns_v37.py','extend_probes_v37.py','extend_allied_probe_v37.py','build-overlap-probe-v37.ps1','build-allied-probe-v37.ps1']]
paths += [S/n for n in ['overlap_probe.c','allied_probe.c','native_probe_host.h','remaining_return_cases.h']]
paths += [R/'ra2/src'/n for n in ['runtime/ground_overlap_bridge.c','runtime/ground_joint_bridge.c','runtime/ground_allied_bridge.c','gameplay/ground_allied.c','gameplay/ground_moving_tail.h','gameplay/ground_allied_relation.h','recomp/gen_game/recomp_0010.c','recomp/gen_game/recomp_0046.c']]
value=dict(passed=True,total_cases=196608,results=results,anchor_aliasing_order_verified=True,callback_updated_passage_verified=True,
    callback_updated_owner_and_saved_registers_verified=True,original_sha256=sha(R/'ra2/game/game.exe'),
    probe_executables=[dict(path=(S/n).relative_to(R).as_posix(),sha256=sha(S/n)) for n in ['overlap_probe.exe','allied_probe.exe']],
    inputs=[dict(path=p.relative_to(R).as_posix(),sha256=sha(p)) for p in paths])
(S/'native-round31-identity.json').write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(passed=True,new_cases=196608)))
