"""Read-only final source, native, natural, inherited evidence and local commit verification."""
from combat_batch_v70 import *
precommit='--precommit' in sys.argv
v=read(S/'validation.json');roll=read(S/'evidence-rollup.json');context=read(S/'vcs-context.json');assert v['passed']
assert (v['formal_baseline_generation'],v['verification_round'],v['combat_batch'])==(69,70,2)
assert not v['full_original_equivalence_verified'] and not v['complete_combat_rewrite'] and v['scoped_movement_acceptance_closed']
receipt=read(R/'ra2/build-original-c/source-content-receipt.json');digest=sha(R/'ra2/build-original-c/ra2.exe')
assert receipt['executable_sha256']==digest==v['exe_sha256'] and receipt['source_count']==186 and len(receipt['inputs'])==321
for p,d in receipt['inputs'].items():assert sha(Path(p))==d,p
for e in read(S/'source-manifest.json'):assert sha(R/e['path'])==e['sha256']==sha(S/'final-source'/e['path']),e['path']
assert len(read(S/'source-manifest.json'))==v['source_files']
for e in read(S/'document-manifest.json'):assert sha(P/e['path'])==e['sha256']==sha(S/'current-project'/e['path']),e['path']
for folder in ['baseline','parts/damage']:
    for e in read(S/folder/'manifest.json'):assert sha(S/folder/e['path'])==e['sha256'],(folder,e['path'])
part=read(S/'parts/damage/validation.json');assert part['passed'] and part['exe_sha256']==digest
for k,n in [('native_receipt_sha256','native-validation.json'),('natural_effects_sha256','natural-effects.json')]:assert part[k]==sha(S/n)
for e in read(S/'protected-inputs.json')['files']:assert sha(Path(e['path']))==e['sha256'],e['path']
assert sha(O/'source-manifest.json')==context['parent_manifest_sha256']
for e in read(O/'source-manifest.json'):assert sha(O/'final-source'/e['path'])==e['sha256'],e['path']
for folder in ['baseline-observer','baseline-command']:
    for e in read(S/(folder+'.json'))['files']:assert sha(Path(e['path']))==e['sha256'],e['path']
for n in ['baseline-review.json','record-parity.json','natural-effects.json','source-preservation.json','native-validation.json','observer-scope.json','initial-native-provenance.json','combat-regressions.json','movement-regressions.json','cleanup.json','remaining-work.json']:assert read(S/n)['passed'],n
for e in roll['traces']+roll['helper_hashes_before_finalization']+roll['probe_and_observer_hashes']:assert sha(Path(e['path']))==e['sha256'],e['path']
frames=strict=0
for x in roll['pairs']:
    p=S/'runs'/x['tag']/'comparison.json';d=read(p);assert sha(p)==x['comparison_sha256'] and d['passed']==x['strict'] and d['comparison']['frames_compared']==x['frames']
    assert all(z['passed'] and z['exit_code']==0 for z in d['runs']) and d['comparison']['negative_control']['passed']
    if x['tag']=='b-rifle-command':expected=sha(S/'baseline-command/combat-command.exe')
    elif x['tag']=='f-rifle-command' or x['tag'].startswith('old-'):expected=sha(S/'combat-command.exe')
    elif x['tag'].startswith('b-'):expected=sha(S/'baseline-observer/combat-observer.exe')
    elif x['tag'].startswith('f-'):expected=sha(S/'combat-observer.exe')
    else:expected=digest
    assert d['exe_sha256']==expected==x['exe_sha256'],x['tag']
    assert x['strict'] or x['tag'] in ['b-splash','f-splash','b-flat','f-flat','old-repair','old-cap']
    strict+=int(x['strict']);frames+=x['frames']
assert len(roll['pairs'])==19==v['accepted_game_pairs'] and frames==23619==roll['accepted_frames']==v['accepted_frames']
assert strict==13==roll['strict_pairs']==v['strict_game_pairs'] and roll['functional_pairs']==6
effects=read(S/'natural-effects.json')
for e in effects['complete_pre_post_traces_unchanged']:
    for phase in ['b','f']:assert sha(S/'runs'/(phase+'-'+e['tag'])/e['mode']/'state.jsonl')==e['sha256']
def standard(p):return b''.join(l for l in p.read_bytes().splitlines(keepends=True) if not json.loads(l)['kind'].startswith('fixture-'))
for e in effects['inherited_combat_traces']:
    a=Path(e['parent_path']);b=S/'runs'/('old-'+e['tag'])/e['mode']/'state.jsonl'
    assert sha(a)==e['parent_trace_sha256'] and sha(b)==e['current_trace_sha256'] and standard(a)==b.read_bytes()
for e in effects['movement_parent_parity']:assert sha(Path(e['parent_path']))==e['sha256']==sha(S/'runs'/e['tag']/e['mode']/'state.jsonl')
probe=read(S/'native-validation.json');assert probe['result']['damage_cases']==262146==v['native_cases'] and probe['result']['neighbor_results']==[179,180] and not probe['result']['mocked_damage_math']
assert sha(S/'damage_probe.exe')==probe['exe_sha256'] and sha(R/'ra2/game/game.exe')==probe['original_sha256']
for e in probe['inputs']:assert sha(Path(e['path']))==e['sha256'],e['path']
initial=read(S/'initial-native-provenance.json');assert sha(Path(initial['source_path']))==initial['source_sha256'] and initial['result']['damage_cases']==262144
for x in read(S/'scene-recipes.json')['fixtures']:
    assert sha(R/x['path'])==x['map_sha256']
    if x.get('rules'):assert sha(R/x['rules'])==x['rules_sha256']
pending=read(S/'scene-pending.json');assert sha(Path(pending['original_rules']))==pending['original_rules_sha256']
for n in ['community-reference-review.json','community-current-use.json','alias-evidence-inheritance.json']:assert sha(S/n)==sha(O/n)
source=read(S/'source-preservation.json');assert source['compile_inputs']==321 and source['guard_sites']==37 and source['generated_definitions']==23117 and source['changed_compile_inputs']==['ra2/src/recomp/gen_game/recomp_0007.c']
observer=read(S/'observer-scope.json');assert sha(Path(observer['generated_source_path']))==observer['generated_source_sha256']
assert (S/'observer-build/damage_generated.c').read_bytes()==(R/'ra2/src/recomp/gen_game/recomp_0007.c').read_bytes().replace(b'void sub_0047E1C0(void) {',b'void observed_damage_original(void) {')
clean=read(S/'cleanup.json');plan=read(S/'cleanup-plan.json');assert clean['plan_sha256']==sha(S/'cleanup-plan.json') and clean['protected_unchanged']
for e in plan['protected']:assert sha(Path(e['path']))==e['sha256'],e['path']
for e in plan['candidates']:assert not Path(e['path']).exists(),e['path']
assert sha(P/'.git/config')==context['config_sha256']
assert hashlib.sha256(git('for-each-ref','--format=%(refname) %(objectname)','refs/remotes/')).hexdigest()==context['remote_refs_sha256']
if not precommit:
    assert not git('status','--porcelain','--untracked-files=all')
    assert git('rev-parse','HEAD^').decode().strip()==context['parent_commit']
print(dict(passed=True,formal=69,verification=70,combat_batch=2,exe_sha256=digest,source_files=v['source_files'],pairs=19,frames=frames,native_cases=262146,precommit=precommit,pushed=False))
