"""Finite natural effects, full before/after records and readonly-observer parity."""
from combat_batch_v69 import *
from analyze_combat_baseline_v69 import load
items=read(S/'scene-recipes.json')['fixtures']+[read(S/'extra-scene.json')['fixture']]
frozen=read(S/'baseline-contract.json')['traces']+read(S/'extra-baseline-contract.json')['traces'];unchanged=[];effects=[]
for x in items:
    tag=x['tag'];target=x['target_id'];records={}
    for mode in ['original','generated-c']:
        base=S/'runs'/('b-'+tag)/mode/'state.jsonl';current=S/'runs'/('f-'+tag)/mode/'state.jsonl'
        contract=next(z for z in frozen if z['tag']=='b-'+tag and z['mode']==mode)
        assert sha(base)==contract['sha256']==sha(current),(tag,mode,'Complete trace changed')
        unchanged.append(dict(tag=tag,mode=mode,sha256=sha(current)))
        records[mode]=load('f-'+tag,mode)
    a=records['original'];hits=[z for z in a if z['kind']=='fixture-health-entry' and z['id']==target];assert hits
    b=[z for z in records['generated-c'] if z['kind']=='fixture-health-entry' and z['id']==target];assert hits==b
    states=[z for z in a if z['kind']=='state'];hp=[(z['frame'],next((o['health'] for o in z['objects'] if o['id']==target),None)) for z in states]
    if tag in ['tank','infantry']:
        assert all(z['incoming']==65 and z['warhead']=='AP' for z in hits)
        assert hp[-1][1] is None and any(v is not None and v<hp[0][1] for _,v in hp)
        removed=next(f for f,v in hp if v is None);maximum=200 if tag=='tank' else 125;assert hp[0][1]==maximum
        effect=dict(initial_health=maximum,last_alive_health=next(v for _,v in reversed(hp) if v is not None),removed_frame=removed,ordinary_lethal_attack=True)
    elif tag=='immune':
        assert all(z['type_flag_203']==1 and z['incoming']==65 for z in hits) and all(v==200 for _,v in hp)
        effect=dict(initial_health=200,final_health=200,explicit_immune_rule_control=True)
    else:
        assert hp[-1][1]==300 and all(z['incoming']==-50 and z['warhead']=='Mechanical' for z in hits)
        if tag=='cap':assert len(hits)==2 and hits[-1]['health']==284
        effect=dict(initial_health=hp[0][1],final_health=300,repairer_entered_engineer_vehicle=True,overheal_cap_exercised=tag=='cap')
    cmp=read(S/'runs'/('f-'+tag)/'comparison.json');assert cmp['passed']==(tag not in ['repair','cap'])
    effects.append(dict(tag=tag,hits=len(hits),first_hit=hits[0],effect=effect,raw_strict=cmp['passed'],existing_variations_preserved=tag in ['repair','cap']))
parity=[]
for phase in ['b','f']:
    for mode in ['original','generated-c']:
        p=S/'runs'/(phase+'-tank')/mode/'state.jsonl';q=S/'runs'/(phase+'-tank-cmd')/mode/'state.jsonl'
        raw=[l for l in p.read_bytes().splitlines(keepends=True) if json.loads(l)['kind']!='fixture-health-entry']
        assert b''.join(raw)==q.read_bytes(),(phase,mode,'Observer changed production records')
        parity.append(dict(phase=phase,mode=mode,standard_record_sha256=sha(q),observer_complete_sha256=sha(p)))
write(S/'natural-effects.json',dict(passed=True,fixtures=effects,full_per_mode_before_after_unchanged=unchanged,baseline_effect_boundary_sha256=sha(S/'baseline-effects.json'),raw_comparator_relaxed=False,direct_damage_health_injection=False,scope='Five finite ordinary-command scenes: vehicle/infantry lethal, engineer/FV repair and overheal cap, explicit immune control. Existing repair RNG/allocation and 1-2 frame completion variations retained.'))
write(S/'record-parity.json',dict(passed=True,records=parity,only_health_entry_records_filtered=True,production_recorder_and_comparator_unchanged=True,command_adapter_scope='Native MEGAMISSION Attack/Enter object targets; no damage or game-state assignment.'))
print(dict(passed=True,scenes=len(effects),full_traces_unchanged=len(unchanged),parity=len(parity)))
