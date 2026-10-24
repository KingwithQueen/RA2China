"""Read-only verification of generation40, current executable/source/archive and local Git."""
from run_batch_v41 import R,P,S,O,read,sha
from pathlib import Path
import argparse,json,subprocess,hashlib
ap=argparse.ArgumentParser();ap.add_argument('--precommit',action='store_true');a=ap.parse_args()
v=read(S/'validation.json');f=read(S/'final-check.json')
assert v['passed'] and f['passed'] and v['formal_baseline_generation']==40 and v['verification_round']==41
assert v['finite_functional_conformance'] and not v['bug_for_bug_required'] and not v['full_original_equivalence_verified']
assert v['total_game_pairs_executed']==24 and v['total_frames_compared']==12574 and v['probes']==6
assert v['native_cases']==393216 and v['production_c_sources']==173 and v['content_inputs']==296 and v['unsupported_guards']==37
assert sha(R/'ra2/build-original-c/ra2.exe')==v['exe_sha256']==f['exe_sha256']
manifest=read(S/'source-manifest.json');assert len(manifest)==v['source_files'] and sha(S/'source-manifest.json')==f['source_manifest_sha256']
for e in manifest:assert sha(R/e['path'])==sha(S/'final-source'/e['path'])==e['sha256'],e['path']
assert sha(S/'document-manifest.json')==f['document_manifest_sha256']
for e in read(S/'document-manifest.json'):assert sha(P/e['path'])==sha(S/'current-project'/e['path'])==e['sha256'],e['path']
for key,field in [('report','report'),('handoff','handoff'),('acceptance_policy','policy')]:assert sha(Path(v[key]))==f[field+'_sha256']
receipt=read(R/'ra2/build-original-c/source-content-receipt.json');assert receipt['source_count']==173 and len(receipt['inputs'])==296
for p,digest in receipt['inputs'].items():assert sha(Path(p))==digest,p
for name in ['native-gates.json','native-input-identity.json','preservation.json','effects.json','alias-evidence-inheritance.json','bridge-cross-release-effects.json','cleanup.json','remaining-work.json','collision-real-effects.json','collision-trial-status.json','prepare-boundary-resolution.json','observer-variation.json']:
 x=read(S/name);assert x['passed'],name
 if name=='native-input-identity.json':
  for e in x['inputs']+x['probe_executables']:assert sha(R/e['path'])==e['sha256'],e['path']
for name in read(S/'native-gates.json')['receipts']:assert read(S/name)['passed'],name
x=read(S/'native-advance.json');assert x['multiple_chain_target_cases']==1841 and x['removed_before_enter_cases']==2383
parts={}
for name in ['prepare','advance']:
 out=S/'parts'/name;x=read(out/'validation.json');assert x['passed'] and x['scene_count']==3 and x['frames']==1303
 for e in read(out/'manifest.json'):assert sha(out/e['path'])==e['sha256'],e['path']
 parts[name]=x
assert parts['advance']['exe_sha256']==v['exe_sha256']
for e in read(S/'baseline/manifest.json'):assert sha(S/'baseline'/e['path'])==e['sha256'],e['path']
context=read(S/'vcs-context.json');assert sha(O/'source-manifest.json')==context['parent_source_manifest_sha256']
scenes=[x['tag'] for x in read(S/'final-scene-matrix.json')['results']]+[r['tag'] for p in parts.values() for r in p['scenes']]
assert len(scenes)==len(set(scenes))==20
frames=0
for tag in scenes:
 x=read(S/'runs'/tag/'comparison.json');c=x['comparison'];functional=S/'runs'/tag/'functional-acceptance.json'
 accepted=x['passed'] or (tag=='observed-contact-train' and functional.exists() and read(functional)['passed'] and read(functional)['comparison_sha256']==sha(S/'runs'/tag/'comparison.json'))
 assert accepted and x['seed']==12345 and c['frames_compared']==c['equal_frames'] and c['rng_equal_all_frames'];frames+=c['frames_compared']
assert frames==10570
for tag in ['baseline-train','baseline-crush','baseline02-train','baseline02-crush']:
 x=read(S/'runs'/tag/'comparison.json');assert x['passed'] and x['comparison']['frames_compared']==501;frames+=501
assert frames==12574
assert v['accepted_game_pairs']==20 and v['accepted_frames']==10570
real=read(S/'collision-real-effects.json')['scenes'];assert real['train']['actor_final_health']==160 and real['crush']['actor_final_health']==200
assert real['train-control']['targets_preserved'] and real['crush-control']['targets_preserved']
aliases=read(S/'alias-evidence-inheritance.json');assert aliases['aliases']==29 and aliases['new_runtime_alias_observation_scenes']==0 and not aliases['direct_C_call_candidates']
assert sha(Path(aliases['parent_static_inventory']))==aliases['parent_static_inventory_sha256'] and sha(Path(aliases['parent_natural_observations']))==aliases['parent_natural_observations_sha256']
assert not read(S/'remaining-work.json')['natural_alias_dispatch_required']
clean=read(S/'cleanup.json');assert clean['protected_files_unchanged'] and sha(S/'cleanup-plan.json')==clean['plan_sha256']
for e in read(S/'cleanup-plan.json')['candidates']:assert not Path(e['path']).exists(),e['path']
for name in ['latest-recovery.json','latest-state-comparison.json','latest-movement-candidate.json']:
 x=read(P/'reports'/name);assert x['validation']==str(S/'validation.json') and x['exe_sha256']==v['exe_sha256']
assert sha(P/'.git/config')==context['config_sha256']
git=lambda *args:subprocess.check_output(['git','-c','core.fsmonitor=false',*args],cwd=P)
assert hashlib.sha256(git('for-each-ref','--format=%(refname) %(objectname)','refs/remotes/')).hexdigest()==context['remote_refs_sha256']
commit=git('rev-parse','HEAD').decode().strip()
if a.precommit:assert commit==context['parent_commit']
else:
 assert not git('status','--porcelain','--untracked-files=all')
 assert git('rev-parse','HEAD^').decode().strip()==context['parent_commit']
 for name in ['git-byte-audit.json','git-whitespace-audit.json','git-staging-scope.json']:assert read(S/name)['passed']
print(json.dumps(dict(passed=True,precommit=a.precommit,commit=commit,exe_sha256=v['exe_sha256'],source_files=len(manifest),accepted_scene_pairs=20,accepted_frames=10570,executed_pairs=24,clean=not bool(git('status','--porcelain','--untracked-files=all')),pushed=False)))
