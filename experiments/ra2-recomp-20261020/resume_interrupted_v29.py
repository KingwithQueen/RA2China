"""Preserve interrupted files and resume only unfinished round-29 connection checks."""
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys

R = Path(__file__).resolve().parent
S = R / 'evidence/movement-state-v29'
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
production = sha(R / 'ra2/build-original-c/ra2.exe')
assert production == read(S / 'parts/returns-verified/validation.json')['exe_sha256']
receipt = read(R / 'ra2/build-original-c/source-content-receipt.json')
for path, digest in receipt['inputs'].items():
    assert sha(Path(path)) == digest, path

ledger = S / 'interruption-recovery.json'
if not ledger.exists():
    archive = S / 'investigations/system-interruption-01'
    assert not archive.exists()
    archive.mkdir(parents=True)
    entries = []
    for tag in ['z-tu', 'z-td']:
        source = S / 'runs' / tag
        assert not (source / 'comparison.json').exists(), tag
        assert source.resolve().is_relative_to(S.resolve()) and source.is_dir()
        files = [dict(path=p.relative_to(source).as_posix(), sha256=sha(p))
                 for p in sorted(source.rglob('*')) if p.is_file()]
        destination = archive / tag
        assert destination.resolve().is_relative_to(S.resolve()) and not destination.exists()
        source.rename(destination)
        for item in files:
            assert sha(destination / item['path']) == item['sha256']
        log = S / (tag + '.log')
        if log.exists():
            log.rename(destination / 'runner-interrupted.log')
            files.append(dict(path='runner-interrupted.log', sha256=sha(destination / 'runner-interrupted.log')))
        entries.append(dict(tag=tag, preserved_path=str(destination), files=files,
                            disposition='User-reported system blue screen; incomplete pair, no comparison receipt. Never accepted.'))
    ledger.write_text(json.dumps(dict(passed=True, production_exe_sha256=production,
        preserved_attempts=entries, accepted_interrupted_pairs=False), indent=2) + '\n', encoding='utf-8')
else:
    for entry in read(ledger)['preserved_attempts']:
        for item in entry['files']:
            assert sha(Path(entry['preserved_path']) / item['path']) == item['sha256']

for direction, goal, tag in [('east', 80, 'z-tu'), ('west', 66, 'z-td')]:
    report = S / 'runs' / tag / 'comparison.json'
    if not report.exists():
        command = [sys.executable, '-B', str(R / 'run_fixture_comparison.py'), '--tag', tag,
            '--evidence-stage', 'movement-state-v29', '--movement-audit', '--seconds', '240', '--range', '0:600',
            '--scenario-map', str(S / f'fixtures/tube-curved-tall-{direction}.MAP'),
            '--order', f'5:1022581:2:{goal}:114']
        with (S / (tag + '.log')).open('x', encoding='utf-8') as output:
            result = subprocess.run(command, cwd=R, stdout=output, stderr=subprocess.STDOUT,
                env=dict(os.environ, PYTHONIOENCODING='utf-8'))
        assert result.returncode == 0, tag
    value = read(report)
    assert value['passed'] and value['exe_sha256'] == production, tag
    assert value['comparison']['frames_compared'] == 601, tag
    print(json.dumps(dict(tag=tag, passed=True, frames=601)), flush=True)

results = []
for prefix in ['q-', 'z-']:
    for direction, goal, name in [('east', 80, 'tu'), ('west', 66, 'td')]:
        tag = prefix + name
        value = read(S / 'runs' / tag / 'comparison.json')
        assert value['passed'] and value['comparison']['frames_compared'] == 601
        last = None
        for line in (S / 'runs' / tag / 'original/state.jsonl').open(encoding='utf-8'):
            row = json.loads(line)
            if row['kind'] == 'state':
                last = next(o for o in row['objects'] if o['id'] == 1022581)
        completed = last['position'] == [goal * 256 + 128, 29312, 728 if direction == 'east' else 416]
        completed = completed and last['ground_drive']['destination'] == [0, 0, 0]
        assert completed == (direction == 'east'), tag
        results.append(dict(tag=tag, paired=True, frames=601, completed=completed, final_position=last['position']))
out = S / 'tall-curved-runtime.json'
assert not out.exists()
out.write_text(json.dumps(dict(passed=True, all_routes_complete=False, results=results), indent=2) + '\n', encoding='utf-8')

print(json.dumps(dict(starting='combined-scenes')), flush=True)
with (S / 'resumed-combined-scenes.log').open('x', encoding='utf-8') as output:
    result = subprocess.run([sys.executable, '-B', str(R / 'run_combined_routes_v29.py')],
        cwd=R, stdout=output, stderr=subprocess.STDOUT, env=dict(os.environ, PYTHONIOENCODING='utf-8'))
assert result.returncode == 0, 'combined-scenes'
assert read(S / 'combined-runs.json')['passed']
assert sha(R / 'ra2/build-original-c/ra2.exe') == production
print(json.dumps(dict(passed=True, completed='remaining-connection-scenes')), flush=True)
