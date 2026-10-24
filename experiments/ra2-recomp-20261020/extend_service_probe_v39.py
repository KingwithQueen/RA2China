"""Position and enter callbacks replace owner, cells, coordinates and saved slots."""
from pathlib import Path
R=Path(__file__).resolve().parent;p=R/'evidence/movement-state-v39/overlap_probe.c';t=p.read_text(encoding='utf-8');t='extern void ra2_ground_advance_place_layer_return_bridge(void);\n'+t
t=t.replace('phase==21||phase==22','phase==21||phase==22||phase==26')
t=t.replace(' if(native_return){',' if(phase==26){entry=0x4A2590;return_slot=frame+0xF4;U(frame+0x18)=n*13;U(frame+0x1C)=n*17;U(frame+0x20)=n*23;}\n if(native_return){',1)
t=t.replace('if(phase==22){for(unsigned i=0;i<4','if(phase==22||phase==26){for(unsigned i=0;i<4')
t=t.replace('if(phase==22){vt[','if(phase==22||phase==26){vt[')
t=t.replace(' else if(phase==22)ra2_', ' else if(phase==26)ra2_ground_advance_place_layer_return_bridge();\n else if(phase==22)ra2_',1)
t=t.replace('phase==20||phase==22','phase==20||phase==22||phase==26')
p.write_text(t,encoding='utf-8',newline='\n')
