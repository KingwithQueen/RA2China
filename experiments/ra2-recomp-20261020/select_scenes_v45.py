"""Keep unsuccessful recipes and select the finite, proven moving-locomotor recipe."""
from run_batch_v45 import *
from accept_dynamic_v45 import accept
x=read(S/'candidate-detour3.json');assert accept(x['baseline_tag'])['passed']
for mode in ['original','generated-c']:
 rows=[json.loads(l) for l in (S/'runs'/x['baseline_tag']/mode/'state.jsonl').open(encoding='utf-8')]
 states=[q for q in rows if q['kind']=='state']
 path=[next(o['position'] for o in q['objects'] if o['id']==1023365) for q in states]
 assert max(p[1] for p in path)-min(p[1] for p in path)>4000
 assert [v//256 for v in path[-1][:2]]==[63,59]
p=S/'dynamic-fixtures.json';initial=read(p);write(S/'initial-dynamic-fixtures.json',initial)
selected=dict(initial,fixtures=initial['fixtures'][:2]+[x],failed_hover_recipe_tags=['b-ds','b-d2'])
p.write_text(json.dumps(selected,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
values=[]
for recipe in selected['fixtures']:
 p=S/'runs'/recipe['baseline_tag']/'comparison.json';q=read(p)
 assert all(r['passed'] for r in q['runs'])
 assert q['passed'] or recipe['tag']=='d3'
 values.append(dict(tag=recipe['baseline_tag'],frames=q['comparison']['frames_compared'],comparison_sha256=sha(p),strict_trace_equal=q['passed'],functional_acceptance=recipe['tag']=='d3'))
write(S/'selected-baseline-scenes.json',dict(passed=True,results=values,excluded_from_final_pair_count=True,failed_hover_recipes_retained=True))
print('Selected reverse repair/control and proven south-entry moving Hover traffic')
