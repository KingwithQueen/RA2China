"""第九批：实际分支命中记录与逐帧状态同时比较，保留所有未通过记录。"""
from pathlib import Path
import concurrent.futures
import hashlib
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
STAGE = ROOT / 'evidence/movement-state-v31'
OLD = ROOT / 'evidence/movement-state-v4'
FIXTURES = STAGE / 'fixtures'
FIXTURES.mkdir(exist_ok=True)
for land in ('Rock', 'Clear'):
    path = FIXTURES / ('restricted-' + land.lower() + '.MAP')
    if not path.exists():
        path.write_bytes((OLD / 'fixtures/dynamic-trucka.MAP').read_bytes()
            + ('\r\n[TRUCKA]\r\nMovementRestrictedTo=' + land + '\r\n').encode('ascii'))

common = ['--evidence-stage', 'movement-state-v31', '--movement-audit', '--seconds', '240']
standard = ['--order', '2192:1032240:2:80:114', '--order', '2230:1032240:2:67:108',
            '--order', '2270:1032240:13:67:108', '--require-completed-stop']
congestion = []
for uid in range(1032240, 1032244):
    congestion += ['--order', f'2192:{uid}:2:70:118']
for uid in [1032240, 1032242]:
    congestion += ['--order', f'2350:{uid}:2:70:117']
for uid in range(1032240, 1032244):
    congestion += ['--order', f'2500:{uid}:13:70:118']
congestion += ['--require-completed-stop']
cases = []
for tag, commands in [('standard-01',standard), ('congestion-01',congestion)]:
    cases.append((tag, 'run_state_comparison.py', common + ['--range','2190:3000'] + commands))
fixture_cases = [
    ('restricted-rock', FIXTURES/'restricted-rock.MAP', '0:300', ['--order','5:1022579:2:70:108']),
    ('restricted-clear', FIXTURES/'restricted-clear.MAP', '0:300', ['--order','5:1022579:2:70:108']),
    ('wall', OLD/'fixtures/budget-ring-owned.MAP', '0:1000', ['--order','5:1022579:2:70:108']),
    ('gate', OLD/'fixtures/allied-gate-owned.MAP', '0:700', ['--order','5:1022579:2:67:108']),
    ('truck', OLD/'fixtures/dynamic-trucka.MAP', '0:300', ['--order','5:1022579:2:70:108','--wall-ring','30:1022579']),
    ('budget-natural', OLD/'fixtures/budget-stress.MAP', '0:300', ['--order','5:1022579:2:67:113','--unit-ring','7:1022579']),
    ('budget-entry', OLD/'fixtures/empty.MAP', '0:100', ['--budget-entry','5:1022579']),
]
for tag, path, span, commands in fixture_cases:
    cases.append((tag,'run_fixture_comparison.py',common+['--range',span,'--scenario-map',str(path)]+commands))
cases += [('cloaked-corridor','run_fixture_comparison.py',common+['--range','0:600','--scenario-map',
    str(FIXTURES/'cloaked-corridor.MAP'),'--order','150:1022579:2:67:108'])]
for name in ('healthy','damaged'):
    cases.append(('slope-'+name,'run_fixture_comparison.py',common+['--range','0:600','--scenario-map',
        str(FIXTURES/('slope-'+name+'.MAP')),'--order','5:1022579:2:98:125',
        '--order','250:1022579:2:94:120','--order','500:1022579:13:94:120','--require-completed-stop']))
cases.append(('chrono-team-reference','run_fixture_comparison.py',common+['--range','0:600',
    '--scenario-map',str(FIXTURES/'chrono-team-reference.MAP')]))
zero_orders=[]
for uid in range(1022579,1022583):
    zero_orders += ['--order',f'5:{uid}:2:70:118']
for uid in (1022579,1022581):
    zero_orders += ['--order',f'163:{uid}:2:70:117']
for uid in range(1022579,1022583):
    zero_orders += ['--order',f'313:{uid}:13:70:118']
cases.append(('zero-delay','run_fixture_comparison.py',common+['--range','0:600','--scenario-map',
    str(ROOT/'evidence/movement-state-v5/fixtures/rapid-obstructed.MAP'),'--scenario-rules',
    str(ROOT/'evidence/movement-state-v5/fixtures/rules-zero-delay.ini')]+zero_orders+['--require-completed-stop']))
cases.append(('chrono-seam-budget','run_fixture_comparison.py',common+['--range','0:600',
    '--scenario-map',str(FIXTURES/'chrono-team-reference.MAP'),'--order','10:1022584:2:70:108',
    '--order','70:1022584:2:70:108','--order','180:1022584:2:70:108','--wall-ring','100:1022584']))
fingerprint = hashlib.sha256((ROOT/'ra2/build-original-c/ra2.exe').read_bytes()).hexdigest()
prefix = sys.argv[1] if len(sys.argv) > 1 else ''
resume = '--resume' in sys.argv[2:]
cases = [(prefix + tag, script, args) for tag, script, args in cases]

def run(case):
    tag, script, args = case
    previous = STAGE/'runs'/tag/'comparison.json'
    if resume and previous.exists():
        report = json.loads(previous.read_text(encoding='utf-8'))
        assert report['passed'] and report['exe_sha256'] == fingerprint
        record = dict(tag=tag, exit_code=0, passed=True,
                      frames=report['comparison']['frames_compared'])
        print(json.dumps(record), flush=True)
        return record
    with (STAGE/(tag+'.log')).open('x',encoding='utf-8') as stream:
        result = subprocess.run([sys.executable,'-B',str(ROOT/script),'--tag',tag]+args,
            cwd=ROOT,stdout=stream,stderr=subprocess.STDOUT)
    path = STAGE/'runs'/tag/'comparison.json'
    report = json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}
    record = dict(tag=tag, exit_code=result.returncode, passed=result.returncode==0 and report.get('passed',False)
        and report.get('exe_sha256')==fingerprint, frames=report.get('comparison',{}).get('frames_compared',0))
    print(json.dumps(record),flush=True)
    return record

with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
    results = list(pool.map(run,cases))
report = dict(exe_sha256=fingerprint, results=results, passed=all(r['passed'] for r in results))
(STAGE/(prefix+'matrix.json')).write_text(json.dumps(report,indent=2),encoding='utf-8')
raise SystemExit(0 if report['passed'] else 1)
