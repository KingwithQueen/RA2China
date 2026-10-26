"""Read-only final lifecycle, storage, source/archive and local-only commit verification."""
from combat_batch_v71 import *
precommit='--precommit' in sys.argv
v=read(S/'validation.json');roll=read(S/'evidence-rollup.json');context=read(S/'vcs-context.json');assert v['passed']
assert (v['formal_baseline_generation'],v['verification_round'],v['combat_batch'])==(70,71,3)
assert not v['full_original_equivalence_verified'] and not v['complete_combat_rewrite'] and v['scoped_movement_acceptance_closed']
receipt=read(R/'ra2/build-original-c/source-content-receipt.json');digest=sha(R/'ra2/build-original-c/ra2.exe');assert receipt['executable_sha256']==digest==v['exe_sha256'] and receipt['source_count']==188 and len(receipt['inputs'])==325
for p,d in receipt['inputs'].items():assert sha(Path(p))==d,p
for e in read(S/'source-manifest.json'):assert sha(R/e['path'])==e['sha256']==sha(S/'final-source'/e['path']),e['path']
assert len(read(S/'source-manifest.json'))==v['source_files']
for e in read(S/'document-manifest.json'):assert sha(P/e['path'])==e['sha256']==sha(S/'current-project'/e['path']),e['path']
for folder in ['baseline','parts/death']:
    for e in read(S/folder/'manifest.json'):assert sha(S/folder/e['path'])==e['sha256'],(folder,e['path'])
part=read(S/'parts/death/validation.json');assert part['passed'] and part['exe_sha256']==digest and part['native_receipt_sha256']==sha(S/'native-validation.json') and part['natural_effects_sha256']==sha(S/'natural-effects.json')
for e in read(S/'protected-inputs.json')['files']:assert sha(Path(e['path']))==e['sha256']
assert sha(O/'source-manifest.json')==context['parent_manifest_sha256']
for e in read(O/'source-manifest.json'):assert sha(O/'final-source'/e['path'])==e['sha256']
for folder in ['baseline-observer','baseline-command']:
    for e in read(S/(folder+'.json'))['files']:assert sha(Path(e['path']))==e['sha256']
required=['baseline-review.json','record-parity.json','natural-effects.json','source-preservation.json','native-validation.json','probe-review.json','implementation-review.json','observer-review.json','input-qualification.json','invalid-owner-independent.json','storage-review.json','cleanup.json','remaining-work.json']
for n in required:assert read(S/n)['passed'],n
for e in roll['traces']+roll['helper_hashes_before_finalization']+roll['probe_and_observer_hashes']:assert sha(Path(e['path']))==e['sha256']
strict=frames=0
for x in roll['pairs']:
    p=S/'runs'/x['tag']/'comparison.json';d=read(p);assert sha(p)==x['comparison_sha256'] and d['passed']==x['strict'] and d['comparison']['frames_compared']==x['frames']
    assert all(z['passed'] and z['exit_code']==0 for z in d['runs']) and d['comparison']['negative_control']['passed']
    if x['tag']=='b-truck-command':expected=sha(S/'baseline-command/combat-command.exe')
    elif x['tag']=='f-truck-command' or x['tag'].startswith('old-'):expected=sha(S/'combat-command.exe')
    elif x['tag'].startswith('b-'):expected=sha(S/'baseline-observer/combat-observer.exe')
    elif x['tag'].startswith('f-'):expected=sha(S/'combat-observer.exe')
    else:expected=digest
    assert d['exe_sha256']==expected==x['exe_sha256'],x['tag']
    assert x['strict'] or x['tag'] in ['old-repair','old-cap','old-flat'];strict+=int(x['strict']);frames+=x['frames']
assert len(roll['pairs'])==26==v['accepted_game_pairs'] and frames==26926==roll['accepted_frames']==v['accepted_frames']
assert strict==23==roll['strict_pairs']==v['strict_game_pairs'] and roll['functional_pairs']==3
effects=read(S/'natural-effects.json')
for e in effects['complete_pre_post_traces']:
    assert sha(S/'runs'/e['baseline_tag']/e['mode']/'state.jsonl')==e['sha256']==sha(S/'runs'/('f-'+e['tag'])/e['mode']/'state.jsonl')
def standard(p):return b''.join(l for l in p.read_bytes().splitlines(keepends=True) if not json.loads(l)['kind'].startswith('fixture-'))
for e in effects['inherited_combat_traces']:
    a=Path(e['parent_path']);b=S/'runs'/e['tag']/e['mode']/'state.jsonl';assert sha(a)==e['parent_sha256'] and sha(b)==e['current_sha256'] and standard(a)==b.read_bytes()
for e in effects['movement_parent_parity']:assert sha(Path(e['parent_path']))==e['sha256']==sha(S/'runs'/e['tag']/e['mode']/'state.jsonl')
probe=read(S/'native-validation.json');assert probe['result']['death_cases']==131072==v['native_cases'] and probe['engine_callbacks_mocked'] and probe['special_fraction']==.25
assert sha(S/'death_probe.exe')==probe['exe_sha256'] and sha(R/'ra2/game/game.exe')==probe['original_sha256']
for e in probe['inputs']:assert sha(Path(e['path']))==e['sha256']
for name,key,hashkey in [('probe-review.json','initial_source','initial_sha256'),('implementation-review.json','unattached_initial_core','initial_sha256'),('observer-review.json','initial_source','initial_sha256')]:
    e=read(S/name);assert sha(Path(e[key]))==e[hashkey]
for x in read(S/'qualified-scene-recipes.json')['fixtures']+[read(S/'extra-scene.json')['fixture']]:
    assert sha(R/x['path'])==x['map_sha256']
    if x.get('rules'):assert sha(R/x['rules'])==x['rules_sha256']
pending=read(S/'scene-pending.json');assert sha(Path(pending['original_rules']))==pending['original_rules_sha256']
for n in ['community-reference-review.json','community-current-use.json','alias-evidence-inheritance.json']:assert sha(S/n)==sha(O/n)
source=read(S/'source-preservation.json');assert source['compile_inputs']==325 and source['guard_sites']==37 and source['generated_definitions']==23117 and source['changed_compile_inputs']==['ra2/src/recomp/gen_game/recomp_0029.c']
assert (S/'observer-build/death_generated.c').read_bytes()==(R/'ra2/src/recomp/gen_game/recomp_0029.c').read_bytes().replace(b'void WaveClass__virtual_86(void) {',b'void observed_health_original(void) {')
disk=read(S/'storage-review.json');assert disk['files']==25731 and disk['all_paths_and_bytes_retained']
for e in disk['bindings']:assert sha(Path(e['path']))==e['sha256']
sd=R/'evidence/storage-review-v1';sv=read(sd/'validation.json');assert sv['saved_bytes']==disk['saved_bytes']==220153295319 and sv['all_content_hashes_verified'] and read(sd/'postcheck.json')['compressed_executable_smoke_passed'] and (R/'evidence').stat().st_file_attributes&0x800
clean=read(S/'cleanup.json');plan=read(S/'cleanup-plan.json');assert clean['plan_sha256']==sha(S/'cleanup-plan.json') and clean['protected_unchanged']
for e in plan['protected']:assert sha(Path(e['path']))==e['sha256']
for e in plan['candidates']:assert not Path(e['path']).exists()
assert sha(P/'.git/config')==context['config_sha256'] and hashlib.sha256(git('for-each-ref','--format=%(refname) %(objectname)','refs/remotes/')).hexdigest()==context['remote_refs_sha256']
if not precommit:
    assert not git('status','--porcelain','--untracked-files=all') and git('rev-parse','HEAD^').decode().strip()==context['parent_commit']
print(dict(passed=True,formal=70,verification=71,combat_batch=3,exe_sha256=digest,source_files=v['source_files'],pairs=26,frames=frames,native_cases=131072,storage_saved_GiB=round(disk['saved_bytes']/2**30,2),precommit=precommit,pushed=False))
