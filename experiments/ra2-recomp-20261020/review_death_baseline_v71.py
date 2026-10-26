"""Qualify native map owners, ordered notifications, posture-sensitive recovery and removal."""
from combat_batch_v71 import *
import collections
def rows(tag,mode):return [json.loads(l) for l in (S/'runs'/tag/mode/'state.jsonl').open(encoding='utf-8')]
if __name__=='__main__':
    items=read(S/'qualified-scene-recipes.json')['fixtures']+[read(S/'extra-scene.json')['fixture']];proofs=[]
    for x in items:
        tag='b-volley' if x['tag']=='volley' else 'b-02-'+x['tag'];d=read(S/'runs'/tag/'comparison.json');assert d['passed'],tag
        a,b=[rows(tag,m) for m in ['original','generated-c']];assert a==b,tag
        target=x['target_id'];entries=[z for z in a if z['kind']=='fixture-death-entry' and z['id']==target];result=[z for z in a if z['kind']=='fixture-death-result' and z['id']==target];events=[z for z in a if z['kind']=='fixture-tag-event' and z['id']==target]
        assert len(entries)==len(result) and entries
        if x['attached_tag']:assert events and all(z['has_tag']==1 for z in entries)
        else:assert not events and all(z['has_tag']==0 for z in entries)
        states=[z for z in a if z['kind']=='state'];alive=any(o['id']==target for o in states[-1]['objects'])
        recoveries=[z for z in result if z['result']==3 and z['health']==31 and z['special_applied']==1]
        if x['tag']=='special':assert len(recoveries)>=2 and alive and all(z['special_kind']==1 for z in entries)
        else:assert not alive and any(z['result']==4 for z in result)
        if x['tag']=='volley':assert any(z['special_applied']==1 and z['health']>31 for z in result)
        proofs.append(dict(tag=x['tag'],baseline_tag=tag,target_id=target,hits=len(entries),events=dict(collections.Counter(z['event'] for z in events)),special_recoveries=recoveries,last_result=result[-1],target_present_at_end=alive,source_sha256=sha(S/'runs'/tag/'original/state.jsonl')))
    assert set(next(p for p in proofs if p['tag']=='infantry')['events'])>={6,38,39,40,41,42,43,44}
    write(S/'baseline-review.json',dict(passed=True,fixtures=proofs,all_strict=True,raw_posture_field_name='special_applied',posture_flag_offset='Infantry+005C3',lifetime_one_shot_recovery_flag=False,scope='Single-vehicle explicit Cyborg control repeatedly recovers as the posture flag resets; dense fire keeps the flag set and kills the target. Both original and unchanged parent agree. Preserve the actual posture boundary rather than inventing an ever-recovered flag.'))
    write(S/'input-qualification.json',dict(passed=True,corrected_country='BadGuy1',invalid_house_instance='BadGuy1 House',initial_invalid_recipes_preserved=True,independent_invalid_command_receipt_sha256=sha(S/'invalid-owner-independent.json'),corrected_all_original_c_passed=True,scope='Only trigger country field corrected; malformed-owner exceptions remain separate from accepted natural scenes.'))
    print([(p['tag'],p['hits'],p['target_present_at_end']) for p in proofs])
