"""Ordinary bridge placement and player-owned infantry/vehicle movement orders."""
from pathlib import Path
import hashlib,json,re
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v32'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
records=[]
for direction,goal,opposite in [('north',72,61),('south',61,72)]:
    source=S/f'fixtures/bridge-mixed-{direction}.MAP';base=source.read_text(encoding='ascii')
    for meeting in [True,False]:
        start=(69 if direction=='north' else 64) if meeting else (64 if direction=='north' else 69)
        text=base.replace('2=Player House,E2,256,60,66,2,Sleep','2=Player House,E2,256,60,'+str(start)+',2,Sleep')
        assert text!=base
        pattern=r'(?ms)^\[Infantry\]\n(.*?)(?=^\[|\Z)';m=re.search(pattern,text);assert m
        body=m[1].rstrip()+'\n4=Player House,E2,256,60,66,2,Sleep,128,None,0,-1,1,1,1\n\n'
        text=text[:m.start(1)]+body+text[m.end(1):]
        name=('meeting-' if meeting else 'following-')+direction;p=S/f'fixtures/bridge-infantry-{name}.MAP'
        p.write_text(text,encoding='ascii',newline='\n')
        orders=[f'5:1023362:2:60:{goal}',f'5:1023367:2:60:{opposite if meeting else goal}','1:1023364:2:60:75']
        records.append(dict(name=name,path=p.relative_to(R).as_posix(),sha256=sha(p),meeting=meeting,
            orders=orders,actor_ids=[1023362,1023367],vehicle_id=1023362,infantry_id=1023367,
            goals={'1023362':[60,goal],'1023367':[60,opposite if meeting else goal]},source=source.relative_to(R).as_posix()))
(S/'bridge-infantry-fixtures.json').write_text(json.dumps(dict(passed=True,fixtures=records,ordinary_player_orders=True,raw_state_writes=False),indent=2)+'\n',encoding='utf-8')
print('Prepared four moving infantry and vehicle scenes')
