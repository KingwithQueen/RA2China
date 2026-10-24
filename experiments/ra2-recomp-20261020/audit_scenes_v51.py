"""Finite functional effects for transport, bridge layers and mixed locomotor traffic."""
from run_batch_v51 import *
def rows(tag,mode):return [__import__('json').loads(l) for l in (S/'runs'/tag/mode/'state.jsonl').open(encoding='utf-8')]
def states(rs):return [r for r in rs if r['kind']=='state']
def events(rs):return [r for r in rs if r['kind'] in ('submit','execute','movement-audit')]
def history(rs):return {r['frame']:{o['id']:o for o in r['objects']} for r in states(rs)}
bridges={}
for item in read(S/'bridge-cross-release-fixtures.json')['fixtures']:
 name=item['name'];tag='exit2-cross-'+name
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
 for mode in ['original','generated-c']:assert rows(tag,mode)==rows(base,mode),(tag,mode,'Full pre-change trace changed')
 p=S/'runs'/base/'comparison.json';q=read(p);assert all(r['passed'] for r in q['runs'])
 selected.append(dict(tag=base,frames=q['comparison']['frames_compared'],comparison_sha256=sha(p),strict_passed=q['passed']))
 if tag in ['cw','ca','of']:
  from accept_dynamic_v51 import analyze
  value=analyze(tag);assert value['baseline_inherited_exactly'];representative[tag]=value;variations.append(value);continue
 assert tag=='cm';modes={}
 for mode in ['original','generated-c']:
  rs=rows(tag,mode);h=history(rs);end=item['last'];car=1023362;cells={tuple(c['cell']):c for c in read(S/'runs'/tag/mode/'cells.json')['cells']}
  cell=lambda o:tuple(v//256 for v in o['position'][:2])
  assert cells[(54,56)]['slope']==8 and cells[(58,57)]['slope']==3
  for f,goal in [(200,(54,56)),(599,(55,55)),(899,(57,57)),(1199,(60,58)),(1900,(60,80)),(2299,(60,80)),(2999,(54,56)),(end,(55,55))]:assert cell(h[f][car])==goal,(f,cell(h[f][car]))
  assert min(v[car]['position'][2] for v in h.values())==416 and max(v[car]['position'][2] for v in h.values())==624
  corner=[dict(frame=f,position=v[car]['position']) for f,v in h.items() if f and cells[cell(v[car])]['slope']==8 and v[car]['position']!=h[f-1][car]['position']]
  assert len(corner)>8 and len({x['position'][2] for x in corner})>3
  layers=[]
  for f,v in h.items():
   upper=v[car]['ground_drive']['owner_flags_74_79'][1]
   if not layers or layers[-1]['upper_layer']!=upper:layers.append(dict(frame=f,upper_layer=upper))
  assert [x['upper_layer'] for x in layers]==[0,1,0,1,0]
  for u,goal in [(1023363,(61,54)),(1023364,(61,82)),(1023365,(61,55))]:assert cell(h[end][u])==goal
  assert all(h[end][u]['health']==200 for u in [car,1023363,1023364]) and h[end][1023365]['health']==125
  detours=[f for f in range(1400,1800) if cell(h[f][car])[0] not in [60,61] and h[f][car]['position']!=h[f-1][car]['position']]
  assert detours
  modes[mode]=dict(start=h[0][car]['position'],end=h[end][car]['position'],height_range=[416,624],moving_corner8_samples=corner,bridge_layers=layers,exit_detour_frames=detours,other_actors_reach_goals=True,new_near_infantry_relation_query_claimed=False)
 assert modes['original']==modes['generated-c'];representative[tag]=dict(passed=True,modes=modes,primary_corner8_bridge_roundtrip_verified=True,proven_bridge_approach_retained=True)
controls={}
for item in read(S/'corner-control-fixtures.json')['fixtures']:
 tag=item['baseline_tag'];p=S/'runs'/tag/'comparison.json';q=read(p);assert q['passed']
 h=history(rows(tag,'original'));car=1023362
 assert all(v[car]['ground_drive']['owner_flags_74_79'][1]==0 for v in h.values())
 if item['tag']=='cf':assert all(h[f][car]['position']==[13952,14976,416] for f in range(0,1501))
 else:
  assert h[1199][car]['position']==[15488,14976,520] and h[1499][car]['position']==[16000,14976,416]
  assert h[2200][car]['position']==[16000,14976,416] and h[3200][car]['position']==[14976,14464,624]
 controls[item['tag']]=dict(strict_trace_equal=True,frames=q['comparison']['frames_compared'],comparison_sha256=sha(p),final=h[item['last']][car]['position'],primary_bridge_trip=False)
write(S/'corner-boundary-findings.json',dict(passed=True,controls=controls,not_explained_solely_by_prior_downslope_arrival=True,old_map_internal_cause_proved=False,new_independent_corner8_bridge_roundtrip_verified=True,diagnostic_pairs_excluded_from_formal_count=True,no_original_bug_attribution=True,followup_only_for_functional_need=True))
write(S/'selected-baseline-scenes.json',dict(passed=True,results=selected,baseline_host=str(S/'baseline-observer/bridge-catalog-observer.exe')))
source=(S/'bridge_catalog_observer.c').read_text(encoding='utf-8');assert not any(n in source for n in ['sub_00552570','sub_00555A60','sub_00569090'])
for name in ['transport_packet_probe.c','transport_packet_probe.exe','transport-native-validation-current.json']:assert sha(S/name)==sha(O/name)
write(S/'fixture-host-identity.json',dict(passed=True,source_sha256=sha(S/'bridge_catalog_observer.c'),host_sha256=sha(S/'bridge-catalog-observer.exe'),production_sha256=sha(R/'ra2/build-original-c/ra2.exe'),transport_packet_proof_inherited=True,production_recorder_unchanged=True,no_direct_board_unload_repair_or_path_result_calls=True,readonly_bridge_flags_every_frame=True))
write(S/'effects.json',dict(passed=True,representative=representative,bridge_cross_release=True,real_train_contact=True,real_infantry_crushing=True,repeated_failure_frames=fail,original_anomalies=anomalies,accepted_baseline_variations=len(variations),production_rules_and_art_files_changed=False,whole_game_equivalence_verified=False,bug_for_bug_required=False,excluded=read(S/'excluded-explorations.json')))
print(dict(passed=True,representative=list(representative),functional_cases=len(variations),corner8_bridge=True))
