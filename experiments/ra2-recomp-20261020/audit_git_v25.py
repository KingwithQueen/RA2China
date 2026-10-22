"""Audit the concrete local index without changing accepted source bytes."""
from pathlib import Path
import json,re,subprocess,sys
R=Path(__file__).resolve().parent;P=R.parent.parent;S=R/'evidence/movement-state-v25'
run=lambda *args:subprocess.check_output(['git',*args],cwd=P)
names=[n.decode('utf-8') for n in run('diff','--cached','--name-only','-z').split(b'\0') if n]
allowed={'README.md','reports/latest-recovery.json','reports/latest-state-comparison.json','reports/latest-movement-candidate.json','交接文档-原版逆向与C重编译-20261020.txt','交接文档-单位移动第二十四批正式验收-20261022.txt','docs/单位移动第二十四批-隧道入口与水平接续及内部模板-20261022.txt'}
prefix=R.relative_to(P).as_posix()+'/'
for name in names:
 assert name in allowed or name.startswith(prefix),name
 assert not any('/'+part+'/' in '/'+name for part in ['baseline','parts','final-source','runs','work','build-original-c']),name
 path=P/name;assert path.is_file() and path.suffix.lower() not in ['.exe','.dll','.obj','.pdb','.sav','.mix','.bag','.zip'] and path.stat().st_size<50*1024*1024,name
check=subprocess.run(['git','diff','--cached','--check'],cwd=P,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
inherited=[]
for line in check.stdout.decode('utf-8').splitlines():
 m=re.match(r'^(.*?):\d+: (?:trailing whitespace|new blank line at EOF|space before tab in indent)\.?$',line)
 if not m:continue
 name=m[1];path=P/name;prior=P/name.replace('v25','v24')
 assert prior!=path and prior.is_file() and path.read_bytes().replace(b'v25',b'v24')==prior.read_bytes(),('New whitespace defect',line)
 if name not in inherited:inherited.append(name)
strict=['git','diff','--cached','--check','--','.']+[':(exclude)'+n for n in inherited]
result=subprocess.run(strict,cwd=P,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
assert result.returncode==0,result.stdout.decode('utf-8')
receipt=dict(passed=True,staged_files=len(names),staged_bytes=sum((P/n).stat().st_size for n in names),scope_verified=True,binary_assets_excluded=True,new_source_and_docs_whitespace_clean=True,inherited_files_preserved=inherited)
(S/'git-whitespace-audit.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in receipt.items() if k!='inherited_files_preserved'}))
