"""第九批修改前核对第八批正式源和程序，并建立完整回退副本。"""
from pathlib import Path
import hashlib,json,shutil
ROOT=Path(__file__).resolve().parent;PROJECT=ROOT.parent.parent
OLD=ROOT/'evidence/movement-state-v8';NEW=ROOT/'evidence/movement-state-v9'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
assert not NEW.exists()
manifest=json.loads((OLD/'source-manifest.json').read_text(encoding='utf-8'));assert len(manifest)==449
for e in manifest:
    for base in (ROOT,OLD/'final-source'): assert sha(base/e['path'])==e['sha256'],base/e['path']
expected='e16033580b82aed1fea031052703407d5b39dfe305b271c36cf6501ce0056ae9'
assert sha(ROOT/'ra2/build-original-c/ra2.exe')==expected
for e in manifest:
    target=NEW/'baseline'/e['path'];target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/e['path'],target)
for relative in ('reports/latest-recovery.json','reports/latest-state-comparison.json',
    'docs/单位移动第八批-路径推进与碰撞前置-20261021.txt','交接文档-单位移动第八批-20261021.txt'):
    target=NEW/'baseline/project'/relative;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(PROJECT/relative,target)
shutil.copy2(OLD/'source-manifest.json',NEW/'baseline/source-manifest.json')
(NEW/'baseline/receipt.json').write_text(json.dumps(dict(passed=True,source_files_verified=len(manifest),
    executable_sha256=expected,previous_validation=str(OLD/'validation.json')),indent=2),encoding='utf-8')
print('Preserved verified v8 baseline:',len(manifest),expected)
