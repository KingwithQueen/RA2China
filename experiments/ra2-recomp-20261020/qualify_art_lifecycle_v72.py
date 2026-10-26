from combat_batch_v72 import *
from lifecycle_scenes_v72 import execute
x=dict(next(v for v in read(S/'qualified-scene-recipes.json')['fixtures'] if v['tag']=='delayed'));x.pop('rules',None);x.pop('rules_sha256',None);x.update(tag='delayed-art',art='evidence/combat-state-v4/fixtures/art-deathframes.ini',art_sha256=sha(S/'fixtures/art-deathframes.ini'),orders=[])
execute('id-delayed-art',x,1)
a=next(json.loads(l) for l in (S/'runs/id-delayed-art/original/state.jsonl').open(encoding='utf-8') if json.loads(l)['kind']=='state');cells={tuple(v//256 for v in o['position'][:2]):o['id'] for o in a['objects']};x.update(attacker_id=cells[80,112],target_id=cells[86,112],orders=[f'5:{cells[80,112]}:1:{cells[86,112]}:0'])
v=execute('b-delayed-art',x,1200);assert v['strict']
a=[json.loads(l) for l in (S/'runs/b-delayed-art/original/state.jsonl').open(encoding='utf-8')];assert any(o['id']==x['target_id'] and o['health']==1 for z in a if z['kind']=='state' for o in z['objects'])
initial=read(S/'qualified-scene-recipes.json')['fixtures'];items=[x]+[v for v in initial if v['tag']!='delayed'];values=[v]+[z for z in read(S/'baseline-scenes.json')['results'] if z['tag']!='b-delayed']
write(S/'accepted-scene-recipes.json',dict(passed=True,fixtures=items,initial_delayed_control_excluded=True))
write(S/'accepted-baseline-scenes.json',dict(passed=True,results=values))
write(S/'accepted-baseline-contract.json',dict(passed=True,traces=[dict(tag=z['tag'],mode=m,path=str(S/'runs'/z['tag']/m/'state.jsonl'),sha256=sha(S/'runs'/z['tag']/m/'state.jsonl')) for z in values for m in ['original','generated-c']]))
write(S/'art-qualification.json',dict(passed=True,initial_untriggered_scene_preserved=True,initial_tag='b-delayed',accepted_tag='b-delayed-art',reason='Original UnitType reads DeathFrames from ART.INI global 008397F0 at 0070AE04/10, not RULES.INI. Initial rules-only control was strict but did not exercise delayed death and is excluded.',actual_one_hp_delayed_phase_observed=True,private_art_copy_only=True,original_art_unchanged=sha(Path(read(S/'art-input.json')['original_path']))==read(S/'art-input.json')['original_sha256']))
print(dict(passed=True,accepted_scenes=9))
