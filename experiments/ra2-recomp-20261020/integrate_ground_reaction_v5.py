from pathlib import Path
ROOT = Path(__file__).resolve().parent
path = ROOT/'ra2/src/recomp/gen_game/recomp_0010.c'
text = path.read_text(encoding='utf-8')
assert 'ra2_ground_reaction_bridge(' not in text
counts = {}
for label,entry in [('004A3A8E',0),('004A3A98',1),('004A3ACF',2),('004A3BFD',3)]:
    needle = 'L_'+label+':\n'
    counts[label] = text.count(needle)
    assert counts[label] > 0
    text = text.replace(needle,needle+f'''    /* 可读 C：阻挡响应、递归重试、障碍攻击和停止。 */
    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT();
    ra2_ground_reaction_bridge({entry});
    RECOMP_REGS_IN(); RECOMP_FLAGS_IN();
    return;
''')
path.write_text(text,encoding='utf-8',newline='\n')
print('Reaction entries:',counts)
path = ROOT/'ra2/CMakeLists.txt'
text = path.read_text(encoding='utf-8')
text = text.replace('  src/gameplay/ground_wait.c\n','  src/gameplay/ground_wait.c\n  src/gameplay/ground_reaction.c\n')
text += '\nset_source_files_properties(src/gameplay/ground_reaction.c PROPERTIES COMPILE_OPTIONS "/W4;/WX;/std:c17;/utf-8")\n'
path.write_text(text,encoding='utf-8',newline='\n')
