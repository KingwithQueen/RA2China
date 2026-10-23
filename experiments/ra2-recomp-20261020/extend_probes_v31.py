"""Add anchor and Advance-service cases without removing previous phases."""
from pathlib import Path
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v31'
p=S/'overlap_probe.c';t=p.read_text(encoding='utf-8')
t='extern unsigned ra2_ground_sample_anchor_bridge(void);\nextern unsigned ra2_ground_advance_service_return_bridge(unsigned entry);\n'+t
t=t.replace('#include "native_probe_host.h"','#include "native_probe_host.h"\n#ifdef RA2_ANCHOR_PHASE\n#define ra2_ground_advance_service_return_bridge(e) (0u)\n#endif')
t=t.replace('STOP(index_stop,','STOP(anchor_stop,04A237Dh) STOP(alive_stop,04A1FA1h) STOP(index_stop,')
t=t.replace('case 9: case 10:','''case 11:
  U(frame+4)=number*13;U(frame+12)=number^0xC0FFEE;
  if(number&1)U(drive+0xC)=P(units[1]);
  return 0xBEEF0000u|((number>>1)&1);
 case 9: case 10:''')
t=t.replace('return 0xC0DE0000u|(number&65535u);','return phase==11 ? 0xC0DE0000u|((number>>4)&1) : 0xC0DE0000u|(number&65535u);')
t=t.replace('static uint32_t __fastcall n_exit2','static uint32_t __fastcall n_exit0(void*c,void*d){(void)d;return dispatch(11,P(c),NULL);}\nstatic uint32_t __fastcall n_exit2')
t=t.replace('L(l_exit2,9,2)','L(l_exit0,11,0) L(l_exit2,9,2)')
t=t.replace('if(a==P(n_exit2))','if(a==P(n_exit0))return l_exit0;if(a==P(n_exit2))')
needle=' if(native_return){'
assert t.count(needle)==1
t=t.replace(needle,''' if(phase==10){entry=0x4A2347;ic=n%4==0?frame+0x78:n%4==1?frame+0x30:P(types[0]);U(ic+8)=n^0xAABBCCDD;for(unsigned j=0;j<3;++j)U(units[0]+0x88+j*4)=n*31337+j;}
 if(phase==11){entry=n%2?0x4A229C:0x4A22BE;return_slot=frame+0xF4;for(unsigned j=0;j<2;++j)units[j][0x7D]=(unsigned char)((n>>(j+2))&1);}
'''+needle)
t=t.replace(' if(phase==9){for(unsigned',' if(phase==10){for(unsigned i=0;i<3;++i)c->locals[i]=U(frame+0x80+i*4);c->locals[3]=U(frame+0x34);}\n if(phase==9||phase==11){for(unsigned')
t=t.replace(' if(phase==8)patch',' if(phase==10)patch(0x4A237D,P(anchor_stop));\n if(phase==11){patch(0x4A1FA1,P(alive_stop));vt[0x414/4]=P(n_exit2);vt[0x490/4]=P(n_exit0);}\n if(phase==8)patch')
t=t.replace(' else if(phase==9)ra2_ground',' else if(phase==10)result=ra2_ground_sample_anchor_bridge();\n else if(phase==11)result=ra2_ground_advance_service_return_bridge(n%2?0:1);\n else if(phase==9)ra2_ground')
t=t.replace('phase==7||phase==9;','phase==7||phase==9||(phase==11&&expected.result!=0x4A1FA1);')
t=t.replace('if(phase==7||phase==8)abi','if(phase==7||phase==8||phase==10)abi')
t=t.replace('phase==8||phase==9){abi','phase==8||phase==9||phase==10||phase==11){abi')
# Capture flags on the host stack, not on the already popped simulated frame.
t=t.replace(' mov native_di,edi\n pushfd',' mov native_di,edi\n mov esp,host_stack\n pushfd')
t=t.replace('static unsigned phase,number,event_count;','static unsigned phase,number,event_count,secondary_queries;')
t=t.replace('case 11:\n  U(frame+4)', 'case 11:\n  ++secondary_queries;U(frame+4)')
t=t.replace('number=n;resume=event_count=0;', 'number=n;resume=event_count=secondary_queries=0;')
t=t.replace('unsigned cases=65536;uint64_t callbacks=0;', 'unsigned cases=65536,fallthrough=0,secondary_total=0,continued=0;uint64_t callbacks=0;')
t=t.replace('capture(&expected,resume?resume:native_ax);setup(n);', 'capture(&expected,resume?resume:native_ax);unsigned expected_secondary=secondary_queries;setup(n);')
t=t.replace('int abi=g_esp!=', 'int abi=secondary_queries!=expected_secondary||g_esp!=')
t=t.replace('callbacks+=event_count;', 'callbacks+=event_count;if(phase==11){secondary_total+=secondary_queries;if(n%2&&secondary_queries)++fallthrough;if(expected.result==0x4A1FA1)++continued;}')
t=t.replace('\\"original_stack_cleanup_verified\\":true}', '\\"original_stack_cleanup_verified\\":true,\\"primary_fallthrough_cases\\":%u,\\"secondary_service_cases\\":%u,\\"alive_continuations\\":%u}')
t=t.replace('(unsigned long long)callbacks);', '(unsigned long long)callbacks,fallthrough,secondary_total,continued);')
p.write_text(t,encoding='utf-8',newline='\n')
print('Extended overlap phases 10 and 11')
