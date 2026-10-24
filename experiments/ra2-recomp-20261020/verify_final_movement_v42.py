"""Read-only acceptance, archive, original-input and local VCS verification."""
from run_batch_v42 import *
import re
precommit='--precommit' in sys.argv
v=read(S/'validation.json');assert v['passed'] and v['formal_baseline_generation']==41 and v['verification_round']==42
exe=R/'ra2/build-original-c/ra2.exe';assert sha(exe)==v['exe_sha256']
r=read(R/'ra2/build-original-c/source-content-receipt.json');assert r['source_count']==174 and len(r['inputs'])==298 and r['executable_sha256']==sha(exe)
for p,d in r['inputs'].items():assert sha(Path(p))==d,p
for stage in [S,O]:
 manifest=read(stage/'source-manifest.json')
 for e in manifest:
  assert sha(stage/'final-source'/e['path'])==e['sha256'],e['path']
  if stage==S:assert sha(R/e['path'])==e['sha256'],e['path']
 for e in read(stage/'document-manifest.json'):
  assert sha(stage/'current-project'/e['path'])==e['sha256']
  if stage==S:assert sha(P/e['path'])==e['sha256']
for e in read(S/'baseline/manifest.json'):assert sha(S/'baseline'/e['path'])==e['sha256']
assert sha(O/'source-manifest.json')==read(S/'vcs-context.json')['parent_source_manifest_sha256']
for part in ['prepare','advance']:
 root=S/'parts'/part;x=read(root/'validation.json');assert x['passed'] and x['scene_count']==3 and x['frames']==1303
 for e in read(root/'manifest.json'):assert sha(root/e['path'])==e['sha256']
 for a in x['scenes']:
  p=S/'runs'/a['tag']/'comparison.json';q=read(p);assert q['passed'] and sha(p)==a['comparison_sha256'] and q['exe_sha256']==x['exe_sha256']
assert read(S/'parts/advance/validation.json')['exe_sha256']==sha(exe)
native=read(S/'native-gates.json');assert native['passed'] and native['groups']==16 and native['cases']==1048576
for name in native['receipts']:
 x=read(S/name);assert x['passed'] and x['original_sha256']==sha(R/'ra2/game/game.exe')
matrix=read(S/'final-scene-matrix.json');frames=0
for a in matrix['results']:
 p=S/'runs'/a['tag']/'comparison.json';x=read(p);c=x['comparison'];assert x['passed'] and sha(p)==a['comparison_sha256'] and x['exe_sha256']==(sha(S/'bridge-catalog-observer.exe') if a['tag'].startswith('observed-') else sha(exe))
 assert c['equal_frames']==c['frames_compared'] and c['rng_equal_all_frames'] and c['negative_control']['passed'];frames+=c['frames_compared']
assert frames==matrix['production_frames']+matrix['observer_frames'] and frames+2606==v['accepted_frames']
assert read(S/'bridge-collapse-real-effects.json')['passed']
for n in ['effects.json','preservation.json','alias-evidence-inheritance.json','cleanup.json','remaining-work.json']:assert read(S/n)['passed']
fixtures=read(S/'representative-acceptance-fixtures.json')
for x in fixtures['fixtures']:
 assert sha(R/x['path'])==x['sha256']
 if x.get('rules'):assert sha(R/x['rules'])==x['rules_sha256']
assert sha(Path(fixtures['original_rules_source']))==fixtures['original_rules_sha256']
for e in read(R/'evidence/original-inputs-before.json'):assert sha(Path('H:/开发/运行版本/原版1.006')/e['name'])==e['sha256']
for p,d in [(R/'ra2/game/game.exe','fe67fdac5073530a79baec14c4e072b5e7e4c0c462cee9659870c5330e9e6e3e'),(R/'ra2/game/SAVE0029.SAV','8a2e04fb4412aa5e51b6ffeacc5cb9fe265682d880966d39c1826dc810768b3b'),(P/'build/ra2battle.exe','05d7221ffacdddb2a300aee2c51b61d1fa1d269a5336a08e0c68b023f51bdd27')]:assert sha(p)==d
for e in read(S/'cleanup-plan.json')['candidates']:assert not Path(e['path']).exists()
for e in read(S/'cleanup-plan.json')['protected']:assert sha(Path(e['path']))==e['sha256']
context=read(S/'vcs-context.json');assert sha(P/'.git/config')==context['config_sha256']
refs=subprocess.check_output(['git','-c','core.fsmonitor=false','for-each-ref','--format=%(refname) %(objectname)','refs/remotes/'],cwd=P);assert hashlib.sha256(refs).hexdigest()==context['remote_refs_sha256']
if not precommit:assert not subprocess.check_output(['git','-c','core.fsmonitor=false','status','--porcelain','--untracked-files=all'],cwd=P)
print(dict(passed=True,generation=41,exe_sha256=sha(exe),source_files=len(read(S/'source-manifest.json')),game_pairs=v['accepted_game_pairs'],frames=v['accepted_frames'],native_cases=native['cases'],precommit=precommit,pushed=False))
