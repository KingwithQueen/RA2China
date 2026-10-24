"""Keep the accepted archive in place and save a bounded, independent build rollback."""
from pathlib import Path
import hashlib,json,shutil,subprocess
R=Path(__file__).resolve().parent;P=R.parent.parent;O=R/'evidence/movement-state-v38';S=R/'evidence/movement-state-v39'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert not S.exists()
assert subprocess.check_output(['git','-c','core.fsmonitor=false','rev-parse','HEAD'],cwd=P,text=True).strip()=='65ffecb844c08b0dbc5d46c53b7646635572c108'
assert subprocess.check_output(['git','-c','core.fsmonitor=false','status','--porcelain'],cwd=P)==b'?? experiments/ra2-recomp-20261020/prepare_movement_v39.py\n'
assert sha(R/'ra2/build-original-c/ra2.exe')=='d697cc4c16d5cb103343c2743c11146eb09b3f13d5c7683b8adbeef8821ae7c8'
S.mkdir();(S/'runs').mkdir();(S/'pending').mkdir()
receipt=json.loads((R/'ra2/build-original-c/source-content-receipt.json').read_text(encoding='utf-8-sig'));assert len(receipt['inputs'])==292
paths={Path(p).relative_to(R).as_posix() for p in receipt['inputs']};paths.add('ra2/build-original-c/ra2.exe')
paths.update(p.relative_to(R).as_posix() for p in O.iterdir() if p.is_file() and p.suffix in ['.c','.h','.asm'])
manifest=[]
for rel in sorted(paths):
 d=S/'baseline'/rel;d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/rel,d);manifest.append(dict(path=rel,sha256=sha(d)))
docs=['README.md','reports/latest-recovery.json','reports/latest-state-comparison.json','reports/latest-movement-candidate.json','交接文档-原版逆向与C重编译-20261020.txt','交接文档-新对话继续推进-20261022.txt','交接文档-单位移动第三十七批正式验收-20261024.txt','docs/单位移动第三十七批-桥层写回与武器分类及桥上相邻车道放行组合-20261024.txt']
for rel in docs:
 d=S/'baseline/project'/rel;d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(P/rel,d)
for name in ['source-manifest.json','validation.json','internal-alias-sources.json']:
 d=S/'baseline/parent'/name;d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(O/name,d)
(S/'baseline/manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
(S/'baseline/receipt.json').write_text(json.dumps(dict(passed=True,parent_commit='65ffecb844c08b0dbc5d46c53b7646635572c108',files=len(manifest),full_parent_archive=str(O/'final-source'),full_parent_source_files=6328,full_parent_manifest_sha256=sha(O/'source-manifest.json'),policy='Complete accepted parent archive stays immutable in place; build inputs and executable have a separate rollback, without copying all older generations again.'),indent=2)+'\n',encoding='utf-8')
for p in O.iterdir():
 if p.is_file() and p.suffix in ['.c','.h','.asm']:shutil.copy2(p,S/p.name)
shutil.copytree(O/'fixtures',S/'fixtures')
for p in O.glob('*fixtures.json'):
 (S/p.name).write_text(p.read_text(encoding='utf-8').replace('movement-state-v38/fixtures','movement-state-v39/fixtures'),encoding='utf-8',newline='\n')
names=['build-overlap-probe-v38.ps1','build-objects-probe-v38.ps1','build-connection-fixture-v38.ps1','make_connection_fixture_v38.py','run_connection_v38.py','run_skirmish_v38.py','audit_legal_sources_v38.py','audit_internal_alias_sources_v38.py','run_occupied_alias_probe_v38.py']
for name in names:(R/name.replace('v38','v39')).write_text((R/name).read_text(encoding='utf-8-sig').replace('v38','v39'),encoding='utf-8',newline='\n')
(S/'vcs-context.json').write_text(json.dumps(dict(parent_commit='65ffecb844c08b0dbc5d46c53b7646635572c108',config_sha256=sha(P/'.git/config'),remote_refs_sha256=hashlib.sha256(subprocess.check_output(['git','-c','core.fsmonitor=false','for-each-ref','--format=%(refname) %(objectname)','refs/remotes/'],cwd=P)).hexdigest()),indent=2)+'\n',encoding='utf-8')
print(dict(passed=True,independent_rollback_files=len(manifest),parent_archive_files=6328),flush=True)
