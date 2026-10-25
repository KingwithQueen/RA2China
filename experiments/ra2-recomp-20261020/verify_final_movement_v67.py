"""Read-only verification of current acceptance, archives, originals and local VCS."""
from run_batch_v67 import *
import re
precommit='--precommit' in sys.argv
v=read(S/'validation.json');assert v['passed'] and (v['formal_baseline_generation'],v['verification_round'])==(66,67)
assert v['positive_game_pairs']==15 and v['traffic_boundary_pairs']==8 and not v['all_traffic_requests_exactly_arrived']
exe=R/'ra2/build-original-c/ra2.exe';assert sha(exe)==v['exe_sha256']
assert not v['path_mechanism_identity_required'] and not v['globally_shortest_paths_verified']
assert v['rollback_parts']==['reaction','recovery'] and v['excluded_rollback_dirs']==[]
assert Path(v['pathfinding_policy_addendum'])==P/'docs/寻路机制改进验收补充-20261025.txt'
assert sha(P/'docs/项目目标与验收边界-20261024.txt')==sha(S/'baseline/project/docs/项目目标与验收边界-20261024.txt')
assert sha(P/'docs/寻路机制改进验收补充-20261025.txt')==sha(S/'baseline/project/docs/寻路机制改进验收补充-20261025.txt')
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
for part in ['reaction','recovery']:
 root=S/'parts'/part;x=read(root/'validation.json');assert x['passed'] and x['scene_count']==3 and x['frames']==1303
 compiled=read(root/'ra2/build-original-c/source-content-receipt.json');assert compiled['executable_sha256']==x['exe_sha256']==sha(root/'ra2/build-original-c/ra2.exe')
 for p,digest in compiled['inputs'].items():assert sha(root/Path(p).relative_to(R))==digest,p
 assert len(x['probes'])==5 and {read(S/n)['kind'] for n in x['probes']}=={'dispatch','report','attack','blocked','failure-budget-finish'}
 for e in read(root/'manifest.json'):assert sha(root/e['path'])==e['sha256']
 for name in x['probes']:
  proof=read(S/name);assert proof['passed'];exe_name=proof['probe_name']+'_probe.exe'
  assert proof['probe_exe_sha256']==sha(root/S.relative_to(R)/exe_name)
 for a in x['scenes']:
  p=S/'runs'/a['tag']/'comparison.json';q=read(p)
  assert q['passed'] and sha(p)==a['comparison_sha256'] and q['exe_sha256']==x['exe_sha256']
  for run in q['runs']:
   state=p.parent/run['mode']/'state.jsonl'
   if run.get('state_sha256'):assert sha(state)==run['state_sha256']
assert read(S/'parts/recovery/validation.json')['exe_sha256']==sha(exe)
native=read(S/'native-gates.json');assert native['passed'] and native['groups']==5 and native['cases']==393216
assert sum(read(S/n)['unique_cases'] for n in native['receipts'])==native['cases']
assert sorted(read(S/n)['unique_cases'] for n in native['receipts'])==[65536,65536,65536,65536,131072]
assert v['native_cases']==native['cases'] and v['synthetic_cases']==0 and v['new_traffic_recipes']==2
for name in native['receipts']:
 q=read(S/name);assert q['passed'] and q['original_sha256']==sha(R/'ra2/game/game.exe')
 assert q['probe_exe_sha256']==sha(S/(q['probe_name']+'_probe.exe'))
identity=read(S/'native-input-identity.json')
for item in identity['inputs']+identity['probe_executables']:assert sha(R/item['path'])==item['sha256']
baseline=read(S/'baseline-native-identity.json');assert baseline['passed']
for e in baseline['files']:assert sha(R/e['path'])==e['sha256']
for name in baseline['receipts']:
 proof=read(S/name);assert proof['passed']
 filename=proof['probe_name']+'_probe.exe'
 assert proof['probe_exe_sha256']==sha(S/'baseline-probe'/filename)
lineage=read(S/'checker-lineage.json');assert lineage['passed']
for item in lineage['entries']:
 assert sha(R/item['derived'])==item['final_derived_sha256']
 assert sha(R/item['source'])==item['source_sha256']
for item in lineage['native_origins']:assert sha(S/item['name'])==item['sha256']==sha(R/item['source'])
selected=read(S/'selected-baseline-scenes.json');assert selected['passed']
for item in selected['results']:
 p=R/'evidence'/item.get('stage',S.name)/'runs'/item['tag']/'comparison.json'
 assert sha(p)==item['comparison_sha256']
 assert read(p)['exe_sha256']==sha(S/'baseline-observer/bridge-catalog-observer.exe')
 for run in read(p)['runs']:assert sha(p.parent/run['mode']/'state.jsonl')==run['state_sha256']
matrix=read(S/'final-scene-matrix.json');traffic_baseline=read(S/'traffic-baseline-scenes.json');assert traffic_baseline['passed']
from accept_traffic_v67 import analyze as traffic_analyze
contract=read(S/'traffic-boundary-contract.json');assert contract['passed'] and len(contract['cases'])==4 and not contract['positive_recovery_acceptance']
review=read(S/'traffic-checker-review.json');assert review['passed'] and not review['positive_recovery_acceptance'] and sha(Path(review['initial_checker']))==review['initial_checker_sha256']
assert sha(S/'traffic-checker-review.json')==contract['checker_review_sha256']
frames=0;strict=6;pair_count=6
for a in matrix['results']+traffic_baseline['results']:
 p=S/'runs'/a['tag']/'comparison.json';x=read(p);c=x['comparison'];is_baseline=a in traffic_baseline['results']
 expected=sha(S/('baseline-channel-observer/channel-observer.exe' if is_baseline else 'channel-observer.exe')) if a['tag'].endswith('-obs') else sha(S/'baseline/ra2/build-original-c/ra2.exe') if is_baseline else sha(S/'bridge-catalog-observer.exe') if a['capture_host'] else sha(exe)
 assert sha(p)==a['comparison_sha256'] and x['exe_sha256']==expected
 for run in x['runs']:assert run['passed'] and sha(p.parent/run['mode']/'state.jsonl')==run['state_sha256']
 assert c['negative_control']['passed']
 if x['passed']:assert c['equal_frames']==c['frames_compared'] and c['rng_equal_all_frames'];strict+=1
 elif 'traffic-' not in a['tag']:
  assert a['tag'] in ['mi','sc','aw3','fm']
  from accept_dynamic_v67 import analyze
  assert analyze(a['tag'])['baseline_inherited_exactly']
 if 'traffic-' in a['tag']:
  proof=traffic_analyze(a['tag']);assert proof['passed'] and proof['acceptance_kind']=='original-behavior-boundary' and not proof['positive_recovery_acceptance']
 frames+=c['frames_compared'];pair_count+=1
assert frames+2606==v['accepted_frames']==62273 and pair_count==v['accepted_game_pairs']==23
assert strict==v['strict_game_pairs'] and pair_count-strict==v['functional_game_pairs']
assert read(S/'traffic-effects.json')['passed'] and read(S/'bridge-channel-effects.json')['passed']
assert read(S/'channel-comparison.json')['passed'] and read(S/'channel-host-identity.json')['passed']
prior=read(S/'prior-explorations.json');assert prior['passed'] and sha(Path(prior['path']))==prior['sha256']
assert read(S/'actor-catalog-validation.json')['passed']
for item in read(S/'actor-catalog-validation.json')['catalogs']:
 proof=S/'runs'/item['tag']/'comparison.json';assert sha(proof)==item['comparison_sha256'] and read(proof)['passed']
assert read(S/'fairness-effects.json')['passed'] and read(S/'traffic-map-provenance.json')['passed']
progress=read(S/'progress-inventory.json');assert progress['passed'] and progress['exe_sha256']==sha(exe) and progress['production_c_sources']==181 and progress['compile_inputs']==312 and progress['unimplemented_guard_sites']==37
assert sha(Path(progress['historical_lift_stats_path']))==progress['historical_lift_stats_sha256']
terrain=read(S/'traffic-goal-terrain-validation.json');assert terrain['passed']
for e in terrain['scenes']:
 assert sha(Path(e['catalog']))==e['catalog_sha256'] and any(x['tag']==e['tag'] and x['sha256']==e['map_sha256'] for x in read(S/'traffic-fixtures.json')['fixtures'])
 assert all(c['land'] in [0,1,6,7] and c['level']==4 for c in e['checked'])
parity=read(S/'channel-observer-baseline-parity.json');assert parity['passed'] and len(parity['records'])==4
assert parity['production_exe_sha256']==sha(S/'baseline/ra2/build-original-c/ra2.exe') and parity['observer_exe_sha256']==sha(S/'baseline-channel-observer/channel-observer.exe')
for e in read(S/'actor-catalog-validation.json')['catalogs']:
 proof=S/'runs'/e['tag']/'comparison.json';assert sha(proof)==e['comparison_sha256'] and read(proof)['passed']
for e in read(S/'traffic-map-provenance.json')['maps']:
 assert sha(Path(e['source']))==e['source_sha256'] and sha(R/e['path'])==e['sha256']
 assert e['only_units_and_infantry_changed']
 def without_units(text):
  for key in ['Units','Infantry']:text=re.sub(rf'(?ms)^\[{key}\]\n.*?(?=^\[|\Z)','['+key+']\n\n',text)
  return text
 assert without_units((R/e['path']).read_text(encoding='ascii'))==without_units(Path(e['source']).read_text(encoding='ascii'))
for e in read(S/'current-explorations.json')['records']:assert sha(Path(e['path']))==e['sha256']
for e in read(S/'baseline-channel-observer/manifest.json'):assert sha(S/'baseline-channel-observer'/e['path'])==e['sha256']
short=read(S/'prior-traffic-inheritance.json');assert short['passed'] and sha(Path(short['parent']))==short['sha256']
assert read(S/'traffic-event-linkage.json')['passed']
for item in read(S/'traffic-fixtures.json')['fixtures']:
 assert sha(R/item['path'])==item['sha256'] and item['source_sha256']==sha(Path(item['source']))
inherited=read(S/'heap-improvement-inheritance.json');assert inherited['passed'] and not inherited['rerun_as_current_cases']
assert sha(Path(inherited['direct_parent']))==inherited['direct_parent_sha256']
for item in inherited['files']:assert sha(Path(item['path']))==item['sha256']
for item in inherited['production_units']:assert sha(R/item['path'])==item['sha256']
assert read(S/'fixture-host-identity.json')['passed']
for name in ['capture_packet_probe.c','capture_packet_probe.exe','capture-native-validation.json','transport_packet_probe.c','transport_packet_probe.exe','transport-native-validation-current.json']:
 assert sha(S/name)==sha(O/name)
assert read(S/'capture-native-validation.json')['passed']
transport=read(S/'transport-native-validation-current.json');assert transport['passed'] and transport['native_transport_constructor_cases']==128
assert transport['source_sha256']==sha(S/'transport_packet_probe.c') and transport['probe_sha256']==sha(S/'transport_packet_probe.exe')
for e in read(S/'baseline-observer/manifest.json'):assert sha(S/'baseline-observer'/e['path'])==e['sha256']
for n in ['effects.json','preservation.json','alias-evidence-inheritance.json','cleanup.json','remaining-work.json','service-boundaries.json','rng-first-split-window.json','boundary-inheritance.json','infrastructure-status.json','community-reference-review.json']:
 assert read(S/n)['passed'],n
for stage in [S,O]:
 alias=read(stage/'alias-evidence-inheritance.json')
 assert sha(Path(alias['parent_static_inventory']))==alias['parent_static_inventory_sha256']
 assert sha(Path(alias['parent_natural_observations']))==alias['parent_natural_observations_sha256']
assert len(read(S/'baseline/manifest.json'))==315
assert set(read(S/'preservation.json')['changed_compile_inputs'])=={'ra2/src/gameplay/ground_reaction.c','ra2/src/gameplay/ground_recovery.c'}
references=read(S/'community-reference-review.json')
assert len(references['sources'])==5 and references['reference_only']
assert sha(S/'community-reference-review.json')==sha(O/'community-reference-review.json')
use=read(S/'community-current-use.json');assert sha(S/'community-current-use.json')==sha(O/'community-current-use.json') and use['passed'] and len(use['rechecked'])==2 and use['locked_review_sha256']==sha(S/'community-reference-review.json')
for e in use['rechecked']:assert any(e['sha256']==q['sha256'] and e['revision']==q['revision'] for q in references['sources'])
assert not references['third_party_engine_code_imported'] and not references['private_project_uploaded']
for item in references['sources']:
 assert re.fullmatch('[0-9a-f]{40}',item['revision']) and re.fullmatch('[0-9a-f]{64}',item['sha256'])
 assert item['url'].startswith('https://github.com/') and item['bytes']>0
assert not list((R/'temp').glob('community-ref-v67-*.dat'))
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
final_check=read(S/'final-check.json');assert final_check['passed'] and not final_check['pushed']
assert final_check['source_manifest_sha256']==sha(S/'source-manifest.json') and final_check['document_manifest_sha256']==sha(S/'document-manifest.json')
refs=subprocess.check_output(['git','-c','core.fsmonitor=false','for-each-ref','--format=%(refname) %(objectname)','refs/remotes/'],cwd=P)
assert hashlib.sha256(refs).hexdigest()==context['remote_refs_sha256']
if not precommit:assert not subprocess.check_output(['git','-c','core.fsmonitor=false','status','--porcelain','--untracked-files=all'],cwd=P)
print(dict(passed=True,generation=66,exe_sha256=sha(exe),source_files=len(read(S/'source-manifest.json')),game_pairs=v['accepted_game_pairs'],frames=v['accepted_frames'],native_cases=native['cases'],precommit=precommit,pushed=False))
