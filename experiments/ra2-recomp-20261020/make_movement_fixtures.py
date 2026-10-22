"""从只读原版地形制作独立试验地图，使用原版 INI 对象创建流程。"""
import re
from pathlib import Path
ROOT = Path(__file__).resolve().parent
STAGE = ROOT / 'evidence/movement-state-v4'
text = (STAGE / 'SOV01T-original.MAP').read_text(encoding='ascii')
sections = re.split(r'(?m)^\[([^]\r\n]+)\]\s*$', text)
data = dict(zip(sections[1::2], sections[2::2]))
keep = ['Countries', 'Player', 'BadGuy1', 'BadGuy2', 'BadGuy3', 'Civilian1', 'Other1', 'Other2', 'Other3',
        'Houses', 'Player House', 'BadGuy1 House', 'BadGuy2 House', 'BadGuy3 House', 'Civie1 House',
        'Other1 House', 'Other2 House', 'Other3 House', 'Map', 'IsoMapPack5', 'Lighting']
base = ''.join('[' + key + ']\n' + data[key].strip() + '\n\n' for key in keep)
base += '''[Basic]
NewINIFormat=4
Name=Ground movement validation
Player=Player House
Intro=<none>
Brief=<none>
Win=<none>
Lose=<none>
Action=<none>
PostScore=<none>
PreMapSelect=<none>
OneTimeOnly=yes
IgnoreGlobalAITriggers=yes
FreeRadar=yes
TiberiumGrowthEnabled=no
VeinGrowthEnabled=no
IceGrowthEnabled=no
InitTime=0
\n[Waypoints]
98=114067
0=114067
\n'''
# 第一张只检查地图装载、对象建立及真实地形；后续墙体/闸门试验另存文件。
units = '[Units]\n0=Player House,HTNK,256,67,114,64,Guard,None,0,-1,0,-1,1,1\n\n'
structures = '[Structures]\n0=Player House,NAPOWR,256,62,114,0,None,1,0,1,0,0,None,None,None,0,0\n\n'
fixtures = STAGE / 'fixtures'
fixtures.mkdir(exist_ok=True)
target = fixtures / 'empty.MAP'
assert not target.exists()
target.write_text(base + units + structures, encoding='ascii', newline='\n')
# 将当前公共运行器复制为专用地图运行器，不更改已发布的 v3 回放逻辑。
runner = (ROOT / 'run_state_comparison.py').read_text(encoding='utf-8')
runner = runner.replace("ap.add_argument('--tag', required=True)", "ap.add_argument('--tag', required=True)\n    ap.add_argument('--scenario-map', type=Path, required=True)")
runner = runner.replace("script = test.SP().press(test.SINGLE, 'LoadSavedGame', 0xB7).select(0xB7, 1317, 0).press(0xB7, 'Load').waitlog(test.INGAME)",
    "script = test.SP().press(test.SINGLE, 'NewCampaign', test.CAMPAIGN).press(test.CAMPAIGN, 1772).waitlog(test.INGAME)")
runner = runner.replace("save = game / 'SAVE0029.SAV'", "(game / 'SOV01T.MAP').write_bytes(args.scenario_map.read_bytes())\n        save = game / 'SAVE0029.SAV'")
runner = runner.replace("'seed': 12345, 'runs': runs,", "'seed': 12345, 'scenario_map': str(args.scenario_map), 'scenario_sha256': sha(args.scenario_map), 'runs': runs,")
target = ROOT / 'run_fixture_comparison.py'
assert not target.exists()
target.write_text(runner, encoding='utf-8', newline='\n')
print('Created isolated fixture map and runner')
