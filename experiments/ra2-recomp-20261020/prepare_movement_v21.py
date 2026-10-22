"""Protect accepted generation 19, without resetting any working files."""
from pathlib import Path
import hashlib,json,shutil
R=Path(__file__).resolve().parent;P=R.parent.parent;O=R/'evidence/movement-state-v20';S=R/'evidence/movement-state-v21'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((O/'source-manifest.json').read_text(encoding='utf-8'));assert len(m)==1902 and not S.exists()
for e in m:assert sha(R/e['path'])==sha(O/'final-source'/e['path'])==e['sha256'],e['path']
assert sha(R/'ra2/build-original-c/ra2.exe')=='ccdda6b1c1ee2985610467dbb40cac6650c84d8af89bcbdad6d8c70bea24ed40'
for e in m:
    dest=S/'baseline'/e['path'];dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/e['path'],dest)
shutil.copy2(O/'source-manifest.json',S/'baseline/source-manifest.json')
for rel in ['reports/latest-recovery.json','reports/latest-state-comparison.json','reports/latest-movement-candidate.json','交接文档-原版逆向与C重编译-20261020.txt','交接文档-单位移动第十九批正式验收-20261022.txt','docs/单位移动第十九批-到达收尾与目标清理及基础通行高度服务-20261022.txt']:
    dest=S/'baseline/project'/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(P/rel,dest)
for p in R.glob('*v20*'):
    if p.is_file() and p.suffix in ('.ps1','.py') and not p.name.startswith(('prepare_','finalize_','integrate_','preflight_','normalize_','preserve-')):
        dest=R/p.name.replace('v20','v21');assert not dest.exists();dest.write_text(p.read_text(encoding='utf-8-sig').replace('v20','v21'),encoding='utf-8',newline='\n')
for p in O.iterdir():
    if p.is_file() and p.suffix in ('.c','.h'):shutil.copy2(p,S/p.name)
shutil.copytree(O/'fixtures',S/'fixtures');(S/'pending').mkdir()
(S/'baseline/receipt.json').write_text(json.dumps(dict(passed=True,files=len(m),formal_exe_sha256=sha(R/'ra2/build-original-c/ra2.exe')),indent=2),encoding='utf-8')
print('Protected',len(m),'files')
