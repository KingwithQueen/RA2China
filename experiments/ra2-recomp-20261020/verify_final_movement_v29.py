"""Read-only post-commit verification; never rebuild, fetch or push."""
from pathlib import Path
import hashlib,json,subprocess
R=Path(__file__).resolve().parent;P=R.parent.parent;S=R/'evidence/movement-state-v29'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
v=read(S/'validation.json');f=read(S/'final-check.json')
assert v['passed'] and f['passed'] and v['formal_baseline_generation']==28 and v['verification_round']==29
assert v['paired_scenes']==48 and v['paired_frames']==28518 and v['probes']==99 and v['new_fragment_cases']==196608
assert v['content_inputs']==288 and v['production_c_sources']==171 and v['unsupported_guards']==37
assert v['combined_curved_height_occupied_runtime_verified'] and v['combined_curved_height_occupied_scenes']==4
assert v['original_equivalent_stall_scenes']==2 and not v['all_curved_height_routes_complete']
assert not v['nonprimary_overlapping_adapter_naturally_observed'] and not v['full_original_equivalence_verified']
assert v['final_build_inputs_match_returns_checkpoint']
assert len(v['part_checkpoints'])==3 and all(x['scenes']==6 and x['frames']==3406 for x in v['part_checkpoints'].values())
assert sha(R/'ra2/build-original-c/ra2.exe')==v['exe_sha256']==f['exe_sha256']
for e in read(S/'source-manifest.json'):assert sha(R/e['path'])==sha(S/'final-source'/e['path'])==e['sha256'],e['path']
for name in ['latest-recovery.json','latest-state-comparison.json','latest-movement-candidate.json']:
    x=read(P/'reports'/name);assert Path(x['validation'])==S/'validation.json'
    assert x.get('sha256',x.get('exe_sha256'))==v['exe_sha256']
assert sha(Path(v['handoff']))==f['handoff_sha256'] and sha(Path(v['report']))==f['report_sha256']
assert read(S/'git-byte-audit.json')['passed'] and read(S/'git-whitespace-audit.json')['passed']
assert read(S/'legal-overlap-sources.json')['passed']
assert read(S/'combined-real-scenes.json')['passed']
assert read(S/'bridge-real-scenes.json')['actual_ordered_three_object_traversal_verified']
assert v['bridge_upper_and_lower_three_object_traversal_verified']
assert v['serial_startup_retries_passed'] and read(S/'startup-failures.json')['failed_records_preserved']
assert v['system_interruption_recovered'] and v['interrupted_pairs_preserved']==2
resumption=read(S/'resumption-validation.json');assert resumption['passed']
for item in resumption['inputs']:assert sha(R/item['path'])==item['sha256'],item['path']
assert resumption['prior_part_scenes_reverified']==18 and resumption['prior_part_frames_reverified']==10218
assert sha(P/'.git/config')==read(S/'resumption-vcs-context.json')['config_sha256']
status=subprocess.check_output(['git','status','--porcelain'],cwd=P);assert not status,status.decode('utf-8')
commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=P,text=True).strip()
print(json.dumps(dict(passed=True,commit=commit,clean=True,exe_sha256=v['exe_sha256'],source_files=v['source_files'],pushed=False)))
