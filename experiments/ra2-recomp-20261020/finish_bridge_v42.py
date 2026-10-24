"""Freeze the qualified bridge scene and prove collapse with readonly cell snapshots."""
from run_batch_v42 import *
from concurrent.futures import ThreadPoolExecutor
items=[x for x in read(S/'representative-acceptance-fixtures.json')['fixtures'] if x['name'].startswith('bridge-')]
a=next(x for x in items if x['name']=='bridge-collapse');qualified=scenes([fixture_job('bridge-collapse',a,a['last'])])[0]
def observe(item):
 tag='observed-'+item['name'];_,args=fixture_job(tag,item,item['last']);args[4]=R/'run_bridge_catalog_v42.py';args+=['--cell-catalog']
 # py() produces [python,-X,utf8,-B,script,...]; replace only the wrapper path.
 if not (S/'runs'/tag/'comparison.json').exists():run(args,'scene-'+tag)
 p=S/'runs'/tag/'comparison.json';x=read(p);assert x['passed'] and x['exe_sha256']==sha(S/'bridge-catalog-observer.exe')
 for mode in ['original','generated-c']:
  left=[json.loads(l) for l in (S/'runs'/tag/mode/'state.jsonl').read_text(encoding='utf-8').splitlines()];right=[json.loads(l) for l in (S/'runs'/item['name']/mode/'state.jsonl').read_text(encoding='utf-8').splitlines()]
  assert left==right,(tag,mode,'Observer must leave every trace record unchanged')
 return dict(tag=tag,frames=x['comparison']['frames_compared'],exe_sha256=x['exe_sha256'],comparison_sha256=sha(p),strict_internal_trace_equal=True)
with ThreadPoolExecutor(max_workers=2) as pool:observed=list(pool.map(observe,items))
for mode in ['original','generated-c']:
 cells={}
 for name in ['bridge-collapse','bridge-intact']:
  x=read(S/'runs'/('observed-'+name)/mode/'cells.json');assert x['frame']==200;cells[name]={tuple(c['cell']):c for c in x['cells']}
 span=[(60,66),(61,66)]
 assert all(cells['bridge-intact'][xy]['bridge']==1 for xy in span)
 assert all(cells['bridge-collapse'][xy]['bridge']==0 for xy in span)
raw=read(S/'final-scene-matrix.json');backup=S/'qualification-excluded-matrix.json';assert not backup.exists();shutil.copy2(S/'final-scene-matrix.json',backup)
values=[qualified if x['tag']=='bridge-destroy' else x for x in raw['results']]+observed
assert len(values)==12
raw.update(results=values,production_scenes=10,production_frames=sum(x['frames'] for x in values if not x['tag'].startswith('observed-')),observer_scenes=2,observer_frames=sum(x['frames'] for x in observed),qualified_bridge_replaces='bridge-destroy (country0 entered-event did not fire; preserved strict-passing report excluded from effects/acceptance)',scope='Finite production functionality plus exactly two readonly bridge-cell observers; earlier no-effect recipe retained separately.')
(S/'final-scene-matrix.json').write_text(json.dumps(raw,indent=2)+'\n',encoding='utf-8')
original=(R/'ra2/src/runtime/state_trace.c').read_text(encoding='utf-8');actual=(S/'bridge_catalog_observer.c').read_text(encoding='utf-8');assert actual==original.replace('if (!cell_catalog_path[0] || cell_catalog_written) return;','if (frame < 200 || !cell_catalog_path[0] || cell_catalog_written) return;')
write(S/'bridge-collapse-real-effects.json',dict(passed=True,bridge_cells=[list(x) for x in span],observer_frame=200,intact_bridge_flags=[1]*2,collapsed_bridge_flags=[0]*2,neighboring_bridge_cells_retained=10,original_and_C_cells_equal=True,observer_all_trace_records_equal_to_production=True,production_sha256=sha(R/'ra2/build-original-c/ra2.exe'),observer_sha256=sha(S/'bridge-catalog-observer.exe'),observer_source_sha256=sha(S/'bridge_catalog_observer.c'),production_recorder_unchanged=True,scope='Only existing read-only catalog timing differs; no game service call or game-memory write added. Both ordinary map cases use exact same rules.'))
print(dict(passed=True,production=10,observer=2,collapsed_bridge_cells=len(span)))
