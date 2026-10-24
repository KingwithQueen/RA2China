"""Generation40: independent baseline, finite collision fixtures and current recipes."""
from pathlib import Path
import hashlib,json,shutil,subprocess,re
R=Path(__file__).resolve().parent;P=R.parent.parent;O=R/'evidence/movement-state-v40';S=R/'evidence/movement-state-v41'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
assert not S.exists()
assert subprocess.check_output(['git','-c','core.fsmonitor=false','rev-parse','HEAD'],cwd=P,text=True).strip()=='77e5905145e8a34a4eed21e486950a91fb0e3442'
assert set(subprocess.check_output(['git','-c','core.fsmonitor=false','status','--porcelain'],cwd=P).splitlines())=={b'?? experiments/ra2-recomp-20261020/prepare_movement_v41.py',b'?? experiments/ra2-recomp-20261020/make_collision_scenes_v41.py'}
assert sha(R/'ra2/build-original-c/ra2.exe')==read(O/'validation.json')['exe_sha256']
S.mkdir();(S/'runs').mkdir();(S/'pending').mkdir();receipt=read(R/'ra2/build-original-c/source-content-receipt.json');assert len(receipt['inputs'])==294
paths={Path(p).relative_to(R).as_posix() for p in receipt['inputs']};paths.update(['ra2/CMakeLists.txt','ra2/build-original-c/ra2.exe','ra2/src/gameplay/阅读说明-单位移动.txt'])
manifest=[]
for rel in sorted(paths):
 d=S/'baseline'/rel;d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/rel,d);manifest.append(dict(path=rel,sha256=sha(d)))
(S/'baseline/manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
for rel in ['README.md','reports/latest-recovery.json','reports/latest-state-comparison.json','reports/latest-movement-candidate.json','交接文档-原版逆向与C重编译-20261020.txt','交接文档-新对话继续推进-20261022.txt','docs/项目目标与验收边界-20261024.txt']:
 d=S/'baseline/project'/rel;d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(P/rel,d)
for name in ['source-manifest.json','document-manifest.json','validation.json','alias-evidence-inheritance.json']:
 d=S/'baseline/parent'/name;d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(O/name,d)
for name in ['advance_probe.c','overlap_probe.c','native_probe_host.h','remaining_return_cases.h','connection_observer.c']:shutil.copy2(O/name,S/name)
for name in ['prepare_probe.c','continuation_probe.c','segment_probe.c']:shutil.copy2(R/'evidence/movement-state-v39'/name,S/name)
shutil.copytree(O/'fixtures',S/'fixtures')
for p in O.glob('*fixtures.json'):(S/p.name).write_text(p.read_text(encoding='utf-8').replace('movement-state-v40/fixtures','movement-state-v41/fixtures'),encoding='utf-8',newline='\n')
for name in ['run_skirmish_v40.py','run_connection_v40.py','make_connection_fixture_v40.py','build-connection-fixture-v40.ps1','build-advance-probe-v40.ps1']:
 (R/name.replace('v40','v41')).write_text((R/name).read_text(encoding='utf-8-sig').replace('v40','v41'),encoding='utf-8',newline='\n')
for name in ['build-continuation-probe-v38.ps1','build-segment-probe-v38.ps1']:
 (R/name.replace('v38','v41')).write_text((R/name).read_text(encoding='utf-8-sig').replace('v38','v41'),encoding='utf-8',newline='\n')
(S/'vcs-context.json').write_text(json.dumps(dict(parent_commit='77e5905145e8a34a4eed21e486950a91fb0e3442',config_sha256=sha(P/'.git/config'),remote_refs_sha256=hashlib.sha256(subprocess.check_output(['git','-c','core.fsmonitor=false','for-each-ref','--format=%(refname) %(objectname)','refs/remotes/'],cwd=P)).hexdigest(),parent_archive=str(O/'final-source'),parent_source_files=353,parent_source_manifest_sha256=sha(O/'source-manifest.json')),indent=2)+'\n',encoding='utf-8')
print(dict(passed=True,baseline_files=len(manifest),parent_files=353))
