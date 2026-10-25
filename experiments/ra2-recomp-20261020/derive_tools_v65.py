"""Explicit v64 parent; Tube exit/recovery services and per-vehicle queue evidence."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
p=R/'prepare_movement_v64.py';t=p.read_text(encoding='utf-8-sig').replace('v64','v65').replace('v63','v64')
t=t.replace('9b5f4e9af1219f6bfbe2f6cf90b5326130510c2a','258b6c324c638e7060fa30ed5af0b9e2f9909c64').replace("[('overlap',51),('segment',42),('travel',38)]","[('tube-state',51),('remainder',50),('progress',50)]")
t=t.replace("(probe+'_probe.c')","(probe.replace('-','_')+'_probe.c')")
t=t.replace("shutil.copy2(R/'evidence/movement-state-v51/remaining_return_cases.h',S/'remaining_return_cases.h')\n",'')
t=t.replace('Batch 63 baseline and bridge/channel inputs','Batch 64 baseline and Tube exit/recovery inputs')
(R/'prepare_movement_v65.py').write_text(t,encoding='utf-8',newline='\n')
entries=[]
for name in ['run_batch','accept_dynamic','audit_sources','audit_evidence','plan_cleanup','commit_movement','verify_final_movement']:
 p=R/(name+'_v64.py');t=p.read_text(encoding='utf-8-sig').replace('v64','v65')
 t=t.replace("O=R/'evidence/movement-state-v63'","O=R/'evidence/movement-state-v64'")
 t=t.replace("{'ra2/src/gameplay/ground_bridge_plane.c','ra2/src/gameplay/ground_segment.c','ra2/src/gameplay/ground_tube_travel.c'}","{'ra2/src/gameplay/ground_tube_state.c','ra2/src/gameplay/ground_landing.c','ra2/src/gameplay/ground_failure.c'}")
 t=t.replace("['bridge','channel']","['exit','recovery']").replace("parts['channel']","parts['recovery']").replace('parts/channel/','parts/recovery/')
 if name=='run_batch':
  a=t.index('def native(part):');b=t.index('def snapshot(',a)
  t=t[:a]+'''def native(part):
 receipts=[]
 for builder in ['tube-state','remainder','progress']:
  run(['pwsh','-NoProfile','-File',R/('build-'+builder+'-probe-v65.ps1')],'build-native-'+part+'-'+builder)
 for kind,probe,phase in [('tube-exit','tube_state',0),('tube-waypoint','tube_state',3),('connection-admission','remainder',0),('connection-retry','remainder',1),('approach','progress',0),('continuation','progress',2)]:
  exe=S/(probe+'_probe.exe');x=read(run([exe,R/'ra2/game/game.exe',str(phase)],'native-'+part+'-'+kind));assert x['passed']
  name='part-'+part+'-'+kind+'.json'
  write(S/name,dict(**x,kind=kind,probe_name=probe,probe_exe_sha256=sha(exe),original_sha256=sha(R/'ra2/game/game.exe')));receipts.append(name)
 if part=='baseline':
  out=S/'baseline-probe';out.mkdir();files=[]
  for name in ['tube_state_probe.c','tube_state_probe.exe','remainder_probe.c','remainder_probe.exe','progress_probe.c','progress_probe.exe','native_probe_host.h']:
   shutil.copy2(S/name,out/name);files.append(dict(path=(out/name).relative_to(R).as_posix(),sha256=sha(out/name)))
  write(S/'baseline-native-identity.json',dict(passed=True,files=files,receipts=receipts))
 return receipts

'''+t[b:]
  t=t.replace("if name=='channel':write(S/'native-gates.json'","if name=='recovery':write(S/'native-gates.json'")
  t=t.replace("['baseline','bridge','channel','final-scenes']","['baseline','exit','recovery','final-scenes']")
  t=t.replace('Early/late bridge layers, segment preparation, Tube entry/remainder/regular movement.','Tube exit/waypoints, connection admission/retry and unchanged approach/continuation integration.')
  t=t.replace('Two new ordinary-map traffic recipes','Two new ordinary-map bridge/Tube and larger queue recipes')
 elif name=='audit_sources':
  t=t.replace("['overlap_probe.exe','segment_probe.exe','travel_probe.exe','capture_packet_probe.exe','transport_packet_probe.exe']","['tube_state_probe.exe','remainder_probe.exe','progress_probe.exe','capture_packet_probe.exe','transport_packet_probe.exe']")
  t=t.replace('bridge level/flag rereads, segment candidate/gate/facing order and tube entry height/numeric service order retained','Tube exit snapshot/clearance/placement, connection admission and retry/stop service order retained')
 elif name=='audit_evidence':
  a=t.index("bridge=(R/");b=t.index("exploration=read(S/'current-explorations.json')",a)
  t=t[:a]+'''tube=(R/'ra2/src/gameplay/ground_tube_state.c').read_text(encoding='utf-8');landing=(R/'ra2/src/gameplay/ground_landing.c').read_text(encoding='utf-8');failure=(R/'ra2/src/gameplay/ground_failure.c').read_text(encoding='utf-8')
assert 'wait_for_occupied_exit' in tube and 'restore_exit_navigation' in tube and 'publish_connection_height' in landing and 'retry_failed_connection' in failure
write(S/'service-boundaries.json',dict(passed=True,changed_units=['ground_tube_state.c','ground_landing.c','ground_failure.c'],new_headers_or_build_sources=False,new_mechanism_change=False,retained=['snapshot complete chain before clearance callbacks','live snapshot count and repeated kind queries','blocked speed before snapshot disposal','place/enter before goal check and mission/speed/facing restoration','connection index validity after leave/clear','approach then current/target heights in live order','retry path/timer/prepare and stop/clear ordering','captured context and callback-return values preserved'],scope='Finite original exit/admission/retry fragments plus ordinary mixed channels and per-vehicle larger queue recovery.'))
'''+t[b:]
  a=t.index("exploration=read(S/'current-explorations.json')");b=t.index("print(dict(passed=True,variants=",a)
  t=t[:a]+'''write(S/'infrastructure-status.json',dict(passed=True,new_game_setup_failures=False,parent_status=str(O/'infrastructure-status.json'),parent_status_sha256=sha(O/'infrastructure-status.json'),scope='Current short-tag scene setup completed; parent startup failures and original elevated-tube anomaly retained by hash, not rerun as current positives.'))
''' +t[b:]
  t=t.replace('current round executes simultaneous upper/lower planes, 1000-frame congestion and ordinary Tube traffic.','current round executes per-vehicle mixed bridge/Tube routes and larger exit queues; prior traffic remains retained.')
 elif name=='commit_movement':
  t=t.replace('第六十三批','第六十四批').replace('桥面层切换与隧道拥堵交通','隧道出口恢复与桥隧队列交通')
  t=t.replace('Stage bridge layers and channel handoff with tube and congestion traffic (batch 63)','Stage tube exit and mixed-channel recovery with larger queues (batch 64)')
 elif name=='verify_final_movement':
  t=t.replace('==(63,64)','==(64,65)').replace('generation=63','generation=64').replace('491520','196608').replace('40673','51873')
  t=t.replace("{'early-layer','late-layer','segment','tube-entry','tube-remainder','tube-regular'}","{'tube-exit','tube-waypoint','connection-admission','connection-retry','approach','continuation'}")
  t=t.replace("v['new_traffic_recipes']==3","v['new_traffic_recipes']==2")
  a=t.index("explore=read(S/'current-explorations.json')");b=t.index("for e in read(S/'baseline-channel-observer/manifest.json')",a)
  t=t[:a]+"prior=read(S/'prior-explorations.json');assert prior['passed'] and sha(Path(prior['path']))==prior['sha256']\nassert read(S/'actor-catalog-validation.json')['passed']\n"+t[b:]
 q=R/(name+'_v65.py');assert not q.exists();q.write_text(t.rstrip()+'\n',encoding='utf-8',newline='\n');entries.append(dict(source=p.name,source_sha256=sha(p),derived=q.name,derived_sha256=sha(q)))
origins=[dict(name=n+'_probe.c',source=f'evidence/movement-state-v{v}/{n}_probe.c',sha256=sha(R/f'evidence/movement-state-v{v}/{n}_probe.c')) for n,v in [('tube_state',51),('remainder',50),('progress',50)]]
(R/'lineage_v65.json').write_text(json.dumps(dict(passed=True,entries=entries,native_origins=origins),indent=2)+'\n',encoding='utf-8')
print(dict(passed=True,derived=len(entries),parent='movement-state-v64'))
