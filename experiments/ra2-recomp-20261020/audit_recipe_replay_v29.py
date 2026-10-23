"""Replay new integrations and probes in isolation from protected sources."""
from pathlib import Path
import hashlib,json,shutil
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v29'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
out=S/'investigations/recipe-replay-04';assert not out.exists();out.mkdir(parents=True)
modules=['gameplay/ground_template.c','gameplay/ground_objects.c','runtime/ground_objects_bridge.c',
 'runtime/ground_overlap_bridge.c','runtime/ground_joint_bridge.c','recomp/gen_game/recomp_0010.c','recomp/gen_game/recomp_0046.c']
for rel in modules:
 destination=out/'ra2/src'/rel;destination.parent.mkdir(parents=True,exist_ok=True)
 shutil.copy2(S/'baseline/ra2/src'/rel,destination)
(out/'evidence/movement-state-v29/pending').mkdir(parents=True)
recipes=['integrate_template_v29.py','integrate_objects_v29.py','integrate_returns_v29.py']
for name in recipes:
 code=(R/name).read_text(encoding='utf-8')
 exec(compile(code,str(R/name),'exec'),dict(__file__=str(out/name)))
modules+=['gameplay/ground_template_table.h','gameplay/ground_building_flags.h']
compared=[]
for rel in modules:
 p=R/'ra2/src'/rel;assert p.read_bytes()==(out/'ra2/src'/rel).read_bytes(),rel;compared.append(p)
def run_recipe(name,destination,cut=None):
 destination.mkdir(parents=True,exist_ok=True)
 code=(R/name).read_text(encoding='utf-8')
 if cut:code=code[:code.index(cut)]
 code=code.replace("S=R/'evidence/movement-state-v29'",'S=Path('+repr(str(destination))+')',1)
 exec(compile(code,str(R/name),'exec'),dict(__file__=str(R/name)))
 recipes.append(name)
run_recipe('extend_probes_v29.py',out/'probes')
for name in ['overlap_probe.c','objects_probe.c']:
 assert (S/name).read_bytes()==(out/'probes'/name).read_bytes(),name;compared.append(S/name)
run_recipe('extend_observer_v29_chain.py',out/'observer',"p=R/'make_connection_fixture_v29.py'")
assert (S/'connection_observer.c').read_bytes()==(out/'observer/connection_observer.c').read_bytes()
compared.append(S/'connection_observer.c')
maps=out/'maps';(maps/'fixtures').mkdir(parents=True)
shutil.copy2(S/'fixtures/dynamic-far-base.MAP',maps/'fixtures/dynamic-far-base.MAP')
run_recipe('make_bridge_scenes_v29.py',maps)
for p in (maps/'fixtures').glob('bridge-chain-*.MAP'):
 assert p.read_bytes()==(S/'fixtures'/p.name).read_bytes(),p.name;compared.append(S/'fixtures'/p.name)
inputs=[R/name for name in recipes]+compared+[Path(__file__)]
value=dict(passed=True,production_sources_replayed=len(modules),probe_sources_replayed=2,
 observer_sources_replayed=1,bridge_maps_replayed=4,byte_identical=True,
 scope='Replay starts from protected generation-27 sources; archived writers never run in place.',
 inputs=[dict(path=p.relative_to(R).as_posix(),sha256=sha(p)) for p in inputs])
(S/'recipe-byte-audit.json').write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in value.items() if k!='inputs'}))
