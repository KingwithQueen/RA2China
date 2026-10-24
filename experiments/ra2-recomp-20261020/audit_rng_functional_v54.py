"""Bounded occupied-shore/capacity/traffic effects without new RNG hooks."""
from run_batch_v54 import *
protected=[O/'rng-functional-impact.json',O/'corner-boundary-inheritance.json',O/'rules-and-locomotors.json'];new={}
windows={}
for tag in ['mi','sc','aw3']:
 p=S/'runs'/tag/'functional-acceptance.json';x=read(p)
 assert x['passed'] and x['baseline_inherited_exactly'] and x['core_functional_goals_equal'] and x['strict_failure_preserved']
 new[tag]=dict(functional_acceptance_sha256=sha(p),rng_first_different_frame=x['rng_first_different_frame'],rng_different_frames=x['rng_different_frames'],finite_goals_and_health_equal=True,raw_generator_stream_or_exact_call_source_proved_this_round=False)
 from accept_dynamic_v54 import records
 modes={m:{r['frame']:r for r in records(tag,m) if r['kind']=='state'} for m in ['original','generated-c']}
 first=x['rng_first_different_frame'];recipe=next(r for r in read(S/'dynamic-fixtures.json')['fixtures'] if r['tag']==tag)
 actors=list(dict.fromkeys([recipe[k] for k in ['carrier_id','ship_id','other_id']]+recipe.get('cargo_ids',[recipe.get('cargo_id')])+([recipe['foot_id']] if recipe.get('foot_id') else [])+[b['id'] for b in recipe.get('blockers',[])]+recipe.get('traffic_ids',[])))
 first_effect_differences={}
 for actor in actors:
  diffs={}
  for key in ['health','position','mission','facings']:
   diffs[key]=next((f for f in modes['original'] if next(o for o in modes['original'][f]['objects'] if o['id']==actor)[key]!=next(o for o in modes['generated-c'][f]['objects'] if o['id']==actor)[key]),None)
  assert diffs['health'] is None
  first_effect_differences[str(actor)]=diffs
 samples=[]
 for frame in range(max(0,first-8),first+9):
  snapshots={}
  for mode,h in modes.items():
   state=h[frame];snapshots[mode]=dict(rng_indices=state['rng']['indices'],rng_table_sha256=hashlib.sha256(bytes.fromhex(state['rng']['table'])).hexdigest(),actors=[{k:o[k] for k in ['id','health','position','mission']} for o in state['objects'] if o['id'] in actors])
  samples.append(dict(frame=frame,modes=snapshots))
 windows[tag]=dict(first_rng_snapshot_difference=first,bounded_window=[first-8,first+8],first_recorded_actor_differences=first_effect_differences,samples=samples,causal_rng_call_not_proved=True,followup_only_for_functional_effect=True)
write(S/'rng-first-split-window.json',dict(passed=True,variants=windows,scope='One fixed 17-frame window per case, plus first object-field differences; complete health and final functional goals checked separately. Snapshot differences are not causal attribution of a random call.'))
write(S/'rng-functional-impact.json',dict(passed=True,protected_parent_files=[dict(path=str(p),sha256=sha(p)) for p in protected],new_variants=new,old1029_analysis_inherited_not_rerun=True,old349_coast_analysis_inherited_not_counted_as_new_pairs=True,no_rng_reset_or_seed_change=True,no_global_comparator_relaxation=True,scope='Mixed vehicle/infantry passengers, alternate Clear/Rough/Beach shore and retained full-adjacent-occupation retry effects only. Current complete per-mode traces equal their pre-change baselines; later combat/random allocation equivalence not claimed.'))
print(dict(passed=True,new={k:v['rng_first_different_frame'] for k,v in new.items()}))
