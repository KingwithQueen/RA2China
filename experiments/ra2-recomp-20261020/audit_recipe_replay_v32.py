"""Reconstruct all changed production and test sources from the protected baseline."""
from pathlib import Path
import hashlib,json,shutil
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v32';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
out=S/'investigations/recipe-replay-02';assert not out.exists();out.mkdir(parents=True)
modules=['runtime/ground_joint_bridge.c','runtime/ground_allied_bridge.c','gameplay/ground_allied.c','recomp/gen_game/recomp_0010.c','recomp/gen_game/recomp_0046.c']
for rel in modules:
    p=out/'ra2/src'/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(S/'baseline/ra2/src'/rel,p)
target=out/'evidence/movement-state-v32';(target/'pending').mkdir(parents=True)
for n in ['overlap_probe.c','allied_probe.c']:shutil.copy2(S/'baseline/evidence/movement-state-v31'/n,target/n)
p=target/'baseline/evidence/movement-state-v31/connection_observer.c';p.parent.mkdir(parents=True);shutil.copy2(S/'baseline/evidence/movement-state-v31/connection_observer.c',p)
recipes=['integrate_template_v32.py','extend_probes_v32.py','integrate_objects_v32.py','extend_allied_probe_v32.py','integrate_returns_v32.py','extend_exit_probe_v32.py','extend_observer_v32.py']
for n in recipes:exec(compile((R/n).read_text(encoding='utf-8'),str(R/n),'exec'),dict(__file__=str(out/n)))
modules+=['gameplay/ground_allied_relation.h'];compared=[]
for rel in modules:
    p=R/'ra2/src'/rel;assert p.read_bytes()==(out/'ra2/src'/rel).read_bytes(),rel;compared.append(p)
for n in ['overlap_probe.c','allied_probe.c','connection_observer.c']:
    p=S/n;assert p.read_bytes()==(target/n).read_bytes(),n;compared.append(p)
(target/'fixtures').mkdir()
for n in ['bridge-mixed-north.MAP','bridge-mixed-south.MAP']:shutil.copy2(S/'fixtures'/n,target/'fixtures'/n)
n='make_bridge_infantry_v32.py';recipes.append(n);exec(compile((R/n).read_text(encoding='utf-8'),str(R/n),'exec'),dict(__file__=str(out/n)))
for p in (target/'fixtures').glob('bridge-infantry-*.MAP'):
    actual=S/'fixtures'/p.name;assert p.read_bytes()==actual.read_bytes();compared.append(actual)
value=dict(passed=True,production_sources_replayed=6,probe_sources_replayed=2,observer_sources_replayed=1,accepted_bridge_maps_replayed=4,byte_identical=True,
    inputs=[dict(path=p.relative_to(R).as_posix(),sha256=sha(p)) for p in [Path(__file__)]+[R/n for n in recipes]+compared])
(S/'recipe-byte-audit.json').write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8');print({k:v for k,v in value.items() if k!='inputs'})
