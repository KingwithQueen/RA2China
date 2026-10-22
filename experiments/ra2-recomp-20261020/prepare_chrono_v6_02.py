"""保留失败地图，使用原版键名大小写建立第二次援军试验。"""
from pathlib import Path
import configparser

ROOT = Path(__file__).resolve().parent
base = (ROOT / 'evidence/movement-state-v4/fixtures/empty.MAP').read_text(encoding='ascii')
original = configparser.ConfigParser(interpolation=None, strict=False)
original.optionxform = str
original.read(ROOT / 'evidence/movement-state-v4/SOV01T-original.MAP', encoding='ascii')
team = dict(original.items('09CCDC8C'))
team.update(Name='Chrono budget investigation', Droppod='no', House='Player', Max='1',
            Waypoint='A', Script='06F00003', TaskForce='06F00002', Reinforce='no', Suicide='no')
base += '\n[TaskForces]\n0=06F00002\n[06F00002]\nName=Chrono HTNK\n0=1,HTNK\nGroup=-1\n'
base += '\n[ScriptTypes]\n0=06F00003\n[06F00003]\nName=Move to B\n0=3,1\n1=5,60\n'
base += '\n[TeamTypes]\n0=06F00001\n[06F00001]\n' + ''.join(k+'='+v+'\n' for k,v in team.items())
base += '\n[Triggers]\n06F00004=Player,<none>,Chrono trial,0,1,1,1,0\n'
base += '\n[Events]\n06F00004=1,13,0,3\n[Actions]\n06F00004=1,107,0,06F00001,0,0,0,0,A\n'
base += '\n[Waypoints]\n0=114071\n1=108071\n'
target = ROOT / 'evidence/movement-state-v6/fixtures/chrono-team-02.MAP'
assert not target.exists()
target.write_text(base, encoding='ascii', newline='\n')
