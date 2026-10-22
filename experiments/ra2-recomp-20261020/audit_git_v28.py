"""Validate staged scope and byte-preserving inherited recipe whitespace."""
from pathlib import Path
import json,re,subprocess
R=Path(__file__).resolve().parent;P=R.parent.parent;S=R/'evidence/movement-state-v28'
run=lambda *args:subprocess.check_output(['git',*args],cwd=P)
names=[n.decode('utf-8') for n in run('diff','--cached','--name-only','-z').split(b'\0') if n]
allowed={'README.md','reports/latest-recovery.json','reports/latest-state-comparison.json','reports/latest-movement-candidate.json',
         '交接文档-原版逆向与C重编译-20261020.txt','交接文档-新对话继续推进-20261022.txt',
         '交接文档-单位移动第二十七批正式验收-20261023.txt','docs/单位移动第二十七批-桥层模板与类别过滤及共享出口-20261023.txt'}
prefix=R.relative_to(P).as_posix()+'/'
for name in names:
    assert name in allowed or name.startswith(prefix),name
    assert not any('/'+part+'/' in '/'+name for part in ['baseline','parts','final-source','runs','work','build-original-c','investigations']),name
    p=P/name
    assert p.is_file() and p.suffix.lower() not in ['.exe','.dll','.obj','.pdb','.sav','.mix','.bag','.zip'] and p.stat().st_size<50*1024*1024,name
check=subprocess.run(['git','diff','--cached','--check'],cwd=P,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
inherited=[]
for line in check.stdout.decode('utf-8').splitlines():
    m=re.match(r'^(.*?):(\d+): (trailing whitespace|new blank line at EOF|space before tab in indent)\.?$',line)
    if not m:continue
    name,number,kind=m[1],int(m[2]),m[3]
    p=P/name;prior=P/name.replace('v28','v27')
    assert prior!=p and prior.is_file(),('New whitespace defect',line)
    current=p.read_text(encoding='utf-8').splitlines();old=prior.read_text(encoding='utf-8').splitlines()
    content=current[number-1]
    if kind=='new blank line at EOF':assert not content and not old[-1]
    else:assert content.replace('v28','v27') in old,('Changed inherited whitespace',line)
    if name not in inherited:inherited.append(name)
strict=['git','diff','--cached','--check','--','.']+[':(exclude)'+n for n in inherited]
result=subprocess.run(strict,cwd=P,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
assert result.returncode==0,result.stdout.decode('utf-8')
value=dict(passed=True,staged_files=len(names),staged_bytes=sum((P/n).stat().st_size for n in names),scope_verified=True,
           binary_assets_excluded=True,new_source_and_docs_whitespace_clean=True,inherited_files_preserved=inherited)
(S/'git-whitespace-audit.json').write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in value.items() if k!='inherited_files_preserved'}))
