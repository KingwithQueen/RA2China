"""Transplant complete original corner neighborhoods; no runtime height/path writes."""
from run_batch_v50 import *
from map_codec_v50 import unpack,encode,decode
import re,struct,base64
base=(S/'fixtures/bridge-intact-06.MAP').read_text(encoding='ascii')
original=(S/'fixtures/bridge-detour.MAP').read_text(encoding='ascii');_,source=unpack(original)
records={struct.unpack_from('<HH',source,p):bytes(source[p+4:p+11]) for p in range(0,len(source)-4,11)}
def section(t,name,body):return re.sub(r'(?ms)^\['+name+r'\]\n.*?(?=^\[|\Z)',lambda m:'['+name+']\n'+body.strip()+'\n\n',t)
items=[];patches=[]
for tag,source_low,source_high,delta,start,orders,last in [
 ('c6',(65,28),(72,34),(-12,26),(60,56),['5:1023362:2:57:57','300:1023362:2:55:58','600:1023362:2:60:80','1300:1023362:2:57:57','1600:1023362:2:60:56'],2000),
 ('c8',(50,32),(56,38),(4,22),(56,58),['5:1023362:2:57:57','300:1023362:2:58:56','600:1023362:2:54:58','900:1023362:2:60:80','1700:1023362:2:58:56'],2400)]:
 m,raw=unpack(base);targets={struct.unpack_from('<HH',raw,p):p for p in range(0,len(raw)-4,11)};details=[]
 for x in range(source_low[0],source_high[0]+1):
  for y in range(source_low[1],source_high[1]+1):
   target=(x+delta[0],y+delta[1]);p=targets[target];before=bytes(raw[p+4:p+11]);raw[p+4:p+11]=records[(x,y)];details.append(dict(source=[x,y],cell=list(target),before=before.hex(),after=records[(x,y)].hex()))
 packed=bytearray()
 for p in range(0,len(raw),8192):
  block=bytes(raw[p:p+8192]);coded=encode(block);assert decode(coded,len(block))==block;packed+=struct.pack('<HH',len(coded),len(block))+coded
 v=base64.b64encode(packed).decode();t=base[:m.start()]+'[IsoMapPack5]\n'+''.join(f'{i//70+1}={v[i:i+70]}\n' for i in range(0,len(v),70))+'\n'+base[m.end():]
 t=section(t,'Units',f'0=Player House,TRUCKA,256,{start[0]},{start[1]},0,Guard,None,0,-1,0,-1,1,1\n1=Player House,TRUCKA,256,61,76,0,Guard,None,0,-1,0,-1,1,1\n2=Player House,TRUCKA,256,60,74,0,Guard,None,0,-1,0,-1,1,1')
 t=section(t,'Infantry','0=Player House,E2,256,61,74,2,Guard,0,None,0,-1,0,1,1')
 p=S/'fixtures'/('bridge-corner-'+tag+'.MAP');p.write_bytes(t.encode('ascii'));assert unpack(t)[1]==raw
 orders+=['60:1023363:2:61:54','75:1023365:2:61:55','450:1023364:2:61:82']
 items.append(dict(tag=tag,baseline_tag='b-'+tag,path=p.relative_to(R).as_posix(),sha256=sha(p),orders=orders,last=last,capture_host=True,slope_type=6 if tag=='c6' else 8,corner_cell=[57,57],start=list(start)))
 patches.append(dict(tag=tag,changes=details))
write(S/'corner-fixtures.json',dict(passed=True,fixtures=items,patches=patches,ordinary_original_neighborhood_records=True,runtime_height_or_path_writes=False))
