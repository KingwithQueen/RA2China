"""Bounded generation-38 verification. Serial builders; at most two original/C scene lanes."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import argparse,hashlib,json,os,shutil,subprocess,sys
R=Path(__file__).resolve().parent;P=R.parent.parent;S=R/'evidence/movement-state-v39';O=R/'evidence/movement-state-v38'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,x):
 assert not p.exists(),p
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def run(args,name):
 print('Starting '+name,flush=True)
 log=S/(name+'.log');assert not log.exists(),log
 with log.open('x',encoding='utf-8') as f:q=subprocess.run([str(x) for x in args],cwd=R,stdout=f,stderr=subprocess.STDOUT,env=dict(os.environ,PYTHONIOENCODING='utf-8'))
 if q.returncode:
  print(log.read_text(encoding='utf-8',errors='replace')[-7000:],flush=True);raise RuntimeError(name)
 return log
def py(name,*args):return [sys.executable,'-X','utf8','-B',R/name,*args]
def setup():
 guide=R/'ra2/src/gameplay/阅读说明-单位移动.txt';dest=S/'baseline'/guide.relative_to(R);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(guide,dest)
 items=read(S/'bridge-neighbor-release-fixtures.json')['fixtures']
 for i,x in enumerate(items):
  source=R/x['path'];dest=S/'fixtures'/('bridge-cross-release-'+x['name']+'.MAP');shutil.copy2(source,dest)
  before=x['release_frame'];after=300+16*i
  x.update(source=source.relative_to(R).as_posix(),path=dest.relative_to(R).as_posix(),sha256=sha(dest),release_frame=after)
  x['orders']=[str(after)+s[len(str(before)):] if s.startswith(str(before)+':') else s for s in x['orders']]
  x['release_frames'][str(x['blocker_id'])]=after
 write(S/'bridge-cross-release-fixtures.json',dict(passed=True,fixtures=items,scope='Ordinary map and orders; main exit release during the main vehicle route, following earlier neighboring-lane traffic. Actual movements are measured separately.'))
 p=R/'audit_internal_alias_sources_v39.py';t=p.read_text(encoding='utf-8').replace('baseline/extra/internal-alias-sources.json','baseline/parent/internal-alias-sources.json')
 t=t.replace("'004A2586'}","'004A2586','004A2326','004A24A2','004A2528','004A2590'}")
 p.write_text(t,encoding='utf-8',newline='\n')
 write(S/'verification-plan.json',dict(passed=True,parent_commit=read(S/'vcs-context.json')['parent_commit'],policy='Overall functional, effect, rules and resource conformance; finite representative per-frame comparisons, not mandatory bug-for-bug replication.',part_scenes=3,part_frames=1303,affected_native_groups=41,new_native_groups=5,cases_per_group=65536,max_scene_lanes=2,max_game_processes=4,serial_builders=True,unaffected_history='Reuse accepted v38 evidence, without claiming it was rerun.',natural_aliases='29 bounded source and ordinary-runtime observations; unobserved indirect entrances stay open, not a release blocker.'))
 print('Setup complete',flush=True)
def fixture_job(tag,item,last=500,runner='run_fixture_comparison.py'):
 args=py(runner,'--tag',tag,'--evidence-stage','movement-state-v39','--movement-audit','--seconds','240','--range','0:'+str(last),'--scenario-map',R/item['path'])
 for order in item.get('orders',[]):args+=['--order',order]
 return (tag,args)
def scenes(jobs):
 def one(job):
  tag,args=job;run(args,'scene-'+tag);x=read(S/'runs'/tag/'comparison.json');c=x['comparison']
  assert x['passed'] and c['equal_frames']==c['frames_compared'] and c['rng_equal_all_frames']
  return dict(tag=tag,frames=c['frames_compared'],exe_sha256=x['exe_sha256'],comparison_sha256=sha(S/'runs'/tag/'comparison.json'))
 with ThreadPoolExecutor(max_workers=2) as pool:values=list(pool.map(one,jobs))
 return values
def probe(exe,phase,name):
 log=run([S/(exe+'_probe.exe'),R/'ra2/game/game.exe',phase],name)
 x=read(log);assert x['passed'] and x.get('cases',x.get('object_cases'))==65536
 write(S/(name+'.json'),dict(**x,probe_exe_sha256=sha(S/(exe+'_probe.exe')),original_sha256=sha(R/'ra2/game/game.exe')))
 return name+'.json'
def snapshot(part,values,probes):
 out=S/'parts'/part;assert not out.exists()
 receipt=read(R/'ra2/build-original-c/source-content-receipt.json');assert len(receipt['inputs'])==292
 paths={Path(p).relative_to(R).as_posix() for p in receipt['inputs']};paths.add('ra2/build-original-c/ra2.exe')
 paths.update(p.relative_to(R).as_posix() for p in S.iterdir() if p.is_file() and p.name in ['overlap_probe.c','objects_probe.c','overlap_probe.exe','objects_probe.exe','bridge-cross-release-fixtures.json','verification-plan.json'])
 paths.update(p.relative_to(R).as_posix() for p in (S/'pending').glob('*.json'))
 paths.update(p.relative_to(R).as_posix() for p in R.glob('*v39*') if p.is_file())
 paths.update((S/name).relative_to(R).as_posix() for name in probes)
 for x in read(S/'bridge-cross-release-fixtures.json')['fixtures']:paths.add(x['path'])
 manifest=[]
 for rel in sorted(paths):
  dest=out/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/rel,dest);manifest.append(dict(path=rel,sha256=sha(dest)))
 write(out/'manifest.json',manifest)
 write(out/'validation.json',dict(passed=True,part=part,exe_sha256=sha(R/'ra2/build-original-c/ra2.exe'),scenes=values,scene_count=len(values),frames=sum(x['frames'] for x in values),probes=probes,files=len(manifest)))
 print('Saved '+part+' checkpoint',flush=True)
def part(name,resume=False):
 kind='objects' if name=='passage' else name
 ext='service' if name=='returns' else kind
 exe='objects' if name=='passage' else 'overlap'
 if not resume:
  run(py('integrate_'+kind+'_v39.py'),'integrate-'+name)
  run(py('extend_'+ext+'_probe_v39.py'),'extend-'+name)
  run(['pwsh','-NoProfile','-File',R/'build-faithful.ps1'],'build-'+name)
  run(['pwsh','-NoProfile','-File',R/('build-'+exe+'-probe-v39.ps1')],'build-probe-'+name)
 phases={'template':[23,24,25],'passage':[13],'returns':[26]}[name]
 probes=[probe(exe,p,'part-'+name+'-native-'+str(p)) for p in phases]
 jobs=[(name+'-default',py('run_skirmish_v39.py','--tag',name+'-default','--range','0:300'))]
 jobs += [fixture_job(name+'-cross-'+x['name'],x) for x in read(S/'bridge-cross-release-fixtures.json')['fixtures']]
 values=scenes(jobs);assert sum(x['frames'] for x in values)==1303;snapshot(name,values,probes)
def native():
 values=[]
 for exe,count in [('overlap',27),('objects',14)]:
  run(['pwsh','-NoProfile','-File',R/('build-'+exe+'-probe-v39.ps1')],'final-build-'+exe)
  for p in range(count):values.append(probe(exe,p,'final-native-'+exe+'-'+str(p)))
 write(S/'native-gates.json',dict(passed=True,groups=len(values),cases=41*65536,new_groups=5,new_cases=5*65536,receipts=values,inherited_unaffected=dict(parent='evidence/movement-state-v38/native-gates.json',sha256=sha(O/'native-gates.json'),scope='Prior complete 126-group matrix; only the affected overlap and object families were rerun here.')))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('action',choices=['setup','template','passage','returns','native']);ap.add_argument('--resume',action='store_true');a=ap.parse_args()
 if a.action=='setup':setup()
 elif a.action=='native':native()
 else:part(a.action,a.resume)
