"""Protect accepted generation 22, without resetting any working files."""
from pathlib import Path
import hashlib,json,shutil
R=Path(__file__).resolve().parent;P=R.parent.parent;O=R/'evidence/movement-state-v23';S=R/'evidence/movement-state-v24'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((O/'source-manifest.json').read_text(encoding='utf-8'));assert len(m)==2373 and not S.exists()
for e in m:assert sha(R/e['path'])==sha(O/'final-source'/e['path'])==e['sha256'],e['path']
assert sha(R/'ra2/build-original-c/ra2.exe')=='a267f7f23652a3a97ecca16b97cc497cebf0d588b4b2eec65190df094ea61f3e'
for e in m:
    dest=S/'baseline'/e['path'];dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/e['path'],dest)
shutil.copy2(O/'source-manifest.json',S/'baseline/source-manifest.json')
for rel in ['reports/latest-recovery.json','reports/latest-state-comparison.json','reports/latest-movement-candidate.json','交接文档-原版逆向与C重编译-20261020.txt','交接文档-单位移动第二十二批正式验收-20261022.txt','docs/单位移动第二十二批-隧道状态与内部接续及通行分类-20261022.txt']:
    dest=S/'baseline/project'/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(P/rel,dest)
for p in R.glob('*v23*'):
    if p.is_file() and p.suffix in ('.ps1','.py') and not p.name.startswith(('prepare_','finalize_','integrate_','preflight_','normalize_','preserve-','polish_')):
        dest=R/p.name.replace('v23','v24');assert not dest.exists();dest.write_text(p.read_text(encoding='utf-8-sig').replace('v23','v24'),encoding='utf-8',newline='\n')
for p in O.iterdir():
    if p.is_file() and p.suffix in ('.c','.h'):shutil.copy2(p,S/p.name)
shutil.copytree(O/'fixtures',S/'fixtures');(S/'pending').mkdir()
(S/'baseline/receipt.json').write_text(json.dumps(dict(passed=True,files=len(m),formal_exe_sha256=sha(R/'ra2/build-original-c/ra2.exe')),indent=2),encoding='utf-8')
print('Protected',len(m),'files')
