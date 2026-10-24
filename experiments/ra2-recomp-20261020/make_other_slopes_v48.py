"""Different original slope types/directions as ordinary map records, with bridge traffic."""
from run_batch_v48 import *
from map_codec_v48 import unpack,encode,decode
import base64,re,struct
base=(S/'fixtures/bridge-intact-06.MAP').read_bytes().decode('ascii').replace('\r\n','\n')
catalog=read(O/'runs/b-vc/original/cells.json');observed={tuple(q['cell']):q for q in catalog['cells']}
assert observed[(54,44)]['slope']==2 and observed[(69,40)]['slope']==3
def section(text,name,body):return re.sub(r'(?ms)^\['+name+r'\]\n.*?(?=^\[|\Z)',lambda m:'['+name+']\n'+body.strip()+'\n\n',text)
items=[];patches=[]
for tag,source in [('ss',(54,44)),('es',(69,40))]:
 m,raw=unpack(base);records={struct.unpack_from('<HH',raw,p):p for p in range(0,len(raw)-4,11)};q=records[source];ramp=bytes(raw[q+4:q+11]);changes=[]
 for (x,y),p in records.items():
  plateau=(55<=x<=66 and 74<=y<=84) if tag=='ss' else (51<=x<=56 and 52<=y<=62)
  slope=(55<=x<=66 and y==73) if tag=='ss' else (x==57 and 52<=y<=62)
  if plateau or slope:
   before=bytes(raw[p+4:p+11])
   if slope:raw[p+4:p+11]=ramp;raw[p+9]=4
   else:struct.pack_into('<I',raw,p+4,0);raw[p+8]=0;raw[p+9]=5
   changes.append(dict(cell=[x,y],before=before.hex(),after=bytes(raw[p+4:p+11]).hex()))
 packed=bytearray()
 for p in range(0,len(raw),8192):
  block=bytes(raw[p:p+8192]);coded=encode(block);assert decode(coded,len(block))==block;packed+=struct.pack('<HH',len(coded),len(block))+coded
 v=base64.b64encode(packed).decode();t=base[:m.start()]+'[IsoMapPack5]\n'+''.join(f'{i//70+1}={v[i:i+70]}\n' for i in range(0,len(v),70))+'\n'+base[m.end():]
 start=[60,56] if tag=='ss' else [54,58]
 t=section(t,'Units',f'0=Player House,TRUCKA,256,{start[0]},{start[1]},0,Guard,None,0,-1,0,-1,1,1\n1=Player House,TRUCKA,256,61,76,0,Guard,None,0,-1,0,-1,1,1\n2=Player House,TRUCKA,256,60,74,0,Guard,None,0,-1,0,-1,1,1')
 t=section(t,'Infantry','0=Player House,E2,256,61,74,2,Guard,0,None,0,-1,0,1,1')
 p=S/'fixtures'/('bridge-slope-'+tag+'.MAP');p.write_bytes(t.encode('ascii'));assert unpack(t)[1]==raw
 item=dict(tag=tag,baseline_tag='b-'+tag,path=p.relative_to(R).as_posix(),sha256=sha(p),orders=['5:1023362:2:60:80','60:1023363:2:61:55','75:1023365:2:60:55','450:1023364:2:61:82',f'900:1023362:2:{start[0]}:{start[1]}'],last=1800,capture_host=True,start=start,slope_type=2 if tag=='ss' else 3,source_cell=list(source))
 items.append(item);patches.append(dict(tag=tag,changes=changes))
write(S/'other-slopes-fixtures.json',dict(passed=True,fixtures=items,patches=patches,original_ramp_catalog=str(O/'runs/b-vc/original/cells.json'),original_ramp_catalog_sha256=sha(O/'runs/b-vc/original/cells.json'),ordinary_map_records=True,runtime_result_writes=False))
write(S/'dynamic-fixtures.json',dict(passed=True,fixtures=read(S/'collapse-transport-fixtures.json')['fixtures']+items,ordinary_maps_and_commands=True,direct_result_or_path_writes=False))
