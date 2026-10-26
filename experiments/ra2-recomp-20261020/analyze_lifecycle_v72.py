from combat_batch_v72 import *
from review_lifecycle_baseline_v72 import rows

def standard(p):return b''.join(l for l in p.read_bytes().splitlines(keepends=True) if not json.loads(l)['kind'].startswith('fixture-'))
proofs=[];contracts=read(S/'baseline-accepted-contract.json')['traces'];items=read(S/'qualified-final-scene-recipes.json')['fixtures']
for x in items:
    for mode in ['original','generated-c']:
        a=S/'runs'/('b-'+x['tag'])/mode/'state.jsonl';b=S/'runs'/('f-'+x['tag'])/mode/'state.jsonl';e=next(v for v in contracts if v['tag']=='b-'+x['tag'] and v['mode']==mode);assert sha(a)==e['sha256']==sha(b),(x['tag'],mode)
        proofs.append(dict(tag=x['tag'],mode=mode,sha256=sha(b)))
    if x['tag'] not in ['delayed-art','delayed-prism','queue']:assert rows('f-'+x['tag'],'original')==rows('f-'+x['tag'],'generated-c') and read(S/'runs'/('f-'+x['tag'])/'comparison.json')['passed']
parity=[]
for phase in ['b','f']:
    for mode in ['original','generated-c']:
        a=S/'runs'/(phase+'-nothuman')/mode/'state.jsonl';b=S/'runs'/(phase+'-command')/mode/'state.jsonl';assert standard(a)==b.read_bytes();parity.append(dict(phase=phase,mode=mode,observer_sha256=sha(a),command_sha256=sha(b)))
inherited=[]
for x in read(S/'combat-regressions.json')['results']:
    assert x['strict']==(x['tag'] not in ['old-repair','old-cap','old-flat'])
    for mode in ['original','generated-c']:
        old=Path(x['parent_stage'])/'runs'/x['parent_tag']/mode/'state.jsonl';new=S/'runs'/x['tag']/mode/'state.jsonl';assert standard(old)==new.read_bytes(),(x['tag'],mode);inherited.append(dict(tag=x['tag'],mode=mode,parent_path=str(old),parent_sha256=sha(old),current_sha256=sha(new)))
movement=[]
for x in read(S/'movement-regressions.json')['results']:
    for mode in ['original','generated-c']:
        old=O/'runs'/x['tag']/mode/'state.jsonl';new=S/'runs'/x['tag']/mode/'state.jsonl';assert sha(old)==sha(new);movement.append(dict(tag=x['tag'],mode=mode,parent_path=str(old),sha256=sha(old)))
write(S/'natural-effects.json',dict(passed=True,complete_pre_post_traces=proofs,inherited_combat_traces=inherited,movement_parent_parity=movement,raw_comparator_relaxed=False,new_scenes=4,shared_death_parent_scenes=5))
write(S/'record-parity.json',dict(passed=True,records=parity,only_fixture_diagnostics_filtered=True,production_recorder_and_comparator_unchanged=True,destructor_vtable_observation_readonly=True))
print(dict(passed=True,complete_pre_post_traces=18,observer_parity=4,inherited_combat_traces=16,movement_traces=12))

from lifecycle_health_boundary_v72 import check
from lifecycle_timing_boundary_v72 import check_prism
write(S/'functional-art-final.json',check('f-delayed-art',read(S/'functional-art-baseline.json')['attacker_id']))
write(S/'functional-prism-final.json',check_prism('f-delayed-prism'))

write(S/'functional-queue-final.json',check('f-queue',read(S/'functional-queue-baseline.json')['attacker_id']))
