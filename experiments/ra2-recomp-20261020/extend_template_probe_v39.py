"""Exercise the three loaded continuations at native boundaries, without game-scene inflation."""
from pathlib import Path
R=Path(__file__).resolve().parent;p=R/'evidence/movement-state-v39/overlap_probe.c';t=p.read_text(encoding='utf-8');t='extern unsigned ra2_ground_template_continuation_bridge(unsigned entry);\n'+t
t=t.replace('STOP(late_layer_stop,','STOP(loaded_sample_stop,04A2347h) STOP(sample_done_stop,04A263Ah) STOP(choice_saved_stop,04A24DCh) STOP(choice_raw_stop,04A24F4h) STOP(choice_primary_stop,04A24C6h) STOP(cell_same_stop,04A2607h) STOP(cell_change_stop,04A2586h) STOP(late_layer_stop,',1)
code=''' if(phase==23){
  entry=0x4A2326;ic=n%3==0?frame+0x88:n%3==1?frame+0x8C:P(types[0]);
  ii=(uint32_t)edge[n%11];is=n&1?ii:(uint32_t)edge[(n/11)%11];id=n&4?ii:(uint32_t)edge[(n/121)%11];
  U(ic+4)=n&2?ii:(uint32_t)edge[(n/1331)%11];
 }
 if(phase==24){
  entry=0x4A24A2;is=P(cells);ii=P(cells+0x180);ia=n%3==0?is:n%3==1?ii:P(cells+0x80);
  id=n%4==0?P(units[0]+0x88):n%4==1?frame+0x14:n%4==2?frame+0x18:frame+0x1C;
  for(unsigned j=0;j<3;++j)U(id+j*4)=(uint32_t)edge[(n+j)%11];
  static const int32_t progress[]={INT32_MIN,-1,0,3,4,7,INT32_MAX};U(drive+0x4C)=(uint32_t)progress[(n/3)%7];
 }
 if(phase==25){
  entry=0x4A2528;ic=P(units[0]);id=n%3==0?P(units[0]+0x88):n%3==1?frame+0x60:P(units[1]+0x88);
  U(units[0]+0x88)=(uint32_t)edge[n%11];U(id+4)=(uint32_t)edge[(n/11)%11];U(id+8)=n*31337;
  U(frame+0x18)=n&1?U(units[0]+0x88):(uint32_t)edge[(n/121)%11];U(frame+0x1C)=n&2?U(id+4):(uint32_t)edge[(n/1331)%11];
 }
'''
t=t.replace(' if(native_return){',code+' if(native_return){',1)
t=t.replace(' if(phase==20){memcpy',' if(phase==23){c->locals[0]=U(frame+0x8C);c->locals[1]=U(frame+0x90);}\n if(phase==24){for(unsigned i=0;i<3;++i)c->locals[i]=U(frame+0x18+i*4);}\n if(phase==25){c->locals[0]=U(frame+0x64);c->locals[1]=U(frame+0x18);c->locals[2]=U(frame+0x1C);}\n if(phase==20){memcpy',1)
t=t.replace(' if(phase==21)patch(', ' if(phase==23){patch(0x4A2347,P(loaded_sample_stop));patch(0x4A263A,P(sample_done_stop));}\n if(phase==24){patch(0x4A24DC,P(choice_saved_stop));patch(0x4A24F4,P(choice_raw_stop));patch(0x4A24C6,P(choice_primary_stop));}\n if(phase==25){patch(0x4A2607,P(cell_same_stop));patch(0x4A2586,P(cell_change_stop));}\n if(phase==21)patch(',1)
t=t.replace(' else if(phase==21)result=', ' else if(phase>=23&&phase<=25)result=ra2_ground_template_continuation_bridge(phase-23);\n else if(phase==21)result=',1)
t=t.replace(' if(phase==21)abi|=', ' if(phase>=23&&phase<=25){abi|=g_eax!=native_ax||g_ecx!=native_cx||g_edx!=native_dx;uint32_t flags=recomp_eflags(g_flag_k,g_flag_a,g_flag_b,g_flag_cf,0);abi|=((flags^native_flags)&0x8C5u)!=0;}\n if(phase==21)abi|=',1)
p.write_text(t,encoding='utf-8',newline='\n')
