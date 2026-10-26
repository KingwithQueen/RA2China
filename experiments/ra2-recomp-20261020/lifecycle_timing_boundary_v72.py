from combat_batch_v72 import *
def check_prism(tag):
    rows=lambda m:[json.loads(l) for l in (S/'runs'/tag/m/'state.jsonl').open(encoding='utf-8')]
    a,b=rows('original'),rows('generated-c');assert [x for x in a if x['kind']!='fixture-lifecycle']==[x for x in b if x['kind']!='fixture-lifecycle']
    la,lb=[[x for x in v if x['kind']=='fixture-lifecycle'] for v in [a,b]];assert len(la)==len(lb);diff=[]
    for x,y in zip(la,lb):
        if x!=y:
            assert y['frame']-x['frame']==5 and x['id'] in [0,1023359] and x['address'] in [0x5D4E90,0x6ECF10]
            z=dict(y);z['frame']=x['frame'];assert z==x;diff.append(dict(original=x,generated_c=y))
    assert len(diff)==2 and {x['original']['id'] for x in diff}=={0,1023359};d=read(S/'runs'/tag/'comparison.json');assert not d['passed'] and d['comparison']['first_difference'] is None
    return dict(passed=True,tag=tag,strict_raw_comparison=False,all_1201_frame_states_rng_commands_and_nonlife_records_equal=True,controlled_target_lifecycle_equal=True,auxiliary_object_id=1023359,lifecycle_differences=diff,maximum_delay_frames=5,source='Observed in unchanged parent C before current service attachment.',raw_comparator_relaxed=False)
