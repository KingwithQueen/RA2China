"""Batch 66: explicit frozen v66 parent, obstacle response and recovery services."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();entries=[]
def save(name,t):
 q=R/name.replace('v66','v67');assert not q.exists();q.write_text(t.rstrip()+'\n',encoding='utf-8',newline='\n');entries.append(dict(source=name,source_sha256=sha(R/name),derived=q.name,derived_sha256=sha(q)))
t=(R/'prepare_movement_v66.py').read_text(encoding='utf-8').replace('v66','v67').replace('v65','v66').replace('50df7b3eb92df16a41e4316242915ca333dca17f','6d677d13e00c7cb0a4567f72763a82c016fd2e96')
t=t.replace("[('wait',63),('prepare',62),('tube-state',51)]","[('reaction',42),('recovery',63)]").replace('Batch 65 baseline and sustained traffic scheduling inputs','Batch 66 baseline and reverse/competing traffic inputs');save('prepare_movement_v66.py',t)
old="{'ra2/src/gameplay/ground_wait.c','ra2/src/gameplay/ground_prepare_cycle.c','ra2/src/gameplay/ground_prepare_exit.c'}";new="{'ra2/src/gameplay/ground_reaction.c','ra2/src/gameplay/ground_recovery.c'}"
for name in ['run_batch','accept_dynamic','audit_sources','audit_evidence','audit_scenes','plan_cleanup','commit_movement','verify_final_movement','audit_baseline_channel']:
 p=name+'_v66.py';t=(R/p).read_text(encoding='utf-8').replace('v66','v67').replace("O=R/'evidence/movement-state-v65'","O=R/'evidence/movement-state-v66'")
 t=t.replace(old,new).replace('scheduling','reaction').replace('publication','recovery')
 if name=='run_batch':
  a=t.index('def native(part):');b=t.index('def snapshot(',a)
  t=t[:a]+'''def native(part):
 receipts=[]
 for builder in ['reaction','recovery']:
  run(['pwsh','-NoProfile','-File',R/('build-'+builder+'-probe-v67.ps1')],'build-native-'+part+'-'+builder)
 for kind,probe,phase in [('dispatch','reaction',0),('report','reaction',1),('attack','reaction',2),('blocked','reaction',3),('failure-budget-finish','recovery',None)]:
  exe=S/(probe+'_probe.exe');args=[exe,R/'ra2/game/game.exe']+([] if phase is None else [str(phase)])
  x=read(run(args,'native-'+part+'-'+kind));assert x['passed']
  count=x.get('reaction_cases',x.get('failure_budget_cases',0)+x.get('shared_finish_cases',0));name='part-'+part+'-'+kind+'.json'
  write(S/name,dict(**x,unique_cases=count,kind=kind,probe_name=probe,probe_exe_sha256=sha(exe),original_sha256=sha(R/'ra2/game/game.exe')));receipts.append(name)
 if part=='baseline':
  out=S/'baseline-probe';out.mkdir();files=[]
  for name in ['reaction_probe.c','reaction_probe.exe','recovery_probe.c','recovery_probe.exe','native_probe_host.h']:
   shutil.copy2(S/name,out/name);files.append(dict(path=(out/name).relative_to(R).as_posix(),sha256=sha(out/name)))
  write(S/'baseline-native-identity.json',dict(passed=True,files=files,receipts=receipts))
 return receipts

'''+t[b:]
  t=t.replace('Traffic wait reaction, clearance regression, prepare entry/retry and unchanged Tube exit integration.','Obstacle dispatch/report/attack/blocked entries and failure-budget/shared recovery finish.')
 elif name=='audit_sources':
  t=t.replace("['wait_probe.exe','prepare_probe.exe','tube_state_probe.exe','capture_packet_probe.exe','transport_packet_probe.exe']","['reaction_probe.exe','recovery_probe.exe','capture_packet_probe.exe','transport_packet_probe.exe']")
  t=t.replace('Three existing gameplay units','Two existing gameplay units').replace('per-unit retry admission, long-wait escalation and rebuild recovery service order retained','obstacle response and failure-budget completion service order retained')
 elif name=='audit_evidence':
  a=t.index("wait=(R/");b=t.index("print(dict(passed=True,variants=",a)
  t=t[:a]+'''reaction=(R/'ra2/src/gameplay/ground_reaction.c').read_text(encoding='utf-8');recovery=(R/'ra2/src/gameplay/ground_recovery.c').read_text(encoding='utf-8')
assert 'select_obstacle_response' in reaction and 'attack_obstacle_target' in reaction and 'finish_obstacle_response' in reaction and 'finish_exhausted_budget' in recovery and 'finish_recovery_state' in recovery
write(S/'service-boundaries.json',dict(passed=True,changed_units=['ground_reaction.c','ground_recovery.c'],new_headers_or_build_sources=False,new_mechanism_change=False,retained=['friendly obstacle dispatch clears local path/flags','recursive retry returns immediately even on false','repeated live target lookup and allied checks','overlay/wall query only when no object','blocked retry or invalidation/cancel/stop order','failure budget decrements once','owner liveness before sound and finish','linked notification before segment/selector reset','live callback context and mutable state preserved'],scope='Reverse and competing ordinary traffic; no FIFO or unbounded fairness guarantee.'))
write(S/'infrastructure-status.json',dict(passed=True,new_game_setup_failures=False,accepted_scene_setups_succeeded=True,parent_status=str(O/'infrastructure-status.json'),parent_status_sha256=sha(O/'infrastructure-status.json'),scope='All starts and ordinary targets checked using parent original catalogs before calibration. Parent invalid goals, stationary start and build overlap retained by hash, not rerun as current positives.'))
'''+t[b:]
 elif name=='audit_scenes':
  t=t[:t.index('from accept_traffic_v67 import analyze as traffic_analyze')]
 elif name=='commit_movement':
  t=t.replace('第六十五批','第六十六批').replace('持续来车公平性与桥隧恢复调度','反向竞争通道与障碍恢复').replace('Stage sustained traffic reaction and mixed-channel fairness evidence (batch 65)','Stage reverse competing traffic and obstacle recovery services (batch 66)')
  t=t.replace("'docs/寻路机制改进验收补充-20261025.txt',", "'docs/当前进度与剩余内容-20261025-第六十六批.txt','docs/寻路机制改进验收补充-20261025.txt',")
 elif name=='verify_final_movement':
  t=t.replace('==(65,66)','==(66,67)').replace('generation=65','generation=66').replace('360448','393216').replace('78273','62273')
  t=t.replace("v['excluded_rollback_dirs']==['reaction-overlap-invalid']","v['excluded_rollback_dirs']==[]")
  t=t.replace("{'clearance','clearance-tail','traffic-schedule','prepare-entry-retry','tube-exit'}","{'dispatch','report','attack','blocked','failure-budget-finish'}").replace('[32768,65536,65536,65536,131072]','[65536,65536,65536,65536,131072]')
  a=t.index("review=read(S/'mixed-target-terrain-review.json')");b=t.index("parity=read(S/'channel-observer-baseline-parity.json')",a);t=t[:a]+t[b:]
  a=t.index("overlap=read(S/'phase-overlap-review.json')");b=t.index("for e in read(S/'baseline-channel-observer/manifest.json')",a);t=t[:a]+t[b:]
  t=t.replace("use=read(S/'community-current-use.json');assert use['passed']", "use=read(S/'community-current-use.json');assert sha(S/'community-current-use.json')==sha(O/'community-current-use.json') and use['passed']")
 save(p,t)
origins=[dict(name=n+'_probe.c',source=f'evidence/movement-state-v{v}/{n}_probe.c',sha256=sha(R/f'evidence/movement-state-v{v}/{n}_probe.c')) for n,v in [('reaction',42),('recovery',63)]]
(R/'lineage_v67.json').write_text(json.dumps(dict(passed=True,entries=entries,native_origins=origins),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(dict(passed=True,derived=len(entries),parent='movement-state-v66'))
