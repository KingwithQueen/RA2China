"""Default rifle/armor and V3 splash combat, plus one explicit edge-multiplier control."""
from combat_batch_v70 import *
import re
def replace_section(t,k,rows):
    pat=rf'(?ms)^\[{k}\]\n.*?(?=^\[|\Z)';assert re.search(pat,t)
    return re.sub(pat,lambda _:f'[{k}]\n{rows}\n',t)
base=R/'evidence/movement-state-v68/fixtures/stop-free.MAP';text=base.read_text(encoding='ascii')
rules_path=Path(read(O/'scene-pending.json')['original_rules']);rules=rules_path.read_text(encoding='cp936')
m=re.search(r'(?ms)^\[V3WH\]\n.*?(?=^\[|\Z)',rules);assert m
block=m[0];assert 'PercentAtMax=.25' in block;flat=rules[:m.start()]+block.replace('PercentAtMax=.25','PercentAtMax=1')+rules[m.end():]
p=S/'fixtures/rules-flat.ini';p.write_text(flat,encoding='cp936',newline='\n')
definitions=[dict(tag='rifle',units=[('BadGuy1 House','MTNK',256,85,112)],infantry=[('Player House','E1',256,80,112)],attacker_cell=[80,112],target_cell=[85,112],kind='default-SA-versus-heavy'),dict(tag='splash',units=[('Player House','V3',256,80,112)]+[('BadGuy1 House','TRUCKA',256,x,y) for x,y in [(86,112),(86,113),(87,112),(87,113),(88,112)]],infantry=[],attacker_cell=[80,112],target_cell=[86,112],kind='default-V3WH-multiple-distances')]
definitions.append(dict(definitions[1],tag='flat',kind='explicit-PercentAtMax-one-control',rules=p.relative_to(R).as_posix(),rules_sha256=sha(p)))
catalog=R/'evidence/movement-state-v67/runs/traffic-rq/original/cells.json';cells={tuple(c['cell']):c for c in read(catalog)['cells']}
for x in definitions:
    points=[(z[3],z[4]) for z in x['units']+x['infantry']]
    for pt in points:
        c=cells[pt];assert c['land'] in [0,1,6,7] and c['level']==4 and pt[1]-pt[0]<51,(pt,c)
    u=''.join(f'{i}={o},{n},{hp},{cx},{cy},0,Sleep,None,0,-1,0,-1,1,1\n' for i,(o,n,hp,cx,cy) in enumerate(x['units']))
    f=''.join(f'{i}={o},{n},{hp},{cx},{cy},2,Sleep,0,None,0,-1,0,1,1\n' for i,(o,n,hp,cx,cy) in enumerate(x['infantry']))
    t=replace_section(replace_section(text,'Units',u),'Infantry',f)
    strip=lambda v:replace_section(replace_section(v,'Units',''),'Infantry','');assert strip(t)==strip(text)
    p=S/'fixtures'/(x['tag']+'.MAP');p.write_text(t,encoding='ascii',newline='\n')
    x.update(path=p.relative_to(R).as_posix(),map_sha256=sha(p),orders=[],last=1500,points=[cells[z] for z in points])
write(S/'scene-pending.json',dict(passed=True,fixtures=definitions,original_rules=str(rules_path),original_rules_sha256=sha(rules_path),source_map=str(base),source_map_sha256=sha(base),native_commands_only=True,damage_or_health_memory_injection=False))
for folder,names in [('baseline-observer',['combat-observer.exe','combat_observer.c','damage_generated.c']),('baseline-command',['combat-command.exe','combat_command.c'])]:
    dst=S/folder;dst.mkdir()
    for n in names:shutil.copy2(S/('observer-build/'+n if n=='damage_generated.c' else n),dst/n)
    write(S/(folder+'.json'),dict(passed=True,files=[dict(path=str(dst/n),sha256=sha(dst/n)) for n in names],exe_sha256=sha(dst/names[0])))
print(dict(passed=True,scenes=len(definitions)))
