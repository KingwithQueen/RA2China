"""Legal map inputs: original bridges, clear lower terrain, three infantry per layer."""
from pathlib import Path
import base64,hashlib,json,re,struct
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v38'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
namespace={}
codec=(R/'make_elevated_tubes_v38.py').read_text(encoding='utf-8').split('recipes=[]')[0]
codec=codec.replace("R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v38'",'')
exec(codec,namespace)
original=R/'evidence/movement-state-v4/SOV01T-original.MAP'
source=S/'fixtures/dynamic-far-base.MAP'
t=source.read_text(encoding='ascii');o=original.read_text(encoding='utf-8-sig')
for key in ['OverlayPack','OverlayDataPack']:
 pattern=rf'(?ms)^\[{key}\]\n.*?(?=^\[|\Z)';section=re.search(pattern,o);assert section
 t=re.sub(pattern,lambda _:section[0],t) if re.search(pattern,t) else t+'\n'+section[0]
m,raw=namespace['unpack'](t);changes=[]
for p in range(0,len(raw)-4,11):
 x,y=struct.unpack_from('<HH',raw,p)
 if 58<=x<=61 and 64<=y<=69:
  changes.append([x,y,bytes(raw[p+4:p+11]).hex()])
  struct.pack_into('<I',raw,p+4,0);raw[p+8]=0;raw[p+9]=0
assert len(changes)==24
packed=bytearray()
for p in range(0,len(raw),8192):
 block=bytes(raw[p:p+8192]);encoded=namespace['encode'](block)
 assert namespace['decode'](encoded,len(block))==block
 packed+=struct.pack('<HH',len(encoded),len(block))+encoded
value=base64.b64encode(packed).decode()
t=t[:m.start()]+'[IsoMapPack5]\n'+''.join(f'{i//70+1}={value[i:i+70]}\n' for i in range(0,len(value),70))+'\n'+t[m.end():]
def replace_section(text,key,body):
 pattern=rf'(?ms)^\[{key}\]\n.*?(?=^\[|\Z)';value='['+key+']\n'+body+'\n'
 return re.sub(pattern,lambda _:value,text) if re.search(pattern,text) else text+'\n'+value
rows=[]
for upper in [0,1]:
 for sub in [2,3,4]:rows.append(f'{len(rows)}=Player House,E2,256,60,66,{sub},Sleep,128,None,0,-1,{upper},1,1')
t=replace_section(t,'Infantry','\n'.join(rows)+'\n')
records=[]
for name,y,goal in [('north',62,72),('south',71,61)]:
 output=replace_section(t,'Units',f'0=Player House,TRUCKA,256,60,{y},128,Guard,None,0,-1,0,-1,1,1\n')
 p=S/f'fixtures/bridge-chain-{name}.MAP'
 if p.exists():assert p.read_bytes()==output.encode('ascii'),p
 else:p.write_text(output,encoding='ascii',newline='\n')
 records.append(dict(name=name,path=p.relative_to(R).as_posix(),sha256=sha(p),start=[60,y],goal=[60,goal],id=1023362))
# Underdeck moves must target ground outside the bridge. A click on a bridge
# cell selects its upper surface in the original, and is not lower-path proof.
m,lower_raw=namespace['unpack'](t)
lower_changes=[]
for offset in range(0,len(lower_raw)-4,11):
 x,y=struct.unpack_from('<HH',lower_raw,offset)
 if 54<=x<=65 and 64<=y<=68:
  lower_changes.append([x,y,bytes(lower_raw[offset+4:offset+11]).hex()])
  struct.pack_into('<I',lower_raw,offset+4,0);lower_raw[offset+8]=lower_raw[offset+9]=0
packed=bytearray()
for offset in range(0,len(lower_raw),8192):
 block=bytes(lower_raw[offset:offset+8192]);encoded=namespace['encode'](block)
 assert namespace['decode'](encoded,len(block))==block
 packed+=struct.pack('<HH',len(encoded),len(block))+encoded
value=base64.b64encode(packed).decode()
lower=t[:m.start()]+'[IsoMapPack5]\n'+''.join(f'{i//70+1}={value[i:i+70]}\n' for i in range(0,len(value),70))+'\n'+t[m.end():]
for name,x,goal in [('lower-west',55,64),('lower-east',64,55)]:
 output=replace_section(lower,'Units',f'0=Player House,TRUCKA,256,{x},66,128,Guard,None,0,-1,0,-1,1,1\n')
 p=S/f'fixtures/bridge-chain-{name}.MAP'
 if p.exists():assert p.read_bytes()==output.encode('ascii'),p
 else:p.write_text(output,encoding='ascii',newline='\n')
 records.append(dict(name=name,path=p.relative_to(R).as_posix(),sha256=sha(p),start=[x,66],goal=[goal,66],id=1023362))
report=dict(passed=True,fixtures=records,original_overlays=True,lower_clear_cells=changes,
 underdeck_corridor_changes=lower_changes,
 ordinary_map_placement=True,raw_runtime_writes=False,infantry_subpositions=[2,3,4],
 inputs=[dict(path=p.relative_to(R).as_posix(),sha256=sha(p)) for p in [original,source,R/'make_elevated_tubes_v38.py',Path(__file__)]])
(S/'bridge-fixtures.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print('Prepared four bridge chain scenes; observed layer and actual chain visits still required')
