"""Ordinary map placements and complete independent rules; no runtime state injection."""
from pathlib import Path
import hashlib,json,re
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v41';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
source=Path('H:/开发/研究资料/提取/原版/ra2.mix_files/local.mix_files/rules.ini');raw=source.read_bytes();rules=raw.decode('latin1')
def section(text,name,body):
 pattern=r'(?ms)^\['+re.escape(name)+r'\]\r?\n.*?(?=^\[|\Z)';assert len(re.findall(pattern,text))==1
 return re.sub(pattern,lambda m:'['+name+']\n'+body.strip()+'\n\n',text)
def flags(text,name,values):
 pattern=r'(?ms)^\['+name+r'\]\r?\n.*?(?=^\[|\Z)';m=re.search(pattern,text);assert m;body=m[0]
 for key,value in values.items():
  keypat=r'(?mi)^'+key+r'\s*=.*$'
  if re.search(keypat,body):body=re.sub(keypat,key+'='+value,body)
  else:body=body.rstrip()+'\n'+key+'='+value+'\n'
 return text[:m.start()]+body+text[m.end():]
base=(S/'fixtures/bridge-cross-release-north.MAP').read_bytes().decode('latin1')
items=[]
for kind in ['train','crush']:
 if kind=='train':
  text=section(base,'Units','0=Player House,TRUCKA,256,60,62,0,Guard,None,0,-1,0,-1,1,1\n1=Player House,TRUCKB,256,60,66,0,Guard,None,0,-1,0,-1,1,1\n2=Player House,TRUCKB,256,60,66,0,Guard,None,0,-1,0,-1,1,1')
  text=section(text,'Infantry','0=Player House,E2,256,60,66,2,Sleep,0,None,0,-1,0,1,1')
  values={'IsTrain':'yes','Crusher':'no'};orders=['5:1023362:2:60:75']
 else:
  text=section(base,'Units','0=Player House,TRUCKA,256,60,62,0,Guard,None,0,-1,0,-1,1,1\n1=Player House,TRUCKB,256,61,66,0,Guard,None,0,-1,1,-1,1,1\n2=Player House,TRUCKB,256,60,66,0,Guard,None,0,-1,1,-1,1,1')
  text=section(text,'Infantry','0=BadGuy1 House,E2,256,60,66,2,Sleep,0,None,0,-1,0,1,1\n1=BadGuy1 House,E2,256,60,66,4,Sleep,0,None,0,-1,0,1,1')
  values={'IsTrain':'no','Crusher':'yes'};orders=['1:1023364:2:60:70','1:1023363:2:61:70','5:1023362:2:60:75','300:1023364:2:60:79','210:1023363:2:61:79']
 p=S/'fixtures'/('bridge-'+kind+'-contact.MAP');p.write_bytes(text.encode('latin1'))
 rule=flags(rules,'TRUCKA',values);rule=flags(rule,'TRUCKB',{'Crewed':'no','Crushable':'no'})
 q=S/'fixtures'/('rules-'+kind+'-contact.ini');q.write_bytes(rule.encode('latin1'))
 items.append(dict(name=kind,path=p.relative_to(R).as_posix(),sha256=sha(p),rules=q.relative_to(R).as_posix(),rules_sha256=sha(q),orders=orders,actor=1023362,targets=[1023363,1023364] if kind=='train' else [1023365,1023366],ordinary_map_rules_orders=True,runtime_state_injection=False))
(S/'collision-fixtures.json').write_text(json.dumps(dict(passed=True,fixtures=items,original_rules_source=str(source),original_rules_sha256=sha(source),rules_flag_binding='IsTrain is read at native 006DB049 and stored at type+AA0; no field is directly written by this recipe.'),indent=2)+'\n',encoding='utf-8')
print(dict(passed=True,fixtures=2,original_rules_sha256=sha(source)))
