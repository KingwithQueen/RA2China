"""Incoming ECX differs from drive.owner; callbacks can change saved slots."""
from pathlib import Path
R=Path(__file__).resolve().parent;p=R/'evidence/movement-state-v34/overlap_probe.c';t=p.read_text(encoding='utf-8')
t='extern void ra2_ground_prepare_owner_stop_return_bridge(void);\n'+t
t=t.replace(' if(native_return){',' if(phase==15){entry=0x4A449B;return_slot=frame+0x5C;ic=P(units[n&1]);}\n if(native_return){',1)
t=t.replace(' if(phase==14){for(unsigned i=', ' if(phase==15){for(unsigned i=0;i<4;++i)c->locals[i]=U(frame+i*4);c->locals[4]=U(drive+0xC);}\n if(phase==14){for(unsigned i=',1)
t=t.replace(' if(phase==14){patch(', ' if(phase==15)vt[0x410/4]=P(n_exit2);\n if(phase==14){patch(',1)
t=t.replace(' else if(phase==14)ra2_', ' else if(phase==15)ra2_ground_prepare_owner_stop_return_bridge();\n else if(phase==14)ra2_',1)
t=t.replace('phase==13||phase==14','phase==13||phase==14||phase==15')
p.write_text(t,encoding='utf-8',newline='\n')
