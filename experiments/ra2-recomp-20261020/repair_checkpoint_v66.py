"""Rebind the retained tested phase from its archived receipt, without changing current code."""
from run_batch_v66 import *
src=S/'parts/scheduling';dst=S/'parts/scheduling-overlap-invalid'
assert src.resolve().parent==dst.resolve().parent==(S/'parts').resolve() and src.resolve().is_relative_to(R.resolve()) and dst.resolve().is_relative_to(R.resolve())
assert src.is_dir() and not dst.exists()
for p in [src,*src.parents]:
 if p==R.parent:break
 assert not (p.lstat().st_file_attributes&0x400),p
receipt=read(src/'ra2/build-original-c/source-content-receipt.json');exe=src/'ra2/build-original-c/ra2.exe';prior=read(src/'validation.json');manifest=read(src/'manifest.json')
assert receipt['executable_sha256']==sha(exe)==prior['exe_sha256'] and prior['frames']==1303
for e in manifest:
 p=src/e['path'];assert p.resolve().is_relative_to(src.resolve()) and sha(p)==e['sha256'],p
wrong=[Path(p).relative_to(R).as_posix() for p,digest in receipt['inputs'].items() if sha(src/Path(p).relative_to(R))!=digest]
assert wrong==['ra2/src/gameplay/ground_prepare_exit.c'],wrong
assert sha(S/'baseline'/wrong[0])==receipt['inputs'][str(R/wrong[0])]
scene_identity=[]
for e in prior['scenes']:
 p=S/'runs'/e['tag']/'comparison.json';q=read(p);assert sha(p)==e['comparison_sha256'] and q['passed'] and q['exe_sha256']==sha(exe)
 for run in q['runs']:
  state=p.parent/run['mode']/'state.jsonl';digest=sha(state)
  if run.get('state_sha256'):assert digest==run['state_sha256']
  scene_identity.append(dict(tag=e['tag'],mode=run['mode'],state_sha256=digest))
for name in prior['probes']:
 proof=read(S/name);probe=src/S.relative_to(R)/(proof['probe_name']+'_probe.exe');assert proof['passed'] and proof['probe_exe_sha256']==sha(probe)
src.rename(dst);src.mkdir();fixed=[]
for e in manifest:
 rel=e['path'];original=S/'baseline'/rel if rel in wrong else dst/rel;target=src/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(original,target);fixed.append(dict(path=rel,sha256=sha(target)))
for p,digest in receipt['inputs'].items():assert sha(src/Path(p).relative_to(R))==digest,p
write(src/'manifest.json',fixed);value=dict(prior);value.update(source_binding_repaired_from_compiled_receipt=True,unaccepted_snapshot=str(dst));write(src/'validation.json',value)
write(S/'phase-overlap-review.json',dict(passed=True,infrastructure_failure=True,original_game_failure=False,failed_link_log=str(S/'build-publication.log'),failed_link_log_sha256=sha(S/'build-publication.log'),attempted_source=str(S/'ground_prepare_exit-overlap.c'),attempted_source_sha256=sha(S/'ground_prepare_exit-overlap.c'),unaccepted_checkpoint=str(dst),unaccepted_manifest_sha256=sha(dst/'manifest.json'),unaccepted_checkpoint_source_binding_valid=False,accepted_checkpoint=str(src),accepted_manifest_sha256=sha(src/'manifest.json'),tested_executable_sha256=sha(src/'ra2/build-original-c/ra2.exe'),compile_receipt_sha256=sha(src/'ra2/build-original-c/source-content-receipt.json'),all_312_archived_inputs_match_tested_executable_receipt=True,scene_state_identity=scene_identity,existing_scene_and_probe_receipts_reused_by_exact_executable_identity=True,game_pairs_added=0,native_cases_added=0,scope='Publication began while scheduling south was running. Linking failed on the open executable; executable bytes stayed unchanged. Retain the mismatched snapshot as unaccepted; copy its exact archived inputs and correct the single mismatched third source from the hash-identical independent baseline. Verify all 312 inputs against the archived compiled receipt and all scene/probe executable identities. Current publication code is untouched. No result was reclassified or rerun.'))
print(dict(passed=True,correct_checkpoint_rebound=True,invalid_checkpoint_retained=True,new_game_pairs=0))
