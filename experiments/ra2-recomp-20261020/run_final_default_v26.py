"""Refresh the independent budget host after the final content build; retain prior checkpoints."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import subprocess,sys,json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v26'
for script in ['make_truck_fixture_v26.py','make_truck_actor_fixture_v26.py']:
 subprocess.run([sys.executable,'-B',str(R/script)],cwd=R,check=True)
with (S/'final-budget-helper-build.log').open('x',encoding='utf-8') as out:
 subprocess.run(['pwsh','-NoProfile','-File',str(R/'build-truck-actor-fixture-v26.ps1')],cwd=R,stdout=out,stderr=subprocess.STDOUT,check=True)
cases=[('d-final-default',[]),('v-default-budget-final',['--host-exe',str(S/'truck-actor-fixture-probe.exe'),'--unit-ring','27:1032259:2'])]
def run(case):
 tag,args=case
 with (S/(tag+'.log')).open('x',encoding='utf-8') as out:
  p=subprocess.run([sys.executable,'-B',str(R/'run_skirmish_v26.py'),'--tag',tag,'--range','0:900']+args,cwd=R,stdout=out,stderr=subprocess.STDOUT)
 x=json.loads((S/'runs'/tag/'comparison.json').read_text(encoding='utf-8'))
 assert p.returncode==0 and x['passed'],tag
 print(json.dumps(dict(passed=True,tag=tag,frames=x['comparison']['frames_compared'])),flush=True)
with ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(run,cases))
