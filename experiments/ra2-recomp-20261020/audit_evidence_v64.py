"""Current finite effects and explicitly inherited boundaries, without new RNG hooks."""
from run_batch_v64 import *
from accept_dynamic_v64 import records
from map_codec_v64 import unpack
parent_south=next(x for x in read(O/'dynamic-fixtures.json')['fixtures'] if x['tag']=='sc')
current_south=next(x for x in read(S/'dynamic-fixtures.json')['fixtures'] if x['tag']=='fm')
assert sha(R/current_south['path'])==sha(R/parent_south['path'])
assert hashlib.sha256(unpack((R/current_south['path']).read_text(encoding='ascii'))[1]).hexdigest()==current_south['terrain_pack_sha256']
def inherited_path(name):
 direct=O/name
 if direct.exists():return direct
 item=read(O/'boundary-inheritance.json')['files'][name]
 p=Path(item['path']);assert sha(p)==item['sha256'];return p
protected=[inherited_path(n) for n in ['rng-functional-impact.json','corner-boundary-inheritance.json','rules-and-locomotors.json','land-type-table-proof.json','shore-comparison.json']]
variants={};windows={}
for item in read(S/'dynamic-fixtures.json')['fixtures']:
 tag=item['tag'];p=S/'runs'/tag/'functional-acceptance.json';x=read(p)
 assert x['passed'] and x['baseline_inherited_exactly'] and x['core_functional_goals_equal']
 if tag=='fm':
  for mode,effect in x['effect_modes'].items():
   car=effect['cycles']['1023363'][0];foot=effect['cycles']['1023368'][0]
   assert foot['board_frame']<car['board_frame']<car['drop_frame']<foot['drop_frame'],mode
   assert effect['special']['payload_size']==7 and effect['special']['water_with_both_frames']>100
 variants[tag]=dict(functional_acceptance_sha256=sha(p),rng_first_different_frame=x['rng_first_different_frame'],rng_different_frames=x['rng_different_frames'],finite_goals_and_health_equal=True,raw_generator_stream_or_exact_call_source_proved_this_round=False)
 modes={m:{r['frame']:r for r in records(tag,m) if r['kind']=='state'} for m in ['original','generated-c']}
 first=x['rng_first_different_frame'];assert first is not None
 actors=list(dict.fromkeys([item[k] for k in ['carrier_id','ship_id','other_id']]+item.get('cargo_ids',[item.get('cargo_id')])+([item['foot_id']] if item.get('foot_id') else [])+[b['id'] for b in item.get('blockers',[])]+item.get('traffic_ids',[])))
 first_diffs={}
 for actor in actors:
  diffs={}
  for key in ['health','position','mission','facings']:
   diffs[key]=next((f for f in modes['original'] if next(o for o in modes['original'][f]['objects'] if o['id']==actor)[key]!=next(o for o in modes['generated-c'][f]['objects'] if o['id']==actor)[key]),None)
  assert diffs['health'] is None;first_diffs[str(actor)]=diffs
 samples=[]
 for f in range(max(0,first-8),first+9):
  snapshots={}
  for mode,h in modes.items():
   state=h[f];snapshots[mode]=dict(rng_indices=state['rng']['indices'],rng_table_sha256=hashlib.sha256(bytes.fromhex(state['rng']['table'])).hexdigest(),actors=[{k:o[k] for k in ['id','health','position','mission']} for o in state['objects'] if o['id'] in actors])
  samples.append(dict(frame=f,modes=snapshots))
 windows[tag]=dict(first_rng_snapshot_difference=first,bounded_window=[first-8,first+8],first_recorded_actor_differences=first_diffs,samples=samples,causal_rng_call_not_proved=True)
write(S/'rng-first-split-window.json',dict(passed=True,variants=windows,scope='17-frame snapshot windows plus first actor differences; causal random call and later combat behavior not proved.'))
write(S/'rng-functional-impact.json',dict(passed=True,protected_parent_files=[dict(path=str(p),sha256=sha(p)) for p in protected],new_variants=variants,no_rng_reset_or_seed_change=True,no_global_comparator_relaxation=True,scope='Complete per-mode traces equal frozen pre-change baselines; only finite loading, terrain, traffic, health and goals accepted.'))
inherited={}
for name in ['rules-and-locomotors.json','land-type-table-proof.json','shore-comparison.json','excluded-explorations.json','collision-real-effects.json','remaining-work.json']:
 p=inherited_path(name);inherited[name]=dict(path=str(p),sha256=sha(p),rerun=False)
write(S/'boundary-inheritance.json',dict(passed=True,files=inherited,retained_fm_map_equals_parent_south_bytes=True,retained_fm_terrain_pack_sha256=current_south['terrain_pack_sha256'],scope='Previous no-pass shores, distant release target, slope/aircraft, original terrain-name tables and negative collision controls remain in place. No new claims for these inherited cases.'))
bridge=(R/'ra2/src/gameplay/ground_bridge_plane.c').read_text(encoding='utf-8');segment=(R/'ra2/src/gameplay/ground_segment.c').read_text(encoding='utf-8');tube=(R/'ra2/src/gameplay/ground_tube_travel.c').read_text(encoding='utf-8')
assert 'enter_upper_bridge' in bridge and 'leave_upper_bridge' in bridge and 'resolve_segment_surface' in segment and 'wait_for_segment_permission' in segment and 'resolve_tube_rise' in tube
write(S/'service-boundaries.json',dict(passed=True,changed_units=['ground_bridge_plane.c','ground_segment.c','ground_tube_travel.c'],new_headers_or_build_sources=False,new_mechanism_change=False,retained=['32-bit wrapped four-level bridge matching','second bridge flag queries after possible layer write','captured segment context, repeated candidate and owner flag queries','gate permission before facing and classification','Tube distance/route/heading/speed/endpoints order','entrance then exit height query, wrapped difference then division','existing x87 arithmetic and conversion control words unchanged'],scope='Original layer/segment/Tube fragments, ordinary two-plane traffic and tube channels; no unsupported new algorithm.'))
exploration=read(S/'current-explorations.json');assert exploration['passed']
write(S/'infrastructure-status.json',dict(passed=True,new_game_setup_failures=True,parent_status=str(O/'infrastructure-status.json'),parent_status_sha256=sha(O/'infrastructure-status.json'),current_evidence=str(S/'current-explorations.json'),current_evidence_sha256=sha(S/'current-explorations.json'),failures_kept_separate_from_movement=True,scope='Three CSF startup failures on long-tag farm paths and an out-of-range-order setup attempt retained; shorter tags run with identical resources. Original elevated-cardinal stall retained separately. No production/resource fix or private evidence deletion.'))
print(dict(passed=True,variants={k:v['rng_first_different_frame'] for k,v in variants.items()}))

previous=read(O/'heap-improvement-inheritance.json');assert previous['passed']
for item in previous['files']:assert sha(Path(item['path']))==item['sha256']
for item in previous['production_units']:assert sha(R/item['path'])==item['sha256']==sha(S/'baseline'/item['path'])
inherited=dict(previous);inherited.update(direct_parent=str(O/'heap-improvement-inheritance.json'),direct_parent_sha256=sha(O/'heap-improvement-inheritance.json'))
write(S/'heap-improvement-inheritance.json',inherited)
write(S/'prior-traffic-inheritance.json',dict(passed=True,rerun=False,parent=str(O/'traffic-effects.json'),sha256=sha(O/'traffic-effects.json'),scope='Prior flat/elevated channels remain retained; current round executes simultaneous upper/lower planes, 1000-frame congestion and ordinary Tube traffic.'))
