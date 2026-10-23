"""Bind the retained interruption evidence to complete, strict replacement pairs."""
from pathlib import Path
import hashlib
import json

R = Path(__file__).resolve().parent
S = R / 'evidence/movement-state-v29'
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
production = sha(R / 'ra2/build-original-c/ra2.exe')
ledger = read(S / 'interruption-recovery.json')
assert ledger['passed'] and not ledger['accepted_interrupted_pairs']
assert ledger['production_exe_sha256'] == production
assert [e['tag'] for e in ledger['preserved_attempts']] == ['z-tu', 'z-td']
evidence = [S / 'interruption-recovery.json', Path(__file__), R / 'resume_interrupted_v29.py']
for entry in ledger['preserved_attempts']:
    directory = Path(entry['preserved_path'])
    assert directory.resolve().is_relative_to((S / 'investigations').resolve())
    assert not (directory / 'comparison.json').exists()
    for item in entry['files']:
        path = directory / item['path']
        assert sha(path) == item['sha256']
        evidence.append(path)
    replacement = read(S / 'runs' / entry['tag'] / 'comparison.json')
    comparison = replacement['comparison']
    assert replacement['passed'] and replacement['exe_sha256'] == production
    assert comparison['frames_compared'] == comparison['equal_frames'] == comparison['consecutive_equal_frames'] == 601
    assert comparison['first_difference'] is None and comparison['command_difference'] is None
    assert comparison['rng_equal_all_frames'] and comparison['negative_control']['passed']
    assert comparison['negative_control']['missing_frame_rejected']
    assert all(r['passed'] and r['exit_code'] == 0 and r['save_before_sha256'] == r['save_after_sha256']
               for r in replacement['runs'])
    evidence.append(S / 'runs' / entry['tag'] / 'comparison.json')

permission = S / 'investigations/resume-link-permission-01'
receipt = read(permission / 'receipt.json')
assert receipt['passed'] and not receipt['simulation_started']
assert not list(permission.rglob('state.jsonl')) and not list(permission.rglob('command.json'))
assert 'PermissionError: [WinError 5]' in (permission / 'runner.log').read_text(encoding='utf-8')
for item in receipt['files']:
    assert sha(permission / item['path']) == item['sha256']
evidence += [permission / 'receipt.json', permission / 'runner.log']
tall = read(S / 'tall-curved-runtime.json')
assert tall['passed'] and not tall['all_routes_complete']
assert len(tall['results']) == 4 and sum(r['completed'] for r in tall['results']) == 2
assert read(S / 'combined-runs.json')['passed'] and read(S / 'combined-real-scenes.json')['passed']
evidence += [S / 'tall-curved-runtime.json', S / 'combined-runs.json', S / 'combined-real-scenes.json']
part_scenes = 0
part_frames = 0
for name in ['template-verified', 'passage-verified', 'returns-verified']:
    checkpoint = S / 'parts' / name / 'validation.json'
    part = read(checkpoint)
    assert part['passed'] and len(part['scenes']) == 6
    evidence.append(checkpoint)
    for scene in part['scenes']:
        directory = S / 'runs' / scene['tag']
        report = read(directory / 'comparison.json')
        comparison = report['comparison']
        assert report['passed'] and report['exe_sha256'] == scene['exe_sha256']
        assert comparison['frames_compared'] == comparison['equal_frames'] == comparison['consecutive_equal_frames'] == scene['frames']
        assert comparison['first_difference'] is None and comparison['command_difference'] is None
        assert comparison['rng_equal_all_frames'] and comparison['negative_control']['passed']
        assert comparison['negative_control']['missing_frame_rejected']
        traces = []
        for run in report['runs']:
            assert run['passed'] and run['exit_code'] == 0
            assert run.get('save_before', run.get('save_before_sha256')) == run.get('save_after', run.get('save_after_sha256'))
            trace = directory / run['mode'] / 'state.jsonl'
            records = [json.loads(line) for line in trace.open(encoding='utf-8')]
            states = [r for r in records if r['kind'] == 'state']
            assert len(states) == scene['frames']
            assert [r['frame'] for r in states] == list(range(states[0]['frame'], states[-1]['frame'] + 1))
            events = [r for r in records if r['kind'] in ['submit', 'execute', 'movement-audit'] or r['kind'].startswith('fixture-')]
            traces.append((states, events))
            evidence.append(trace)
        assert len(traces) == 2 and traces[0] == traces[1], scene['tag']
        evidence.append(directory / 'comparison.json')
        part_scenes += 1
        part_frames += scene['frames']
assert part_scenes == 18 and part_frames == 10218
out = S / 'resumption-validation.json'
assert not out.exists()
value = dict(passed=True, production_exe_sha256=production, incomplete_pairs_preserved=2,
    interrupted_pairs_never_accepted=True, production_unchanged_during_resumption=True,
    prelaunch_permission_failure_preserved=True, replacements_strictly_passed=True,
    prior_part_scenes_reverified=part_scenes, prior_part_frames_reverified=part_frames,
    original_height_anomalies_preserved=True,
    scope='Two incomplete pairs after the user-reported system blue screen were archived and replaced. '
          'One restricted-process resource-link failure happened before game launch; its evidence is retained. '
          'The replacement pairs and four height/occupied-exit combinations passed the unchanged comparator. '
          'This receipt makes no diagnosis of the system crash.',
    inputs=[dict(path=p.relative_to(R).as_posix(), sha256=sha(p)) for p in evidence])
out.write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')
print(json.dumps(dict(passed=True, incomplete_pairs_preserved=2, strict_replacements=True)))
