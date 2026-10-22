"""Read-only verification after local commit; does not fetch, push or change Git state."""
from pathlib import Path
import hashlib,json,subprocess
R=Path(__file__).resolve().parent;P=R.parent.parent;S=R/'evidence/movement-state-v26'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
v=read(S/'validation.json');f=read(S/'final-check.json');assert v['passed'] and f['passed']
assert v['formal_baseline_generation']==25 and v['verification_round']==26
assert v['paired_scenes']==35 and v['paired_frames']==19505 and v['probes']==89
assert v['final_build_inputs_match_returns_checkpoint']
assert len(v['part_checkpoints'])==3 and all(p['scenes']==6 and p['frames']==3406 for p in v['part_checkpoints'].values())
assert v['new_fragment_cases']==262144 and not v['full_original_equivalence_verified']
exe=R/'ra2/build-original-c/ra2.exe';assert sha(exe)==v['exe_sha256']==f['exe_sha256']
for e in read(S/'source-manifest.json'):assert sha(R/e['path'])==sha(S/'final-source'/e['path'])==e['sha256'],e['path']
for name in ['latest-recovery.json','latest-state-comparison.json','latest-movement-candidate.json']:
 x=read(P/'reports'/name);assert Path(x['validation'])==S/'validation.json'
 assert x.get('sha256',x.get('exe_sha256'))==v['exe_sha256']
assert sha(Path(v['handoff']))==f['handoff_sha256'] and sha(Path(v['report']))==f['report_sha256']
assert read(S/'git-byte-audit.json')['passed']
status=subprocess.check_output(['git','status','--porcelain'],cwd=P);assert not status,status.decode('utf-8')
commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=P).decode('ascii').strip()
print(json.dumps(dict(passed=True,commit=commit,clean=True,exe_sha256=v['exe_sha256'],source_files=v['source_files'],pushed=False)))
