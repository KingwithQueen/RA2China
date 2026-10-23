"""Exercise both service chains, replacement owner and callback-mutated saved frames."""
from pathlib import Path
R=Path(__file__).resolve().parent;p=R/'evidence/movement-state-v33/overlap_probe.c';t=p.read_text(encoding='utf-8')
t='extern void ra2_ground_prepare_following_return_bridge(unsigned entry);\n'+t
t=t.replace(' default:exit(3);',''' case 14:
  if(number&2)U(drive+0xC)=P(units[1]);
  U(frame+8)=number^0xBADCAFEu;return 0xC0010000u|number;
 case 15:
  ev(a[0]);ev(a[1]);ev(U(a[0]));U(a[0])^=number;
  U(frame+4)=number*91;U(frame+12)=number^0xABCD4321u;
  return 0xFACE0000u|number;
 default:exit(3);''',1)
t=t.replace('static uint32_t __fastcall n_stop','static uint32_t __fastcall n_cleanup(void*c,void*d){(void)d;return dispatch(14,P(c),NULL);}\nstatic uint32_t __fastcall n_sample(void*c,void*d,uint32_t a,uint32_t b){(void)d;uint32_t v[]={a,b};return dispatch(15,P(c),v);}\nstatic uint32_t __fastcall n_stop',1)
t=t.replace('L(l_stop,','L(l_cleanup,14,0) L(l_sample,15,2) L(l_stop,',1)
t=t.replace('recomp_func_t recomp_lookup_manual(uint32_t a){','recomp_func_t recomp_lookup_manual(uint32_t a){if(a==0x4CD9B0)return l_cleanup;if(a==0x4A0BC0)return l_sample;',1)
t=t.replace(' if(native_return){',''' if(phase==14){entry=n%2?0x4A46BD:0x4A456E;return_slot=frame+0x5C;ic=P(units[0]);U(frame+0x38)=n*733;}
 if(native_return){''',1)
t=t.replace(' if(phase==13){for(unsigned i=', ' if(phase==14){for(unsigned i=0;i<4;++i)c->locals[i]=U(frame+i*4);c->locals[4]=U(frame+0x38);c->locals[5]=U(drive+0xC);}\n if(phase==13){for(unsigned i=',1)
t=t.replace(' if(phase==13){vt', ' if(phase==14){patch(0x4CD9B0,P(n_cleanup));patch(0x4A0BC0,P(n_sample));vt[0x414/4]=P(n_exit2);}\n if(phase==13){vt',1)
t=t.replace(' else if(phase==13)ra2_', ' else if(phase==14)ra2_ground_prepare_following_return_bridge(n%2);\n else if(phase==13)ra2_',1)
t=t.replace('phase==13||(phase==11','phase==13||phase==14||(phase==11')
t=t.replace('phase==11||phase==13){','phase==11||phase==13||phase==14){')
p.write_text(t,encoding='utf-8',newline='\n')
