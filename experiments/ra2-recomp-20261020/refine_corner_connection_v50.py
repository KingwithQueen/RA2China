"""Join the preserved corner8 neighborhood to the bridge using an ordinary lower road."""
from run_batch_v50 import *
from map_codec_v50 import unpack,encode,decode
import struct,base64
p=S/'dynamic-fixtures.json';data=read(p);old=next(x for x in data['fixtures'] if x['tag']=='c8')
write(S/'unconnected-corner-exploration.json',dict(passed=True,recipe=old,strict_trace_passed=True,qualified_corner_height=True,qualified_main_bridge_trip=False,reason='Ordinary transplanted neighborhood had no passable seam from [54,58] to the bridge; both originals hold there after900. Retain as fixture connectivity trial, not an original-game bug.',baseline_comparison_sha256=sha(S/'runs/b-c8/comparison.json'),current_comparison_sha256=sha(S/'runs/c8/comparison.json')))
t=(R/old['path']).read_text(encoding='ascii');m,raw=unpack(t);changes=[]
for q in range(0,len(raw)-4,11):
 x,y=struct.unpack_from('<HH',raw,q)
 if (52<=x<=53 and 56<=y<=62) or (53<=x<=61 and y==62):
  before=bytes(raw[q+4:q+11]);struct.pack_into('<I',raw,q+4,0);raw[q+8]=0;raw[q+9]=4;changes.append(dict(cell=[x,y],before=before.hex(),after=bytes(raw[q+4:q+11]).hex()))
packed=bytearray()
for q in range(0,len(raw),8192):
 block=bytes(raw[q:q+8192]);coded=encode(block);assert decode(coded,len(block))==block;packed+=struct.pack('<HH',len(coded),len(block))+coded
v=base64.b64encode(packed).decode();t=t[:m.start()]+'[IsoMapPack5]\n'+''.join(f'{i//70+1}={v[i:i+70]}\n' for i in range(0,len(v),70))+'\n'+t[m.end():]
q=S/'fixtures/bridge-corner-connected.MAP';q.write_bytes(t.encode('ascii'));assert unpack(t)[1]==raw
item=dict(old,tag='d8',baseline_tag='b-d8',path=q.relative_to(R).as_posix(),sha256=sha(q),connection_changes=changes)
data['fixtures']=[item if x['tag']=='c8' else x for x in data['fixtures']];p.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
wrapper=(R/'run_bridge_catalog_v50.py').read_text(encoding='utf-8').replace('movement-state-v50/bridge-catalog-observer.exe','movement-state-v50/baseline-observer/bridge-catalog-observer.exe');(R/'run_baseline_bridge_v50.py').write_text(wrapper,encoding='utf-8',newline='\n')
