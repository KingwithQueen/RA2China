"""保全第十批修正版正式基线，后续只写第十二轮证据。"""
from pathlib import Path
import json,hashlib,shutil
R=Path(__file__).resolve().parent;P=R.parent.parent;O=R/'evidence/movement-state-v11';S=R/'evidence/movement-state-v12'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((O/'source-manifest.json').read_text(encoding='utf-8'));assert len(m)==727;assert not S.exists()
for e in m:assert sha(R/e['path'])==sha(O/'final-source'/e['path'])==e['sha256'],e['path']
assert sha(R/'ra2/build-original-c/ra2.exe')=='f40ca4c47e788636e149545112da046a9463f71498797699438a8835e33377b4'
for e in m:
    target=S/'baseline'/e['path'];target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/e['path'],target)
shutil.copy2(O/'source-manifest.json',S/'baseline/source-manifest.json')
for rel in ['reports/latest-recovery.json','reports/latest-state-comparison.json','reports/latest-movement-candidate.json','交接文档-原版逆向与C重编译-20261020.txt','交接文档-单位移动第十批正式验收-20261021.txt','docs/单位移动第十批-正式验收与预算回调-20261021.txt']:
    target=S/'baseline/project'/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(P/rel,target)
(S/'baseline/receipt.json').write_text(json.dumps(dict(passed=True,files=len(m),formal_executable_sha256=sha(R/'ra2/build-original-c/ra2.exe')),indent=2),encoding='utf-8')
print('Protected formal baseline',len(m))
