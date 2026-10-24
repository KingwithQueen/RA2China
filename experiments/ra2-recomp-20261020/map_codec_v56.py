from pathlib import Path
import base64,hashlib,json,re,struct

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
