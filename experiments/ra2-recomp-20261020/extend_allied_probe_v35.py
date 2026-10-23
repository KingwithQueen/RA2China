"""Exercise the actual internal relation entry independently of the full entry."""
from pathlib import Path
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v35'
p=S/'allied_probe.c';t=p.read_text(encoding='utf-8')
t='extern unsigned ra2_ground_allied_relation_bridge(void);\n'+t
t=t.replace('outcomes[5],mission_reads,tail;','outcomes[5],mission_reads,tail,relation;\nstatic uint32_t initial_bx;')
t=t.replace('lea ebx,cell','mov ebx,initial_bx')
t=t.replace('    if(tail){entry_address=', '    initial_bx=P(cell);if(relation){entry_address=0x70372C;initial_bx=(P(cell)&0xFFFFFF00u)|(n&1);MEM32(frame+0x20)=P(object_data);}\n    if(tail){entry_address=',1)
t=t.replace('tail=argc==3;hold_image();','relation=argc==3&&!strcmp(argv[2],"relation");tail=argc==3&&!relation;hold_image();')
t=t.replace('g_ebx=P(cell);g_esi=','g_ebx=initial_bx;g_esi=')
t=t.replace('uint32_t resume=tail?','uint32_t resume=relation?ra2_ground_allied_relation_bridge():tail?')
p.write_text(t,encoding='utf-8',newline='\n')
print('Added relation entry cases')
