from pathlib import Path
ROOT = Path(__file__).resolve().parent
path = ROOT / 'ra2/src/recomp/gen_game/recomp_0010.c'
text = path.read_text(encoding='utf-8')
old = next(line for line in text.splitlines() if '0x004A32CA:' in line)
assert text.count(old) == 2 and 'segment_prepare_resume' not in text
text = text.replace(old, '''    /* 可读 C：路径下一格、高度层、桥面标志、闸门许可及转向等待。 */
    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT();
    uint32_t segment_prepare_resume = ra2_ground_prepare_segment_bridge();
    RECOMP_REGS_IN(); RECOMP_FLAGS_IN();
    if (!segment_prepare_resume) return;
    goto L_004A3550;
''' + old)
# 下一阶段原本顺序落入，接入可读 C 后显式保留恢复标签。
old = next(line for line in text.splitlines() if '0x004A3550:' in line)
assert text.count('L_004A3550:') == 2
path.write_text(text, encoding='utf-8', newline='\n')
path = ROOT / 'ra2/CMakeLists.txt'
text = path.read_text(encoding='utf-8')
assert 'src/gameplay/ground_segment.c' not in text
text = text.replace('  src/gameplay/ground_prepare.c\n', '  src/gameplay/ground_prepare.c\n  src/gameplay/ground_segment.c\n')
text += '\nset_source_files_properties(src/gameplay/ground_segment.c PROPERTIES COMPILE_OPTIONS "/W4;/WX;/std:c17;/utf-8")\n'
path.write_text(text, encoding='utf-8', newline='\n')
