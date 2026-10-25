"""Allowlisted local commit, verified index bytes, no hooks or remote operations."""
from run_batch_v68 import *
import re
subprocess.run(py('verify_closeout_v68.py','--precommit'),cwd=R,check=True)
assert not git('diff','--cached','--name-only')
root_files={'README.md','交接文档-原版逆向与C重编译-20261020.txt','交接文档-新对话继续推进-20261022.txt','交接文档-单位移动第六十七批正式验收-20261025.txt','docs/单位移动第六十七批-移动域收口-20261025.txt','docs/移动域收口清单-20261025.txt','docs/当前进度与剩余内容-20261025-第六十七批.txt'}
root_files|={'reports/'+n for n in ['latest-recovery.json','latest-state-comparison.json','latest-movement-candidate.json']}
source=read(S/'source-preservation.json');sources=set(source['changed_compile_inputs']+source['added_compile_inputs'])|{'ra2/CMakeLists.txt','ra2/src/gameplay/阅读说明-单位移动.txt'}
prefix=R.relative_to(P).as_posix()+'/';names=[]
for row in git('status','--porcelain','-z','--untracked-files=all').split(b'\0'):
    if not row:continue
    status=row[:2];name=row[3:].decode('utf-8');assert status in [b' M',b'??'],(status,name)
    allowed=name in root_files
    if name.startswith(prefix):
        rel=name[len(prefix):];p=Path(rel);allowed|=rel in sources
        allowed|='/' not in rel and 'v68' in p.name and p.suffix in ['.py','.ps1']
        if rel.startswith('evidence/movement-state-v68/'):
            tail=Path(rel).parts[2:]
            allowed|=len(tail)==1 and (p.suffix in ['.json','.c','.h'] or p.name in ['analyze-other-initial.py','stop-command-initial.py'])
            allowed|=len(tail)==2 and tail[0]=='fixtures' and p.suffix.lower() in ['.map','.ini']
    assert allowed and (P/name).is_file() and (P/name).resolve().is_relative_to(P.resolve()),name
    names.append(name)
for start in range(0,len(names),40):git('add','--',*names[start:start+40])
write(S/'git-staging-scope.json',dict(passed=True,selected_files=len(names),allowlist_verified=True,executables_archives_traces_original_assets_excluded=True,remote_actions=False))
git('add','--',(S/'git-staging-scope.json').relative_to(P).as_posix())
q=subprocess.run(['git','-c','core.fsmonitor=false','-c','core.quotepath=false','diff','--cached','--check'],cwd=P,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
output=q.stdout.decode('utf-8',errors='replace');(S/'git-whitespace-check.log').write_text(output,encoding='utf-8')
inherited={}
for name in ['native-origins.json','collision-origin.json']:
    for e in read(S/name)['files']:inherited[e['sha256']]=e['path']
for p in O.iterdir():
    if p.is_file() and p.suffix in ['.c','.h']:inherited[sha(p)]=str(p)
old_chunk=(S/'baseline/ra2/src/recomp/gen_game/recomp_0023.c').read_bytes().splitlines()
rules=read(S/'scene-recipes-pending.json');original_rules=Path(rules['rules_original']);assert sha(original_rules)==rules['rules_original_sha256'];rules_lines=original_rules.read_bytes().splitlines()
warnings=[]
for line in output.splitlines():
    m=re.match(r'(.+):(\d+): (.+)',line)
    if not m:continue
    name,number,reason=m[1],int(m[2]),m[3];p=P/name;assert p.exists() and p.is_relative_to(S),(name,reason)
    if sha(p) in inherited:origin=inherited[sha(p)]
    elif p.name=='map-area-generated-before.c':
        assert reason=='trailing whitespace.' and p.read_bytes().splitlines()[number-1] in old_chunk;origin='Exact original generated map function slice'
    elif p.suffix.lower()=='.map' and p.parent==S/'fixtures' and reason=='new blank line at EOF.':origin='Map layout EOF retained'
    elif p.suffix.lower()=='.ini' and p.parent==S/'fixtures':
        rawline=p.read_bytes().splitlines()[number-1]
        assert rawline in rules_lines or rawline.replace(b'CloseEnough=0',b'CloseEnough=2.25') in rules_lines
        origin=str(original_rules)+' (same original rule line; explicit CloseEnough override only)'
    else:raise AssertionError((name,number,reason))
    warnings.append(dict(path=name,line=number,reason=reason,inherited_source=origin,sha256=sha(p)))
assert q.returncode==0 or warnings,output
write(S/'git-whitespace-audit.json',dict(passed=True,exit_code=q.returncode,warnings=warnings,only_exact_original_bytes_or_map_layout=True))
git('add','--',(S/'git-whitespace-audit.json').relative_to(P).as_posix())
def verify_blobs(names):
    content=subprocess.check_output(['git','-c','core.fsmonitor=false','cat-file','--batch'],cwd=P,input=''.join(':'+n+'\n' for n in names).encode('utf-8'));offset=0
    for name in names:
        end=content.index(b'\n',offset);header=content[offset:end].split();assert len(header)==3 and header[1]==b'blob',(name,header)
        length=int(header[2]);assert content[end+1:end+1+length]==(P/name).read_bytes(),name;offset=end+length+2
    assert offset==len(content)
staged=[x.decode('utf-8') for x in git('diff','--cached','--name-only','-z').split(b'\0') if x]
compiled=[Path(p).relative_to(P).as_posix() for p in read(R/'ra2/build-original-c/source-content-receipt.json')['inputs']]
verify_blobs(sorted(set(staged+compiled)))
write(S/'git-byte-audit.json',dict(passed=True,staged_files=len(staged),compiled_inputs=len(compiled),all_index_and_worktree_bytes_equal=True))
git('add','--',(S/'git-byte-audit.json').relative_to(P).as_posix())
staged=[x.decode('utf-8') for x in git('diff','--cached','--name-only','-z').split(b'\0') if x];verify_blobs(staged)
for row in git('status','--porcelain','-z','--untracked-files=all').split(b'\0'):
    if row:assert row[:2] in [b'A ',b'M '],row
context=read(S/'vcs-context.json');assert git('rev-parse','HEAD').decode().strip()==context['parent_commit'] and sha(P/'.git/config')==context['config_sha256']
assert hashlib.sha256(git('for-each-ref','--format=%(refname) %(objectname)','refs/remotes/')).hexdigest()==context['remote_refs_sha256']
hook=subprocess.run(['git','config','--get','core.hooksPath'],cwd=P,stdout=subprocess.PIPE,text=True);assert hook.returncode in [0,1]
hooks=Path(hook.stdout.strip()) if hook.returncode==0 else P/'.git/hooks'
if not hooks.is_absolute():hooks=P/hooks
assert not hooks.exists() or not any(p.is_file() and not p.name.endswith('.sample') for p in hooks.iterdir())
git('commit','-m','Close movement admission, occupation, stop and finite fairness boundaries (batch 67)')
assert not git('status','--porcelain','--untracked-files=all')
subprocess.run(py('verify_closeout_v68.py'),cwd=R,check=True)
value=dict(passed=True,commit=git('rev-parse','HEAD').decode().strip(),parent_commit=context['parent_commit'],staged_files=len(staged),all_index_bytes_verified=True,pushed=False)
write(S/'postcommit/git-local-commit.json',value);print(json.dumps(value))
