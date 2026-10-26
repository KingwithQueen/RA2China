"""Verify staged compiled source bytes using the build receipt, without local handoff files."""
from pathlib import Path
import hashlib,json,subprocess
P=Path(__file__).resolve().parent.parent;R=P/'experiments/ra2-recomp-20261020'
git=lambda *a:subprocess.check_output(['git','-c','core.fsmonitor=false',*a],cwd=P)
build=json.loads((R/'ra2/build-original-c/source-content-receipt.json').read_text(encoding='utf-8-sig'))
assert hashlib.sha256((R/'ra2/build-original-c/ra2.exe').read_bytes()).hexdigest()==build['executable_sha256']
index={}
for row in git('ls-files','--stage','-z').split(b'\0'):
    if not row:continue
    meta,name=row.split(b'\t',1);mode,oid,stage=meta.split();assert mode!=b'160000' and stage==b'0'
    index[name.decode('utf-8')]=oid.decode('ascii')
algorithm=git('rev-parse','--show-object-format').decode().strip();assert algorithm in ['sha1','sha256']
for name,digest in build['inputs'].items():
    p=Path(name);assert p.resolve().is_relative_to(R.resolve());rel=p.relative_to(P).as_posix();data=p.read_bytes()
    assert rel in index and hashlib.sha256(data).hexdigest()==digest,rel
    assert hashlib.new(algorithm,b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==index[rel],('Index differs from compiled source',rel)
print(json.dumps(dict(passed=True,compiled_inputs=len(build['inputs']),source_count=build['source_count'],all_index_bytes_match=True,requires_handoff_or_evidence=False)))
