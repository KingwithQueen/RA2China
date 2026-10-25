"""Explicit batch 65 derivation from the frozen batch 64 tools; no production edits."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
entries=[]
def save(source,text):
 target=R/source.replace('v65','v66');assert not target.exists(),target
 target.write_text(text.rstrip()+'\n',encoding='utf-8',newline='\n')
 entries.append(dict(source=source,source_sha256=sha(R/source),derived=target.name,derived_sha256=sha(target)))

p=R/'prepare_movement_v65.py';t=p.read_text(encoding='utf-8-sig').replace('v65','v66').replace('v64','v65')
t=t.replace('258b6c324c638e7060fa30ed5af0b9e2f9909c64','50df7b3eb92df16a41e4316242915ca333dca17f')
t=t.replace("[('tube-state',51),('remainder',50),('progress',50)]","[('wait',63),('prepare',62),('tube-state',51)]")
t=t.replace('Batch 64 baseline and Tube exit/recovery inputs','Batch 65 baseline and sustained traffic scheduling inputs')
save(p.name,t)
units="{'ra2/src/gameplay/ground_wait.c','ra2/src/gameplay/ground_prepare_cycle.c','ra2/src/gameplay/ground_prepare_exit.c'}"
oldunits="{'ra2/src/gameplay/ground_tube_state.c','ra2/src/gameplay/ground_landing.c','ra2/src/gameplay/ground_failure.c'}"
for name in ['run_batch','accept_dynamic','audit_sources','audit_evidence','audit_scenes','plan_cleanup','commit_movement','verify_final_movement']:
 source=name+'_v65.py';t=(R/source).read_text(encoding='utf-8-sig').replace('v65','v66')
 t=t.replace("O=R/'evidence/movement-state-v64'","O=R/'evidence/movement-state-v65'")
 t=t.replace(oldunits,units).replace("['exit','recovery']","['scheduling','publication']").replace("parts['recovery']","parts['publication']").replace('parts/recovery/','parts/publication/')
 if name=='run_batch':
  a=t.index('def native(part):');b=t.index('def snapshot(',a)
  t=t[:a]+'''def native(part):
 receipts=[]
 for builder in ['wait','prepare','tube-state']:
  run(['pwsh','-NoProfile','-File',R/('build-'+builder+'-probe-v66.ps1')],'build-native-'+part+'-'+builder)
 for kind,probe,phase in [('clearance','wait',0),('clearance-tail','wait',1),('traffic-schedule','wait',2),('prepare-entry-retry','prepare',None),('tube-exit','tube_state',0)]:
  exe=S/(probe+'_probe.exe');args=[exe,R/'ra2/game/game.exe']+([] if phase is None else [str(phase)])
  x=read(run(args,'native-'+part+'-'+kind));assert x['passed']
  count=x.get('cases',x.get('fragment_cases',x.get('entry_cases',0)+x.get('retry_cases',0)))
  name='part-'+part+'-'+kind+'.json'
  write(S/name,dict(**x,unique_cases=count,kind=kind,probe_name=probe,probe_exe_sha256=sha(exe),original_sha256=sha(R/'ra2/game/game.exe')));receipts.append(name)
 if part=='baseline':
  out=S/'baseline-probe';out.mkdir();files=[]
  for name in ['wait_probe.c','wait_probe.exe','prepare_probe.c','prepare_probe.exe','tube_state_probe.c','tube_state_probe.exe','native_probe_host.h']:
   shutil.copy2(S/name,out/name);files.append(dict(path=(out/name).relative_to(R).as_posix(),sha256=sha(out/name)))
  write(S/'baseline-native-identity.json',dict(passed=True,files=files,receipts=receipts))
 return receipts

'''+t[b:]
  t=t.replace("if name=='recovery':write(S/'native-gates.json'","if name=='publication':write(S/'native-gates.json'")
  t=t.replace("groups=6,cases=sum(read(S/n)['cases']","groups=5,cases=sum(read(S/n)['unique_cases']")
  t=t.replace("['baseline','exit','recovery','final-scenes']","['baseline','scheduling','publication','final-scenes']")
  t=t.replace('Tube exit/waypoints, connection admission/retry and unchanged approach/continuation integration.','Traffic wait scheduling, clearance regression, prepare entry/retry and unchanged Tube exit integration.')
  t=t.replace('Two new ordinary-map bridge/Tube and larger queue recipes','Two new sustained-arrival queue and mixed bridge/Tube recipes')
 elif name=='audit_sources':
  t=t.replace("['tube_state_probe.exe','remainder_probe.exe','progress_probe.exe','capture_packet_probe.exe','transport_packet_probe.exe']","['wait_probe.exe','prepare_probe.exe','tube_state_probe.exe','capture_packet_probe.exe','transport_packet_probe.exe']")
  t=t.replace("native['groups']==6","native['groups']==5").replace('groups=6,','groups=5,')
  t=t.replace('Tube exit snapshot/clearance/placement, connection admission and retry/stop service order retained','per-unit retry admission, long-wait escalation and rebuild publication service order retained')
 elif name=='audit_evidence':
  a=t.index("tube=(R/");b=t.index("print(dict(passed=True,variants=",a)
  t=t[:a]+'''wait=(R/'ra2/src/gameplay/ground_wait.c').read_text(encoding='utf-8');cycle=(R/'ra2/src/gameplay/ground_prepare_cycle.c').read_text(encoding='utf-8');publish=(R/'ra2/src/gameplay/ground_prepare_exit.c').read_text(encoding='utf-8')
assert 'traffic_rebuild_mode' in wait and 'schedule_empty_queue_retry' in cycle and 'publish_retry_deadline' in publish
write(S/'service-boundaries.json',dict(passed=True,changed_units=['ground_wait.c','ground_prepare_cycle.c','ground_prepare_exit.c'],new_headers_or_build_sources=False,new_mechanism_change=False,retained=['waiting starts once before short retry gate','short gate before long-wait mode escalation','signed wrapped timer comparisons unchanged','retry timer then frame read only for depleted queues','post-rebuild owner and destination checks before retry publication','current frame before converted delay and timer restart','per-callback live context reads and callback-mutated state preserved'],scope='Per-unit recovery scheduling under finite sustained arrivals; no global FIFO or arbitrary-load fairness guarantee.'))
write(S/'infrastructure-status.json',dict(passed=True,new_game_setup_failures=False,parent_status=str(O/'infrastructure-status.json'),parent_status_sha256=sha(O/'infrastructure-status.json'),scope='Current ordinary-map inputs use accepted parent terrain/overlays. Prior startup and packing failures retained by hash, not counted as current traffic.'))
'''+t[b:]
  t=t.replace('current round executes per-vehicle mixed bridge/Tube routes and larger exit queues; prior traffic remains retained.','current round executes finite sustained arrivals and mixed bridge/Tube throughput; prior finite queue and failure evidence remain retained.')
 elif name=='audit_scenes':
  # Keep the established affected regression checks; replace only new traffic analysis below.
  t=t[:t.index("from accept_traffic_v66 import analyze as traffic_analyze")]
  t=t.replace("tag='recovery-cross-'","tag='publication-cross-'")
 elif name=='commit_movement':
  t=t.replace('第六十四批','第六十五批').replace('隧道出口恢复与桥隧队列交通','持续来车公平性与桥隧恢复调度')
  t=t.replace('Stage tube exit and mixed-channel recovery with larger queues (batch 64)','Stage sustained traffic scheduling and mixed-channel fairness evidence (batch 65)')
 elif name=='verify_final_movement':
  t=t.replace('==(64,65)','==(65,66)').replace('generation=64','generation=65').replace('196608','360448')
  t=t.replace("len(x['probes'])==6","len(x['probes'])==5").replace("{'tube-exit','tube-waypoint','connection-admission','connection-retry','approach','continuation'}","{'clearance','clearance-tail','traffic-schedule','prepare-entry-retry','tube-exit'}")
  t=t.replace("native['groups']==6","native['groups']==5")
  a=t.index("for key in ['mixed-recovery-effects.json'");b=t.index("for e in read(S/'baseline-channel-observer/manifest.json')",a)
  t=t[:a]+'''assert read(S/'fairness-effects.json')['passed'] and read(S/'traffic-map-provenance.json')['passed']
for e in read(S/'actor-catalog-validation.json')['catalogs']:
 proof=S/'runs'/e['tag']/'comparison.json';assert sha(proof)==e['comparison_sha256'] and read(proof)['passed']
for e in read(S/'traffic-map-provenance.json')['maps']:
 assert sha(Path(e['source']))==e['source_sha256'] and sha(R/e['path'])==e['sha256']
 assert e['only_units_and_infantry_changed']
for e in read(S/'current-explorations.json')['records']:assert sha(Path(e['path']))==e['sha256']
'''+t[b:]
 save(source,t)
origins=[dict(name=n+'_probe.c',source=f'evidence/movement-state-v{v}/{n}_probe.c',sha256=sha(R/f'evidence/movement-state-v{v}/{n}_probe.c')) for n,v in [('wait',63),('prepare',62),('tube_state',51)]]
payload=dict(passed=True,entries=entries,native_origins=origins)
(R/'lineage_v66.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(dict(passed=True,derived=len(entries),parent='movement-state-v65'))
