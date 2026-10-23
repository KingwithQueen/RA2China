"""Two bounded lanes start only after all production changes and observer builds finish."""
from pathlib import Path
import argparse,json,os,subprocess,sys,time
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v35'
ap=argparse.ArgumentParser();ap.add_argument('lane',choices=['core','bridge']);a=ap.parse_args()
ready=S/'final-build-ready.json'
while not ready.exists():time.sleep(3)
assert json.loads(ready.read_text(encoding='utf-8'))['passed']
if a.lane=='core':jobs=[['run_acceptance_v35.py','production'],['run_acceptance_v35.py','observer','--only','internal-scenes','tube-scenes','combined-scenes','bridge-observer']]
else:
    jobs=[['run_bridge_detour_v35.py','production'],['run_bridge_detour_v35.py','observer'],['audit_bridge_detour_v35.py'],['run_bridge_occupied_v35.py','production'],['run_bridge_occupied_v35.py','observer'],['audit_bridge_occupied_v35.py']]
    for script in ['run_north_query_v35.py','run_bridge_mixed_v35.py','run_bridge_hostile_v35.py','run_bridge_infantry_v35.py']:
        jobs.extend([[script,'production'],[script,'observer']])
    jobs.extend([['audit_north_query_v35.py'],['run_alias_scenes_v35.py'],['run_acceptance_v35.py','observer','--only','tall-scenes']])
for args in jobs:
    print('Starting '+' '.join(args),flush=True)
    subprocess.run([sys.executable,'-X','utf8','-B',str(R/args[0]),*args[1:]],cwd=R,check=True,env=dict(os.environ,PYTHONIOENCODING='utf-8'))
(S/(a.lane+'-scenes-complete.json')).write_text(json.dumps(dict(passed=True,lane=a.lane),indent=2)+'\n',encoding='utf-8')
print(a.lane+' lane complete',flush=True)
