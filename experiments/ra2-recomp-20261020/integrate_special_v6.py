from pathlib import Path
ROOT = Path(__file__).resolve().parent
path = ROOT/'ra2/src/recomp/gen_game/recomp_0010.c'
text = path.read_text(encoding='utf-8')
needle = 'L_004A36ED:\n'
assert text.count(needle)==2 and 'special_resume_v6' not in text
text = text.replace(needle,needle+'''    /* 可读 C：临时阻挡、隐形揭露、单次递归及桥层通知。 */
    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT();
    uint32_t special_resume_v6 = ra2_ground_special_obstacle_bridge();
    RECOMP_REGS_IN(); RECOMP_FLAGS_IN();
    if (!special_resume_v6) return;
    goto L_004A35FE;
''')
path.write_text(text,encoding='utf-8',newline='\n')
path = ROOT/'ra2/CMakeLists.txt'
text = path.read_text(encoding='utf-8')
text = text.replace('  src/gameplay/ground_reaction.c\n','  src/gameplay/ground_reaction.c\n  src/gameplay/ground_special.c\n')
text += '\nset_source_files_properties(src/gameplay/ground_special.c PROPERTIES COMPILE_OPTIONS "/W4;/WX;/std:c17;/utf-8")\n'
path.write_text(text,encoding='utf-8',newline='\n')
