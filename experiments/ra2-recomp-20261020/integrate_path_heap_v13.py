"""Replace full expanded heap regions and retained internal entry continuations."""
from pathlib import Path
import re,json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v13'
p=R/'ra2/src/recomp/gen_game/recomp_0003.c';t=p.read_text(encoding='utf-8')
t='#include "ground_path_heap_bridge.h"\n'+t
# Full offers and takes are repeated in recovered shared-entry functions.
offer='    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); ra2_path_heap_offer_bridge(); RECOMP_REGS_IN(); RECOMP_FLAGS_IN();\n'
t,n=re.subn(r'    eax = MEM32\(esp \+ 0x1C\); /\* 0x00427914:.*?(?=L_00427A02:)',offer,t,flags=re.S);assert n==7,n
take='    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); ra2_path_heap_take_bridge(); RECOMP_REGS_IN(); RECOMP_FLAGS_IN();\n    if (!MEM32(esp + 0x14)) goto L_00427CA6;\n'
t,m=re.subn(r'L_00427A90:.*?(?=L_00427C96:)', 'L_00427A90:\n'+take,t,flags=re.S);assert m==11,m
# Only these three catalog entries begin partway through an operation.
start=t.index('void sub_00427987(void)');end=t.index('\nvoid ',start+10)
chunk=t[start:end];chunk,k=re.subn(r'L_00427987:.*?(?=L_00427A02:)', 'L_00427987:\n    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); ra2_path_heap_offer_tail_bridge(); RECOMP_REGS_IN(); RECOMP_FLAGS_IN();\n',chunk,flags=re.S);assert k==1;t=t[:start]+chunk+t[end:]
for name,flag in [('00427B1F',1),('00427C22',0)]:
    start=t.index('void sub_'+name+'(void)');end=t.index('\nvoid ',start+10);chunk=t[start:end]
    stop=r'(?=(?:L_00427C96:\n)?    eax = MEM32\(esp \+ 0x14\); /\* 0x00427C96:)'
    chunk,k=re.subn('L_'+name+':.*?'+stop, 'L_'+name+':\n    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); ra2_path_heap_take_tail_bridge('+str(flag)+'); RECOMP_REGS_IN(); RECOMP_FLAGS_IN();\n',chunk,flags=re.S);assert k==1;t=t[:start]+chunk+t[end:]
p.write_text(t,encoding='utf-8')
p=R/'ra2/CMakeLists.txt';t=p.read_text(encoding='utf-8');t+='\ntarget_sources(ra2 PRIVATE src/gameplay/ground_path_heap.c src/runtime/ground_path_heap_bridge.c)\nset_source_files_properties(src/gameplay/ground_path_heap.c src/runtime/ground_path_heap_bridge.c PROPERTIES COMPILE_OPTIONS "/W4;/WX;/std:c17;/utf-8")\n';p.write_text(t,encoding='utf-8')
(S/'heap-integration.json').write_text(json.dumps(dict(full_offer_copies=n,full_take_copies=m,internal_continuations=3),indent=2),encoding='utf-8')
print('Integrated heap',n,m,'plus 3 continuations')
