"""Loaded table/offset differ from cached and global selections."""
from pathlib import Path
R=Path(__file__).resolve().parent;p=R/'evidence/movement-state-v35/tube_state_probe.c';t=p.read_text(encoding='utf-8')
a=' if(phase==3){static const int32_t edges[]='
b=' if(phase==5){entry=0x4A2320;ip=P(drive);U(drive+0xC)=P(unit);U(drive+0x5C)=(n+7)%16;id=n%16;ic=(n/16)%44;ii=(n/704)%3?0:n%7;\n  for(unsigned i=0;i<8;++i){U(0x7A00A0+i*16)=P(samples[(i+3)%8]);for(unsigned j=0;j<48;++j)samples[i][j]=j%5?(int32_t)(n+i+j):0;}\n  ia=P(samples[(n/2112)%8]);if(n%3==0){U(ia+ic*4)=ii;U(ia+ic*4+4)=ii;}}\n'
assert a in t;t=t.replace(a,b+a,1).replace('phase==1||phase==4','phase==1||phase==4||phase==5').replace('phase==4?65536','phase>=4?65536')
t=t.replace('  else if(phase==4)result=', '  else if(phase==5)result=ra2_ground_internal_handoff_bridge(4);\n  else if(phase==4)result=',1).replace('  if(phase==4)abi|=', '  if(phase>=4)abi|=')
p.write_text(t,encoding='utf-8',newline='\n')
