"""Add a native index-continuation phase without replacing prior accepted phases."""
from pathlib import Path
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v30'
t=(R/'evidence/movement-state-v29/overlap_probe.c').read_text(encoding='utf-8')
t='extern unsigned ra2_ground_template_index_bridge(void);\n'+t
t=t.replace('STOP(table_turn_stop,','STOP(index_stop,04A2311h) STOP(table_turn_stop,',1)
needle=' if(native_return){';assert t.count(needle)==1
t=t.replace(needle,''' if(phase==8){entry=0x4A1FBE;ia=n%72;drive[0x60]=(uint8_t)(n>>8);MEM8(0x7A0180+ia*12)=(uint8_t)n;MEM8(0x7A0181+ia*12)=(uint8_t)(n^0x80);}
'''+needle)
t=t.replace(' unsigned cases=65536;',' if(phase==8)patch(0x4A2311,P(index_stop));\n unsigned cases=65536;',1)
t=t.replace(' else if(phase==6)result=', ' else if(phase==8)result=ra2_ground_template_index_bridge();\n else if(phase==6)result=',1)
t=t.replace(' if(phase==7)abi|=g_ecx!=native_cx;', ' if(phase==7||phase==8)abi|=g_ecx!=native_cx;')
t=t.replace('if(phase==4||phase==5||phase==6||phase==7){','if(phase==4||phase==5||phase==6||phase==7||phase==8){')
(S/'overlap_probe.c').write_text(t,encoding='utf-8',newline='\n')
p=R/'build-overlap-probe-v30.ps1';t=p.read_text(encoding='utf-8');needle='overlap_probe.c ';assert t.count(needle)==1
t=t.replace(needle,needle+'..\\..\\ra2\\src\\gameplay\\ground_sampling_shared.c ',1);p.write_text(t,encoding='utf-8',newline='\n')
print('Extended native template-index phase8')
