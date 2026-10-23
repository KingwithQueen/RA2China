"""Add the remembered moving-object entry to the original machine-code probe."""
from pathlib import Path
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v31'
p=S/'allied_probe.c';t=p.read_text(encoding='utf-8')
t='extern unsigned ra2_ground_moving_tail_bridge(void);\n'+t
t=t.replace('static unsigned outcomes[5],mission_reads;','static unsigned outcomes[5],mission_reads,tail;')
t=t.replace('case WANTS: r[2]=args[0];return','case WANTS: if(tail && number%3==0){MEM32(frame+0x8C)=number%9-3;MEM32(frame+0x14)=P(unit)+4;}r[2]=args[0];return')
t=t.replace('MEM32(0x7D8964)=','if(tail){entry_address=0x703895;MEM32(frame+0x20)=P(object_data);}\n    MEM32(0x7D8964)=')
t=t.replace('if(argc!=2) return 2;','if(argc<2||argc>3) return 2;tail=argc==3;')
t=t.replace('uint32_t resume=ra2_ground_allied_bridge();','uint32_t resume=tail?ra2_ground_moving_tail_bridge():ra2_ground_allied_bridge();')
t=t.replace('if(resume!=expected_resume ||','if((tail && (g_ebp!=native_ebp||g_esi!=native_esi||g_edi!=native_edi)) || resume!=expected_resume ||')
t=t.replace('\\"allied_cases\\":65536,','\\"allied_cases\\":65536,\\"moving_tail_cases\\":%u,').replace('outcomes[0],outcomes[1]','tail?65536u:0u,outcomes[0],outcomes[1]')
p.write_text(t,encoding='utf-8',newline='\n')
print('Extended allied tail entry and callback-mutated passage slot')
