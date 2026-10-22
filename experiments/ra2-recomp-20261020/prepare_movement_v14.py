"""Protect generation 12 before expanding the readable search loop."""
from pathlib import Path
import hashlib,json,shutil,subprocess
R=Path(__file__).resolve().parent;P=R.parent.parent;O=R/'evidence/movement-state-v13';S=R/'evidence/movement-state-v14'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((O/'source-manifest.json').read_text(encoding='utf-8'));assert len(m)==1002 and not S.exists()
for e in m:assert sha(R/e['path'])==sha(O/'final-source'/e['path'])==e['sha256'],e['path']
assert sha(R/'ra2/build-original-c/ra2.exe')=='e1d8e97c5706794f8de58d37ad726a1855ccf075947c403c9aeb7204b35dbff5'
for e in m:
    dest=S/'baseline'/e['path'];dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/e['path'],dest)
shutil.copy2(O/'source-manifest.json',S/'baseline/source-manifest.json')
for rel in ['reports/latest-recovery.json','reports/latest-state-comparison.json','reports/latest-movement-candidate.json','交接文档-原版逆向与C重编译-20261020.txt','交接文档-单位移动第十二批正式验收-20261022.txt','docs/单位移动第十二批-寻路堆与节点缓存-20261022.txt']:
    dest=S/'baseline/project'/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(P/rel,dest)
state={repo:subprocess.run(['git','-C',str(R/repo),'status','--porcelain'],capture_output=True,text=True,encoding='utf-8').stdout for repo in ['ra2','pcrecomp']}
(S/'baseline/receipt.json').write_text(json.dumps(dict(passed=True,files=len(m),formal_exe_sha256=sha(R/'ra2/build-original-c/ra2.exe'),git_status=state),ensure_ascii=False,indent=2),encoding='utf-8')
print('Protected',len(m),'files')
