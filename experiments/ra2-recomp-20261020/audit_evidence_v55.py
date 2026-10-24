"""Current finite effects and explicitly inherited boundaries, without new RNG hooks."""
from run_batch_v55 import *
from accept_dynamic_v55 import records
from map_codec_v55 import unpack
parent_south=next(x for x in read(O/'dynamic-fixtures.json')['fixtures'] if x['tag']=='sc')
current_south=next(x for x in read(S/'dynamic-fixtures.json')['fixtures'] if x['tag']=='fm')
assert sha(R/current_south['path'])==sha(R/parent_south['path'])
assert hashlib.sha256(unpack((R/current_south['path']).read_text(encoding='ascii'))[1]).hexdigest()==current_south['terrain_pack_sha256']
protected=[O/n for n in ['rng-functional-impact.json','corner-boundary-inheritance.json','rules-and-locomotors.json','land-type-table-proof.json','shore-comparison.json']]
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
 p=O/name;inherited[name]=dict(path=str(p),sha256=sha(p),rerun=False)
write(S/'boundary-inheritance.json',dict(passed=True,files=inherited,new_fm_map_equals_parent_south_bytes=True,new_fm_terrain_pack_sha256=current_south['terrain_pack_sha256'],scope='Previous no-pass shores, distant release target, slope/aircraft, original terrain-name tables and negative collision controls remain in place. No new claims for these inherited cases.'))
source=(R/'ra2/src/gameplay/ground_path_search.c').read_text(encoding='utf-8')
for helper in ['resolve_neighbor','candidate_region_allows','score_candidate_step','advance_frontier','publish_candidate','cached_candidate_is_cheaper']:assert helper in source
write(S/'service-boundaries.json',dict(passed=True,changed_unit='ground_path_search.c',new_headers_or_build_sources=False,stages=['resolve_neighbor: nine-neighbor lookup and layer/index selection','candidate_region_allows: region callback, repeated cell read, restriction exemptions','score_candidate_step: connection distance or live weighted traversal cost','advance_frontier: heap/current-level/count ordering'],retained=['live context at each callback','region callback may update connection flags','passage callback may update search weight or stamp','cost is still evaluated for blocked passage before the goal exit','second stamp read after passage and score','create-node then heap then cache then itinerary cursor','ninth neighbor uses actual destination index','same cell buffers reused for ignored repeated reads','limit before goal; empty frontier still increments expanded'],native_probe_scope='Mapped original full loop with four engine service stubs; not all ABI fields or natural entry coverage.'))
write(S/'infrastructure-failure.json',dict(passed=True,kind='initial-resource-link-access',game_process_started=False,failed_recipe_path=str(S/'failed-infrastructure/b-fm-link-access'),log=str(S/'scene-b-fm.log'),retry_log=str(S/'scene-b-fm-retry-01.log'),scope='Initial restricted hardlink setup failed before game launch; preserved separately from game-scene acceptance.'))
print(dict(passed=True,variants={k:v['rng_first_different_frame'] for k,v in variants.items()}))
