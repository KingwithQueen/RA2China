"""Replace the unqualified rough trial with its independently baseline-checked recipe."""
from run_batch_v49 import *
item=read(S/'dynamic-fixtures.json')['fixtures'][0];assert item['tag']=='r2'
values=[]
for tag in ['b-r2','r2']:
 p=S/'runs'/tag/'comparison.json';q=read(p);assert q['passed'] and q['comparison']['rng_equal_all_frames']
 expected=S/'baseline-observer/bridge-catalog-observer.exe' if tag=='b-r2' else S/'bridge-catalog-observer.exe'
 assert q['exe_sha256']==sha(expected)
 values.append(dict(tag=tag,frames=q['comparison']['frames_compared'],exe_sha256=q['exe_sha256'],comparison_sha256=sha(p),capture_host=True,strict_trace_equal=True))
p=S/'final-scene-matrix.json';matrix=read(p);write(S/'initial-scene-matrix.json',matrix)
assert sum(x['tag']=='ru' for x in matrix['results'])==1
matrix['results']=[values[1] if x['tag']=='ru' else x for x in matrix['results']]
matrix.update(scope='Qualified actual rough landing, bridge upper/lower collapse with adjacent loaded carrier, slope1 and finite affected regression. Mixed-terrain ru excluded.',excluded_strict_but_unqualified_trials=['ru'])
p.write_text(json.dumps(matrix,indent=2)+'\n',encoding='utf-8')
