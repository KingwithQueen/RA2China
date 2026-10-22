"""核对 v3 后建立独立 v4 回退；拒绝覆盖已有证据。"""
import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parent.parent
STAGE = ROOT / 'evidence/movement-state-v4'
PREVIOUS = ROOT / 'evidence/movement-prepare-v3'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

pointer = json.loads((PROJECT / 'reports/latest-recovery.json').read_text(encoding='utf-8'))
assert pointer['sha256'] == sha(ROOT / 'ra2/build-original-c/ra2.exe') == '3a3024ced1d2315662d7534b096054ba1bcbd4e92f64bb44021b31ca12eb0581'
manifest = json.loads((PREVIOUS / 'source-manifest.json').read_text(encoding='utf-8'))
assert all(sha(ROOT / item['path']) == item['sha256'] for item in manifest)
STAGE.mkdir(exist_ok=False)
baseline = STAGE / 'baseline'
for item in manifest:
    target = baseline / item['path']
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / item['path'], target)
for relative in ['reports/latest-recovery.json', 'reports/latest-state-comparison.json',
                 'docs/逆向恢复与C重编译.txt', 'docs/路径准备重寻路与障碍状态整理-20261021.txt']:
    target = baseline / 'project' / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(PROJECT / relative, target)
(baseline / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
shutil.copy2(PREVIOUS / 'native_probe_host.h', STAGE / 'native_probe_host.h')
print(json.dumps({'baseline_files': len(manifest), 'sha256': pointer['sha256']}))
