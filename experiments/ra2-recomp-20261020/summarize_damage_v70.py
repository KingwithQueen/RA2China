"""Freeze one verified rollback and count this batch's comparisons once."""
from combat_batch_v70 import *
for n in ['natural-effects.json','record-parity.json','source-preservation.json','native-validation.json','combat-regressions.json','movement-regressions.json','baseline-review.json']:assert read(S/n)['passed'],n
receipt=read(R/'ra2/build-original-c/source-content-receipt.json');part=S/'parts/damage';part.mkdir(parents=True);entries=[]
paths={Path(p).relative_to(R).as_posix() for p in receipt['inputs']};paths|={'ra2/CMakeLists.txt','ra2/build-original-c/ra2.exe','ra2/build-original-c/source-content-receipt.json'}
for rel in sorted(paths):
    p=part/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/rel,p);entries.append(dict(path=rel,sha256=sha(p)))
write(part/'manifest.json',entries)
write(part/'validation.json',dict(passed=True,exe_sha256=receipt['executable_sha256'],files=len(entries),native_receipt_sha256=sha(S/'native-validation.json'),natural_effects_sha256=sha(S/'natural-effects.json')))
rows=[]
for n in ['baseline-scenes.json','final-scenes.json','combat-regressions.json','movement-regressions.json']:rows+=read(S/n)['results']
rows+=[read(S/(x+'-command-scenes.json'))['result'] for x in ['b','f']];assert len(rows)==19
traces=[]
for x in rows:
    p=S/'runs'/x['tag']/'comparison.json';d=read(p);assert sha(p)==x['comparison_sha256'] and d['passed']==x['strict']
    assert all(z['passed'] and z['exit_code']==0 for z in d['runs']) and d['comparison']['negative_control']['passed']
    assert x['strict'] or x['tag'] in ['b-splash','f-splash','b-flat','f-flat','old-repair','old-cap']
    for mode in ['original','generated-c']:
        t=p.parent/mode/'state.jsonl'
        traces.append(dict(tag=x['tag'],mode=mode,path=str(t),sha256=sha(t)))
helpers=[dict(path=str(p),sha256=sha(p)) for p in sorted(R.glob('*v70*')) if p.is_file()]
probe=[dict(path=str(p),sha256=sha(p)) for p in sorted(S.iterdir()) if p.is_file() and p.suffix in ['.c','.h','.exe']]
write(S/'evidence-rollup.json',dict(passed=True,formal_generation=69,verification_round=70,combat_batch=2,accepted_pairs=len(rows),accepted_frames=sum(x['frames'] for x in rows),strict_pairs=sum(x['strict'] for x in rows),functional_pairs=sum(not x['strict'] for x in rows),pairs=rows,traces=traces,helper_hashes_before_finalization=helpers,probe_and_observer_hashes=probe,native_cases=262146,native_programs=1,native_fragments=1,repeated_native_runs_counted_again=False,excluded=['id-rifle','id-splash','id-flat','Repeated initial native matrix'],full_original_equivalence_verified=False,complete_combat_rewrite=False,rule_parser_precision_fix_included=False,whole_game_acceptance=False))
print(dict(passed=True,pairs=len(rows),frames=sum(x['frames'] for x in rows),strict=sum(x['strict'] for x in rows),native_cases=262146))
