"""Legal IsoMapPack5 fixtures: change map heights, never raw runtime movement state.
Codec follows the existing read-only src/map_pack.c LZO1X decoder and 11-byte cells.
The encoder uses literal-only LZO blocks so its output is easy to audit.
"""
from pathlib import Path
import base64,hashlib,json,re,struct
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v26'
def decode(data,size):
 p=0;out=bytearray();state=0
 def literal(n):
  nonlocal p
  assert p+n<=len(data) and len(out)+n<=size
  out.extend(data[p:p+n]);p+=n
 def length(n,mask):
  nonlocal p
  if n:return n
  n=mask
  while data[p]==0:n+=255;p+=1
  n+=data[p];p+=1;return n
 if data[0]>17:
  n=data[p]-17;p+=1;literal(n);state=n if n<4 else 4
 while p<len(data):
  token=data[p];p+=1
  if token<16 and state==0:
   n=length(token,15);literal(n+3);state=4;continue
  if token<16:
   distance=1+(token>>2)+(data[p]<<2)+(2048 if state==4 else 0);p+=1;n=3 if state==4 else 2;tail=token&3
  elif token>=64:
   distance=1+((token>>2)&7)+(data[p]<<3);p+=1;n=(token>>5)+1;tail=token&3
  else:
   n=length(token&(31 if token>=32 else 7),31 if token>=32 else 7)
   word=struct.unpack_from('<H',data,p)[0];p+=2;distance=word>>2;tail=word&3
   if token>=32:distance+=1
   else:
    distance+=(token&8)<<11
    if not distance:
     assert n==1 and tail==0 and p==len(data) and len(out)==size
     return bytes(out)
    distance+=16384
   n+=2
  assert 0<distance<=len(out) and len(out)+n<=size
  for _ in range(n):out.append(out[-distance])
  literal(tail);state=tail
 raise AssertionError('missing LZO terminator')
def encode(data):
 assert len(data)>=4
 if len(data)<=238:return bytes([len(data)+17])+data+b'\x11\0\0'
 extra=len(data)-18;zeros=(extra-1)//255
 return b'\0'+bytes(zeros)+bytes([extra-zeros*255])+data+b'\x11\0\0'
def unpack(text):
 m=re.search(r'(?ms)^\[IsoMapPack5\]\n(.*?)(?=^\[|\Z)',text);assert m
 binary=base64.b64decode(''.join(l.split('=',1)[1] for l in m[1].splitlines() if '=' in l))
 p=0;out=bytearray()
 while p<len(binary):
  compressed,size=struct.unpack_from('<HH',binary,p);p+=4
  out.extend(decode(binary[p:p+compressed],size));p+=compressed
 assert p==len(binary);return m,out
recipes=[]
for direction in ['east','west']:
 original=S/'fixtures'/('tube-'+direction+'.MAP');text=original.read_text(encoding='ascii');m,raw=unpack(text)
 size=len(raw)-4 if len(raw)%11==4 and raw[-4:]==bytes(4) else len(raw);assert size%11==0
 changed=[];levels={}
 for p in range(0,size,11):
  x,y=struct.unpack_from('<HH',raw,p)
  if 74<=x<=83 and 108<=y<=120:
   changed.append(dict(cell=[x,y],before=raw[p+9],after=6));raw[p+9]=6
  if (x,y) in [(68,114),(78,114)]:levels[(x,y)]=raw[p+9]
 assert levels[(68,114)]==4 and levels[(78,114)]==6
 packed=bytearray()
 for p in range(0,len(raw),8192):
  block=bytes(raw[p:p+8192]);encoded=encode(block);assert decode(encoded,len(block))==block
  packed+=struct.pack('<HH',len(encoded),len(block))+encoded
 value=base64.b64encode(packed).decode('ascii');lines=''.join(f'{i//70+1}={value[i:i+70]}\n' for i in range(0,len(value),70))
 output=text[:m.start(1)]+lines+'\n'+text[m.end(1):]
 _,roundtrip=unpack(output);assert roundtrip==raw
 path=S/'fixtures'/('tube-elevated-'+direction+'.MAP');
 if path.exists():assert path.read_bytes()==output.encode('ascii')
 else:path.write_text(output,encoding='ascii',newline='\n')
 recipes.append(dict(path=path.relative_to(R).as_posix(),source_sha256=hashlib.sha256(original.read_bytes()).hexdigest(),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),changed=changed,entrance_exit_levels=[4,6],actor_start_level=4 if direction=='east' else 6,raw_runtime_writes=False))
(S/'elevated-tube-fixtures.json').write_text(json.dumps(dict(passed=True,scope='Map terrain records only, normal TubeClass parsing and ordinary move orders; east ascends and west descends. Independent source pack is retained.',recipes=recipes),indent=2),encoding='utf-8')
print('Created elevated bidirectional tube maps; engine runtime acceptance pending')
