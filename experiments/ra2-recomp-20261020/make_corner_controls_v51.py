"""Two bounded ordinary-command controls; the inherited corner8 map bytes stay intact."""
from run_batch_v51 import *
import re
source=O/'fixtures/bridge-corner-east-ramp.MAP';base=source.read_text(encoding='ascii')
traffic=['60:1023363:2:61:54','75:1023365:2:61:55','450:1023364:2:61:82'];items=[]
for tag,orders,last in [('cf',['5:1023362:2:60:80','900:1023362:2:54:58'],1500),('cs',['5:1023362:2:57:57','300:1023362:2:58:56','600:1023362:2:54:58','900:1023362:2:60:58','1200:1023362:2:62:58','1500:1023362:2:60:80','2400:1023362:2:58:56'],3200)]:
 t=base.replace('TRUCKA,256,56,58','TRUCKA,256,54,58') if tag=='cf' else base
 p=S/'fixtures'/('corner8-control-'+tag+'.MAP');p.write_bytes(t.encode('ascii'))
 items.append(dict(tag=tag,baseline_tag='b-'+tag,path=p.relative_to(R).as_posix(),sha256=sha(p),orders=orders+traffic,last=last,capture_host=True,scope='Fresh lower-road departure' if tag=='cf' else 'Arrival history then ordinary high/low waypoints and bridge target'))
write(S/'corner-control-fixtures.json',dict(passed=True,fixtures=items,parent_map_sha256=sha(source),ordinary_initial_positions_and_commands=True,runtime_state_or_path_injection=False,maximum_new_control_recipes=2))
