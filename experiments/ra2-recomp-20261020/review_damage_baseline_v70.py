"""Freeze observed input-precision and one-HP boundaries on the unchanged parent."""
from combat_batch_v70 import *
from analyze_combat_baseline_v69 import differences
import collections,re,struct
def records(tag,mode):return [json.loads(l) for l in (S/'runs'/tag/mode/'state.jsonl').open(encoding='utf-8')]
def ledger(rows):
    values=[x for x in rows if x['kind'].startswith('fixture-damage-')];assert len(values)%2==0
    out=[]
    for i in range(0,len(values),2):
        a,b=values[i:i+2];assert a['kind']=='fixture-damage-entry' and b['kind']=='fixture-damage-exit' and a['frame']==b['frame']
        out.append(dict(input=a,result=b['damage']))
    return out
if __name__=='__main__':
    assert read(S/'baseline-scenes.json')['passed'];values=[]
    for x in read(S/'scene-recipes.json')['fixtures']:
        tag=x['tag'];a,b=[records('b-'+tag,m) for m in ['original','generated-c']];assert len(a)==len(b)
        counts=collections.Counter();health_frames=[];neighbor_inputs=[]
        for u,v in zip(a,b):
            assert u['kind']==v['kind']
            for path,left,right in differences(u,v):
                counts[(u['kind'],path)]+=1
                if u['kind']=='fixture-damage-entry' and path=='.verse':
                    assert struct.unpack('<Q',struct.pack('<d',right))[0]-struct.unpack('<Q',struct.pack('<d',left))[0]==1
                    neighbor_inputs.append(dict(original=left,generated_c=right));continue
                if tag=='flat' and u['kind']=='fixture-damage-exit' and path=='.damage':assert (left,right)==(179,180);continue
                if tag=='flat' and ((u['kind']=='state' and re.fullmatch(r'\.objects\[\d+\]\.health',path)) or (u['kind']=='fixture-health-entry' and path=='.health')):
                    assert left-right==1;health_frames.append(u['frame']);continue
                raise AssertionError((tag,u.get('frame'),u['kind'],path,left,right))
        sa=[z for z in a if z['kind']=='state'];sb=[z for z in b if z['kind']=='state'];assert sa[0]==sb[0] and sa[-1]==sb[-1]
        la,lb=ledger(a),ledger(b);assert la and len(la)==len(lb)
        if tag=='rifle':assert all(z['input']['warhead']=='SA' and z['input']['armor']==5 and z['input']['verse']==.25 for z in la)
        else:
            assert {z['input']['distance'] for z in la}=={37,244} and len(la)==4
            if tag=='splash':assert {z['result'] for z in la}=={51,160} and [z['result'] for z in la]==[z['result'] for z in lb]
            else:assert {z['result'] for z in la}=={179} and {z['result'] for z in lb}=={180}
        d=read(S/'runs'/('b-'+tag)/'comparison.json');assert d['passed']==(tag=='rifle')
        values.append(dict(tag=tag,raw_strict=d['passed'],all_other_records_equal=True,initial_and_final_states_equal=True,coefficient_neighbor_inputs=neighbor_inputs,maximum_health_difference=1 if health_frames else 0,health_difference_frame_range=[min(health_frames),max(health_frames)] if health_frames else None,differences=[dict(kind=k[0],path=k[1],count=v) for k,v in counts.items()],original_damage=la,generated_damage=lb))
    assert read(S/'damage-probe-02.log')['neighbor_results']==[179,180]
    write(S/'baseline-review.json',dict(passed=True,fixtures=values,exe_sha256=sha(S/'baseline/ra2/build-original-c/ra2.exe'),numeric_input_difference_root_cause_fully_proved=False,native_same_input_conversion_verified=True,scope='Unchanged parent already loads adjacent double coefficients for V3WH. Default splash effects match; PercentAtMax=1 control differs by 1 HP between hits, with identical final state and casualty timing. Freeze full per-mode traces; retain raw failures and comparator. This is not a rule-parser fix or a complete visual-equivalence claim.'))
    print([(x['tag'],len(x['original_damage']),x['maximum_health_difference']) for x in values])
