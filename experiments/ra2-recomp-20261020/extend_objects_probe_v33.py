"""Cover the contact entry and a relation change during the ability callback."""
from pathlib import Path
R=Path(__file__).resolve().parent;p=R/'evidence/movement-state-v33/objects_probe.c';t=p.read_text(encoding='utf-8')
t=t.replace('case ABILITY: r[2]=args[0];return', 'case ABILITY: if(phase==7&&number%3==0)fixture^=1u<<11;r[2]=args[0];return',1)
t=t.replace('0x7035DF,0x703A12','0x7035DF,0x703A12,0x70399A').replace('phase>6','phase>7')
p.write_text(t,encoding='utf-8',newline='\n')
