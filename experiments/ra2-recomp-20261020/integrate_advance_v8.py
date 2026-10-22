from pathlib import Path
ROOT=Path(__file__).resolve().parent
p=ROOT/'ra2/src/recomp/gen_game/recomp_0010.c'
t=p.read_text(encoding='utf-8')
assert 'ground_advance_bridge.h' not in t
t='#include "ground_advance_bridge.h"\n'+t
needle='L_004A16A6:\n'
assert t.count(needle)>0
t=t.replace(needle,needle+'''    /* 可读 C：路径采样放置、桥面层、列车碰撞与朝向更新。 */
    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT();
    uint32_t advance_resume_v8 = ra2_ground_advance_sample_bridge();
    RECOMP_REGS_IN(); RECOMP_FLAGS_IN();
    if (advance_resume_v8 == 0x4A263A) goto L_004A263A;
    goto L_004A1B60;
''')
p.write_text(t,encoding='utf-8',newline='\n')
p=ROOT/'ra2/CMakeLists.txt'
t=p.read_text(encoding='utf-8').replace('  src/gameplay/ground_path.c\n','  src/gameplay/ground_path.c\n  src/gameplay/ground_advance.c\n  src/runtime/ground_advance_bridge.c\n')
t+='\nset_source_files_properties(src/gameplay/ground_advance.c src/runtime/ground_advance_bridge.c PROPERTIES COMPILE_OPTIONS "/W4;/WX;/std:c17;/utf-8")\n'
p.write_text(t,encoding='utf-8',newline='\n')
