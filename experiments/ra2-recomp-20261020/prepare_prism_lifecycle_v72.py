from combat_batch_v72 import *
from lifecycle_scenes_v72 import execute
import re
p=S/'fixtures/art-deathframes-long.ini';old=(S/'fixtures/art-deathframes.ini').read_text(encoding='cp936');p.write_text(old.replace('DeathFrameRate=1\n','DeathFrameRate=1\nMaxDeathCounter=40\nStartDeathFrame=0\n'),encoding='cp936',newline='\n')
x=dict(next(v for v in read(S/'qualified-scene-recipes.json')['fixtures'] if v['tag']=='delayed'));x.pop('rules',None);x.pop('rules_sha256',None)
text=(R/x['path']).read_text(encoding='ascii');text=text.replace('Player House,MTNK,','Player House,SREF,');mp=S/'fixtures/delayed-prism.MAP';mp.write_text(text,encoding='ascii',newline='\n')
x.update(tag='delayed-prism',path=mp.relative_to(R).as_posix(),map_sha256=sha(mp),art=p.relative_to(R).as_posix(),art_sha256=sha(p),orders=[])
execute('id-delayed-prism',x,1);a=next(json.loads(l) for l in (S/'runs/id-delayed-prism/original/state.jsonl').open(encoding='utf-8') if json.loads(l)['kind']=='state');cells={tuple(v//256 for v in o['position'][:2]):o['id'] for o in a['objects']};x.update(attacker_id=cells[80,112],target_id=cells[86,112],orders=[f'5:{cells[80,112]}:1:{cells[86,112]}:0'])
write(S/'prism-scene.json',dict(passed=True,fixture=x));v=execute('b-delayed-prism',x,1200);write(S/'prism-baseline.json',dict(passed=True,result=v))
print(v)
