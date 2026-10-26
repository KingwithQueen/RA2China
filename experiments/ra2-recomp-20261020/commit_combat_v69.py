"""Allowlisted local-only commit with exact staged-source and inherited whitespace audit."""
from combat_batch_v69 import *
import re
subprocess.run(py('verify_combat_v69.py','--precommit'),cwd=R,check=True)
assert not git('diff','--cached','--name-only')
roots={'README.md','交接文档-原版逆向与C重编译-20261020.txt','交接文档-新对话继续推进-20261022.txt','交接文档-战斗与对象生命周期第一批正式验收-20261026.txt','docs/战斗与对象生命周期第一批-伤害接纳与生命结算-20261026.txt','docs/当前进度与剩余内容-20261026-战斗第一批.txt'}
roots|={'reports/'+n for n in ['latest-recovery.json','latest-state-comparison.json','latest-movement-candidate.json']}
source=read(S/'source-preservation.json');sources=set(source['changed_compile_inputs']+source['added_compile_inputs'])|{'ra2/CMakeLists.txt','ra2/src/gameplay/阅读说明-战斗.txt'}
prefix=R.relative_to(P).as_posix()+'/';names=[]
for row in git('status','--porcelain','-z','--untracked-files=all').split(b'\0'):
    if not row:continue
    status=row[:2];name=row[3:].decode('utf-8');assert status in [b' M',b'??'],(status,name)
    allowed=name in roots
    if name.startswith(prefix):
        rel=name[len(prefix):];p=Path(rel);allowed|=rel in sources
        allowed|='/' not in rel and 'v69' in p.name and p.suffix in ['.py','.ps1']
        if rel.startswith('evidence/combat-state-v1/'):
            tail=Path(rel).parts[2:];allowed|=len(tail)==1 and p.suffix in ['.json','.c','.h']
            allowed|=len(tail)==2 and tail[0]=='fixtures' and p.suffix.lower() in ['.map','.ini']
    assert allowed and (P/name).is_file() and (P/name).resolve().is_relative_to(P.resolve()),name
    names.append(name)
for start in range(0,len(names),40):git('add','--',*names[start:start+40])
write(S/'git-staging-scope.json',dict(passed=True,selected_files=len(names),allowlist_verified=True,executables_archives_traces_original_assets_excluded=True,remote_actions=False))
git('add','--',(S/'git-staging-scope.json').relative_to(P).as_posix())
q=subprocess.run(['git','-c','core.fsmonitor=false','-c','core.quotepath=false','diff','--cached','--check'],cwd=P,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
output=q.stdout.decode('utf-8',errors='replace');(S/'git-whitespace-check.log').write_text(output,encoding='utf-8')
inherited={sha(O/'native_probe_host.h'):str(O/'native_probe_host.h')};pending=read(S/'scene-pending.json');rules=Path(pending['original_rules']);assert sha(rules)==pending['original_rules_sha256'];rules_lines=rules.read_bytes().splitlines();warnings=[]
for line in output.splitlines():
    m=re.match(r'(.+):(\d+): (.+)',line)
    if not m:continue
    name,number,reason=m[1],int(m[2]),m[3];p=P/name;assert p.exists() and p.is_relative_to(S),(name,reason)
    if sha(p) in inherited:origin=inherited[sha(p)]
    elif p.suffix.lower()=='.map' and p.parent==S/'fixtures' and reason=='new blank line at EOF.':origin='Original map EOF layout retained'
    elif p.suffix.lower()=='.ini' and p.parent==S/'fixtures':
        assert p.read_bytes().splitlines()[number-1] in rules_lines;origin=str(rules)+' (same original rule line; Immune override itself has no whitespace waiver)'
    else:raise AssertionError((name,number,reason))
    warnings.append(dict(path=name,line=number,reason=reason,inherited_source=origin,sha256=sha(p)))
assert q.returncode==0 or warnings,output
write(S/'git-whitespace-audit.json',dict(passed=True,exit_code=q.returncode,warnings=warnings,only_exact_original_bytes_or_map_layout=True))
git('add','--',(S/'git-whitespace-audit.json').relative_to(P).as_posix())
def verify_blobs(items):
    content=subprocess.check_output(['git','-c','core.fsmonitor=false','cat-file','--batch'],cwd=P,input=''.join(':'+n+'\n' for n in items).encode('utf-8'));offset=0
    for name in items:
        end=content.index(b'\n',offset);header=content[offset:end].split();assert len(header)==3 and header[1]==b'blob',(name,header)
        length=int(header[2]);assert content[end+1:end+1+length]==(P/name).read_bytes(),name;offset=end+length+2
    assert offset==len(content)
staged=[x.decode('utf-8') for x in git('diff','--cached','--name-only','-z').split(b'\0') if x]
compiled=[Path(p).relative_to(P).as_posix() for p in read(R/'ra2/build-original-c/source-content-receipt.json')['inputs']];verify_blobs(sorted(set(staged+compiled)))
write(S/'git-byte-audit.json',dict(passed=True,staged_files=len(staged),compiled_inputs=len(compiled),all_index_and_worktree_bytes_equal=True))
git('add','--',(S/'git-byte-audit.json').relative_to(P).as_posix());staged=[x.decode('utf-8') for x in git('diff','--cached','--name-only','-z').split(b'\0') if x];verify_blobs(staged)
for row in git('status','--porcelain','-z','--untracked-files=all').split(b'\0'):
    if row:assert row[:2] in [b'A ',b'M '],row
context=read(S/'vcs-context.json');assert git('rev-parse','HEAD').decode().strip()==context['parent_commit'] and sha(P/'.git/config')==context['config_sha256']
assert hashlib.sha256(git('for-each-ref','--format=%(refname) %(objectname)','refs/remotes/')).hexdigest()==context['remote_refs_sha256']
hook=subprocess.run(['git','config','--get','core.hooksPath'],cwd=P,stdout=subprocess.PIPE,text=True);assert hook.returncode in [0,1]
hooks=Path(hook.stdout.strip()) if hook.returncode==0 else P/'.git/hooks'
if not hooks.is_absolute():hooks=P/hooks
assert not hooks.exists() or not any(p.is_file() and not p.name.endswith('.sample') for p in hooks.iterdir())
git('commit','-m','Extract combat damage admission and health settlement services (batch 68)')
assert not git('status','--porcelain','--untracked-files=all')
subprocess.run(py('verify_combat_v69.py'),cwd=R,check=True)
value=dict(passed=True,commit=git('rev-parse','HEAD').decode().strip(),parent_commit=context['parent_commit'],staged_files=len(staged),all_index_bytes_verified=True,pushed=False)
write(S/'postcommit/git-local-commit.json',value);print(json.dumps(value))
