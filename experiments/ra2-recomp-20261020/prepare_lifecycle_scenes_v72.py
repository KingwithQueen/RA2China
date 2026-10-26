from combat_batch_v72 import *
import re

def section(t,key,rows):
    pat=rf'(?ms)^\[{key}\]\n.*?(?=^\[|\Z)';new=f'[{key}]\n{rows}\n'
    return re.sub(pat,lambda _:new,t) if re.search(pat,t) else t+'\n'+new
base=O/'fixtures/truck-02.MAP';text=base.read_text(encoding='ascii');rule_path=Path(read(O/'scene-pending.json')['original_rules']);rules=rule_path.read_text(encoding='cp936')
def override(name,field,value,filename):
    match=re.search(rf'(?ms)^\[{name}\]\n.*?(?=^\[|\Z)',rules);assert match
    block=match[0];changed=re.sub(rf'(?m)^{field}=.*$',field+'='+value,block) if re.search(rf'(?m)^{field}=',block) else block.rstrip()+'\n'+field+'='+value+'\n\n'
    p=S/'fixtures'/filename;p.write_text(rules[:match.start()]+changed+rules[match.end():],encoding='cp936',newline='\n');return p
controls={'delayed':override('TRUCKA','DeathFrames','8','rules-deathframes.ini'),'nothuman':override('E2','NotHuman','yes','rules-nothuman.ini')}
items=[]
for tag in ['delayed','nothuman','electric','queue']:
    actors=[(80,112)];targets=[(86,112)];infantry=tag in ['nothuman','electric']
    if tag=='queue':actors=[(80,112),(80,113),(81,112),(81,113)];targets=[(86,112),(86,113),(87,112),(87,113)]
    units='';inf=''
    for i,(a,b) in enumerate(actors):
        if tag=='electric':inf+=f'{i}=Player House,SHK,256,{a},{b},2,Sleep,0,None,0,-1,0,1,1\n'
        else:units+=f'{i}=Player House,MTNK,256,{a},{b},0,Sleep,None,0,-1,0,-1,1,1\n'
    for i,(a,b) in enumerate(targets):
        if infantry:inf+=f'{i+len(actors)}=BadGuy1 House,E2,256,{a},{b},2,Sleep,0,99000000,0,-1,0,1,1\n'
        else:units+=f'{i+len(actors)}=BadGuy1 House,TRUCKA,256,{a},{b},0,Sleep,99000000,0,-1,0,-1,1,1\n'
    t=section(section(text,'Units',units),'Infantry',inf);p=S/'fixtures'/(tag+'.MAP');p.write_text(t,encoding='ascii',newline='\n')
    x=dict(tag=tag,path=p.relative_to(R).as_posix(),map_sha256=sha(p),attacker_cell=list(actors[0]),target_cell=list(targets[0]),attack_pairs=[(a,b) for a,b in zip(actors,targets)],last=1200,orders=[],new_scene=True)
    if tag in controls:x.update(rules=controls[tag].relative_to(R).as_posix(),rules_sha256=sha(controls[tag]))
    items.append(x)
for x in read(O/'qualified-scene-recipes.json')['fixtures']+[read(O/'extra-scene.json')['fixture']]:
    x=dict(x);x['orders']=[];x['new_scene']=False
    if x['tag']=='volley':x['attack_pairs']=[(a,x['target_cell']) for a in [(80,112),(80,113),(81,112)]]
    items.append(x)
write(S/'scene-pending.json',dict(passed=True,fixtures=items,original_rules=str(rule_path),original_rules_sha256=sha(rule_path),source_map=str(base),source_map_sha256=sha(base),ordinary_attacks_only=True,injected_damage_or_lifetime=False,trigger_country='BadGuy1',explicit_rule_controls=['DeathFrames=8','NotHuman=yes']))
for folder,names in [('baseline-observer',['combat-observer.exe','combat_observer.c','death_generated.c']),('baseline-command',['combat-command.exe','combat_command.c'])]:
    dst=S/folder;dst.mkdir()
    for n in names:shutil.copy2(S/('observer-build/'+n if n=='death_generated.c' else n),dst/n)
    write(S/(folder+'.json'),dict(passed=True,files=[dict(path=str(dst/n),sha256=sha(dst/n)) for n in names],exe_sha256=sha(dst/names[0])))
print(dict(passed=True,new_scenes=4,inherited_scenes=5))
