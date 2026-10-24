"""Finite Prepare/Advance acceptance; serial builders and two original/C scene lanes."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import argparse,hashlib,json,os,shutil,subprocess,sys
R=Path(__file__).resolve().parent;P=R.parent.parent;S=R/'evidence/movement-state-v51';O=R/'evidence/movement-state-v50'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,x):
 assert not p.exists(),p
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def run(args,name,allowed_codes=(0,)):
 print('Starting '+name,flush=True);log=S/(name+'.log');attempt=1
 while log.exists():log=S/(name+'-retry-'+str(attempt).zfill(2)+'.log');attempt+=1
 with log.open('x',encoding='utf-8') as f:q=subprocess.run([str(x) for x in args],cwd=R,stdout=f,stderr=subprocess.STDOUT,env=dict(os.environ,PYTHONIOENCODING='utf-8'))
 if q.returncode not in allowed_codes:
  print(log.read_text(encoding='utf-8',errors='replace')[-6000:],flush=True);raise RuntimeError(name)
 return log
def py(name,*args):return [sys.executable,'-X','utf8','-B',R/name,*args]
def fixture_job(tag,item,last=500):
 args=py('run_bridge_catalog_v51.py' if item.get('capture_host') else 'run_fixture_comparison.py','--tag',tag,'--evidence-stage',S.name,'--movement-audit','--seconds','240','--range','0:'+str(last),'--scenario-map',R/item['path'])
 if item.get('rules'):args+=['--scenario-rules',R/item['rules']]
 for order in item.get('orders',[]):args+=['--order',order]
 if item.get('capture_host'):args+=['--cell-catalog']
 return tag,args

def scenes(jobs,max_workers=2):
 def one(job):
  tag,args=job;p=S/'runs'/tag/'comparison.json'
  if not p.exists():run(args,'scene-'+tag,allowed_codes=(0,1) if tag in ['cw','ca','of'] else (0,))
  x=read(p);c=x['comparison'];observer=Path(args[4]).name=='run_bridge_catalog_v51.py';expected=sha(S/'bridge-catalog-observer.exe') if observer else sha(R/'ra2/build-original-c/ra2.exe')
  if not x['passed'] and tag in ['cw','ca','of']:
   from accept_dynamic_v51 import analyze
   assert analyze(tag)['baseline_inherited_exactly']
  else:assert x['passed'] and c['rng_equal_all_frames'] and c['equal_frames']==c['frames_compared']
  assert x['exe_sha256']==expected
  return dict(tag=tag,frames=c['frames_compared'],exe_sha256=x['exe_sha256'],comparison_sha256=sha(p),capture_host=observer,strict_trace_equal=x['passed'])
 with ThreadPoolExecutor(max_workers=max_workers) as pool:return list(pool.map(one,jobs))

def snapshot(name,values,probes):
 out=S/'parts'/name;assert not out.exists();receipt=read(R/'ra2/build-original-c/source-content-receipt.json');assert len(receipt['inputs'])==312 and receipt['source_count']==181
 paths={Path(p).relative_to(R).as_posix() for p in receipt['inputs']};paths.update(['ra2/CMakeLists.txt','ra2/build-original-c/ra2.exe']);paths.update(p.relative_to(R).as_posix() for p in R.glob('*v51*') if p.is_file());paths.update(p.relative_to(R).as_posix() for p in S.iterdir() if p.is_file() and p.suffix in ['.c','.h','.exe'])
 entries=[]
 for rel in sorted(paths):
  d=out/rel;d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/rel,d);entries.append(dict(path=rel,sha256=sha(d)))
 write(out/'manifest.json',entries);write(out/'validation.json',dict(passed=True,part=name,exe_sha256=sha(R/'ra2/build-original-c/ra2.exe'),scenes=values,scene_count=len(values),frames=sum(x['frames'] for x in values),probes=probes,files=len(entries)))
 print('Saved '+name+' checkpoint',flush=True)


def native(name,phase,part):
 tag='part-'+part+'-'+name+'-'+str(phase);p=S/(tag+'.json')
 if p.exists():assert read(p)['passed'] and read(p)['probe_exe_sha256']==sha(S/(name+'_probe.exe'));return p.name
 run(['pwsh','-NoProfile','-File',R/('build-'+name.replace('_','-')+'-probe-v51.ps1')],'build-'+tag)
 log=run([S/(name+'_probe.exe'),R/'ra2/game/game.exe',*([str(phase)] if phase is not None else [])],tag);x=read(log);assert x['passed'];write(p,dict(**x,probe_exe_sha256=sha(S/(name+'_probe.exe')),original_sha256=sha(R/'ra2/game/game.exe')));return p.name

def part(name):
 if name=='exit' and 'snapshot_exit_chain' not in (R/'ra2/src/gameplay/ground_tube_state.c').read_text(encoding='utf-8'):run(py('integrate_tube_exit_v51.py'),'integrate-exit')
 run(['pwsh','-NoProfile','-File',R/'build-faithful.ps1'],'build-'+name)
 receipts=[native('overlap',1,name)] if name=='gate' else [native('overlap',1,'exit2'),native('tube_state',0,'exit2')]
 prefix=name if name=='gate' else 'exit2'
 jobs=[(prefix+'-default',py('run_skirmish_v51.py','--tag',prefix+'-default','--range','0:300'))]
 jobs += [fixture_job(prefix+'-cross-'+x['name'],x) for x in read(S/'bridge-cross-release-fixtures.json')['fixtures']]
 values=scenes(jobs,max_workers=1);assert sum(x['frames'] for x in values)==1303;snapshot(name,values,receipts)
 if name=='exit':
  names=receipts
  write(S/'native-gates.json',dict(passed=True,groups=2,cases=98304,capture_packet_cases_inherited=64,receipts=names,scope='Template live type/overlay gates and occupied/empty shared tube exits; native service callback mutation and cleanup boundaries.'))

def final_scenes():
 run(py('make_bridge_catalog_v51.py','--relink'),'prepare-final-fixture-host')
 run(['pwsh','-NoProfile','-File',R/'build-bridge-catalog-v51.ps1'],'build-final-capture-host')
 jobs=[fixture_job(x['tag'],x,x['last']) for x in read(S/'dynamic-fixtures.json')['fixtures']]
 for x in read(S/'collision-acceptance-fixtures.json')['fixtures']:
  if 'control' not in x['name']:jobs.append(fixture_job('contact-'+x['name'],x))
 for tag,filename,goal in [('curve-up','tube-curved-elevated-east.MAP',80),('curve-tall-down','tube-curved-tall-west.MAP',66)]:jobs.append(fixture_job(tag,dict(path=(S/'fixtures'/filename).relative_to(R).as_posix(),orders=[f'5:1022581:2:{goal}:114']),600))
 x=dict(path=(S/'fixtures/dynamic-far-base.MAP').relative_to(R).as_posix(),orders=['5:1022579:2:100:114']+[f'{f}:1022579:2:100:114' for f in range(450,1111,60)]);tag,command=fixture_job('repeat-failure',x,1250);jobs.append((tag,command+['--unit-ring','398:1022579:2']))
 values=scenes(jobs,max_workers=2)
 write(S/'final-scene-matrix.json',dict(passed=True,results=values,production_scenes=sum(not x['capture_host'] for x in values),production_frames=sum(x['frames'] for x in values if not x['capture_host']),observer_scenes=sum(x['capture_host'] for x in values),observer_frames=sum(x['frames'] for x in values if x['capture_host']),scope='Independent corner8 bridge module, repeated water/air transport, occupied-shore fallback and normal-airfield aircraft return, with affected collision/failure/height regression.'))
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('action',choices=['gate','exit','final-scenes']);x=a.parse_args()
 if x.action=='final-scenes':final_scenes()
 else:part(x.action)
