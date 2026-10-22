"""最终指纹上的固定逐帧矩阵；最多同时运行两对原版/C，不覆盖旧证据。"""
import concurrent.futures
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STAGE = ROOT / 'evidence/movement-state-v4'
common = ['--evidence-stage', 'movement-state-v4', '--range', '0:3000', '--seconds', '360']
standard = ['--order', '2192:1032240:2:80:114', '--order', '2230:1032240:2:67:108',
            '--order', '2270:1032240:13:67:108', '--require-completed-stop']
congestion = []
for unit in [1032240, 1032241, 1032242, 1032243]:
    congestion += ['--order', f'2192:{unit}:2:70:118']
for unit in [1032240, 1032242]:
    congestion += ['--order', f'2350:{unit}:2:70:117']
for unit in [1032240, 1032241, 1032242, 1032243]:
    congestion += ['--order', f'2500:{unit}:13:70:118']
congestion += ['--require-completed-stop']
cases = [('final-idle', 'run_state_comparison.py', common)]
for i in ['01', '02']:
    cases += [(f'final-standard-{i}', 'run_state_comparison.py', common + standard),
              (f'final-congestion-{i}', 'run_state_comparison.py', common + congestion)]
fixture_common = ['--evidence-stage', 'movement-state-v4', '--movement-audit', '--seconds', '180']
cases += [
    ('final-wall', 'run_fixture_comparison.py', fixture_common + ['--range', '0:1000', '--scenario-map',
        str(STAGE / 'fixtures/budget-ring-owned.MAP'), '--order', '5:1022579:2:70:108', '--cell-catalog']),
    ('final-truck', 'run_fixture_comparison.py', fixture_common + ['--range', '0:300', '--scenario-map',
        str(STAGE / 'fixtures/dynamic-trucka.MAP'), '--order', '5:1022579:2:70:108', '--wall-ring', '30:1022579']),
    ('final-budget-natural', 'run_fixture_comparison.py', fixture_common + ['--range', '0:300', '--scenario-map',
        str(STAGE / 'fixtures/budget-stress.MAP'), '--order', '5:1022579:2:67:113', '--unit-ring', '7:1022579'])]

fingerprint = hashlib.sha256((ROOT / 'ra2/build-original-c/ra2.exe').read_bytes()).hexdigest()

def run(case):
    tag, script, arguments = case
    output = STAGE / (tag + '.log')
    with output.open('x', encoding='utf-8') as stream:
        result = subprocess.run([sys.executable, '-B', str(ROOT / script), '--tag', tag] + arguments,
            cwd=ROOT, stdout=stream, stderr=subprocess.STDOUT)
    report = json.loads((STAGE / 'runs' / tag / 'comparison.json').read_text(encoding='utf-8'))
    passed = result.returncode == 0 and report['passed'] and report['exe_sha256'] == fingerprint
    print(json.dumps({'tag': tag, 'passed': passed, 'frames': report.get('comparison', {}).get('frames_compared')}), flush=True)
    return {'tag': tag, 'passed': passed, 'exit_code': result.returncode}

with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    results = list(pool.map(run, cases))
report = {'exe_sha256': fingerprint, 'results': results, 'passed': all(item['passed'] for item in results)}
with (STAGE / 'matrix.json').open('x', encoding='utf-8') as stream:
    json.dump(report, stream, ensure_ascii=False, indent=2)
raise SystemExit(0 if report['passed'] else 1)
