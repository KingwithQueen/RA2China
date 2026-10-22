"""Compare every newly shared native epilogue, including AL and live flags."""
from pathlib import Path
R = Path(__file__).resolve().parent
S = R / 'evidence/movement-state-v28'
p = S / 'overlap_probe.c'
t = p.read_text(encoding='utf-8')
assert 'remaining_return_cases.h' not in t
t = t.replace('#include "ground_joint_bridge.h"', '#include "ground_joint_bridge.h"\n#include "remaining_return_cases.h"')
marker = ' if(native_return){'
assert t.count(marker) == 1
t = t.replace(marker, ''' if(phase==5){const struct ReturnCase *c=&return_cases[n%(sizeof(return_cases)/sizeof(return_cases[0]))];entry=c->address;return_slot=frame+(c->kind==RA2_FRAME_PREPARE?0x5C:0x78);}
'''+marker)
marker = ' else if(phase==4)result=ra2_ground_template_layer_bridge();'
assert t.count(marker) == 1
t = t.replace(marker, marker+'''
 else if(phase==5){const struct ReturnCase *c=&return_cases[n%(sizeof(return_cases)/sizeof(return_cases[0]))];uint32_t value=c->mode==0?g_eax:c->mode==1?(g_eax&0xFFFFFF00u):c->mode==2?((g_eax&0xFFFFFF00u)|1u):7u;ra2_ground_return_frame(g_esp,c->kind,value);}''')
t = t.replace('int returned=phase==3;', 'int returned=phase==3||phase==5;')
marker = ' if(phase==4){abi|=g_eax!=native_ax;'
assert t.count(marker) == 1
t = t.replace(marker, ' if(phase==4||phase==5){abi|=g_eax!=native_ax;')
p.write_text(t, encoding='utf-8', newline='\n')
p = R / 'run_lifecycle_part_v28.py'
t = p.read_text(encoding='utf-8')
t = t.replace("'passage-shared-exits-probe-verified-01.json'", "'passage-shared-exits-probe-verified-01.json','remaining-exits-probe-verified-01.json'")
p.write_text(t, encoding='utf-8', newline='\n')
print('Added 65536 cases across all 27 newly shared native epilogues')
