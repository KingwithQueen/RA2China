"""Ordinary maps for repairing, bypassing and other locomotors; all parents preserved."""
from run_batch_v43 import *
import re,base64,struct
# Existing independent LZO map codec, used solely on ordinary map records.
ns={};codec=(R/'make_elevated_tubes_v29.py').read_text(encoding='utf-8').split('recipes=[]')[0];exec(codec.replace("R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v29'",''),ns)
def sec(t,n,b):
 p=r'(?ms)^\['+n+r'\]\r?\n.*?(?=^\[|\Z)';v='['+n+']\n'+b.strip()+'\n\n';return re.sub(p,lambda m:v,t) if re.search(p,t) else t+'\n'+v
base=(S/'fixtures/bridge-destroy-08.MAP').read_bytes().decode('latin1')
# Hut placement is copied from the original SOV01T structure, adjacent to the same bridge end.
b=sec(base,'Structures','0=Player House,NAPOWR,256,60,120,0,None,1,0,1,0,0,None,None,None,0,0\n1=Civie1 House,CABHUT,256,58,73,0,None,0,0,1,0,0,None,None,None,0,0')
b=sec(b,'Infantry','0=Player House,ENGINEER,256,58,75,2,Guard,0,None,0,-1,0,1,1')
p=S/'fixtures/bridge-repair.MAP';p.write_bytes(b.encode('latin1'))
# Give the ground vehicle a real alternative corridor around the broken span.
t=sec(base,'Infantry','');m,raw=ns['unpack'](t);changed=[]
for k in range(0,len(raw)-4,11):
 x,y=struct.unpack_from('<HH',raw,k)
 if 62<=x<=66 and 59<=y<=74:
  changed.append([x,y,bytes(raw[k+4:k+11]).hex()]);struct.pack_into('<I',raw,k+4,0);raw[k+8]=0;raw[k+9]=4
packed=bytearray()
for k in range(0,len(raw),8192):
 block=bytes(raw[k:k+8192]);encoded=ns['encode'](block);assert ns['decode'](encoded,len(block))==block;packed+=struct.pack('<HH',len(encoded),len(block))+encoded
v=base64.b64encode(packed).decode();t=t[:m.start()]+'[IsoMapPack5]\n'+''.join(f'{k//70+1}={v[k:k+70]}\n' for k in range(0,len(v),70))+'\n'+t[m.end():]
p=S/'fixtures/bridge-detour.MAP';p.write_bytes(t.encode('latin1'))
# A jumpjet infantry crosses the damaged bridge gap using its own original rules/locomotor.
t=sec(base,'Infantry','0=Player House,JUMPJET,256,60,58,2,Guard,0,None,0,-1,0,1,1');p=S/'fixtures/bridge-jumpjet.MAP';p.write_bytes(t.encode('latin1'))
write(S/'new-map-inputs.json',dict(passed=True,repair_hut_original='evidence/movement-state-v4/SOV01T-original.MAP: CABHUT at58,73',ordinary_map_changes=True,direct_runtime_state_writes=False,detour_changed_map_cells=changed,files=[dict(path=p.relative_to(R).as_posix(),sha256=sha(p)) for p in [S/'fixtures/bridge-repair.MAP',S/'fixtures/bridge-detour.MAP',S/'fixtures/bridge-jumpjet.MAP']]))
print('Created ordinary repair, detour and jumpjet bridge maps')
