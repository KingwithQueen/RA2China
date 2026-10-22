"""Preserve original LF bytes, proving the two recompiled COFFs differ only in creation time.
The executable is never modified; compilation uses the same object path, then restores
the production object bytes and times. Roll back source bytes if proof fails.
"""
from pathlib import Path
import argparse,hashlib,json,os,shlex,shutil
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v18';D=S/'investigations/line-ending-build'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
ap=argparse.ArgumentParser();ap.add_argument('phase',choices=['prepare','finish']);a=ap.parse_args()
receipt=R/'ra2/build-original-c/source-content-receipt.json'
if a.phase=='prepare':
 assert not D.exists();D.mkdir(parents=True)
 shutil.copy2(receipt,D/'receipt-before.json');jobs=[]
 entries=read(R/'ra2/build-original-c/compile_commands.json')
 for name in ['recomp_0010.c','recomp_0022.c']:
  p=R/'ra2/src/recomp/gen_game'/name;prior=p.stat();shutil.copy2(p,D/name)
  raw=p.read_bytes();normalized=raw.replace(b'\r\n',b'\n');assert b'\r' not in normalized
  assert b'\r' not in (S/'baseline/ra2/src/recomp/gen_game'/name).read_bytes()
  p.write_bytes(normalized);os.utime(p,ns=(prior.st_atime_ns,prior.st_mtime_ns))
  entry=next(e for e in entries if e['file'].endswith(name))
  args=[s.strip('"') for s in shlex.split(entry['command'],posix=False)][1:]
  output=D/(name+'.obj');original=R/'ra2/build-original-c/CMakeFiles/ra2.dir/src/recomp/gen_game'/(name+'.obj')
  object_backup=D/('original-'+original.name);shutil.copy2(original,object_backup)
  repaired=[]
  for arg in args:
   if arg.startswith('-I') and '\\ra2\\' in arg:arg='-I'+str(R/'ra2'/arg.split('\\ra2\\',1)[1])
   elif arg.replace('\\','/').endswith('/src/recomp/gen_game/'+name):arg=str(p)
   repaired.append(arg)
  jobs.append(dict(source=str(p),backup=str(D/name),original_object=str(original),object_backup=str(object_backup),original_object_sha256=sha(original),output=str(output),args=repaired,
   before_sha256=sha(D/name),after_sha256=sha(p),mtime_ns=prior.st_mtime_ns,atime_ns=prior.st_atime_ns))
 (D/'jobs.json').write_text(json.dumps(jobs,ensure_ascii=False,indent=2),encoding='utf-8')
else:
 jobs=read(D/'jobs.json');results=[]
 try:
  for j in jobs:
   p=Path(j['source']);old=Path(j['original_object']);new=Path(j['output'])
   assert sha(old)==j['original_object_sha256'] and sha(p)==j['after_sha256']
   b=old.read_bytes();n=new.read_bytes();assert b[:2]==n[:2]==b'\x4c\x01'
   assert len(b)==len(n) and b[:4]+b[8:]==n[:4]+n[8:],p.name
   assert p.read_bytes()==Path(j['backup']).read_bytes().replace(b'\r\n',b'\n')
   results.append(dict(source=str(p),before_sha256=j['before_sha256'],after_sha256=j['after_sha256'],
    original_object_sha256=sha(old),compiled_object_sha256=sha(new),object_bytes_equal_except_coff_creation_timestamp=True))
  before=read(D/'receipt-before.json');now=read(receipt);assert now==before
  assert sha(R/'ra2/build-original-c/ra2.exe')==before['executable_sha256']
  for j in jobs:
   assert j['source'] in now['inputs'];now['inputs'][j['source']]=j['after_sha256']
  receipt.write_text(json.dumps(now,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
  repair=read(S/'prepare-label-repair.json');repair['repaired_source_before_newline_preservation_sha256']=repair['repaired_source_sha256']
  repair['repaired_source_sha256']=sha(R/'ra2/src/recomp/gen_game/recomp_0010.c')
  (S/'prepare-label-repair.json').write_text(json.dumps(repair,indent=2)+'\n',encoding='utf-8')
  (S/'newline-object-equivalence.json').write_text(json.dumps(dict(passed=True,production_executable_unchanged=True,
   production_objects_unchanged=True,exe_sha256=before['executable_sha256'],results=results),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
  print('Original LF restored; both independently compiled objects match apart from COFF creation timestamps; executable unchanged.')
 except BaseException:
  for j in jobs:shutil.copy2(j['backup'],j['source'])
  raise
