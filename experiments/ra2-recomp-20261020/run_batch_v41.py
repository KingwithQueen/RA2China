"""Finite Prepare/Advance acceptance; serial builders and two original/C scene lanes."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import argparse,hashlib,json,os,shutil,subprocess,sys
R=Path(__file__).resolve().parent;P=R.parent.parent;S=R/'evidence/movement-state-v41';O=R/'evidence/movement-state-v40'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,x):
 assert not p.exists(),p
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def run(args,name):
 print('Starting '+name,flush=True);log=S/(name+'.log');attempt=1
 while log.exists():log=S/(name+'-retry-'+str(attempt).zfill(2)+'.log');attempt+=1
 with log.open('x',encoding='utf-8') as f:q=subprocess.run([str(x) for x in args],cwd=R,stdout=f,stderr=subprocess.STDOUT,env=dict(os.environ,PYTHONIOENCODING='utf-8'))
 if q.returncode:
  print(log.read_text(encoding='utf-8',errors='replace')[-6000:],flush=True);raise RuntimeError(name)
 return log
def py(name,*args):return [sys.executable,'-X','utf8','-B',R/name,*args]
def fixture_job(tag,item,last=500,observed=False):
 args=py('run_connection_v41.py' if observed else 'run_fixture_comparison.py','--tag',tag,'--evidence-stage',S.name,'--movement-audit','--seconds','240','--range','0:'+str(last),'--scenario-map',R/item['path'])
 if item.get('rules'):args+=['--scenario-rules',R/item['rules']]
 for order in item.get('orders',[]):args+=['--order',order]
 return tag,args
def scenes(jobs):
 def one(job):
  tag,args=job;report=S/'runs'/tag/'comparison.json'
  if not report.exists():run(args,'scene-'+tag)
  x=read(report);c=x['comparison'];functional=S/'runs'/tag/'functional-acceptance.json'
  accepted=x['passed'] or (tag=='observed-contact-train' and functional.exists() and read(functional)['passed'] and read(functional)['comparison_sha256']==sha(report))
  expected=sha(S/'connection-fixture-probe.exe') if tag.startswith('observed-') else sha(R/'ra2/build-original-c/ra2.exe')
  assert accepted and x['exe_sha256']==expected and c['equal_frames']==c['frames_compared'] and c['rng_equal_all_frames']
  return dict(tag=tag,frames=c['frames_compared'],exe_sha256=x['exe_sha256'],comparison_sha256=sha(report),strict_internal_trace_equal=x['passed'])
 with ThreadPoolExecutor(max_workers=2) as pool:return list(pool.map(one,jobs))
def probe(name,tag):
 log=run([S/(name+'_probe.exe'),R/'ra2/game/game.exe'],tag);x=read(log);assert x['passed']
 if name=='prepare':assert x['entry_cases']==x['retry_cases']==x['cycle_cases']==65536
 else:assert 65536 in [x.get(k) for k in ['advance_cases','continuation_cases','segment_cases','cases']]
 write(S/(tag+'.json'),dict(**x,probe_exe_sha256=sha(S/(name+'_probe.exe')),original_sha256=sha(R/'ra2/game/game.exe')))
 return tag+'.json'
def build_probe(name,tag):run(['pwsh','-NoProfile','-File',R/('build-'+name+'-probe-v41.ps1')],tag)
def snapshot(name,values,probes):
 out=S/'parts'/name;assert not out.exists();receipt=read(R/'ra2/build-original-c/source-content-receipt.json');assert len(receipt['inputs'])==296 and receipt['source_count']==173
 paths={Path(p).relative_to(R).as_posix() for p in receipt['inputs']};paths.update(['ra2/CMakeLists.txt','ra2/build-original-c/ra2.exe'])
 paths.update(p.relative_to(R).as_posix() for p in R.glob('*v41*') if p.is_file());paths.update(p.relative_to(R).as_posix() for p in S.iterdir() if p.is_file() and p.suffix in ['.c','.h','.exe'])
 entries=[]
 for rel in sorted(paths):
  d=out/rel;d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/rel,d);entries.append(dict(path=rel,sha256=sha(d)))
 write(out/'manifest.json',entries);write(out/'validation.json',dict(passed=True,part=name,exe_sha256=sha(R/'ra2/build-original-c/ra2.exe'),scenes=values,scene_count=len(values),frames=sum(x['frames'] for x in values),probes=probes,files=len(entries)))
 print('Saved '+name+' checkpoint',flush=True)
def part(name,resume):
 if name=='advance' and not resume:
  run(py('integrate_advance_v41.py'),'integrate-advance');run(['pwsh','-NoProfile','-File',R/'build-faithful.ps1'],'build-advance')
 probes=[]
 for n in (['prepare'] if name=='prepare' else ['segment','continuation','advance']):
  build_probe(n,'build-part-'+n);probes.append(probe(n,'part-'+name+'-'+n))
 jobs=[(name+'-default',py('run_skirmish_v41.py','--tag',name+'-default','--range','0:300'))]
 jobs += [fixture_job(name+'-cross-'+x['name'],x) for x in read(S/'bridge-cross-release-fixtures.json')['fixtures']]
 values=scenes(jobs);assert sum(x['frames'] for x in values)==1303;snapshot(name,values,probes)
def final_build():
 receipts=[]
 for name in ['prepare','segment','continuation','advance']:
  build_probe(name,'build-final-'+name);receipts.append(probe(name,'native-'+name))
 write(S/'native-gates.json',dict(passed=True,groups=6,cases=393216,new_cycle_cases=65536,receipts=receipts,scope='Entry, retry, combined Prepare cycle, segment gate, Advance turn continuation and sampled cell effects. Unaffected historic matrices retained.'))
 run(py('make_connection_fixture_v41.py'),'prepare-connection-observer');run(['pwsh','-NoProfile','-File',R/'build-connection-fixture-v41.ps1'],'build-connection-observer')
 write(S/'final-build-ready.json',dict(passed=True,production_sha256=sha(R/'ra2/build-original-c/ra2.exe'),observer_sha256=sha(S/'connection-fixture-probe.exe')))
def final_scenes():
 assert read(S/'final-build-ready.json')['passed'];jobs=[]
 for x in read(S/'bridge-cross-release-fixtures.json')['fixtures']:
  jobs.extend([fixture_job('cross-'+x['name'],x),fixture_job('observed-cross-'+x['name'],x,observed=True)])
 for x in read(S/'collision-acceptance-fixtures.json')['fixtures']:
  jobs.append(fixture_job('contact-'+x['name'],x))
  if 'control' not in x['name']:jobs.append(fixture_job('observed-contact-'+x['name'],x,observed=True))
 for tag,filename,goal in [('curve-up','tube-curved-elevated-east.MAP',80),('curve-tall-down','tube-curved-tall-west.MAP',66)]:
  jobs.append(fixture_job(tag,dict(path=(S/'fixtures'/filename).relative_to(R).as_posix(),orders=[f'5:1022581:2:{goal}:114']),600))
 x=dict(path=(S/'fixtures/tube-east.MAP').relative_to(R).as_posix(),orders=['5:1022581:2:80:114']);tag,args=fixture_job('blocked-tube',x);jobs.append((tag,args+['--unit-ring','170:1022581:2']))
 x=dict(path=(S/'fixtures/dynamic-far-base.MAP').relative_to(R).as_posix(),orders=['5:1022579:2:100:114']+[f'{f}:1022579:2:100:114' for f in range(450,1111,60)]);tag,args=fixture_job('repeat-failure',x,1250);jobs.append((tag,args+['--unit-ring','398:1022579:2']))
 values=scenes(jobs);assert len(values)==14
 write(S/'final-scene-matrix.json',dict(passed=True,results=values,production_scenes=10,production_frames=5960,observer_scenes=4,observer_frames=2004,scope='New real train/crush effects, rule-flag controls, occupied bridge traffic and affected retry/height/exit regression.'))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('action',choices=['prepare','advance','final-build','final-scenes']);ap.add_argument('--resume',action='store_true');a=ap.parse_args()
 if a.action=='final-build':final_build()
 elif a.action=='final-scenes':final_scenes()
 else:part(a.action,a.resume)
