"""Read-only final source, trace, archive, protection and local-commit verification."""
from run_batch_v68 import *
precommit='--precommit' in sys.argv
v=read(S/'validation.json');roll=read(S/'evidence-rollup.json');context=read(S/'vcs-context.json')
assert v['passed'] and v['verification_round']==68 and v['formal_baseline_generation']==67
assert v['scoped_movement_acceptance_closed'] and not v['all_locomotors_readably_rewritten'] and not v['full_original_equivalence_verified']
assert v['rollback_parts']==['closeout'] and not v['fifo_guarantee'] and not v['unbounded_starvation_freedom_proved']
receipt=read(R/'ra2/build-original-c/source-content-receipt.json');digest=sha(R/'ra2/build-original-c/ra2.exe')
assert receipt['executable_sha256']==digest==v['exe_sha256'] and receipt['source_count']==182 and len(receipt['inputs'])==313
for p,d in receipt['inputs'].items():assert sha(Path(p))==d,p
for e in read(S/'source-manifest.json'):
    assert sha(R/e['path'])==e['sha256']==sha(S/'final-source'/e['path']),e['path']
assert len(read(S/'source-manifest.json'))==v['source_files']
for e in read(S/'document-manifest.json'):
    assert sha(P/e['path'])==e['sha256']==sha(S/'current-project'/e['path']),e['path']
for folder in ['baseline','parts/closeout']:
    for e in read(S/folder/'manifest.json'):assert sha(S/folder/e['path'])==e['sha256'],(folder,e['path'])
part=read(S/'parts/closeout/validation.json');assert part['passed'] and part['exe_sha256']==digest
for e in read(S/'protected-inputs.json')['files']:assert sha(Path(e['path']))==e['sha256'],e['path']
assert sha(O/'source-manifest.json')==context['parent_manifest_sha256']
for e in read(O/'source-manifest.json'):assert sha(O/'final-source'/e['path'])==e['sha256'],e['path']
for e in read(S/'baseline-probe.json')['files']:assert sha(Path(e['path']))==e['sha256'],e['path']
assert sha(S/'baseline-observer/bridge-catalog-observer.exe')==read(S/'baseline-observer.json')['exe_sha256']
required=['source-preservation.json','movement-code-inventory.json','record-parity.json','reachability-fairness.json','occupation-stop-rules.json','other-movement-acceptance.json','stop-command-acceptance.json','regressions.json','final-native.json','map-area-original-calls.json','cleanup.json','remaining-work.json','other-movement-input-review.json','other-movement-checker-review.json','stop-command-checker-review.json']
for n in required:assert read(S/n)['passed'],n
for e in roll['traces']:assert sha(Path(e['path']))==e['sha256'],e['path']
for e in roll['helper_hashes_before_finalization']+roll['probe_and_observer_hashes']:assert sha(Path(e['path']))==e['sha256'],e['path']
strict=frames=0
for q in roll['pairs']:
    p=S/'runs'/q['tag']/'comparison.json';d=read(p);c=d['comparison'];assert sha(p)==q['comparison_sha256']
    assert c['frames_compared']==q['frames'] and c['negative_control']['passed'] and all(x['passed'] and x['exit_code']==0 for x in d['runs'])
    assert d['passed']==q['strict'];strict+=int(q['strict']);frames+=q['frames']
    if q['tag'] in ['b-gtypes','b-stopcmd','b-rq-prod']:expected=sha(S/'baseline/ra2/build-original-c/ra2.exe')
    elif q['tag'].startswith('b-'):expected=sha(S/'baseline-observer/bridge-catalog-observer.exe')
    elif q['tag']=='f-gtypes-obs':expected=sha(S/'other-movement-observer.exe')
    elif q['tag'].startswith('f-') and q['tag'] not in ['f-rq-prod','f-gtypes','f-stopcmd']:expected=sha(S/'bridge-catalog-observer.exe')
    else:expected=digest
    assert d['exe_sha256']==expected==q['exe_sha256'],q['tag']
    assert q['strict'] or q['tag'] in ['b-gtypes','f-gtypes','f-gtypes-obs']
assert frames==roll['accepted_frames']==v['accepted_frames'] and len(roll['pairs'])==v['accepted_game_pairs']
assert strict==roll['strict_pairs']==v['strict_game_pairs'] and len(roll['pairs'])-strict==3
keys={'prepare':['entry_cases','retry_cases'],'obstacle':['failed_rebuild_cases','rebuilt_cases'],'arrival':['native_arrival_cases'],'ground-services':['cases'],'collision':['native_occupation_cases','native_bridge_layer_cases'],'map-area':['map_area_cases']}
cases=0
for q in read(S/'final-native.json')['probes']:
    p=S/(q['probe'].replace('-','_')+'_probe.exe');assert sha(p)==q['exe_sha256'] and q['result']['passed']
    cases+=sum(q['result'][k] for k in keys[q['probe']])
assert cases==630784==v['native_cases']
for name in ['native-origins.json','collision-origin.json']:
    for e in read(S/name)['files']:assert sha(Path(e['path']))==e['sha256']==sha(Path(e['copy']))
assert sha(S/'analyze-other-initial.py')==read(S/'other-movement-checker-review.json')['initial_checker_sha256']
assert sha(S/'stop-command-initial.py')==read(S/'stop-command-checker-review.json')['initial_checker_sha256']
assert read(S/'reachability-fairness.json')['exact_arrivals']==12
assert len(read(S/'occupation-stop-rules.json')['mixed_requests'])==3
assert len(read(S/'other-movement-acceptance.json')['types'])==6
assert read(S/'movement-code-inventory.json')['guard_sites']==37 and read(S/'movement-code-inventory.json')['aliases']==29
pending=read(S/'scene-recipes-pending.json');assert sha(Path(pending['rules_original']))==pending['rules_original_sha256']
for n in ['community-reference-review.json','community-current-use.json','alias-evidence-inheritance.json']:assert sha(S/n)==sha(O/n),n
clean=read(S/'cleanup.json');plan=read(S/'cleanup-plan.json');assert clean['plan_sha256']==sha(S/'cleanup-plan.json') and clean['protected_unchanged']
for e in plan['protected']:assert sha(Path(e['path']))==e['sha256'],e['path']
for e in plan['candidates']:assert not Path(e['path']).exists(),e['path']
assert sha(P/'.git/config')==context['config_sha256']
assert hashlib.sha256(git('for-each-ref','--format=%(refname) %(objectname)','refs/remotes/')).hexdigest()==context['remote_refs_sha256']
if not precommit:
    assert not git('status','--porcelain','--untracked-files=all')
    assert git('rev-parse','HEAD^').decode().strip()==context['parent_commit']
print(dict(passed=True,formal=67,verification=68,exe_sha256=digest,source_files=v['source_files'],pairs=v['accepted_game_pairs'],frames=frames,native_cases=cases,precommit=precommit,pushed=False))
