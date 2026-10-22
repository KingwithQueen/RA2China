from pathlib import Path
ROOT = Path(__file__).resolve().parent
path = ROOT / 'ra2/src/recomp/gen_game/recomp_0010.c'
text = path.read_text(encoding='utf-8')
assert 'clearance_resume_v5' not in text
def inject(label, body, count):
    global text
    needle = 'L_' + label + ':\n'
    assert text.count(needle) == count, (label, text.count(needle))
    text = text.replace(needle, needle + body)
inject('004A3550', '''    /* 可读 C：覆盖物净空、地面高度与阻挡分流。 */
    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT();
    uint32_t clearance_resume_v5 = ra2_ground_clearance_bridge(0);
    RECOMP_REGS_IN(); RECOMP_FLAGS_IN();
    if (clearance_resume_v5 == 0x4A3C9B) goto L_004A3C9B;
    if (clearance_resume_v5 == 0x4A36ED) goto L_004A36ED;
    if (clearance_resume_v5 == 0x4A364F) goto L_004A364F;
    goto L_004A3A8E;
''', 2)
inject('004A35FE', '''    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT();
    uint32_t clear_resume_v5 = ra2_ground_clearance_bridge(1);
    RECOMP_REGS_IN(); RECOMP_FLAGS_IN();
    if (clear_resume_v5 == 0x4A364F) goto L_004A364F;
    goto L_004A3A8E;
''', 3)
inject('004A364F', '''    /* 可读 C：车辆阻挡的短重试和长等待计时器。 */
    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT();
    uint32_t traffic_resume_v5 = ra2_ground_traffic_wait_bridge();
    RECOMP_REGS_IN(); RECOMP_FLAGS_IN();
    if (!traffic_resume_v5) return;
    goto L_004A3A98;
''', 4)
path.write_text(text, encoding='utf-8', newline='\n')
path = ROOT / 'ra2/CMakeLists.txt'
text = path.read_text(encoding='utf-8')
text = text.replace('  src/gameplay/ground_segment.c\n', '  src/gameplay/ground_segment.c\n  src/gameplay/ground_wait.c\n')
text += '\nset_source_files_properties(src/gameplay/ground_wait.c PROPERTIES COMPILE_OPTIONS "/W4;/WX;/std:c17;/utf-8")\n'
path.write_text(text, encoding='utf-8', newline='\n')
