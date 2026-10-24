"""Three services may replace owner, cells, coordinates and saved slots."""
from pathlib import Path
R=Path(__file__).resolve().parent;p=R/'evidence/movement-state-v38/overlap_probe.c';t=p.read_text();t='extern void ra2_ground_advance_leave_place_return_bridge(void);\n'+t
code=''' case 18:
  ev(a[0]);ev(U(drive+0xC));ev(*(uint8_t*)(uintptr_t)(object+0x79));
  for(unsigned j=0;j<4;++j)U(frame+j*4)=number*(j*71+1)^0xAABBCCDD;
  U(drive+0xC)=P(units[(number>>a[0])&1]);
  if(!a[0]){U(frame+0x54)=P(cells+0x180);U(frame+0x6C)=P(cells);U(frame+0x18)^=number;}
  return 0xDABC0000u|number;
 case 19:
  ev(a[0]);for(unsigned j=0;j<3;++j)ev(U(a[0]+j*4));ev(U(drive+0xC));
  for(unsigned j=0;j<4;++j)U(frame+j*4)=number*(j*91+1)^0xBADCAFE;
  U(frame+0x54)=P(cells);U(frame+0x6C)=P(cells+0x180);U(a[0]+4)^=number;
  U(drive+0xC)=P(units[(number>>2)&1]);
  cells[0x11B]=(uint8_t)(number>>8);cells[0x180+0x11B]=(uint8_t)number;
  U(cells+0x140)=((number>>3)&1)?0x100:0;U(cells+0x180+0x140)=((number>>4)&1)?0x100:0;
  return 0xCAFEBABE;
 case 17:'''
t=t.replace(' case 17:',code,1)
t=t.replace('static uint32_t __fastcall n_enter(', 'static uint32_t __fastcall n_leave_enter(void*c,void*d,uint32_t a){(void)d;return dispatch(18,P(c),&a);}\nstatic uint32_t __fastcall n_relocate(void*c,void*d,uint32_t a){(void)d;return dispatch(19,P(c),&a);}\nstatic uint32_t __fastcall n_enter(',1)
t=t.replace('L(l_enter,17,1)', 'L(l_leave_enter,18,1) L(l_relocate,19,1) L(l_enter,17,1)',1).replace('if(a==P(n_enter))','if(a==P(n_leave_enter))return l_leave_enter;if(a==P(n_relocate))return l_relocate;if(a==P(n_enter))',1)
t=t.replace(' if(native_return){',' if(phase==22){entry=0x4A2586;return_slot=frame+0xF4;ic=P(units[(n>>5)&1]);U(frame+0x18)=n*13;U(frame+0x1C)=n*17;U(frame+0x20)=n*23;}\n if(native_return){',1)
t=t.replace(' if(phase==20)vt[',' if(phase==22){vt[0x11C/4]=P(n_leave_enter);vt[0x19C/4]=P(n_relocate);}\n if(phase==20)vt[',1)
t=t.replace(' else if(phase==20)ra2_', ' else if(phase==22)ra2_ground_advance_leave_place_return_bridge();\n else if(phase==20)ra2_',1)
t=t.replace(' if(phase==20){memcpy', ' if(phase==22){for(unsigned i=0;i<4;++i)c->locals[i]=U(frame+i*4);for(unsigned i=0;i<3;++i)c->locals[4+i]=U(frame+0x18+i*4);}\n if(phase==20){memcpy',1)
t=t.replace('phase==17||phase==20','phase==17||phase==20||phase==22')
p.write_text(t,encoding='utf-8',newline='\n')
