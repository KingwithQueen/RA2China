"""Verify affected C content, preserved archives/originals and unchanged alias dispatch."""
from run_batch_v40 import R,P,S,O,read,write,sha
from pathlib import Path
import re,hashlib,subprocess
receipt=read(R/'ra2/build-original-c/source-content-receipt.json');assert receipt['source_count']==172 and len(receipt['inputs'])==294
assert receipt['executable_sha256']==sha(R/'ra2/build-original-c/ra2.exe')
before={e['path']:e['sha256'] for e in read(S/'baseline/manifest.json')};changed=[];added=[]
for name,digest in receipt['inputs'].items():
 p=Path(name);assert sha(p)==digest;rel=p.relative_to(R).as_posix()
 if rel not in before:added.append(rel)
 elif before[rel]!=digest:changed.append(rel)
assert set(changed)=={'ra2/src/gameplay/ground_advance.c','ra2/src/gameplay/ground_advance.h','ra2/src/runtime/ground_joint_bridge.c'},changed
assert set(added)=={'ra2/src/gameplay/ground_cell_placement.c','ra2/src/gameplay/ground_cell_placement.h'},added
parent={e['path']:e['sha256'] for e in read(O/'source-manifest.json')}
for rel in ['run_fixture_comparison.py','run_state_comparison.py','ra2/src/runtime/state_trace.c']:assert sha(R/rel)==parent[rel]
for e in read(S/'baseline/manifest.json'):assert sha(S/'baseline'/e['path'])==e['sha256']
for e in read(O/'source-manifest.json'):assert sha(O/'final-source'/e['path'])==e['sha256']
assert sha(O/'source-manifest.json')==read(S/'vcs-context.json')['parent_source_manifest_sha256']
parts={}
for name in ['advance','services']:
 out=S/'parts'/name;x=read(out/'validation.json');assert x['passed'] and x['frames']==1303
 for e in read(out/'manifest.json'):assert sha(out/e['path'])==e['sha256']
 parts[name]=dict(files=x['files'],exe_sha256=x['exe_sha256'])
assert parts['services']['exe_sha256']==receipt['executable_sha256']
guards=0;gen=[]
for p in (R/'ra2/src/recomp/gen_game').glob('*.c'):
 rel=p.relative_to(R).as_posix();assert sha(p)==before[rel];gen.append(rel)
 guards+=len(re.findall(r'ra2_recovery_unimplemented\(0x[0-9A-Fa-f]+',p.read_text(encoding='utf-8')))
assert guards==37
old=read(O/'internal-alias-sources.json');aliases={e['entry'] for e in old['entries'] if e['entry_kind']=='alias'};assert len(aliases)==29 and old['unique_native_edges']==86
pattern=re.compile(r'\b(?:'+'|'.join('sub_'+n for n in sorted(aliases))+r')\b');direct=[]
for path in receipt['inputs']:
 p=Path(path)
 for n,line in enumerate(p.read_text(encoding='utf-8').splitlines(),1):
  for m in pattern.finditer(line):
   name=m[0]
   known=line.startswith('/* '+name+' ') or line=='void '+name+'(void) {' or re.fullmatch(r'(?:extern )?void '+name+r'\(void\);',line) or re.fullmatch(r'\s*\{ 0x[0-9A-F]+u, '+name+r' \},',line)
   if not known:direct.append(dict(path=p.relative_to(R).as_posix(),line=n,text=line))
assert not direct,direct
write(S/'alias-evidence-inheritance.json',dict(passed=True,aliases=29,byte_checked_original_edges_in_parent=86,all_generated_functions_unchanged=True,direct_C_call_candidates=direct,new_native_entries=0,new_runtime_alias_observation_scenes=0,parent_static_inventory=str(O/'internal-alias-sources.json'),parent_static_inventory_sha256=sha(O/'internal-alias-sources.json'),parent_natural_observations=str(O/'alias-natural-scenes.json'),parent_natural_observations_sha256=sha(O/'alias-natural-scenes.json'),nonprimary_natural_entry_proved=False,scope='Original instruction bytes, generated entry/registration code and alias references unchanged. Prior bounded 29-candidate observations retained; no claim that their scenes were rerun. This open investigation is not a completion blocker.'))
for e in read(R/'evidence/original-inputs-before.json'):assert sha(Path('H:/开发/运行版本/原版1.006')/e['name'])==e['sha256']
for p,digest in [(R/'ra2/game/game.exe','fe67fdac5073530a79baec14c4e072b5e7e4c0c462cee9659870c5330e9e6e3e'),(R/'ra2/game/SAVE0029.SAV','8a2e04fb4412aa5e51b6ffeacc5cb9fe265682d880966d39c1826dc810768b3b'),(P/'build/ra2battle.exe','05d7221ffacdddb2a300aee2c51b61d1fa1d269a5336a08e0c68b023f51bdd27')]:assert sha(p)==digest
assert sha(P/'docs/项目目标与验收边界-20261024.txt')==sha(S/'baseline/project/docs/项目目标与验收边界-20261024.txt')
native=read(S/'native-gates.json');assert native['groups']==28
x=read(S/'native-advance.json');assert x['multiple_chain_target_cases'] and x['removed_before_enter_cases']
for name in native['receipts']:assert read(S/name)['passed']
inputs=[Path(p) for p in receipt['inputs']]+[R/'ra2/CMakeLists.txt',R/'ra2/game/game.exe',R/'build-advance-probe-v40.ps1',R/'build-overlap-probe-v40.ps1']+[p for p in S.iterdir() if p.is_file() and p.suffix in ['.c','.h','.asm']]
write(S/'native-input-identity.json',dict(passed=True,inputs=[dict(path=p.relative_to(R).as_posix(),sha256=sha(p)) for p in inputs],probe_executables=[dict(path=p.relative_to(R).as_posix(),sha256=sha(p)) for p in [S/'advance_probe.exe',S/'overlap_probe.exe']],scope='Native-oracle coverage for both workflows, train chain removal, death before entering and shared callbacks. Synthetic fragment evidence, not real train/bridge-destruction scene acceptance.'))
context=read(S/'vcs-context.json');assert sha(P/'.git/config')==context['config_sha256']
assert hashlib.sha256(subprocess.check_output(['git','-c','core.fsmonitor=false','for-each-ref','--format=%(refname) %(objectname)','refs/remotes/'],cwd=P)).hexdigest()==context['remote_refs_sha256']
write(S/'preservation.json',dict(passed=True,changed_compile_inputs=changed,added_compile_inputs=added,build_recipe_changed='ra2/CMakeLists.txt',source_count=172,content_inputs=294,unsupported_guards=37,generated_C_and_entry_tables_unchanged=True,parent_archive_files=len(parent),baseline_files=len(before),parts=parts,originals_checked=20,original_executable_save_and_old_engine_preserved=True,comparator_recorder_and_policy_unchanged=True))
print(dict(passed=True,changed=changed,added=added,source_count=172,inputs=294,guards=37,aliases=29))
