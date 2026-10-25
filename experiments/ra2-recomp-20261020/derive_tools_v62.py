"""Current exhaustion/retry/arrival gates and distinct flat/deck channels."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v62'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();entries=[]
changed="{'ra2/src/gameplay/ground_drive.c','ra2/src/gameplay/ground_prepare.c','ra2/src/gameplay/ground_arrival.c'}"
for name in ['run_batch_v61.py','accept_dynamic_v61.py','accept_traffic_v61.py','audit_scenes_v61.py','audit_sources_v61.py','plan_cleanup_v61.py','commit_movement_v61.py','audit_evidence_v61.py','verify_final_movement_v61.py']:
 p=R/name;t=p.read_text(encoding='utf-8-sig').replace('v61','v62')
 t=t.replace("O=R/'evidence/movement-state-v60'","O=R/'evidence/movement-state-v61'")
 t=t.replace("{'ra2/src/gameplay/ground_followup.c','ra2/src/gameplay/ground_template.c'}",changed)
 t=t.replace("['consumer','queue']","['retry','arrival']").replace("parts['queue']","parts['arrival']").replace('parts/queue/','parts/arrival/')
 if name=='run_batch_v61.py':
  a=t.index('def native(part):');b=t.index('def snapshot(',a)
  t=t[:a]+'''def native(part):
 receipts=[]
 for probe in ['drive_process','prepare','arrival']:
  run(['pwsh','-NoProfile','-File',R/('build-'+probe+'-probe-v62.ps1')],'build-native-'+part+'-'+probe)
 for kind,probe,key in [('exhaustion','drive_process','native_process_fixtures'),('retry','prepare',None),('arrival','arrival','native_arrival_cases')]:
  exe=S/(probe+'_probe.exe');log=run([exe,R/'ra2/game/game.exe'],'native-'+part+'-'+kind);x=read(log);assert x['passed']
  cases=x[key] if key else x['entry_cases']+x['retry_cases']
  name='part-'+part+'-'+kind+'.json'
  write(S/name,dict(**x,kind=kind,cases=cases,probe_name=probe,probe_exe_sha256=sha(exe),original_sha256=sha(R/'ra2/game/game.exe')));receipts.append(name)
 if part=='baseline':
  out=S/'baseline-probe';out.mkdir();files=[]
  for name in ['drive_process_probe.c','drive_process_probe.exe','prepare_probe.c','prepare_probe.exe','arrival_probe.c','arrival_probe.exe','native_probe_host.h']:
   shutil.copy2(S/name,out/name);files.append(dict(path=(out/name).relative_to(R).as_posix(),sha256=sha(out/name)))
  write(S/'baseline-native-identity.json',dict(passed=True,files=files,receipts=receipts))
 return receipts

''' +t[b:]
  t=t.replace("if name=='queue':write(S/'native-gates.json'", "if name=='arrival':write(S/'native-gates.json'")
  t=t.replace("['baseline','consumer','queue','final-scenes']","['baseline','retry','arrival','final-scenes']")
  t=t.replace('Missing-next-direction result consumption and two 24-slot queue commit entries. Finite mapped original states, ordered callbacks and checked ABI/control words; no unrelated speed or template-selection phases counted.', 'Drive exhaustion and restart, preparation entry/retry, and segment arrival. Finite original state, callback order and checked ABI/control evidence; repeated runs do not add unique cases.')
 elif name=='accept_traffic_v61.py':
  t=t.replace("assert all(cells[cell(frame[u])]['land'] in [0,6,7] and frame[u]['position'][2]==0 for frame in states.values() for u in actors)", "assert all((cells[cell(frame[u])]['land'] in [0,6,7] or (recipe['channel_kind']=='deck' and cells[cell(frame[u])]['bridge'])) and frame[u]['position'][2]==recipe['expected_height'] for frame in states.values() for u in actors)")
  t=t.replace('legal_land_and_zero_height=True','legal_channel_and_height=True,expected_height=recipe[\'expected_height\']')
  t=t.replace('Two new ordinary traffic recipes on unchanged original map.', 'Two distinct ordinary traffic channels on unchanged source map bytes: flat coast and elevated deck.')
  t=t.replace('consumer/queue branch','exhaustion/retry/arrival branch')
 elif name=='audit_sources_v61.py':
  t=t.replace("['followup_probe.exe','template_probe.exe','capture_packet_probe.exe','transport_packet_probe.exe']","['drive_process_probe.exe','prepare_probe.exe','arrival_probe.exe','capture_packet_probe.exe','transport_packet_probe.exe']")
  t=t.replace('result-consumer/queue service phases','exhaustion/retry/arrival service phases').replace('candidate preparation, result checks, direction reread, 24-slot shift/keep and segment admission ordering retained','drive exhaustion restart flags, empty-queue handling, retry timer/failure order, arrival relocation and owner completion retained')
 elif name=='audit_scenes_v61.py':
  t=t.replace("'queue-cross-'","'arrival-cross-'").replace('consumer/queue','retry/arrival')
 elif name=='audit_evidence_v61.py':
  a=t.index("consumer=(R/");b=t.index("write(S/'infrastructure-status.json'",a)
  t=t[:a]+'''drive=(R/'ra2/src/gameplay/ground_drive.c').read_text(encoding='utf-8');prepare=(R/'ra2/src/gameplay/ground_prepare.c').read_text(encoding='utf-8');arrival=(R/'ra2/src/gameplay/ground_arrival.c').read_text(encoding='utf-8')
assert 'resume_exhausted_segment' in drive and 'handle_empty_queue' in drive and 'restart_and_rebuild_path' in prepare and 'publish_arrived_segment' in arrival and 'mark_reached_destination' in arrival
write(S/'service-boundaries.json',dict(passed=True,changed_units=['ground_drive.c','ground_prepare.c','ground_arrival.c'],new_headers_or_build_sources=False,new_mechanism_change=False,retained=['advance and owner checks before exhausted-segment handling','continuing=1 avoids adding speed twice; fresh segment uses 0','empty queue synchronizes target or speed and finishes without new segment','timer wrap semantics and delay/restart/rebuild ordering','failure callbacks may change owner/destination; recheck after rebuild','relocate before invalidation; reset selector/sample','target cell plus strict wrapped height tolerance','refresh and owner completion retain live callback queries'],scope='Finite original exhaustion/retry/arrival fragments and different ordinary channels. Existing bounded heap improvement inherited; no new unsupported mechanism change.'))
''' +t[b:]
  a=t.index("write(S/'heap-improvement-inheritance.json'");b=t.index("write(S/'short-traffic-inheritance.json'",a)
  t=t[:a]+"inherited=dict(previous);inherited.update(direct_parent=str(O/'heap-improvement-inheritance.json'),direct_parent_sha256=sha(O/'heap-improvement-inheritance.json'))\nwrite(S/'heap-improvement-inheritance.json',inherited)\n"+t[b:]
  t=t.replace('short-traffic-inheritance.json','prior-traffic-inheritance.json').replace('The two prior 901-frame traffic recipes remain retained; this round executes two longer 2401-frame recipes with four active command rounds.', 'Prior long coastal recipes remain retained; current round executes distinct flat-coast and elevated-deck channels with normal movement orders.')
 elif name=='commit_movement_v61.py':
  t=t.replace('第六十批','第六十一批').replace('路径消费队列衔接与长交通','队列耗尽重试到达与不同通道交通')
  t=t.replace('Stage path-result consumption and queue handoff with longer traffic (batch 60)','Stage exhausted-queue retry and arrival with distinct traffic channels (batch 61)')
 elif name=='verify_final_movement_v61.py':
  t=t.replace('==(60,61)','==(61,62)').replace('generation=60','generation=61').replace('196608','229376')
  t=t.replace("{'consumer','queue-shift','queue-keep'}","{'exhaustion','retry','arrival'}")
  t=t.replace('short-traffic-inheritance.json','prior-traffic-inheritance.json')
 q=R/name.replace('v61','v62');assert not q.exists();q.write_text(t,encoding='utf-8',newline='\n');entries.append(dict(source=name,source_sha256=sha(p),derived=q.name,derived_sha256=sha(q)))
origins=[dict(name=n+'_probe.c',source=f'evidence/movement-state-v{version}/{n}_probe.c',sha256=sha(S/(n+'_probe.c'))) for n,version in [('drive_process',46),('prepare',52),('arrival',46)]]
(S/'checker-lineage.json').write_text(json.dumps(dict(passed=True,entries=entries,native_origins=origins),indent=2)+'\n',encoding='utf-8')
print(dict(passed=True,derived=len(entries),parent='movement-state-v61'))
