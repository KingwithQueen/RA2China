from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json, os, subprocess, sys
R = Path(__file__).resolve().parent
S = R / 'evidence/movement-state-v28'
cases = [(observed, direction, goal) for observed in [True, False] for direction, goal in [('east', 80), ('west', 66)]]
def run(case):
    observed, direction, goal = case
    tag = ('q-' if observed else 'z-') + ('hu' if direction == 'east' else 'hd')
    script = 'run_connection_v28.py' if observed else 'run_fixture_comparison.py'
    args = ['--tag', tag, '--evidence-stage', 'movement-state-v28', '--movement-audit', '--seconds', '240', '--range', '0:600',
            '--scenario-map', str(S / f'fixtures/tube-cardinal-elevated-{direction}.MAP'), '--order', f'5:1022581:2:{goal}:114']
    with (S / (tag + '.log')).open('x', encoding='utf-8') as output:
        p = subprocess.run([sys.executable, '-B', str(R / script), *args], cwd=R, stdout=output, stderr=subprocess.STDOUT,
                           env=dict(os.environ, PYTHONIOENCODING='utf-8'))
    report = json.loads((S / 'runs' / tag / 'comparison.json').read_text(encoding='utf-8'))
    last = None
    for line in (S / 'runs' / tag / 'original/state.jsonl').open(encoding='utf-8'):
        row = json.loads(line)
        if row['kind'] == 'state':
            last = next(o for o in row['objects'] if o['id'] == 1022581)
    completed = last['position'] == [goal * 256 + 128, 29312, 624 if direction == 'east' else 416] and last['ground_drive']['destination'] == [0, 0, 0]
    value = dict(tag=tag, paired=p.returncode == 0 and report['passed'], frames=report['comparison']['frames_compared'],
                 completed=completed, final_position=last['position'])
    print(json.dumps(value), flush=True)
    return value
with ThreadPoolExecutor(max_workers=2) as pool:
    results = list(pool.map(run, cases))
(S / 'cardinal-curved-runtime.json').write_text(json.dumps(dict(passed=all(r['paired'] and r['completed'] for r in results), results=results), indent=2) + '\n', encoding='utf-8')
assert all(r['paired'] and r['completed'] for r in results), results
