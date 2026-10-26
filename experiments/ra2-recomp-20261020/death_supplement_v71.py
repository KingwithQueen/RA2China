"""Sustained ordinary tank volley distinguishes special recovery from final removal."""
from combat_batch_v71 import *
from death_scenes_v71 import execute
import re
if sys.argv[1]=='prepare':
    x=dict(next(x for x in read(S/'qualified-scene-recipes.json')['fixtures'] if x['tag']=='special'))
    source=R/x['path'];text=source.read_text(encoding='ascii');units=''.join(f'{i}=Player House,MTNK,256,{a},{b},0,Sleep,None,0,-1,0,-1,1,1\n' for i,(a,b) in enumerate([(80,112),(80,113),(81,112)]))
    text=re.sub(r'(?ms)^\[Units\]\n.*?(?=^\[|\Z)',lambda _:'[Units]\n'+units+'\n',text)
    p=S/'fixtures/volley.MAP';p.write_text(text,encoding='ascii',newline='\n');x.update(tag='volley',path=p.relative_to(R).as_posix(),map_sha256=sha(p),orders=[])
    execute('id-volley',x,1)
    a=next(json.loads(l) for l in (S/'runs/id-volley/original/state.jsonl').open(encoding='utf-8') if json.loads(l)['kind']=='state');cells={tuple(v//256 for v in o['position'][:2]):o['id'] for o in a['objects']}
    target=cells[86,112];actors=[cells[z] for z in [(80,112),(80,113),(81,112)]];x.update(target_id=target,actor_ids=actors,orders=[f'5:{a}:1:{target}:0' for a in actors])
    write(S/'extra-scene.json',dict(passed=True,fixture=x,ordinary_multiple_attackers=True))
    value=execute('b-volley',x,900);write(S/'extra-baseline.json',dict(passed=True,result=value,traces=[dict(tag='b-volley',mode=m,path=str(S/'runs/b-volley'/m/'state.jsonl'),sha256=sha(S/'runs/b-volley'/m/'state.jsonl')) for m in ['original','generated-c']]))
elif sys.argv[1]=='final':
    x=read(S/'extra-scene.json')['fixture'];value=execute('f-volley',x,900);write(S/'extra-final.json',dict(passed=True,result=value))
else:raise ValueError(sys.argv[1])
