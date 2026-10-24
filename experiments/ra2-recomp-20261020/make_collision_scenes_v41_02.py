"""Use bridge placements on the correct layer; start the train with a native map team."""
from pathlib import Path
import json,re,hashlib,configparser
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v41';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
old=json.loads((S/'collision-fixtures.json').read_text(encoding='utf-8'));items=[]
def replace_section(t,name,body):return re.sub(r'(?ms)^\['+re.escape(name)+r'\]\r?\n.*?(?=^\[|\Z)',lambda m:'['+name+']\n'+body+'\n\n',t)
for x in old['fixtures']:
 x=dict(x);t=(R/x['path']).read_bytes().decode('latin1')
 if x['name']=='crush':
  t=replace_section(t,'Infantry','0=BadGuy1 House,E2,256,60,66,2,Sleep,0,None,0,-1,1,1,1\n1=BadGuy1 House,E2,256,60,66,4,Sleep,0,None,0,-1,1,1,1')
 else:
  t=replace_section(t,'Units','0=BadGuy1 House,TRUCKA,256,60,62,128,Guard,None,0,-1,0,-1,1,1\n1=Player House,TRUCKB,256,60,66,0,Guard,None,0,-1,1,-1,1,1\n2=Player House,TRUCKB,256,60,66,0,Guard,None,0,-1,1,-1,1,1')
  t=replace_section(t,'Infantry','0=Player House,E2,256,60,66,2,Sleep,0,None,0,-1,1,1,1')
  original=configparser.ConfigParser(interpolation=None,strict=False);original.optionxform=str;original.read(R/'evidence/movement-state-v4/SOV01T-original.MAP',encoding='ascii')
  team=dict(original.items('09CCDC8C'));team.update(Name='Train contact',House='BadGuy1',Droppod='no',Full='no',Recruiter='yes',LooseRecruit='yes',Max='1',Waypoint='A',Script='41F00003',TaskForce='41F00002',AreTeamMembersRecruitable='no')
  t+='\n[TaskForces]\n0=41F00002\n[41F00002]\nName=Train contact\n0=1,TRUCKA\nGroup=-1\n[ScriptTypes]\n0=41F00003\n[41F00003]\nName=Train contact move\n0=3,99\n1=5,60\n[TeamTypes]\n0=41F00001\n[41F00001]\n'+''.join(k+'='+v+'\n' for k,v in team.items())
  t+='\n[Triggers]\n41F00004=BadGuy1,<none>,Train contact,0,1,1,1,0\n[Events]\n41F00004=1,13,0,0\n[Actions]\n41F00004=1,4,1,41F00001,0,0,0,0,A\n[Tags]\n41F00005=0,Train contact,41F00004\n'
  t=t.replace('[Waypoints]\n','[Waypoints]\n99=75060\n',1)
  t=re.sub(r'(?ms)(^\[Waypoints\]\n.*?)(?=^\[)',lambda m:re.sub(r'(?m)^0=\d+$','0=62060',m[0]),t)
  x['orders']=[];x['ordinary_native_team_script']=True
 p=S/'fixtures'/('bridge-'+x['name']+'-contact-02.MAP');assert not p.exists();p.write_bytes(t.encode('latin1'));x.update(path=p.relative_to(R).as_posix(),sha256=sha(p));items.append(x)
(S/'collision-fixtures-02.json').write_text(json.dumps(dict(passed=True,fixtures=items,original_rules_source=old['original_rules_source'],original_rules_sha256=old['original_rules_sha256'],prior_nonqualifying_recipe='collision-fixtures.json',correction='Targets must spawn on bridge layer. Train receives a native team movement script rather than a player command.'),indent=2)+'\n',encoding='utf-8')
t=(R/'trial_collision_v41.py').read_text(encoding='utf-8').replace("'baseline-'","'baseline02-'").replace("S/'collision-fixtures.json'","S/'collision-fixtures-02.json'").replace("S/'baseline-collision-runs.json'","S/'baseline-collision-runs-02.json'")
(R/'trial_collision_v41_02.py').write_text(t,encoding='utf-8',newline='\n')
print('Prepared second bounded collision pair')
