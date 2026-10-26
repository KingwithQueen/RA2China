from combat_batch_v72 import *
import collections

def rows(tag,mode):return [json.loads(l) for l in (S/'runs'/tag/mode/'state.jsonl').open(encoding='utf-8')]
if __name__=='__main__':
    proofs=[]
    for x in read(S/'qualified-final-scene-recipes.json')['fixtures']:
        tag='b-'+x['tag'];assert read(S/'runs'/tag/'comparison.json')['passed']==(x['tag'] not in ['delayed-art','delayed-prism','queue']),tag
        a,b=[rows(tag,m) for m in ['original','generated-c']];
        if x['tag'] not in ['delayed-art','delayed-prism','queue']:assert a==b,tag
        ids=sorted({int(v.split(':')[3]) for v in x['orders']});states=[v for v in a if v['kind']=='state'];events=[v for v in a if v['kind']=='fixture-lifecycle' and v['id'] in ids];counts=collections.Counter(v['address'] for v in events)
        remain=[i for i in ids if any(o['id']==i for o in states[-1]['objects'])]
        if x['tag']=='special':assert remain==ids
        else:
            assert not remain,(tag,remain)
            assert counts[0x4CCE40]>=len(ids) and counts[0x5D4E90]>=len(ids),tag
            assert counts[0x70A330]+counts[0x509810]>=len(ids),tag
        if x['tag'] in ['delayed-art','delayed-prism']:assert any(v['health']==1 for v in events if v['address']==0x5D4E90)
        drain=[v for v in a if v['kind']=='fixture-lifecycle' and v['address']==0x6ECF10]
        if x['tag']=='queue':assert len(ids)==4 and max(v['queued'] for v in drain)>=2
        proofs.append(dict(tag=x['tag'],new_scene=x['new_scene'],targets=ids,remaining=remain,lifecycle_counts={hex(k):v for k,v in counts.items()},maximum_delete_queue=max([v['queued'] for v in drain] or [0]),first_death_frame=min([v['frame'] for v in events if v['address'] in [0x70A330,0x509810]] or [-1]),original_sha256=sha(S/'runs'/tag/'original/state.jsonl')))
    write(S/'baseline-review.json',dict(passed=True,fixtures=proofs,new_scene_count=4,inherited_scenes=5,strict_original_c_scenes=6,bounded_functional_original_c_scenes=3,ordinary_attacks_and_map_rules=True,health_path_lifetime_or_queue_memory_injection=False,scope='Derived handoff, deferred death, electric/nonhuman infantry and queued destruction in finite natural attacks; whole derived death effects and destructors remain delegated.'))
    print(proofs)
