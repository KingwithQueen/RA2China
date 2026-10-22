"""Each independent integration must pass default, ring and default-budget scenes."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import argparse,hashlib,json,subprocess,sys
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v20'
ap=argparse.ArgumentParser();ap.add_argument('part',choices=['arrival','cleanup','passage']);a=ap.parse_args()
prefix={'arrival':'a-arrival','cleanup':'b-cleanup','passage':'c-passage'}[a.part]
for name in ['make_truck_fixture_v20.py','make_truck_actor_fixture_v20.py']:
    subprocess.run([sys.executable,'-B',str(R/name)],cwd=R,check=True)
with (S/(prefix+'-helper-build.log')).open('x',encoding='utf-8') as out:
    subprocess.run(['pwsh','-NoProfile','-File',str(R/'build-truck-actor-fixture-v20.ps1')],cwd=R,stdout=out,stderr=subprocess.STDOUT,check=True)
budget='h-default-budget' if a.part=='passage' else prefix+'-budget'
cases=[(prefix+'-default','run_skirmish_v20.py',['--range','0:900']),
    (prefix+'-ur3','run_fixture_comparison.py',['--evidence-stage','movement-state-v20','--movement-audit','--seconds','240',
    '--range','0:100','--scenario-map',str(S/'fixtures/dynamic-far-base.MAP'),'--order','5:1022579:2:70:108','--unit-ring','7:1022579:3']),
    (budget,'run_skirmish_v20.py',['--range','0:900','--host-exe',str(S/'truck-actor-fixture-probe.exe'),'--unit-ring','27:1032259:2'])]
def run(case):
    tag,script,args=case
    with (S/(tag+'.log')).open('x',encoding='utf-8') as out:
        p=subprocess.run([sys.executable,'-B',str(R/script),'--tag',tag]+args,cwd=R,stdout=out,stderr=subprocess.STDOUT)
    report=S/'runs'/tag/'comparison.json';x=json.loads(report.read_text(encoding='utf-8')) if report.exists() else {}
    result=dict(tag=tag,passed=p.returncode==0 and x.get('passed',False),frames=x.get('comparison',{}).get('frames_compared',0))
    print(json.dumps(result),flush=True);return result
with ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(run,cases))
assert all(r['passed'] for r in results),results
probes={'arrival':['arrival-native.json'],'cleanup':['cleanup-native.json'],'passage':['passage-native.json','height-native.json']}[a.part]
command=[sys.executable,'-B',str(R/'snapshot_part_v20.py'),'--name',a.part+'-verified',]
for probe in probes:command+=['--probe',probe]
for tag,_,_ in cases:command+=['--scene',tag]
subprocess.run(command,cwd=R,check=True)
print(json.dumps(dict(passed=True,part=a.part,scenes=results,exe_sha256=hashlib.sha256((R/'ra2/build-original-c/ra2.exe').read_bytes()).hexdigest())),flush=True)
