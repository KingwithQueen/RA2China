"""Preserve accepted bytes and originals; distinguish current proofs from inherited history."""
from run_batch_v39 import R,P,S,O,read,write,sha
from pathlib import Path
import re,subprocess,hashlib
receipt=read(R/'ra2/build-original-c/source-content-receipt.json');assert receipt['source_count']==171 and len(receipt['inputs'])==292
assert receipt['executable_sha256']==sha(R/'ra2/build-original-c/ra2.exe')
old={e['path']:e['sha256'] for e in read(S/'baseline/manifest.json')};changed=[]
for name,digest in receipt['inputs'].items():
 p=Path(name);assert sha(p)==digest,name
 rel=p.relative_to(R).as_posix()
 if old[rel]!=digest:changed.append(rel)
assert set(changed)=={'ra2/src/runtime/ground_joint_bridge.c','ra2/src/runtime/ground_objects_bridge.c','ra2/src/recomp/gen_game/recomp_0010.c','ra2/src/recomp/gen_game/recomp_0046.c'},changed
parent={e['path']:e['sha256'] for e in read(S/'baseline/parent/source-manifest.json')}
for rel in ['run_fixture_comparison.py','run_state_comparison.py','ra2/src/runtime/state_trace.c']:
 assert sha(R/rel)==parent[rel],rel
for filename,nl in [('recomp_0010.c','LF'),('recomp_0046.c','CRLF')]:
 p=R/'ra2/src/recomp/gen_game'/filename;raw=p.read_bytes()
 assert (b'\r\n' not in raw) if nl=='LF' else raw.count(b'\n')==raw.count(b'\r\n')
 before=(S/'baseline'/p.relative_to(R)).read_text(encoding='utf-8');after=p.read_text(encoding='utf-8')
 for pattern in [r'^L_[0-9A-F]+:',r'case (0x[0-9A-Fa-f]+u): goto',r'ra2_recovery_unimplemented\((0x[0-9A-Fa-f]+)',r'/\* 0x[0-9A-F]+:[^\n]*']:
  assert re.findall(pattern,before,re.M)==re.findall(pattern,after,re.M),(filename,pattern)
guards=sum(len(re.findall(r'ra2_recovery_unimplemented\((0x[0-9A-Fa-f]+)',p.read_text(encoding='utf-8'))) for p in (R/'ra2/src/recomp/gen_game').glob('*.c'));assert guards==37
archives={}
for name in ['template','passage','returns']:
 part=S/'parts'/name;v=read(part/'validation.json');assert v['passed'] and v['scene_count']==3 and v['frames']==1303
 entries=read(part/'manifest.json')
 for e in entries:assert sha(part/e['path'])==e['sha256'],(name,e['path'])
 archives[name]=len(entries)
assert read(S/'parts/returns/validation.json')['exe_sha256']==receipt['executable_sha256']
for e in read(S/'baseline/manifest.json'):assert sha(S/'baseline'/e['path'])==e['sha256'],e['path']
for e in read(O/'source-manifest.json'):assert sha(O/'final-source'/e['path'])==e['sha256'],e['path']
assert sha(O/'source-manifest.json')==read(S/'baseline/receipt.json')['full_parent_manifest_sha256']
originals=read(R/'evidence/original-inputs-before.json');assert len(originals)==20
for e in originals:assert sha(Path('H:/开发/运行版本/原版1.006')/e['name'])==e['sha256'],e['name']
for p,digest in [(R/'ra2/game/game.exe','fe67fdac5073530a79baec14c4e072b5e7e4c0c462cee9659870c5330e9e6e3e'),(R/'ra2/game/SAVE0029.SAV','8a2e04fb4412aa5e51b6ffeacc5cb9fe265682d880966d39c1826dc810768b3b'),(P/'build/ra2battle.exe','05d7221ffacdddb2a300aee2c51b61d1fa1d269a5336a08e0c68b023f51bdd27')]:assert sha(p)==digest,str(p)
context=read(S/'vcs-context.json');assert sha(P/'.git/config')==context['config_sha256']
assert hashlib.sha256(subprocess.check_output(['git','-c','core.fsmonitor=false','for-each-ref','--format=%(refname) %(objectname)','refs/remotes/'],cwd=P)).hexdigest()==context['remote_refs_sha256']
v=read(S/'internal-alias-sources.json');assert v['alias_count']==29 and v['unique_native_edges']==86
assert not v['direct_call_candidates'] and not v['noncode_literal_candidates'] and not v['direct_c_reference_candidates']
assert read(S/'native-gates.json')['groups']==41
inputs=[Path(p) for p in receipt['inputs']]+[R/'ra2/game/game.exe',R/'build-overlap-probe-v39.ps1',R/'build-objects-probe-v39.ps1']
inputs += [p for p in S.iterdir() if p.is_file() and p.suffix in ['.c','.h','.asm']]
write(S/'native-input-identity.json',dict(passed=True,scope='Current affected probes and production input bytes. Other copied historical probe sources are retained recipes, not claimed as rerun.',inputs=[dict(path=p.relative_to(R).as_posix(),sha256=sha(p)) for p in inputs],probe_executables=[dict(path=p.relative_to(R).as_posix(),sha256=sha(p)) for p in [S/'overlap_probe.exe',S/'objects_probe.exe']],groups=41,new_cases=327680))
write(S/'preservation.json',dict(passed=True,changed_compile_inputs=changed,content_inputs=292,production_c_sources=171,unsupported_guards=guards,current_baseline_files=len(old),part_files=archives,accepted_parent_archive_files=len(parent),accepted_parent_archive_in_place=True,H_originals_checked=20,old_engine_and_original_save_preserved=True,native_labels_tails_annotations_and_registration_unchanged=True,comparator_and_recorder_unchanged=True,config_and_remote_refs_unchanged=True,whole_game_equivalence_verified=False))
print(dict(passed=True,changed_compile_inputs=changed,guards=guards,aliases=29,archives=archives),flush=True)
