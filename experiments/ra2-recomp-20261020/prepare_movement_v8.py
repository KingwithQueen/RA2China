"""在任何第八批修改前核对并保留第七批正式节点，不覆盖既有证据。"""
from pathlib import Path
import hashlib
import json
import shutil

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parent.parent
OLD = ROOT / 'evidence/movement-state-v7'
NEW = ROOT / 'evidence/movement-state-v8'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

assert not NEW.exists(), NEW
manifest = json.loads((OLD / 'source-manifest.json').read_text(encoding='utf-8'))
for entry in manifest:
    for base in (ROOT, OLD / 'final-source'):
        assert sha(base / entry['path']) == entry['sha256'], base / entry['path']
expected = '8d84594096407e3442a6e66c0d1baa64c34996256b1a9fef97cb0d24f98f6b0f'
assert sha(ROOT / 'ra2/build-original-c/ra2.exe') == expected
for entry in manifest:
    target = NEW / 'baseline' / entry['path']
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / entry['path'], target)
for relative in ('reports/latest-recovery.json', 'reports/latest-state-comparison.json',
                 'docs/单位移动第七批-速度准备与转弯碰撞-20261021.txt',
                 '交接文档-单位移动第七批-20261021.txt'):
    target = NEW / 'baseline/project' / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(PROJECT / relative, target)
shutil.copy2(OLD / 'source-manifest.json', NEW / 'baseline/source-manifest.json')
(NEW / 'baseline/receipt.json').write_text(json.dumps(dict(
    passed=True, source_files_verified=len(manifest), executable_sha256=expected,
    previous_validation=str(OLD / 'validation.json')), ensure_ascii=False, indent=2), encoding='utf-8')
print('Preserved verified v7 baseline:', len(manifest), expected)
