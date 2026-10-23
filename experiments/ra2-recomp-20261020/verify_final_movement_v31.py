"""Read-only verification of generation30, accepted source bytes and local commit."""
from pathlib import Path
import hashlib,json,subprocess
R=Path(__file__).resolve().parent;P=R.parent.parent;S=R/'evidence/movement-state-v31'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
v=read(S/'validation.json');f=read(S/'final-check.json')
assert v['passed'] and f['passed'] and v['formal_baseline_generation']==30 and v['verification_round']==31
assert v['paired_scenes']==56 and v['paired_frames']==35726 and v['probes']==105 and v['new_fragment_cases']==196608
assert v['content_inputs']==290 and v['production_c_sources']==171 and v['unsupported_guards']==37
assert v['bridge_hostile_dynamic_traffic_verified']
assert v['bridge_mixed_object_chain_verified'] and v['bridge_opposing_dynamic_traffic_verified']
assert v['legal_alias_sources_examined']==26 and v['independent_alias_observer_frames']==3604
assert read(S/'alias-natural-scenes.json')['passed'] and read(S/'internal-alias-sources.json')['passed']
assert not v['nonprimary_overlapping_adapter_naturally_observed'] and not v['full_original_equivalence_verified']
assert v['original_equivalent_stall_scenes']==2 and not v['all_curved_height_routes_complete']
assert sha(R/'ra2/build-original-c/ra2.exe')==v['exe_sha256']==f['exe_sha256']
for e in read(S/'source-manifest.json'):assert sha(R/e['path'])==sha(S/'final-source'/e['path'])==e['sha256'],e['path']
for name in ['latest-recovery.json','latest-state-comparison.json','latest-movement-candidate.json']:
    x=read(P/'reports'/name);assert Path(x['validation'])==S/'validation.json';assert x.get('sha256',x.get('exe_sha256'))==v['exe_sha256']
for key in ['report','handoff']:assert sha(Path(v[key]))==f[key+'_sha256']
for name in ['git-byte-audit.json','git-whitespace-audit.json','bridge-mixed-real-scenes.json','bridge-hostile-real-scenes.json','recipe-byte-audit.json','preservation.json']:assert read(S/name)['passed']
context=read(S/'vcs-context.json');assert sha(P/'.git/config')==context['config_sha256']
assert hashlib.sha256(subprocess.check_output(['git','-c','core.fsmonitor=false','for-each-ref','--format=%(refname) %(objectname)','refs/remotes/'],cwd=P)).hexdigest()==context['remote_refs_sha256']
assert not subprocess.check_output(['git','-c','core.fsmonitor=false','status','--porcelain'],cwd=P)
print(json.dumps(dict(passed=True,commit=subprocess.check_output(['git','-c','core.fsmonitor=false','rev-parse','HEAD'],cwd=P,text=True).strip(),clean=True,exe_sha256=v['exe_sha256'],source_files=v['source_files'],pushed=False)))
