"""All 256 warhead flag bytes and signed passage boundaries; zero callbacks."""
from pathlib import Path
R=Path(__file__).resolve().parent;p=R/'evidence/movement-state-v37/objects_probe.c';t=p.read_text();t=t.replace('0x703A23,0x703A7F','0x703A23,0x703A7F,0x703A53').replace('phase>10','phase>11')
t=t.replace('        lea eax,object_type','        lea eax,object_type\n        cmp phase,11\n        jne original_entry_v37\n        lea eax,warhead\noriginal_entry_v37:')
mark='    const uint32_t entries[]=';assert t.count(mark)==1;t=t.replace(mark,'    if(phase==11){static const int32_t limits[]={INT32_MIN,-1,0,4,5,6,7,INT32_MAX};MEM32(frame+0x8C)=(uint32_t)limits[n%8];warhead[0x146]=(uint8_t)(n/8);}\n'+mark)
t=t.replace('uint32_t resume=ra2_ground_object_branch_bridge(phase);','if(phase==11)g_eax=P(warhead);\n        uint32_t resume=ra2_ground_object_branch_bridge(phase);\n        if(phase==11&&count)return 4;')
p.write_text(t,encoding='utf-8',newline='\n')
