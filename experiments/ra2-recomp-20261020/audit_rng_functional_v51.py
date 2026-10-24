"""Bounded effect analysis for new transport/airfield cases, without new RNG hooks."""
from run_batch_v51 import *
protected=[O/'rng-functional-impact.json',O/'corner-qualification.json',O/'rules-and-locomotors.json'];new={}
for tag in ['cw','ca','of']:
 p=S/'runs'/tag/'functional-acceptance.json';x=read(p)
 assert x['passed'] and x['baseline_inherited_exactly'] and x['core_functional_goals_equal'] and x['strict_failure_preserved']
 new[tag]=dict(functional_acceptance_sha256=sha(p),rng_first_different_frame=x['rng_first_different_frame'],rng_different_frames=x['rng_different_frames'],finite_goals_and_health_equal=True,raw_generator_stream_or_exact_call_source_proved_this_round=False)
write(S/'rng-functional-impact.json',dict(passed=True,protected_parent_files=[dict(path=str(p),sha256=sha(p)) for p in protected],new_variants=new,old1029_analysis_inherited_not_rerun=True,old349_coast_analysis_inherited_not_counted_as_new_pairs=True,no_rng_reset_or_seed_change=True,no_global_comparator_relaxation=True,scope='New repeated transport, occupied-shore and normal-airfield effects only. Current full mode traces equal their pre-change baselines; later combat/random allocation equivalence not claimed.'))
print(dict(passed=True,new={k:v['rng_first_different_frame'] for k,v in new.items()}))
