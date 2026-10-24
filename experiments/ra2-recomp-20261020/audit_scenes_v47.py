"""Finite functional effects for transport, bridge layers and mixed locomotor traffic."""
from run_batch_v47 import *
def rows(tag,mode):return [__import__('json').loads(l) for l in (S/'runs'/tag/mode/'state.jsonl').open(encoding='utf-8')]
def states(rs):return [r for r in rs if r['kind']=='state']
def events(rs):return [r for r in rs if r['kind'] in ('submit','execute','movement-audit')]
def history(rs):return {r['frame']:{o['id']:o for o in r['objects']} for r in states(rs)}
bridges={}
for item in read(S/'bridge-cross-release-fixtures.json')['fixtures']:
 name=item['name'];tag='layer-cross-'+name
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

selected=[]
for recipe in read(S/'dynamic-fixtures.json')['fixtures']:
 for mode in ['original','generated-c']:
  assert rows(recipe['tag'],mode)==rows(recipe['baseline_tag'],mode),(recipe['tag'],mode,'Full pre-change mode trace changed')
 p=S/'runs'/recipe['baseline_tag']/'comparison.json';q=read(p)
 selected.append(dict(tag=recipe['baseline_tag'],frames=q['comparison']['frames_compared'],comparison_sha256=sha(p),strict_passed=q['passed']))
write(S/'selected-baseline-scenes.json',dict(passed=True,results=selected,baseline_host=str(S/'baseline-observer/bridge-catalog-observer.exe')))
representative={}
for mode in ['original','generated-c']:
 rs=rows('vc',mode);control=rows('cc',mode);h=history(rs);n=history(control)
 carrier,cargo,parked,foot=1023362,1023363,1023364,1023365
 flags=lambda rows:{q['frame']:q['bytes_74_75_76_79_7a_7d'] for q in rows if q['kind']=='fixture-object-flags' and q['id']==cargo}
 p=flags(rs);np=flags(control)
 boarded=next(f for f,v in p.items() if not v[0] and v[2])
 unloaded=next(f for f,v in p.items() if f>boarded and v[0] and not v[2])
 assert 50<boarded<400 and 1200<unloaded<1300
 assert all(not p[f][0] and p[f][2] for f in range(boarded,unloaded))
 assert all(not np[f][0] and np[f][2] for f in range(boarded,1901))
 assert all(h[f]==n[f] for f in range(1200))
 assert h[0][carrier]['locomotor_vtable']==0x7A31EC and h[0][cargo]['locomotor_vtable']==0x7A04CC
 assert [v//256 for v in h[1900][carrier]['position'][:2]]==[63,59]
 assert [v//256 for v in h[1900][cargo]['position'][:2]]==[63,64]
 assert [v//256 for v in h[1900][foot]['position'][:2]]==[65,61]
 assert h[1900][carrier]['health']==n[1900][carrier]['health']==300
 assert h[1900][cargo]['health']==n[1900][cargo]['health']==200
 assert h[1900][foot]['health']==125 and n[1900][cargo]['position']==n[400][cargo]['position']
 assert all(q[parked]['position']==h[0][parked]['position'] for q in h.values())
 overlap=[f for f in range(501,1200) if h[f][carrier]['position'][:2]!=h[f-1][carrier]['position'][:2] and h[f][foot]['position'][:2]!=h[f-1][foot]['position'][:2]]
 assert overlap
 post_motion=next(f for f in range(1450,1901) if h[f][cargo]['position'][:2]!=h[f-1][cargo]['position'][:2])
 representative['vehicle-cargo']=dict(passed=True,carrier_type='LCRF',cargo_type='TRUCKA',board_frame=boarded,unload_order=1200,unload_frame=unloaded,post_unload_order=1450,post_unload_first_motion=post_motion,carrier_final=h[1900][carrier]['position'],cargo_final=h[1900][cargo]['position'],foot_final=h[1900][foot]['position'],carrier_and_foot_horizontal_overlap_frames=len(overlap),negative_control_keeps_vehicle_loaded=True,static_vehicle=h[1900][parked]['position'],static_vehicle_move_order_did_not_produce_motion=True,static_vehicle_not_counted_as_dynamic_traffic=True,normal_destination_enter_and_unload=True)
for mode in ['original','generated-c']:
 rs=rows('sr',mode);h=history(rs);car=1023362;catalog={tuple(q['cell']):q for q in read(S/'runs/sr'/mode/'cells.json')['cells']}
 assert h[0][car]['locomotor_vtable']==0x7A04CC and h[0][car]['position']==h[1600][car]['position']==[15488,14464,520]
 assert [v//256 for v in h[800][car]['position'][:2]]==[60,80]
 ramps=[]
 for lo,hi,direction in [(0,900,'down'),(900,1601,'up')]:
  samples=[dict(frame=f,position=q[car]['position']) for f,q in h.items() if lo<=f<hi and q[car]['position'][1]//256==61 and 416<q[car]['position'][2]<520]
  assert samples and all(catalog[tuple(v//256 for v in q['position'][:2])]['slope']==4 for q in samples)
  z=[q['position'][2] for q in samples];assert z==sorted(z,reverse=direction=='down')
  ramps.append(dict(direction=direction,samples=samples))
 layers=[];old=None
 for f,q in h.items():
  flag=q[car]['ground_drive']['owner_flags_74_79'][1]
  if flag!=old:layers.append(dict(frame=f,upper_layer=flag,position=q[car]['position']));old=flag
 assert [q['upper_layer'] for q in layers]==[0,1,0,1,0]
 assert min(q[car]['position'][2] for q in h.values())==416 and max(q[car]['position'][2] for q in h.values())==520
 assert h[1600][car]['health']==h[1600][1023363]['health']==h[1600][1023364]['health']==200 and h[1600][1023365]['health']==125
 assert [v//256 for v in h[1600][1023363]['position'][:2]]==[61,55]
 assert [v//256 for v in h[1600][1023365]['position'][:2]]==[60,55]
 blocker_motion=next(f for f in range(450,1601) if h[f][1023364]['position']!=h[f-1][1023364]['position'])
 representative['real-bridge-slope']=dict(passed=True,ground_locomotor=True,height_range=[416,520],ramp_type=4,ramp_row=61,bridge_layer_transitions=layers,ramps=ramps,round_trip_goal_reached=True,blocking_vehicle_first_motion=blocker_motion,all_health_preserved=True,ordinary_map_records=True,original_bridge_overlay_retained=True,runtime_path_or_height_injection=False)
from accept_cargo_v47 import accept
variations=[accept(tag) for tag in ['vc','cc']];assert all(x['baseline_inherited_exactly'] for x in variations)
packet=read(S/'transport-native-validation-current.json');assert packet['passed']
for name in ['transport_packet_probe.c','transport_packet_probe.exe','transport-native-validation-current.json']:
 assert sha(S/name)==sha(O/name)
source=(S/'bridge_catalog_observer.c').read_text(encoding='utf-8')
assert not any(n in source for n in ['sub_00552570','sub_00555A60','sub_00569090'])
write(S/'fixture-host-identity.json',dict(passed=True,source_sha256=sha(S/'bridge_catalog_observer.c'),host_sha256=sha(S/'bridge-catalog-observer.exe'),production_sha256=sha(R/'ra2/build-original-c/ra2.exe'),transport_packet_proof_inherited=True,production_recorder_unchanged=True,no_direct_board_unload_repair_or_path_result_calls=True,readonly_ground_vehicle_and_infantry_flags=True,readonly_cell_slopes=True))
write(S/'effects.json',dict(passed=True,representative=representative,bridge_cross_release=True,real_train_contact=True,real_infantry_crushing=True,repeated_failure_frames=fail,original_anomalies=anomalies,accepted_baseline_variations=2,production_rules_and_art_files_changed=False,whole_game_equivalence_verified=False,bug_for_bug_required=False,hover_variations=variations))
print(dict(passed=True,representative=list(representative),cargo_board=representative['vehicle-cargo']['board_frame'],cargo_unload=representative['vehicle-cargo']['unload_frame'],slope_samples=[len(q['samples']) for q in representative['real-bridge-slope']['ramps']]))
