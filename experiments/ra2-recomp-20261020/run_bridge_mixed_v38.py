"""Bounded mixed bridge scenes; each saved pair keeps its own private resources."""
from pathlib import Path
import argparse,json,subprocess,sys
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v38'
ap=argparse.ArgumentParser();ap.add_argument('mode',choices=['production','observer']);ap.add_argument('--only',nargs='+');a=ap.parse_args()
recipes=json.loads((S/'bridge-mixed-fixtures.json').read_text(encoding='utf-8'))['fixtures']
for item in recipes:
    if a.only and item['name'] not in a.only:continue
    tag=('mh-' if a.mode=='observer' else 'mp-')+item['name']
    report=S/'runs'/tag/'comparison.json'
    if report.exists():
        value=json.loads(report.read_text(encoding='utf-8'));assert value['passed'],tag
        print(json.dumps(dict(tag=tag,passed=True,retained_verified_pair=True)),flush=True);continue
    script='run_connection_v38.py' if a.mode=='observer' else 'run_fixture_comparison.py'
    args=[sys.executable,'-X','utf8','-B',str(R/script),'--tag',tag,'--evidence-stage','movement-state-v38',
        '--movement-audit','--seconds','240','--range','0:900','--scenario-map',str(R/item['path'])]
    for order in item['orders']:args+=['--order',order]
    with (S/(tag+'.log')).open('x',encoding='utf-8') as output:
        result=subprocess.run(args,cwd=R,stdout=output,stderr=subprocess.STDOUT)
    value=json.loads(report.read_text(encoding='utf-8')) if report.exists() else {}
    assert result.returncode==0 and value.get('passed'),tag
    print(json.dumps(dict(tag=tag,passed=True,frames=value['comparison']['frames_compared'])),flush=True)
