"""Qualify ordinary collision scenes on the accepted executable before changing production."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json,subprocess,sys,os
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v41'
def one(item):
 tag='baseline02-'+item['name'];args=[sys.executable,'-X','utf8','-B',str(R/'run_fixture_comparison.py'),'--tag',tag,'--evidence-stage',S.name,'--movement-audit','--seconds','240','--range','0:500','--scenario-map',str(R/item['path']),'--scenario-rules',str(R/item['rules'])]
 for order in item['orders']:args+=['--order',order]
 with (S/(tag+'.log')).open('x',encoding='utf-8') as f:q=subprocess.run(args,cwd=R,stdout=f,stderr=subprocess.STDOUT,env=dict(os.environ,PYTHONIOENCODING='utf-8'))
 print(dict(tag=tag,exit_code=q.returncode),flush=True)
 if q.returncode:raise RuntimeError(tag)
 return tag
items=json.loads((S/'collision-fixtures-02.json').read_text(encoding='utf-8'))['fixtures']
with ThreadPoolExecutor(max_workers=2) as pool:tags=list(pool.map(one,items))
(S/'baseline-collision-runs-02.json').write_text(json.dumps(dict(passed=True,tags=tags),indent=2)+'\n',encoding='utf-8')
