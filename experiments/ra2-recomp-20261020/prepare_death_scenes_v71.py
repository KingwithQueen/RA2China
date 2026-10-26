"""Native map tags and one explicit Cyborg control, with ordinary attacks only."""
from combat_batch_v71 import *
import re
def section(t,key,rows):
    pat=rf'(?ms)^\[{key}\]\n.*?(?=^\[|\Z)';new=f'[{key}]\n{rows}\n'
    return re.sub(pat,lambda _:new,t) if re.search(pat,t) else t+'\n'+new
base=R/'evidence/movement-state-v68/fixtures/stop-free.MAP';text=base.read_text(encoding='ascii')
for key,row in [('Triggers','99000001=BadGuy1 House,<none>,Damage notifications,0,1,1,1,0\n'),('Events','99000001=1,6,0,0\n'),('Actions','99000001=1,0,0,0,0,0,0,A\n'),('Tags','99000000=2,Damage notifications,99000001\n')]:
    assert f'[{key}]' not in text;text=section(text,key,row)
rule_path=Path(read(O/'scene-pending.json')['original_rules']);rules=rule_path.read_text(encoding='cp936');m=re.search(r'(?ms)^\[E2\]\n.*?(?=^\[|\Z)',rules);assert m
block=m[0];changed=re.sub(r'(?m)^Cyborg=.*$','Cyborg=yes',block) if re.search(r'(?m)^Cyborg=',block) else block.rstrip()+'\nCyborg=yes\n\n'
cyborg=S/'fixtures/rules-cyborg.ini';cyborg.write_text(rules[:m.start()]+changed+rules[m.end():],encoding='cp936',newline='\n')
items=[]
for tag,infantry,attached in [('truck',False,True),('infantry',True,True),('special',True,True),('unattached',True,False)]:
    target_tag='99000000' if attached else 'None'
    units='0=Player House,MTNK,256,80,112,0,Sleep,None,0,-1,0,-1,1,1\n'
    if not infantry:units+=f'1=BadGuy1 House,TRUCKA,256,86,112,0,Sleep,{target_tag},0,-1,0,-1,1,1\n'
    inf=f'0=BadGuy1 House,E2,256,86,112,2,Sleep,0,{target_tag},0,-1,0,1,1\n' if infantry else ''
    t=section(section(text,'Units',units),'Infantry',inf);p=S/'fixtures'/(tag+'.MAP');p.write_text(t,encoding='ascii',newline='\n')
    x=dict(tag=tag,path=p.relative_to(R).as_posix(),map_sha256=sha(p),attacker_cell=[80,112],target_cell=[86,112],last=900,orders=[],attached_tag=attached,special_control=tag=='special')
    if tag=='special':x.update(rules=cyborg.relative_to(R).as_posix(),rules_sha256=sha(cyborg))
    items.append(x)
write(S/'scene-pending.json',dict(passed=True,fixtures=items,original_rules=str(rule_path),original_rules_sha256=sha(rule_path),source_map=str(base),source_map_sha256=sha(base),tag_event=6,trigger_action=0,trigger_repetition=2,ordinary_native_map_tags=True,health_or_damage_memory_injection=False))
for folder,names in [('baseline-observer',['combat-observer.exe','combat_observer.c','death_generated.c']),('baseline-command',['combat-command.exe','combat_command.c'])]:
    dst=S/folder;dst.mkdir()
    for n in names:shutil.copy2(S/('observer-build/'+n if n=='death_generated.c' else n),dst/n)
    write(S/(folder+'.json'),dict(passed=True,files=[dict(path=str(dst/n),sha256=sha(dst/n)) for n in names],exe_sha256=sha(dst/names[0])))
print(dict(passed=True,new_scenes=4))
