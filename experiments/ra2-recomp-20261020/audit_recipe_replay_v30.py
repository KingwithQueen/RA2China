"""Rebuild new production changes and scene inputs in an isolated directory."""
from pathlib import Path
import hashlib,json,shutil
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v30'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
out=S/'investigations/recipe-replay-01';assert not out.exists();out.mkdir(parents=True)
modules=['gameplay/ground_sampling_shared.c','gameplay/ground_sampling_shared.h','runtime/ground_overlap_bridge.c',
 'gameplay/ground_objects.c','runtime/ground_objects_bridge.c','runtime/ground_joint_bridge.c','recomp/gen_game/recomp_0010.c','recomp/gen_game/recomp_0046.c']
for rel in modules:
    dest=out/'ra2/src'/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(S/'baseline/ra2/src'/rel,dest)
(out/'evidence/movement-state-v30/pending').mkdir(parents=True)
for name in ['objects_probe.c','overlap_probe.c','connection_observer.c']:
    p=out/'evidence/movement-state-v29'/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/'evidence/movement-state-v29'/name,p)
shutil.copy2(out/'evidence/movement-state-v29/objects_probe.c',out/'evidence/movement-state-v30/objects_probe.c')
t=(S/'baseline/build-overlap-probe-v29.ps1').read_text(encoding='utf-8').replace('v29','v30')
(out/'build-overlap-probe-v30.ps1').write_text(t,encoding='utf-8',newline='\n')
recipes=['integrate_template_v30.py','extend_probes_v30.py','integrate_objects_v30.py','integrate_returns_v30.py','extend_exit_probe_v30.py','extend_observer_v30.py']
for name in recipes:
    exec(compile((R/name).read_text(encoding='utf-8'),str(R/name),'exec'),dict(__file__=str(out/name)))
modules+=['gameplay/ground_enemy_kind.h'];compared=[]
for rel in modules:
    p=R/'ra2/src'/rel;assert p.read_bytes()==(out/'ra2/src'/rel).read_bytes(),rel;compared.append(p)
for name in ['objects_probe.c','overlap_probe.c','connection_observer.c']:
    p=S/name;assert p.read_bytes()==(out/'evidence/movement-state-v30'/name).read_bytes(),name;compared.append(p)
assert (R/'build-overlap-probe-v30.ps1').read_bytes()==(out/'build-overlap-probe-v30.ps1').read_bytes()
for name in ['bridge-chain-north.MAP','bridge-chain-south.MAP']:
    p=out/'evidence/movement-state-v30/fixtures'/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(S/'fixtures'/name,p)
name='make_bridge_mixed_v30.py';recipes.append(name)
exec(compile((R/name).read_text(encoding='utf-8'),str(R/name),'exec'),dict(__file__=str(out/name)))
for p in (out/'evidence/movement-state-v30/fixtures').glob('bridge-*.MAP'):
    actual=S/'fixtures'/p.name;assert p.read_bytes()==actual.read_bytes();compared.append(actual)
value=dict(passed=True,production_sources_replayed=9,probe_sources_replayed=2,observer_sources_replayed=1,mixed_maps_replayed=4,byte_identical=True,
    inputs=[dict(path=p.relative_to(R).as_posix(),sha256=sha(p)) for p in [Path(__file__)]+[R/n for n in recipes]+compared])
(S/'recipe-byte-audit.json').write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in value.items() if k!='inputs'}))
