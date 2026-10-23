"""Use existing ordinary map objects and house alliances for enemy bridge cases."""
from pathlib import Path
import hashlib,json,re
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v37'
records=[]
for direction in ['north','south']:
    for dynamic in [False,True]:
        old=('traffic-' if dynamic else 'mixed-')+direction
        source=S/f'fixtures/bridge-{old}.MAP';text=source.read_text(encoding='ascii')
        enemy_index=1 if dynamic else 2
        needle=f'{enemy_index}=Player House,TRUCKA,'
        assert text.count(needle)==1
        text=text.replace(needle,f'{enemy_index}=BadGuy1 House,TRUCKA,')
        name=('enemy-traffic-' if dynamic else 'enemy-mixed-')+direction
        p=S/f'fixtures/bridge-{name}.MAP';assert not p.exists();p.write_text(text,encoding='ascii',newline='\n')
        goal=72 if direction=='north' else 61
        orders=[f'5:1023362:2:60:{goal}']
        if dynamic:orders += [f'5:1023363:2:60:{61 if direction=="north" else 72}','1:1023365:2:60:75']
        records.append(dict(name=name,path=p.relative_to(R).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),
            dynamic=dynamic,actor_ids=[1023362,1023363] if dynamic else [1023362],enemy_id=1023362+enemy_index,
            orders=orders,goal=[60,goal],source=source.relative_to(R).as_posix()))
(S/'bridge-hostile-fixtures.json').write_text(json.dumps(dict(passed=True,fixtures=records,ordinary_map_objects=True,
    native_house_alliances_unchanged=True,raw_state_writes=False),indent=2)+'\n',encoding='utf-8')
print('Created four enemy bridge maps from accepted mixed and traffic inputs')
