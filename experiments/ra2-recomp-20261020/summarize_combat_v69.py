"""Freeze one successful rollback and count each bounded game/probe comparison once."""
from combat_batch_v69 import *
for n in ['natural-effects.json','record-parity.json','source-preservation.json','native-validation.json','regressions.json']:
    assert read(S/n)['passed'],n
prior={'default':'default','reg-north':'cross-north','reg-south':'cross-south','reg-train':'contact-train','reg-crush':'contact-crush','reg-stop':'f-stopcmd'};checks=[]
for tag,oldtag in prior.items():
    for mode in ['original','generated-c']:
        a=S/'runs'/tag/mode/'state.jsonl';b=O/'runs'/oldtag/mode/'state.jsonl';assert sha(a)==sha(b),(tag,mode)
        checks.append(dict(tag=tag,mode=mode,parent_path=str(b),sha256=sha(a)))
write(S/'parent-regression-parity.json',dict(passed=True,traces=checks))
receipt=read(R/'ra2/build-original-c/source-content-receipt.json');part=S/'parts/health';part.mkdir(parents=True);entries=[]
paths={Path(p).relative_to(R).as_posix() for p in receipt['inputs']};paths|={'ra2/CMakeLists.txt','ra2/build-original-c/ra2.exe','ra2/build-original-c/source-content-receipt.json'}
for rel in sorted(paths):
    p=part/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/rel,p);entries.append(dict(path=rel,sha256=sha(p)))
write(part/'manifest.json',entries)
write(part/'validation.json',dict(passed=True,exe_sha256=receipt['executable_sha256'],files=len(entries),native_receipt_sha256=sha(S/'native-validation.json'),natural_effects_sha256=sha(S/'natural-effects.json'),regressions_sha256=sha(S/'regressions.json')))
rows=read(S/'baseline-scenes.json')['results']+[read(S/'extra-baseline-contract.json')['result']]+read(S/'final-scenes.json')['results']+read(S/'regressions.json')['results']
rows+=[read(S/(p+'-command-scenes.json'))['result'] for p in ['b','f']];assert len(rows)==18
traces=[]
for q in rows:
    p=S/'runs'/q['tag']/'comparison.json';d=read(p);assert sha(p)==q['comparison_sha256'] and d['passed']==q['strict']
    assert all(x['passed'] and x['exit_code']==0 for x in d['runs']) and d['comparison']['negative_control']['passed']
    assert q['strict'] or q['tag'] in ['b-repair','b-cap','f-repair','f-cap']
    for m in ['original','generated-c']:
        t=p.parent/m/'state.jsonl';traces.append(dict(tag=q['tag'],mode=m,path=str(t),sha256=sha(t)))
helpers=[dict(path=str(p),sha256=sha(p)) for p in sorted(R.glob('*v69*')) if p.is_file()]
probes=[dict(path=str(p),sha256=sha(p)) for p in sorted(S.iterdir()) if p.is_file() and p.suffix in ['.c','.h','.exe']]
write(S/'evidence-rollup.json',dict(passed=True,formal_generation=68,verification_round=69,combat_batch=1,accepted_pairs=len(rows),accepted_frames=sum(q['frames'] for q in rows),strict_pairs=sum(q['strict'] for q in rows),functional_pairs=sum(not q['strict'] for q in rows),pairs=rows,traces=traces,helper_hashes_before_finalization=helpers,probe_and_observer_hashes=probes,native_cases=131072,native_programs=1,native_fragments=1,excluded=['id-tank','id-infantry','id-repair','id-immune','failed initial native stack capture','failed production label build'],repeated_native_runs_counted_again=False,full_original_equivalence_verified=False,whole_game_acceptance=False,armor_calculation_mocked_in_probe=True,actual_armor_calculation_exercised_in_natural_scenes=True,complete_combat_rewrite=False))
print(dict(passed=True,pairs=len(rows),frames=sum(q['frames'] for q in rows),strict=sum(q['strict'] for q in rows),native_cases=131072))
