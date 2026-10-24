"""Loaded weapon nullable warheads, all flag bytes and signed passage boundaries."""
from pathlib import Path
R=Path(__file__).resolve().parent;p=R/'evidence/movement-state-v38/objects_probe.c';t=p.read_text();t=t.replace('0x703A7F,0x703A53','0x703A7F,0x703A53,0x703A45').replace('phase>11','phase>12')
t=t.replace('        lea eax,object_type','        lea eax,object_type\n        cmp phase,12\n        jne weapon_original_v38\n        lea eax,weapon\n        jmp original_entry_v37\nweapon_original_v38:')
mark='    const uint32_t entries[]=';t=t.replace(mark,'    if(phase==12){static const int32_t limits[]={INT32_MIN,-1,0,4,5,6,7,INT32_MAX};MEM32(frame+0x8C)=(uint32_t)limits[n%8];warhead[0x146]=(uint8_t)(n/8);F(weapon,0xAC)=(n>>11)&1?P(warhead):0;}\n'+mark)
t=t.replace('uint32_t resume=ra2_ground_object_branch_bridge(phase);','if(phase==12)g_eax=P(weapon);\n        uint32_t resume=ra2_ground_object_branch_bridge(phase);\n        if(phase==12&&count)return 4;')
p.write_text(t,encoding='utf-8',newline='\n')
