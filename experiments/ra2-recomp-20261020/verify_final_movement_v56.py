"""Read-only verification of current acceptance, archives, originals and local VCS."""
from run_batch_v56 import *
import re
precommit='--precommit' in sys.argv
v=read(S/'validation.json');assert v['passed'] and (v['formal_baseline_generation'],v['verification_round'])==(55,56)
exe=R/'ra2/build-original-c/ra2.exe';assert sha(exe)==v['exe_sha256']
r=read(R/'ra2/build-original-c/source-content-receipt.json')
assert r['source_count']==181 and len(r['inputs'])==312 and r['executable_sha256']==sha(exe)
for p,d in r['inputs'].items():assert sha(Path(p))==d,p
for stage in [S,O]:
 for e in read(stage/'source-manifest.json'):
  assert sha(stage/'final-source'/e['path'])==e['sha256'],e['path']
  if stage==S:assert sha(R/e['path'])==e['sha256'],e['path']
 for e in read(stage/'document-manifest.json'):
  assert sha(stage/'current-project'/e['path'])==e['sha256']
  if stage==S:assert sha(P/e['path'])==e['sha256']
for e in read(S/'baseline/manifest.json'):assert sha(S/'baseline'/e['path'])==e['sha256']
assert sha(O/'source-manifest.json')==read(S/'vcs-context.json')['parent_source_manifest_sha256']
for part in ['layers','edges']:
 root=S/'parts'/part;x=read(root/'validation.json');assert x['passed'] and x['scene_count']==3 and x['frames']==1303
 for e in read(root/'manifest.json'):assert sha(root/e['path'])==e['sha256']
 for name in x['probes']:
  proof=read(S/name);assert proof['passed'] and proof['cases']==6144
  assert proof['successes']>0 and proof['failures']>0 and proof['final_numeric_control_compared']
  assert proof['successes']+proof['failures']==6144
  assert proof['probe_exe_sha256']==sha(root/S.relative_to(R)/'region_search_probe.exe')
 for a in x['scenes']:
  p=S/'runs'/a['tag']/'comparison.json';q=read(p)
  assert q['passed'] and sha(p)==a['comparison_sha256'] and q['exe_sha256']==x['exe_sha256']
  for run in q['runs']:
   state=p.parent/run['mode']/'state.jsonl'
   if run.get('state_sha256'):assert sha(state)==run['state_sha256']
assert read(S/'parts/edges/validation.json')['exe_sha256']==sha(exe)
native=read(S/'native-gates.json');assert native['passed'] and native['groups']==1 and native['cases']==6144
for name in native['receipts']:
 x=read(S/name);assert x['passed'] and x['original_sha256']==sha(R/'ra2/game/game.exe')
 assert x['probe_exe_sha256']==sha(S/'region_search_probe.exe')
identity=read(S/'native-input-identity.json')
for item in identity['inputs']+identity['probe_executables']:assert sha(R/item['path'])==item['sha256']
baseline=read(S/'part-baseline-region-search.json');assert baseline['passed'] and baseline['cases']==6144 and baseline['final_numeric_control_compared']
selected=read(S/'selected-baseline-scenes.json');assert selected['passed']
for item in selected['results']:
 p=R/'evidence'/item.get('stage',S.name)/'runs'/item['tag']/'comparison.json'
 assert sha(p)==item['comparison_sha256']
 assert read(p)['exe_sha256']==sha(S/'baseline-observer/bridge-catalog-observer.exe')
 for run in read(p)['runs']:assert sha(p.parent/run['mode']/'state.jsonl')==run['state_sha256']
matrix=read(S/'final-scene-matrix.json');frames=0;variations=0
for a in matrix['results']:
 p=S/'runs'/a['tag']/'comparison.json';x=read(p);c=x['comparison']
 assert sha(p)==a['comparison_sha256'] and x['exe_sha256']==(sha(S/'bridge-catalog-observer.exe') if a['capture_host'] else sha(exe))
 for run in x['runs']:assert run['passed'] and sha(p.parent/run['mode']/'state.jsonl')==run['state_sha256']
 assert c['negative_control']['passed']
 if x['passed']:assert c['equal_frames']==c['frames_compared'] and c['rng_equal_all_frames']
 else:
  assert a['tag'] in ['mi','sc','aw3','fm'];variations+=1
  from accept_dynamic_v56 import analyze
  assert analyze(a['tag'])['baseline_inherited_exactly']
 frames+=c['frames_compared']
assert frames==matrix['production_frames']+matrix['observer_frames'] and frames+2606==v['accepted_frames']==19065
assert variations==4 and v['accepted_game_pairs']==15 and v['strict_game_pairs']==11
assert read(S/'fixture-host-identity.json')['passed']
for name in ['capture_packet_probe.c','capture_packet_probe.exe','capture-native-validation.json','transport_packet_probe.c','transport_packet_probe.exe','transport-native-validation-current.json']:
 assert sha(S/name)==sha(O/name)
assert read(S/'capture-native-validation.json')['passed']
transport=read(S/'transport-native-validation-current.json');assert transport['passed'] and transport['native_transport_constructor_cases']==128
assert transport['source_sha256']==sha(S/'transport_packet_probe.c') and transport['probe_sha256']==sha(S/'transport_packet_probe.exe')
for e in read(S/'baseline-observer/manifest.json'):assert sha(S/'baseline-observer'/e['path'])==e['sha256']
for n in ['effects.json','preservation.json','alias-evidence-inheritance.json','cleanup.json','remaining-work.json','service-boundaries.json','rng-first-split-window.json','boundary-inheritance.json','infrastructure-status.json','tooling-correction.json']:
 assert read(S/n)['passed'],n
for stage in [S,O]:
 alias=read(stage/'alias-evidence-inheritance.json')
 assert sha(Path(alias['parent_static_inventory']))==alias['parent_static_inventory_sha256']
 assert sha(Path(alias['parent_natural_observations']))==alias['parent_natural_observations_sha256']
assert len(read(S/'baseline/manifest.json'))==315
assert read(S/'preservation.json')['changed_compile_inputs']==['ra2/src/gameplay/ground_region_search.c']
correction=read(S/'tooling-correction.json')
assert correction['current_helper_sha256']==sha(R/'run_batch_v56.py')
assert correction['executed_part_helper_sha256']==sha(S/'parts/edges/run_batch_v56.py')
assert correction['parent_manifest_sha256']==sha(O/'source-manifest.json')
for x in read(S/'boundary-inheritance.json')['files'].values():assert sha(Path(x['path']))==x['sha256']
rng=read(S/'rng-functional-impact.json');assert rng['passed']
for x in rng['protected_parent_files']:assert sha(Path(x['path']))==x['sha256']
for x in read(S/'dynamic-fixtures.json')['fixtures']:
 assert sha(R/x['path'])==x['sha256']
 if x.get('rules'):assert sha(R/x['rules'])==x['rules_sha256']
rules=read(S/'collision-acceptance-fixtures.json');assert sha(Path(rules['original_rules_source']))==rules['original_rules_sha256']
for e in read(R/'evidence/original-inputs-before.json'):assert sha(Path('H:/开发/运行版本/原版1.006')/e['name'])==e['sha256']
for p,d in [(R/'ra2/game/game.exe','fe67fdac5073530a79baec14c4e072b5e7e4c0c462cee9659870c5330e9e6e3e'),(R/'ra2/game/SAVE0029.SAV','8a2e04fb4412aa5e51b6ffeacc5cb9fe265682d880966d39c1826dc810768b3b'),(P/'build/ra2battle.exe','05d7221ffacdddb2a300aee2c51b61d1fa1d269a5336a08e0c68b023f51bdd27')]:assert sha(p)==d
for e in read(S/'cleanup-plan.json')['candidates']:assert not Path(e['path']).exists()
for e in read(S/'cleanup-plan.json')['protected']:assert sha(Path(e['path']))==e['sha256']
context=read(S/'vcs-context.json');assert sha(P/'.git/config')==context['config_sha256']
refs=subprocess.check_output(['git','-c','core.fsmonitor=false','for-each-ref','--format=%(refname) %(objectname)','refs/remotes/'],cwd=P)
assert hashlib.sha256(refs).hexdigest()==context['remote_refs_sha256']
if not precommit:assert not subprocess.check_output(['git','-c','core.fsmonitor=false','status','--porcelain','--untracked-files=all'],cwd=P)
print(dict(passed=True,generation=55,exe_sha256=sha(exe),source_files=len(read(S/'source-manifest.json')),game_pairs=15,frames=19065,native_cases=6144,precommit=precommit,pushed=False))
