from pathlib import Path
import concurrent.futures,json,subprocess,sys,hashlib
ROOT=Path(__file__).resolve().parent; S=ROOT/'evidence/movement-state-v17'
cases=[]
for r in (2,3): cases.append(('ring'+str(r),'partial-ring-'+str(r)+'.MAP','0:350',['--order','5:1022579:2:70:108']))
for i in range(3): cases.append(('tc'+str(i),'turn-cloak-'+str(i)+'.MAP','0:400',['--order','150:1022579:2:71:111']))
cases.append(('large','large-target.MAP','0:350',['--order','5:1022579:2:71:109']))
for r in (2,3):
    name='dynamic-trucka.MAP' if r==2 else 'dynamic-far-base.MAP'
    cases.append(('ur'+str(r),name,'0:350',['--order','5:1022579:2:70:108','--unit-ring',f'7:1022579:{r}']))
cases += [
    ('long','dynamic-far-base.MAP','0:1500',['--order','5:1022579:2:100:114']),
    ('second-failure','dynamic-far-base.MAP','0:650',['--order','5:1022579:2:100:114','--unit-ring','398:1022579:2'])]
cases += [
    ('repeat-failure','dynamic-far-base.MAP','0:1250',
        ['--order','5:1022579:2:100:114','--unit-ring','398:1022579:2']
        + [x for f in range(450,1111,60) for x in ['--order',f'{f}:1022579:2:100:114']]),
    ('zero-road','dynamic-far-base.MAP','0:300',
        ['--order','5:1022579:2:100:114','--scenario-rules',str(S/'fixtures/rules-zero-road.ini')])]
prefix=sys.argv[1] if len(sys.argv)>1 else 'i-' 
fingerprint=hashlib.sha256((ROOT/'ra2/build-original-c/ra2.exe').read_bytes()).hexdigest()
def run(case):
    tag,name,span,orders=case; tag=prefix+tag
    with (S/(tag+'.log')).open('x',encoding='utf-8') as out:
        proc=subprocess.run([sys.executable,'-B',str(ROOT/'run_fixture_comparison.py'),'--tag',tag,'--evidence-stage','movement-state-v17',
            '--movement-audit','--seconds','240','--range',span,'--scenario-map',str(S/'fixtures'/name)]+orders,cwd=ROOT,stdout=out,stderr=subprocess.STDOUT)
    p=S/'runs'/tag/'comparison.json'; report=json.loads(p.read_text(encoding='utf-8')) if p.exists() else {}
    result=dict(tag=tag,exit_code=proc.returncode,passed=proc.returncode==0 and report.get('passed') and report.get('exe_sha256')==fingerprint,
        frames=report.get('comparison',{}).get('frames_compared',0))
    print(json.dumps(result),flush=True); return result
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool: results=list(pool.map(run,cases))
p=S/(prefix+'additional-matrix.json'); assert not p.exists()
p.write_text(json.dumps(dict(exe_sha256=fingerprint,results=results,passed=all(r['passed'] for r in results)),indent=2),encoding='utf-8')
raise SystemExit(0 if all(r['passed'] for r in results) else 1)
