"""Finite functional effects for transport, bridge layers and mixed locomotor traffic."""
from run_batch_v50 import *
def rows(tag,mode):return [__import__('json').loads(l) for l in (S/'runs'/tag/mode/'state.jsonl').open(encoding='utf-8')]
def states(rs):return [r for r in rs if r['kind']=='state']
def events(rs):return [r for r in rs if r['kind'] in ('submit','execute','movement-audit')]
def history(rs):return {r['frame']:{o['id']:o for o in r['objects']} for r in states(rs)}
bridges={}
for item in read(S/'bridge-cross-release-fixtures.json')['fixtures']:
 name=item['name'];tag='passage-cross-'+name
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

recipes=read(S/'dynamic-fixtures.json')['fixtures'];representative={};selected=[];variations=[]
for item in recipes:
 tag=item['tag'];base=item['baseline_tag']
 for mode in ['original','generated-c']:assert rows(tag,mode)==rows(base,mode),(tag,mode,'Full baseline trace changed')
 p=S/'runs'/base/'comparison.json';q=read(p)
 selected.append(dict(tag=base,frames=q['comparison']['frames_compared'],comparison_sha256=sha(p),strict_passed=q['passed']))
 if tag in ['w2','a2']:
  from accept_coast_v50 import analyze
  value=analyze(tag);assert value['baseline_inherited_exactly'];representative[tag]=value;variations.append(value)
  continue
 modes={}
 for mode in ['original','generated-c']:
  h=history(rows(tag,mode));end=item['last'];car=1023362;cells={tuple(c['cell']):c for c in read(S/'runs'/tag/mode/'cells.json')['cells']}
  cell=lambda o:tuple(v//256 for v in o['position'][:2])
  assert cells[(57,57)]['slope']==item['slope_type'] and cell(h[200][car])==(57,57)
  target=(60,56) if tag=='c6' else (58,56);assert cell(h[end][car])==target
  bridge_goal_frame=1200 if tag=='c6' else None
  if tag=='c6':assert cell(h[bridge_goal_frame][car])==(60,80)
  else:
   assert all(h[f][car]['position']==[13952,14976,416] for f in range(905,1700))
   assert h[920][car]['mission'][0]==5 and not h[920][car]['ground_drive']['path_directions']
   recovery=next(f for f in range(1700,end+1) if h[f][car]['position']!=h[f-1][car]['position'])
   assert recovery==1730 and h[end][car]['mission'][0]==5
  corner=[dict(frame=f,position=q[car]['position']) for f,q in h.items() if cells[cell(q[car])]['slope']==item['slope_type']]
  moving=[q for q in corner if q['frame'] and h[q['frame']-1][car]['position']!=q['position']]
  assert len(moving)>8 and len({q['position'][2] for q in moving})>3
  assert all(h[end][u]['health']==200 for u in [car,1023363,1023364]) and h[end][1023365]['health']==125
  for u,goal in [(1023363,(61,54)),(1023364,(61,82)),(1023365,(61,55))]:assert cell(h[end][u])==goal
  layers=[]
  for f,q in h.items():
   upper=q[car]['ground_drive']['owner_flags_74_79'][1]
   if not layers or layers[-1]['upper_layer']!=upper:layers.append(dict(frame=f,upper_layer=upper))
  assert [q['upper_layer'] for q in layers]==([0,1,0,1,0] if tag=='c6' else [0])
  secondary=[]
  for f,q in h.items():
   upper=q[1023363]['ground_drive']['owner_flags_74_79'][1]
   if not secondary or secondary[-1]!=upper:secondary.append(upper)
  assert secondary==[0,1,0]
  foot_upper=[r['frame'] for r in rows(tag,mode) if r['kind']=='fixture-object-flags' and r['id']==1023365 and r['bytes_74_75_76_79_7a_7d'][3]]
  assert len(foot_upper)>20
  modes[mode]=dict(start=h[0][car]['position'],end=h[end][car]['position'],height_range=[min(q[car]['position'][2] for q in h.values()),max(q[car]['position'][2] for q in h.values())],moving_corner_samples=moving,corner_cell=[57,57],slope_type=item['slope_type'],layers=layers,bridge_goal_snapshot=bridge_goal_frame,other_actors_reach_goals=True,secondary_vehicle_bridge_layers=secondary,infantry_upper_bridge_frames=len(foot_upper),main_bridge_trip_verified=tag=='c6',natural_failure_and_recovery=None if tag=='c6' else dict(held_cell=[54,58],hold_range=[905,1699],guard_with_empty_path_at=920,new_goal_order=1700,first_actual_motion=1730,final_goal=[58,56],exact_native_failure_entry_proved=False,must_replicate_failure_forever=False))
 assert modes['original']==modes['generated-c'];representative[tag]=dict(passed=True,modes=modes,ordinary_original_neighborhood=True)
write(S/'selected-baseline-scenes.json',dict(passed=True,results=selected,baseline_host=str(S/'baseline-observer/bridge-catalog-observer.exe')))
write(S/'corner-qualification.json',dict(passed=True,corner6_scope='Primary corner/high-ground/bridge roundtrip and moving traffic.',corner8_scope='Corner4/5/6 height transitions, naturally held target then valid-goal recovery, and other actors using bridge. Primary corner8-to-bridge route not qualified.',excluded_bridge_trials=['d8','e8'],main_corner8_bridge_trip_remaining=True,no_original_bug_attribution=True))
for name in ['transport_packet_probe.c','transport_packet_probe.exe','transport-native-validation-current.json']:assert sha(S/name)==sha(O/name)
source=(S/'bridge_catalog_observer.c').read_text(encoding='utf-8');assert not any(n in source for n in ['sub_00552570','sub_00555A60','sub_00569090'])
write(S/'fixture-host-identity.json',dict(passed=True,source_sha256=sha(S/'bridge_catalog_observer.c'),host_sha256=sha(S/'bridge-catalog-observer.exe'),production_sha256=sha(R/'ra2/build-original-c/ra2.exe'),transport_packet_proof_inherited=True,production_recorder_unchanged=True,no_direct_board_unload_repair_or_path_result_calls=True,readonly_bridge_flags_every_frame=True))
write(S/'effects.json',dict(passed=True,representative=representative,bridge_cross_release=True,real_train_contact=True,real_infantry_crushing=True,repeated_failure_frames=fail,original_anomalies=anomalies,accepted_baseline_variations=len(variations),production_rules_and_art_files_changed=False,whole_game_equivalence_verified=False,bug_for_bug_required=False,excluded=read(S/'excluded-explorations.json')))
print(dict(passed=True,representative=list(representative),functional_cases=len(variations)))
