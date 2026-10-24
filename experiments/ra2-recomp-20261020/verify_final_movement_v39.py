"""Read-only verification of current generation38; accepted history remains in place."""
from run_batch_v39 import R,P,S,O,read,sha
from pathlib import Path
import argparse,subprocess,hashlib,json
ap=argparse.ArgumentParser();ap.add_argument('--precommit',action='store_true');a=ap.parse_args()
v=read(S/'validation.json');f=read(S/'final-check.json');assert v['passed'] and f['passed']
assert v['formal_baseline_generation']==38 and v['verification_round']==39
assert v['finite_functional_conformance'] and not v['bug_for_bug_required'] and not v['full_original_equivalence_verified']
assert v['paired_scenes']==9 and v['paired_frames']==5459 and v['observer_frames']==4008 and v['part_frames']==3909
assert v['total_game_pairs_executed']==26 and v['total_frames_compared']==13376 and v['probes']==41
assert v['new_fragment_cases']==327680 and v['content_inputs']==292 and v['unsupported_guards']==37
assert sha(R/'ra2/build-original-c/ra2.exe')==v['exe_sha256']==f['exe_sha256']
manifest=read(S/'source-manifest.json');assert len(manifest)==v['source_files'] and sha(S/'source-manifest.json')==f['source_manifest_sha256']
for e in manifest:assert sha(R/e['path'])==sha(S/'final-source'/e['path'])==e['sha256'],e['path']
assert sha(S/'document-manifest.json')==f['document_manifest_sha256']
for e in read(S/'document-manifest.json'):assert sha(P/e['path'])==sha(S/'current-project'/e['path'])==e['sha256'],e['path']
for key in ['report','handoff','acceptance_policy']:
 field='policy' if key=='acceptance_policy' else key
 assert sha(Path(v[key]))==f[field+'_sha256']
receipt=read(R/'ra2/build-original-c/source-content-receipt.json');assert len(receipt['inputs'])==292 and receipt['source_count']==171
for p,digest in receipt['inputs'].items():assert sha(Path(p))==digest,p
for name in ['native-gates.json','native-input-identity.json','preservation.json','effects.json','alias-natural-scenes.json','bridge-cross-release-effects.json','internal-alias-sources.json','cleanup.json','remaining-work.json']:
 x=read(S/name);assert x['passed'],name
 if name=='native-input-identity.json':
  for e in x['inputs']+x['probe_executables']:assert sha(R/e['path'])==e['sha256'],e['path']
assert read(S/'native-gates.json')['groups']==41
for name in read(S/'native-gates.json')['receipts']:assert read(S/name)['passed'],name
parts={}
for name in ['template','passage','returns']:
 out=S/'parts'/name;x=read(out/'validation.json');assert x['passed'] and x['frames']==1303
 for e in read(out/'manifest.json'):assert sha(out/e['path'])==e['sha256'],e['path']
 parts[name]=x
assert parts['returns']['exe_sha256']==v['exe_sha256']
for e in read(S/'baseline/manifest.json'):assert sha(S/'baseline'/e['path'])==e['sha256'],e['path']
assert sha(O/'source-manifest.json')==read(S/'baseline/receipt.json')['full_parent_manifest_sha256']
scenes=[x['tag'] for x in read(S/'final-scene-matrix.json')['results']]+[r['tag'] for p in parts.values() for r in p['scenes']]
assert len(scenes)==len(set(scenes))==26
frames=0
for tag in scenes:
 x=read(S/'runs'/tag/'comparison.json');c=x['comparison'];assert x['passed'] and c['frames_compared']==c['equal_frames'] and c['rng_equal_all_frames'];frames+=c['frames_compared']
assert frames==13376
aliases=read(S/'alias-natural-scenes.json');assert aliases['aliases']==29 and not aliases['natural_entry_candidates']
inventory=read(S/'internal-alias-sources.json');assert inventory['alias_count']==29 and inventory['unique_native_edges']==86
assert not inventory['direct_call_candidates'] and not inventory['noncode_literal_candidates'] and not inventory['direct_c_reference_candidates']
assert not read(S/'remaining-work.json')['natural_aliases_required_for_completion']
clean=read(S/'cleanup.json');assert clean['protected_files_unchanged'] and sha(S/'cleanup-plan.json')==clean['plan_sha256']
for e in read(S/'cleanup-plan.json')['candidates']:assert not Path(e['path']).exists(),e['path']
for name in ['latest-recovery.json','latest-state-comparison.json','latest-movement-candidate.json']:
 x=read(P/'reports'/name);assert x['validation']==str(S/'validation.json') and x['exe_sha256']==v['exe_sha256']
context=read(S/'vcs-context.json');assert sha(P/'.git/config')==context['config_sha256']
git=lambda *args:subprocess.check_output(['git','-c','core.fsmonitor=false',*args],cwd=P)
assert hashlib.sha256(git('for-each-ref','--format=%(refname) %(objectname)','refs/remotes/')).hexdigest()==context['remote_refs_sha256']
commit=git('rev-parse','HEAD').decode().strip()
if a.precommit:assert commit==context['parent_commit']
else:
 assert not git('status','--porcelain','--untracked-files=all')
 assert git('rev-parse','HEAD^').decode().strip()==context['parent_commit']
 for name in ['git-byte-audit.json','git-whitespace-audit.json','git-staging-scope.json']:assert read(S/name)['passed']
print(json.dumps(dict(passed=True,precommit=a.precommit,commit=commit,exe_sha256=v['exe_sha256'],source_files=len(manifest),scene_pairs=26,frames=13376,clean=not bool(git('status','--porcelain','--untracked-files=all')),pushed=False)),flush=True)
