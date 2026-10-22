from pathlib import Path
import argparse,json,re
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v16'
ap=argparse.ArgumentParser();ap.add_argument('part',choices=['graph','smoothing','postprocess']);a=ap.parse_args()
p=R/'ra2/src/recomp/gen_game/recomp_0003.c';t=p.read_text(encoding='utf-8')
entry,bridge={'graph':('00429B60','ra2_region_search_bridge'),'smoothing':('00428AE0','ra2_path_smooth_bridge'),'postprocess':('004290C0','ra2_path_postprocess_bridge')}[a.part]
if a.part!='graph':
    previous='graph' if a.part=='smoothing' else 'smoothing'
    assert json.loads((S/f'parts/{previous}-verified/validation.json').read_text())['passed']
else:t='#include "ground_path_routing_bridge.h"\n'+t
replacement=f'''void sub_{entry}(void) {{
    uint32_t _flag_k=FK_NONE,_flag_a=0,_flag_b=0,_cf=0;
    RECOMP_ENTER(0x{entry}u);
    {bridge}();
}}'''
t,n=re.subn(r'void sub_'+entry+r'\(void\) \{.*?\n\}',replacement,t,flags=re.S);assert n==1,n
p.write_text(t,encoding='utf-8')
if a.part!='postprocess':
    cm=R/'ra2/CMakeLists.txt';c=cm.read_text(encoding='utf-8')
    files='src/gameplay/ground_region_search.c src/runtime/ground_path_routing_bridge.c' if a.part=='graph' else 'src/gameplay/ground_path_optimize.c'
    c+=f'\ntarget_sources(ra2 PRIVATE {files})\nset_source_files_properties({files} PROPERTIES COMPILE_OPTIONS "/W4;/WX;/std:c17;/utf-8")\n';cm.write_text(c,encoding='utf-8')
(S/(a.part+'-integration.json')).write_text(json.dumps(dict(passed=True,part=a.part,entries=n),indent=2),encoding='utf-8')
print('Integrated',a.part,n,'entry')
