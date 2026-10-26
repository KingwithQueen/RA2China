"""Freeze a verified lifecycle rollback and count each accepted comparison once."""
from combat_batch_v72 import *
for n in ['natural-effects.json','record-parity.json','source-preservation.json','native-validation.json','baseline-review.json','probe-review.json','implementation-review.json','art-qualification.json','functional-art-final.json','functional-prism-final.json','functional-queue-final.json','electric-exception-preservation.json','baseline-finalization.json','native-initial-frame.json']:assert read(S/n)['passed'],n
receipt=read(R/'ra2/build-original-c/source-content-receipt.json');part=S/'parts/lifecycle';part.mkdir(parents=True);entries=[]
paths={Path(p).relative_to(R).as_posix() for p in receipt['inputs']};paths|={'ra2/CMakeLists.txt','ra2/build-original-c/ra2.exe','ra2/build-original-c/source-content-receipt.json'}
for rel in sorted(paths):
    p=part/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/rel,p);entries.append(dict(path=rel,sha256=sha(p)))
write(part/'manifest.json',entries);write(part/'validation.json',dict(passed=True,exe_sha256=receipt['executable_sha256'],files=len(entries),native_receipt_sha256=sha(S/'native-validation.json'),natural_effects_sha256=sha(S/'natural-effects.json'),native_supplement_receipt_sha256=sha(S/'native-initial-frame.json')))
values=[]
for n in ['baseline-accepted.json','final-scenes.json','combat-regressions.json','movement-regressions.json']:values+=read(S/n)['results']
values += [read(S/(x+'-command-scenes.json'))['result'] for x in ['b','f']];assert len(values)==34
traces=[]
for x in values:
    p=S/'runs'/x['tag']/'comparison.json';d=read(p);assert sha(p)==x['comparison_sha256'] and d['passed']==x['strict'] and all(z['passed'] and z['exit_code']==0 for z in d['runs']) and d['comparison']['negative_control']['passed']
    assert x['strict'] or x['tag'] in ['old-repair','old-cap','old-flat','b-delayed-art','f-delayed-art','b-delayed-prism','f-delayed-prism','b-queue','f-queue']
    for mode in ['original','generated-c']:
        t=p.parent/mode/'state.jsonl';traces.append(dict(tag=x['tag'],mode=mode,path=str(t),sha256=sha(t)))
helpers=[dict(path=str(p),sha256=sha(p)) for p in sorted(R.glob('*v72*')) if p.is_file()];probes=[dict(path=str(p),sha256=sha(p)) for p in sorted(S.iterdir()) if p.is_file() and p.suffix in ['.c','.h','.exe']]
write(S/'evidence-rollup.json',dict(passed=True,formal_generation=71,verification_round=72,combat_batch=4,accepted_pairs=len(values),accepted_frames=sum(x['frames'] for x in values),strict_pairs=sum(x['strict'] for x in values),functional_pairs=sum(not x['strict'] for x in values),pairs=values,traces=traces,helper_hashes_before_finalization=helpers,probe_and_observer_hashes=probes,native_cases=232106,native_programs=2,primary_native_cases=229376,targeted_distinct_native_cases=2730,native_fragments=7,repeated_native_runs_counted_again=False,excluded=['Pre-existing electric RNG/cleanup diagnostic, not accepted equivalence','Initial RULES-only DeathFrames control did not trigger delay','Identity calibration','Initial probe logger and compiler failure','Preattachment erase-boundary draft and failures'],storage_smoke_counted_in_combat=False,full_original_equivalence_verified=False,complete_combat_rewrite=False,whole_game_acceptance=False))
print(dict(passed=True,pairs=len(values),frames=sum(x['frames'] for x in values),strict=sum(x['strict'] for x in values),native_cases=232106))
