"""保全第十批候选源、候选程序及仍在使用的第九批正式程序。"""
from pathlib import Path
import hashlib,json,shutil
R=Path(__file__).resolve().parent; P=R.parent.parent
O=R/'evidence/movement-state-v10'; S=R/'evidence/movement-state-v11'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert not S.exists()
m=json.loads((O/'source-manifest.json').read_text(encoding='utf-8'));assert len(m)==637
for e in m:
    assert sha(O/'final-source'/e['path'])==e['sha256']
    if e['path'] not in ('ra2/build-original-c/ra2.exe','build-faithful.ps1'):assert sha(R/e['path'])==e['sha256'],e['path']
assert sha(R/'ra2/build-original-c/ra2.exe')=='734138bb0a3b1638745a3e61adb9f59953e3e48ddca2129d1a4ef585407b0bfa'
for e in m:
    target=S/'baseline'/e['path'];target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(O/'final-source'/e['path'],target)
shutil.copy2(O/'source-manifest.json',S/'baseline/source-manifest.json')
shutil.copy2(R/'ra2/build-original-c/ra2.exe',S/'baseline/formal-v9.exe')
for rel in ['reports/latest-recovery.json','reports/latest-state-comparison.json','reports/latest-movement-candidate.json',
    'docs/单位移动第十批-友方碰撞与地形尾部-候选-20261021.txt','交接文档-单位移动第十批-20261021.txt']:
    target=S/'baseline/project'/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(P/rel,target)
(S/'baseline/receipt.json').write_text(json.dumps(dict(passed=True,candidate_files=637,
    candidate_sha256=sha(O/'candidate/ra2.exe'),formal_sha256=sha(S/'baseline/formal-v9.exe'),
    permitted_live_change={'path':'build-faithful.ps1','sha256':sha(R/'build-faithful.ps1'),
    'reason':'Content-based rebuild check added before snapshot; original script archived unchanged.'}),indent=2),encoding='utf-8')
print('Preserved candidate source and both executables',len(m))
