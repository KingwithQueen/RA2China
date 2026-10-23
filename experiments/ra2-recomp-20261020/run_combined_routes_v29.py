"""Successful curved height routes with real, normally placed exit blockers."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json, os, subprocess, sys
R = Path(__file__).resolve().parent
S = R / 'evidence/movement-state-v29'
specs = [('ub','tube-curved-tall-east.MAP',80,728), ('db','tube-curved-elevated-west.MAP',66,416),
         ('mu','tube-mirror-east.MAP',80,728), ('md','tube-mirror-west.MAP',66,416)]
cases = [(observed,*spec) for spec in specs for observed in [False,True]]

def run(case):
    observed,name,fixture,goal,height = case
    tag = ('k-' if observed else 'x-')+name
    command = [sys.executable,'-B',str(R/('run_connection_v29.py' if observed else 'run_fixture_comparison.py')),
        '--tag',tag,'--evidence-stage','movement-state-v29','--movement-audit','--seconds','240','--range','0:600',
        '--scenario-map',str(S/'fixtures'/fixture),'--order',f'5:1022581:2:{goal}:114','--unit-ring','217:1022581:2']
    with (S/(tag+'.log')).open('x',encoding='utf-8') as output:
        p = subprocess.run(command,cwd=R,stdout=output,stderr=subprocess.STDOUT,env=dict(os.environ,PYTHONIOENCODING='utf-8'))
    path = S/'runs'/tag/'comparison.json'
    report = json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}
    value = dict(tag=tag,passed=p.returncode==0 and report.get('passed',False),frames=report.get('comparison',{}).get('frames_compared',0))
    print(json.dumps(value),flush=True)
    return value

with ThreadPoolExecutor(max_workers=1) as pool:
    results = list(pool.map(run,cases))
(S/'combined-runs.json').write_text(json.dumps(dict(passed=all(x['passed'] for x in results),results=results),indent=2)+'\n',encoding='utf-8')
assert all(x['passed'] for x in results),results
