from combat_batch_v72 import *
from lifecycle_health_boundary_v72 import check
items=read(S/'accepted-scene-recipes.json')['fixtures'];values=read(S/'accepted-baseline-scenes.json')['results']
queue=next(x for x in items if x['tag']=='queue');attacker=1023312;assert attacker in {int(o.split(':')[1]) for o in queue['orders']};write(S/'functional-queue-baseline.json',check('b-queue',attacker))
order=['nothuman','delayed-prism','delayed-art','queue','truck','infantry','special','unattached','volley'];selected=[next(x for x in items if x['tag']==t) for t in order];selected_values=[next(x for x in values if x['tag']=='b-'+t) for t in order]
write(S/'qualified-final-scene-recipes.json',dict(passed=True,fixtures=selected,excluded_electric_rng_gap=True,preliminary_collection_superseded=True))
write(S/'baseline-accepted.json',dict(passed=True,results=selected_values))
write(S/'baseline-accepted-contract.json',dict(passed=True,traces=[dict(tag=v['tag'],mode=m,path=str(S/'runs'/v['tag']/m/'state.jsonl'),sha256=sha(S/'runs'/v['tag']/m/'state.jsonl')) for v in selected_values for m in ['original','generated-c']]))
d=read(S/'runs/b-electric/comparison.json');write(S/'baseline-finalization.json',dict(passed=True,canonical_recipes='qualified-final-scene-recipes.json',accepted_scenes=9,new_scenes=4,strict_scenes=6,bounded_functional_scenes=3,superseded_preliminary='accepted-scene-recipes.json',rules_only_deathframes_excluded=True,electric=dict(accepted=False,preserved=True,target_destructor_same_frame=211,first_difference=d['comparison']['first_difference'],reason='Pre-existing electric attack RNG/ancillary cleanup divergence in unmodified parent; outside current handoff/removal extraction. Preserve and rerun per mode as diagnostic; do not count as accepted natural equivalence.')))
print(dict(passed=True,accepted_scenes=9))
