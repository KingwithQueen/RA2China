"""Normal vehicle Enter/Unload using the previously verified destination payload."""
from run_batch_v47 import *
import re
def section(text,name,body):
 pat=r'(?ms)^\['+name+r'\]\r?\n.*?(?=^\[|\Z)'
 return re.sub(pat,lambda m:'['+name+']\n'+body.strip()+'\n\n',text)
t=(S/'fixtures/bridge-detour.MAP').read_bytes().decode('latin1')
t=section(t,'Units','0=Player House,LCRF,256,63,79,0,Guard,None,0,-1,0,-1,1,1\n1=Player House,TRUCKA,256,64,79,0,Guard,None,0,-1,0,-1,1,1\n2=Player House,TRUCKA,256,64,62,0,Guard,None,0,-1,0,-1,1,1')
t=section(t,'Infantry','0=Player House,E2,256,65,75,2,Guard,0,None,0,-1,0,1,1')
p=S/'fixtures/vehicle-cargo.MAP';p.write_bytes(t.encode('latin1'))
orders=['50:1023363:7:1023362:0','400:1023362:2:63:59','500:1023364:2:64:73','500:1023365:2:65:61','1200:1023362:16:0:0','1450:1023363:2:63:64']
items=[dict(tag='vc',baseline_tag='b-vc',path=p.relative_to(R).as_posix(),sha256=sha(p),orders=orders,last=1900,capture_host=True),dict(tag='cc',baseline_tag='b-cc',path=p.relative_to(R).as_posix(),sha256=sha(p),orders=[o for o in orders if ':16:' not in o and not o.startswith('1450:')],last=1900,capture_host=True)]
write(S/'vehicle-cargo-fixtures.json',dict(passed=True,fixtures=items,ordinary_map_and_commands=True))
