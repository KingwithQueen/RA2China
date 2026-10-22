from pathlib import Path
ROOT=Path(__file__).resolve().parent
p=ROOT/'ra2/src/recomp/gen_game/recomp_0010.c';t=p.read_text(encoding='utf-8')
assert 'ground_continuation_bridge.h' not in t
t='#include "ground_continuation_bridge.h"\n'+t
needle='L_004A1B60:\n';assert t.count(needle)>0
t=t.replace(needle,needle+'''    /* 可读 C：采样推进后的转弯模板接续与碰撞处理。 */
    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT();
    uint32_t continuation_resume_v9 = ra2_ground_continue_turn_bridge();
    RECOMP_REGS_IN(); RECOMP_FLAGS_IN();
    if (continuation_resume_v9 == 0x4A263A) goto L_004A263A;
    goto L_004A1F8D;
''')
p.write_text(t,encoding='utf-8',newline='\n')
p=ROOT/'ra2/CMakeLists.txt';t=p.read_text(encoding='utf-8').replace('  src/gameplay/ground_advance.c\n',
    '  src/gameplay/ground_advance.c\n  src/gameplay/ground_continuation.c\n  src/runtime/ground_continuation_bridge.c\n')
t+='\nset_source_files_properties(src/gameplay/ground_continuation.c src/runtime/ground_continuation_bridge.c PROPERTIES COMPILE_OPTIONS "/W4;/WX;/std:c17;/utf-8")\n'
p.write_text(t,encoding='utf-8',newline='\n')
