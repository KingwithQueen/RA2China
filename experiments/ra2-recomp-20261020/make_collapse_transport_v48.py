"""Ordinary bridge trigger while loaded; clear shore and rejected water unload."""
from run_batch_v48 import *
from map_codec_v48 import unpack,encode,decode
import re,struct,base64
t=(S/'fixtures/bridge-detour.MAP').read_bytes().decode('ascii').replace('\r\n','\n')
m,raw=unpack(t);changes=[]
for p in range(0,len(raw)-4,11):
 x,y=struct.unpack_from('<HH',raw,p)
 if 62<=x<=66 and 57<=y<=80:
  before=bytes(raw[p+4:p+11]);struct.pack_into('<I',raw,p+4,0);raw[p+8]=raw[p+9]=0
  changes.append(dict(cell=[x,y],before=before.hex(),after=bytes(raw[p+4:p+11]).hex()))
packed=bytearray()
for p in range(0,len(raw),8192):
 block=bytes(raw[p:p+8192]);coded=encode(block);assert decode(coded,len(block))==block;packed+=struct.pack('<HH',len(coded),len(block))+coded
v=base64.b64encode(packed).decode();t=t[:m.start()]+'[IsoMapPack5]\n'+''.join(f'{i//70+1}={v[i:i+70]}\n' for i in range(0,len(v),70))+'\n'+t[m.end():]
def section(name,body):
 global t
 t=re.sub(r'(?ms)^\['+name+r'\]\n.*?(?=^\[|\Z)',lambda m:'['+name+']\n'+body.strip()+'\n\n',t)
section('Units','0=Player House,LCRF,256,63,79,0,Guard,None,0,-1,0,-1,1,1\n1=Player House,TRUCKA,256,64,79,0,Guard,None,0,-1,0,-1,1,1\n2=Player House,TRUCKA,256,60,62,0,Guard,None,0,-1,0,-1,1,1\n3=Player House,TRUCKA,256,64,63,0,Guard,None,0,-1,0,-1,1,1')
section('Infantry','0=Player House,E2,256,65,75,2,Guard,0,None,0,-1,0,1,1')
p=S/'fixtures/collapse-cargo-shore.MAP';p.write_bytes(t.encode('ascii'));assert unpack(t)[1]==raw
common=['50:1023363:7:1023362:0','300:1023364:2:60:79','500:1023366:2:65:61','1000:1023365:2:64:72']
items=[dict(tag='dc',baseline_tag='b-dc',path=p.relative_to(R).as_posix(),sha256=sha(p),orders=common+['400:1023362:2:63:59','1500:1023362:16:0:0','1700:1023363:2:64:62'],last=2200,capture_host=True),dict(tag='wg',baseline_tag='b-wg',path=p.relative_to(R).as_posix(),sha256=sha(p),orders=common+['400:1023362:2:60:66','1200:1023362:16:0:0','1450:1023362:2:63:59','2000:1023362:16:0:0','2150:1023363:2:64:62'],last=2550,capture_host=True)]
write(S/'collapse-transport-fixtures.json',dict(passed=True,fixtures=items,shore_record_changes=changes,original_bridge_trigger_retained=True,ordinary_maps_and_commands=True,runtime_result_writes=False))
