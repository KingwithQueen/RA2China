"""Port node allocation, two-layer cache access, publication and search reset."""
from pathlib import Path
import json,re,shutil
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v13'
assert json.loads((S/'parts/heap-verified/validation.json').read_text())['passed']
for name in ['ground_path_nodes.h','ground_path_nodes.c']:shutil.copy2(S/'pending'/name,R/'ra2/src/gameplay'/name)
for name in ['ground_path_nodes_bridge.h','ground_path_nodes_bridge.c']:shutil.copy2(S/'pending'/name,R/'ra2/src/runtime'/name)
# Name the deferred candidate accurately; no semantic changes to the verified heap.
for rel in ['ra2/src/gameplay/ground_path_heap.h','ra2/src/gameplay/ground_path_heap.c','ra2/src/runtime/ground_path_heap_bridge.c']:
    p=R/rel;t=p.read_text(encoding='utf-8');t=re.sub(r'\bbest\b','pending',t)
    t=t.replace('pending 是旧接口名，表示单独暂存的候选，不保证分数最优。','pending 表示单独暂存的候选，不保证分数最优。')
    p.write_text(t,encoding='utf-8')
p=R/'ra2/src/recomp/gen_game/recomp_0003.c';t=p.read_text(encoding='utf-8');t='#include "ground_path_nodes_bridge.h"\n'+t
counts={}
for lower,start,end in [(1,'004277AC','004277BF'),(0,'004277E1','004277F4')]:
    def replace(m):return m[0].replace('MEM32(ecx + ebp)','ra2_path_cache_stamp_bridge(esi, '+str(lower)+', ebp)')
    t,n=re.subn('L_'+start+':.*?(?=L_'+end+':)',replace,t,flags=re.S);assert n==5,(start,n);counts['stamp-read-'+str(lower)]=n
for lower,address in [(1,'004277C6'),(0,'004277FB')]:
    pattern=r'^.*0x'+address+r'\.\.0x.*$'
    def replace_cost(m):return m[0].replace('*(float*)ADDR(eax + ebp)','ra2_path_cache_cost_bridge(esi, '+str(lower)+', ebp)')
    t,n=re.subn(pattern,replace_cost,t,flags=re.M);assert n==5,(address,n);counts['cost-read-'+str(lower)]=n
for old,new,address in [
    ('ecx = MEM32(eax + ebp);','ecx = ra2_path_cache_stamp_bridge(esi, 1, ebp);','004278DB'),
    ('eax = MEM32(edx + ebp);','eax = ra2_path_cache_stamp_bridge(esi, 0, ebp);','004278F0')]:
    pattern=r'^.*0x'+address+r':.*$'
    t,n=re.subn(pattern,lambda m:m[0].replace(old,new),t,flags=re.M);assert n==7,(address,n);counts['visited-read-'+address]=n
stop=r'(?=    eax = MEM32\(esi \+ 0x6C\); /\* 0x00427A36:)'
call='    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); ra2_path_cache_publish_bridge(0); RECOMP_REGS_IN(); RECOMP_FLAGS_IN();\n'
t,n=re.subn('L_00427A02:.*?'+stop,'L_00427A02:\n'+call,t,flags=re.S);assert n==9,n;counts['publish']=n
t,n=re.subn('L_00427A2C:.*?'+stop,'L_00427A2C:\n'+call.replace('(0)','(1)'),t,flags=re.S);assert n==1,n;counts['publish-cost-tail']=n
call='    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); ra2_path_node_create_bridge(); RECOMP_REGS_IN(); RECOMP_FLAGS_IN();\n'
t,n=re.subn('L_00427D40:.*?(?=L_00427E2A:)','L_00427D40:\n'+call,t,flags=re.S);assert n==1,n;counts['node-initializer']=n
start=t.index('void sub_00427E90(void)');end=t.index('\n/* ',start+10)
t=t[:start]+'''void sub_00427E90(void) {
    uint32_t _flag_k = FK_NONE, _flag_a = 0, _flag_b = 0, _cf = 0;
    RECOMP_ENTER(0x00427E90u);
    ra2_path_search_reset_bridge();
}
'''+t[end:]
p.write_text(t,encoding='utf-8')
p=R/'ra2/CMakeLists.txt';t=p.read_text(encoding='utf-8');t+='\ntarget_sources(ra2 PRIVATE src/gameplay/ground_path_nodes.c src/runtime/ground_path_nodes_bridge.c)\nset_source_files_properties(src/gameplay/ground_path_nodes.c src/runtime/ground_path_nodes_bridge.c PROPERTIES COMPILE_OPTIONS "/W4;/WX;/std:c17;/utf-8")\n';p.write_text(t,encoding='utf-8')
# The same probe now compiles the production files, rather than its staging draft.
p=R/'build-path-nodes-probe-v13.ps1';t=p.read_text(encoding='utf-8').replace('/I pending ','').replace('pending\\ground_path_nodes.c','..\\..\\ra2\\src\\gameplay\\ground_path_nodes.c');p.write_text(t,encoding='utf-8')
(S/'node-cache-integration.json').write_text(json.dumps(counts,indent=2),encoding='utf-8')
print(counts)
