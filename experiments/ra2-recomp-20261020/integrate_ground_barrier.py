"""分开接入墙体/覆盖物与闸门，分别保存逐帧对照结果。"""
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ap = argparse.ArgumentParser()
ap.add_argument('part', choices=['overlay', 'gate'])
args = ap.parse_args()
path = ROOT / 'ra2/src/recomp/gen_game/recomp_0046.c'
text = path.read_text(encoding='utf-8')
if args.part == 'overlay':
    old = '    eax = MEM32(ebx + 0x44); /* 0x00703331: mov eax, dword ptr [ebx + 0x44] */'
    new = '''    /* 可读 C：箱子限制、墙体碾压/攻击与同盟优先级。 */
    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT();
    uint32_t overlay_resume = ra2_ground_overlay_bridge();
    RECOMP_REGS_IN(); RECOMP_FLAGS_IN();
    if (!overlay_resume) return;
    goto L_00703439;
''' + old
    assert text.count(old) == 1 and 'overlay_resume' not in text
    text = '#include "ground_barrier_bridge.h"\n' + text.replace(old, new)
    cmake_path = ROOT / 'ra2/CMakeLists.txt'
    cmake = cmake_path.read_text(encoding='utf-8')
    assert 'src/gameplay/ground_barrier.c' not in cmake
    cmake = cmake.replace('  src/gameplay/ground_recovery.c\n', '  src/gameplay/ground_recovery.c\n  src/gameplay/ground_barrier.c\n  src/runtime/ground_barrier_bridge.c\n')
    cmake += '\nset_source_files_properties(src/gameplay/ground_barrier.c src/runtime/ground_barrier_bridge.c PROPERTIES COMPILE_OPTIONS "/W4;/WX;/std:c17;/utf-8")\n'
    cmake_path.write_text(cmake, encoding='utf-8', newline='\n')
else:
    old = '    eax = MEM32(esi + 0x418); /* 0x00703536: mov eax, dword ptr [esi + 0x418] */'
    new = '''    /* 可读 C：闸门状态、同盟通行和敌方障碍处理。 */
    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT();
    uint32_t gate_resume = ra2_ground_gate_bridge();
    RECOMP_REGS_IN(); RECOMP_FLAGS_IN();
    if (!gate_resume) return;
    if (gate_resume == 0x007035ACu) goto L_007035AC;
    goto L_007038FD;
''' + old
    assert text.count(old) == 2 and 'gate_resume' not in text
    text = text.replace(old, new)
path.write_text(text, encoding='utf-8', newline='\n')
print('Integrated barrier part:', args.part)
