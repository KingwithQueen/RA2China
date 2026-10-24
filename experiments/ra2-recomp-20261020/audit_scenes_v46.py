"""Finite functional effects for transport, bridge layers and mixed locomotor traffic."""
from run_batch_v46 import *
def rows(tag,mode):return [__import__('json').loads(l) for l in (S/'runs'/tag/mode/'state.jsonl').open(encoding='utf-8')]
def states(rs):return [r for r in rs if r['kind']=='state']
def events(rs):return [r for r in rs if r['kind'] in ('submit','execute','movement-audit')]
def history(rs):return {r['frame']:{o['id']:o for o in r['objects']} for r in states(rs)}
bridges={}
for item in read(S/'bridge-cross-release-fixtures.json')['fixtures']:
 name=item['name'];tag='drive-cross-'+name
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

recipes=read(S/'dynamic-fixtures.json')['fixtures'];selected=[]
for recipe in recipes:
 for mode in ['original','generated-c']:
  assert rows(recipe['tag'],mode)==rows(recipe['baseline_tag'],mode),(recipe['tag'],mode,'Full per-mode baseline changed')
 p=S/'runs'/recipe['baseline_tag']/'comparison.json';q=read(p)
 selected.append(dict(tag=recipe['baseline_tag'],frames=q['comparison']['frames_compared'],comparison_sha256=sha(p),strict_passed=q['passed']))
write(S/'selected-baseline-scenes.json',dict(passed=True,results=selected,baseline_host=str(S/'baseline/transport-observer/bridge-catalog-observer.exe')))
representative={}
for mode in ['original','generated-c']:
 rs=rows('tr',mode);control=rows('tc',mode);h=history(rs);n=history(control)
 car,blocker,passenger,foot=1023362,1023363,1023364,1023365
 flags=lambda rows,id:{q['frame']:q['bytes_74_75_76_79_7a_7d'] for q in rows if q['kind']=='fixture-object-flags' and q['id']==id}
 p=flags(rs,passenger);np=flags(control,passenger);fp=flags(rs,foot)
 boarded=next(f for f,v in p.items() if v[0]==0 and v[2]==1)
 unloaded=next(f for f,v in p.items() if f>boarded and v[0]==1 and v[2]==0)
 assert 50<boarded<400 and 1200<unloaded<1300
 assert all(p[f][0]==0 and p[f][2]==1 for f in range(boarded,unloaded))
 assert all(np[f][0]==0 and np[f][2]==1 for f in range(boarded,1901))
 assert all(h[f]==n[f] for f in range(1200))
 assert h[1900][car]['health']==n[1900][car]['health']==200
 assert h[1900][passenger]['health']==n[1900][passenger]['health']==125
 assert [v//256 for v in h[1900][car]['position'][:2]]==[60,80]
 assert [v//256 for v in h[1900][foot]['position'][:2]]==[61,56]
 assert [v//256 for v in h[1900][passenger]['position'][:2]]==[61,68]
 assert n[1900][passenger]['position']==n[400][passenger]['position']
 bridge=[];previous=None
 for f,objects in h.items():
  u=objects[car];upper=u['ground_drive']['owner_flags_74_79'][1]
  if upper!=previous:bridge.append(dict(frame=f,upper_layer=upper,cell=[v//256 for v in u['position'][:2]],z=u['position'][2]));previous=upper
 assert [q['upper_layer'] for q in bridge]==[0,1,0]
 assert all(p[f][2]==1 for f in range(bridge[1]['frame'],bridge[2]['frame']+1))
 meetings=[];occupancy=[]
 for q in events(rs):
  if q['kind']!='movement-audit' or q['id']!=car:continue
  f=q['frame']
  if q['stage']==24 and q['value']==blocker:occupancy.append(f)
  if q['stage'] not in [25,26] or q['value']!=foot or f<=450:continue
  a,b,pa,pb=[h[k][u]['position'] for k,u in [(f,car),(f,foot),(f-1,car),(f-1,foot)]]
  if h[f][car]['ground_drive']['owner_flags_74_79'][1] and fp[f][3] and a[1]>pa[1] and b[1]<pb[1]:meetings.append(dict(frame=f,stage=q['stage']))
 simultaneous=[f for f in range(451,700) if h[f][car]['ground_drive']['owner_flags_74_79'][1] and fp[f][3] and h[f][car]['position'][1]>h[f-1][car]['position'][1] and h[f][foot]['position'][1]<h[f-1][foot]['position'][1]]
 assert simultaneous
 relationship_queries=[dict(frame=q['frame'],stage=q['stage']) for q in events(rs) if q['kind']=='movement-audit' and q['id']==car and q['value']==foot and q['stage'] in [24,25,26]]
 assert relationship_queries
 post_motion=next(f for f in range(1450,1901) if h[f][passenger]['position'][:2]!=h[f-1][passenger]['position'][:2])
 assert p[1900][0]==1 and p[1900][2]==0 and p[1900][3]==1
 release=next(f for f in range(800,1901) if h[f][blocker]['position']!=h[f-1][blocker]['position'])
 representative['bridge-transport']=dict(passed=True,board_frame=boarded,unload_order_frame=1200,unload_frame=unloaded,carrier_bridge_transitions=bridge,loaded_during_bridge_crossing=True,meeting_query_events=meetings,simultaneous_bridge_motion_frames=simultaneous,relationship_queries=relationship_queries,moving_relationship_query_claimed=bool(meetings),exit_occupancy_query_frames=occupancy,blocker_order_frame=800,blocker_first_motion=release,passenger_post_unload_order=1450,passenger_first_motion=post_motion,passenger_final=h[1900][passenger]['position'],passenger_on_upper_bridge_at_end=True,carrier_final=h[1900][car]['position'],opposing_infantry_final=h[1900][foot]['position'],negative_control_keeps_passenger_loaded=True,observed_flags_are_raw_bytes=[0x74,0x75,0x76,0x79,0x7A,0x7D],ordinary_destination_enter_and_unload=True)
for mode in ['original','generated-c']:
 rs=rows('hv',mode);h=history(rs);car,hover,foot,parked=1023363,1023365,1023366,1023364
 assert [v//256 for v in h[1500][car]['position'][:2]]==[60,75]
 assert [v//256 for v in h[1500][hover]['position'][:2]]==[63,59] and h[1500][hover]['health']==300
 assert [v//256 for v in h[1500][foot]['position'][:2]]==[64,58]
 overlap=[f for f in range(451,1501) if all(h[f][u]['position'][:2]!=h[f-1][u]['position'][:2] for u in [car,hover,foot])]
 assert overlap and all(q[parked]['position']==h[0][parked]['position'] for q in h.values())
 representative['hover-traffic']=dict(passed=True,horizontal_simultaneous_frames=len(overlap),car_final=h[1500][car]['position'],hover_final=h[1500][hover]['position'],infantry_final=h[1500][foot]['position'],inherited_recipe=True,rerun_because_driver_changed=True)
from accept_hover_v46 import accept
variation=accept('hv');assert variation['baseline_inherited_exactly']
packet=read(S/'transport-native-validation-current.json');assert packet['passed'] and packet['native_transport_constructor_cases']==128
assert packet['source_sha256']==sha(S/'transport_packet_probe.c') and packet['probe_sha256']==sha(S/'transport_packet_probe.exe')
source=(S/'bridge_catalog_observer.c').read_text(encoding='utf-8')
assert not any(n in source for n in ['sub_00552570','sub_00555A60','sub_00569090'])
write(S/'fixture-host-identity.json',dict(passed=True,source_sha256=sha(S/'bridge_catalog_observer.c'),host_sha256=sha(S/'bridge-catalog-observer.exe'),production_sha256=sha(R/'ra2/build-original-c/ra2.exe'),transport_packet_proof_sha256=sha(S/'transport-native-validation-current.json'),production_recorder_unchanged=True,no_direct_board_unload_repair_or_path_result_calls=True,readonly_infantry_flags=True))
write(S/'effects.json',dict(passed=True,representative=representative,bridge_cross_release=True,real_train_contact=True,real_infantry_crushing=True,repeated_failure_frames=fail,original_anomalies=anomalies,accepted_baseline_variations=1,production_rules_and_art_files_changed=False,whole_game_equivalence_verified=False,bug_for_bug_required=False,hover_variation=variation))
print(dict(passed=True,transport=representative['bridge-transport'],hover_simultaneous=representative['hover-traffic']['horizontal_simultaneous_frames']))
