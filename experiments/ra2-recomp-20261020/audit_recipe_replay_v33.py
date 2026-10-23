"""Rebuild this batch from its baseline and compare exact source and candidate-map bytes."""
from pathlib import Path
import hashlib,json,shutil
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v33';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
out=S/'investigations/recipe-replay-01';assert not out.exists();out.mkdir(parents=True)
modules=['runtime/ground_joint_bridge.c','runtime/ground_objects_bridge.c','gameplay/ground_objects.c','recomp/gen_game/recomp_0010.c','recomp/gen_game/recomp_0046.c']
for rel in modules:
    p=out/'ra2/src'/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(S/'baseline/ra2/src'/rel,p)
target=out/'evidence/movement-state-v33';(target/'pending').mkdir(parents=True)
for n in ['overlap_probe.c','objects_probe.c']:shutil.copy2(S/'baseline/evidence/movement-state-v32'/n,target/n)
p=target/'baseline/evidence/movement-state-v32/connection_observer.c';p.parent.mkdir(parents=True);shutil.copy2(S/'baseline/evidence/movement-state-v32/connection_observer.c',p)
recipes=['integrate_template_v33.py','integrate_objects_v33.py','extend_objects_probe_v33.py','integrate_returns_v33.py','extend_exit_probe_v33.py','extend_observer_v33.py']
for n in recipes:exec(compile((R/n).read_text(encoding='utf-8'),str(R/n),'exec'),dict(__file__=str(out/n)))
modules+=['gameplay/ground_enemy_contact.h'];compared=[]
for rel in modules:
    p=R/'ra2/src'/rel;assert p.read_bytes()==(out/'ra2/src'/rel).read_bytes(),rel;compared.append(p)
for n in ['overlap_probe.c','objects_probe.c','connection_observer.c']:
    p=S/n;assert p.read_bytes()==(target/n).read_bytes(),n;compared.append(p)
(target/'fixtures').mkdir()
for direction in ['north','south']:shutil.copy2(S/f'fixtures/bridge-infantry-meeting-{direction}.MAP',target/f'fixtures/bridge-infantry-meeting-{direction}.MAP')
n='make_bridge_north_query_v33.py';recipes.append(n);exec(compile((R/n).read_text(encoding='utf-8'),str(R/n),'exec'),dict(__file__=str(out/n)))
maps=list((target/'fixtures').glob('bridge-north-lane-*.MAP'));assert len(maps)==3
for p in maps:
    actual=S/'fixtures'/p.name;assert p.read_bytes()==actual.read_bytes();compared.append(actual)
value=dict(passed=True,production_sources_replayed=6,probe_sources_replayed=2,observer_sources_replayed=1,candidate_maps_replayed=3,byte_identical=True,
    inputs=[dict(path=p.relative_to(R).as_posix(),sha256=sha(p)) for p in [Path(__file__)]+[R/n for n in recipes]+compared])
(S/'recipe-byte-audit.json').write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8');print({k:v for k,v in value.items() if k!='inputs'})
