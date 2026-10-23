"""All compilers use the shared probe directory sequentially."""
from pathlib import Path
import json, os, subprocess, sys
R = Path(__file__).resolve().parent
S = R / 'evidence/movement-state-v31'
def run(command, log):
    with (S / log).open('w', encoding='utf-8') as output:
        subprocess.run(command, cwd=R, check=True, stdout=output, stderr=subprocess.STDOUT,
                       env=dict(os.environ, PYTHONIOENCODING='utf-8'))
run(['pwsh', '-NoProfile', '-File', str(R / 'run_regressions_all_v31.ps1')], 'sequential-regressions.log')
run(['pwsh', '-NoProfile', '-File', str(R / 'build-joint-probe-v31.ps1')], 'final-build-joint.log')
names = ['sample-entry-probe', 'prepare-passage-entry-probe', 'object-passage-entry-probe', 'shared-return-plan-probe']
for phase, name in enumerate(names):
    run([str(S / 'joint_probe.exe'), str(R / 'ra2/game/game.exe'), str(phase)], name + '-verified-01.json')
run(['pwsh', '-NoProfile', '-File', str(R / 'build-overlap-probe-v31.ps1')], 'final-build-overlap.log')
for name in ['record_internal_receipt', 'record_connection_numeric_receipt', 'record_tube_state_receipt',
             'record_progress_receipt', 'record_travel_receipt', 'record_joint_receipt', 'record_overlap_receipt', 'record_round28_receipt', 'record_round29_receipt', 'record_round30_receipt', 'record_round31_receipt']:
    run([sys.executable, '-B', str(R / (name + '_v31.py'))], name + '.log')
receipts = list(S.glob('*-verified-01.json'))
assert len(receipts) == 105 and all(json.loads(p.read_text(encoding='utf-8-sig'))['passed'] for p in receipts)
value = dict(passed=True, groups=105, sequential_builds=True, new_cases=196608)
(S / 'native-gates.json').write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')
print(json.dumps(value))
