"""Verify each compiled source/header byte against the local commit index."""
from pathlib import Path
import hashlib
import json
import subprocess

R = Path(__file__).resolve().parent
P = R.parent.parent
S = R / 'evidence/movement-state-v29'
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
sha = lambda data: hashlib.sha256(data).hexdigest()
validation = read(S / 'validation.json')
receipt = read(R / 'ra2/build-original-c/source-content-receipt.json')
assert validation['passed'] and receipt['executable_sha256'] == validation['exe_sha256']
assert len(receipt['inputs']) == 288
paths = [(Path(path).relative_to(P).as_posix(), digest) for path, digest in receipt['inputs'].items()]
query = ''.join(':' + path + '\n' for path, _ in paths).encode('utf-8')
result = subprocess.run(['git', 'cat-file', '--batch'], cwd=P, input=query, stdout=subprocess.PIPE, check=True)
offset = 0
for path, digest in paths:
    end = result.stdout.index(b'\n', offset)
    header = result.stdout[offset:end].split()
    assert len(header) == 3 and header[1] == b'blob', (path, header)
    length = int(header[2])
    content = result.stdout[end + 1:end + 1 + length]
    assert sha(content) == digest == sha((P / path).read_bytes()), path
    offset = end + 1 + length
    assert result.stdout[offset:offset + 1] == b'\n'
    offset += 1
assert offset == len(result.stdout)
changed = subprocess.check_output(['git', 'diff', '--cached', '--name-only', '-z'], cwd=P)
names = [n.decode('utf-8') for n in changed.split(b'\0') if n]
for name in names:
    content = subprocess.check_output(['git', 'show', ':' + name], cwd=P)
    assert content == (P / name).read_bytes(), name
value = dict(passed=True, compiled_inputs=288, compiled_inputs_match_index_byte_for_byte=True,
    staged_files_checked=len(names), staged_worktree_bytes_identical=True, executable_sha256=validation['exe_sha256'],
    remote_actions=False)
out = S / 'git-byte-audit.json'
assert not out.exists()
out.write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')
print(json.dumps(value))
