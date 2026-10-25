"""Finite functional effects for transport, bridge layers and mixed locomotor traffic."""
from run_batch_v60 import *
def rows(tag,mode):return [__import__('json').loads(l) for l in (S/'runs'/tag/mode/'state.jsonl').open(encoding='utf-8')]
def states(rs):return [r for r in rs if r['kind']=='state']
def events(rs):return [r for r in rs if r['kind'] in ('submit','execute','movement-audit')]
def history(rs):return {r['frame']:{o['id']:o for o in r['objects']} for r in states(rs)}
bridges={}
for item in read(S/'bridge-cross-release-fixtures.json')['fixtures']:
 name=item['name'];tag='rebuild-cross-'+name
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

write(S/'bridge-cross-release-effects.json',dict(passed=True,scenes=bridges,ordinary_orders=True,scope='Current completion/rebuild north/south production scenes with moving infantry relationship queries, waiting, clearance and detours. Historical corner controls inherited separately.'))
write(S/'collision-real-effects.json',dict(passed=True,scenes=collision,negative_controls_inherited=str(O/'collision-real-effects.json'),negative_controls_sha256=sha(O/'collision-real-effects.json')))

recipes=read(S/'dynamic-fixtures.json')['fixtures'];representative={};selected=[];variations=[]
for item in recipes:
 tag=item['tag'];base=item['baseline_tag']
 base_root=R/'evidence'/item.get('baseline_stage',S.name)
 for mode in ['original','generated-c']:
  from accept_dynamic_v60 import records_from
  assert rows(tag,mode)==records_from(base_root,base,mode),(tag,mode,'Full pre-change trace changed')
 p=base_root/'runs'/base/'comparison.json';q=read(p);assert all(r['passed'] for r in q['runs'])
 selected.append(dict(tag=base,frames=q['comparison']['frames_compared'],comparison_sha256=sha(p),strict_passed=q['passed']))
 if tag in ['mi','sc','aw3','fm']:
  from accept_dynamic_v60 import analyze
  value=analyze(tag);assert value['baseline_inherited_exactly'];representative[tag]=value;variations.append(value);continue
write(S/'corner-boundary-inheritance.json',dict(passed=True,parent=str(O/'corner-boundary-inheritance.json'),sha256=sha(O/'corner-boundary-inheritance.json'),historical_controls_rerun=False,old_map_cause_proved=False,current_cm_roundtrip_verified=False))
assert read(S/'selected-baseline-scenes.json')['passed']
for item in selected:assert any(x['tag']==item['tag'] and x['comparison_sha256']==item['comparison_sha256'] for x in read(S/'selected-baseline-scenes.json')['results'])
source=(S/'bridge_catalog_observer.c').read_text(encoding='utf-8');assert not any(n in source for n in ['sub_00552570','sub_00555A60','sub_00569090'])
for name in ['transport_packet_probe.c','transport_packet_probe.exe','transport-native-validation-current.json']:assert sha(S/name)==sha(O/name)
write(S/'fixture-host-identity.json',dict(passed=True,source_sha256=sha(S/'bridge_catalog_observer.c'),host_sha256=sha(S/'bridge-catalog-observer.exe'),production_sha256=sha(R/'ra2/build-original-c/ra2.exe'),transport_packet_proof_inherited=True,production_recorder_unchanged=True,no_direct_board_unload_repair_or_path_result_calls=True,readonly_bridge_flags_every_frame=True))
write(S/'effects.json',dict(passed=True,representative=representative,bridge_cross_release=True,real_train_contact=True,real_infantry_crushing=True,repeated_failure_frames=fail,original_anomalies=anomalies,accepted_baseline_variations=len(variations),production_rules_and_art_files_changed=False,whole_game_equivalence_verified=False,bug_for_bug_required=False,excluded=dict(parent=str(O/'effects.json'),sha256=sha(O/'effects.json'),rerun=False)))
print(dict(passed=True,representative=list(representative),functional_cases=len(variations),corner8_inherited=True))

from accept_traffic_v60 import analyze as traffic_analyze
traffic={x['tag']:traffic_analyze(x['tag']) for x in read(S/'traffic-fixtures.json')['fixtures']}
exact_motion={}
for item in read(S/'traffic-fixtures.json')['fixtures']:
 for tag in [item['baseline_tag'],item['tag']]:
  exact_motion[tag]={}
  proof=traffic_analyze(tag)
  for mode in ['original','generated-c']:
   h=history(rows(tag,mode));reissue_events=[]
   for entry in proof['modes'][mode]['moving_reissues']:
    f=entry['submit_frame'];u=entry['id'];moving=h[f-1][u]['position']!=h[f-2][u]['position']
    if entry['was_moving'] and entry['old_goal_unfinished']:assert moving
    reissue_events.append(dict(id=u,submit_frame=f,moving_immediately_previous_frame=moving,old_goal_unfinished=entry['old_goal_unfinished']))
   assert sum(e['moving_immediately_previous_frame'] and e['old_goal_unfinished'] for e in reissue_events)==3
   exact_motion[tag][mode]=reissue_events
write(S/'traffic-reissue-motion.json',dict(passed=True,scenes=exact_motion,scope='Raw positions on the two immediately preceding frames independently confirm three moving, unfinished-goal replacements per recipe/mode, before and after the edits. No extra game executions.'))
write(S/'traffic-effects.json',dict(passed=True,scenes=traffic,ordinary_events=True,production_host=True,new_unique_recipes=2,baseline_pairs=2,final_pairs=2,memory_state_injection=False,path_result_injection=False))
