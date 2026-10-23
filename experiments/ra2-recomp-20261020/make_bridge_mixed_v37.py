"""Legal map-object inputs for mixed bridge layers and ordinary opposing traffic."""
from pathlib import Path
import hashlib,json,re
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v37'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def section(text,key,body):
    pattern=rf'(?ms)^\[{key}\]\n.*?(?=^\[|\Z)'
    assert len(re.findall(pattern,text))==1,key
    return re.sub(pattern,lambda _:f'[{key}]\n{body}\n\n',text)
def unit(index,x,y,upper=0):
    return f'{index}=Player House,TRUCKA,256,{x},{y},128,Guard,None,0,-1,{upper},-1,1,1'
records=[]
for direction,start,goal in [('north',62,72),('south',71,61)]:
    source=S/f'fixtures/bridge-chain-{direction}.MAP'
    base=source.read_text(encoding='ascii')
    for dynamic in [False,True]:
        infantry=[]
        for upper in [0,1]:
            for sub in [2,4]:
                infantry.append(f'{len(infantry)}=Player House,E2,256,60,66,{sub},Sleep,128,None,0,-1,{upper},1,1')
        rows=[unit(0,60,start)]
        if dynamic:rows.append(unit(1,60,71 if direction=='north' else 62))
        rows += [unit(len(rows),60,66,0),unit(len(rows)+1,60,66,1)]
        text=section(section(base,'Infantry','\n'.join(infantry)),'Units','\n'.join(rows))
        name=('traffic-' if dynamic else 'mixed-')+direction
        p=S/f'fixtures/bridge-{name}.MAP'
        if p.exists():assert p.read_bytes()==text.encode('ascii')
        else:p.write_text(text,encoding='ascii',newline='\n')
        orders=[f'5:1023362:2:60:{goal}']
        if dynamic:
            orders.append(f'5:1023363:2:60:{61 if direction=="north" else 72}')
            orders.append('1:1023365:2:60:75')
        records.append(dict(name=name,path=p.relative_to(R).as_posix(),sha256=sha(p),dynamic=dynamic,
            actor_ids=[1023362,1023363] if dynamic else [1023362],orders=orders,goal=[60,goal],
            mixed_cell=[60,66],expected_static_types=['TRUCKA','E2'],source=source.relative_to(R).as_posix()))
out=S/'bridge-mixed-fixtures.json';assert not out.exists()
out.write_text(json.dumps(dict(passed=True,fixtures=records,ordinary_map_placement=True,raw_movement_state_writes=False),indent=2)+'\n',encoding='utf-8')
print('Prepared four mixed/traffic bridge maps; natural chain coverage still requires runtime evidence')
