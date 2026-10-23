"""Move two unchanged suites to the core lane after its observers finish."""
from pathlib import Path
import hashlib,json,os,subprocess,sys,time
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v33'
ready=S/'core-observers-complete.json'
while not ready.exists():time.sleep(3)
assert json.loads(ready.read_text(encoding='utf-8'))['passed']
jobs=[('combined-scenes','run_combined_routes_v33.py',[]),('bridge-observer','run_bridge_scenes_v33.py',['observer'])]
for label,script,args in jobs:
    print('Starting delegated '+label,flush=True)
    with (S/('accept-'+label+'.log')).open('x',encoding='utf-8') as output:
        subprocess.run([sys.executable,'-X','utf8','-B',str(R/script),*args],cwd=R,check=True,stdout=output,stderr=subprocess.STDOUT,env=dict(os.environ,PYTHONIOENCODING='utf-8'))
    (S/('delegated-'+label+'.json')).write_text(json.dumps(dict(passed=True,job=label,runner=script,runner_sha256=hashlib.sha256((R/script).read_bytes()).hexdigest(),two_lanes_max=True),indent=2)+'\n',encoding='utf-8')
    print('Completed delegated '+label,flush=True)
