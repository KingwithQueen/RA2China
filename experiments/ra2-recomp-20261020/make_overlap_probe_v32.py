"""Build a direct original-x86 probe for the new internal boundaries and returns."""
from pathlib import Path
R = Path(__file__).resolve().parent
S = R / 'evidence/movement-state-v32'
t = (S / 'joint_probe.c').read_text(encoding='utf-8')
t = t.replace('#include "ground_joint_bridge.h"', '#include "ground_joint_bridge.h"\n#include "ground_overlap_bridge.h"')
t = t.replace('static unsigned char units[2][0x800],cells[0x180],drive[128];',
              'static unsigned char units[2][0x800],types[2][0xB20],cells[0x180],drive[128];')
t = t.replace('STOP(sample_stop,04A17FEh) STOP(prepare_stop,04A3502h) STOP(passage_stop,0703331h)',
              'STOP(sample_stop,04A186Ch) STOP(sample_same_stop,04A1AB0h) STOP(prepare_stop,04A3550h) STOP(chain_stop,070346Bh) STOP(chain_empty_stop,0703905h)')
t = t.replace(' case 1:ev(a[0]);', ''' case 8:
  if(number%11==0)U(frame+0x18)=(number/11)%10;
  if(number%7==0)U(drive+0xC)=P(units[1]);
  return object==P(units[0])?P(types[0]):P(types[1]);
 case 1:ev(a[0]);''')
t = t.replace('static void lifted(unsigned k,unsigned count)',
              'static uint32_t __fastcall n_type(void*c,void*d){(void)d;return dispatch(8,P(c),NULL);}\nstatic void lifted(unsigned k,unsigned count)')
t = t.replace('L(l_lookup,1,1)', 'L(l_type,8,0) L(l_lookup,1,1)')
t = t.replace('recomp_func_t recomp_lookup_manual(uint32_t a){', 'recomp_func_t recomp_lookup_manual(uint32_t a){if(a==P(n_type))return l_type;')
t = t.replace('memset(cells,0,sizeof(cells));', 'memset(cells,0,sizeof(cells));memset(types,0,sizeof(types));')
start = t.index(' if(phase==0)entry=')
end = t.index(' if(native_return)', start)
t = t[:start] + '''
 if(phase==0){entry=0x4A17FE;ic=P(units[0]);is=(uint32_t)edge[n%11];ia=(uint32_t)edge[(n/11)%11];U(units[0]+0x88)=n%3==0?is:(uint32_t)edge[(n/121)%11];U(units[0]+0x8C)=n%3==0?ia:(uint32_t)edge[(n/1331)%11];U(units[0]+0x90)=n*31337;}
 if(phase==1){entry=0x4A3502;is=P(cells);U(frame+0x18)=n%11-1;U(cells+0x44)=n%3-1;for(unsigned k=0;k<2;++k){types[k][0xAA0]=(uint8_t)((n>>(k+1))&1);types[k][0xAF3]=(uint8_t)((n>>(k+3))&1);}}
 if(phase==2){entry=n%2?0x7038EF:0x703439;is=P(units[0]);ib=P(cells);*(uint8_t*)(uintptr_t)(frame+0x11)=(uint8_t)((n>>1)&1);U(cells+0xE4)=n%3?P(units[0]):0;U(cells+0xE8)=n%5?P(units[1]):0;U(units[0]+0x30)=n%7?P(units[1]):0;U(frame+0x7C)=P(cells);U(frame+0x8C)=n%9;}
 if(phase==3){static const uint32_t entries[]={0x7031B1,0x703B5A,0x703B69,0x703BA8,0x703BBC};entry=entries[n%5];ii=n*997;return_slot=frame+0x78;}
''' + t[end:]
start = t.index(' if(phase==0){c->locals')
end = t.index('\n}', start)
t = t[:start] + '''
 if(phase==0){c->locals[0]=U(frame+0xA4);c->locals[1]=U(frame+0x68);c->locals[2]=U(frame+0xEC);c->locals[3]=U(frame+0xF0);}
 if(phase==1)c->locals[0]=U(frame+0x18);
 if(phase==2)c->locals[0]=U(frame+0x88);
''' + t[end:]
t = t.replace('vt[0x11C/4]=', 'vt[0x80/4]=P(n_type);vt[0x11C/4]=')
start = t.index(' if(phase==0)patch(')
end = t.index('\n unsigned cases=', start)
t = t[:start] + '''
 if(phase==0){patch(0x4A186C,P(sample_stop));patch(0x4A1AB0,P(sample_same_stop));}
 if(phase==1)patch(0x4A3550,P(prepare_stop));
 if(phase==2){patch(0x70346B,P(chain_stop));patch(0x703905,P(chain_empty_stop));}
''' + t[end:]
start = t.index(' if(phase<2)result=')
end = t.index('\n capture(&actual', start)
t = t[:start] + '''
 if(phase<2)result=ra2_ground_template_transition_bridge(phase);
 else if(phase==2)result=ra2_ground_object_chain_bridge(n%2);
 else ra2_ground_passage_return_bridge(n%5);
''' + t[end:]
t = t.replace('int returned=phase==3||(phase==2&&expected.result==7);', 'int returned=phase==3;')
t = t.replace('if(phase==0)abi|=g_eax!=native_ax;',
              'if(phase==0)abi|=g_eax!=native_ax;\n if(phase==2)abi|=g_eax!=native_ax;')
(S / 'overlap_probe.c').write_text(t, encoding='utf-8', newline='\n')
t = (R / 'build-joint-probe-v32.ps1').read_text(encoding='utf-8')
t = t.replace('joint_probe.c ', 'overlap_probe.c ..\\..\\ra2\\src\\runtime\\ground_overlap_bridge.c ..\\..\\ra2\\src\\gameplay\\ground_template_transition.c ..\\..\\ra2\\src\\gameplay\\ground_object_chain.c ')
t = t.replace('/Fe:joint_probe.exe', '/Fe:overlap_probe.exe')
(R / 'build-overlap-probe-v32.ps1').write_text(t, encoding='utf-8', newline='\n')
print('Prepared four direct original-fragment groups')
