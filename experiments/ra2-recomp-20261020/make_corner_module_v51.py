"""One integration recipe: corner8 module beside an unchanged proven bridge approach."""
from run_batch_v51 import *
from map_codec_v51 import unpack,encode,decode
import re,struct,base64
base=(O/'fixtures/bridge-corner-c6.MAP').read_text(encoding='ascii');m,raw=unpack(base)
_,source=unpack((S/'fixtures/bridge-detour.MAP').read_text(encoding='ascii'));records={struct.unpack_from('<HH',source,p):bytes(source[p+4:p+11]) for p in range(0,len(source)-4,11)}
positions={struct.unpack_from('<HH',raw,p):p for p in range(0,len(raw)-4,11)};before=bytes(raw);changes=[]
for x in range(50,57):
 for y in range(32,39):
  cell=(x+1,y+21);p=positions[cell];value=records[(x,y)];changes.append(dict(source=[x,y],cell=list(cell),before=bytes(raw[p+4:p+11]).hex(),after=value.hex()));raw[p+4:p+11]=value
for y in range(53,60):
 p=positions[(58,y)];value=records[(69,40)];changes.append(dict(source=[69,40],cell=[58,y],before=bytes(raw[p+4:p+11]).hex(),after=value.hex()));raw[p+4:p+11]=value
for (x,y),p in positions.items():
 if 59<=x<=61 and 60<=y<=73:assert raw[p:p+11]==before[p:p+11]
packed=bytearray()
for p in range(0,len(raw),8192):
 block=bytes(raw[p:p+8192]);coded=encode(block);assert decode(coded,len(block))==block;packed+=struct.pack('<HH',len(coded),len(block))+coded
v=base64.b64encode(packed).decode();t=base[:m.start()]+'[IsoMapPack5]\n'+''.join(f'{i//70+1}={v[i:i+70]}\n' for i in range(0,len(v),70))+'\n'+base[m.end():]
t=t.replace('TRUCKA,256,60,56','TRUCKA,256,53,57');p=S/'fixtures/bridge-corner-module.MAP';p.write_bytes(t.encode('ascii'));assert unpack(t)[1]==raw
item=dict(tag='cm',baseline_tag='b-cm',path=p.relative_to(R).as_posix(),sha256=sha(p),orders=['5:1023362:2:54:56','300:1023362:2:55:55','600:1023362:2:57:57','900:1023362:2:60:58','1200:1023362:2:60:80','1300:1023363:2:61:54','1350:1023365:2:61:55','1700:1023364:2:61:82','2300:1023362:2:54:56','3000:1023362:2:55:55'],last=3600,capture_host=True)
write(S/'corner-module-fixtures.json',dict(passed=True,fixtures=[item],changes=changes,proven_bridge_approach_and_span_records_unchanged=True,maximum_new_integration_recipes=1,ordinary_map_and_waypoint_commands=True))
