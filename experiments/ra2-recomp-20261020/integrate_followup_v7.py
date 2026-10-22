from pathlib import Path

ROOT = Path(__file__).resolve().parent
path = ROOT/'ra2/src/recomp/gen_game/recomp_0010.c'
text = path.read_text(encoding='utf-8')
assert 'speed_prepare_bridge' not in text
text = '#include "ground_followup_bridge.h"\n'+text
for label,code in [
    ('004A3C9B', '''    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT();
    ra2_ground_speed_prepare_bridge();
    RECOMP_REGS_IN(); RECOMP_FLAGS_IN();
    goto L_004A3E35;
'''),
    ('004A3E35', '''    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT();
    uint32_t followup_resume_v7 = ra2_ground_followup_bridge();
    RECOMP_REGS_IN(); RECOMP_FLAGS_IN();
    if (!followup_resume_v7) return;
    if (followup_resume_v7 == 0x4A3F9F) goto L_004A3F9F;
    goto L_004A3F8B;
''')]:
    needle = 'L_'+label+':\n'
    print(label,text.count(needle))
    assert text.count(needle)>0
    text = text.replace(needle,needle+'    /* 可读 C：地形速度与第二方向路径准备。 */\n'+code)
path.write_text(text,encoding='utf-8',newline='\n')
path = ROOT/'ra2/CMakeLists.txt'
text = path.read_text(encoding='utf-8').replace('  src/gameplay/ground_template.c\n',
    '  src/gameplay/ground_template.c\n  src/gameplay/ground_followup.c\n  src/runtime/ground_followup_bridge.c\n')
text += '\nset_source_files_properties(src/gameplay/ground_followup.c src/runtime/ground_followup_bridge.c PROPERTIES COMPILE_OPTIONS "/W4;/WX;/std:c17;/utf-8")\n'
path.write_text(text,encoding='utf-8',newline='\n')
