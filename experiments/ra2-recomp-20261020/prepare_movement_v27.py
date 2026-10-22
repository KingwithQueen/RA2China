"""Protect accepted generation 25 before continuing readable movement work."""
from pathlib import Path
import hashlib, json, shutil

R = Path(__file__).resolve().parent
P = R.parent.parent
O = R / 'evidence/movement-state-v26'
S = R / 'evidence/movement-state-v27'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
manifest = json.loads((O / 'source-manifest.json').read_text(encoding='utf-8'))
assert len(manifest) == 2908 and not S.exists()
for item in manifest:
    assert sha(R / item['path']) == sha(O / 'final-source' / item['path']) == item['sha256'], item['path']
assert sha(R / 'ra2/build-original-c/ra2.exe') == '6f539c31d0029d807673022e595a6300caad6b2a1e5291be55934e49a2dd6bab'
for item in manifest:
    dest = S / 'baseline' / item['path']
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(R / item['path'], dest)
shutil.copy2(O / 'source-manifest.json', S / 'baseline/source-manifest.json')
for rel in ['README.md', 'reports/latest-recovery.json', 'reports/latest-state-comparison.json',
            'reports/latest-movement-candidate.json', '交接文档-原版逆向与C重编译-20261020.txt',
            '交接文档-单位移动第二十五批正式验收-20261022.txt',
            'docs/单位移动第二十五批-内部模板与通行入口及共享返回-20261022.txt']:
    dest = S / 'baseline/project' / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(P / rel, dest)
for path in R.glob('*v26*'):
    if path.is_file() and path.suffix in ('.ps1', '.py') and not path.name.startswith(
            ('prepare_', 'finalize_', 'integrate_', 'preflight_', 'normalize_', 'preserve-', 'polish_')):
        dest = R / path.name.replace('v26', 'v27')
        assert not dest.exists()
        dest.write_text(path.read_text(encoding='utf-8-sig').replace('v26', 'v27'), encoding='utf-8', newline='\n')
for path in O.iterdir():
    if path.is_file() and path.suffix in ('.c', '.h', '.asm'):
        shutil.copy2(path, S / path.name)
shutil.copytree(O / 'fixtures', S / 'fixtures')
(S / 'pending').mkdir()
(S / 'baseline/receipt.json').write_text(json.dumps(dict(
    passed=True, files=len(manifest), formal_exe_sha256=sha(R / 'ra2/build-original-c/ra2.exe')),
    indent=2) + '\n', encoding='utf-8')
print('Protected', len(manifest), 'files')
