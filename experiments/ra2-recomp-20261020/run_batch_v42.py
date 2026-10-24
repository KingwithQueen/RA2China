"""Finite Prepare/Advance acceptance; serial builders and two original/C scene lanes."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import argparse,hashlib,json,os,shutil,subprocess,sys
R=Path(__file__).resolve().parent;P=R.parent.parent;S=R/'evidence/movement-state-v42';O=R/'evidence/movement-state-v41'
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
 args=py('run_connection_v42.py' if observed else 'run_fixture_comparison.py','--tag',tag,'--evidence-stage',S.name,'--movement-audit','--seconds','240','--range','0:'+str(last),'--scenario-map',R/item['path'])
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
def build_probe(name,tag):run(['pwsh','-NoProfile','-File',R/('build-'+name+'-probe-v42.ps1')],tag)
def snapshot(name,values,probes):
 out=S/'parts'/name;assert not out.exists();receipt=read(R/'ra2/build-original-c/source-content-receipt.json');assert len(receipt['inputs'])==298 and receipt['source_count']==174
 paths={Path(p).relative_to(R).as_posix() for p in receipt['inputs']};paths.update(['ra2/CMakeLists.txt','ra2/build-original-c/ra2.exe'])
 paths.update(p.relative_to(R).as_posix() for p in R.glob('*v42*') if p.is_file());paths.update(p.relative_to(R).as_posix() for p in S.iterdir() if p.is_file() and p.suffix in ['.c','.h','.exe'])
 entries=[]
 for rel in sorted(paths):
  d=out/rel;d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/rel,d);entries.append(dict(path=rel,sha256=sha(d)))
 write(out/'manifest.json',entries);write(out/'validation.json',dict(passed=True,part=name,exe_sha256=sha(R/'ra2/build-original-c/ra2.exe'),scenes=values,scene_count=len(values),frames=sum(x['frames'] for x in values),probes=probes,files=len(entries)))
 print('Saved '+name+' checkpoint',flush=True)
def native_group(name,phases,tag):
 old=[tag+'-'+name+('' if phase is None else '-'+str(phase))+'.json' for phase in phases]
 if all((S/n).exists() for n in old):
  assert all(read(S/n)['passed'] and read(S/n)['probe_exe_sha256']==sha(S/(name+'_probe.exe')) for n in old);return old
 build_probe(name,'build-'+tag+'-'+name)
 receipts=[]
 for phase in phases:
  label=tag+'-'+name+('' if phase is None else '-'+str(phase))
  args=[S/(name+'_probe.exe'),R/'ra2/game/game.exe']+([] if phase is None else [str(phase)])
  log=run(args,label);x=read(log);assert x['passed']
  case_keys={'advance':['advance_cases'],'continuation':['continuation_cases'],'prepare':['entry_cases','retry_cases','cycle_cases'],'obstacle':['failed_rebuild_cases','rebuilt_cases'],'recovery':['failure_budget_cases','shared_finish_cases'],'wait':['fragment_cases'],'reaction':['reaction_cases']}
  cases=sum(x[k] for k in case_keys[name])
  assert cases>=65536,(name,x)
  write(S/(label+'.json'),dict(**x,validated_cases=cases,probe_exe_sha256=sha(S/(name+'_probe.exe')),original_sha256=sha(R/'ra2/game/game.exe'),production_sources_at_validation=[dict(path=p.relative_to(R).as_posix(),sha256=sha(p)) for p in (R/'ra2/src/gameplay').glob('*.c')])) ;receipts.append(label+'.json')
 return receipts

def part(name,resume):
 if name=='advance' and not resume:
  run(py('integrate_transitions_v42.py','advance'),'integrate-advance');run(['pwsh','-NoProfile','-File',R/'build-faithful.ps1'],'build-advance')
 receipts=[]
 families=[('obstacle',[None]),('reaction',[0,1,2,3]),('recovery',[None])] if name=='prepare' else [('wait',[0,1,2]),('continuation',[None]),('prepare',[None]),('advance',[None])]
 for n,phases in families:receipts+=native_group(n,phases,'part-'+name)
 jobs=[(name+'-default',py('run_skirmish_v42.py','--tag',name+'-default','--range','0:300'))]
 jobs += [fixture_job(name+'-cross-'+x['name'],x) for x in read(S/'bridge-cross-release-fixtures.json')['fixtures']]
 values=scenes(jobs);assert sum(x['frames'] for x in values)==1303;snapshot(name,values,receipts)
 if name=='advance':
  all_receipts=read(S/'parts/prepare/validation.json')['probes']+receipts
  total=sum(read(S/n)['validated_cases'] for n in all_receipts)
  write(S/'native-gates.json',dict(passed=True,groups=total//65536,cases=total,receipts=all_receipts,scope='Affected obstacle, reaction, recovery, clearance/traffic wait, combined Prepare, Advance continuation and sampled-cell effects. Each receipt identifies its independently built probe.'))

def final_scenes():
 jobs=[]
 for x in read(S/'representative-acceptance-fixtures.json')['fixtures']:
  tag,args=fixture_job(x['name'],x,x['last']);jobs.append((tag,args+(['--cell-catalog'] if x['name'].startswith('bridge-') else [])))
 for x in read(S/'collision-acceptance-fixtures.json')['fixtures']:
  if 'control' not in x['name']:jobs.append(fixture_job('contact-'+x['name'],x))
 for tag,filename,goal in [('curve-up','tube-curved-elevated-east.MAP',80),('curve-tall-down','tube-curved-tall-west.MAP',66)]:
  jobs.append(fixture_job(tag,dict(path=(S/'fixtures'/filename).relative_to(R).as_posix(),orders=[f'5:1022581:2:{goal}:114']),600))
 x=dict(path=(S/'fixtures/dynamic-far-base.MAP').relative_to(R).as_posix(),orders=['5:1022579:2:100:114']+[f'{f}:1022579:2:100:114' for f in range(450,1111,60)]);tag,args=fixture_job('repeat-failure',x,1250);jobs.append((tag,args+['--unit-ring','398:1022579:2']))
 values=scenes(jobs)
 write(S/'final-scene-matrix.json',dict(passed=True,results=values,production_scenes=len(values),production_frames=sum(x['frames'] for x in values),observer_scenes=0,scope='Finite representative other-locomotor, building/terrain, bridge-destruction and occupied-exit/collision/failure/height regression; ordinary scene evidence separated from diagnostic unit-ring and inherited observer evidence.'))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('action',choices=['prepare','advance','final-scenes']);ap.add_argument('--resume',action='store_true');a=ap.parse_args()
 if a.action=='final-scenes':final_scenes()
 else:part(a.action,a.resume)
