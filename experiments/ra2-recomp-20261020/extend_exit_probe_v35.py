"""Destination aliases owner, saved slots and the global invalid sentinel."""
from pathlib import Path
R=Path(__file__).resolve().parent;p=R/'evidence/movement-state-v35/overlap_probe.c';t=p.read_text(encoding='utf-8');t='extern void ra2_ground_prepare_invalidate_return_bridge(void);\n'+t
mark=' if(native_return){';code=' if(phase==16){entry=0x4A46D7;return_slot=frame+0x5C;units[0][0x7D]=(uint8_t)(n&1);drive[0x63]=(uint8_t)n;\n  U(0x852998)=P(units[1]);U(0x85299C)=n^0xAABBCCDD;U(0x8529A0)=n*733;\n  is=n%5==0?P(drive+0xC):n%5==1?frame+4:n%5==2?0x85299C:P(units[0]+0x200);}\n'
assert mark in t;t=t.replace(mark,code+mark,1)
t=t.replace(' if(phase==15){for(unsigned i=', ' if(phase==16){for(unsigned i=0;i<4;++i)c->locals[i]=U(frame+i*4);c->locals[4]=U(drive+0xC);c->locals[5]=U(drive+0x58);c->locals[6]=U(drive+0x60);for(unsigned i=0;i<3;++i)c->locals[7+i]=U(0x852998+i*4);}\n if(phase==15){for(unsigned i=',1)
t=t.replace(' if(phase==15)vt[', ' if(phase==16)vt[0x4C8/4]=P(n_exit2);\n if(phase==15)vt[',1).replace(' else if(phase==15)ra2_', ' else if(phase==16)ra2_ground_prepare_invalidate_return_bridge();\n else if(phase==15)ra2_',1)
t=t.replace('phase==14||phase==15','phase==14||phase==15||phase==16');t=t.replace('uint32_t events[128],count,result,locals[10];','unsigned char drive_bytes[128];uint32_t events[128],count,result,locals[11];')
t=t.replace('U(0x852998)=P(units[1]);','U(0x8529A4)=n^0x44556677;U(0x852998)=P(units[1]);',1)
t=t.replace('if(phase==16){for(unsigned i=0;i<4;++i)c->locals[i]=U(frame+i*4);','if(phase==16){memcpy(c->drive_bytes,drive,sizeof(drive));for(unsigned i=0;i<4;++i)c->locals[i]=U(frame+i*4);',1)
t=t.replace('for(unsigned i=0;i<3;++i)c->locals[7+i]=U(0x852998+i*4);','for(unsigned i=0;i<4;++i)c->locals[7+i]=U(0x852998+i*4);',1)
p.write_text(t,encoding='utf-8',newline='\n')
