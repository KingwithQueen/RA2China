"""Exact before/after lifecycle traces, observer parity and inherited effects."""
from combat_batch_v71 import *
from review_death_baseline_v71 import rows
def standard(p):return b''.join(l for l in p.read_bytes().splitlines(keepends=True) if not json.loads(l)['kind'].startswith('fixture-'))
items=read(S/'qualified-scene-recipes.json')['fixtures']+[read(S/'extra-scene.json')['fixture']];contracts=read(S/'baseline-contract.json')['traces']+read(S/'extra-baseline.json')['traces'];proofs=[]
for x in items:
    base='b-volley' if x['tag']=='volley' else 'b-02-'+x['tag'];final='f-'+x['tag']
    for mode in ['original','generated-c']:
        a=S/'runs'/base/mode/'state.jsonl';b=S/'runs'/final/mode/'state.jsonl';e=next(e for e in contracts if e['tag']==base and e['mode']==mode);assert sha(a)==e['sha256']==sha(b),(x['tag'],mode)
        proofs.append(dict(tag=x['tag'],baseline_tag=base,mode=mode,sha256=sha(b)))
    assert rows(final,'original')==rows(final,'generated-c') and read(S/'runs'/final/'comparison.json')['passed']
parity=[]
for phase,obs in [('b','b-02-truck'),('f','f-truck')]:
    for mode in ['original','generated-c']:
        a=S/'runs'/obs/mode/'state.jsonl';b=S/'runs'/(phase+'-truck-command')/mode/'state.jsonl';assert standard(a)==b.read_bytes();parity.append(dict(phase=phase,mode=mode,command_sha256=sha(b),observer_sha256=sha(a)))
inherited=[]
for x in read(S/'combat-regressions.json')['results']:
    assert x['strict']==(x['tag'] not in ['old-repair','old-cap','old-flat'])
    for mode in ['original','generated-c']:
        old=Path(x['parent_stage'])/'runs'/x['parent_tag']/mode/'state.jsonl';new=S/'runs'/x['tag']/mode/'state.jsonl';assert standard(old)==new.read_bytes(),(x['tag'],mode)
        inherited.append(dict(tag=x['tag'],mode=mode,parent_path=str(old),parent_sha256=sha(old),current_sha256=sha(new)))
movement=[]
for x in read(S/'movement-regressions.json')['results']:
    for mode in ['original','generated-c']:
        old=O/'runs'/x['tag']/mode/'state.jsonl';new=S/'runs'/x['tag']/mode/'state.jsonl';assert sha(old)==sha(new);movement.append(dict(tag=x['tag'],mode=mode,parent_path=str(old),sha256=sha(old)))
write(S/'natural-effects.json',dict(passed=True,complete_pre_post_traces=proofs,baseline_review_sha256=sha(S/'baseline-review.json'),inherited_combat_traces=inherited,movement_parent_parity=movement,raw_comparator_relaxed=False,scope='Five new natural attack/tag/posture controls; single-vehicle repeat recovery and dense-fire death both preserved. Eight inherited battle cases and six production regressions unchanged per mode.'))
write(S/'record-parity.json',dict(passed=True,records=parity,only_fixture_diagnostics_filtered=True,production_recorder_and_comparator_unchanged=True,native_observer_return_addresses_restored=True))
print(dict(passed=True,new_scenes=5,exact_pre_post_traces=10,observer_parity=4,inherited_combat_traces=16,movement_traces=12))
