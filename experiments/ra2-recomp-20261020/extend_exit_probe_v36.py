"""Placement callback changes owner, position, saved slots and flag restoration target."""
from pathlib import Path
R=Path(__file__).resolve().parent;p=R/'evidence/movement-state-v36/overlap_probe.c';t=p.read_text(encoding='utf-8');t='extern void ra2_ground_advance_place_return_bridge(void);\n'+t
mark=' if(native_return){';code=' if(phase==17){entry=0x4A2607;return_slot=frame+0xF4;ic=P(units[(n/8)%2]);units[0][0x74]=(uint8_t)n;units[1][0x74]=(uint8_t)(n^0xD3);U(frame+0x18)=n*13;U(frame+0x1C)=n*17;U(frame+0x20)=n*23;}\n'
assert mark in t;t=t.replace(mark,code+mark,1)
mark=' case 15:';code=' case 16:\n  ev(a[0]);ev(U(a[0]));ev(U(a[0]+4));ev(U(a[0]+8));ev(units[0][0x74]);ev(units[1][0x74]);\n  U(frame+4)=number*71;U(frame+8)=number^0xAABBCCDD;U(frame+12)=number^0xDEADBEEF;\n  U(a[0])^=number;U(drive+0xC)=number%3==0?P(units[1]):number%3==1?frame-0x74+(number/3%4)*4:P(units[0]);\n  return 0xCAFEBABEu;\n'
assert mark in t;t=t.replace(mark,code+mark,1)
t=t.replace('static uint32_t __fastcall n_destination(', 'static uint32_t __fastcall n_place(void*c,void*d,uint32_t a){(void)d;return dispatch(16,P(c),&a);}\nstatic uint32_t __fastcall n_destination(',1)
t=t.replace('L(l_cleanup,14,0)','L(l_place,16,1) L(l_cleanup,14,0)',1).replace('if(a==0x4CD9B0)','if(a==P(n_place))return l_place;if(a==0x4CD9B0)',1)
t=t.replace(' if(phase==16)vt[',' if(phase==17)vt[0x19C/4]=P(n_place);\n if(phase==16)vt[',1)
t=t.replace(' else if(phase==18)result=', ' else if(phase==17)ra2_ground_advance_place_return_bridge();\n else if(phase==18)result=',1)
t=t.replace(' if(phase==16){memcpy',' if(phase==17){memcpy(c->drive_bytes,drive,sizeof(drive));for(unsigned i=0;i<4;++i)c->locals[i]=U(frame+i*4);for(unsigned i=0;i<3;++i)c->locals[4+i]=U(frame+0x18+i*4);}\n if(phase==16){memcpy',1)
t=t.replace('phase==15||phase==16','phase==15||phase==16||phase==17')
p.write_text(t,encoding='utf-8',newline='\n')
