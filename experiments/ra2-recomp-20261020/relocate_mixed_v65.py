"""Compose a short ordinary bridge/Tube route; preserve the long failed candidate and all bridge cells."""
from run_batch_v65 import *
from map_codec_v65 import unpack,encode,decode
import re,struct,base64
def block(t,k):return re.search(rf'(?ms)^\[{k}\]\n(.*?)(?=^\[|\Z)',t)
def replace(t,k,raw,codec):
 data=bytearray()
 for i in range(0,len(raw),8192):
  part=bytes(raw[i:i+8192]);packed=codec(part);data+=struct.pack('<HH',len(packed),len(part))+packed
 value=base64.b64encode(data).decode();body=''.join(f'{i//70+1}={value[i:i+70]}\n' for i in range(0,len(value),70))+'\n'
 m=block(t,k);assert m;return t[:m.start(1)]+body+t[m.end(1):]
def lcw(data,size):
 p=0;out=bytearray();relative=data[0]==0
 if relative:p=1
 while p<len(data):
  v=data[p];p+=1
  if v<128:
   n=(v>>4)+3;distance=((v&15)<<8)+data[p];p+=1
  elif v<192:
   n=v&63
   if not n:assert p==len(data) and len(out)==size;return bytes(out)
   out+=data[p:p+n];p+=n;assert len(out)<=size;continue
  elif v==254:
   n=struct.unpack_from('<H',data,p)[0];c=data[p+2];p+=3;out+=bytes([c])*n;assert len(out)<=size;continue
  else:
   n=(v&63)+3
   if v==255:n=struct.unpack_from('<H',data,p)[0];p+=2
   source=struct.unpack_from('<H',data,p)[0];p+=2;distance=source if relative else len(out)-source
  assert 0<distance<=len(out) and len(out)+n<=size
  for _ in range(n):out.append(out[-distance])
 raise AssertionError('LCW terminator missing')
def literal(data):
 out=bytearray();p=0
 def run(i):
  n=1
  while i+n<len(data) and data[i+n]==data[i] and n<65535:n+=1
  return n
 while p<len(data):
  n=run(p)
  if n>=4:
   out.append(254);out+=struct.pack('<H',n);out.append(data[p]);p+=n
  else:
   start=p;p+=n
   while p<len(data) and p-start<63:
    n=run(p)
    if n>=4:break
    p+=min(n,63-(p-start))
   out.append(128+p-start);out+=data[start:p]
 out.append(128);out=bytes(out);assert lcw(out,len(data))==data and len(out)<=len(data);return out
def overlay(t,k):
 m=block(t,k)
 if m is None:return bytearray([255 if k=='OverlayPack' else 0])*(512*512)
 raw=base64.b64decode(''.join(l.split('=',1)[1] for l in m[1].splitlines() if '=' in l));p=0;out=bytearray()
 while p<len(raw):
  n,size=struct.unpack_from('<HH',raw,p);p+=4;out+=lcw(raw[p:p+n],size);p+=n
 assert p==len(raw) and len(out)==512*512;return out
bridge=R/'evidence/movement-state-v38/fixtures/bridge-chain-lower-west.MAP';tube=R/'evidence/movement-state-v38/fixtures/tube-curved-east.MAP'
t=bridge.read_text(encoding='ascii');source=tube.read_text(encoding='ascii');m,raw=unpack(t);original=bytes(raw);_,donor=unpack(source)
index={struct.unpack_from('<HH',raw,i):i for i in range(0,len(raw)-4,11)};changes=[];dx=-8;dy=-38
for i in range(0,len(donor)-4,11):
 x,y=struct.unpack_from('<HH',donor,i)
 if 64<=x<=84 and 110<=y<=118:
  target=(x+dx,y+dy);j=index[target];changes.append(dict(cell=list(target),before=bytes(raw[j+4:j+11]).hex(),after=bytes(donor[i+4:i+11]).hex()));raw[j+4:j+11]=donor[i+4:i+11]
assert len(changes)==189 and all(y>=72 for x,y in [c['cell'] for c in changes])
t=replace(t,'IsoMapPack5',raw,encode);assert unpack(t)[1]==raw
overlay_changes={}
for key in ['OverlayPack','OverlayDataPack']:
 a=overlay(t,key);before=bytes(a);b=overlay(source,key);changed=[];targets=set()
 for y in range(110,119):
  for x in range(64,85):
   j=(y+dy)*512+x+dx;targets.add(j);changed.append([x+dx,y+dy,a[j],b[y*512+x]]);a[j]=b[y*512+x]
 assert all(before[i]==a[i] for i in range(len(a)) if i not in targets)
 assert all(before[y*512+x]==a[y*512+x] for x in range(58,62) for y in range(63,71))
 t=replace(t,key,a,literal);assert overlay(t,key)==a;overlay_changes[key]=changed
def section(t,k,value):
 pattern=rf'(?ms)^\[{k}\]\n.*?(?=^\[|\Z)';v='['+k+']\n'+value+'\n';return re.sub(pattern,lambda _:v,t) if re.search(pattern,t) else t+'\n'+v
records=[]
for l in block(source,'Tubes')[1].splitlines():
 if not l.strip():continue
 key,values=l.split('=');v=list(map(int,values.split(',')));v[0]+=dx;v[1]+=dy;v[3]+=dx;v[4]+=dy;records.append(key+'='+','.join(map(str,v)))
t=section(t,'Tubes','\n'.join(records)+'\n');t=section(t,'Units',''.join(f'{i}=Player House,TRUCKA,256,{x},{y},0,Guard,None,0,-1,0,-1,1,1\n' for i,(x,y) in enumerate([(60,61),(61,60),(60,59),(61,58)])));t=section(t,'Infantry','')
p=S/'fixtures/traffic-m3.MAP';assert not p.exists();p.write_text(t,encoding='ascii',newline='\n')
write(S/'mixed-relocation-rle.json',dict(passed=True,path=p.relative_to(R).as_posix(),sha256=sha(p),source=str(bridge),source_sha256=sha(bridge),donor=str(tube),donor_sha256=sha(tube),translation=[dx,dy],tube_endpoints=[[60,76],[70,76]],tile_changes=changes,overlay_changes=overlay_changes,original_bridge_unchanged=True,roundtrip_codecs_verified=True,rules_or_resources_changed=False,ordinary_map_only=True,old_failed_map_retained=str(S/'fixtures/traffic-m.MAP')))
print(dict(passed=True,new_map=str(p),cells=len(changes),bridge_unchanged=True))
