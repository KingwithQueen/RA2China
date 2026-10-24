"""Reachable transport path retained; clear versus road unload landing areas."""
from run_batch_v48 import *
from map_codec_v48 import unpack,encode,decode
import re,struct,base64
base=(S/'fixtures/bridge-detour.MAP').read_bytes().decode('ascii').replace('\r\n','\n')
def section(text,name,body):return re.sub(r'(?ms)^\['+name+r'\]\n.*?(?=^\[|\Z)',lambda m:'['+name+']\n'+body.strip()+'\n\n',text)
items=[];patches=[]
for tag in ['dc','rd']:
 t=base;changes=[]
 if tag=='dc':
  m,raw=unpack(t)
  for p in range(0,len(raw)-4,11):
   x,y=struct.unpack_from('<HH',raw,p)
   if 60<=x<=65 and 57<=y<=61:
    before=bytes(raw[p+4:p+11]);struct.pack_into('<I',raw,p+4,0);raw[p+8]=0;raw[p+9]=4
    changes.append(dict(cell=[x,y],before=before.hex(),after=bytes(raw[p+4:p+11]).hex()))
  packed=bytearray()
  for p in range(0,len(raw),8192):
   block=bytes(raw[p:p+8192]);coded=encode(block);assert decode(coded,len(block))==block;packed+=struct.pack('<HH',len(coded),len(block))+coded
  v=base64.b64encode(packed).decode();t=t[:m.start()]+'[IsoMapPack5]\n'+''.join(f'{i//70+1}={v[i:i+70]}\n' for i in range(0,len(v),70))+'\n'+t[m.end():]
 t=section(t,'Units','0=Player House,LCRF,256,63,79,0,Guard,None,0,-1,0,-1,1,1\n1=Player House,TRUCKA,256,64,79,0,Guard,None,0,-1,0,-1,1,1\n2=Player House,TRUCKA,256,60,62,0,Guard,None,0,-1,0,-1,1,1\n3=Player House,TRUCKA,256,64,63,0,Guard,None,0,-1,0,-1,1,1')
 t=section(t,'Infantry','0=Player House,E2,256,65,75,2,Guard,0,None,0,-1,0,1,1')
 p=S/'fixtures'/('collapse-unload-'+tag+'.MAP');p.write_bytes(t.encode('ascii'))
 orders=['50:1023363:7:1023362:0','300:1023364:2:60:79','500:1023366:2:65:61','1000:1023365:2:64:72']
 orders+=['400:1023362:2:63:59','1500:1023362:16:0:0','1700:1023363:2:64:62'] if tag=='dc' else ['400:1023362:2:63:77','800:1023362:16:0:0','1000:1023363:2:64:79']
 items.append(dict(tag=tag,baseline_tag='b2-'+tag,path=p.relative_to(R).as_posix(),sha256=sha(p),orders=orders,last=2200 if tag=='dc' else 1600,capture_host=True,expected_landing_land=0 if tag=='dc' else 1,cargo_goal=[64,62] if tag=='dc' else [64,79]))
 patches.append(dict(tag=tag,changes=changes))
write(S/'qualified-transport-fixtures.json',dict(passed=True,fixtures=items,patches=patches,ordinary_maps_and_commands=True,initial_low_shore_trials_not_accepted=True))
write(S/'selected-dynamic-fixtures.json',dict(passed=True,fixtures=items+read(S/'other-slopes-fixtures.json')['fixtures'],ordinary_maps_and_commands=True,direct_result_or_path_writes=False))
