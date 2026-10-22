"""Protect accepted generation 16, without resetting any working files."""
from pathlib import Path
import hashlib,json,shutil
R=Path(__file__).resolve().parent;P=R.parent.parent;O=R/'evidence/movement-state-v17';S=R/'evidence/movement-state-v18'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((O/'source-manifest.json').read_text(encoding='utf-8'));assert len(m)==1497 and not S.exists()
for e in m:assert sha(R/e['path'])==sha(O/'final-source'/e['path'])==e['sha256'],e['path']
assert sha(R/'ra2/build-original-c/ra2.exe')=='c2d76b8f30c83a52fb6785367d641c89e69afe94bc76cb849e9e81d04cb371c0'
for e in m:
    dest=S/'baseline'/e['path'];dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/e['path'],dest)
shutil.copy2(O/'source-manifest.json',S/'baseline/source-manifest.json')
for rel in ['reports/latest-recovery.json','reports/latest-state-comparison.json','reports/latest-movement-candidate.json','交接文档-原版逆向与C重编译-20261020.txt','交接文档-单位移动第十六批正式验收-20261022.txt','docs/单位移动第十六批-局部碰撞与搜索退出-20261022.txt']:
    dest=S/'baseline/project'/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(P/rel,dest)
for p in R.glob('*v17*'):
    if p.is_file() and p.suffix in ('.ps1','.py') and not p.name.startswith(('prepare_','finalize_','integrate_','preflight_')):
        dest=R/p.name.replace('v17','v18');assert not dest.exists();dest.write_text(p.read_text(encoding='utf-8-sig').replace('v17','v18'),encoding='utf-8')
for p in O.iterdir():
    if p.is_file() and p.suffix in ('.c','.h'):shutil.copy2(p,S/p.name)
shutil.copytree(O/'fixtures',S/'fixtures');(S/'pending').mkdir()
(S/'baseline/receipt.json').write_text(json.dumps(dict(passed=True,files=len(m),formal_exe_sha256=sha(R/'ra2/build-original-c/ra2.exe')),indent=2),encoding='utf-8')
print('Protected',len(m),'files')
