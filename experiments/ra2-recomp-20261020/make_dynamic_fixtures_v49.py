"""Finite ordinary-map extension: rough unload, near-collapse damage, reverse ramp."""
from run_batch_v49 import *
from map_codec_v49 import unpack,encode,decode
import re,struct,base64
def section(t,name,body):return re.sub(r'(?ms)^\['+name+r'\]\n.*?(?=^\[|\Z)',lambda m:'['+name+']\n'+body.strip()+'\n\n',t)
def patch(t,changes):
 m,raw=unpack(t);records={struct.unpack_from('<HH',raw,p):p for p in range(0,len(raw)-4,11)};details=[]
 for cell,record in changes.items():
  p=records[cell];before=bytes(raw[p+4:p+11]);raw[p+4:p+11]=record;details.append(dict(cell=list(cell),before=before.hex(),after=record.hex()))
 packed=bytearray()
 for p in range(0,len(raw),8192):
  block=bytes(raw[p:p+8192]);coded=encode(block);assert decode(coded,len(block))==block;packed+=struct.pack('<HH',len(coded),len(block))+coded
 v=base64.b64encode(packed).decode();t=t[:m.start()]+'[IsoMapPack5]\n'+''.join(f'{i//70+1}={v[i:i+70]}\n' for i in range(0,len(v),70))+'\n'+t[m.end():]
 assert unpack(t)[1]==raw
 return t,details
def original_record(cell):
 t=(S/'fixtures/bridge-detour.MAP').read_text(encoding='ascii');_,raw=unpack(t)
 p=next(p for p in range(0,len(raw)-4,11) if struct.unpack_from('<HH',raw,p)==cell)
 return bytes(raw[p+4:p+11])
items=[];patches=[]
# Keep same-height reachable transport corridor; actual cargo landing is checked later.
old=read(O/'dynamic-fixtures.json')['fixtures'][1];t=(R/old['path']).read_text(encoding='ascii')
t,detail=patch(t,{(x,y):original_record((75,21)) for x in range(62,66) for y in range(77,81)})
p=S/'fixtures/collapse-rough.MAP';p.write_bytes(t.encode('ascii'))
items.append(dict(**{k:v for k,v in old.items() if k not in ['tag','baseline_tag','path','sha256','expected_landing_land']},tag='ru',baseline_tag='b-ru',path=p.relative_to(R).as_posix(),sha256=sha(p),expected_landing_land=7))
patches.append(dict(tag='ru',changes=detail,source_cell=[75,21]))
# Victim is on the collapsing bridge, loaded craft waits one adjacent cell away.
t=(S/'fixtures/bridge-detour.MAP').read_text(encoding='ascii')
t=section(t,'Units','0=Player House,LCRF,256,63,79,0,Guard,None,0,-1,0,-1,1,1\n1=Player House,TRUCKA,256,64,79,0,Guard,None,0,-1,0,-1,1,1\n2=Player House,TRUCKA,256,60,62,0,Guard,None,0,-1,0,-1,1,1\n3=Player House,TRUCKA,256,61,66,0,Guard,None,0,-1,0,-1,1,1')
t=section(t,'Infantry','0=Player House,E2,256,65,75,2,Guard,0,None,0,-1,0,1,1')
p=S/'fixtures/collapse-near.MAP';p.write_bytes(t.encode('ascii'))
items.append(dict(tag='nc',baseline_tag='b-nc',path=p.relative_to(R).as_posix(),sha256=sha(p),orders=['50:1023363:7:1023362:0','200:1023362:2:62:66','1000:1023364:2:60:79','1400:1023362:2:63:77','1900:1023362:16:0:0','2100:1023363:2:64:79','500:1023366:2:65:61'],last=2500,capture_host=True))
# East high platform; ramp1 is traversed westward down and eastward up.
t=(O/'fixtures/bridge-slope-es.MAP').read_text(encoding='ascii')
# Start from intact original instead of inheriting the previous west plateau.
t=(S/'fixtures/bridge-intact-06.MAP').read_text(encoding='ascii');changes={}
flat=bytearray(original_record((75,21)));struct.pack_into('<I',flat,0,0);flat[4]=0;flat[5]=5
ramp=bytearray(original_record((51,32)));ramp[5]=4
for x in range(63,70):
 for y in range(52,63):changes[(x,y)]=bytes(ramp if x==63 else flat)
t,detail=patch(t,changes)
t=section(t,'Units','0=Player House,TRUCKA,256,66,58,0,Guard,None,0,-1,0,-1,1,1\n1=Player House,TRUCKA,256,61,76,0,Guard,None,0,-1,0,-1,1,1\n2=Player House,TRUCKA,256,60,74,0,Guard,None,0,-1,0,-1,1,1')
t=section(t,'Infantry','0=Player House,E2,256,61,74,2,Guard,0,None,0,-1,0,1,1')
p=S/'fixtures/bridge-slope-west.MAP';p.write_bytes(t.encode('ascii'))
items.append(dict(tag='ws',baseline_tag='b-ws',path=p.relative_to(R).as_posix(),sha256=sha(p),orders=['5:1023362:2:60:80','60:1023363:2:61:55','75:1023365:2:60:55','450:1023364:2:61:82','900:1023362:2:66:58'],last=1800,capture_host=True,start=[66,58],slope_type=1,source_cell=[51,32]))
patches.append(dict(tag='ws',changes=detail,source_cell=[51,32]))
write(S/'dynamic-fixtures.json',dict(passed=True,fixtures=items,patches=patches,ordinary_maps_and_commands=True,direct_result_or_path_writes=False))
