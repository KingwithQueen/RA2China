"""接入障碍观察完整双入口，不改动后续路径模板选择。"""
from pathlib import Path
ROOT = Path(__file__).resolve().parent
path = ROOT / 'ra2/src/recomp/gen_game/recomp_0010.c'
text = path.read_text(encoding='utf-8')
assert 'obstacle_resume' not in text
for address, rebuilt in [('004A2A83', 0), ('004A2F7A', 1)]:
    old = next(line for line in text.splitlines() if f'0x{address}:' in line)
    assert text.count(old) == 1
    new = f'''    /* 可读 C：相邻格观察、请求开闸、友军让路和近距离停止。 */
    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT();
    uint32_t obstacle_resume_{rebuilt} = ra2_ground_observe_obstacle_bridge({rebuilt});
    RECOMP_REGS_IN(); RECOMP_FLAGS_IN();
    if (!obstacle_resume_{rebuilt}) return;
    if (obstacle_resume_{rebuilt} == 0x004A2DFDu) goto L_004A2DFD;
    goto L_004A32CA;
''' + old
    text = text.replace(old, new)
path.write_text(text, encoding='utf-8', newline='\n')
path = ROOT / 'ra2/CMakeLists.txt'
text = path.read_text(encoding='utf-8')
assert 'src/gameplay/ground_obstacle.c' not in text
text = text.replace('  src/gameplay/ground_prepare.c\n', '  src/gameplay/ground_prepare.c\n  src/gameplay/ground_obstacle.c\n')
text += '\nset_source_files_properties(src/gameplay/ground_obstacle.c PROPERTIES COMPILE_OPTIONS "/W4;/WX;/std:c17;/utf-8")\n'
path.write_text(text, encoding='utf-8', newline='\n')
print('Integrated obstacle observation')
