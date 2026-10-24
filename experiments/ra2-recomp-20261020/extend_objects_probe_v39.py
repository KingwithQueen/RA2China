"""Already selected holders: empty weapon, empty warhead, flags and passage levels."""
from pathlib import Path
R=Path(__file__).resolve().parent;p=R/'evidence/movement-state-v39/objects_probe.c';t=p.read_text(encoding='utf-8')
t=t.replace('0x703A53,0x703A45','0x703A53,0x703A45,0x703A3B').replace('if(phase>12)','if(phase>13)')
t=t.replace('        cmp phase,12','        cmp phase,13\n        jne holder_original_v39\n        lea eax,holders\n        jmp original_entry_v37\nholder_original_v39:\n        cmp phase,12',1)
t=t.replace('    const uint32_t entries[]=','    if(phase==13){static const int32_t limits[]={INT32_MIN,-1,0,4,5,6,7,INT32_MAX};MEM32(frame+0x8C)=(uint32_t)limits[n%8];holders[0]=(n>>11)&1?P(weapon):0;F(weapon,0xAC)=(n>>12)&1?P(warhead):0;warhead[0x146]=(uint8_t)(n/8);}\n    const uint32_t entries[]=',1)
t=t.replace('        uint32_t resume=ra2_ground_object_branch_bridge(phase);','        if(phase==13)g_eax=P(holders);\n        uint32_t resume=ra2_ground_object_branch_bridge(phase);\n        if(phase==13&&count)return 4;',1)
p.write_text(t,encoding='utf-8',newline='\n')
