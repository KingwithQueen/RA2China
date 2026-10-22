"""第十批修改前核对第九批正式源和程序，并建立完整回退副本。"""
from pathlib import Path
import hashlib,json,shutil
ROOT=Path(__file__).resolve().parent;PROJECT=ROOT.parent.parent
OLD=ROOT/'evidence/movement-state-v9';NEW=ROOT/'evidence/movement-state-v10'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
assert not (NEW/'baseline/receipt.json').exists()
manifest=json.loads((OLD/'source-manifest.json').read_text(encoding='utf-8'));assert len(manifest)==536
for e in manifest:
    for base in (ROOT,OLD/'final-source'): assert sha(base/e['path'])==e['sha256'],base/e['path']
expected='734138bb0a3b1638745a3e61adb9f59953e3e48ddca2129d1a4ef585407b0bfa'
assert sha(ROOT/'ra2/build-original-c/ra2.exe')==expected
for e in manifest:
    target=NEW/'baseline'/e['path'];target.parent.mkdir(parents=True,exist_ok=True)
    if target.exists(): assert sha(target)==e['sha256'],target
    else: shutil.copy2(ROOT/e['path'],target)
for relative in ('reports/latest-recovery.json','reports/latest-state-comparison.json',
    'docs/单位移动第九批-转弯接续与对象碰撞-20261021.txt','交接文档-单位移动第九批-20261021.txt'):
    target=NEW/'baseline/project'/relative;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(PROJECT/relative,target)
shutil.copy2(OLD/'source-manifest.json',NEW/'baseline/source-manifest.json')
(NEW/'baseline/receipt.json').write_text(json.dumps(dict(passed=True,source_files_verified=len(manifest),
    executable_sha256=expected,previous_validation=str(OLD/'validation.json')),indent=2),encoding='utf-8')
print('Preserved verified v9 baseline:',len(manifest),expected)
