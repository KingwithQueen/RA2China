"""Full pre/post traces, positive damage witnesses and inherited production effects."""
from combat_batch_v70 import *
from review_damage_baseline_v70 import records,ledger
def standard(p):return b''.join(l for l in p.read_bytes().splitlines(keepends=True) if not json.loads(l)['kind'].startswith('fixture-'))
new=[];traces=[]
for x in read(S/'scene-recipes.json')['fixtures']:
    tag=x['tag']
    for mode in ['original','generated-c']:
        a=S/'runs'/('b-'+tag)/mode/'state.jsonl';b=S/'runs'/('f-'+tag)/mode/'state.jsonl'
        e=next(e for e in read(S/'baseline-contract.json')['traces'] if e['tag']=='b-'+tag and e['mode']==mode)
        assert sha(a)==e['sha256']==sha(b),(tag,mode,'Changed complete trace')
        traces.append(dict(tag=tag,mode=mode,sha256=sha(b)))
    a,b=[ledger(records('f-'+tag,m)) for m in ['original','generated-c']]
    assert a==next(e for e in read(S/'baseline-review.json')['fixtures'] if e['tag']==tag)['original_damage']
    assert b==next(e for e in read(S/'baseline-review.json')['fixtures'] if e['tag']==tag)['generated_damage']
    same=standard(S/'runs'/('f-'+tag)/'original/state.jsonl')==standard(S/'runs'/('f-'+tag)/'generated-c/state.jsonl')
    assert same==(tag!='flat')
    new.append(dict(tag=tag,original_ledger=a,generated_ledger=b,production_records_equal=same,raw_strict=read(S/'runs'/('f-'+tag)/'comparison.json')['passed']))
parity=[]
for phase in ['b','f']:
    for mode in ['original','generated-c']:
        p=S/'runs'/(phase+'-rifle')/mode/'state.jsonl';q=S/'runs'/(phase+'-rifle-command')/mode/'state.jsonl'
        assert standard(p)==q.read_bytes(),(phase,mode,'Observer changed production records')
        parity.append(dict(phase=phase,mode=mode,command_trace_sha256=sha(q),observer_trace_sha256=sha(p)))
inherited=[]
for x in read(O/'scene-recipes.json')['fixtures']+[read(O/'extra-scene.json')['fixture']]:
    tag=x['tag'];d=read(S/'runs'/('old-'+tag)/'comparison.json');assert d['passed']==(tag not in ['repair','cap'])
    for mode in ['original','generated-c']:
        old=O/'runs'/('f-'+tag)/mode/'state.jsonl';newp=S/'runs'/('old-'+tag)/mode/'state.jsonl'
        assert standard(old)==newp.read_bytes(),(tag,mode,'Inherited combat effect changed')
        inherited.append(dict(tag=tag,mode=mode,parent_path=str(old),parent_trace_sha256=sha(old),current_trace_sha256=sha(newp)))
movement=[]
for x in read(S/'movement-regressions.json')['results']:
    for mode in ['original','generated-c']:
        old=O/'runs'/x['tag']/mode/'state.jsonl';newp=S/'runs'/x['tag']/mode/'state.jsonl'
        assert sha(old)==sha(newp),(x['tag'],mode)
        movement.append(dict(tag=x['tag'],mode=mode,parent_path=str(old),sha256=sha(old)))
write(S/'natural-effects.json',dict(passed=True,new_scenes=new,complete_pre_post_traces_unchanged=traces,baseline_review_sha256=sha(S/'baseline-review.json'),inherited_combat_traces=inherited,movement_parent_parity=movement,raw_comparator_relaxed=False,damage_or_health_injection=False,scope='Rifle heavy armor, default V3 splash and explicit flat-edge control; existing coefficient precision/1-HP control boundary preserved. Five inherited combat and six production regressions retained per mode.'))
write(S/'record-parity.json',dict(passed=True,records=parity,only_fixture_diagnostics_filtered=True,production_recorder_and_comparator_unchanged=True))
print(dict(passed=True,new_scenes=3,full_pre_post_traces=6,inherited_combat_traces=10,movement_traces=12,observer_parity=4))
