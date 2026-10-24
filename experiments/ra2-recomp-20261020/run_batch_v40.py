"""Finite functional-unit acceptance: two part checkpoints, two scene lanes, serial builds."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import argparse,hashlib,json,os,shutil,subprocess,sys
R=Path(__file__).resolve().parent;P=R.parent.parent;S=R/'evidence/movement-state-v40';O=R/'evidence/movement-state-v39'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,x):
 assert not p.exists(),p
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def run(args,name):
 print('Starting '+name,flush=True);log=S/(name+'.log');assert not log.exists(),log
 with log.open('x',encoding='utf-8') as f:q=subprocess.run([str(x) for x in args],cwd=R,stdout=f,stderr=subprocess.STDOUT,env=dict(os.environ,PYTHONIOENCODING='utf-8'))
 if q.returncode:
  print(log.read_text(encoding='utf-8',errors='replace')[-6000:],flush=True);raise RuntimeError(name)
 return log
def py(name,*args):return [sys.executable,'-X','utf8','-B',R/name,*args]
def fixture_job(tag,item,last=500,runner='run_fixture_comparison.py'):
 args=py(runner,'--tag',tag,'--evidence-stage','movement-state-v40','--movement-audit','--seconds','240','--range','0:'+str(last),'--scenario-map',R/item['path'])
 for order in item.get('orders',[]):args+=['--order',order]
 return tag,args
def scenes(jobs):
 def one(job):
  tag,args=job;run(args,'scene-'+tag);x=read(S/'runs'/tag/'comparison.json');c=x['comparison']
  assert x['passed'] and c['equal_frames']==c['frames_compared'] and c['rng_equal_all_frames']
  return dict(tag=tag,frames=c['frames_compared'],exe_sha256=x['exe_sha256'],comparison_sha256=sha(S/'runs'/tag/'comparison.json'))
 with ThreadPoolExecutor(max_workers=2) as pool:return list(pool.map(one,jobs))
def probe(exe,phase,name):
 args=[S/(exe+'_probe.exe'),R/'ra2/game/game.exe']+([] if phase is None else [str(phase)])
 log=run(args,name);x=read(log);assert x['passed'] and x.get('advance_cases',x.get('cases'))==65536
 write(S/(name+'.json'),dict(**x,probe_exe_sha256=sha(S/(exe+'_probe.exe')),original_sha256=sha(R/'ra2/game/game.exe')))
 return name+'.json'
def snapshot(part,values,probes):
 out=S/'parts'/part;assert not out.exists();receipt=read(R/'ra2/build-original-c/source-content-receipt.json');assert len(receipt['inputs'])==294 and receipt['source_count']==172
 paths={Path(p).relative_to(R).as_posix() for p in receipt['inputs']};paths.update(['ra2/build-original-c/ra2.exe','ra2/CMakeLists.txt'])
 paths.update(p.relative_to(R).as_posix() for p in R.glob('*v40*') if p.is_file())
 paths.update(p.relative_to(R).as_posix() for p in S.iterdir() if p.is_file() and p.suffix in ['.c','.h','.asm','.exe'])
 paths.update((S/name).relative_to(R).as_posix() for name in probes)
 entries=[]
 for rel in sorted(paths):
  dest=out/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/rel,dest);entries.append(dict(path=rel,sha256=sha(dest)))
 write(out/'manifest.json',entries);write(out/'validation.json',dict(passed=True,part=part,exe_sha256=sha(R/'ra2/build-original-c/ra2.exe'),scenes=values,scene_count=len(values),frames=sum(x['frames'] for x in values),probes=probes,files=len(entries)))
 print('Saved '+part+' checkpoint',flush=True)
def part(name,resume):
 if name=='services' and not resume:
  run(py('integrate_services_v40.py'),'integrate-services')
  run(['pwsh','-NoProfile','-File',R/'build-faithful.ps1'],'build-services')
 exe='advance' if name=='advance' else 'overlap'
 run(['pwsh','-NoProfile','-File',R/('build-'+exe+'-probe-v40.ps1')],'build-part-'+exe)
 probes=[probe(exe,p,'part-'+name+'-native-'+str(p)) for p in ([None] if name=='advance' else [22,26])]
 jobs=[(name+'-default',py('run_skirmish_v40.py','--tag',name+'-default','--range','0:300'))]
 jobs += [fixture_job(name+'-cross-'+x['name'],x) for x in read(S/'bridge-cross-release-fixtures.json')['fixtures']]
 values=scenes(jobs);assert sum(x['frames'] for x in values)==1303;snapshot(name,values,probes)
def final_build():
 run(['pwsh','-NoProfile','-File',R/'build-advance-probe-v40.ps1'],'build-final-advance')
 receipts=[probe('advance',None,'native-advance')]
 run(['pwsh','-NoProfile','-File',R/'build-overlap-probe-v40.ps1'],'build-final-overlap')
 receipts += [probe('overlap',p,'native-overlap-'+str(p)) for p in range(27)]
 write(S/'native-gates.json',dict(passed=True,groups=28,cases=28*65536,receipts=receipts,scope='Full affected sampled-Advance family plus shared exit/continuation regressions; no invented new native aliases.',inherited_parent=str(O/'native-gates.json')))
 run(py('make_connection_fixture_v40.py'),'prepare-connection-observer')
 run(['pwsh','-NoProfile','-File',R/'build-connection-fixture-v40.ps1'],'build-connection-observer')
 write(S/'final-build-ready.json',dict(passed=True,production_sha256=sha(R/'ra2/build-original-c/ra2.exe'),observer_sha256=sha(S/'connection-fixture-probe.exe')))
def final_scenes():
 assert read(S/'final-build-ready.json')['passed'];jobs=[]
 for x in read(S/'bridge-cross-release-fixtures.json')['fixtures']:
  jobs.extend([fixture_job('cross-'+x['name'],x),fixture_job('observed-cross-'+x['name'],x,runner='run_connection_v40.py')])
 for x in read(S/'bridge-infantry-fixtures.json')['fixtures']:jobs.append(fixture_job(x['name'],x))
 jobs.append(fixture_job('enemy-traffic-north',read(S/'bridge-hostile-fixtures.json')['fixtures'][0]))
 for tag,filename,goal in [('curve-up','tube-curved-elevated-east.MAP',80),('curve-tall-down','tube-curved-tall-west.MAP',66)]:
  jobs.append(fixture_job(tag,dict(path=(S/'fixtures'/filename).relative_to(R).as_posix(),orders=[f'5:1022581:2:{goal}:114']),600))
 x=dict(path=(S/'fixtures/tube-east.MAP').relative_to(R).as_posix(),orders=['5:1022581:2:80:114']);tag,args=fixture_job('blocked-tube',x);jobs.append((tag,args+['--unit-ring','170:1022581:2']))
 x=dict(path=(S/'fixtures/dynamic-far-base.MAP').relative_to(R).as_posix(),orders=['5:1022579:2:100:114']+[f'{f}:1022579:2:100:114' for f in range(450,1111,60)]);tag,args=fixture_job('repeat-failure',x,1250);jobs.append((tag,args+['--unit-ring','398:1022579:2']))
 values=scenes(jobs);assert len(values)==11
 write(S/'final-scene-matrix.json',dict(passed=True,results=values,production_scenes=9,production_frames=5459,observer_scenes=2,observer_frames=1002,scope='Affected core effects and representative original anomalies; unchanged alias dispatch/source investigation inherited from accepted v39.'))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('action',choices=['advance','services','final-build','final-scenes']);ap.add_argument('--resume',action='store_true');a=ap.parse_args()
 if a.action=='final-build':final_build()
 elif a.action=='final-scenes':final_scenes()
 else:part(a.action,a.resume)
