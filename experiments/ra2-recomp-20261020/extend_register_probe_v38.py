"""Signed level boundaries and layer writes overlapping flags and cached pointers."""
from pathlib import Path
R=Path(__file__).resolve().parent;p=R/'evidence/movement-state-v38/overlap_probe.c';t=p.read_text();t='extern unsigned ra2_ground_late_layer_bridge(void);\n'+t
t=t.replace('native_flags,native_cx;','native_flags,native_cx,native_dx;').replace(' mov native_cx,ecx',' mov native_dx,edx\n mov native_cx,ecx')
t=t.replace('STOP(destination_stop,','STOP(late_layer_stop,04A25E8h) STOP(destination_stop,',1)
code=''' if(phase==21||phase==22){
  entry=0x4A25A0;U(frame+0x6C)=P(cells+0x180);U(frame+0x54)=P(cells);
  cells[0x180+0x11B]=(uint8_t)n;cells[0x11B]=(uint8_t)(n>>8);
  U(cells+0x140)=((n>>2)&1?0x100:0)|(n&0xFE);U(cells+0x180+0x140)=((n>>3)&1?0x100:0)|(n&0xFC);
  units[0][0x79]=(uint8_t)n;units[1][0x79]=(uint8_t)(n^0xD3);
  if(phase==21){unsigned alias=n%5;U(drive+0xC)=alias<2?P(units[alias]):alias==2?P(cells+0x141)-0x79:alias==3?P(cells+0x180+0x141)-0x79:frame+0x55-0x79;}
 }
'''
t=t.replace(' if(native_return){',code+' if(native_return){',1)
t=t.replace('unsigned char drive_bytes[128];','unsigned char drive_bytes[128],cell_bytes[0x300];')
t=t.replace(' if(phase==20){memcpy',' if(phase==21||phase==22){memcpy(c->cell_bytes,cells,sizeof(cells));memcpy(c->drive_bytes,drive,sizeof(drive));c->locals[7]=U(frame+0x6C);c->locals[8]=U(frame+0x54);}\n if(phase==20){memcpy',1)
t=t.replace(' if(phase==20)vt[',' if(phase==21)patch(0x4A25E8,P(late_layer_stop));\n if(phase==20)vt[',1)
t=t.replace(' else if(phase==20)ra2_', ' else if(phase==21)result=ra2_ground_late_layer_bridge();\n else if(phase==20)ra2_',1)
t=t.replace(' if(phase==0)abi|=', ' if(phase==21)abi|=g_ecx!=native_cx||g_edx!=native_dx;\n if(phase==0)abi|=',1)
t=t.replace('if(phase==4||phase==5','if(phase==21||phase==4||phase==5')
p.write_text(t,encoding='utf-8',newline='\n')
