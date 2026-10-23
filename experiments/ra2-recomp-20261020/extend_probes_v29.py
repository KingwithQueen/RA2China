"""Reproducible round-29 probe additions from the protected round-28 sources."""
from pathlib import Path
R=Path(__file__).resolve().parent;O=R/'evidence/movement-state-v28';S=R/'evidence/movement-state-v29'
t=(O/'objects_probe.c').read_text(encoding='utf-8').replace('0x70394F,0x7034BF','0x70394F,0x7034BF,0x7035DF').replace('phase>4','phase>5')
(S/'objects_probe.c').write_text(t,encoding='utf-8',newline='\n')
t=(O/'overlap_probe.c').read_text(encoding='utf-8')
t='extern unsigned ra2_ground_template_table_bridge(void);\nextern void ra2_ground_prepare_written_return_bridge(unsigned entry);\n'+t
t=t.replace('STOP(layer_stop,','STOP(table_turn_stop,04A4015h) STOP(table_straight_stop,04A45B7h) STOP(layer_stop,')
t=t.replace('static uint32_t native_flags;', 'static uint32_t native_flags,native_cx;')
t=t.replace(' mov native_ax,eax',' mov native_cx,ecx\n mov native_ax,eax')
t=t.replace(' if(native_return){',''' if(phase==6){entry=0x4A3FE3;ib=n%8;is=(n/8)%9-1;drive[0x60]=(unsigned char)n;drive[0x64]=(unsigned char)(n>>8);for(unsigned k=0;k<72;++k){MEM8(0x7A0180+k*12)=(unsigned char)((n+k)%3);MEM8(0x7A0188+k*12)=(unsigned char)(n^k);}}
 if(phase==7){static const uint32_t entries[]={0x4A26FE,0x4A28F6,0x4A2F3B,0x4A3F55};entry=entries[n%4];return_slot=frame+0x5C;unsigned slot=(n/4)%7;U(frame+0x60)=slot<4?frame+slot*4:slot==4?frame+0x30:P(units[0]+0x200+slot);if(n%4==2 && (n/28)%2)ip=frame-0x58;drive[0x61]=(unsigned char)n;U(drive+0x58)=n*31337;}
 if(native_return){''')
t=t.replace(' if(phase==4)c->locals[0]=U(frame+0x40);',''' if(phase==4)c->locals[0]=U(frame+0x40);
 if(phase==6){c->locals[0]=U(drive+0x58);c->locals[1]=U(drive+0x60);c->locals[2]=U(drive+0x64);}
 if(phase==7){for(unsigned i=0;i<4;++i)c->locals[i]=U(frame+i*4);c->locals[4]=U(frame+0x30);c->locals[5]=U(drive+0x58);c->locals[6]=U(drive+0x60);}
''')
t=t.replace(' unsigned cases=65536;',' if(phase==6){patch(0x4A4015,P(table_turn_stop));patch(0x4A45B7,P(table_straight_stop));}\n unsigned cases=65536;')
t=t.replace(' else if(phase==5){',' else if(phase==6)result=ra2_ground_template_table_bridge();\n else if(phase==7)ra2_ground_prepare_written_return_bridge(n%4);\n else if(phase==5){')
t=t.replace('int returned=phase==3||phase==5;', 'int returned=phase==3||phase==5||phase==7;')
t=t.replace('if(phase==4||phase==5){','if(phase==4||phase==5||phase==6||phase==7){')
t=t.replace(' if(phase==0)abi|=g_eax!=native_ax;',' if(phase==7)abi|=g_ecx!=native_cx;\n if(phase==0)abi|=g_eax!=native_ax;')
(S/'overlap_probe.c').write_text(t,encoding='utf-8',newline='\n')
print('Extended probes: table, building flags, four written epilogues with output/frame aliases')
