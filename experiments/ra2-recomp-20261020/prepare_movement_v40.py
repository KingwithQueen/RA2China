"""Prepare bounded generation39 rollback and only the recipes used this round."""
from pathlib import Path
import hashlib,json,shutil,subprocess
R=Path(__file__).resolve().parent;P=R.parent.parent;O=R/'evidence/movement-state-v39';S=R/'evidence/movement-state-v40'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
assert not S.exists()
assert subprocess.check_output(['git','-c','core.fsmonitor=false','rev-parse','HEAD'],cwd=P,text=True).strip()=='4c674913e268521e323b3329f38677388b6595ab'
assert subprocess.check_output(['git','-c','core.fsmonitor=false','status','--porcelain'],cwd=P)==b'?? experiments/ra2-recomp-20261020/prepare_movement_v40.py\n'
assert sha(R/'ra2/build-original-c/ra2.exe')==read(O/'validation.json')['exe_sha256']
S.mkdir();(S/'runs').mkdir();(S/'pending').mkdir()
receipt=read(R/'ra2/build-original-c/source-content-receipt.json');assert len(receipt['inputs'])==292
paths={Path(p).relative_to(R).as_posix() for p in receipt['inputs']}
paths.update(['ra2/CMakeLists.txt','ra2/build-original-c/ra2.exe','ra2/src/gameplay/阅读说明-单位移动.txt'])
manifest=[]
for rel in sorted(paths):
 dest=S/'baseline'/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/rel,dest);manifest.append(dict(path=rel,sha256=sha(dest)))
(S/'baseline/manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
for rel in ['README.md','reports/latest-recovery.json','reports/latest-state-comparison.json','reports/latest-movement-candidate.json','交接文档-原版逆向与C重编译-20261020.txt','交接文档-新对话继续推进-20261022.txt','docs/项目目标与验收边界-20261024.txt']:
 dest=S/'baseline/project'/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(P/rel,dest)
for name in ['source-manifest.json','document-manifest.json','validation.json','internal-alias-sources.json']:
 dest=S/'baseline/parent'/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(O/name,dest)
for name in ['advance_probe.c','overlap_probe.c','native_probe_host.h','remaining_return_cases.h','connection_observer.c']:shutil.copy2(O/name,S/name)
for name in ['bridge-cross-release-fixtures.json','bridge-infantry-fixtures.json','bridge-hostile-fixtures.json']:
 value=read(O/name)
 if name=='bridge-infantry-fixtures.json':value['fixtures']=[x for x in value['fixtures'] if x['meeting']]
 if name=='bridge-hostile-fixtures.json':value['fixtures']=[x for x in value['fixtures'] if x['name']=='enemy-traffic-ai3-north']
 for x in value['fixtures']:
  old=R/x['path'];new=S/'fixtures'/old.name;new.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(old,new);x['path']=new.relative_to(R).as_posix();x['sha256']=sha(new)
 (S/name).write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
for name in ['tube-curved-elevated-east.MAP','tube-curved-tall-west.MAP','tube-east.MAP','dynamic-far-base.MAP']:shutil.copy2(O/'fixtures'/name,S/'fixtures'/name)
for name in ['run_skirmish_v39.py','run_connection_v39.py','make_connection_fixture_v39.py','build-connection-fixture-v39.ps1','build-overlap-probe-v39.ps1']:
 (R/name.replace('v39','v40')).write_text((R/name).read_text(encoding='utf-8-sig').replace('v39','v40'),encoding='utf-8',newline='\n')
(R/'build-advance-probe-v40.ps1').write_text((R/'build-advance-probe-v38.ps1').read_text(encoding='utf-8-sig').replace('v38','v40'),encoding='utf-8',newline='\n')
(S/'vcs-context.json').write_text(json.dumps(dict(parent_commit='4c674913e268521e323b3329f38677388b6595ab',config_sha256=sha(P/'.git/config'),remote_refs_sha256=hashlib.sha256(subprocess.check_output(['git','-c','core.fsmonitor=false','for-each-ref','--format=%(refname) %(objectname)','refs/remotes/'],cwd=P)).hexdigest(),parent_archive=str(O/'final-source'),parent_source_files=475,parent_source_manifest_sha256=sha(O/'source-manifest.json')),indent=2)+'\n',encoding='utf-8')
print(dict(passed=True,rollback_files=len(manifest),parent_archive_files=475))
