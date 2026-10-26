"""Freeze the accepted shared-death batch before derived lifecycle work."""
from combat_batch_v72 import *
assert not S.exists();assert git('rev-parse','HEAD').decode().strip()=='8767b55e64667f8b0304be5e932865e2da5c9098'
assert not git('diff','--cached','--name-only')
for row in git('status','--porcelain','-z','--untracked-files=all').split(b'\0'):
    if row:
        name=row[3:].decode();assert row[:2]==b'??' and name.endswith(('combat_batch_v72.py','prepare_combat_v72.py')),row
receipt=read(R/'ra2/build-original-c/source-content-receipt.json');assert receipt['source_count']==188 and len(receipt['inputs'])==325
assert sha(R/'ra2/build-original-c/ra2.exe')==read(O/'validation.json')['exe_sha256']==receipt['executable_sha256']
S.mkdir();(S/'runs').mkdir();(S/'fixtures').mkdir();entries=[]
paths={Path(p).relative_to(R).as_posix() for p in receipt['inputs']};paths|={'ra2/CMakeLists.txt','ra2/build-original-c/ra2.exe','ra2/build-original-c/source-content-receipt.json','ra2/src/gameplay/阅读说明-战斗.txt'}
for rel in sorted(paths):
    p=S/'baseline'/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/rel,p);entries.append(dict(path=rel,sha256=sha(p)))
write(S/'baseline/manifest.json',entries)
protected=read(O/'protected-inputs.json')['files']
for x in protected:assert sha(Path(x['path']))==x['sha256']
write(S/'protected-inputs.json',dict(passed=True,files=protected))
write(S/'vcs-context.json',dict(passed=True,parent_commit=git('rev-parse','HEAD').decode().strip(),parent_manifest_sha256=sha(O/'source-manifest.json'),parent_archive=str(O/'final-source'),config_sha256=sha(P/'.git/config'),remote_refs_sha256=hashlib.sha256(git('for-each-ref','--format=%(refname) %(objectname)','refs/remotes/')).hexdigest()))
shutil.copy2(O/'native_probe_host.h',S/'native_probe_host.h')
for n in ['README.md','交接文档-原版逆向与C重编译-20261020.txt','交接文档-新对话继续推进-20261022.txt','reports/latest-recovery.json','reports/latest-state-comparison.json','reports/latest-movement-candidate.json']:
    p=S/'baseline-project'/n;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(P/n,p)
print(dict(passed=True,baseline_files=len(entries),protected=len(protected)))
