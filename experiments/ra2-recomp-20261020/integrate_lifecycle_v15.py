from pathlib import Path
import argparse,json,re
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v15'
ap=argparse.ArgumentParser();ap.add_argument('part',choices=['entry','route','rebuild']);a=ap.parse_args()
p=R/'ra2/src/recomp/gen_game/recomp_0003.c';t=p.read_text(encoding='utf-8')
call=lambda name:'    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); '+name+'(); RECOMP_REGS_IN(); RECOMP_FLAGS_IN();\n'
if a.part=='entry':
    t='#include "ground_path_lifecycle_bridge.h"\n'+t
    replacement='''    { int prepared; RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); prepared=ra2_path_prepare_bridge(); RECOMP_REGS_IN(); RECOMP_FLAGS_IN();
      if(prepared<=1) goto L_00427D2E;
      if(prepared==2) goto L_00427D1F; }
'''
    t,n=re.subn(r'    edi = MEM32\(esp \+ 0x64\); /\* 0x00427377:.*?(?=L_0042764A:)',replacement,t,flags=re.S);assert n==1,n
    cm=R/'ra2/CMakeLists.txt';c=cm.read_text(encoding='utf-8')
    files='src/gameplay/ground_path_prepare.c src/gameplay/ground_region_route.c src/gameplay/ground_path_rebuild.c src/runtime/ground_path_lifecycle_bridge.c'
    c+=f'\ntarget_sources(ra2 PRIVATE {files})\nset_source_files_properties({files} PROPERTIES COMPILE_OPTIONS "/W4;/WX;/std:c17;/utf-8")\n';cm.write_text(c,encoding='utf-8')
elif a.part=='route':
    assert json.loads((S/'parts/entry-verified/validation.json').read_text())['passed']
    t,n=re.subn(r'L_0042A12A:.*?(?=    _flag_a = \(uint32_t\)\(esi\); _flag_b = \(uint32_t\)\(1\);\n    esi = esi - 1; /\* 0x0042A1A6:)',
        'L_0042A12A:\n'+call('ra2_region_route_publish_bridge')+'L_0042A1A6:\n',t,flags=re.S);assert n>=1,n
else:
    assert json.loads((S/'parts/route-verified/validation.json').read_text())['passed']
    pattern=r'void sub_00428370\(void\) \{.*?\n\}'
    replacement='''void sub_00428370(void) {
    uint32_t _flag_k=FK_NONE,_flag_a=0,_flag_b=0,_cf=0;
    RECOMP_ENTER(0x00428370u);
    ra2_path_rebuild_bridge();
}'''
    t,n=re.subn(pattern,replacement,t,flags=re.S);assert n==1,n
p.write_text(t,encoding='utf-8')
(S/(a.part+'-integration.json')).write_text(json.dumps(dict(passed=True,part=a.part,entries=n),indent=2),encoding='utf-8')
print('Integrated',a.part,n,'entries')
