from pathlib import Path
import json,re
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v14'
assert json.loads((S/'parts/distance-verified/validation.json').read_text())['passed']
p=R/'ra2/src/recomp/gen_game/recomp_0003.c';t=p.read_text(encoding='utf-8');t='#include "ground_path_search_bridge.h"\n'+t
call='    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); ra2_path_search_neighbors_bridge(); RECOMP_REGS_IN(); RECOMP_FLAGS_IN();\n'
t,n=re.subn(r'L_0042764A:\n.*?(?=L_00427CBB:)', 'L_0042764A:\n'+call,t,flags=re.S);assert n==2,n
# Recovered legacy mid-function entries remain callable. Their region decision uses the same named C rule.
call='''    { int allowed; RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); allowed=ra2_path_region_allows_bridge(); RECOMP_REGS_IN(); RECOMP_FLAGS_IN();
      if(!allowed) goto L_00427A7E; }
'''
t,m=re.subn(r'    /\* cmp MEM32\(edx \+ ecx \* 4\), eax \*/.*?(?=L_004277A4:)',call,t,flags=re.S);assert m==3,m
p.write_text(t,encoding='utf-8')
p=R/'ra2/CMakeLists.txt';t=p.read_text(encoding='utf-8');t+='\ntarget_sources(ra2 PRIVATE src/gameplay/ground_path_search.c src/runtime/ground_path_search_bridge.c)\nset_source_files_properties(src/gameplay/ground_path_search.c src/runtime/ground_path_search_bridge.c PROPERTIES COMPILE_OPTIONS "/W4;/WX;/std:c17;/utf-8")\n';p.write_text(t,encoding='utf-8')
(S/'search-integration.json').write_text(json.dumps(dict(complete_neighbor_loops=n,legacy_region_decisions=m,original_range='42764A..427CB5',recovered_partial_entries_retained=True),indent=2),encoding='utf-8')
