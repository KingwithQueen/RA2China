"""原版只读指令夹具：连续状态逐步比较，不把局部结果称为完整游戏验收。"""
import sys
sys.dont_write_bytecode = True
import json
import random
import struct
import subprocess
from pathlib import Path
from native_reference import *


def compare(exe, mode, inputs, expected):
    lines = subprocess.check_output([str(exe), mode], input='\n'.join(inputs) + '\n', encoding='ascii').splitlines()
    assert len(lines) == len(expected), (mode, len(lines), len(expected))
    for i, (actual, wanted) in enumerate(zip(lines, expected)):
        assert actual == wanted, f'{mode} #{i}: input={inputs[i]} C={actual} native={wanted}'


def main():
    exe, output = map(Path, sys.argv[1:3])
    n = Native()
    inputs, expected, traces = [], [], []
    for base in (15, 17):
        # 相邻停靠、临时远点、地表变化及严格小于 500 的边界都连续保留系数。
        current = bits(1.0)
        sequence = [(499, 100, 0)] * 35 + [(500, 100, 0)] * 30 + [(900, 70, 0)] * 25
        sequence += [(900, 70, -1)] * 25 + [(499, 70, -1)] * 35 + [(900, 100, 1)] * 40
        sequence += [(501, 100, 0), (500, 100, 0), (499, 100, 0)] * 10
        for step, (distance, terrain, slope) in enumerate(sequence):
            n.real(STACK + 0x18, terrain / 100)
            n.run(0x4a3d2f, 0x4a3dbe, registers={UC_X86_REG_ESI: 1 if slope > 0 else 0, UC_X86_REG_EDI: 1 if slope < 0 else 0, UC_X86_REG_EBP: LOC})
            target = n.raw(STACK + 0x18)
            n.uc.mem_write(LOC + 0x50, struct.pack('<Q', target))
            n.uc.mem_write(OBJ + 0x468, struct.pack('<Q', current))
            n.uc.mem_write(STACK + 0x24, struct.pack('<Q', current))
            n.put(STACK + 0x30, base)
            n.run(0x4a1196, 0x4a12f8, registers={UC_X86_REG_ESI: TYPE, UC_X86_REG_EDI: distance, UC_X86_REG_EBP: LOC, UC_X86_REG_EBX: 0})
            value = n.raw(OBJ + 0x468)
            n.put(TYPE + 0x5a0, base)
            speed = n.run(0x4c9b10, registers={UC_X86_REG_ECX: OBJ})
            inputs.append(f'{base} 500 20 300 {distance} {terrain} {slope} {current:016x}')
            expected.append(f'{target:016x} {value:016x} {speed}')
            traces.append({'base': base, 'step': step + 1, 'distance': distance, 'terrain': terrain, 'slope': slope, 'factor': f'{value:016x}', 'speed': speed})
            current = value
    compare(exe, '--motion', inputs, expected)
    assert traces[19]['speed'] == 5, '必须覆盖已发现的第 20 步整数边界'

    turns_in, turns_out = [], []
    rng = random.Random(1006)
    for rot in (1, 5, 8, 127):
        for initial in (0, 16000, 32768, 65000):
            tick, target = 100, initial
            n.put(0xa40d2c, tick)
            n.run(0x4b89f0, args=u32(rot), registers={UC_X86_REG_ECX: FACE})
            n.put(FACE, initial)
            n.put(FACE + 4, initial)
            # 包含目标不变、跨零、反转、尚未转完便改向和结束后改向。
            for i in range(80):
                if i % 5: target = rng.randrange(65536)
                tick += rng.randrange(0, 12)
                n.put(0xa40d2c, tick)
                n.put(ARG, target)
                n.run(0x4b8a30, args=u32(ARG), registers={UC_X86_REG_ECX: FACE})
                n.run(0x4b8be0, args=u32(ARG + 8), registers={UC_X86_REG_ECX: FACE})
                turns_in.append(f'{int(i == 0)} {initial} {rot} {target} {tick}')
                # 同目标不重启时，构造函数的起始步是 100。
                turns_out.append(f'{n.integer(FACE+4)&65535} {n.integer(FACE)&65535} {n.integer(FACE+8)} {n.integer(FACE+0x10)} {n.integer(ARG+8)&65535}')
    compare(exe, '--turns', turns_in, turns_out)

    n = Native()
    legacy_in, legacy_out = [], []
    # 直接执行原版查表函数，包括浮点截断、索引边界和正负象限。
    functions = {'s': 0x4ba410, 'i': 0x4ba480, 'c': 0x4ba4d0, 'a': 0x4ba580, 't': 0x4ba600}
    n.uc.mem_write(STOP, b'\xdd\x1d' + u32(ARG + 0x100))
    def legacy(operation, a, b=0.0):
        n.run(functions[operation], STOP + 6, args=struct.pack('<dd', a, b))
        legacy_in.append(f'{operation} {bits(a):016x} {bits(b):016x}')
        legacy_out.append(f'{n.raw(ARG+0x100):016x}')
    for i in range(513):
        legacy('s', float(i*i) + (i % 5) / 100)
        legacy('i', (i - 256) / 17)
        legacy('c', (i - 256) / 17)
        legacy('a', (i - 256) / 256)
        legacy('t', float(i - 256), float((i * 31 % 513) - 256))
    compare(exe, '--legacy', legacy_in, legacy_out)

    n = Native()
    arc_in, arc_out = [], []
    for distance in (1, 32, 64, 128, 255, 256, 499, 500, 768, 1024, 1280, 1472):
        for height in (-312, -104, -68, 0, 36, 104):
            for high in (0, 1):
                for gravity in (3.0, 6.0):
                    speed = n.run(0x47fb70, args=struct.pack('<d', gravity), registers={UC_X86_REG_ECX: distance})
                    # 极短距离采用显式最小速度，以覆盖解算器而不依赖零速异常。
                    speed = max(speed, 16)
                    n.uc.mem_write(ARG, b'\0' * 16)
                    args = u32(distance) + u32(height) + struct.pack('<d', gravity) + u32(ARG)
                    valid = n.run(0x47f9b0, args=args, registers={UC_X86_REG_ECX: high, UC_X86_REG_EDX: speed}) & 255
                    angle = n.raw(ARG) if valid else 0
                    directed = n.run(0x47f8b0, args=args, registers={UC_X86_REG_ECX: high, UC_X86_REG_EDX: speed}) & 255
                    direction = n.integer(ARG) & 65535 if directed else 0
                    derived = n.run(0x47fb70, args=struct.pack('<d', gravity), registers={UC_X86_REG_ECX: distance})
                    arc_in.append(f'{distance} {height} {speed} {bits(gravity):016x} {high}')
                    arc_out.append(f'{valid} {angle:016x} {directed} {direction} {derived}')
    compare(exe, '--arcs', arc_in, arc_out)

    n = Native()
    n.put(0x850c40, 104)
    height_in, height_out = [], []
    for level in (0, 2, 14):
        for ramp in range(21):
            n.uc.mem_write(OBJ + 0x11b, bytes((level, ramp)))
            for x in (0, 1, 64, 127, 128, 192, 254, 255):
                for y in (0, 1, 64, 127, 128, 192, 254, 255):
                    n.put(ARG, x)
                    n.put(ARG + 4, y)
                    value = n.run(0x4706c0, args=u32(ARG), registers={UC_X86_REG_ECX: OBJ})
                    height_in.append(f'{level} {ramp} {x} {y}')
                    height_out.append(str(value))
    compare(exe, '--heights', height_in, height_out)

    n = Native()
    n.put(TABLE + 0x304, STOP + 0x300)
    n.put(TABLE + 0x154, STOP + 0x400)
    n.uc.mem_write(STOP + 0x300, b'\xa1' + u32(ARG + 0x10) + b'\xc3')
    n.uc.mem_write(STOP + 0x400, bytes.fromhex('8b4424048b0485') + u32(ARG + 0x20) + bytes.fromhex('c20400'))
    guard_in, guard_out = [], []
    for guard in (0, 128, 1536, 2560, 5000):
        for primary, secondary in ((1280, 0), (1472, 2048), (512, 256), (3000, 2400)):
            for kind in (-1, 0, 1, 2):
                for special in (0, 1):
                    n.put(TYPE + 0x504, guard)
                    n.put(ARG + 0x10, special)
                    n.put(ARG + 0x20, primary)
                    n.put(ARG + 0x24, secondary)
                    value = n.run(0x6d31e0, args=u32(kind), registers={UC_X86_REG_ECX: OBJ})
                    if value >= 0x80000000: value -= 0x100000000
                    guard_in.append(f'{guard} {primary} {secondary} {kind} {special}')
                    guard_out.append(str(value))
    compare(exe, '--guards', guard_in, guard_out)

    n, math_native = Native(), Native()
    math_native.uc.mem_write(STOP, b'\xdd\x1d' + u32(ARG + 0x100))
    def native_sqrt(value):
        math_native.run(0x4ba410, STOP + 6, args=struct.pack('<d', value))
        return struct.unpack('<d', math_native.uc.mem_read(ARG + 0x100, 8))[0]
    def canonical(value): return value if value & 0x7fffffffffffffff else 0
    launch_in, launch_out = [], []
    gravity_code = STOP + 0x2000
    n.uc.mem_write(gravity_code, b'\xdd\x05' + u32(ARG + 0x300) + b'\xe9' + struct.pack('<i', 0x460397 - (gravity_code + 11)))
    for dx, dy in ((1024, 0), (-1024, 0), (0, 1024), (0, -1024), (768, 768), (-768, 768), (768, -768), (-768, -768), (499, 37), (37, 499)):
        for height in (-104, -68, 0, 36):
            for high, floater in ((0, 0), (1, 0), (0, 1)):
                gravity = 6.0 / (2 if floater else 1)
                distance = int(native_sqrt(float(dx*dx + dy*dy)))
                speed = n.run(0x47fb70, args=struct.pack('<d', gravity), registers={UC_X86_REG_ECX: distance})
                n.put(STACK + 0x7c, dx)
                n.run(0x6cb062, 0x6cb0e7, registers={UC_X86_REG_EAX: dy})
                n.put(STACK + 0x1c, 0)
                n.put(STACK + 0x28, speed)
                n.run(0x6cb1ac, 0x6cb3f1)
                args = u32(distance) + u32(height) + struct.pack('<d', gravity) + u32(ARG)
                valid = n.run(0x47f8b0, args=args, registers={UC_X86_REG_ECX: high, UC_X86_REG_EDX: speed}) & 255
                words = [str(valid)]
                if valid:
                    n.put(STACK + 0x60, n.integer(ARG) & 65535)
                    try: n.run(0x6cb605, 0x6cb6be)
                    except Exception as error: raise RuntimeError(f"launch {(dx,dy,height,high,floater)} EIP={n.uc.reg_read(UC_X86_REG_EIP):x}") from error
                    n.run(0x6cb6be, 0x6cb747)
                    velocity = [n.raw(STACK + offset) for offset in (0x3c, 0x44, 0x4c)]
                    words += [f'{canonical(value):016x}' for value in velocity]
                    position = [3000, 4000, 100]
                    n.put(OBJ + 0x98, TYPE)
                    n.real(ARG + 0x300, gravity)
                    for step in range(20):
                        n.uc.mem_write(STACK + 0xa0, struct.pack('<Q', velocity[2]))
                        n.run(gravity_code, 0x4603c7, registers={UC_X86_REG_EBP: OBJ, UC_X86_REG_EAX: TYPE})
                        velocity[2] = n.raw(STACK + 0xa0)
                        for i in range(3):
                            n.real(ARG + 0x100 + i*8, float(position[i]))
                            n.uc.mem_write(ARG + 0x200 + i*8, struct.pack('<Q', velocity[i]))
                        n.run(0x4642a0, args=u32(ARG + 0x200), registers={UC_X86_REG_ECX: ARG + 0x100})
                        position = [int(value) for value in struct.unpack('<3d', n.uc.mem_read(ARG + 0x100, 24))]
                        words += [str(value) for value in position] + [f'{canonical(velocity[2]):016x}']
                launch_in.append(f'{dx} {dy} {height} 6 {high} {floater}')
                launch_out.append(' '.join(words))
    compare(exe, '--launches', launch_in, launch_out)
    report = {'passed': True, 'engine_sha256': ENGINE_HASH, 'scope': '隔离原版数值指令；显式对象夹具；不是完整原版游戏运行验收',
              'projectile_zero': '正负零规范化为零；其余速度位和整数坐标逐步比较',
              'continuous_motion_steps': len(inputs), 'retarget_turn_steps': len(turns_in), 'legacy_math_cases': len(legacy_in), 'arc_cases': len(arc_in),
              'ramp_height_cases': len(height_in), 'guard_range_cases': len(guard_in), 'launch_cases': len(launch_in), 'projectile_steps': len(launch_in) * 20,
              'sites': {'motion': '0x4a1196..0x4a12f8', 'speed': '0x4c9b10', 'slope_target': '0x4a3d2f..0x4a3dbe', 'facing': '0x4b89f0/0x4b8a30/0x4b8be0', 'ballistic_math': '0x4ba410/480/4d0/580/600', 'arc': '0x47f9b0/0x47f8b0', 'projectile_speed': '0x47fb70', 'ramp_height': '0x4706c0', 'guard_range': '0x6d31e0', 'launch': '0x6cb062..0x6cb0e7/0x6cb1ac..0x6cb3f1/0x6cb605..0x6cb747', 'gravity': '0x460397..0x4603c7', 'position': '0x4642a0'}, 'motion': traces}
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({k: v for k, v in report.items() if k not in ('motion', 'sites')}, ensure_ascii=True))


if __name__ == '__main__': main()
