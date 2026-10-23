"""Protect generation 27; never run archived round-28 writers in place."""
from pathlib import Path
import hashlib, json, shutil, subprocess

R = Path(__file__).resolve().parent
P = R.parent.parent
O = R / 'evidence/movement-state-v28'
S = R / 'evidence/movement-state-v29'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
manifest = read(O / 'source-manifest.json')
assert len(manifest) == 3340 and not S.exists()
assert subprocess.check_output(['git', 'status', '--porcelain'], cwd=P) == b'?? experiments/ra2-recomp-20261020/prepare_movement_v29.py\n'
assert sha(R / 'ra2/build-original-c/ra2.exe') == '597bfc9d99c93154564687292098ed199b8a98ea5848d587459317aa0859e5e8'
for item in manifest:
    assert sha(R / item['path']) == sha(O / 'final-source' / item['path']) == item['sha256'], item['path']
for item in manifest:
    dest = S / 'baseline' / item['path']
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(R / item['path'], dest)
shutil.copy2(O / 'source-manifest.json', S / 'baseline/source-manifest.json')
for rel in ['README.md', 'reports/latest-recovery.json', 'reports/latest-state-comparison.json',
            'reports/latest-movement-candidate.json', '交接文档-原版逆向与C重编译-20261020.txt',
            '交接文档-新对话继续推进-20261022.txt', '交接文档-单位移动第二十七批正式验收-20261023.txt',
            'docs/单位移动第二十七批-桥层模板与类别过滤及共享出口-20261023.txt']:
    dest = S / 'baseline/project' / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(P / rel, dest)
for path in R.glob('*v28*'):
    if path.is_file() and path.suffix in ('.ps1', '.py') and not path.name.startswith(
            ('prepare_', 'finalize_', 'integrate_', 'preflight_', 'normalize_', 'preserve-', 'polish_', 'verify_final_', 'audit_git_')):
        dest = R / path.name.replace('v28', 'v29')
        assert not dest.exists()
        dest.write_text(path.read_text(encoding='utf-8-sig').replace('v28', 'v29'), encoding='utf-8', newline='\n')
for path in O.iterdir():
    if path.is_file() and path.suffix in ('.c', '.h', '.asm'):
        shutil.copy2(path, S / path.name)
shutil.copytree(O / 'fixtures', S / 'fixtures')
(S / 'pending').mkdir()
for item in manifest:
    assert sha(S / 'baseline' / item['path']) == item['sha256'], item['path']
(S / 'baseline/receipt.json').write_text(json.dumps(dict(
    passed=True, files=len(manifest), code_commit='3cbe4f4c6222dea05722a807f82be309057c2fae',
    head=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=P, text=True).strip(),
    formal_exe_sha256=sha(R / 'ra2/build-original-c/ra2.exe')), indent=2) + '\n', encoding='utf-8')
print('Protected', len(manifest), 'files')
