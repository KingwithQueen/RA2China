"""按原版 PC/RC 恢复内部速度加减，避免卡车第 27 帧一位差异累积。"""
from pathlib import Path
ROOT = Path(__file__).resolve().parent
counts = [0, 0]
for path in (ROOT / 'ra2/src/recomp/gen_game').glob('recomp_*.c'):
    text = path.read_text(encoding='utf-8')
    original = text
    for i, (old, new) in enumerate([
        ('    _st[0] += *(double*)ADDR(ecx + 0x468); /* 0x004A1289: fadd qword ptr [ecx + 0x468] */',
         '    _st[0] = ra2_ground_add_acceleration(*(double*)ADDR(ecx + 0x468), _st[0], g_fpu_cw); /* 0x004A1289: original PC/RC */'),
        ('    fp_push((double)(int32_t)MEM32(esp + 0x30)); /* 0x004A12C1: fild dword ptr [esp + 0x30] */',
         '    fp_push(ra2_ground_apply_deceleration(*(double*)ADDR(ecx + 0x468), (int32_t)MEM32(esp + 0x30),\n'
         '        *(double*)ADDR(esi + 0x2D0), g_fpu_cw)); /* 0x004A12C1..004A12CB: original PC/RC */\n'
         '    goto L_004A12D1;\n'
         '    fp_push((double)(int32_t)MEM32(esp + 0x30)); /* 0x004A12C1: fild dword ptr [esp + 0x30] */')]):
        if new in text:
            counts[i] += text.count(new)
        else:
            counts[i] += text.count(old)
            text = text.replace(old, new)
    if text != original:
        if '#include "unit_movement.h"' not in text:
            text = '#include "unit_movement.h"\n' + text
        path.write_text(text, encoding='utf-8', newline='\n')
assert counts == [1, 1], counts
print('Speed ramp copies:', counts)
