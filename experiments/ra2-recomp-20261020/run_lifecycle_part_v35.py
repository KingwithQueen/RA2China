"""Each independent integration must pass default, ring and default-budget scenes."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import argparse,hashlib,json,subprocess,sys
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v35'
ap=argparse.ArgumentParser();ap.add_argument('part',choices=['template','passage','returns']);ap.add_argument('--resume',action='store_true');a=ap.parse_args()
prefix={'template':'a-template','passage':'b-passage','returns':'c-final'}[a.part]
probe_name={'template':'loaded-sample','passage':'terrain-weapon','returns':'invalidate-service'}[a.part]
legacy=S/(probe_name+'-verified-01.json');canonical=S/(probe_name+'-probe-verified-01.json')
if legacy.exists():
    assert not canonical.exists() and legacy.resolve().is_relative_to(S.resolve()) and canonical.resolve().is_relative_to(S.resolve())
    legacy.replace(canonical)
if not a.resume:
    for name in ['make_truck_fixture_v35.py','make_truck_actor_fixture_v35.py']:
        subprocess.run([sys.executable,'-B',str(R/name)],cwd=R,check=True)
    with (S/(prefix+'-helper-build.log')).open('x',encoding='utf-8') as out:
        subprocess.run(['pwsh','-NoProfile','-File',str(R/'build-truck-actor-fixture-v35.ps1')],cwd=R,stdout=out,stderr=subprocess.STDOUT,check=True)
budget='v-default-budget' if a.part=='returns' else prefix+'-budget'
cases=[(prefix+'-default','run_skirmish_v35.py',['--range','0:900']),
    (prefix+'-ur3','run_fixture_comparison.py',['--evidence-stage','movement-state-v35','--movement-audit','--seconds','240',
    '--range','0:100','--scenario-map',str(S/'fixtures/dynamic-far-base.MAP'),'--order','5:1022579:2:70:108','--unit-ring','7:1022579:3']),
    (budget,'run_skirmish_v35.py',['--range','0:900','--host-exe',str(S/'truck-actor-fixture-probe.exe'),'--unit-ring','27:1032259:2'])]
for direction,goal in [('east',80),('west',66)]:
 cases.append((prefix+'-tube-'+direction,'run_fixture_comparison.py',['--evidence-stage','movement-state-v35','--movement-audit','--seconds','240','--range','0:500','--scenario-map',str(S/'fixtures'/('tube-'+direction+'.MAP')),'--order',f'5:1022581:2:{goal}:114']))

cases.append((prefix+'-tube-blocked','run_fixture_comparison.py',['--evidence-stage','movement-state-v35','--movement-audit','--seconds','240','--range','0:500','--scenario-map',str(S/'fixtures/tube-east.MAP'),'--order','5:1022581:2:80:114','--unit-ring','170:1022581:2']))

def run(case):
    tag,script,args=case
    report=S/'runs'/tag/'comparison.json'
    if report.exists():
        x=json.loads(report.read_text(encoding='utf-8'));assert a.resume and x['passed'],tag
        return dict(tag=tag,passed=True,frames=x['comparison']['frames_compared'],retained_verified_pair=True)
    with (S/(tag+'.log')).open('x',encoding='utf-8') as out:
        p=subprocess.run([sys.executable,'-B',str(R/script),'--tag',tag]+args,cwd=R,stdout=out,stderr=subprocess.STDOUT)
    report=S/'runs'/tag/'comparison.json';x=json.loads(report.read_text(encoding='utf-8')) if report.exists() else {}
    result=dict(tag=tag,passed=p.returncode==0 and x.get('passed',False),frames=x.get('comparison',{}).get('frames_compared',0))
    print(json.dumps(result),flush=True);return result
with ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(run,cases))
assert all(r['passed'] for r in results),results
probes={'template':['loaded-sample-probe-verified-01.json'],'passage':['terrain-weapon-probe-verified-01.json'],'returns':['invalidate-service-probe-verified-01.json']}[a.part]
command=[sys.executable,'-B',str(R/'snapshot_part_v35.py'),'--name',a.part+'-verified',]
for probe in probes:command+=['--probe',probe]
for tag,_,_ in cases:command+=['--scene',tag]
subprocess.run(command,cwd=R,check=True)
print(json.dumps(dict(passed=True,part=a.part,scenes=results,exe_sha256=hashlib.sha256((R/'ra2/build-original-c/ra2.exe').read_bytes()).hexdigest())),flush=True)
