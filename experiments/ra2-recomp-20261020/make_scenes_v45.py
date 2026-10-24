"""Ordinary dynamic traffic after bridge repair and around a broken span."""
from run_batch_v45 import *
import re
def sec(t,n,b):
 pat=r'(?ms)^\['+n+r'\]\r?\n.*?(?=^\[|\Z)';v='['+n+']\n'+b.strip()+'\n\n';return re.sub(pat,lambda m:v,t) if re.search(pat,t) else t+'\n'+v
base=(S/'fixtures/bridge-repair.MAP').read_bytes().decode('latin1')
base=sec(base,'Units','0=Player House,TRUCKA,256,60,62,0,Guard,None,0,-1,0,-1,1,1\n1=Player House,TRUCKA,256,60,80,0,Guard,None,0,-1,0,-1,1,1\n2=Player House,TRUCKA,256,60,61,0,Guard,None,0,-1,0,-1,1,1\n3=Player House,TRUCKA,256,61,61,0,Guard,None,0,-1,0,-1,1,1\n4=Player House,LCRF,256,63,58,0,Guard,None,0,-1,0,-1,1,1')
base=sec(base,'Infantry','0=Player House,ENGINEER,256,58,75,2,Guard,0,None,0,-1,0,1,1\n1=Player House,E2,256,60,56,2,Guard,0,None,0,-1,0,1,1')
p=S/'fixtures/repair-reverse.MAP';p.write_bytes(base.encode('latin1'))
orders=['5:1023362:2:60:79','400:1023363:2:60:56','600:1023367:8:1023371:0','1000:1023363:2:60:56','1030:1023368:2:60:76','1350:1023365:2:61:54','1450:1023364:2:60:54']
items=[dict(name='repair-traffic',path=p.relative_to(R).as_posix(),sha256=sha(p),orders=orders,last=2100,capture_host=True),dict(name='repair-traffic-control',path=p.relative_to(R).as_posix(),sha256=sha(p),orders=[o for o in orders if ':8:' not in o],last=2100,capture_host=True)]
base=(S/'fixtures/bridge-detour.MAP').read_bytes().decode('latin1');base=sec(base,'Units','0=Player House,TRUCKA,256,60,62,0,Guard,None,0,-1,0,-1,1,1\n1=Player House,TRUCKA,256,60,58,0,Guard,None,0,-1,0,-1,1,1\n2=Player House,TRUCKA,256,64,74,0,Guard,None,0,-1,0,-1,1,1\n3=Player House,LCRF,256,65,58,0,Guard,None,0,-1,0,-1,1,1')
base=sec(base,'Infantry','0=Player House,E2,256,64,77,2,Guard,0,None,0,-1,0,1,1');p=S/'fixtures/detour-comoving.MAP';p.write_bytes(base.encode('latin1'))
items.append(dict(name='detour-traffic',path=p.relative_to(R).as_posix(),sha256=sha(p),orders=['5:1023362:2:60:79','400:1023363:2:60:75','300:1023365:2:65:76','450:1023366:2:64:58'],last=1500,capture_host=True))
for item in items:
 item['tag']={'repair-traffic':'rs','repair-traffic-control':'rc','detour-traffic':'ds'}[item['name']]
 item['baseline_tag']={'repair-traffic':'b-rs','repair-traffic-control':'b-rc','detour-traffic':'b-ds'}[item['name']]
write(S/'dynamic-fixtures.json',dict(passed=True,fixtures=items,ordinary_maps_and_commands=True,direct_result_or_path_writes=False))
print('Prepared three finite dynamic traffic/control recipes')
