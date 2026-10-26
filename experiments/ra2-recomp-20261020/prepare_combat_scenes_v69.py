"""Ordinary attacks and engineer-loaded IFV repair; explicit immunity control rule."""
from combat_batch_v69 import *
import re
def section(t,key,rows):
    pattern=rf'(?ms)^\[{key}\]\n.*?(?=^\[|\Z)';new='['+key+']\n'+rows+'\n'
    return re.sub(pattern,lambda _:new,t) if re.search(pattern,t) else t+'\n'+new
source=O/'fixtures/stop-free.MAP';t=source.read_text(encoding='ascii');catalog=R/'evidence/movement-state-v67/runs/traffic-rq/original/cells.json';cells={tuple(c['cell']):c for c in read(catalog)['cells']}
definitions=[dict(tag='tank',units=[('Player House','MTNK',256,80,112),('BadGuy1 House','TRUCKA',256,86,112)],infantry=[],kind='lethal-vehicle'),dict(tag='infantry',units=[('Player House','MTNK',256,80,112)],infantry=[('BadGuy1 House','E2',256,86,112)],kind='lethal-infantry'),dict(tag='repair',units=[('Player House','FV',256,80,112),('Player House','MTNK',128,85,112)],infantry=[('Player House','ENGINEER',256,80,113)],kind='ordinary-IFV-repair')]
definitions.append(dict(definitions[0],tag='immune',kind='explicit-immune-rule-control'))
rule_path=Path(read(O/'scene-recipes-pending.json')['rules_original']);rules=rule_path.read_text(encoding='cp936')
m=re.search(r'(?ms)^\[TRUCKA\]\n.*?(?=^\[|\Z)',rules);assert m
block=m[0]
if re.search(r'(?m)^Immune=',block):new=re.sub(r'(?m)^Immune=.*$', 'Immune=yes',block)
else:new=block.rstrip()+'\nImmune=yes\n\n'
immune=rules[:m.start()]+new+rules[m.end():];rp=S/'fixtures/rules-immune.ini';rp.write_text(immune,encoding='cp936',newline='\n')
items=[]
for x in definitions:
    points=[(z[3],z[4]) for z in x['units']+x['infantry']]
    assert len(set(points))==len(points)
    for p in points:
        c=cells[p];assert c['land'] in [0,1,6,7] and c['level']==4,(x['tag'],p,c)
        assert p[1]-p[0]<51
    units=''.join(f'{i}={o},{n},{hp},{cx},{cy},0,Sleep,None,0,-1,0,-1,1,1\n' for i,(o,n,hp,cx,cy) in enumerate(x['units']))
    infantry=''.join(f'{i}={o},{n},{hp},{cx},{cy},2,Sleep,0,None,0,-1,0,1,1\n' for i,(o,n,hp,cx,cy) in enumerate(x['infantry']))
    out=section(section(t,'Units',units),'Infantry',infantry);p=S/'fixtures'/(x['tag']+'.MAP');p.write_text(out,encoding='ascii',newline='\n')
    strip=lambda z:section(section(z,'Units',''),'Infantry','');assert strip(out)==strip(t)
    x.update(path=p.relative_to(R).as_posix(),map_sha256=sha(p),last=1500,orders=[],source=str(source),source_sha256=sha(source),points=[cells[p] for p in points])
    if x['tag']=='immune':x['rules']=rp.relative_to(R).as_posix()
    items.append(x)
write(S/'scene-pending.json',dict(passed=True,fixtures=items,original_rules=str(rule_path),original_rules_sha256=sha(rule_path),immune_rule_sha256=sha(rp),natural_commands_only=True,engine_damage_or_health_injection=False))
old="exe = ROOT / 'ra2/build-original-c/ra2.exe'"
wrapper='from pathlib import Path\nR=Path(__file__).resolve().parent\nsource=(R/\'run_fixture_comparison.py\').read_text(encoding=\'utf-8\')\nold='+repr(old)+'\nassert source.count(old)==1\nsource=source.replace(old,'+repr("exe = ROOT / 'evidence/combat-state-v1/combat-observer.exe'")+")\nexec(compile(source,str(R/'run_fixture_comparison.py'),'exec'),dict(__file__=str(R/'run_fixture_comparison.py'),__name__='__main__'))\n"
(R/'run_combat_observer_v69.py').write_text(wrapper,encoding='utf-8')
print(dict(passed=True,recipes=4,positions_prechecked=True))
