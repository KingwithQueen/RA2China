"""Add destination service cases, including callback owner and frame mutation."""
from pathlib import Path
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v37'
p=S/'overlap_probe.c';t=p.read_text(encoding='utf-8')
t='extern unsigned ra2_ground_template_destination_bridge(unsigned alternate);\n'+t
t=t.replace('STOP(anchor_stop,','STOP(destination_stop,04A2528h) STOP(anchor_stop,',1)
t=t.replace(' default:exit(3);',''' case 12:
  ev(a[0]);for(unsigned j=0;j<3;++j)ev(U(a[0]+j*4));
  if(number&1)U(drive+0xC)=P(units[1]);
  U(frame+0xD4)^=number;U(frame+0x18)+=number;
  return 0xD00D0000u|number;
 default:exit(3);''',1)
t=t.replace('static uint32_t __fastcall n_lookup','static uint32_t __fastcall n_destination(void*c,void*d,uint32_t a){(void)d;return dispatch(12,P(c),&a);}\nstatic uint32_t __fastcall n_lookup',1)
t=t.replace('L(l_exit0,','L(l_destination,12,1) L(l_exit0,',1)
t=t.replace('recomp_func_t recomp_lookup_manual(uint32_t a){','recomp_func_t recomp_lookup_manual(uint32_t a){if(a==0x548000)return l_destination;',1)
t=t.replace(' if(native_return){',''' if(phase==12){entry=n%2?0x4A24DC:0x4A24C6;for(unsigned j=0;j<3;++j){U(frame+0x24+j*4)=(uint32_t)edge[(n+j)%11];U(frame+0x74+j*4)=n*31337+j;}}
 if(native_return){''',1)
t=t.replace(' if(phase==10){for(unsigned i=0;i<3;++i)c->locals', ' if(phase==12){for(unsigned i=0;i<3;++i){c->locals[i]=U(frame+0x18+i*4);c->locals[i+3]=U(frame+0xD0+i*4);}c->locals[6]=U(frame+0x54);c->locals[7]=U(drive+0xC);}\n if(phase==10){for(unsigned i=0;i<3;++i)c->locals',1)
t=t.replace(' if(phase==10)patch',' if(phase==12){patch(0x548000,P(n_destination));patch(0x4A2528,P(destination_stop));}\n if(phase==10)patch',1)
t=t.replace(' else if(phase==10)result=', ' else if(phase==12)result=ra2_ground_template_destination_bridge(n%2);\n else if(phase==10)result=',1)
t=t.replace(' if(phase==0)abi|=', ' if(phase==12)abi|=g_eax!=native_ax||g_ecx!=native_cx;\n if(phase==0)abi|=',1)
p.write_text(t,encoding='utf-8',newline='\n')
print('Added native phase12')
