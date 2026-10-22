"""Check that staged source blobs preserve accepted bytes (including line endings)."""
from pathlib import Path
import hashlib,json,subprocess
P=Path(__file__).resolve().parent.parent;R=P/'experiments/ra2-recomp-20261020'
latest=json.loads((P/'reports/latest-recovery.json').read_text(encoding='utf-8-sig'))
S=Path(latest['validation']).parent
manifest=json.loads((S/'source-manifest.json').read_text(encoding='utf-8-sig'))
build=json.loads((R/'ra2/build-original-c/source-content-receipt.json').read_text(encoding='utf-8-sig'))
compiled={Path(name).relative_to(P).as_posix() for name in build['inputs']}
records=subprocess.check_output(['git','ls-files','--stage','-z'],cwd=P).split(b'\0')
index={}
for row in records:
 if not row:continue
 meta,name=row.split(b'\t',1);mode,oid,stage=meta.split()
 assert mode!=b'160000' and stage==b'0','Unexpected gitlink or unresolved index stage'
 index[name.decode('utf-8')]=oid.decode('ascii')
checked=0;local=[]
for entry in manifest:
 path=R/entry['path'];name=path.relative_to(P).as_posix();data=path.read_bytes()
 assert hashlib.sha256(data).hexdigest()==entry['sha256'],name
 if name not in index:
  # Historical scratch copies, diagnostics and the full build receipt stay local.
  assert name not in compiled,('Compiled input missing from index',name)
  local.append(name);continue
 blob=hashlib.sha1(b'blob '+str(len(data)).encode('ascii')+b'\0'+data).hexdigest()
 assert blob==index[name],('Staged bytes differ from accepted working file',name)
 checked+=1
for name,digest in build['inputs'].items():
 path=Path(name);rel=path.relative_to(P).as_posix();data=path.read_bytes()
 assert rel in index and hashlib.sha256(data).hexdigest()==digest,rel
 assert hashlib.sha1(b'blob '+str(len(data)).encode('ascii')+b'\0'+data).hexdigest()==index[rel],rel
receipt=dict(passed=True,source_manifest=str(S/'source-manifest.json'),checked_staged_files=checked,
 compiled_inputs_checked=len(compiled),retained_local_files=local,all_staged_source_bytes_match=True,gitlinks=0)
(S/'git-byte-audit.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(passed=True,checked_staged_files=checked,compiled_inputs=len(compiled),local_files=len(local))))
