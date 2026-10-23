from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json,subprocess,sys,os
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v30'
source=(R/'run_scenes_v30.py').read_text(encoding='utf-8');scope={'__file__':str(R/'run_scenes_v30.py'),'__name__':'case_definitions'}
exec(compile(source[:source.index('prefix=sys.argv')],str(R/'run_scenes_v30.py'),'exec'),scope)
cases=[('j-default','run_skirmish_v30.py',['--range','0:900','--host-exe',str(S/'connection-fixture-probe.exe')])]
for name,fixture,span,args in scope['cases']:
 if name not in ['long','tc1','repeat-failure']:continue
 cases.append(('j-'+('fail' if name=='repeat-failure' else name),'run_connection_v30.py',['--evidence-stage','movement-state-v30','--movement-audit','--seconds','240','--range',span,'--scenario-map',str(S/'fixtures'/fixture)]+args))
assert len(cases)==4
def run(case):
 tag,script,args=case
 with (S/(tag+'.log')).open('x',encoding='utf-8') as out:p=subprocess.run([sys.executable,'-B',str(R/script),'--tag',tag]+args,cwd=R,stdout=out,stderr=subprocess.STDOUT,env=dict(os.environ,PYTHONIOENCODING='utf-8'))
 path=S/'runs'/tag/'comparison.json';x=json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}
 result=dict(tag=tag,passed=p.returncode==0 and x.get('passed',False),frames=x.get('comparison',{}).get('frames_compared',0));print(json.dumps(result),flush=True);return result
with ThreadPoolExecutor(max_workers=1) as pool:results=list(pool.map(run,cases))
assert all(r['passed'] for r in results),results
