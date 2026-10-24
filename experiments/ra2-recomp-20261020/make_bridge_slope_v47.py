"""Reuse an observed original ramp row as the northern bridge approach, via map records only."""
from run_batch_v47 import *
from map_codec_v47 import unpack,encode,decode
import base64,re,struct
t=(S/'fixtures/bridge-intact-06.MAP').read_bytes().decode('ascii').replace('\r\n','\n')
m,raw=unpack(t);records={struct.unpack_from('<HH',raw,p):p for p in range(0,len(raw)-4,11)}
catalog=read(S/'runs/b-vc/original/cells.json');observed={tuple(q['cell']):q for q in catalog['cells']}
assert observed[(60,48)]['slope']==4 and observed[(60,48)]['level']==4
changes=[]
for (x,y),p in records.items():
 if 55<=x<=66 and 51<=y<=60:
  before=bytes(raw[p+4:p+11]);struct.pack_into('<I',raw,p+4,0);raw[p+8]=0;raw[p+9]=5
  changes.append(dict(cell=[x,y],before=before.hex(),after=bytes(raw[p+4:p+11]).hex()))
 elif 55<=x<=66 and y==61:
  q=records[(x,48)];before=bytes(raw[p+4:p+11]);raw[p+4:p+11]=raw[q+4:q+11]
  changes.append(dict(cell=[x,y],source_cell=[x,48],before=before.hex(),after=bytes(raw[p+4:p+11]).hex()))
packed=bytearray()
for p in range(0,len(raw),8192):
 block=bytes(raw[p:p+8192]);coded=encode(block);assert decode(coded,len(block))==block;packed+=struct.pack('<HH',len(coded),len(block))+coded
value=base64.b64encode(packed).decode('ascii');t=t[:m.start()]+'[IsoMapPack5]\n'+''.join(f'{i//70+1}={value[i:i+70]}\n' for i in range(0,len(value),70))+'\n'+t[m.end():]
def section(name,body):
 global t
 t=re.sub(r'(?ms)^\['+name+r'\]\n.*?(?=^\[|\Z)',lambda m:'['+name+']\n'+body.strip()+'\n\n',t)
section('Units','0=Player House,TRUCKA,256,60,56,0,Guard,None,0,-1,0,-1,1,1\n1=Player House,TRUCKA,256,61,76,0,Guard,None,0,-1,0,-1,1,1\n2=Player House,TRUCKA,256,60,74,0,Guard,None,0,-1,0,-1,1,1')
section('Infantry','0=Player House,E2,256,61,74,2,Guard,0,None,0,-1,0,1,1')
p=S/'fixtures/bridge-slope.MAP';p.write_bytes(t.encode('ascii'));_,back=unpack(t);assert back==raw
item=dict(tag='sr',baseline_tag='b-sr',path=p.relative_to(R).as_posix(),sha256=sha(p),orders=['5:1023362:2:60:80','60:1023363:2:61:55','75:1023365:2:60:55','450:1023364:2:61:82','900:1023362:2:60:56'],last=1600,capture_host=True)
write(S/'slope-bridge-fixtures.json',dict(passed=True,fixtures=[item],ordinary_map_records=True,runtime_state_writes=False,ramp_source_catalog_sha256=sha(S/'runs/b-vc/original/cells.json'),changes=changes))
items=read(S/'vehicle-cargo-fixtures.json')['fixtures']+[item]
write(S/'dynamic-fixtures.json',dict(passed=True,fixtures=items,ordinary_maps_and_commands=True,direct_result_or_path_writes=False))
