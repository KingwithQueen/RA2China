"""在任何第六批修改前核对并保留第五批正式节点，不覆盖既有证据。"""
from pathlib import Path
import hashlib
import json
import shutil

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parent.parent
OLD = ROOT / 'evidence/movement-state-v5'
NEW = ROOT / 'evidence/movement-state-v6'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

assert not NEW.exists(), NEW
manifest = json.loads((OLD / 'source-manifest.json').read_text(encoding='utf-8'))
for entry in manifest:
    for base in (ROOT, OLD / 'final-source'):
        assert sha(base / entry['path']) == entry['sha256'], base / entry['path']
expected = '21bf588194a220e34a8793f3cfe2335e851656c089c34a05da2caf8dcfbf0964'
assert sha(ROOT / 'ra2/build-original-c/ra2.exe') == expected
for entry in manifest:
    target = NEW / 'baseline' / entry['path']
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / entry['path'], target)
for relative in ('reports/latest-recovery.json', 'reports/latest-state-comparison.json',
                 'docs/单位移动第五批-阻挡等待与预算条件-20261021.txt',
                 '交接文档-单位移动第五批-20261021.txt'):
    target = NEW / 'baseline/project' / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(PROJECT / relative, target)
shutil.copy2(OLD / 'source-manifest.json', NEW / 'baseline/source-manifest.json')
(NEW / 'baseline/receipt.json').write_text(json.dumps(dict(
    passed=True, source_files_verified=len(manifest), executable_sha256=expected,
    previous_validation=str(OLD / 'validation.json')), ensure_ascii=False, indent=2), encoding='utf-8')
print('Preserved verified v5 baseline:', len(manifest), expected)
