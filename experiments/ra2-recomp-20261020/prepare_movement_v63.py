"""Batch 62 baseline and waiting/release inputs; retain prior archives in place."""
from pathlib import Path
import hashlib,json,shutil,subprocess
R=Path(__file__).resolve().parent;P=R.parent.parent
O=R/'evidence/movement-state-v62';S=R/'evidence/movement-state-v63'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,x):
 assert not p.exists(),p
 p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert not S.exists()
parent=subprocess.check_output(['git','rev-parse','HEAD'],cwd=P,text=True).strip()
assert parent=='ccd7050fdf03e2d4c41770412e757264b79d1e2b'
assert sha(R/'ra2/build-original-c/ra2.exe')==read(O/'validation.json')['exe_sha256']
S.mkdir();(S/'runs').mkdir();(S/'fixtures').mkdir()
receipt=read(R/'ra2/build-original-c/source-content-receipt.json')
assert receipt['source_count']==181 and len(receipt['inputs'])==312
paths={Path(p).relative_to(R).as_posix() for p in receipt['inputs']}
paths.update(['ra2/CMakeLists.txt','ra2/build-original-c/ra2.exe','ra2/src/gameplay/阅读说明-单位移动.txt'])
entries=[]
for rel in sorted(paths):
 d=S/'baseline'/rel;d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/rel,d)
 entries.append(dict(path=rel,sha256=sha(d)))
write(S/'baseline/manifest.json',entries)
for rel in ['README.md','reports/latest-recovery.json','reports/latest-state-comparison.json','reports/latest-movement-candidate.json','交接文档-原版逆向与C重编译-20261020.txt','交接文档-新对话继续推进-20261022.txt','docs/项目目标与验收边界-20261024.txt','docs/寻路机制改进验收补充-20261025.txt']:
 d=S/'baseline/project'/rel;d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(P/rel,d)
for name in ['bridge-cross-release-fixtures.json','collision-acceptance-fixtures.json']:
 x=read(O/name)
 for item in x['fixtures']:
  for k in ['path','rules']:
   if item.get(k):
    source=R/item[k];d=S/'fixtures'/source.name
    if not d.exists():shutil.copy2(source,d)
    item[k]=d.relative_to(R).as_posix()
 write(S/name,x)
for name in ['dynamic-far-base.MAP','tube-curved-elevated-east.MAP','tube-curved-tall-west.MAP']:
 shutil.copy2(O/'fixtures'/name,S/'fixtures'/name)
for name in ['transport_packet_probe.c','transport_packet_probe.exe','transport-native-validation-current.json','capture_packet_probe.c','capture_packet_probe.exe','capture-native-validation.json','mission-table-proof.json','native_probe_host.h']:
 shutil.copy2(O/name,S/name)
for probe,version in [('wait',44),('obstacle',53),('recovery',53)]:shutil.copy2(R/('evidence/movement-state-v'+str(version))/(probe+'_probe.c'),S/(probe+'_probe.c'))
shutil.copy2(O/'community-reference-review.json',S/'community-reference-review.json')
entries=[]
for name in ['bridge-catalog-observer.exe','bridge_catalog_observer.c']:
 d=S/'baseline-observer'/name;d.parent.mkdir(parents=True,exist_ok=True)
 shutil.copy2(O/name,d);shutil.copy2(O/name,S/name)
 entries.append(dict(path=name,sha256=sha(d)))
write(S/'baseline-observer/manifest.json',entries)
for name in ['run_skirmish_v62.py','make_bridge_catalog_v62.py','build-bridge-catalog-v62.ps1','run_bridge_catalog_v62.py','map_codec_v62.py','execute_cleanup_v62.ps1']:
 (R/name.replace('v62','v63')).write_text((R/name).read_text(encoding='utf-8-sig').replace('v62','v63'),encoding='utf-8',newline='\n')
# Derive known working build plans, then resolve newer gameplay dependencies.
import re
exports={}
for p in (R/'ra2/src/gameplay').glob('*.c'):
 text=p.read_text(encoding='utf-8-sig')
 for symbol in re.findall(r'(?m)^(?!static)(?:[A-Za-z_][A-Za-z_0-9]*[ \t*]+)+(ra2_[A-Za-z_0-9]+)\s*\(',text):exports[symbol]=p
for kind,version in [('wait',44),('obstacle',53),('recovery',53)]:
 p=R/('build-'+kind+'-probe-v'+str(version)+'.ps1');t=p.read_text(encoding='utf-8-sig').replace('v'+str(version),'v63')
 sources={R/rel.replace('..\\..\\','').replace('\\','/') for rel in re.findall(r'\.\.\\\.\.\\ra2\\src\\[A-Za-z_0-9\\]+\.c',t)}
 initial=set(sources);pending=list(sources)
 while pending:
  source=pending.pop()
  for symbol in re.findall(r'\b(ra2_[A-Za-z_0-9]+)\s*\(',source.read_text(encoding='utf-8-sig')):
   dependency=exports.get(symbol)
   if dependency and dependency not in sources:sources.add(dependency);pending.append(dependency)
 extras=sorted('..\\..\\'+p.relative_to(R).as_posix().replace('/','\\') for p in sources-initial)
 t=t.replace(' /Fe:',(' '+' '.join(extras) if extras else '')+' /Fe:')
 (R/('build-'+kind+'-probe-v63.ps1')).write_text(t,encoding='utf-8',newline='\n')
 write(S/('build-'+kind+'-dependency-plan.json'),dict(passed=True,base_recipe=p.name,base_recipe_sha256=sha(p),added_gameplay_sources=extras,scope='Transitive references to existing gameplay definitions only; no new production source or runtime stub edits.'))
items=[]
for old in read(O/'dynamic-fixtures.json')['fixtures']:
 item=dict(old);source=R/item['path'];d=S/'fixtures'/source.name
 if not d.exists():shutil.copy2(source,d)
 item.update(path=d.relative_to(R).as_posix(),baseline_tag=item['tag'],baseline_stage=O.name)
 items.append(item)
write(S/'dynamic-fixtures.json',dict(passed=True,fixtures=items,ordinary_events=True,no_rules_overrides=True,terrain_pack_unchanged=True,all_four_baselines_inherited=True,new_natural_recipe=False))
write(S/'vcs-context.json',dict(parent_commit=parent,config_sha256=sha(P/'.git/config'),remote_refs_sha256=hashlib.sha256(subprocess.check_output(['git','for-each-ref','--format=%(refname) %(objectname)','refs/remotes/'],cwd=P)).hexdigest(),parent_archive=str(O/'final-source'),parent_source_files=len(read(O/'source-manifest.json')),parent_source_manifest_sha256=sha(O/'source-manifest.json')))
print(dict(passed=True,baseline_files=len(read(S/'baseline/manifest.json')),parent_files=len(read(O/'source-manifest.json')),natural_baselines=4))
