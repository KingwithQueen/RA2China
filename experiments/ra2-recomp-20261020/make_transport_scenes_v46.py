"""Ordinary Enter/Move/Unload inputs; no production rules or result mutation."""
from run_batch_v46 import *
import re
def section(text,name,body):
 pattern=r'(?ms)^\['+name+r'\]\r?\n.*?(?=^\[|\Z)'
 return re.sub(pattern,lambda m:'['+name+']\n'+body.strip()+'\n\n',text)
t=(S/'fixtures/bridge-intact-06.MAP').read_bytes().decode('latin1')
t=section(t,'Units','0=Player House,FV,256,60,58,0,Guard,None,0,-1,0,-1,1,1\n1=Player House,TRUCKA,256,60,76,0,Guard,None,0,-1,0,-1,1,1')
t=section(t,'Infantry','0=Player House,E2,256,60,57,2,Guard,0,None,0,-1,0,1,1\n1=Player House,E2,256,61,79,2,Guard,0,None,0,-1,0,1,1')
p=S/'fixtures/ifv-bridge.MAP';p.write_bytes(t.encode('latin1'))
orders=['50:1023364:7:1023362:0','400:1023362:2:60:80','450:1023365:2:61:56','800:1023363:2:61:84','1200:1023362:16:0:0','1450:1023364:2:62:82']
items=[dict(tag='tr',baseline_tag='b-tr',path=p.relative_to(R).as_posix(),sha256=sha(p),orders=orders,last=1900,capture_host=True),dict(tag='tc',baseline_tag='b-tc',path=p.relative_to(R).as_posix(),sha256=sha(p),orders=[o for o in orders if ':16:' not in o and not o.startswith('1450:')],last=1900,capture_host=True)]
# A proven moving Hover route with a new traffic phase, independent of transport mechanics.
p=S/'fixtures/hover-traffic.MAP';shutil.copy2(O/'fixtures/detour-mixed3.MAP',p)
items.append(dict(tag='hv',baseline_tag='b-hv',path=p.relative_to(R).as_posix(),sha256=sha(p),orders=['5:1023362:2:60:79','400:1023363:2:60:75','300:1023365:2:63:59','450:1023366:2:64:58'],last=1500,capture_host=True))
write(S/'dynamic-fixtures.json',dict(passed=True,fixtures=items,ordinary_maps_and_commands=True,direct_result_or_path_writes=False))
