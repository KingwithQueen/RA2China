"""每部分接入前留存 EXE/源码，拒绝覆盖已有阶段；不重新生成整套提升代码。"""
import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('part', choices=['fraction', 'interpolation', 'transform', 'arrival'])
args = parser.parse_args()
part = args.part
backup = ROOT / 'evidence/movement-readable-v1/parts' / part / 'before'
backup.mkdir(parents=True, exist_ok=False)
files = ['ra2/build-original-c/ra2.exe', 'ra2/CMakeLists.txt', 'ra2/src/recomp/gen_game/recomp_0010.c',
         'ra2/src/recomp/gen_game/recomp_0012.c', 'ra2/src/recomp/gen_game/recomp_0048.c',
         'ra2/src/gameplay/unit_movement.c', 'ra2/src/gameplay/unit_movement.h',
         'ra2/src/runtime/movement_bridge.c', 'ra2/src/runtime/movement_bridge.h',
         'ra2/src/compat/x87_arithmetic.c', 'ra2/src/compat/x87_arithmetic.h',
         'ra2/src/runtime/state_trace.c', 'ra2/src/runtime/state_trace.h']
receipt = []
for relative in files:
    source = ROOT / relative
    destination = backup / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    receipt.append({'path': relative, 'sha256': hashlib.sha256(source.read_bytes()).hexdigest()})
(backup / 'manifest.json').write_text(json.dumps(receipt, indent=2), encoding='utf-8')

shard = ROOT / ('ra2/src/recomp/gen_game/recomp_0048.c' if part == 'interpolation' else 'ra2/src/recomp/gen_game/recomp_0010.c')
text = shard.read_text(encoding='utf-8')
if '#include "movement_bridge.h"' not in text:
    text = '#include "movement_bridge.h"\n' + text
if part == 'fraction':
    old = '(void)fp_pop(); MEM32(esp) = ra2_x87_imul_store_f32((int32_t)MEM32(ebp + 0x4C), MEM64(0x7A05C0), _fpu_cw);'
    assert text.count(old) == 12
    text = text.replace(old, '(void)fp_pop(); MEM32(esp) = ra2_movement_progress_bits((int32_t)MEM32(ebp + 0x4C), _fpu_cw);')
    cmake = ROOT / 'ra2/CMakeLists.txt'
    build = cmake.read_text(encoding='utf-8')
    assert '  src/runtime/movement_bridge.c\n' not in build
    build = build.replace('  src/runtime/x87_precision.c\n', '  src/runtime/x87_precision.c\n  src/runtime/movement_bridge.c\n')
    build = build.replace('set_source_files_properties(src/compat/x87_arithmetic.c src/gameplay/unit_movement.c PROPERTIES',
                          'set_source_files_properties(src/runtime/movement_bridge.c src/compat/x87_arithmetic.c src/gameplay/unit_movement.c PROPERTIES')
    cmake.write_text(build, encoding='utf-8', newline='\n')
elif part in ('interpolation', 'transform'):
    address = '007220C0' if part == 'interpolation' else '004A4740'
    call = 'ra2_movement_interpolate_bridge' if part == 'interpolation' else 'ra2_movement_transform_bridge'
    pattern = rf'void sub_{address}\(void\) \{{.*?\n\}}'
    text, count = re.subn(pattern, f'void sub_{address}(void)\n{{\n    {call}();\n}}', text, count=1, flags=re.S)
    assert count == 1
else:
    if '#include "unit_movement.h"' not in text:
        text = '#include "unit_movement.h"\n' + text
    needle = '    ra2_state_phase(esp, ebp, NULL, &_st[0]);\n    RECOMP_CALL(sub_0077F110); /* 0x004A202B: call 0x77f110 */'
    assert text.count(needle) == 6
    replacement = ('    /* 保留原始共享尾部的入口标签和 __ftol 的 ABI 副作用，将到达补偿公式交给可读模块。 */\n'
                   '    _st[0] = (double)ra2_ground_arrival_progress_adjustment((int32_t)MEM32(esp + 0x34),\n'
                   '        &ra2_original_ground_path_sampling, _fpu_cw);\n' + needle)
    text = text.replace(needle, replacement)
shard.write_text(text, encoding='utf-8', newline='\n')
print(json.dumps({'part': part, 'before_exe_sha256': receipt[0]['sha256'], 'backup': str(backup)}, ensure_ascii=False))
