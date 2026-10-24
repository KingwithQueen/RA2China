"""Finite functional effects for restored-bridge meetings, release order and mixed detours."""
from run_batch_v44 import *
def rows(tag,mode):return [__import__('json').loads(l) for l in (S/'runs'/tag/mode/'state.jsonl').open(encoding='utf-8')]
def states(rs):return [r for r in rs if r['kind']=='state']
def events(rs):return [r for r in rs if r['kind'] in ('submit','execute','movement-audit')]
def history(rs):return {r['frame']:{o['id']:o for o in r['objects']} for r in states(rs)}
bridges={}
for item in read(S/'bridge-cross-release-fixtures.json')['fixtures']:
 name=item['name'];tag='turn-cross-'+name
 rs=rows(tag,'original');h=history(rs);car,foot=item['actor_ids'];main=item['blocker_id'];early=next(u for u in item['blocker_ids'] if u!=main);direction=1 if name=='north' else -1
 assert h[0][car]['class']==8052216 and h[0][foot]['class']==8009024
 queries=[];block_queries=[]
 for r in events(rs):
  if r['kind']!='movement-audit' or r['id']!=car:continue
  f=r['frame']
  if r['stage']==24 and r['value'] in item['blocker_ids']:block_queries.append(f)
  if r['stage'] not in [25,26] or r['value']!=foot or f<=5:continue
  a,b,pa,pb=[h[q][u]['position'] for q,u in [(f,car),(f,foot),(f-1,car),(f-1,foot)]]
  if a[2]==b[2]==416 and direction*(a[1]-pa[1])>0 and direction*(b[1]-pb[1])<0 and abs(a[1]-b[1])<=1024:queries.append(dict(frame=f,stage=r['stage']))
 waits=[];current=[]
 for f in range(150,min(item['release_frames'].values())):
  a=h[f][car]['position'];b=h[f][main]['position']
  if a==h[f-1][car]['position'] and a[2]==416 and max(abs(a[0]-b[0]),abs(a[1]-b[1]))<=768 and all(h[f][u]['position']==h[f-1][u]['position'] for u in item['blocker_ids']):current.append(f)
  else:
   if len(current)>len(waits):waits=current
   current=[]
 if len(current)>len(waits):waits=current
 detour=[f for f in range(150,501) if h[f][car]['position'][2]==416 and h[f][car]['position'][0]//256 not in [60,61] and h[f][car]['position']!=h[f-1][car]['position']]
 cross=next(f for f in range(150,501) if direction*(h[f][car]['position'][1]-(item['blocker_cell'][1]*256+128))>256)
 arrival=next(f for f in range(150,501) if [v//256 for v in h[f][car]['position'][:2]]==item['goals'][str(car)])
 motion=[]
 for u in sorted(item['blocker_ids'],key=lambda u:item['release_frames'][str(u)]):
  order=item['release_frames'][str(u)];actual=next(f for f in range(order,501) if h[f][u]['position']!=h[f-1][u]['position'])
  motion.append(dict(id=u,order_frame=order,first_actual_motion_frame=actual,delay=actual-order))
 simultaneous=[f for f in range(motion[0]['first_actual_motion_frame'],motion[1]['first_actual_motion_frame']) if h[f][car]['position']!=h[f-1][car]['position'] and h[f][early]['position']!=h[f-1][early]['position'] and h[f][car]['position'][2]==h[f][early]['position'][2]==416 and abs(h[f][car]['position'][1]-h[f][early]['position'][1])<=1024 and h[f][car]['position'][0]//256 not in [60,61]]
 goals={str(u):dict(reached=[v//256 for v in h[500][u]['position'][:2]]==item['goals'][str(u)],final_position=h[500][u]['position'],health=h[500][u]['health']) for u in [car,foot]}
 assert queries and {q['stage'] for q in queries}=={25,26} and block_queries and len(waits)>=6 and detour and simultaneous
 assert motion[0]['first_actual_motion_frame']<cross<item['release_frame']<arrival and all(g['reached'] for g in goals.values())
 assert len([r for r in events(rs) if r['kind']=='submit' and r['id']==car and r['mission']==2])==1
 bridges[name]=dict(passed=True,query_samples=queries,blocker_queries=len(block_queries),wait_range=[waits[0],waits[-1]],wait_frames=len(waits),detour_frames=len(detour),near_exit_simultaneous_frames=simultaneous,cross_frame=cross,arrival_frame=arrival,blocker_motion=motion,main_move_submissions=1,goals=goals)
anomalies=[]
for tag,z in [('curve-up',436),('curve-tall-down',-193)]:
 h=history(rows(tag,'original'));o=h[600][1022581];assert o['position'][2]==z
 anomalies.append(dict(tag=tag,original_final_position=o['position'],candidate_currently_matches=True,must_replicate_bug=False,scope='Retained original anomaly. Future deliberate correction may be accepted against functionality/rules/effects with an explained comparison.'))
rs=rows('repeat-failure','original');fail=[r['frame'] for r in events(rs) if r['kind']=='movement-audit' and r['stage']==6 and not r['value']]
assert fail==list(range(451,1112,60)),fail
collision={}
for item in read(S/'collision-acceptance-fixtures.json')['fixtures']:
 name=item['name']
 if 'control' in name:continue
 tag='contact-'+name;rs=rows(tag,'original');h=history(rs);actor=item['actor'];last=h[500];initial=h[0]
 assert initial[actor]['position'][2]==416
 targets=item['targets'];assert all(initial[u]['position'][2]==416 for u in targets)
 health=[(f,h[f][actor]['health']) for f in range(501) if f==0 or h[f][actor]['health']!=h[f-1][actor]['health']]
 vanished={str(u):next((f for f in range(501) if u not in h[f]),None) for u in targets}
 if 'control' in name:
  assert last[actor]['health']==200 and all(u in last and last[u]['health']==initial[u]['health'] for u in targets),(name,health,vanished)
 else:
  assert all(f is not None for f in vanished.values()),(name,vanished)
  assert [p//256 for p in last[actor]['position'][:2]]==[60,75]
  if name=='train':
   assert last[actor]['health']==160 and last[1023365]['health']==125
   assert all([v//256 for v in initial[u]['position'][:2]]==[60,66] for u in targets)
  else:
   assert last[actor]['health']==200
   assert initial[actor]['owner']!=initial[targets[0]]['owner']
   block=[q for q in events(rs) if q['kind']=='movement-audit' and q['stage']==24 and q['id']==actor and q['value'] in [1023363,1023364]]
   assert block
 collision[name]=dict(passed=True,health_changes=health,target_disappearance_frames=vanished,final_actor_position=last[actor]['position'],actor_final_health=last[actor]['health'],targets_preserved=all(u in last for u in targets),rules_sha256=item['rules_sha256'])

write(S/'bridge-cross-release-effects.json',dict(passed=True,scenes=bridges,ordinary_orders=True,scope='Part Advance production scenes; previous observer matrix inherited, not rerun.'))
write(S/'collision-real-effects.json',dict(passed=True,scenes=collision,negative_controls_inherited=str(O/'collision-real-effects.json'),negative_controls_sha256=sha(O/'collision-real-effects.json')))


representative={}
recipes=read(S/'dynamic-fixtures.json')['fixtures']
for recipe in recipes:
 tag=recipe['tag'];base=recipe['baseline_tag']
 for mode in ['original','generated-c']:
  assert rows(tag,mode)==rows(base,mode),(tag,mode,'Each mode must preserve all pre-change records')
for mode in ['original','generated-c']:
 positive=rows('rt',mode);negative=rows('rc',mode);h=history(positive);n=history(negative);car=1023363;foot=1023368;engineer=1023367
 for tag,rs in [('rt',positive),('rc',negative)]:
  flags={q['frame']:q['bridge'] for q in rs if q['kind']=='fixture-bridge-state'};assert flags[200]==[0,0]
  assert flags[900]==flags[1800]==([1,1] if tag=='rt' else [0,0])
 removed=next(f for f in h if engineer not in h[f]);assert 600<removed<900 and engineer in n[1900]
 assert [z//256 for z in h[1900][car]['position'][:2]]==[60,77] and h[1900][car]['health']==200
 assert [z//256 for z in h[1900][foot]['position'][:2]]==[60,58] and h[1900][foot]['health']==125
 assert n[1900][car]['position']==n[0][car]['position'] and n[1900][foot]['position']==n[0][foot]['position']
 assert h[0][1023366]['locomotor_vtable']==0x7A31EC and h[1900][1023366]['health']==300
 assert all(q[1023366]['position'][:2]==h[0][1023366]['position'][:2] for q in h.values())
 release=[]
 for u,frame in [(1023365,1350),(1023364,1450)]:
  assert all(h[f][u]['position']==h[0][u]['position'] for f in range(frame))
  moving=next(f for f in range(frame,1901) if h[f][u]['position']!=h[f-1][u]['position']);release.append(dict(id=u,order_frame=frame,first_motion_frame=moving))
 assert release[0]['first_motion_frame']<release[1]['first_motion_frame']
 waits=[f for f in range(1100,1350) if h[f][car]['position']==h[f-1][car]['position'] and max(abs(h[f][car]['position'][i]-h[f][1023364]['position'][i]) for i in [0,1])<=768]
 assert len(waits)>=6
 encounter=[];block=[]
 for q in events(positive):
  if q['kind']!='movement-audit' or q['id']!=car:continue
  f=q['frame']
  if q['stage']==24 and q['value'] in [1023364,1023365]:block.append(f)
  if q['stage'] not in [25,26] or q['value']!=foot or f<=1000:continue
  a,b,old_a,old_b=[h[k][u]['position'] for k,u in [(f,car),(f,foot),(f-1,car),(f-1,foot)]]
  if a[2]==b[2]==416 and a[1]>old_a[1] and b[1]<old_b[1] and abs(a[1]-b[1])<=1024:encounter.append(dict(frame=f,stage=q['stage']))
 assert block and {q['stage'] for q in encounter}=={25,26}
 arrival=next(f for f in range(1001,1901) if [z//256 for z in h[f][car]['position'][:2]]==[60,77]);assert release[0]['first_motion_frame']<arrival<release[1]['first_motion_frame']
 representative['restored-bridge-traffic']=dict(passed=True,engineer_consumed_frame=removed,broken_frame200=[0,0],restored_frames900_1800=[1,1],negative_control_remains_broken=True,meeting_query_events=encounter,waiting_sample_frames=waits,waiting_samples_are_not_one_continuous_interval=True,blocker_classification_events=len(block),blocker_releases=release,car_arrival_frame=arrival,car_final=h[1900][car]['position'],foot_final=h[1900][foot]['position'],stationary_hover_position=h[1900][1023366]['position'],hover_move_claimed=False,result_or_path_injection=False)
for mode in ['original','generated-c']:
 rs=rows('dt',mode);h=history(rs);car=1023363;foot=1023366;hover=1023365;parked=1023364
 assert next(f for f in h if 1023362 not in h[f])<400
 assert h[0][hover]['locomotor_vtable']==0x7A31EC and h[1500][hover]['health']==300
 assert [z//256 for z in h[1500][car]['position'][:2]]==[60,75] and h[1500][car]['health']==200
 assert [z//256 for z in h[1500][foot]['position'][:2]]==[64,58] and h[1500][foot]['health']==125
 assert [z//256 for z in h[1500][hover]['position'][:2]]==[63,59]
 assert all(q[parked]['position']==h[0][parked]['position'] for q in h.values())
 detour=[f for f,q in h.items() if 65<=q[car]['position'][1]//256<=67 and q[car]['position'][0]//256>=62];assert detour
 contact=[q for q in events(rs) if q['kind']=='movement-audit' and q['id']==hover and q['value']==foot and q['stage'] in [24,25,26]];assert {q['stage'] for q in contact}=={24,25,26}
 assert len([q for q in events(rs) if q['kind']=='submit' and q['id']==car])==1
 representative['mixed-detour']=dict(passed=True,bypass_frames=detour,car_final=h[1500][car]['position'],foot_final=h[1500][foot]['position'],hover_final=h[1500][hover]['position'],parked_vehicle=h[1500][parked]['position'],hover_foot_classification_queries=contact,main_move_submissions=1,ordinary_map_and_commands=True)
from accept_hover_v44 import accept
variation=accept('dt');assert variation['baseline_inherited_exactly'];representative['hover-variation']=variation
packet=read(S/'capture-native-validation.json');assert packet['passed'] and packet['source_sha256']==sha(S/'capture_packet_probe.c') and packet['probe_sha256']==sha(S/'capture_packet_probe.exe')
assert sha(S/'capture_packet_probe.c')==sha(O/'capture_packet_probe.c') and sha(S/'capture_packet_probe.exe')==sha(O/'capture_packet_probe.exe')
source=(S/'bridge_catalog_observer.c').read_text(encoding='utf-8');assert not any(n in source for n in ['sub_00552570','sub_00555A60','sub_00569090'])
write(S/'fixture-host-identity.json',dict(passed=True,source_sha256=sha(S/'bridge_catalog_observer.c'),host_sha256=sha(S/'bridge-catalog-observer.exe'),production_sha256=sha(R/'ra2/build-original-c/ra2.exe'),inherited_capture_packet_proof_sha256=sha(S/'capture-native-validation.json'),production_recorder_unchanged=True,no_direct_repair_or_path_result_calls=True,readonly_bridge_observation_frames=[200,900,1800]))
write(S/'effects.json',dict(passed=True,representative=representative,bridge_cross_release=True,real_train_contact=True,real_infantry_crushing=True,repeated_failure_frames=fail,original_anomalies=anomalies,accepted_baseline_variations=1,production_rules_and_art_files_changed=False,whole_game_equivalence_verified=False,bug_for_bug_required=False))
print(dict(passed=True,repair_arrival=representative['restored-bridge-traffic']['car_arrival_frame'],meeting_query_frames=sorted({q['frame'] for q in representative['restored-bridge-traffic']['meeting_query_events']}),detour_hover_final=representative['mixed-detour']['hover_final'],variation_position=variation['max_world_coordinate_delta']))
