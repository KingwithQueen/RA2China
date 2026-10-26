"""Check the Git index against the source-only publication boundary; never edits files."""
from pathlib import Path
import json,subprocess
P=Path(__file__).resolve().parent.parent
args=['git','-c','core.fsmonitor=false','-c','core.quotepath=false']
rows=subprocess.check_output(args+['ls-files','--stage','-z'],cwd=P).split(b'\0');names=[]
for row in rows:
    if not row:continue
    meta,name=row.split(b'\t',1);mode,oid,stage=meta.split();assert mode!=b'160000' and stage==b'0','Gitlink or unresolved stage'
    names.append(name)
check=subprocess.run(args+['check-ignore','--no-index','-z','--stdin'],cwd=P,input=b'\0'.join(names)+b'\0',stdout=subprocess.PIPE,check=False)
assert check.returncode in [0,1]
bad=[x.decode('utf-8') for x in check.stdout.split(b'\0') if x]
if bad:raise SystemExit('Files outside source-only scope: '+repr(bad[:20]))
# These paths must stay private even when created under a public source directory.
private=['交接文档-测试.txt','docs/当前进度.txt','reports/latest-recovery.json','experiments/ra2-recomp-20261020/evidence/combat-state-v5/validation.json','experiments/ra2-recomp-20261020/publish_example_v73.py','experiments/ra2-recomp-20261020/ra2/src/gameplay/阅读说明-战斗.txt','experiments/ra2-recomp-20261020/ra2/src/runtime/notes.md']
r=subprocess.run(args+['check-ignore','--no-index','-z','--stdin'],cwd=P,input=b'\0'.join(s.encode() for s in private)+b'\0',stdout=subprocess.PIPE,check=False)
assert {x.decode() for x in r.stdout.split(b'\0') if x}==set(private),'Private-document exclusion regression'
public=['README.md','experiments/ra2-recomp-20261020/ra2/src/gameplay/ground_handoff.c','experiments/ra2-recomp-20261020/ra2/src/gameplay/ground_handoff.h','experiments/ra2-recomp-20261020/build-faithful.ps1']
r=subprocess.run(args+['check-ignore','--no-index','-z','--stdin'],cwd=P,input=b'\0'.join(s.encode() for s in public)+b'\0',stdout=subprocess.PIPE,check=False)
assert r.returncode==1 and not r.stdout,'Required code/build file ignored'
print(json.dumps(dict(passed=True,tracked_files=len(names),source_only=True,private_path_controls=len(private)),ensure_ascii=False))
