"""Read the two land-name pointer tables from the locked original PE; no external packages."""
from run_batch_v54 import *
import struct
p=R/'ra2/game/game.exe';b=p.read_bytes();u16=lambda x:struct.unpack_from('<H',b,x)[0];u32=lambda x:struct.unpack_from('<I',b,x)[0]
pe=u32(0x3C);opt=pe+24;base=u32(opt+28);sections=[]
for i in range(u16(pe+6)):
 at=opt+u16(pe+20)+i*40;sections.append((u32(at+12),u32(at+16),u32(at+20)))
def offset(va):
 for rva,size,raw in sections:
  if rva<=va-base<rva+size:return raw+va-base-rva
 raise ValueError(hex(va))
expected=['Clear','Road','Water','Rock','Wall','Tiberium','Beach','Rough','Ice','Railroad','Tunnel','Weeds'];tables=[]
for va in [0x7D3878,0x7EEBBC]:
 entries=[]
 for i in range(12):
  pointer=u32(offset(va)+i*4);name=b[offset(pointer):offset(pointer)+32].split(b'\0')[0].decode('ascii');assert name==expected[i]
  entries.append(dict(value=i,name=name,string_va=hex(pointer)))
 tables.append(dict(table_va=hex(va),entries=entries))
write(S/'land-type-table-proof.json',dict(passed=True,original=str(p),original_sha256=sha(p),tables=tables,land7_is_rough=True,road_is_land1=True,scope='Readonly ordered original data tables; no claim all call sites were traced. Historical prose which called land7 Road is corrected here without altering old baselines, rules or traces.'))
print(dict(passed=True,road=1,rough=7,beach=6,tables=2))
