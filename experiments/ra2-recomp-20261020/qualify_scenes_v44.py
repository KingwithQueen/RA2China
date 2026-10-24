from run_batch_v44 import *
values=[]
for x in read(S/'dynamic-fixtures.json')['fixtures']:
 tag=x['baseline_tag'];_,args=fixture_job(tag,x,x['last']);p=S/'runs'/tag/'comparison.json'
 if not p.exists():run(args,'scene-'+tag,allowed_codes=(0,1))
 q=read(p);assert all(v['passed'] for v in q['runs'])
 if not q['passed']:
  assert tag=='b-dt'
  from accept_hover_v44 import accept
  assert accept(tag)['passed']
 values.append(dict(name=x['name'],tag=tag,passed=True,strict_passed=q['passed'],comparison_sha256=sha(p),frames=q['comparison']['frames_compared']))
write(S/'baseline-scene-matrix.json',dict(passed=True,results=values,scope='Pre-change linked host qualification; Hover variation recorded separately, startup failures retained.'))
