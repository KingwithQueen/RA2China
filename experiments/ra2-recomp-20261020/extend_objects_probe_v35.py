"""Weapon service writes back warhead before the concrete terrain check."""
from pathlib import Path
R=Path(__file__).resolve().parent;p=R/'evidence/movement-state-v35/objects_probe.c';t=p.read_text(encoding='utf-8')
a='if(phase==8&&number%3==0)';assert a in t;t=t.replace(a,'if(phase==9){F(weapon,0xAC)=number%3?P(warhead):0;warhead[0x146]=(number>>2)&1;}'+a,1)
t=t.replace('0x70399A,0x7039EC','0x70399A,0x7039EC,0x703A23').replace('phase>8','phase>9');p.write_text(t,encoding='utf-8',newline='\n')
