"""Freeze the accepted parent before changing movement rules or test inputs."""
from run_batch_v68 import *
import re
assert not S.exists()
assert git('rev-parse','HEAD').decode().strip()=='67f8f2a0cd55336e625aac5671490cc2c1be04c8'
# Only these new tools may precede the baseline; production and the index are clean.
for row in git('status','--porcelain','-z','--untracked-files=all').split(b'\0'):
    if row:assert row[:2]==b'??' and row[3:].decode().endswith(('run_batch_v68.py','prepare_closeout_v68.py')),row
assert not git('diff','--cached','--name-only')
receipt=read(R/'ra2/build-original-c/source-content-receipt.json')
assert receipt['executable_sha256']==sha(R/'ra2/build-original-c/ra2.exe')==read(O/'validation.json')['exe_sha256']
S.mkdir();(S/'runs').mkdir();(S/'fixtures').mkdir()
paths={Path(p).relative_to(R).as_posix() for p in receipt['inputs']}
paths.update(['ra2/CMakeLists.txt','ra2/build-original-c/ra2.exe','ra2/build-original-c/source-content-receipt.json','ra2/src/gameplay/阅读说明-单位移动.txt'])
entries=[]
for rel in sorted(paths):
    p=R/rel;d=S/'baseline'/rel;d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,d)
    entries.append(dict(path=rel,sha256=sha(d)))
write(S/'baseline/manifest.json',entries)
protected=[]
for e in read(R/'evidence/original-inputs-before.json'):
    p=Path('H:/开发/运行版本/原版1.006')/e['name'];assert sha(p)==e['sha256'];protected.append(dict(path=str(p),sha256=sha(p)))
for p in [R/'ra2/game/game.exe',R/'ra2/game/SAVE0029.SAV',P/'build/ra2battle.exe',P/'docs/项目目标与验收边界-20261024.txt',P/'docs/寻路机制改进验收补充-20261025.txt',R/'run_fixture_comparison.py',R/'ra2/src/runtime/state_trace.c']:
    protected.append(dict(path=str(p),sha256=sha(p)))
write(S/'protected-inputs.json',dict(passed=True,files=protected))
write(S/'vcs-context.json',dict(passed=True,parent_commit=git('rev-parse','HEAD').decode().strip(),config_sha256=sha(P/'.git/config'),remote_refs_sha256=hashlib.sha256(git('for-each-ref','--format=%(refname) %(objectname)','refs/remotes/')).hexdigest(),parent_archive=str(O/'final-source'),parent_manifest_sha256=sha(O/'source-manifest.json')))
for name in ['community-reference-review.json','community-current-use.json','alias-evidence-inheritance.json','native_probe_host.h']:
    shutil.copy2(O/name,S/name)
for name in ['traffic-rq.MAP','traffic-bm.MAP','dynamic-far-base.MAP']:
    shutil.copy2(O/'fixtures'/name,S/'fixtures'/name)
for name in ['run_bridge_catalog_v67.py','build-bridge-catalog-v67.ps1','make_bridge_catalog_v67.py','run_skirmish_v67.py']:
    p=R/name;(R/name.replace('v67','v68')).write_text(p.read_text(encoding='utf-8').replace('v67','v68').rstrip()+'\n',encoding='utf-8')
# Existing original-machine-code probes are retained byte-for-byte. Resolve current C dependencies.
exports={}
for p in (R/'ra2/src/gameplay').glob('*.c'):
    for symbol in re.findall(r'(?m)^(?!static)(?:[A-Za-z_][A-Za-z_0-9]*[ \t*]+)+(ra2_[A-Za-z_0-9]+)\s*\(',p.read_text(encoding='utf-8')):exports[symbol]=p
origins=[]
for kind,version,probe in [('prepare',66,'prepare'),('obstacle',63,'obstacle'),('arrival',62,'arrival'),('ground-services',38,'ground_services')]:
    src=R/f'evidence/movement-state-v{version}/{probe}_probe.c';shutil.copy2(src,S/src.name);origins.append(dict(path=str(src),sha256=sha(src),copy=str(S/src.name)))
    src=R/f'build-{kind}-probe-v{version}.ps1';t=src.read_text(encoding='utf-8-sig').replace(f'v{version}','v68')
    sources={R/rel.replace('..\\..\\','').replace('\\','/') for rel in re.findall(r'\.\.\\\.\.\\ra2\\src\\[A-Za-z_0-9\\]+\.c',t)}
    initial=set(sources);pending=list(sources)
    while pending:
        for sym in re.findall(r'\b(ra2_[A-Za-z_0-9]+)\s*\(',pending.pop().read_text(encoding='utf-8')):
            dependency=exports.get(sym)
            if dependency and dependency not in sources:sources.add(dependency);pending.append(dependency)
    extras=sorted('..\\..\\'+p.relative_to(R).as_posix().replace('/','\\') for p in sources-initial)
    t=t.replace(' /Fe:',(' '+' '.join(extras) if extras else '')+' /Fe:')
    (R/f'build-{kind}-probe-v68.ps1').write_text(t.rstrip()+'\n',encoding='utf-8')
write(S/'native-origins.json',dict(passed=True,files=origins))
print(dict(passed=True,baseline_files=len(entries),protected=len(protected),source_count=receipt['source_count']))
