"""Mark-enter service mutates owner, all popped nonvolatile slots and callback EAX."""
from pathlib import Path
R=Path(__file__).resolve().parent;p=R/'evidence/movement-state-v37/overlap_probe.c';t=p.read_text();t='extern void ra2_ground_advance_mark_return_bridge(void);\n'+t
mark=' if(native_return){';code=' if(phase==20){entry=0x4A25E8;return_slot=frame+0xF4;U(drive+0xC)=P(units[(n/8)%2]);}\n';assert t.count(mark)==1;t=t.replace(mark,code+mark)
t=t.replace(' case 16:', ' case 17:\n  ev(a[0]);ev(U(drive+0xC));\n  for(unsigned j=0;j<4;++j)U(frame+j*4)=number*(j*71+1)^0xAABBCCDD;\n  U(drive+0xC)=P(units[(number>>1)&1]);return 0xDABC0000u|number;\n case 16:',1)
t=t.replace('static uint32_t __fastcall n_place(', 'static uint32_t __fastcall n_enter(void*c,void*d,uint32_t a){(void)d;return dispatch(17,P(c),&a);}\nstatic uint32_t __fastcall n_place(',1)
t=t.replace('L(l_place,16,1)', 'L(l_enter,17,1) L(l_place,16,1)',1).replace('if(a==P(n_place))','if(a==P(n_enter))return l_enter;if(a==P(n_place))',1)
t=t.replace(' if(phase==17)vt[',' if(phase==20)vt[0x11C/4]=P(n_enter);\n if(phase==17)vt[',1)
t=t.replace(' else if(phase==17)ra2_', ' else if(phase==20)ra2_ground_advance_mark_return_bridge();\n else if(phase==17)ra2_',1)
t=t.replace(' if(phase==17){memcpy',' if(phase==20){memcpy(c->drive_bytes,drive,sizeof(drive));for(unsigned i=0;i<4;++i)c->locals[i]=U(frame+i*4);}\n if(phase==17){memcpy',1)
t=t.replace('phase==16||phase==17','phase==16||phase==17||phase==20')
p.write_text(t,encoding='utf-8',newline='\n')
