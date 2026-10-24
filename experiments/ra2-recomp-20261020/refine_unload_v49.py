"""Use a stable observed rough tile family; qualify actual landing, not author intent."""
from run_batch_v49 import *
from map_codec_v49 import unpack,encode,decode
import struct,base64
p=S/'dynamic-fixtures.json';data=read(p);old=data['fixtures'][0];assert old['tag']=='ru'
write(S/'mixed-terrain-exploration.json',dict(passed=True,recipe=old,strict_trace_passed=True,qualified_rough_unload=False,actual_landing_cell=[63,78],actual_landing_land=0,reason='Raw clear/randomized tile501 did not produce rough land at every authored cell; runtime actual landing takes precedence.',original_comparison_sha256=sha(S/'runs/b-ru/comparison.json'),candidate_comparison_sha256=sha(S/'runs/ru/comparison.json')))
t=(R/old['path']).read_text(encoding='ascii');m,raw=unpack(t)
_,original=unpack((S/'fixtures/bridge-detour.MAP').read_text(encoding='ascii'))
q=next(q for q in range(0,len(original)-4,11) if struct.unpack_from('<HH',original,q)==(83,32));record=bytes(original[q+4:q+11]);assert record.hex()=='b5010000070400'
changes=[]
for q in range(0,len(raw)-4,11):
 x,y=struct.unpack_from('<HH',raw,q)
 if 62<=x<=65 and 77<=y<=80:
  changes.append(dict(cell=[x,y],before=bytes(raw[q+4:q+11]).hex(),after=record.hex()));raw[q+4:q+11]=record
packed=bytearray()
for q in range(0,len(raw),8192):
 block=bytes(raw[q:q+8192]);coded=encode(block);assert decode(coded,len(block))==block;packed+=struct.pack('<HH',len(coded),len(block))+coded
v=base64.b64encode(packed).decode();t=t[:m.start()]+'[IsoMapPack5]\n'+''.join(f'{i//70+1}={v[i:i+70]}\n' for i in range(0,len(v),70))+'\n'+t[m.end():]
q=S/'fixtures/collapse-rough-stable.MAP';q.write_bytes(t.encode('ascii'));assert unpack(t)[1]==raw
item=dict(old,tag='r2',baseline_tag='b-r2',path=q.relative_to(R).as_posix(),sha256=sha(q));data['fixtures'][0]=item;data['refined_rough_tile']=dict(source_cell=[83,32],changes=changes);p.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
wrapper=(R/'run_bridge_catalog_v49.py').read_text(encoding='utf-8').replace('movement-state-v49/bridge-catalog-observer.exe','movement-state-v49/baseline-observer/bridge-catalog-observer.exe');(R/'run_baseline_bridge_v49.py').write_text(wrapper,encoding='utf-8',newline='\n')
