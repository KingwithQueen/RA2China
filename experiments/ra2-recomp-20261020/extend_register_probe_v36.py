"""Exercise register coordinates unlike cached stack coordinates, with callback writes."""
from pathlib import Path
R=Path(__file__).resolve().parent;p=R/'evidence/movement-state-v36/overlap_probe.c';t=p.read_text(encoding='utf-8')
mark=' if(native_return){';code=' if(phase==18){entry=0x4A24F4;ic=(uint32_t)edge[n%11];id=(uint32_t)edge[(n/11)%11];ib=(uint32_t)edge[(n/121)%11];U(frame+0x18)=n*17;U(frame+0x1C)=n*31;U(frame+0x20)=n*47;}\n'
assert mark in t;t=t.replace(mark,code+mark,1).replace('if(phase==12){','if(phase==12||phase==18){')
t=t.replace(' else if(phase==16)ra2_', ' else if(phase==18)result=ra2_ground_template_destination_bridge(2);\n else if(phase==16)ra2_',1)
p.write_text(t,encoding='utf-8',newline='\n')
