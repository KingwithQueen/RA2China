"""逐部分接入路径准备；保留原版共享标签，不重新生成其他模块。"""
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ap = argparse.ArgumentParser()
ap.add_argument('part', choices=['entry', 'retry', 'recovery'])
args = ap.parse_args()
path = ROOT / 'ra2/src/recomp/gen_game/recomp_0010.c'
text = path.read_text(encoding='utf-8')
if args.part == 'entry':
    old = '    /* test LO8(eax), LO8(eax) */ /* 0x004A2690: test al, al */'
    new = '''    /* 可读 C：路径准备入口、等待条件和有效路径队列选择。 */
    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT();
    uint32_t prepare_entry_resume = ra2_ground_prepare_entry_bridge();
    RECOMP_REGS_IN(); RECOMP_FLAGS_IN();
    if (!prepare_entry_resume) return;
    if (prepare_entry_resume == 0x004A285Eu) goto L_004A285E;
    goto L_004A32CA;
''' + old
    assert text.count(old) == 1 and 'prepare_entry_resume' not in text
    text = '#include "ground_prepare_bridge.h"\n' + text.replace(old, new)
    cmake_path = ROOT / 'ra2/CMakeLists.txt'
    cmake = cmake_path.read_text(encoding='utf-8')
    assert 'src/gameplay/ground_prepare.c' not in cmake
    cmake = cmake.replace('  src/gameplay/ground_arrival.c\n', '  src/gameplay/ground_arrival.c\n  src/gameplay/ground_prepare.c\n  src/runtime/ground_prepare_bridge.c\n')
    cmake += '\nset_source_files_properties(src/gameplay/ground_prepare.c src/runtime/ground_prepare_bridge.c PROPERTIES COMPILE_OPTIONS "/W4;/WX;/std:c17;/utf-8")\n'
    cmake_path.write_text(cmake, encoding='utf-8', newline='\n')
elif args.part == 'retry':
    old = '    eax = MEM32(ebp + 0xC); /* 0x004A285E: mov eax, dword ptr [ebp + 0xc] */'
    new = '''    /* 可读 C：重寻路计时器、重建尝试、目标复核和近距离停止。 */
    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT();
    uint32_t retry_path_resume = ra2_ground_retry_path_bridge();
    RECOMP_REGS_IN(); RECOMP_FLAGS_IN();
    if (!retry_path_resume) return;
    if (retry_path_resume == 0x004A2F7Au) goto L_004A2F7A;
    if (retry_path_resume == 0x004A2EACu) goto L_004A2EAC;
    goto L_004A2A83;
''' + old
    assert text.count(old) == 1 and 'retry_path_resume' not in text
    text = text.replace(old, new)
else:
    text = '#include "ground_recovery_bridge.h"\n' + text
    for address, statement, finish_only, copies in [('004A2DFD', 'ecx = MEM32(ebp + 0xC);', 0, 2),
        ('004A2EAC', 'eax = MEM32(esp + 0x14);', 1, 3)]:
        old = next(line for line in text.splitlines() if f'0x{address}:' in line)
        assert old.strip().startswith(statement) and text.count(old) == copies
        new = f'''    /* 可读 C：寻路失败预算、通知与状态收尾，保留共享入口区别。 */
    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT();
    ra2_ground_recover_path_bridge({finish_only});
    RECOMP_REGS_IN(); RECOMP_FLAGS_IN();
    return;
''' + old
        text = text.replace(old, new)
    cmake_path = ROOT / 'ra2/CMakeLists.txt'
    cmake = cmake_path.read_text(encoding='utf-8')
    assert 'src/gameplay/ground_recovery.c' not in cmake
    cmake = cmake.replace('  src/gameplay/ground_prepare.c\n', '  src/gameplay/ground_prepare.c\n  src/gameplay/ground_recovery.c\n  src/runtime/ground_recovery_bridge.c\n')
    cmake += '\nset_source_files_properties(src/gameplay/ground_recovery.c src/runtime/ground_recovery_bridge.c PROPERTIES COMPILE_OPTIONS "/W4;/WX;/std:c17;/utf-8")\n'
    cmake += '\nset_source_files_properties(src/runtime/host.c PROPERTIES COMPILE_OPTIONS "/W3;/utf-8")\n'
    cmake_path.write_text(cmake, encoding='utf-8', newline='\n')
path.write_text(text, encoding='utf-8', newline='\n')
print('Integrated prepare part:', args.part)
