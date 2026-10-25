"""Resume the staged local commit; preserve the exact executed checker's EOF bytes."""
from run_batch_v64 import *
import re

def git(*args):
 return subprocess.check_output(['git','-c','core.fsmonitor=false','-c','core.autocrlf=false','-c','core.quotepath=false',*args],cwd=P)

def verify_index(names):
 batch=subprocess.check_output(['git','-c','core.fsmonitor=false','cat-file','--batch'],cwd=P,input=''.join(':'+n+'\n' for n in names).encode('utf-8'));offset=0
 for name in names:
  end=batch.index(b'\n',offset);header=batch[offset:end].split();assert len(header)==3 and header[1]==b'blob'
  length=int(header[2]);assert batch[end+1:end+1+length]==(P/name).read_bytes(),name;offset=end+length+2
 assert offset==len(batch)

assert not (S/'postcommit/git-local-commit.json').exists()
assert git('rev-parse','HEAD').decode().strip()==read(S/'vcs-context.json')['parent_commit']
scope=read(S/'git-staging-scope.json');assert scope['passed'] and scope['allowlist_verified']
staged=[x.decode('utf-8') for x in git('diff','--cached','--name-only','-z').split(b'\0') if x]
assert len(staged)==scope['selected_files']+1
verify_index(staged)

checker=R/'audit_scenes_v64.py';manifest=read(S/'source-manifest.json')
accepted_checker_sha256=next(e['sha256'] for e in manifest if e['path']==checker.name)
assert sha(checker)==accepted_checker_sha256 and checker.read_bytes().endswith(b'\n\n')
assert sha(S/'final-source'/checker.name)==accepted_checker_sha256
assert next(e['sha256'] for e in read(S/'cleanup-plan.json')['protected'] if Path(e['path'])==checker)==accepted_checker_sha256

# Keep the original failed staging/format report before the narrowly scoped resume.
out=S/'postcommit';out.mkdir(exist_ok=True)
for name in ['git-staging-scope.json','git-whitespace-check.log']:
 destination=out/('first-attempt-'+name);assert not destination.exists();shutil.copy2(S/name,destination)

# Append this new commit-only tool without changing any frozen checker or game input.
tool=Path(__file__).resolve();assert tool==R/'resume_commit_v64.py'
assert not tool.read_bytes().endswith(b'\n\n') and tool.name not in {e['path'] for e in manifest}
destination=S/'final-source'/tool.name;assert not destination.exists();shutil.copy2(tool,destination)
manifest.append(dict(path=tool.name,sha256=sha(tool)))
(S/'source-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
validation=read(S/'validation.json');validation['source_files']=len(manifest);validation['commit_resume_tool']=tool.name
(S/'validation.json').write_text(json.dumps(validation,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
check=read(S/'final-check.json');check['source_manifest_sha256']=sha(S/'source-manifest.json')
(S/'final-check.json').write_text(json.dumps(check,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
scope.update(selected_files=scope['selected_files']+1,resumed_after_format_audit=True,executed_checker_eof_exception_sha256=accepted_checker_sha256)
(S/'git-staging-scope.json').write_text(json.dumps(scope,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
git('add','--',*[p.relative_to(P).as_posix() for p in [tool,S/'source-manifest.json',S/'validation.json',S/'final-check.json',S/'git-staging-scope.json']])
subprocess.run(py('verify_final_movement_v64.py','--precommit'),cwd=R,check=True)

source=(R/'commit_movement_v64.py').read_text(encoding='utf-8')
source=source[source.index('whitespace=subprocess.run('):]
old=" assert p.exists() and p.is_relative_to(S),(name,reason)"
assert source.count(old)==1
source=source.replace(old," assert p.exists() and (p.is_relative_to(S) or (p==checker and reason=='new blank line at EOF.')),(name,reason)")
old=" if sha(p) in inherited:origin=inherited[sha(p)]"
assert source.count(old)==1
source=source.replace(old," if p==checker and reason=='new blank line at EOF.':\n  assert sha(p)==accepted_checker_sha256 and p.read_bytes().endswith(b'\\n\\n')\n  origin='Exact executed and archived checker bytes retained; only a terminal blank line, no trailing spaces or production change.'\n elif sha(p) in inherited:origin=inherited[sha(p)]")
source=source.replace('all_warnings_are_unchanged_inherited_bytes=True','all_warnings_are_preserved_validated_or_inherited_bytes=True')
exec(compile(source,str(R/'commit_movement_v64.py'),'exec'),globals())
