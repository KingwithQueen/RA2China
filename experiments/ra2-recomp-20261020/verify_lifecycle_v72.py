"""Read-only formal71 verification: sources, protected originals, lifecycle and natural receipts."""
from combat_batch_v72 import *
from vcs_completion_v72 import expected_remote_hash,reviewed_tools
from integrate_lifecycle_v72 import blocks,attached,cmake
import re
precommit='--precommit' in sys.argv
v=read(S/'validation.json');roll=read(S/'evidence-rollup.json');context=read(S/'vcs-context.json');assert v['passed']
assert (v['formal_baseline_generation'],v['verification_round'],v['combat_batch'])==(71,72,4)
assert not v['full_original_equivalence_verified'] and not v['complete_combat_rewrite'] and v['scoped_movement_acceptance_closed']
receipt=read(R/'ra2/build-original-c/source-content-receipt.json');digest=sha(R/'ra2/build-original-c/ra2.exe');assert receipt['executable_sha256']==digest==v['exe_sha256'] and receipt['source_count']==190 and len(receipt['inputs'])==329
for p,d in receipt['inputs'].items():assert sha(Path(p))==d,p
revisions=reviewed_tools()
for e in read(S/'source-manifest.json'):
    assert sha(S/'final-source'/e['path'])==e['sha256'],e['path']
    revision=revisions.get(str(R/e['path']));assert sha(R/e['path'])==(revision['sha256'] if revision else e['sha256']),e['path']
assert len(read(S/'source-manifest.json'))==v['source_files']
for e in read(S/'document-manifest.json'):assert sha(P/e['path'])==e['sha256']==sha(S/'current-project'/e['path']),e['path']
for folder in ['baseline','parts/lifecycle']:
    for e in read(S/folder/'manifest.json'):assert sha(S/folder/e['path'])==e['sha256'],(folder,e['path'])
part=read(S/'parts/lifecycle/validation.json');assert part['passed'] and part['exe_sha256']==digest and part['native_receipt_sha256']==sha(S/'native-validation.json') and part['natural_effects_sha256']==sha(S/'natural-effects.json') and part['native_supplement_receipt_sha256']==sha(S/'native-initial-frame.json')
for e in read(S/'protected-inputs.json')['files']:assert sha(Path(e['path']))==e['sha256']
assert sha(O/'source-manifest.json')==context['parent_manifest_sha256']
for e in read(O/'source-manifest.json'):assert sha(O/'final-source'/e['path'])==e['sha256']
for folder in ['baseline-observer','baseline-command']:
    for e in read(S/(folder+'.json'))['files']:assert sha(Path(e['path']))==e['sha256']
for n in ['baseline-review.json','record-parity.json','natural-effects.json','source-preservation.json','native-validation.json','probe-review.json','implementation-review.json','art-input.json','art-qualification.json','lifecycle-layout.json','cleanup.json','remaining-work.json','functional-art-baseline.json','functional-art-final.json','functional-prism-baseline.json','functional-prism-final.json','functional-queue-baseline.json','functional-queue-final.json','baseline-finalization.json','electric-exception-preservation.json','native-initial-frame.json']:assert read(S/n)['passed'],n
for e in roll['traces']+roll['helper_hashes_before_finalization']+roll['probe_and_observer_hashes']:
    revision=revisions.get(e['path']);assert sha(Path(e['path']))==(revision['sha256'] if revision else e['sha256'])
strict=frames=0
for x in roll['pairs']:
    p=S/'runs'/x['tag']/'comparison.json';d=read(p);assert sha(p)==x['comparison_sha256'] and d['passed']==x['strict'] and d['comparison']['frames_compared']==x['frames']
    assert all(z['passed'] and z['exit_code']==0 for z in d['runs']) and d['comparison']['negative_control']['passed']
    if x['tag']=='b-command':expected=sha(S/'baseline-command/combat-command.exe')
    elif x['tag']=='f-command' or x['tag'].startswith('old-'):expected=sha(S/'combat-command.exe')
    elif x['tag'].startswith('b-'):expected=sha(S/'baseline-observer/combat-observer.exe')
    elif x['tag'].startswith('f-'):expected=sha(S/'combat-observer.exe')
    else:expected=digest
    assert d['exe_sha256']==expected==x['exe_sha256'],x['tag']
    assert x['strict'] or x['tag'] in ['old-repair','old-cap','old-flat','b-delayed-art','f-delayed-art','b-delayed-prism','f-delayed-prism','b-queue','f-queue'];strict+=int(x['strict']);frames+=x['frames']
assert len(roll['pairs'])==34==v['accepted_game_pairs'] and frames==37134==roll['accepted_frames']==v['accepted_frames']
assert strict==25==roll['strict_pairs']==v['strict_game_pairs'] and roll['functional_pairs']==9
assert not any(x['tag']=='b-delayed' for x in roll['pairs'])
for e in read(S/'electric-exception-preservation.json')['complete_per_mode_before_after']:
    assert sha(S/'runs/b-electric'/e['mode']/'state.jsonl')==e['baseline_sha256']==e['final_sha256']==sha(S/'runs/f-electric-diagnostic'/e['mode']/'state.jsonl')
effects=read(S/'natural-effects.json')
for e in effects['complete_pre_post_traces']:assert sha(S/'runs'/('b-'+e['tag'])/e['mode']/'state.jsonl')==e['sha256']==sha(S/'runs'/('f-'+e['tag'])/e['mode']/'state.jsonl')
def standard(p):return b''.join(l for l in p.read_bytes().splitlines(keepends=True) if not json.loads(l)['kind'].startswith('fixture-'))
for e in effects['inherited_combat_traces']:
    a=Path(e['parent_path']);b=S/'runs'/e['tag']/e['mode']/'state.jsonl';assert sha(a)==e['parent_sha256'] and sha(b)==e['current_sha256'] and standard(a)==b.read_bytes()
for e in effects['movement_parent_parity']:assert sha(Path(e['parent_path']))==e['sha256']==sha(S/'runs'/e['tag']/e['mode']/'state.jsonl')
probe=read(S/'native-validation.json');assert probe['result']['lifecycle_cases']==229376 and probe['result']['fragments']==7 and probe['engine_callbacks_mocked']
assert sha(S/'lifecycle_probe.exe')==probe['exe_sha256'] and sha(R/'ra2/game/game.exe')==probe['original_sha256']
for e in probe['inputs']:assert sha(Path(e['path']))==e['sha256']
supplement=read(S/'native-initial-frame.json');assert supplement['result']['lifecycle_cases']==2730 and probe['result']['lifecycle_cases']+supplement['distinct_new_cases']==232106==v['native_cases'] and v['native_programs']==2
assert sha(S/'lifecycle_probe_initial_frame.exe')==supplement['exe_sha256']
for e in supplement['inputs']:assert sha(Path(e['path']))==e['sha256']
for n in ['probe-review.json','implementation-review.json']:
    e=read(S/n);assert sha(Path(e['initial_source']))==e['initial_sha256']
for x in read(S/'qualified-final-scene-recipes.json')['fixtures']:
    assert sha(R/x['path'])==x['map_sha256']
    if x.get('rules'):assert sha(R/x['rules'])==x['rules_sha256']
    if x.get('art'):
        assert sha(R/x['art'])==x['art_sha256']
art=read(S/'art-input.json');assert sha(Path(art['original_path']))==art['original_sha256'] and sha(Path(art['source_mix']))==art['source_mix_sha256'] and sha(Path(art['audit_tool']))==art['audit_tool_sha256'] and sha(Path(art['private_art']))==art['private_art_sha256']
# All ART sections outside TRUCKA remain byte-for-byte original.
import re
art_before=Path(art['original_path']).read_bytes();art_after=Path(art['private_art']).read_bytes();pat=rb'(?ms)^\[TRUCKA\]\r?\n.*?(?=^\[|\Z)';assert re.sub(pat,b'',art_before)==re.sub(pat,b'',art_after)
for x in read(S/'qualified-final-scene-recipes.json')['fixtures']:
    if x.get('art'):
        before=art_before.replace(b'\r\n',b'\n');after=(R/x['art']).read_bytes().replace(b'\r\n',b'\n');assert re.sub(pat,b'',before)==re.sub(pat,b'',after)
pending=read(S/'scene-pending.json');assert sha(Path(pending['original_rules']))==pending['original_rules_sha256']
for n in ['community-reference-review.json','community-current-use.json','alias-evidence-inheritance.json']:assert sha(S/n)==sha(O/n)
source=read(S/'source-preservation.json');assert source['compile_inputs']==329 and source['guard_sites']==37 and source['generated_definitions']==23117 and set(source['changed_compile_inputs'])=={'ra2/src/recomp/gen_game/'+n for n in blocks}
for name,points in blocks.items():
    rel='ra2/src/recomp/gen_game/'+name;assert (R/rel).read_bytes()==attached((S/'baseline'/rel).read_bytes(),points)
assert (R/'ra2/CMakeLists.txt').read_bytes()==(S/'baseline/ra2/CMakeLists.txt').read_bytes()+cmake
assert (S/'observer-build/death_generated.c').read_bytes()==(R/'ra2/src/recomp/gen_game/recomp_0029.c').read_bytes().replace(b'void WaveClass__virtual_86(void) {',b'void observed_health_original(void) {')
assert (R/'evidence').stat().st_file_attributes&0x800 and (S/'final-source').stat().st_file_attributes&0x800
clean=read(S/'cleanup.json');plan=read(S/'cleanup-plan.json');assert clean['plan_sha256']==sha(S/'cleanup-plan.json') and clean['protected_unchanged']
for e in plan['protected']:assert sha(Path(e['path']))==e['sha256']
for e in plan['candidates']:assert not Path(e['path']).exists()
assert sha(P/'.git/config')==context['config_sha256'] and hashlib.sha256(git('for-each-ref','--format=%(refname) %(objectname)','refs/remotes/')).hexdigest()==expected_remote_hash(context)
if not precommit:assert not git('status','--porcelain','--untracked-files=all') and git('rev-parse','HEAD^').decode().strip()==context['parent_commit']
print(dict(passed=True,formal=71,verification=72,combat_batch=4,exe_sha256=digest,source_files=v['source_files'],pairs=34,frames=frames,native_cases=232106,precommit=precommit,pushed=False))
