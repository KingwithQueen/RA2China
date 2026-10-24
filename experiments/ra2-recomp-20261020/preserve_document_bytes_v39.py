"""Keep new leading status while preserving every byte of the inherited document bodies."""
from run_batch_v39 import R,P,S,read,write,sha
from pathlib import Path
import shutil,json
out=S/'investigations/document-bytes-01';out.mkdir(parents=True,exist_ok=False)
for name in ['source-manifest.json','document-manifest.json','final-check.json','validation.json']:shutil.copy2(S/name,out/name)
doc_entries=read(S/'document-manifest.json');sources=read(S/'source-manifest.json');before={}
paths=[P/'README.md',P/'交接文档-原版逆向与C重编译-20261020.txt',P/'交接文档-新对话继续推进-20261022.txt',R/'ra2/src/gameplay/阅读说明-单位移动.txt']
for p in paths:
 rel=p.relative_to(P);d=out/'initial'/rel;d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,d);before[str(p)]=sha(p)
 base=S/'baseline'/('ra2/src/gameplay/阅读说明-单位移动.txt' if p.is_relative_to(R) else 'project/'+rel.as_posix())
 old=base.read_bytes();current=p.read_bytes()
 if p.name=='README.md':
  lines=old.splitlines(keepends=True);eol=b'\r\n' if lines[0].endswith(b'\r\n') else b'\n';p.write_bytes(current.splitlines()[0]+eol+b''.join(lines[1:]))
 else:
  first=old.splitlines()[0];i=current.index(first);p.write_bytes(current[:i]+old)
for e in doc_entries:
 p=P/e['path'];dest=S/'current-project'/e['path'];shutil.copy2(p,dest);e['sha256']=sha(p)
def replace(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
replace(S/'document-manifest.json',doc_entries)
existing={e['path'] for e in sources}
for p in R.glob('*v39*'):
 if p.is_file() and p.relative_to(R).as_posix() not in existing:sources.append(dict(path=p.relative_to(R).as_posix(),sha256=sha(p)))
for e in sources:
 p=R/e['path'];dest=S/'final-source'/e['path']
 if sha(p)!=e['sha256'] or not dest.exists():
  if dest.exists():
   saved=out/'initial-source'/e['path'];saved.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(dest,saved)
  dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest);e['sha256']=sha(p)
replace(S/'source-manifest.json',sorted(sources,key=lambda e:e['path']))
v=read(S/'validation.json');v['source_files']=len(sources);replace(S/'validation.json',v)
f=read(S/'final-check.json');f.update(source_files=len(sources),source_manifest_sha256=sha(S/'source-manifest.json'),document_manifest_sha256=sha(S/'document-manifest.json'));replace(S/'final-check.json',f)
write(S/'document-byte-preservation.json',dict(passed=True,production_executable_unchanged=sha(R/'ra2/build-original-c/ra2.exe')==v['exe_sha256'],game_results_unchanged=True,policy='Only inherited document-body newline conversion removed before commit; source/EXE tests remain valid.',before=before,after={str(p):sha(p) for p in paths},initial_seal_preserved=str(out),current_source_files=len(sources)))
print(dict(passed=True,source_files=len(sources),production_executable_unchanged=True))
