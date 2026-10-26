"""Read-only final content, fixed-frame evidence and local-only delivery verification."""
from combat_batch_v69 import *
precommit='--precommit' in sys.argv
v=read(S/'validation.json');roll=read(S/'evidence-rollup.json');context=read(S/'vcs-context.json');assert v['passed']
assert v['formal_baseline_generation']==68 and v['verification_round']==69 and v['combat_batch']==1
assert not v['full_original_equivalence_verified'] and not v['complete_combat_rewrite'] and v['scoped_movement_acceptance_closed']
receipt=read(R/'ra2/build-original-c/source-content-receipt.json');digest=sha(R/'ra2/build-original-c/ra2.exe')
assert receipt['executable_sha256']==digest==v['exe_sha256'] and receipt['source_count']==184 and len(receipt['inputs'])==317
for p,d in receipt['inputs'].items():assert sha(Path(p))==d,p
for e in read(S/'source-manifest.json'):assert sha(R/e['path'])==e['sha256']==sha(S/'final-source'/e['path']),e['path']
assert len(read(S/'source-manifest.json'))==v['source_files']
for e in read(S/'document-manifest.json'):assert sha(P/e['path'])==e['sha256']==sha(S/'current-project'/e['path']),e['path']
for folder in ['baseline','parts/health']:
    for e in read(S/folder/'manifest.json'):assert sha(S/folder/e['path'])==e['sha256'],(folder,e['path'])
part=read(S/'parts/health/validation.json');assert part['passed'] and part['exe_sha256']==digest
for key,name in [('native_receipt_sha256','native-validation.json'),('natural_effects_sha256','natural-effects.json'),('regressions_sha256','regressions.json')]:assert part[key]==sha(S/name)
for e in read(S/'protected-inputs.json')['files']:assert sha(Path(e['path']))==e['sha256'],e['path']
assert sha(O/'source-manifest.json')==context['parent_manifest_sha256']
for e in read(O/'source-manifest.json'):assert sha(O/'final-source'/e['path'])==e['sha256'],e['path']
for folder,name in [('baseline-observer','combat-observer.exe'),('baseline-command','combat-command.exe')]:assert sha(S/folder/name)==read(S/(folder+'.json'))['exe_sha256']
for name in ['natural-effects.json','record-parity.json','baseline-effects.json','source-preservation.json','native-validation.json','implementation-review.json','regressions.json','parent-regression-parity.json','cleanup.json','remaining-work.json']:assert read(S/name)['passed'],name
for e in roll['traces']+roll['helper_hashes_before_finalization']+roll['probe_and_observer_hashes']:assert sha(Path(e['path']))==e['sha256'],e['path']
strict=frames=0
for q in roll['pairs']:
    p=S/'runs'/q['tag']/'comparison.json';d=read(p);assert sha(p)==q['comparison_sha256']
    assert all(x['passed'] and x['exit_code']==0 for x in d['runs']) and d['comparison']['negative_control']['passed']
    assert d['passed']==q['strict'] and d['comparison']['frames_compared']==q['frames']
    if q['tag']=='b-tank-cmd':expected=sha(S/'baseline-command/combat-command.exe')
    elif q['tag']=='f-tank-cmd':expected=sha(S/'combat-command.exe')
    elif q['tag'].startswith('b-'):expected=sha(S/'baseline-observer/combat-observer.exe')
    elif q['tag'].startswith('f-'):expected=sha(S/'combat-observer.exe')
    else:expected=digest
    assert d['exe_sha256']==expected==q['exe_sha256'],q['tag']
    assert q['strict'] or q['tag'] in ['b-repair','f-repair','b-cap','f-cap']
    strict+=int(q['strict']);frames+=q['frames']
assert len(roll['pairs'])==18==v['accepted_game_pairs'] and frames==22118==roll['accepted_frames']==v['accepted_frames']
assert strict==14==roll['strict_pairs']==v['strict_game_pairs'] and roll['functional_pairs']==4
for e in read(S/'natural-effects.json')['full_per_mode_before_after_unchanged']:
    for phase in ['b','f']:assert sha(S/'runs'/(phase+'-'+e['tag'])/e['mode']/'state.jsonl')==e['sha256']
for e in read(S/'parent-regression-parity.json')['traces']:assert sha(Path(e['parent_path']))==e['sha256']==sha(S/'runs'/e['tag']/e['mode']/'state.jsonl')
probe=read(S/'native-validation.json');assert probe['result']['health_cases']==131072==v['native_cases'] and probe['result']['armor_calculation_mocked']
assert sha(S/'health_probe.exe')==probe['exe_sha256'] and sha(R/'ra2/game/game.exe')==probe['original_sha256']
for e in probe['inputs']:assert sha(Path(e['path']))==e['sha256']
for e in read(S/'scene-recipes.json')['fixtures']+[read(S/'extra-scene.json')['fixture']]:
    assert sha(R/e['path'])==e['map_sha256']
    if e.get('rules'):assert sha(R/e['rules'])==read(S/'scene-pending.json')['immune_rule_sha256']
pending=read(S/'scene-pending.json');assert sha(Path(pending['original_rules']))==pending['original_rules_sha256']
capture=read(S/'native-capture-review.json');assert sha(Path(capture['initial_probe_source']))==capture['initial_probe_sha256']
for n in ['community-reference-review.json','community-current-use.json','alias-evidence-inheritance.json']:assert sha(S/n)==sha(O/n)
source=read(S/'source-preservation.json');assert source['compile_inputs']==317 and source['guard_sites']==37 and source['generated_definitions']==23117
assert source['changed_compile_inputs']==['ra2/src/recomp/gen_game/recomp_0029.c'] and source['tail_and_other_generated_code_byte_identical']
clean=read(S/'cleanup.json');plan=read(S/'cleanup-plan.json');assert clean['plan_sha256']==sha(S/'cleanup-plan.json') and clean['protected_unchanged']
for e in plan['protected']:assert sha(Path(e['path']))==e['sha256'],e['path']
for e in plan['candidates']:assert not Path(e['path']).exists(),e['path']
assert sha(P/'.git/config')==context['config_sha256']
assert hashlib.sha256(git('for-each-ref','--format=%(refname) %(objectname)','refs/remotes/')).hexdigest()==context['remote_refs_sha256']
if not precommit:
    assert not git('status','--porcelain','--untracked-files=all')
    assert git('rev-parse','HEAD^').decode().strip()==context['parent_commit']
print(dict(passed=True,formal=68,verification=69,combat_batch=1,exe_sha256=digest,source_files=v['source_files'],pairs=18,frames=frames,native_cases=131072,precommit=precommit,pushed=False))
