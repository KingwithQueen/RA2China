"""Native entry includes the stack height write before the map service."""
from pathlib import Path
R=Path(__file__).resolve().parent;p=R/'evidence/movement-state-v37/overlap_probe.c';t=p.read_text();t=t.replace('phase==12||phase==18','phase==12||phase==18||phase==19')
mark=' if(native_return){';code=' if(phase==19){entry=0x4A24F0;ic=(uint32_t)edge[n%11];id=(uint32_t)edge[(n/11)%11];ib=(uint32_t)edge[(n/121)%11];U(frame+0x18)=n*17;U(frame+0x1C)=n*31;U(frame+0x20)=n*47;}\n';assert t.count(mark)==1;t=t.replace(mark,code+mark)
t=t.replace(' else if(phase==18)result=', ' else if(phase==19)result=ra2_ground_template_destination_bridge(3);\n else if(phase==18)result=',1)
t=t.replace('if(phase==12)abi|=', 'if(phase==12||phase==18||phase==19)abi|=')
# Capture the height visible inside the service, not only after it.
t=t.replace('case 12:\n  ev(a[0]);','case 12:\n  if(phase==19)ev(U(frame+0x20));\n  ev(a[0]);')
p.write_text(t,encoding='utf-8',newline='\n')
