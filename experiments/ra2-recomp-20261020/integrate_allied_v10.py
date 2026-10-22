from pathlib import Path
ROOT=Path(__file__).resolve().parent
p=ROOT/'ra2/src/recomp/gen_game/recomp_0046.c'
t=p.read_text(encoding='utf-8'); assert '#include "ground_allied_bridge.h"' not in t
t='#include "ground_allied_bridge.h"\n'+t
needle='L_00703693:\n'; assert needle in t
code='''    /* 可读 C：移动对象分流、友方迎面距离与让路分类。 */
    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT();
    uint32_t allied_resume_v10 = ra2_ground_allied_bridge();
    RECOMP_REGS_IN(); RECOMP_FLAGS_IN();
    if (allied_resume_v10 == 0x7031B1) goto L_007031B1;
    if (allied_resume_v10 == 0x703B5A) goto L_00703B5A;
    if (allied_resume_v10 == 0x70397C) goto L_0070397C;
    if (allied_resume_v10 == 0x70394F) goto L_0070394F;
    goto L_007038EF;
'''
t=t.replace(needle,needle+code);p.write_text(t,encoding='utf-8',newline='\n')
p=ROOT/'ra2/CMakeLists.txt';t=p.read_text(encoding='utf-8')
t=t.replace('  src/gameplay/ground_objects.c\n','  src/gameplay/ground_objects.c\n  src/gameplay/ground_allied.c\n  src/runtime/ground_allied_bridge.c\n')
t+='\nset_source_files_properties(src/gameplay/ground_allied.c src/runtime/ground_allied_bridge.c PROPERTIES COMPILE_OPTIONS "/W4;/WX;/std:c17;/utf-8")\n'
p.write_text(t,encoding='utf-8',newline='\n')
