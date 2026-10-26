"""Exact ignored-file allowlist; preserve original inputs, accepted source and evidence."""
from combat_batch_v71 import *
import stat
def ordinary(p):
    q=p.resolve();assert q.is_relative_to(R.resolve()),p
    for a in [p,*p.parents]:
        if a==R.parent:break
        assert not a.lstat().st_file_attributes&0x400,a
def plan():
    assert read(S/'evidence-rollup.json')['passed'];candidates=[];dirs=[]
    tracked={x.decode('utf-8') for x in git('ls-files','-z').split(b'\0') if x}
    def add(p,kind):
        ordinary(p);rel=p.relative_to(P).as_posix();assert rel not in tracked
        assert subprocess.run(['git','check-ignore','--quiet','--',rel],cwd=P).returncode==0,rel
        candidates.append(dict(path=str(p.resolve()),sha256=sha(p),bytes=p.stat().st_size,kind=kind))
    for p in S.glob('*.obj'):add(p,'native-observer-intermediate')
    for d in [R/'__pycache__',R/'ra2/tools/__pycache__']:
        if not d.exists():continue
        ordinary(d)
        for p in d.glob('*.pyc'):
            if (d.parent/(p.name.split('.cpython-')[0]+'.py')).exists():add(p,'reproducible-python-cache')
        if all(str(p.resolve()) in {v['path'] for v in candidates} for p in d.iterdir()):dirs.append(str(d.resolve()))
    excluded={x['path'] for x in candidates};paths={Path(p) for p in read(R/'ra2/build-original-c/source-content-receipt.json')['inputs']}
    paths.update(Path(e['path']) for e in read(S/'protected-inputs.json')['files'])
    paths.update(p for p in S.iterdir() if p.is_file() and str(p.resolve()) not in excluded)
    protected=[dict(path=str(p),sha256=sha(p)) for p in sorted(paths)]
    write(S/'cleanup-plan.json',dict(passed=True,workspace=str(R.resolve()),authorized_by_current_user=True,candidates=candidates,protected=protected,empty_cache_directories=dirs,files=len(candidates),bytes=sum(x['bytes'] for x in candidates),scope='Only ignored root probe/observer .obj and reproducible Python cache; no originals, accepted executables, baseline, rollback, anomalous inputs, source or traces.'))
    print(dict(files=len(candidates),bytes=sum(x['bytes'] for x in candidates)))
def execute():
    p=S/'cleanup-plan.json';d=read(p);assert d['workspace']==str(R.resolve())
    for x in d['protected']:assert sha(Path(x['path']))==x['sha256'],x['path']
    for x in d['candidates']:
        f=Path(x['path']);ordinary(f);assert f.is_file() and sha(f)==x['sha256'] and f.stat().st_size==x['bytes']
        assert f.suffix in ['.obj','.pyc']
    # Literal file removal only; no recursive deletion, no shell-built paths.
    for x in d['candidates']:Path(x['path']).unlink()
    for name in d['empty_cache_directories']:
        f=Path(name);ordinary(f);assert not list(f.iterdir());f.rmdir()
    for x in d['protected']:assert sha(Path(x['path']))==x['sha256'],x['path']
    assert all(not Path(x['path']).exists() for x in d['candidates'])
    write(S/'cleanup.json',dict(passed=True,deleted_files=d['files'],deleted_bytes=d['bytes'],protected_files=len(d['protected']),protected_unchanged=True,plan_sha256=sha(p),recursive_deletion=False))
    print(dict(passed=True,deleted_files=d['files'],protected=len(d['protected'])))
if __name__=='__main__':
    if sys.argv[1]=='plan':plan()
    elif sys.argv[1]=='execute':execute()
    else:raise ValueError(sys.argv[1])
