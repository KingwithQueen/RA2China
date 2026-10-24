"""Allowlisted local commit with exact source/index verification; no network actions."""
from run_batch_v40 import R,P,S,O,read,write,sha
from pathlib import Path
import subprocess,hashlib,re,sys,json
def git(*args):return subprocess.check_output(['git','-c','core.fsmonitor=false','-c','core.autocrlf=false','-c','core.quotepath=false',*args],cwd=P)
subprocess.run([sys.executable,'-X','utf8','-B',str(R/'verify_final_movement_v40.py'),'--precommit'],cwd=R,check=True)
assert not git('diff','--cached','--name-only')
root_files={'README.md','reports/latest-recovery.json','reports/latest-state-comparison.json','reports/latest-movement-candidate.json','交接文档-原版逆向与C重编译-20261020.txt','交接文档-新对话继续推进-20261022.txt','交接文档-单位移动第三十九批正式验收-20261024.txt','docs/单位移动第三十九批-跨格进入与列车碰撞及共享定位业务-20261024.txt'}
pres=read(S/'preservation.json');sources=set(pres['changed_compile_inputs']+pres['added_compile_inputs'])|{'ra2/CMakeLists.txt','ra2/src/gameplay/阅读说明-单位移动.txt'};prefix=R.relative_to(P).as_posix()+'/'
names=[]
for row in git('status','--porcelain','-z','--untracked-files=all').split(b'\0'):
 if not row:continue
 status=row[:2];name=row[3:].decode('utf-8');assert status in [b' M',b'??'],(status,name)
 allowed=name in root_files
 if name.startswith(prefix):
  rel=name[len(prefix):];p=Path(rel);allowed|=rel in sources
  allowed|='/' not in rel and 'v40' in p.name and p.suffix in ['.py','.ps1']
  if rel.startswith('evidence/movement-state-v40/'):
   tail=Path(rel).parts[2:]
   allowed|=len(tail)==1 and p.suffix in ['.json','.c','.h','.asm']
   allowed|=len(tail)==2 and tail[0]=='fixtures' and p.suffix.lower() in ['.map','.ini']
 assert allowed and (P/name).is_file() and (P/name).resolve().is_relative_to(P.resolve()),name
 names.append(name)
for start in range(0,len(names),40):git('add','--',*names[start:start+40])
write(S/'git-staging-scope.json',dict(passed=True,selected_files=len(names),allowlist_verified=True,baselines_archives_traces_executables_excluded=True,remote_actions=False))
git('add','--',(S/'git-staging-scope.json').relative_to(P).as_posix())
whitespace=subprocess.run(['git','-c','core.fsmonitor=false','-c','core.quotepath=false','diff','--cached','--check'],cwd=P,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8')
(S/'git-whitespace-check.log').write_text(whitespace.stdout,encoding='utf-8')
inherited={sha(p):str(p) for p in (O/'fixtures').iterdir() if p.is_file()}
inherited.update({sha(p):str(p) for p in O.iterdir() if p.is_file() and p.suffix in ['.c','.h','.asm','.json']})
warnings=[]
for line in whitespace.stdout.splitlines():
 match=re.match(r'(.+):(\d+): (.+)',line)
 if not match:continue
 name=match[1];reason=match[3];p=P/name
 assert p.exists() and p.is_relative_to(S) and sha(p) in inherited,(name,reason)
 warnings.append(dict(path=name,reason=reason,inherited_source=inherited[sha(p)],sha256=sha(p)))
assert whitespace.returncode==0 or warnings,whitespace.stdout
write(S/'git-whitespace-audit.json',dict(passed=True,exit_code=whitespace.returncode,all_warnings_are_unchanged_inherited_bytes=True,warnings=warnings))
git('add','--',(S/'git-whitespace-audit.json').relative_to(P).as_posix())
def verify_blobs(names):
 batch=subprocess.check_output(['git','-c','core.fsmonitor=false','cat-file','--batch'],cwd=P,input=''.join(':'+n+'\n' for n in names).encode('utf-8'));offset=0
 for name in names:
  end=batch.index(b'\n',offset);header=batch[offset:end].split();assert len(header)==3 and header[1]==b'blob',(name,header)
  length=int(header[2]);blob=batch[end+1:end+1+length];assert blob==(P/name).read_bytes(),name;offset=end+length+2
 assert offset==len(batch)
staged=[n.decode('utf-8') for n in git('diff','--cached','--name-only','-z').split(b'\0') if n]
compiled=[Path(p).relative_to(P).as_posix() for p in read(R/'ra2/build-original-c/source-content-receipt.json')['inputs']]
verify_blobs(sorted(set(staged+compiled)))
write(S/'git-byte-audit.json',dict(passed=True,staged_files=len(staged),compiled_inputs=len(compiled),all_staged_and_compiled_index_bytes_equal_worktree=True,generated_C_unchanged=True))
git('add','--',(S/'git-byte-audit.json').relative_to(P).as_posix())
staged=[n.decode('utf-8') for n in git('diff','--cached','--name-only','-z').split(b'\0') if n];verify_blobs(staged)
for row in git('status','--porcelain','-z','--untracked-files=all').split(b'\0'):
 if row:assert row[:2] in [b'A ',b'M '],row
context=read(S/'vcs-context.json');assert git('rev-parse','HEAD').decode().strip()==context['parent_commit'] and sha(P/'.git/config')==context['config_sha256']
assert hashlib.sha256(git('for-each-ref','--format=%(refname) %(objectname)','refs/remotes/')).hexdigest()==context['remote_refs_sha256']
hook=subprocess.run(['git','-c','core.fsmonitor=false','config','--get','core.hooksPath'],cwd=P,stdout=subprocess.PIPE,text=True);assert hook.returncode in [0,1]
hooks=Path(hook.stdout.strip()) if hook.returncode==0 else P/'.git/hooks'
if not hooks.is_absolute():hooks=P/hooks
assert not hooks.exists() or not any(p.is_file() and not p.name.endswith('.sample') for p in hooks.iterdir())
git('commit','-m','Share cell-placement workflow and expose sampled movement effects (batch 39)')
assert not git('status','--porcelain','--untracked-files=all')
subprocess.run([sys.executable,'-X','utf8','-B',str(R/'verify_final_movement_v40.py')],cwd=R,check=True)
value=dict(passed=True,commit=git('rev-parse','HEAD').decode().strip(),parent_commit=context['parent_commit'],staged_files=len(staged),all_index_bytes_verified=True,pushed=False)
write(S/'postcommit/git-local-commit.json',value);print(json.dumps(value))
