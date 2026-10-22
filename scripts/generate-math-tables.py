"""从公开数学函数生成确定性查表数据；不读取游戏、资源或旧项目。"""
import math
import struct
from pathlib import Path


def float_bits(value):
    bits = struct.unpack('<I', struct.pack('<f', value))[0]
    rounded = struct.unpack('<f', struct.pack('<I', bits))[0]
    if abs(rounded) > abs(value): bits -= 1
    return bits


def float_value(value): return struct.unpack('<f', struct.pack('<I', float_bits(value)))[0]


def main():
    sine = [float_bits(math.sin(i * math.pi / 4096)) for i in range(2049)]
    arcsine = [float_bits(math.asin(i / 2048)) for i in range(2049)]
    step = struct.unpack('<f', struct.pack('<I', 0x3cc7fe84))[0]
    value, arctangent = 0.0, []
    for _ in range(4097):
        arctangent.append(float_bits(math.atan(value)))
        value = float_value(value + step)
    lines = ['/* 数学公式生成的单精度向零查表值；可用 scripts/generate-math-tables.py 重建。 */', '#ifndef RA2_BATTLE_TRIG_TABLES_H', '#define RA2_BATTLE_TRIG_TABLES_H']
    for name, values in (('sine', sine), ('arcsine', arcsine), ('arctangent', arctangent)):
        lines += [f'static const uint32_t battle_{name}_table[{len(values)}] = {{']
        lines += ['    ' + ', '.join(f'0x{x:08x}u' for x in values[i:i+10]) + ',' for i in range(0, len(values), 10)]
        lines += ['};']
    lines += ['#endif', '']
    (Path(__file__).resolve().parent.parent / 'src' / 'battle_trig_tables.h').write_text('\n'.join(lines), encoding='utf-8', newline='\n')


if __name__ == '__main__': main()
