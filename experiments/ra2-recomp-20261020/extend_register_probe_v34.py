"""EDX intentionally differs from the cached index; compare native live outputs."""
from pathlib import Path
R=Path(__file__).resolve().parent;p=R/'evidence/movement-state-v34/tube_state_probe.c';t=p.read_text(encoding='utf-8')
t=t.replace('native_ax,native_sp,','native_ax,native_dx,native_sp,',1).replace(' mov native_ax,eax',' mov native_dx,edx\n mov native_ax,eax',1)
t=t.replace(' if(phase==3){static const int32_t edges[]=', ''' if(phase==4){entry=0x4A2314;ip=P(drive);U(drive+0xC)=P(unit);U(drive+0x5C)=(n+7)%16;id=n%16;ia=(n/16)%8;ii=(n/128)%3?0:n%7;
  for(unsigned i=0;i<8;++i){U(0x7A00A0+i*16)=P(samples[i]);for(unsigned j=0;j<16;++j){samples[i][j*3]=j%3?(int32_t)n:0;samples[i][j*3+1]=j%3?(int32_t)(n+1):0;samples[i][j*3+2]=(int32_t)(n+j);}}}
 if(phase==3){static const int32_t edges[]=''',1)
t=t.replace(' if(phase==1){unsigned offsets[]=', ' if(phase==1||phase==4){unsigned offsets[]=',1)
t=t.replace(' if(phase==1){patch(', ' if(phase==1||phase==4){patch(',1)
t=t.replace('unsigned cases=32768','unsigned cases=phase==4?65536:32768')
t=t.replace('  else if(phase==1)result=', '  else if(phase==4)result=ra2_ground_internal_handoff_bridge(3);\n  else if(phase==1)result=',1)
t=t.replace('  if(memcmp(&expected,&actual,sizeof(actual))||abi)', '  if(phase==4)abi|=g_esp!=frame||native_sp!=frame+4||g_eax!=native_ax||g_edx!=native_dx||g_ebx!=native_bx||g_ebp!=native_bp||g_esi!=native_si||g_edi!=native_di;\n  if(memcmp(&expected,&actual,sizeof(actual))||abi)',1)
p.write_text(t,encoding='utf-8',newline='\n')
