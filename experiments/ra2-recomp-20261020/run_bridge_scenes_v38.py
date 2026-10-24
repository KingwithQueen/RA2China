"""Bounded production/independent-observer pairs, ordinary move orders only."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import argparse,json,subprocess,sys
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v38'
ap=argparse.ArgumentParser();ap.add_argument('mode',choices=['production','observer']);ap.add_argument('--only',nargs='+');a=ap.parse_args()
recipes=json.loads((S/'bridge-fixtures.json').read_text(encoding='utf-8'))['fixtures']
if a.only:recipes=[r for r in recipes if r['name'] in a.only]
script='run_fixture_comparison.py' if a.mode=='production' else 'run_connection_v38.py'
prefix='b' if a.mode=='production' else 'h3'
def run(item):
 tag=prefix+'-'+item['name'];goal=item['goal']
 command=[sys.executable,'-X','utf8','-B',str(R/script),'--tag',tag,'--evidence-stage','movement-state-v38',
 '--movement-audit','--seconds','240','--range','0:900','--scenario-map',str(R/item['path']),
 '--order',f"5:{item['id']}:2:{goal[0]}:{goal[1]}"]
 with (S/(tag+'.log')).open('x',encoding='utf-8') as output:p=subprocess.run(command,cwd=R,stdout=output,stderr=subprocess.STDOUT)
 report=S/'runs'/tag/'comparison.json';value=json.loads(report.read_text(encoding='utf-8')) if report.exists() else {}
 assert p.returncode==0 and value.get('passed'),tag
 print(json.dumps(dict(passed=True,tag=tag,frames=value['comparison']['frames_compared'])),flush=True)
with ThreadPoolExecutor(max_workers=1) as pool:list(pool.map(run,recipes))

# 核心路仍归此进程；步兵组完成后才发出 core-scenes-complete。
if a.mode=='observer' and not a.only and json.loads((S/'observer-lane-assignment.json').read_text(encoding='utf-8')).get('bridge_infantry_on_core_lane'):
    subprocess.run([sys.executable,'-X','utf8','-B',str(R/'complete_core_infantry_v38.py')],cwd=R,check=True)
