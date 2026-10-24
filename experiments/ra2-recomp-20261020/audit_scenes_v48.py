"""Finite functional effects for transport, bridge layers and mixed locomotor traffic."""
from run_batch_v48 import *
def rows(tag,mode):return [__import__('json').loads(l) for l in (S/'runs'/tag/mode/'state.jsonl').open(encoding='utf-8')]
def states(rs):return [r for r in rs if r['kind']=='state']
def events(rs):return [r for r in rs if r['kind'] in ('submit','execute','movement-audit')]
def history(rs):return {r['frame']:{o['id']:o for o in r['objects']} for r in states(rs)}
bridges={}
for item in read(S/'bridge-cross-release-fixtures.json')['fixtures']:
 name=item['name'];tag='approach-cross-'+name
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
  assert rows(recipe['tag'],mode)==rows(recipe['baseline_tag'],mode),(recipe['tag'],mode,'Complete pre-change mode trace changed')
 p=S/'runs'/recipe['baseline_tag']/'comparison.json';q=read(p)
 selected.append(dict(tag=recipe['baseline_tag'],frames=q['comparison']['frames_compared'],comparison_sha256=sha(p),strict_passed=q['passed']))
write(S/'selected-baseline-scenes.json',dict(passed=True,results=selected,baseline_host=str(S/'baseline-observer/bridge-catalog-observer.exe')))
representative={}
for item in recipes[:2]:
 tag=item['tag'];per_mode={}
 for mode in ['original','generated-c']:
  rs=rows(tag,mode);h=history(rs);end=item['last'];carrier,cargo,trap,traffic,foot=range(1023362,1023367)
  flags={q['frame']:q['bytes_74_75_76_79_7a_7d'] for q in rs if q['kind']=='fixture-object-flags' and q['id']==cargo}
  board=next(f for f,v in flags.items() if not v[0] and v[2]);drop=next(f for f,v in flags.items() if f>board and v[0] and not v[2])
  bridges={q['frame']:q['bridge'] for q in rs if q['kind']=='fixture-bridge-state'};collapse=next(f for f,v in bridges.items() if v==[0,0])
  assert bridges[0]==[1,1] and bridges[end]==[0,0] and board<collapse<drop
  assert all(not flags[f][0] and flags[f][2] for f in range(board,drop))
  moving=h[collapse][carrier]['position'][:2]!=h[collapse-1][carrier]['position'][:2]
  if tag=='rd':assert moving
  trap_removed=next(f for f,v in h.items() if trap not in v);assert collapse<=trap_removed<drop
  catalog={tuple(q['cell']):q for q in read(S/'runs'/tag/mode/'cells.json')['cells']}
  landing=[v//256 for v in h[drop][cargo]['position'][:2]];land=catalog[tuple(landing)]['land'];assert land==item['expected_landing_land']
  assert [v//256 for v in h[end][cargo]['position'][:2]]==item['cargo_goal']
  assert h[end][carrier]['health']==300 and h[end][cargo]['health']==h[end][traffic]['health']==200 and h[end][foot]['health']==125
  assert [v//256 for v in h[end][foot]['position'][:2]]==[65,61]
  assert [v//256 for v in h[end][traffic]['position'][:2]]==[64,72]
  traffic_motion=next(f for f in range(1000,end+1) if h[f][traffic]['position'][:2]!=h[f-1][traffic]['position'][:2])
  per_mode[mode]=dict(board_frame=board,collapse_frame=collapse,trap_removed_frame=trap_removed,horizontally_moving_at_collapse=moving,drop_frame=drop,landing_cell=landing,landing_land=land,cargo_final=h[end][cargo]['position'],carrier_final=h[end][carrier]['position'],traffic_first_motion=traffic_motion,foot_final=h[end][foot]['position'],bridge_remains_broken=True)
 assert per_mode['original']['collapse_frame']==per_mode['generated-c']['collapse_frame'] and per_mode['original']['landing_cell']==per_mode['generated-c']['landing_cell']
 representative[tag]=dict(passed=True,modes=per_mode,normal_trigger_and_transport_events=True,carrier_not_on_breaking_bridge_deck=True,direct_collapse_damage_to_carrier_not_verified=True)
for item in recipes[2:]:
 tag=item['tag'];per_mode={}
 for mode in ['original','generated-c']:
  rs=rows(tag,mode);h=history(rs);car=1023362;end=item['last'];catalog={tuple(q['cell']):q for q in read(S/'runs'/tag/mode/'cells.json')['cells']}
  assert h[0][car]['position']==h[end][car]['position']
  assert max(abs(h[800][car]['position'][i]//256-[60,80][i]) for i in [0,1])<=1
  samples=[]
  for lo,hi in [(0,900),(900,end+1)]:
   ramp=[dict(frame=f,position=q[car]['position']) for f,q in h.items() if lo<=f<hi and 416<q[car]['position'][2]<520 and catalog[tuple(v//256 for v in q[car]['position'][:2])]['slope']==item['slope_type']]
   assert ramp
   z=[q['position'][2] for q in ramp];ascending=(tag=='ss')==(lo==0);assert z==sorted(z,reverse=not ascending)
   samples.append(dict(direction='up' if ascending else 'down',samples=ramp))
  layers=[];old=None
  for f,q in h.items():
   upper=q[car]['ground_drive']['owner_flags_74_79'][1]
   if upper!=old:layers.append(dict(frame=f,upper_layer=upper,position=q[car]['position']));old=upper
  assert [q['upper_layer'] for q in layers]==[0,1,0,1,0]
  assert min(q[car]['position'][2] for q in h.values())==416 and max(q[car]['position'][2] for q in h.values())==520
  assert all(h[end][u]['health']==200 for u in [car,1023363,1023364]) and h[end][1023365]['health']==125
  per_mode[mode]=dict(start=h[0][car]['position'],end=h[end][car]['position'],ramp_type=item['slope_type'],height_range=[416,520],ramps=samples,layers=layers)
 representative[tag]=dict(passed=True,modes=per_mode,ordinary_map_records=True,axis='north-south' if tag=='ss' else 'east-west turning into bridge road',runtime_height_or_path_injection=False)
variations=[]
for recipe in recipes:
 if not read(S/'runs'/recipe['tag']/'comparison.json')['passed']:
  from accept_transport_v48 import accept
  q=accept(recipe['tag']);assert q['baseline_inherited_exactly'];variations.append(q)
for name in ['transport_packet_probe.c','transport_packet_probe.exe','transport-native-validation-current.json']:assert sha(S/name)==sha(O/name)
source=(S/'bridge_catalog_observer.c').read_text(encoding='utf-8');assert not any(n in source for n in ['sub_00552570','sub_00555A60','sub_00569090'])
write(S/'fixture-host-identity.json',dict(passed=True,source_sha256=sha(S/'bridge_catalog_observer.c'),host_sha256=sha(S/'bridge-catalog-observer.exe'),production_sha256=sha(R/'ra2/build-original-c/ra2.exe'),transport_packet_proof_inherited=True,production_recorder_unchanged=True,no_direct_board_unload_repair_or_path_result_calls=True,readonly_bridge_flags_every_frame=True))
write(S/'effects.json',dict(passed=True,representative=representative,bridge_cross_release=True,real_train_contact=True,real_infantry_crushing=True,repeated_failure_frames=fail,original_anomalies=anomalies,accepted_baseline_variations=len(variations),production_rules_and_art_files_changed=False,whole_game_equivalence_verified=False,bug_for_bug_required=False,hover_variations=variations,excluded_prechange_rng_variant=read(S/'excluded-explorations.json')))
print(dict(passed=True,cases=list(representative),landing_lands=[representative[tag]['modes']['original']['landing_land'] for tag in ['dc','rd']],slope_samples={tag:[len(q['samples']) for q in representative[tag]['modes']['original']['ramps']] for tag in ['ss','es']}))
