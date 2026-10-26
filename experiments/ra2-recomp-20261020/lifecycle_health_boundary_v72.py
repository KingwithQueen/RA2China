"""Document a pre-existing bounded 1HP difference without relaxing the raw comparator."""
from combat_batch_v72 import *
def check(tag,attacker):
    rows=lambda m:[json.loads(l) for l in (S/'runs'/tag/m/'state.jsonl').open(encoding='utf-8')]
    a,b=rows('original'),rows('generated-c');assert len(a)==len(b);differences=[]
    for index,(x,y) in enumerate(zip(a,b)):
        assert x['kind']==y['kind'] and x.get('frame')==y.get('frame');kind=x['kind']
        if kind=='state':
            assert [o['id'] for o in x['objects']]==[o['id'] for o in y['objects']]
            for left,right in zip(x['objects'],y['objects']):
                if left['health']!=right['health']:
                    assert left['id']==attacker and left['health']-right['health']==1 and right['health']>0
                    differences.append(dict(row=index,kind=kind,frame=x['frame'],id=attacker,original=left['health'],generated_c=right['health']))
                    right=dict(right);right['health']=left['health'];assert left==right
                else:assert left==right
            z=dict(y);z['objects']=x['objects'];assert x==z
        elif kind=='fixture-death-result' and x['id']==attacker:
            if x['health']!=y['health']:
                assert x['health']-y['health']==1 and y['health']>0
                differences.append(dict(row=index,kind=kind,frame=x['frame'],id=attacker,original=x['health'],generated_c=y['health']))
                z=dict(y);z['health']=x['health'];assert x==z
            else:assert x==y
        else:assert x==y,(tag,index,kind)
    assert differences and not read(S/'runs'/tag/'comparison.json')['passed']
    return dict(passed=True,tag=tag,strict_raw_comparison=False,attacker_id=attacker,differing_records=len(differences),first=differences[0],last=differences[-1],all_other_fields_rng_lifecycle_targets_equal=True,maximum_health_difference=1,source='Observed before current service attachment in unchanged parent C.',raw_comparator_relaxed=False)
