"""Natural water/beach/land from the existing map; only ordinary units and orders."""
from run_batch_v50 import *
from map_codec_v50 import unpack
import re,hashlib
base=(S/'fixtures/bridge-detour.MAP').read_text(encoding='ascii')
def section(t,name,body):return re.sub(r'(?ms)^\['+name+r'\]\n.*?(?=^\[|\Z)',lambda m:'['+name+']\n'+body.strip()+'\n\n',t)
def unit(kind,x,y):return f'Player House,{kind},256,{x},{y},0,Guard,None,0,-1,0,-1,1,1'
def foot(kind,x,y):return f'Player House,{kind},256,{x},{y},2,Guard,0,None,0,-1,0,1,1'
items=[]
for tag,units,infantry,orders,last in [
 ('wa',[('LCRF',138,102),('TRUCKA',139,102),('DEST',130,99),('TRUCKA',138,104)],[('E2',139,104),('CLEG',138,98)],['50:1023363:7:1023362:0','200:1023364:2:130:106','1200:1023364:2:130:94','400:1023362:2:129:103','1300:1023362:2:138:102','1900:1023362:16:0:0','2200:1023363:2:139:104','700:1023365:2:140:102','1600:1023365:2:138:104','900:1023366:2:140:100','300:1023367:2:139:96','1500:1023367:2:138:105'],2600),
 ('af',[('SHAD',138,102),('DEST',130,99)],[('E2',139,102),('CLEG',138,98),('E2',139,104)],['50:1023364:7:1023362:0','500:1023362:2:129:103','1300:1023362:2:139:102','2000:1023362:16:0:0','2300:1023364:2:140:104','200:1023363:2:130:106','1400:1023363:2:130:96','300:1023365:2:139:96','1500:1023365:2:138:105','700:1023366:2:140:100'],2700)]:
 t=section(base,'Units','\n'.join(f'{i}='+unit(*u) for i,u in enumerate(units)))
 t=section(t,'Infantry','\n'.join(f'{i}='+foot(*u) for i,u in enumerate(infantry)))
 assert unpack(t)[1]==unpack(base)[1]
 p=S/'fixtures'/('natural-coast-'+tag+'.MAP');p.write_bytes(t.encode('ascii'))
 items.append(dict(tag=tag,baseline_tag='b-'+tag,path=p.relative_to(R).as_posix(),sha256=sha(p),orders=orders,last=last,capture_host=True,units=units,infantry=infantry,natural_terrain_pack_sha256=hashlib.sha256(unpack(t)[1]).hexdigest()))
write(S/'coast-fixtures.json',dict(passed=True,fixtures=items,ordinary_maps_and_commands=True,terrain_pack_unchanged=True,natural_cell_reference=str(O/'runs/nd/original/cells.json'),natural_cell_reference_sha256=sha(O/'runs/nd/original/cells.json')))
