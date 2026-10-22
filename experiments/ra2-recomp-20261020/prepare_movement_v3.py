"""核对上一轮验收指纹并保留第三批工作所需的完整聚焦回退。"""
import hashlib
import json
import shutil
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parent.parent
STAGE = ROOT / 'evidence/movement-prepare-v3'
PREVIOUS = ROOT / 'evidence/movement-state-v2'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


pointer = json.loads((PROJECT / 'reports/latest-recovery.json').read_text(encoding='utf-8'))
assert pointer['sha256'] == sha(ROOT / 'ra2/build-original-c/ra2.exe') == 'b1471d51b290b91040b529e084b35240f4e2b96c2bb8360675181dd97cecf46e'
manifest = json.loads((PREVIOUS / 'source-manifest.json').read_text(encoding='utf-8'))
assert all(sha(ROOT / item['path']) == item['sha256'] for item in manifest)
STAGE.mkdir(exist_ok=False)
baseline = STAGE / 'baseline'
for item in manifest:
    source = ROOT / item['path']
    target = baseline / item['path']
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
for relative in ['reports/latest-recovery.json', 'reports/latest-state-comparison.json', 'docs/逆向恢复与C重编译.txt',
    'docs/单位移动路径碰撞与状态机整理-20261021.txt']:
    target = baseline / 'project' / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(PROJECT / relative, target)
(baseline / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
sys.path.insert(0, str(ROOT / 'python_lib'))
import pefile
pe = pefile.PE(str(ROOT / 'ra2/game/game.exe'))
image = pe.get_memory_mapped_image()
constants = {hex(address): struct.unpack_from('<d', image, address - 0x400000)[0] for address in [0x79B608, 0x79B610]}
(STAGE / 'constants.json').write_text(json.dumps(constants, indent=2), encoding='utf-8')
shutil.copy2(PREVIOUS / 'native_probe_host.h', STAGE / 'native_probe_host.h')
print(json.dumps({'baseline_files': len(manifest), 'previous_exe': pointer['sha256'], 'constants': constants}))
