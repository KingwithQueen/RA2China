"""把已通过原版机器码探针的路段收尾接入现有 C；不重新生成分片。"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
path = ROOT / 'ra2/src/recomp/gen_game/recomp_0010.c'
text = path.read_text(encoding='utf-8')
old = '    MEM8(edi + 0x5A0) = (uint8_t)(1); /* 0x004A2034: mov byte ptr [edi + 0x5a0], 1 */'
new = '''    /* 可读 C：路段结束后的落位、到达确认和任务收尾；原标签保留给共享尾部入口。 */
    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT();
    uint32_t arrival_resume = ra2_ground_finish_segment_bridge();
    RECOMP_REGS_IN(); RECOMP_FLAGS_IN();
    if (arrival_resume == 0) return;
    goto L_004A1FA1;
''' + old
assert text.count(old) == 6
assert 'arrival_resume' not in text
text = '#include "ground_arrival_bridge.h"\n' + text.replace(old, new)
path.write_text(text, encoding='utf-8', newline='\n')
path = ROOT / 'ra2/CMakeLists.txt'
text = path.read_text(encoding='utf-8')
assert 'src/gameplay/ground_arrival.c' not in text
text = text.replace('  src/gameplay/ground_collision.c\n', '  src/gameplay/ground_collision.c\n  src/gameplay/ground_arrival.c\n  src/runtime/ground_arrival_bridge.c\n')
text += '\nset_source_files_properties(src/gameplay/ground_arrival.c src/runtime/ground_arrival_bridge.c PROPERTIES COMPILE_OPTIONS "/W4;/WX;/std:c17;/utf-8")\n'
path.write_text(text, encoding='utf-8', newline='\n')
print('Integrated 6 segment-finish entries; preserved old shared labels.')
