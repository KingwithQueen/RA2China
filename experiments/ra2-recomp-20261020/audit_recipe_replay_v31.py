"""Replay this batch from its protected baseline in an isolated directory."""
from pathlib import Path
import hashlib,json,shutil
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v31'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
out=S/'investigations/recipe-replay-03';assert not out.exists();out.mkdir(parents=True)
modules=['runtime/ground_overlap_bridge.c','runtime/ground_joint_bridge.c','runtime/ground_allied_bridge.c','gameplay/ground_allied.c','recomp/gen_game/recomp_0010.c','recomp/gen_game/recomp_0046.c']
for rel in modules:
    dest=out/'ra2/src'/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(S/'baseline/ra2/src'/rel,dest)
target=out/'evidence/movement-state-v31';(target/'pending').mkdir(parents=True)
for name in ['overlap_probe.c','allied_probe.c']:
    shutil.copy2(S/'baseline/evidence/movement-state-v30'/name,target/name)
dest=target/'baseline/evidence/movement-state-v30/connection_observer.c';dest.parent.mkdir(parents=True)
shutil.copy2(S/'baseline/evidence/movement-state-v30/connection_observer.c',dest)
recipes=['integrate_template_v31.py','extend_probes_v31.py','integrate_objects_v31.py','extend_allied_probe_v31.py','integrate_returns_v31.py','extend_observer_v31.py']
for name in recipes:
    exec(compile((R/name).read_text(encoding='utf-8'),str(R/name),'exec'),dict(__file__=str(out/name)))
modules+=['gameplay/ground_moving_tail.h'];compared=[]
for rel in modules:
    p=R/'ra2/src'/rel;assert p.read_bytes()==(out/'ra2/src'/rel).read_bytes(),rel;compared.append(p)
for name in ['overlap_probe.c','allied_probe.c','connection_observer.c']:
    p=S/name;assert p.read_bytes()==(target/name).read_bytes(),name;compared.append(p)
for name in ['bridge-chain-north.MAP','bridge-chain-south.MAP']:
    p=target/'fixtures'/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(S/'fixtures'/name,p)
dest=out/'evidence/movement-state-v4/SOV01T-original.MAP';dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/'evidence/movement-state-v4/SOV01T-original.MAP',dest)
for name in ['make_bridge_mixed_v31.py','make_bridge_hostile_v31.py','extend_bridge_hostile_ai_v31.py']:
    recipes.append(name);exec(compile((R/name).read_text(encoding='utf-8'),str(R/name),'exec'),dict(__file__=str(out/name)))
maps=[p for p in (target/'fixtures').glob('bridge-*.MAP') if 'chain-' not in p.name]
assert len(maps)==10
for p in maps:
    actual=S/'fixtures'/p.name;assert p.read_bytes()==actual.read_bytes();compared.append(actual)
value=dict(passed=True,production_sources_replayed=7,probe_sources_replayed=2,observer_sources_replayed=1,accepted_bridge_maps_replayed=8,rejected_order_control_maps_replayed=2,byte_identical=True,
    inputs=[dict(path=p.relative_to(R).as_posix(),sha256=sha(p)) for p in [Path(__file__),R/'evidence/movement-state-v4/SOV01T-original.MAP']+[R/n for n in recipes]+compared])
(S/'recipe-byte-audit.json').write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in value.items() if k!='inputs'}))
