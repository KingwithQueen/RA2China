"""Current result consumption and direction-queue gates; longer ordinary traffic."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v61'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();entries=[]
for name in ['run_batch_v60.py','accept_dynamic_v60.py','accept_traffic_v60.py','audit_scenes_v60.py','audit_sources_v60.py','plan_cleanup_v60.py','commit_movement_v60.py','audit_evidence_v60.py','verify_final_movement_v60.py']:
 p=R/name;t=p.read_text(encoding='utf-8-sig').replace('v60','v61')
 t=t.replace("O=R/'evidence/movement-state-v59'","O=R/'evidence/movement-state-v60'")
 t=t.replace("'ground_path_completion.c','ground_path_rebuild.c'","'ground_followup.c','ground_template.c'")
 t=t.replace("{'ra2/src/gameplay/ground_path_completion.c','ra2/src/gameplay/ground_path_rebuild.c'}","{'ra2/src/gameplay/ground_followup.c','ra2/src/gameplay/ground_template.c'}")
 t=t.replace("['completion','rebuild']","['consumer','queue']").replace("parts['rebuild']","parts['queue']").replace('parts/rebuild/','parts/queue/')
 if name=='run_batch_v60.py':
  a=t.index('def native(part):');b=t.index('def snapshot(',a)
  t=t[:a]+'''def native(part):
 receipts=[]
 for probe in ['followup','template']:
  run(['pwsh','-NoProfile','-File',R/('build-'+probe+'-probe-v61.ps1')],'build-native-'+part+'-'+probe)
 for kind,probe,phase,key in [('consumer','followup',1,'followup_cases'),('queue-shift','template',1,'template_cases'),('queue-keep','template',2,'template_cases')]:
  exe=S/(probe+'_probe.exe');log=run([exe,R/'ra2/game/game.exe',phase],'native-'+part+'-'+kind);x=read(log);assert x['passed']
  name='part-'+part+'-'+kind+'.json'
  write(S/name,dict(**x,kind=kind,cases=x[key],probe_name=probe,probe_exe_sha256=sha(exe),original_sha256=sha(R/'ra2/game/game.exe')));receipts.append(name)
 if part=='baseline':
  out=S/'baseline-probe';out.mkdir();files=[]
  for name in ['followup_probe.c','followup_probe.exe','template_probe.c','template_probe.exe','native_probe_host.h']:
   shutil.copy2(S/name,out/name);files.append(dict(path=(out/name).relative_to(R).as_posix(),sha256=sha(out/name)))
  write(S/'baseline-native-identity.json',dict(passed=True,files=files,receipts=receipts))
 return receipts

''' +t[b:]
  t=t.replace("if name=='rebuild':write(S/'native-gates.json',dict(passed=True,groups=2", "if name=='queue':write(S/'native-gates.json',dict(passed=True,groups=3")
  t=t.replace("['baseline','completion','rebuild','final-scenes']","['baseline','consumer','queue','final-scenes']")
  t=t.replace('Completion callback/return/stack control and original complete path reconstruction. Exact fragment results; finite scope. Prior bounded heap improvement inherited separately.', 'Missing-next-direction result consumption and two 24-slot queue commit entries. Finite mapped original states, ordered callbacks and checked ABI/control words; no unrelated speed or template-selection phases counted.')
 elif name=='accept_traffic_v60.py':
  t=t.replace("was_moving=bool(recent),old_goal_unfinished=unfinished", "was_moving=states[f-1][u]['position']!=states[f-2][u]['position'],recent_motion_in_eight_frames=bool(recent),old_goal_unfinished=unfinished")
  a=t.index("  modes[mode]=dict(")
  t=t[:a]+'''  activity=[]
  for start,end in recipe['activity_windows']:
   multi=[f for f in range(max(1,start),end+1) if len(moving[f])>=3]
   active={str(u):sum(u in moving[f] for f in range(max(1,start),end+1)) for u in actors}
   assert len(multi)>=8 and all(n>=5 for n in active.values()),(tag,mode,'Insufficient later traffic',start,end,multi,active)
   activity.append(dict(window=[start,end],simultaneous_three_or_more_frames=len(multi),actor_moving_frames=active))
''' +t[a:]
  t=t.replace('modes[mode]=dict(goals=', 'modes[mode]=dict(activity_windows=activity,goals=')
  t=t.replace('do not prove every internal completion/rebuild branch or optimal routes','do not prove every internal consumer/queue branch or optimal routes')
 elif name=='audit_sources_v60.py':
  t=t.replace("['path_local_probe.exe','path_lifecycle_probe.exe','capture_packet_probe.exe','transport_packet_probe.exe']","['followup_probe.exe','template_probe.exe','capture_packet_probe.exe','transport_packet_probe.exe']")
  t=t.replace('completion/rebuild service phases','result-consumer/queue service phases').replace('completion gate, callback ordering, delayed obstacle restoration, metadata publication and reverse parent-chain reconstruction retained','candidate preparation, result checks, direction reread, 24-slot shift/keep and segment admission ordering retained')
  t=t.replace("native['groups']==2","native['groups']==3").replace("groups=2,new_cycle_cases=", "groups=3,new_cycle_cases=")
 elif name=='audit_scenes_v60.py':
  t=t.replace("'rebuild-cross-'","'queue-cross-'").replace('completion/rebuild','consumer/queue')
  t=t.replace("assert sum(e['moving_immediately_previous_frame'] and e['old_goal_unfinished'] for e in reissue_events)==3", "assert sum(e['moving_immediately_previous_frame'] and e['old_goal_unfinished'] for e in reissue_events)>=3")
  t=t.replace('three moving, unfinished-goal replacements per recipe/mode','at least three moving, unfinished-goal replacements per recipe/mode')
 elif name=='audit_evidence_v60.py':
  a=t.index("completion=(R/");b=t.index("write(S/'infrastructure-status.json'",a)
  t=t[:a]+'''consumer=(R/'ra2/src/gameplay/ground_followup.c').read_text(encoding='utf-8');queue=(R/'ra2/src/gameplay/ground_template.c').read_text(encoding='utf-8')
assert 'consume_followup_rebuild' in consumer and 'consume_direction_queue' in queue and 'prepare_segment_publication' in queue
write(S/'service-boundaries.json',dict(passed=True,changed_units=['ground_followup.c','ground_template.c'],new_headers_or_build_sources=False,new_mechanism_change=False,retained=['prepare candidate before reading second direction','missing -1 direction and distance <=512 choose straight fallback','train queried before rebuild','shared result check with check_success=0; success skips owner recheck','no-owner abort; rejected destination stops then still rereads direction','shift exactly 23 slots then tail -1, or preserve queue and supplied tail','cell coordinates truncate toward zero; reset sound and sample index','invalidate only a noninvalid old segment','admission callbacks then unchanged terminal/speed fallback'],scope='Finite original consumer/queue fragments and longer ordinary traffic; existing bounded heap change inherited, no new mechanism change.'))
''' +t[b:]
  a=t.index('units=[]')
  t=t[:a]+'''previous=read(O/'heap-improvement-inheritance.json');assert previous['passed']
for item in previous['files']:assert sha(Path(item['path']))==item['sha256']
for item in previous['production_units']:assert sha(R/item['path'])==item['sha256']==sha(S/'baseline'/item['path'])
write(S/'heap-improvement-inheritance.json',dict(**previous,direct_parent=str(O/'heap-improvement-inheritance.json'),direct_parent_sha256=sha(O/'heap-improvement-inheritance.json')))
write(S/'short-traffic-inheritance.json',dict(passed=True,rerun=False,parent=str(O/'traffic-effects.json'),sha256=sha(O/'traffic-effects.json'),scope='The two prior 901-frame traffic recipes remain retained; this round executes two longer 2401-frame recipes with four active command rounds.'))
'''
 elif name=='commit_movement_v60.py':
  t=t.replace('第五十九批','第六十批').replace('路径完成重建与自然交通','路径消费队列衔接与长交通')
  t=t.replace('Stage path completion and reconstruction with natural traffic (batch 59)','Stage path-result consumption and queue handoff with longer traffic (batch 60)')
 elif name=='verify_final_movement_v60.py':
  t=t.replace('==(59,60)','==(60,61)').replace('generation=59','generation=60').replace('24576','196608').replace('22669','28669')
  t=t.replace("len(x['probes'])==2 and {read(S/n)['kind'] for n in x['probes']}=={'completion','rebuild'}", "len(x['probes'])==3 and {read(S/n)['kind'] for n in x['probes']}=={'consumer','queue-shift','queue-keep'}")
  t=t.replace("{'completion':'path_local_probe.exe','rebuild':'path_lifecycle_probe.exe'}[proof['kind']]", "proof['probe_name']+'_probe.exe'")
  t=t.replace("({'completion':'path_local_probe.exe','rebuild':'path_lifecycle_probe.exe'}[q['kind']])", "(q['probe_name']+'_probe.exe')")
  t=t.replace("native['groups']==2","native['groups']==3")
  t=t.replace("for name,digest in lineage['native_origins'].items():assert sha(S/name)==digest==sha(R/'evidence/movement-state-v38'/name)", "for item in lineage['native_origins']:assert sha(S/item['name'])==item['sha256']==sha(R/item['source'])")
  t=t.replace("assert read(S/'traffic-effects.json')['passed']", "assert read(S/'traffic-effects.json')['passed']\nshort=read(S/'short-traffic-inheritance.json');assert short['passed'] and sha(Path(short['parent']))==short['sha256']")
 q=R/name.replace('v60','v61');assert not q.exists();q.write_text(t,encoding='utf-8',newline='\n');entries.append(dict(source=name,source_sha256=sha(p),derived=q.name,derived_sha256=sha(q)))
origins=[dict(name=n+'_probe.c',source=f'evidence/movement-state-v{version}/{n}_probe.c',sha256=sha(S/(n+'_probe.c'))) for n,version in [('followup',44),('template',45)]]
(S/'checker-lineage.json').write_text(json.dumps(dict(passed=True,entries=entries,native_origins=origins),indent=2)+'\n',encoding='utf-8')
print(dict(passed=True,derived=len(entries),parent='movement-state-v60'))
