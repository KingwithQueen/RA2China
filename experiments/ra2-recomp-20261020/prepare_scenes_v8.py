from pathlib import Path
import re
ROOT=Path(__file__).resolve().parent
S=ROOT/'evidence/movement-state-v8/fixtures'
base=(ROOT/'evidence/movement-state-v4/fixtures/empty.MAP').read_text(encoding='ascii')
def section(text,name,body):
    pattern=r'(?ms)^\['+re.escape(name)+r'\]\n.*?(?=^\[|\Z)'
    assert re.search(pattern,text)
    return re.sub(pattern,'['+name+']\n'+body+'\n\n',text)
def save(name,units,walls,extra=''):
    data=section(base,'Units',units)
    structures=['0=Player House,NAPOWR,256,62,114,0,None,1,0,1,0,0,None,None,None,0,0']
    for i,(x,y) in enumerate(sorted(walls),1):
        structures.append(f'{i}=Player House,NAWALL,256,{x},{y},0,None,1,0,1,0,0,None,None,None,0,0')
    data=section(data,'Structures','\n'.join(structures))+extra
    p=S/(name+'.MAP'); assert not p.exists(); p.write_text(data,encoding='ascii',newline='\n')
for radius in (2,3):
    walls={(67+dx,114+dy) for dx in range(-radius,radius+1) for dy in range(-radius,radius+1) if abs(dx)==radius or abs(dy)==radius}
    save('partial-ring-'+str(radius),'0=Player House,TRUCKA,256,67,114,64,Guard,None,0,-1,0,-1,1,1',walls)
route={(67,y) for y in range(111,115)}|{(x,111) for x in range(67,72)}
walls={(x,y) for x in range(66,73) for y in range(110,116)}-route
for i,(x,y) in enumerate([(68,111),(67,111),(69,111)]):
    units=f'0=Player House,TRUCKA,256,67,114,64,Guard,None,0,-1,0,-1,1,1\n1=BadGuy1 House,TRUCKA,256,{x},{y},64,Guard,None,0,-1,0,-1,1,1'
    save('turn-cloak-'+str(i),units,walls,'\n[TRUCKA]\nCloakable=yes\nCloakingSpeed=1\n')
# 大目标足迹：目标中心与最近可达边缘可能相隔超过二格。
data=section(base,'Units','0=Player House,TRUCKA,256,67,114,64,Guard,None,0,-1,0,-1,1,1')
data=section(data,'Structures','0=Player House,NAPOWR,256,62,114,0,None,1,0,1,0,0,None,None,None,0,0\n1=Player House,CAWASH07,256,70,108,0,None,1,0,1,0,0,None,None,None,0,0')
p=S/'large-target.MAP'; assert not p.exists(); p.write_text(data,encoding='ascii',newline='\n')
