"""Preflight every actor start and ordinary command goal using the native cell catalog."""
from run_batch_v66 import *
results=[]
for r in read(S/'traffic-fixtures.json')['fixtures']:
 tag='id-cq3' if r['kind']=='queue' else 'id-cm5';catalog=S/'runs'/tag/'original/cells.json';cells={tuple(c['cell']):c for c in read(catalog)['cells']};checked=[]
 for stage,points in [('start',r['starts']),('ordinary-move-goal',[e['cell'] for e in r['events']])]:
  for p in points:
   c=cells[tuple(p)];assert c['land'] in [0,1,6,7] and c['level']==4,(r['tag'],stage,p,c)
   checked.append(dict(stage=stage,cell=p,land=c['land'],level=c['level'],overlay=c['overlay'],bridge=c['bridge']))
 results.append(dict(tag=r['tag'],map_sha256=sha(R/r['path']),catalog=str(catalog),catalog_sha256=sha(catalog),checked=checked))
write(S/'traffic-goal-terrain-validation.json',dict(passed=True,scenes=results,scope='Start and ordinary intermediate/final targets have legal ground land classes and the intended native level. Dynamic occupancy and complete route acceptance still require the natural game gates.'))
print(dict(passed=True,scenes=len(results),all_starts_and_move_goals_checked=True))
