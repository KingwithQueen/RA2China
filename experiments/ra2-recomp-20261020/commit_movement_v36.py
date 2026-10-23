"""Commit this accepted batch locally after staged scope and exact-byte audits; never push."""
from pathlib import Path
import hashlib,json,subprocess,sys
R=Path(__file__).resolve().parent;P=R.parent.parent;S=R/'evidence/movement-state-v36'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def git(*args):return subprocess.check_output(['git','-c','core.fsmonitor=false','-c','core.autocrlf=false',*args],cwd=P)
assert read(S/'validation.json')['passed'] and read(S/'final-check.json')['passed']
for n in ['stage_movement','audit_git','audit_git_bytes']:
    subprocess.run([sys.executable,'-X','utf8','-B',str(R/(n+'_v36.py'))],cwd=R,check=True)
for n in ['git-whitespace-audit.json','git-byte-audit.json']:
    assert read(S/n)['passed'];git('add','--',(S/n).relative_to(P).as_posix())
names=[n.decode('utf-8') for n in git('diff','--cached','--name-only','-z').split(b'\0') if n]
assert names
batch=subprocess.check_output(['git','-c','core.fsmonitor=false','cat-file','--batch'],cwd=P,input=''.join(':'+n+'\n' for n in names).encode('utf-8'))
offset=0
for n in names:
    end=batch.index(b'\n',offset);header=batch[offset:end].split();assert len(header)==3 and header[1]==b'blob',(n,header)
    length=int(header[2]);blob=batch[end+1:end+1+length];assert blob==(P/n).read_bytes(),n
    offset=end+length+2
assert offset==len(batch)
for row in git('status','--porcelain','-z','--untracked-files=all').split(b'\0'):
    if row:assert row[:2] in [b'A ',b'M '],row
context=read(S/'vcs-context.json');assert git('rev-parse','HEAD').decode().strip()==context['parent_commit']
assert sha(P/'.git/config')==context['config_sha256']
assert hashlib.sha256(git('for-each-ref','--format=%(refname) %(objectname)','refs/remotes/')).hexdigest()==context['remote_refs_sha256']
hook=subprocess.run(['git','-c','core.fsmonitor=false','config','--get','core.hooksPath'],cwd=P,stdout=subprocess.PIPE,text=True);assert hook.returncode in [0,1]
hooks=Path(hook.stdout.strip()) if hook.returncode==0 else P/'.git/hooks'
if not hooks.is_absolute():hooks=P/hooks
assert not hooks.exists() or not any(p.is_file() and not p.name.endswith('.sample') for p in hooks.iterdir())
subprocess.run(['git','-c','core.fsmonitor=false','-c','core.autocrlf=false','commit','-m','Refactor movement destinations, building gates and placement exits; validate staggered bridge traffic (batch 35)'],cwd=P,check=True)
assert not git('status','--porcelain','--untracked-files=all')
subprocess.run([sys.executable,'-X','utf8','-B',str(R/'verify_final_movement_v36.py')],cwd=R,check=True)
print(json.dumps(dict(passed=True,local_commit=git('rev-parse','HEAD').decode().strip(),staged_files=len(names),all_index_bytes_verified=True,pushed=False)))
