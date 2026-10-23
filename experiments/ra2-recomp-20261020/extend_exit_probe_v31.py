"""Native callback stubs expose entry state, service arguments and saved-frame mutation."""
from pathlib import Path
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v31'
p=S/'overlap_probe.c';t=p.read_text(encoding='utf-8')
t='extern void ra2_ground_prepare_service_return_bridge(unsigned entry);\n'+t
needle=' default:exit(3);';assert t.count(needle)==1
t=t.replace(needle,''' case 9: case 10:
  for(unsigned i=0;i<(k==9?2u:3u);++i)ev(a[i]);
  ev(U(drive+0x58));ev(U(units[0]+0x4D0));
  U(frame+4)=number*31337;U(frame+12)=number^0xC001CAFEu;
  if(number&1)U(drive+0xC)=P(units[1]);
  return 0xC0DE0000u|(number&65535u);
'''+needle)
needle='static uint32_t __fastcall n_lookup';i=t.index(needle)
t=t[:i]+'''static uint32_t __fastcall n_exit2(void*c,void*d,uint32_t a,uint32_t b){(void)d;uint32_t v[]={a,b};return dispatch(9,P(c),v);}
static uint32_t __fastcall n_exit3(void*c,void*d,uint32_t a,uint32_t b,uint32_t e){(void)d;uint32_t v[]={a,b,e};return dispatch(10,P(c),v);}
'''+t[i:]
t=t.replace('L(l_type,8,0)','L(l_exit2,9,2) L(l_exit3,10,3) L(l_type,8,0)',1)
t=t.replace('recomp_func_t recomp_lookup_manual(uint32_t a){','recomp_func_t recomp_lookup_manual(uint32_t a){if(a==P(n_exit2))return l_exit2;if(a==0x4A2670)return l_exit3;',1)
t=t.replace(' if(native_return){',''' if(phase==9){static const uint32_t entries[]={0x4A46FE,0x4A41AE,0x4A41CC};entry=entries[n%3];return_slot=frame+0x5C;U(frame+0x60)=n*777;U(frame+0x64)=n*999;U(drive+0x58)=n^0x12345678;U(units[0]+0x4D0)=n^0x87654321;}
 if(native_return){''',1)
t=t.replace(' if(phase==6){c->locals[0]', ' if(phase==9){for(unsigned i=0;i<4;++i)c->locals[i]=U(frame+i*4);c->locals[4]=U(drive+0x58);c->locals[5]=U(drive+0xC);}\n if(phase==6){c->locals[0]',1)
t=t.replace(' unsigned cases=65536;',' if(phase==9){patch(0x4A2670,P(n_exit3));vt[0x4C8/4]=P(n_exit2);}\n unsigned cases=65536;',1)
t=t.replace(' else if(phase==8)result=', ' else if(phase==9)ra2_ground_prepare_service_return_bridge(n%3);\n else if(phase==8)result=',1)
t=t.replace('phase==3||phase==5||phase==7;', 'phase==3||phase==5||phase==7||phase==9;')
t=t.replace('phase==7||phase==8){','phase==7||phase==8||phase==9){')
p.write_text(t,encoding='utf-8',newline='\n')
print('Extended service-return phase9')
