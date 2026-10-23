"""The weapon callback may change the train property before it is read."""
from pathlib import Path
R=Path(__file__).resolve().parent;p=R/'evidence/movement-state-v34/objects_probe.c';t=p.read_text(encoding='utf-8')
t=t.replace('r[2]=args[0];return P(&holders[weapon_reads++ ? 1 : 0]);','if(phase==8&&number%3==0)owner_type[0xAA0]^=1;r[2]=args[0];return P(&holders[weapon_reads++ ? 1 : 0]);',1)
t=t.replace('0x703A12,0x70399A','0x703A12,0x70399A,0x7039EC').replace('phase>7','phase>8')
p.write_text(t,encoding='utf-8',newline='\n')
