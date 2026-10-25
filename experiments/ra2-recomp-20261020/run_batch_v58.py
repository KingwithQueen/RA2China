"""Two reversible search phases and finite original/C acceptance."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import argparse,hashlib,json,os,shutil,subprocess,sys
R=Path(__file__).resolve().parent;P=R.parent.parent
S=R/'evidence/movement-state-v58';O=R/'evidence/movement-state-v57'
assert O==Path(json.loads((S/'vcs-context.json').read_text(encoding='utf-8-sig'))['parent_archive']).parent
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,x):
 assert not p.exists(),p
 p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def run(args,name,allowed_codes=(0,)):
 print('Starting '+name,flush=True);log=S/(name+'.log');attempt=1
 while log.exists():log=S/(name+'-retry-'+str(attempt).zfill(2)+'.log');attempt+=1
 with log.open('x',encoding='utf-8') as f:
  q=subprocess.run([str(x) for x in args],cwd=R,stdout=f,stderr=subprocess.STDOUT,env=dict(os.environ,PYTHONIOENCODING='utf-8'))
 if q.returncode not in allowed_codes:
  print(log.read_text(encoding='utf-8',errors='replace')[-6000:],flush=True);raise RuntimeError(name)
 return log
def py(name,*args):return [sys.executable,'-X','utf8','-B',R/name,*args]
def fixture_job(tag,item,last=500):
 args=py('run_bridge_catalog_v58.py' if item.get('capture_host') else 'run_fixture_comparison.py','--tag',tag,'--evidence-stage',S.name,'--movement-audit','--seconds','240','--range','0:'+str(last),'--scenario-map',R/item['path'])
 if item.get('rules'):args+=['--scenario-rules',R/item['rules']]
 for order in item.get('orders',[]):args+=['--order',order]
 if item.get('capture_host'):args+=['--cell-catalog']
 return tag,args
def scenes(jobs,max_workers=2,baseline=False):
 def one(job):
  tag,args=job;p=S/'runs'/tag/'comparison.json'
  if not p.exists():run(args,'scene-'+tag,allowed_codes=(0,1) if tag in ['mi','sc','aw3','fm','b-fm'] else (0,))
  x=read(p);c=x['comparison'];observer=Path(args[4]).name=='run_bridge_catalog_v58.py'
  expected=sha(S/('baseline-observer/bridge-catalog-observer.exe' if baseline else 'bridge-catalog-observer.exe')) if observer else sha(R/'ra2/build-original-c/ra2.exe')
  assert all(r['passed'] and r['exit_code']==0 for r in x['runs'])
  assert x['exe_sha256']==expected and c['negative_control']['passed']
  if not x['passed']:
   assert tag in ['mi','sc','aw3','fm','b-fm']
   from accept_dynamic_v58 import analyze
   assert analyze(tag)['passed']
  else:assert c['rng_equal_all_frames'] and c['equal_frames']==c['frames_compared']
  return dict(tag=tag,frames=c['frames_compared'],exe_sha256=x['exe_sha256'],comparison_sha256=sha(p),capture_host=observer,strict_trace_equal=x['passed'])
 with ThreadPoolExecutor(max_workers=max_workers) as pool:return list(pool.map(one,jobs))
def native(part):
 run(['pwsh','-NoProfile','-File',R/'build-path-local-probe-v58.ps1'],'build-native-'+part)
 receipts=[]
 for phase in [0,1,2]:
  log=run([S/'path_local_probe.exe',R/'ra2/game/game.exe',str(phase)],'native-'+part+'-'+str(phase))
  x=read(log);assert x['passed'] and x['cases']==(8192 if phase==0 else 12288) and x['phase']==phase
  name='part-'+part+'-path-local-'+str(phase)+'.json'
  write(S/name,dict(**x,probe_exe_sha256=sha(S/'path_local_probe.exe'),original_sha256=sha(R/'ra2/game/game.exe')))
  receipts.append(name)
 if part=='baseline':
  out=S/'baseline-probe';assert not out.exists();out.mkdir();entries=[]
  for name in ['path_local_probe.c','path_local_probe.exe','native_probe_host.h']:
   shutil.copy2(S/name,out/name);entries.append(dict(path=(out/name).relative_to(R).as_posix(),sha256=sha(out/name)))
  write(S/'baseline-native-identity.json',dict(passed=True,files=entries,receipts=receipts,production_source=str(S/'baseline/ra2/src/gameplay/ground_path_local.c'),production_source_sha256=sha(S/'baseline/ra2/src/gameplay/ground_path_local.c'),probe_sha256=sha(out/'path_local_probe.exe')))
 return receipts
def snapshot(name,values,probes):
 out=S/'parts'/name;assert not out.exists()
 receipt=read(R/'ra2/build-original-c/source-content-receipt.json')
 assert receipt['source_count']==181 and len(receipt['inputs'])==312
 paths={Path(p).relative_to(R).as_posix() for p in receipt['inputs']}
 paths.update(['ra2/CMakeLists.txt','ra2/build-original-c/ra2.exe','ra2/build-original-c/source-content-receipt.json'])
 paths.update(p.relative_to(R).as_posix() for p in R.glob('*v58*') if p.is_file())
 paths.update(p.relative_to(R).as_posix() for p in S.iterdir() if p.is_file() and p.suffix in ['.c','.h','.exe'])
 entries=[]
 for rel in sorted(paths):
  d=out/rel;d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/rel,d);entries.append(dict(path=rel,sha256=sha(d)))
 write(out/'manifest.json',entries)
 write(out/'validation.json',dict(passed=True,part=name,exe_sha256=sha(R/'ra2/build-original-c/ra2.exe'),scenes=values,scene_count=len(values),frames=sum(x['frames'] for x in values),probes=probes,files=len(entries)))
 print('Saved '+name+' checkpoint',flush=True)
def part(name):
 run(py('integrate_services_v58.py',name),'integrate-'+name)
 run(['pwsh','-NoProfile','-File',R/'build-faithful.ps1'],'build-'+name)
 probes=native(name)
 jobs=[(name+'-default',py('run_skirmish_v58.py','--tag',name+'-default','--range','0:300'))]
 jobs += [fixture_job(name+'-cross-'+x['name'],x) for x in read(S/'bridge-cross-release-fixtures.json')['fixtures']]
 values=scenes(jobs,max_workers=1);assert sum(x['frames'] for x in values)==1303
 snapshot(name,values,probes)
 if name=='segments':write(S/'native-gates.json',dict(passed=True,groups=3,cases=32768,receipts=probes,capture_packet_cases_inherited=64,transport_packet_cases_inherited=128,scope='Original anchor 8192, turn shortening 12288, segment rewrite 12288 inputs; repeated before/after both parts counted once. Full buffers, cells, ordered callbacks, return values and native stack cleanup. Engine services stubbed; completion phase 3 not rerun.'))

def baseline_scenes():
 jobs=[fixture_job(x['baseline_tag'],x,x['last']) for x in read(S/'dynamic-fixtures.json')['fixtures'] if not x.get('baseline_stage')]
 values=scenes(jobs,baseline=True)
 for x in read(S/'dynamic-fixtures.json')['fixtures']:
  if x.get('baseline_stage'):
   p=R/'evidence'/x['baseline_stage']/'runs'/x['baseline_tag']/'comparison.json';q=read(p)
   assert q['exe_sha256']==sha(S/'baseline-observer/bridge-catalog-observer.exe')
   values.append(dict(tag=x['baseline_tag'],stage=x['baseline_stage'],frames=q['comparison']['frames_compared'],comparison_sha256=sha(p),inherited=True))
 write(S/'selected-baseline-scenes.json',dict(passed=True,results=values,scope='All four exact parent per-mode traces inherited by hash; frozen observer retained. No duplicate pre-change game runs.'))
def final_scenes():
 run(py('make_bridge_catalog_v58.py','--relink'),'prepare-final-fixture-host')
 run(['pwsh','-NoProfile','-File',R/'build-bridge-catalog-v58.ps1'],'build-final-capture-host')
 jobs=[fixture_job(x['tag'],x,x['last']) for x in read(S/'dynamic-fixtures.json')['fixtures']]
 for x in read(S/'collision-acceptance-fixtures.json')['fixtures']:
  if 'control' not in x['name']:jobs.append(fixture_job('contact-'+x['name'],x))
 for tag,filename,goal in [('curve-up','tube-curved-elevated-east.MAP',80),('curve-tall-down','tube-curved-tall-west.MAP',66)]:
  jobs.append(fixture_job(tag,dict(path=(S/'fixtures'/filename).relative_to(R).as_posix(),orders=[f'5:1022581:2:{goal}:114']),600))
 x=dict(path=(S/'fixtures/dynamic-far-base.MAP').relative_to(R).as_posix(),orders=['5:1022579:2:100:114']+[f'{f}:1022579:2:100:114' for f in range(450,1111,60)])
 tag,cmd=fixture_job('repeat-failure',x,1250);jobs.append((tag,cmd+['--unit-ring','398:1022579:2']))
 values=scenes(jobs)
 write(S/'final-scene-matrix.json',dict(passed=True,results=values,production_scenes=sum(not x['capture_host'] for x in values),production_frames=sum(x['frames'] for x in values if not x['capture_host']),observer_scenes=sum(x['capture_host'] for x in values),observer_frames=sum(x['frames'] for x in values if x['capture_host']),scope='Finite regression: mixed loading in both orders, two natural shores, full occupancy/release, bridge contact, repeated search failure and retained height anomalies.'))
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('action',choices=['baseline','turns','segments','final-scenes']);x=a.parse_args()
 if x.action=='baseline':baseline_scenes()
 elif x.action=='final-scenes':final_scenes()
 else:part(x.action)
