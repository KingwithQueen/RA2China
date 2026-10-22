from pathlib import Path
ROOT=Path(__file__).resolve().parent
p=ROOT/'ra2/src/recomp/gen_game/recomp_0046.c'
t=p.read_text(encoding='utf-8'); assert 'ground_entry_bridge.h' not in t
t='#include "ground_entry_bridge.h"\n'+t
needle='L_00703182:\n'; assert t.count(needle)==1
t=t.replace(needle,needle+'''    /* 可读 C：连接方向、桥面占用层、可见性与基础通行。 */
    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT();
    uint32_t entry_resume_v8 = ra2_ground_entry_bridge();
    RECOMP_REGS_IN(); RECOMP_FLAGS_IN();
    if (entry_resume_v8 == 0x703B5A) goto L_00703B5A;
    if (entry_resume_v8 == 0x7031B1) goto L_007031B1;
    goto L_00703331;
''')
p.write_text(t,encoding='utf-8',newline='\n')
p=ROOT/'ra2/CMakeLists.txt'; t=p.read_text(encoding='utf-8').replace('  src/gameplay/ground_collision.c\n','  src/gameplay/ground_collision.c\n  src/gameplay/ground_entry.c\n  src/runtime/ground_entry_bridge.c\n')
t+='\nset_source_files_properties(src/gameplay/ground_entry.c src/runtime/ground_entry_bridge.c PROPERTIES COMPILE_OPTIONS "/W4;/WX;/std:c17;/utf-8")\n'
p.write_text(t,encoding='utf-8',newline='\n')
