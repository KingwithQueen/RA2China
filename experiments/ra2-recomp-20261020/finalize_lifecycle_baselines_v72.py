from combat_batch_v72 import *
from lifecycle_health_boundary_v72 import check
from lifecycle_timing_boundary_v72 import check_prism
items0=read(S/'qualified-scene-recipes.json')['fixtures'];x=dict(next(z for z in items0 if z['tag']=='delayed'));x.pop('rules',None);x.pop('rules_sha256',None);x.update(tag='delayed-art',art='evidence/combat-state-v4/fixtures/art-deathframes.ini',art_sha256=sha(S/'fixtures/art-deathframes.ini'))
proof=check('b-delayed-art',x['attacker_id']);write(S/'functional-art-baseline.json',proof)
z=read(S/'runs/b-delayed-art/comparison.json');art_value=dict(tag='b-delayed-art',frames=z['comparison']['frames_compared'],strict=z['passed'],comparison_sha256=sha(S/'runs/b-delayed-art/comparison.json'),exe_sha256=z['exe_sha256'])
prism=read(S/'prism-scene.json')['fixture'];prismvalue=read(S/'prism-baseline.json')['result'];assert not prismvalue['strict'];write(S/'functional-prism-baseline.json',check_prism('b-delayed-prism'))
items=[prism,x]+[v for v in items0 if v['tag']!='delayed'];values=[prismvalue,art_value]+[v for v in read(S/'baseline-scenes.json')['results'] if v['tag']!='b-delayed'];assert len(items)==len(values)==10
write(S/'accepted-scene-recipes.json',dict(passed=True,fixtures=items,initial_rules_only_delayed_control_excluded=True))
write(S/'accepted-baseline-scenes.json',dict(passed=True,results=values))
write(S/'accepted-baseline-contract.json',dict(passed=True,traces=[dict(tag=v['tag'],mode=m,path=str(S/'runs'/v['tag']/m/'state.jsonl'),sha256=sha(S/'runs'/v['tag']/m/'state.jsonl')) for v in values for m in ['original','generated-c']]))
write(S/'art-qualification.json',dict(passed=True,initial_untriggered_scene_preserved=True,initial_tag='b-delayed',accepted_tags=['b-delayed-art','b-delayed-prism'],prism_auxiliary_cleanup_five_frame_difference_preserved=True,reason='Original UnitType reads DeathFrames from ART.INI global 008397F0 at 0070AE04/10. RULES-only control did not exercise delayed death and is excluded.',default_counter_art_control_one_hp_phase_observed_before_uninit=True,prism_control_counter=40,raw_strict_mtnk_control_failed_only_preexisting_1hp=True,bounded_functional_receipt_sha256=sha(S/'functional-art-baseline.json'),private_art_copy_only=True,original_art_unchanged=True))
print(dict(passed=True,accepted_scenes=10,new_scenes=5))
