from pathlib import Path
import hashlib, json, subprocess
R = Path(__file__).resolve().parent
S = R / 'evidence/movement-state-v29'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
names = ['sample-cell-transition-probe', 'prepare-type-gate-probe', 'object-chain-probe', 'passage-shared-exits-probe']
results = {}
for phase, name in enumerate(names):
    result = subprocess.run([str(S / 'overlap_probe.exe'), str(R / 'ra2/game/game.exe'), str(phase)],
                            cwd=R, check=True, capture_output=True, text=True)
    value = json.loads(result.stdout)
    assert value['passed'] and value['phase'] == phase and value['cases'] == 65536
    (S / (name + '-verified-01.json')).write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')
    results[name] = value
sources = [S / 'overlap_probe.c', S / 'native_probe_host.h', R / 'build-overlap-probe-v29.ps1', R / 'make_overlap_probe_v29.py']
for directory, modules in [('gameplay', ['ground_template_transition', 'ground_object_chain', 'ground_template_entry', 'ground_passage_entry', 'ground_return_plan']),
                           ('runtime', ['ground_overlap_bridge', 'ground_joint_bridge'])]:
    for module in modules:
        sources += [R / f'ra2/src/{directory}/{module}.{ext}' for ext in ['c', 'h']]
value = dict(passed=True, total_cases=262144, results=results, original_sha256=sha(R / 'ra2/game/game.exe'),
             scope='Direct original 4A17FE cell comparison, 4A3502 type-dependent gate with mutable classification/owner callbacks, 703439 and 7038EF object-chain state, five original passage return entries. Complete runtime module coverage is not claimed.',
             stack_and_nonvolatile_registers_verified=True, callback_sequence_and_values_verified=True,
             probe_executable=dict(path=(S / 'overlap_probe.exe').relative_to(R).as_posix(), sha256=sha(S / 'overlap_probe.exe')),
             inputs=[dict(path=p.relative_to(R).as_posix(), sha256=sha(p)) for p in sources])
(S / 'native-overlap-identity.json').write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')
print(json.dumps(dict(passed=True, cases=262144)))
