"""Explicit v62 parent; current waiting/release services and finite height traffic gates."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v63'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
probes="[('wait',44),('obstacle',53),('recovery',53)]"
p=R/'prepare_movement_v62.py'
t=p.read_text(encoding='utf-8-sig').replace('v62','v63').replace('v61','v62')
t=t.replace('a58365d95d7b6c844cd8cecd58d636f2c9eec6e6','ccd7050fdf03e2d4c41770412e757264b79d1e2b').replace("[('drive_process',46),('prepare',52),('arrival',46)]",probes)
(R/'prepare_movement_v63.py').write_text(t,encoding='utf-8',newline='\n')
entries=[]
for name in ['run_batch','accept_dynamic','accept_traffic','audit_scenes','audit_sources','plan_cleanup','commit_movement','audit_evidence','verify_final_movement']:
 p=R/(name+'_v62.py');t=p.read_text(encoding='utf-8-sig').replace('v62','v63')
 t=t.replace("O=R/'evidence/movement-state-v61'","O=R/'evidence/movement-state-v62'")
 t=t.replace("{'ra2/src/gameplay/ground_drive.c','ra2/src/gameplay/ground_prepare.c','ra2/src/gameplay/ground_arrival.c'}","{'ra2/src/gameplay/ground_wait.c','ra2/src/gameplay/ground_obstacle.c'}")
 t=t.replace("['retry','arrival']","['wait','release']").replace("parts['arrival']","parts['release']").replace('parts/arrival/','parts/release/').replace("'arrival-cross-'","'release-cross-'")
 if name=='run_batch':
  a=t.index('def native(part):');b=t.index('def snapshot(',a)
  t=t[:a]+'''def native(part):
 receipts=[]
 for probe in ['wait','obstacle','recovery']:
  run(['pwsh','-NoProfile','-File',R/('build-'+probe+'-probe-v63.ps1')],'build-native-'+part+'-'+probe)
 specs=[('clearance','wait',0),('invalidate','wait',1),('wait','wait',2),('obstacle','obstacle',None),('recovery','recovery',None)]
 for kind,probe,phase in specs:
  exe=S/(probe+'_probe.exe');args=[exe,R/'ra2/game/game.exe']+([] if phase is None else [str(phase)])
  x=read(run(args,'native-'+part+'-'+kind));assert x['passed']
  cases=x['fragment_cases'] if phase is not None else sum(x[k] for k in (['failed_rebuild_cases','rebuilt_cases'] if probe=='obstacle' else ['failure_budget_cases','shared_finish_cases']))
  name='part-'+part+'-'+kind+'.json'
  write(S/name,dict(**x,kind=kind,cases=cases,probe_name=probe,probe_exe_sha256=sha(exe),original_sha256=sha(R/'ra2/game/game.exe')));receipts.append(name)
 if part=='baseline':
  out=S/'baseline-probe';out.mkdir();files=[]
  for name in ['wait_probe.c','wait_probe.exe','obstacle_probe.c','obstacle_probe.exe','recovery_probe.c','recovery_probe.exe','native_probe_host.h']:
   shutil.copy2(S/name,out/name);files.append(dict(path=(out/name).relative_to(R).as_posix(),sha256=sha(out/name)))
  write(S/'baseline-native-identity.json',dict(passed=True,files=files,receipts=receipts))
 return receipts

'''+t[b:]
  t=t.replace("if name=='arrival':write(S/'native-gates.json',dict(passed=True,groups=3", "if name=='release':write(S/'native-gates.json',dict(passed=True,groups=5")
  t=t.replace("['baseline','retry','arrival','final-scenes']","['baseline','wait','release','final-scenes']")
  t=t.replace('Drive exhaustion and restart, preparation entry/retry, and segment arrival.', 'Clearance, invalidation, traffic wait, failed/rebuilt obstacle observation and failure recovery.')
 elif name=='audit_sources':
  t=t.replace("['drive_process_probe.exe','prepare_probe.exe','arrival_probe.exe','capture_packet_probe.exe','transport_packet_probe.exe']","['wait_probe.exe','obstacle_probe.exe','recovery_probe.exe','capture_packet_probe.exe','transport_packet_probe.exe']")
  t=t.replace("native['groups']==3","native['groups']==5").replace('groups=3,new_cycle_cases','groups=5,new_cycle_cases').replace('Three existing gameplay units','Two existing gameplay units')
  t=t.replace('drive exhaustion restart flags, empty-queue handling, retry timer/failure order, arrival relocation and owner completion retained','clearance level fallback, wait timer/rebuild and released-obstacle queue handoff order retained')
 elif name=='commit_movement':
  t=t.replace('第六十一批','第六十二批').replace('队列耗尽重试到达与不同通道交通','等待障碍恢复与层高通道交通')
  t=t.replace('Stage exhausted-queue retry and arrival with distinct traffic channels (batch 61)','Stage wait and obstacle-release recovery with height-channel traffic (batch 62)')
 elif name=='verify_final_movement':
  t=t.replace('==(61,62)','==(62,63)').replace('generation=61','generation=62').replace('229376','458752').replace('28669','31069')
  t=t.replace("len(x['probes'])==3","len(x['probes'])==5").replace("{'exhaustion','retry','arrival'}","{'clearance','invalidate','wait','obstacle','recovery'}").replace("native['groups']==3","native['groups']==5")
 elif name=='audit_evidence':
  a=t.index("drive=(R/");b=t.index("write(S/'infrastructure-status.json'",a)
  t=t[:a]+'''wait=(R/'ra2/src/gameplay/ground_wait.c').read_text(encoding='utf-8');obstacle=(R/'ra2/src/gameplay/ground_obstacle.c').read_text(encoding='utf-8')
assert all(s in wait for s in ['resolve_clear_terrain','start_traffic_wait_once','rebuild_after_traffic_wait'])
assert all(s in obstacle for s in ['observe_neighbor_passage','publish_recovered_queue','finish_near_allied_blocker'])
write(S/'service-boundaries.json',dict(passed=True,changed_units=['ground_wait.c','ground_obstacle.c'],new_headers_or_build_sources=False,new_mechanism_change=False,retained=['overlay query before passage branch and repeated live level/land queries','clear-only bypass and gate-before-invalidate','wait starts only once; retry gate before long-wait mode choice','callback-mutated state/context rechecked after rebuild','captured obstacle context and second direction query after bounds','allied blocker filtering before distance/height check','bridge layer notification only when target not finished','failure budget reset before live queue-head publication'],scope='Finite original waiting, clearance, obstacle observation and unchanged recovery fragments; ordinary ramps/crossroads supplement internal probes.'))
'''+t[b:]
 q=R/(name+'_v63.py');assert not q.exists();q.write_text(t,encoding='utf-8',newline='\n');entries.append(dict(source=p.name,source_sha256=sha(p),derived=q.name,derived_sha256=sha(q)))
# Written after prepare creates the independently hashed baseline.
(R/'lineage_v63.json').write_text(json.dumps(dict(passed=True,entries=entries,native_origins=[dict(name=n+'_probe.c',source=f'evidence/movement-state-v{v}/{n}_probe.c',sha256=sha(R/f'evidence/movement-state-v{v}/{n}_probe.c')) for n,v in [('wait',44),('obstacle',53),('recovery',53)]]),indent=2)+'\n',encoding='utf-8')
print(dict(passed=True,derived=len(entries),parent='movement-state-v62'))
