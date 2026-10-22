"""在任何第五批修改前核对并保留第四批正式节点，不覆盖既有证据。"""
from pathlib import Path
import hashlib
import json
import shutil

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parent.parent
OLD = ROOT / 'evidence/movement-state-v4'
NEW = ROOT / 'evidence/movement-state-v5'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

assert not NEW.exists(), NEW
manifest = json.loads((OLD / 'source-manifest.json').read_text(encoding='utf-8'))
for entry in manifest:
    for base in (ROOT, OLD / 'final-source'):
        assert sha(base / entry['path']) == entry['sha256'], base / entry['path']
expected = 'a91b434a273fe2e621b6fdfa500e6eecd0f4c33f1c7cc41e2f48e7e3a1f7ce0d'
assert sha(ROOT / 'ra2/build-original-c/ra2.exe') == expected
for entry in manifest:
    target = NEW / 'baseline' / entry['path']
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / entry['path'], target)
for relative in ('reports/latest-recovery.json', 'reports/latest-state-comparison.json',
                 'docs/路径准备内部状态与墙闸实景验证-20261021.txt',
                 '交接文档-单位移动第四批-20261021.txt'):
    target = NEW / 'baseline/project' / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(PROJECT / relative, target)
shutil.copy2(OLD / 'source-manifest.json', NEW / 'baseline/source-manifest.json')
(NEW / 'baseline/receipt.json').write_text(json.dumps(dict(
    passed=True, source_files_verified=len(manifest), executable_sha256=expected,
    previous_validation=str(OLD / 'validation.json')), ensure_ascii=False, indent=2), encoding='utf-8')
print('Preserved verified v4 baseline:', len(manifest), expected)
