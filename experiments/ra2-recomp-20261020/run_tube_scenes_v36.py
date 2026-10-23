"""Plain production and independent native/C observer gates with ordinary move orders."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import argparse,json,subprocess,sys
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v36'
ap=argparse.ArgumentParser();ap.add_argument('--blocked-only',action='store_true');ap.add_argument('--serial',action='store_true');a=ap.parse_args()
cases=[]
for direction,goal in [('east',80),('west',66),('blocked',80)]:
 if a.blocked_only and direction!='blocked':continue
 for observed in [True]:
  tag=('w3-tube-hook-' if observed else 'z-tube-production-')+direction
  args=['--tag',tag,'--evidence-stage','movement-state-v36','--movement-audit','--seconds','240','--range','0:500',
        '--scenario-map',str(S/'fixtures'/('tube-'+('east' if direction=='blocked' else direction)+'.MAP')),
        '--order',f'5:1022581:2:{goal}:114']
  # At frame170 the hidden actor is in cell76,114: a radius2 boundary covers
  # exit78,114. Unlike the old radius1 fixture this does not explicitly rebuild.
  if direction=='blocked':args+=['--unit-ring','170:1022581:2']
  cases.append((tag,'run_connection_v36.py' if observed else 'run_fixture_comparison.py',args))
for name,direction,goal in [('uphill','east',80),('downhill','west',66)]:
 for observed in [False,True]:
  tag=('w3-tube-hook-' if observed else 'z-tube-production-')+name
  args=['--tag',tag,'--evidence-stage','movement-state-v36','--movement-audit','--seconds','240','--range','0:500',
        '--scenario-map',str(S/'fixtures'/('tube-elevated-'+direction+'.MAP')),'--order',f'5:1022581:2:{goal}:114']
  cases.append((tag,'run_connection_v36.py' if observed else 'run_fixture_comparison.py',args))
for direction,goal in [('east',80),('west',66)]:
 for observed in [False,True]:
  tag='w3-tube-hook-curved-'+direction if observed else ('z-ce' if direction=='east' else 'z-cw')
  args=['--tag',tag,'--evidence-stage','movement-state-v36','--movement-audit','--seconds','240','--range','0:600','--scenario-map',str(S/'fixtures'/('tube-curved-'+direction+'.MAP')),'--order',f'5:1022581:2:{goal}:114']
  cases.append((tag,'run_connection_v36.py' if observed else 'run_fixture_comparison.py',args))
for name,fixture,goal,blocked in [('cu','tube-curved-elevated-east.MAP',80,False),('cd','tube-curved-elevated-west.MAP',66,False),('cb','tube-curved-east.MAP',80,True)]:
 for observed in [False,True]:
  tag=('p-' if observed else 'z-')+name
  args=['--tag',tag,'--evidence-stage','movement-state-v36','--movement-audit','--seconds','240','--range','0:600','--scenario-map',str(S/'fixtures'/fixture),'--order',f'5:1022581:2:{goal}:114']
  if blocked:args+=['--unit-ring','217:1022581:2']
  cases.append((tag,'run_connection_v36.py' if observed else 'run_fixture_comparison.py',args))

def run(case):
 tag,script,args=case
 path=S/'runs'/tag/'comparison.json'
 if path.exists():
  x=json.loads(path.read_text(encoding='utf-8'));assert x['passed'],tag
  result=dict(tag=tag,passed=True,frames=x['comparison']['frames_compared'],retained_verified_run=True);print(json.dumps(result),flush=True);return result
 with (S/(tag+'.log')).open('x',encoding='utf-8') as out:
  p=subprocess.run([sys.executable,'-B',str(R/script)]+args,cwd=R,stdout=out,stderr=subprocess.STDOUT)
 path=S/'runs'/tag/'comparison.json';x=json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}
 result=dict(tag=tag,passed=p.returncode==0 and x.get('passed',False),frames=x.get('comparison',{}).get('frames_compared',0))
 print(json.dumps(result),flush=True);return result
with ThreadPoolExecutor(max_workers=1 if a.serial else 2) as pool:results=list(pool.map(run,cases))
assert all(r['passed'] for r in results),results
