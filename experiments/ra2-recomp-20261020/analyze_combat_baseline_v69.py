"""Record bounded pre-existing repair effects without relaxing the raw comparator."""
from combat_batch_v69 import *
import collections
def load(tag,mode):
    return [json.loads(l) for l in (S/'runs'/tag/mode/'state.jsonl').open(encoding='utf-8')]
def differences(a,b,path=''):
    if type(a)!=type(b):yield path,a,b
    elif isinstance(a,dict):
        assert a.keys()==b.keys()
        for k in a:yield from differences(a[k],b[k],path+'.'+k)
    elif isinstance(a,list):
        if len(a)!=len(b):yield path+'.length',len(a),len(b)
        else:
            for i,(x,y) in enumerate(zip(a,b)):yield from differences(x,y,path+f'[{i}]')
    elif a!=b:yield path,a,b
if __name__=='__main__':
    values=[]
    for tag in ['repair','cap']:
        a=load('b-'+tag,'original');b=load('b-'+tag,'generated-c')
        assert [x for x in a if x['kind']!='state']==[x for x in b if x['kind']!='state']
        sa=[x for x in a if x['kind']=='state'];sb=[x for x in b if x['kind']=='state'];assert len(sa)==len(sb)==1501
        counts=collections.Counter();mission=[];allocation=[]
        for x,y in zip(sa,sb):
            assert x['frame']==y['frame']
            for p,u,v in differences(x,y):
                counts[p]+=1
                if p.startswith('.rng.'):continue
                if p=='.next_id':allocation.append(v-u);continue
                assert p=='.objects[0].mission[0]' and x['objects'][0]['id']==1023310 and (u,v)==(5,1),(tag,x['frame'],p,u,v)
                mission.append(dict(frame=x['frame'],id=1023310,original=u,generated_c=v))
        assert len(mission)<=2 and (not mission or max(z['frame'] for z in mission)-min(z['frame'] for z in mission)<=1)
        hits=[x for x in a if x['kind']=='fixture-health-entry' and x['id']==1023311]
        assert hits and all(x['incoming']==-50 and x['warhead']=='Mechanical' for x in hits)
        last=next(z for z in sa[-1]['objects'] if z['id']==1023311);assert last['health']==300
        if tag=='cap':assert any(x['health']==284 for x in hits) and len(hits)==2
        values.append(dict(tag=tag,raw_strict=False,first_difference=read(S/'runs'/('b-'+tag)/'comparison.json')['comparison']['first_difference'],allocation_counter_delta_range=[min(allocation),max(allocation)],mission_completion_difference=mission,all_other_recorded_fields_equal=True,non_state_records_equal=True,hits=hits,final_health=300,difference_counts=dict(counts)))
    write(S/'baseline-effects.json',dict(passed=True,fixtures=values,pre_attach_exe_sha256=sha(S/'baseline/ra2/build-original-c/ra2.exe'),allocation_counter_cause_fully_proved=False,particle_visual_equivalence_proved=False,scope='Finite known repair variations on the unchanged parent; final full per-mode traces must equal the frozen baseline. Raw strict comparisons remain failed.'))
    print([(x['tag'],len(x['hits']),x['mission_completion_difference']) for x in values])
