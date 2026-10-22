from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
STAGE = ROOT/'evidence/movement-state-v7'
common = ['--evidence-stage','movement-state-v7','--movement-audit','--seconds','240','--range','0:600']
cases = [
    ('final-slope-damaged',['--scenario-map',str(STAGE/'fixtures/slope-damaged.MAP'),
        '--order','5:1022579:2:98:125','--order','250:1022579:2:94:120','--order','500:1022579:13:94:120',
        '--require-completed-stop']),
    ('final-chrono-team-reference',['--scenario-map',str(STAGE/'fixtures/chrono-team-reference.MAP')]),
]
orders = []
for uid in range(1022579,1022583):
    orders += ['--order',f'5:{uid}:2:70:118']
for uid in (1022579,1022581):
    orders += ['--order',f'163:{uid}:2:70:117']
for uid in range(1022579,1022583):
    orders += ['--order',f'313:{uid}:13:70:118']
cases += [('final-zero-delay',['--scenario-map',str(ROOT/'evidence/movement-state-v5/fixtures/rapid-obstructed.MAP'),
    '--scenario-rules',str(ROOT/'evidence/movement-state-v5/fixtures/rules-zero-delay.ini')]+orders+['--require-completed-stop'])]
fingerprint = hashlib.sha256((ROOT/'ra2/build-original-c/ra2.exe').read_bytes()).hexdigest()

def run(case):
    tag,args = case
    with (STAGE/(tag+'.log')).open('x',encoding='utf-8') as stream:
        code = subprocess.run([sys.executable,'-B',str(ROOT/'run_fixture_comparison.py'),'--tag',tag]+common+args,
            cwd=ROOT,stdout=stream,stderr=subprocess.STDOUT).returncode
    path = STAGE/'runs'/tag/'comparison.json'
    report = json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}
    result = dict(tag=tag,exit_code=code,passed=code==0 and report.get('passed',False)
        and report.get('exe_sha256')==fingerprint,frames=report.get('comparison',{}).get('equal_frames',0))
    print(json.dumps(result),flush=True)
    return result

with ThreadPoolExecutor(max_workers=2) as pool:
    results = list(pool.map(run,cases))
report = dict(passed=all(r['passed'] for r in results),exe_sha256=fingerprint,results=results)
assert not (STAGE/'additional-matrix.json').exists()
(STAGE/'additional-matrix.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
raise SystemExit(0 if report['passed'] else 1)
