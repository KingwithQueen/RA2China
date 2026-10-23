"""Replace the rejected enemy player order with an original map team script."""
from pathlib import Path
import configparser,hashlib,json,re
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v31'
original=configparser.ConfigParser(interpolation=None,strict=False);original.optionxform=str
original.read(R/'evidence/movement-state-v4/SOV01T-original.MAP',encoding='ascii')
value=json.loads((S/'bridge-hostile-fixtures.json').read_text(encoding='utf-8'))
for item in value['fixtures']:
    if not item['dynamic']:continue
    direction=item['name'].rsplit('-',1)[1]
    text=(S/f'fixtures/bridge-enemy-traffic-{direction}.MAP').read_text(encoding='ascii')
    # House/country naming, TeamType keys and script action3 follow original map inputs.
    team=dict(original.items('09CCDC8C'))
    team.update(Name='Bridge enemy traffic',House='BadGuy1',Droppod='no',Full='no',Recruiter='yes',
        LooseRecruit='yes',Max='1',Waypoint='A',Script='31F00003',TaskForce='31F00002',AreTeamMembersRecruitable='no')
    goal=61 if direction=='north' else 72
    text+='\n[TaskForces]\n0=31F00002\n[31F00002]\nName=Bridge traffic\n0=1,TRUCKA\nGroup=-1\n'
    text+='\n[ScriptTypes]\n0=31F00003\n[31F00003]\nName=Bridge movement\n0=3,99\n1=5,60\n'
    text+='\n[TeamTypes]\n0=31F00001\n[31F00001]\n'+''.join(k+'='+v+'\n' for k,v in team.items())
    text+='\n[Triggers]\n31F00004=BadGuy1,<none>,Bridge enemy team,0,1,1,1,0\n'
    text+='\n[Events]\n31F00004=1,13,0,0\n[Actions]\n31F00004=1,4,1,31F00001,0,0,0,0,A\n'
    text+='\n[Tags]\n31F00005=0,Bridge enemy team,31F00004\n'
    pattern=r'(?m)^\[Waypoints\]\n';assert len(re.findall(pattern,text))==1
    text=re.sub(pattern,lambda _:f'[Waypoints]\n99={goal*1000+60}\n',text)
    start=71 if direction=='north' else 62
    text=re.sub(r'(?ms)(^\[Waypoints\]\n.*?)(?=^\[)',lambda m:re.sub(r'(?m)^0=\d+$',f'0={start*1000+60}',m[1]),text)
    name='enemy-traffic-ai3-'+direction;p=S/f'fixtures/bridge-{name}.MAP'
    assert not p.exists();p.write_text(text,encoding='ascii',newline='\n')
    item.update(name=name,path=p.relative_to(R).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),
        orders=[x for x in item['orders'] if ':1023363:' not in x],enemy_motion='native triggered CreateTeam plus script action3 to waypoint99')
value.update(enemy_player_orders=False,enemy_native_team_script=True)
(S/'bridge-hostile-fixtures.json').write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
print('Prepared native enemy-team traffic; actual recruitment and movement require runtime validation')
