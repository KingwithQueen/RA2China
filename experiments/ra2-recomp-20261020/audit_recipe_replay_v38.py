"""Reconstruct this round from generation36 rather than replaying old integrations."""
from pathlib import Path
import hashlib,json,shutil
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v38';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();out=S/'investigations/recipe-replay-01';assert not out.exists();out.mkdir(parents=True)
modules=['runtime/ground_tube_state_bridge.c','runtime/ground_joint_bridge.c','runtime/ground_objects_bridge.c','gameplay/ground_objects.c','gameplay/ground_enemy_kind.h','recomp/gen_game/recomp_0010.c','recomp/gen_game/recomp_0046.c']
for rel in modules:
    d=out/'ra2/src'/rel;d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(S/'baseline/ra2/src'/rel,d)
target=out/'evidence/movement-state-v38';(target/'pending').mkdir(parents=True)
for n in ['tube_state_probe.c','objects_probe.c','overlap_probe.c']:shutil.copy2(S/'baseline/evidence/movement-state-v37'/n,target/n)
p=target/'baseline/evidence/movement-state-v37/connection_observer.c';p.parent.mkdir(parents=True);shutil.copy2(S/'baseline/evidence/movement-state-v37/connection_observer.c',p)
recipes=['integrate_template_v38.py','extend_register_probe_v38.py','integrate_objects_v38.py','extend_objects_probe_v38.py','integrate_returns_v38.py','extend_exit_probe_v38.py','extend_observer_v38.py'];compared=[]
for n in recipes:exec(compile((R/n).read_text(encoding='utf-8'),str(R/n),'exec'),dict(__file__=str(out/n)))
for rel in modules:
    p=R/'ra2/src'/rel;assert p.read_bytes()==(out/'ra2/src'/rel).read_bytes(),rel;compared.append(p)
for n in ['tube_state_probe.c','objects_probe.c','overlap_probe.c','connection_observer.c']:
    p=S/n;assert p.read_bytes()==(target/n).read_bytes(),n;compared.append(p)
(target/'fixtures').mkdir()
for direction in ['north','south']:shutil.copy2(S/'fixtures'/('bridge-detour-'+direction+'.MAP'),target/'fixtures'/('bridge-detour-'+direction+'.MAP'))
shutil.copy2(S/'bridge-detour-fixtures.json',target/'bridge-detour-fixtures.json')
n='make_bridge_neighbor_release_v38.py';recipes.append(n);exec(compile((R/n).read_text(encoding='utf-8'),str(R/n),'exec'),dict(__file__=str(out/n)))
for p in (target/'fixtures').glob('bridge-neighbor-release-*.MAP'):
    actual=S/'fixtures'/p.name;assert p.read_bytes()==actual.read_bytes();compared.append(actual)
v=dict(passed=True,production_sources_replayed=7,production_sources_changed=4,probe_sources_replayed=3,probe_sources_changed=2,observer_sources_replayed=1,candidate_maps_replayed=2,byte_identical=True,inputs=[dict(path=p.relative_to(R).as_posix(),sha256=sha(p)) for p in [Path(__file__)]+[R/n for n in recipes]+compared])
(S/'recipe-byte-audit.json').write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8');print({k:v for k,v in v.items() if k!='inputs'})
