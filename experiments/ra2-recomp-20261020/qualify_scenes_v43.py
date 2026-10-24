from run_batch_v43 import *
from concurrent.futures import ThreadPoolExecutor
def one(x):
 tag='baseline-'+x['name'];_,args=fixture_job(tag,x,x['last'])
 if x['capture_host']:args[4]=R/'run_bridge_catalog_v43.py';args+=['--cell-catalog']
 run(args,'scene-'+tag);p=S/'runs'/tag/'comparison.json';q=read(p);assert q['passed']
 return dict(tag=tag,comparison_sha256=sha(p),frames=q['comparison']['frames_compared'])
with ThreadPoolExecutor(max_workers=2) as pool:values=list(pool.map(one,read(S/'new-scene-fixtures.json')['fixtures']))
write(S/'baseline-scene-matrix.json',dict(passed=True,results=values))
