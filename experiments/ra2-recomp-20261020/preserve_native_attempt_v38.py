"""Retain the failed parallel-build attempt before rebuilding sequentially."""
from pathlib import Path
import hashlib, json, shutil
R = Path(__file__).resolve().parent
S = R / 'evidence/movement-state-v38'
dest = S / 'investigations/native-build-attempt01'
assert not dest.exists()
dest.mkdir(parents=True)
paths = set(S.glob('*-verified-01.json'))
paths.update(p for p in S.glob('*.log') if p.name.startswith(('regression-', 'final-build-', 'all-regressions', 'advance-shared-build')))
manifest = []
for path in sorted(paths):
    shutil.copy2(path, dest / path.name)
    manifest.append(dict(name=path.name, sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
value = dict(passed=True, acceptance=False, reason='Two cl invocations shared object filenames; remainder C1083 and advance LNK1181. No production validation was accepted from the failed invocation. Sequential rebuild replaces the canonical receipts; this attempt is retained.',
             files=manifest)
(dest / 'receipt.json').write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')
(S / 'native-build-development.json').write_text(json.dumps(dict(
    retained_attempt=str(dest), accepted_attempt='Sequential final-native-gates', failure_kind='Shared intermediate build objects',
    simulation_difference=False), indent=2) + '\n', encoding='utf-8')
print('Preserved', len(paths), 'native build attempt files')
