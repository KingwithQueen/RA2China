from pathlib import Path
ROOT = Path(__file__).resolve().parent
path = ROOT / 'ra2/src/recomp/gen_game/recomp_0046.c'
text = path.read_text(encoding='utf-8')
line = next(line for line in text.splitlines() if '0x007030B6:' in line)
assert text.count(line) == 1
text = text.replace(line, '''    /* 可读 C：地形类别、斜坡子格与桥面高度限制。 */
    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT();
    int terrain_continue_v5 = ra2_ground_terrain_bridge();
    RECOMP_REGS_IN(); RECOMP_FLAGS_IN();
    if (!terrain_continue_v5) return;
    goto L_00703182;
''' + line)
path.write_text(text, encoding='utf-8', newline='\n')
path = ROOT / 'ra2/CMakeLists.txt'
text = path.read_text(encoding='utf-8')
text = text.replace('  src/gameplay/ground_collision.c\n', '  src/gameplay/ground_collision.c\n  src/gameplay/ground_terrain.c\n')
text += '\nset_source_files_properties(src/gameplay/ground_terrain.c PROPERTIES COMPILE_OPTIONS "/W4;/WX;/std:c17;/utf-8")\n'
path.write_text(text, encoding='utf-8', newline='\n')
