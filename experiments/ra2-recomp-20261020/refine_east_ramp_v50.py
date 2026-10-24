"""Add an original east-facing grade transition, then allow bounded travel time."""
from run_batch_v50 import *
from map_codec_v50 import unpack,encode,decode
import struct,base64
p=S/'dynamic-fixtures.json';data=read(p);old=next(x for x in data['fixtures'] if x['tag']=='d8')
write(S/'lower-road-corner-exploration.json',dict(passed=True,recipe=old,strict_trace_passed=True,qualified_main_bridge_trip=False,baseline_sha256=sha(S/'runs/b-d8/comparison.json'),current_sha256=sha(S/'runs/d8/comparison.json'),scope='Added lower connection alone did not yield bridge travel; both modes retained. No original-game bug attribution.'))
t=(R/old['path']).read_text(encoding='ascii');m,raw=unpack(t);_,source=unpack((S/'fixtures/bridge-detour.MAP').read_text(encoding='ascii'));q=next(q for q in range(0,len(source)-4,11) if struct.unpack_from('<HH',source,q)==(69,40));ramp=bytes(source[q+4:q+11]);assert ramp[5]==4;changes=[]
for q in range(0,len(raw)-4,11):
 x,y=struct.unpack_from('<HH',raw,q)
 if x==61 and 54<=y<=60:
  changes.append(dict(cell=[x,y],before=bytes(raw[q+4:q+11]).hex(),after=ramp.hex()));raw[q+4:q+11]=ramp
packed=bytearray()
for q in range(0,len(raw),8192):
 block=bytes(raw[q:q+8192]);coded=encode(block);assert decode(coded,len(block))==block;packed+=struct.pack('<HH',len(coded),len(block))+coded
v=base64.b64encode(packed).decode();t=t[:m.start()]+'[IsoMapPack5]\n'+''.join(f'{i//70+1}={v[i:i+70]}\n' for i in range(0,len(v),70))+'\n'+t[m.end():]
q=S/'fixtures/bridge-corner-east-ramp.MAP';q.write_bytes(t.encode('ascii'));assert unpack(t)[1]==raw
item=dict(old,tag='e8',baseline_tag='b-e8',path=q.relative_to(R).as_posix(),sha256=sha(q),last=2800,orders=[x.replace('1700:1023362','1900:1023362') for x in old['orders']],east_transition=changes)
data['fixtures']=[item if x['tag']=='d8' else x for x in data['fixtures']];p.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
q=S/'unconnected-corner-exploration.json';x=read(q);x['reason']='Both modes held after900 and did not form main bridge travel; retained as an unqualified authored transition trial, with no original-game bug attribution.';q.write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8')
