"""Preservation and bounded legal-source audit for the new Prepare/Advance cycle."""
from run_batch_v46 import R,P,S,O,read,write,sha
from pathlib import Path
import re,hashlib,subprocess
receipt=read(R/'ra2/build-original-c/source-content-receipt.json');assert receipt['source_count']==177 and len(receipt['inputs'])==304
assert receipt['executable_sha256']==sha(R/'ra2/build-original-c/ra2.exe')
before={e['path']:e['sha256'] for e in read(S/'baseline/manifest.json')};changed=[];added=[]
for name,digest in receipt['inputs'].items():
 p=Path(name);assert sha(p)==digest;rel=p.relative_to(R).as_posix()
 if rel not in before:added.append(rel)
 elif before[rel]!=digest:changed.append(rel)
assert set(changed)=={'ra2/src/gameplay/'+n+'.c' for n in ['ground_arrival','ground_drive']},changed
assert set(added)=={'ra2/src/gameplay/ground_owner_boundary.c','ra2/src/gameplay/ground_owner_boundary.h'},added
parent={e['path']:e['sha256'] for e in read(O/'source-manifest.json')}
for rel in ['run_fixture_comparison.py','run_state_comparison.py','ra2/src/runtime/state_trace.c']:assert sha(R/rel)==parent[rel]
for e in read(S/'baseline/manifest.json'):assert sha(S/'baseline'/e['path'])==e['sha256']
for e in read(O/'source-manifest.json'):assert sha(O/'final-source'/e['path'])==e['sha256']
assert sha(O/'source-manifest.json')==read(S/'vcs-context.json')['parent_source_manifest_sha256']
parts={}
for name in ['arrival','drive']:
 out=S/'parts'/name;x=read(out/'validation.json');assert x['passed'] and x['frames']==1303
 for e in read(out/'manifest.json'):assert sha(out/e['path'])==e['sha256']
 parts[name]=dict(files=x['files'],exe_sha256=x['exe_sha256'])
assert parts['drive']['exe_sha256']==receipt['executable_sha256']
guards=0
for p in (R/'ra2/src/recomp/gen_game').glob('*.c'):
 rel=p.relative_to(R).as_posix();after=p.read_text(encoding='utf-8');guards+=len(re.findall(r'ra2_recovery_unimplemented\(0x[0-9A-Fa-f]+',after))
 assert sha(p)==before[rel]
assert guards==37
inherit=read(O/'alias-evidence-inheritance.json');inventory=Path(inherit['parent_static_inventory']);old=read(inventory)
aliases={e['entry'] for e in old['entries'] if e['entry_kind']=='alias'};assert len(aliases)==29 and old['unique_native_edges']==86
pattern=re.compile(r'\b(?:'+'|'.join('sub_'+n for n in sorted(aliases))+r')\b');direct=[]
for path in receipt['inputs']:
 p=Path(path)
 for n,line in enumerate(p.read_text(encoding='utf-8').splitlines(),1):
  for m in pattern.finditer(line):
   name=m[0];known=line.startswith('/* '+name+' ') or line=='void '+name+'(void) {' or re.fullmatch(r'(?:extern )?void '+name+r'\(void\);',line) or re.fullmatch(r'\s*\{ 0x[0-9A-F]+u, '+name+r' \},',line)
   if not known:direct.append(dict(path=p.relative_to(R).as_posix(),line=n,text=line))
assert not direct,direct
write(S/'alias-evidence-inheritance.json',dict(passed=True,aliases=29,byte_checked_original_edges_in_parent=86,all_original_labels_and_tail_tables_retained=True,direct_C_call_candidates=direct,new_native_entries=0,new_runtime_alias_observation_scenes=0,parent_static_inventory=str(inventory),parent_static_inventory_sha256=sha(inventory),parent_natural_observations=inherit['parent_natural_observations'],parent_natural_observations_sha256=sha(Path(inherit['parent_natural_observations'])),nonprimary_natural_entry_proved=False,scope='Two gameplay units and a new shared owner-boundary helper changed; generated/runtime glue unchanged; original instruction labels/tail dispatch and alias names/registrations retained. Prior bounded 29-candidate investigation inherited; no claim it was rerun.'))
for e in read(R/'evidence/original-inputs-before.json'):assert sha(Path('H:/开发/运行版本/原版1.006')/e['name'])==e['sha256']
for p,digest in [(R/'ra2/game/game.exe','fe67fdac5073530a79baec14c4e072b5e7e4c0c462cee9659870c5330e9e6e3e'),(R/'ra2/game/SAVE0029.SAV','8a2e04fb4412aa5e51b6ffeacc5cb9fe265682d880966d39c1826dc810768b3b'),(P/'build/ra2battle.exe','05d7221ffacdddb2a300aee2c51b61d1fa1d269a5336a08e0c68b023f51bdd27')]:assert sha(p)==digest
fixture=read(S/'collision-acceptance-fixtures.json');assert sha(Path(fixture['original_rules_source']))==fixture['original_rules_sha256']
for x in fixture['fixtures']:assert sha(R/x['path'])==x['sha256'] and sha(R/x['rules'])==x['rules_sha256']
assert sha(P/'docs/项目目标与验收边界-20261024.txt')==sha(S/'baseline/project/docs/项目目标与验收边界-20261024.txt')
native=read(S/'native-gates.json');assert native['groups']==2
for name in native['receipts']:assert read(S/name)['passed']
inputs=[Path(p) for p in receipt['inputs']]+[R/'ra2/CMakeLists.txt',R/'ra2/game/game.exe']+[p for p in S.iterdir() if p.is_file() and p.suffix in ['.c','.h','.asm']]+list(R.glob('build-*-probe-v46.ps1'))
write(S/'native-input-identity.json',dict(passed=True,inputs=[dict(path=p.relative_to(R).as_posix(),sha256=sha(p)) for p in inputs],probe_executables=[dict(path=p.relative_to(R).as_posix(),sha256=sha(p)) for p in [S/(name+'_probe.exe') for name in ['arrival','drive_process','capture_packet','transport_packet']]],groups=2,new_cycle_cases=98304,probe_build_identity='Each part manifest retains the exact sources/binaries at validation; the inputs list is the current production identity.'))
context=read(S/'vcs-context.json');assert sha(P/'.git/config')==context['config_sha256']
assert hashlib.sha256(subprocess.check_output(['git','-c','core.fsmonitor=false','for-each-ref','--format=%(refname) %(objectname)','refs/remotes/'],cwd=P)).hexdigest()==context['remote_refs_sha256']
write(S/'preservation.json',dict(passed=True,changed_compile_inputs=changed,added_compile_inputs=added,build_recipe_changed=True,source_count=177,content_inputs=304,unsupported_guards=37,native_labels_and_entry_tables_preserved=True,parent_archive_files=len(parent),baseline_files=len(before),parts=parts,originals_checked=20,original_rules_source_preserved=True,original_executable_save_and_old_engine_preserved=True,comparator_recorder_and_policy_unchanged=True))
print(dict(passed=True,changed=changed,added=added,source_count=177,inputs=304,guards=37,aliases=29))
