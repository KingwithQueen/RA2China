"""Callbacks mutate saved registers and redirect output to saved-frame aliases."""
from pathlib import Path
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v32'
p=S/'overlap_probe.c';t=p.read_text(encoding='utf-8');t='extern void ra2_ground_prepare_stop_return_bridge(unsigned entry);\n'+t
t=t.replace(' default:exit(3);',''' case 13:
  ev(a[0]);ev(a[1]);U(frame+4)=number*71;U(frame+12)=number^0x12345678u;
  U(frame+0x60)=number%5<4?frame+(number%5)*4:P(units[1]+0x200);
  return 0xABCD0000u|number;
 default:exit(3);''',1)
t=t.replace('static uint32_t __fastcall n_destination','static uint32_t __fastcall n_stop(void*c,void*d,uint32_t a,uint32_t b){(void)d;uint32_t v[]={a,b};return dispatch(13,P(c),v);}\nstatic uint32_t __fastcall n_destination',1)
t=t.replace('L(l_destination,','L(l_stop,13,2) L(l_destination,',1)
t=t.replace('recomp_func_t recomp_lookup_manual(uint32_t a){','recomp_func_t recomp_lookup_manual(uint32_t a){if(a==P(n_stop))return l_stop;',1)
t=t.replace(' if(native_return){',''' if(phase==13){entry=n%2?0x4A2916:0x4A26EC;return_slot=frame+0x5C;U(frame+0x60)=P(units[0]+0x200);}
 if(native_return){''',1)
t=t.replace(' if(phase==12){for(unsigned i=', ' if(phase==13){for(unsigned i=0;i<4;++i)c->locals[i]=U(frame+i*4);c->locals[4]=U(frame+0x60);}\n if(phase==12){for(unsigned i=',1)
t=t.replace(' if(phase==12){patch',' if(phase==13){vt[0x414/4]=P(n_stop);vt[0x410/4]=P(n_stop);}\n if(phase==12){patch',1)
t=t.replace(' else if(phase==12)result=', ' else if(phase==13)ra2_ground_prepare_stop_return_bridge(n%2);\n else if(phase==12)result=',1)
t=t.replace('phase==9||(phase==11','phase==9||phase==13||(phase==11')
t=t.replace('phase==10||phase==11){','phase==10||phase==11||phase==13){')
p.write_text(t,encoding='utf-8',newline='\n');print('Added prepare stop phase13')
