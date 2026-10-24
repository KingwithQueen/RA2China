"""Generation47 independent baseline and bounded current inputs; parent archive stays in place."""
from pathlib import Path
import hashlib,json,shutil,subprocess
R=Path(__file__).resolve().parent;P=R.parent.parent;O=R/'evidence/movement-state-v47';S=R/'evidence/movement-state-v48'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
assert not S.exists()
assert subprocess.check_output(['git','-c','core.fsmonitor=false','rev-parse','HEAD'],cwd=P,text=True).strip()=='824796f8bbac6b8d48d74375bb545afae8b7e387'
assert set(subprocess.check_output(['git','-c','core.fsmonitor=false','status','--porcelain'],cwd=P).splitlines())=={b'?? experiments/ra2-recomp-20261020/prepare_movement_v48.py'}
assert sha(R/'ra2/build-original-c/ra2.exe')==read(O/'validation.json')['exe_sha256']
S.mkdir();(S/'runs').mkdir();(S/'fixtures').mkdir();r=read(R/'ra2/build-original-c/source-content-receipt.json');assert len(r['inputs'])==306 and r['source_count']==178
paths={Path(p).relative_to(R).as_posix() for p in r['inputs']};paths.update(['ra2/CMakeLists.txt','ra2/build-original-c/ra2.exe','ra2/src/gameplay/阅读说明-单位移动.txt']);manifest=[]
for rel in sorted(paths):
 d=S/'baseline'/rel;d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/rel,d);manifest.append(dict(path=rel,sha256=sha(d)))
(S/'baseline/manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
for rel in ['README.md','reports/latest-recovery.json','reports/latest-state-comparison.json','reports/latest-movement-candidate.json','交接文档-原版逆向与C重编译-20261020.txt','交接文档-新对话继续推进-20261022.txt','docs/项目目标与验收边界-20261024.txt']:
 d=S/'baseline/project'/rel;d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(P/rel,d)
for name in ['source-manifest.json','document-manifest.json','validation.json','alias-evidence-inheritance.json']:
 d=S/'baseline/parent'/name;d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(O/name,d)
files=set(['dynamic-far-base.MAP','tube-curved-elevated-east.MAP','tube-curved-tall-west.MAP'])
for name in ['bridge-cross-release-fixtures.json','collision-acceptance-fixtures.json','representative-acceptance-fixtures.json']:
 x=read(O/name)
 for a in x['fixtures']:
  for k in ['path','rules']:
   if a.get(k):files.add(Path(a[k]).name);a[k]=(S/'fixtures'/Path(a[k]).name).relative_to(R).as_posix()
 (S/name).write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8')
for name in sorted(files):shutil.copy2(O/'fixtures'/name,S/'fixtures'/name)
for name in ['native_probe_host.h','capture_packet_probe.c','capture_packet_probe.exe','capture-native-validation.json']:shutil.copy2(O/name,S/name)
for name in ['completion_services_probe.c','progress_probe.c']:shutil.copy2(R/'evidence/movement-state-v38'/name,S/name)
for name in ['run_skirmish_v47.py','make_bridge_catalog_v47.py','build-bridge-catalog-v47.ps1','run_bridge_catalog_v47.py']:
 (R/name.replace('v47','v48')).write_text((R/name).read_text(encoding='utf-8-sig').replace('v47','v48'),encoding='utf-8',newline='\n')
for name in ['bridge-repair.MAP','bridge-detour.MAP']:shutil.copy2(O/'fixtures'/name,S/'fixtures'/name)
(S/'vcs-context.json').write_text(json.dumps(dict(parent_commit='824796f8bbac6b8d48d74375bb545afae8b7e387',config_sha256=sha(P/'.git/config'),remote_refs_sha256=hashlib.sha256(subprocess.check_output(['git','-c','core.fsmonitor=false','for-each-ref','--format=%(refname) %(objectname)','refs/remotes/'],cwd=P)).hexdigest(),parent_archive=str(O/'final-source'),parent_source_files=380,parent_source_manifest_sha256=sha(O/'source-manifest.json')),indent=2)+'\n',encoding='utf-8')
print(dict(passed=True,baseline_files=len(manifest),parent_files=380,fixture_files=len(files)))
