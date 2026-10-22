"""只读原版 1.006 的桥面偏移与显示方向对照，不替代原版整局画面验收。"""
import sys
sys.dont_write_bytecode = True
import json
import math
import struct
import subprocess
from importlib.machinery import SourceFileLoader
from pathlib import Path
from native_reference import Native, ARG, LOC, OBJ, FACE, STOP, u32, UC_X86_REG_ECX, UC_X86_REG_EDX, UC_X86_REG_ESI


def main():
    executable, output = map(Path, sys.argv[1:3])
    native = Native()
    native.put(0x839634, 0)
    offsets = subprocess.check_output([str(executable), '--bridge-offsets'], encoding='ascii').splitlines()
    for line in offsets:
        kind, state, actual = map(int, line.split())
        native.put(OBJ + 0x140, 0x80 if kind < 2 else 0)
        native.put(OBJ + 0x44, 0)
        native.uc.mem_write(OBJ + 0x11b, b'\0')
        native.uc.mem_write(OBJ + 0x11e, bytes([state]))
        # 保留 Get_Draw_Offset 的真实桥梁分支和高度投影；入口前的格坐标夹具为 (200,100)。
        native.run(0x475457, 0x47549e, registers={UC_X86_REG_ESI: OBJ, UC_X86_REG_ECX: 100, UC_X86_REG_EDX: 200})
        # 出口位于弹栈前，格中心的 +15 尚未执行，此处只比较相对偏移。
        expected = native.uc.reg_read(UC_X86_REG_ECX) - 100
        assert actual == expected, (kind, state, actual, expected)

    generator = SourceFileLoader('rendering_chassis', str(Path(__file__).with_name('generate-chassis-tables.py'))).load_module()
    native = Native()
    generator.initialize(native)
    # 显式固定 60 度俯仰补角与 45 度地图旋转，执行原版相机矩阵合成，而非移植尤里地址。
    native.real(0xaf7390, math.pi / 3)
    native.real(0xaf7928, math.pi / 4)
    native.run(0x718c7e, 0x718cb4)
    view = struct.unpack('<12f', native.uc.mem_read(0xaf77a8, 48))
    cell = ARG + 0x1200
    for address, result in ((0x548000, cell), (0x4b8be0, FACE)):
        native.uc.mem_write(address, b'\xb8' + u32(result) + b'\xc2\x04\x00')
        native.uc.ctl_remove_cache(address, address + 32)
    native.put(LOC + 8, OBJ)
    projections = subprocess.check_output([str(executable), '--projections'], encoding='ascii').splitlines()
    maximum = 0.0
    for line in projections:
        index, x, y = map(float, line.split())
        native.put(FACE, int(index) * 2048)
        native.run(0x53d0d0, args=u32(LOC) + u32(ARG) + u32(0))
        matrix = struct.unpack('<12f', native.uc.mem_read(ARG, 48))
        point = [matrix[row * 4] * 30.5 for row in range(3)]
        expected_x = sum(view[i] * point[i] for i in range(3))
        expected_y = -sum(view[4 + i] * point[i] for i in range(3))
        distance = max(abs(x - expected_x), abs(y - expected_y))
        maximum = max(maximum, distance)
        assert distance < 0.8, (index, (x, y), (expected_x, expected_y))
    assert len(offsets) == 72 and len(projections) == 32
    result = dict(passed=True, bridge_offsets=len(offsets), raster_facing_probes=len(projections), max_pixel_error=maximum,
                  original_sha256='fe67fdac5073530a79baec14c4e072b5e7e4c0c462cee9659870c5330e9e6e3e',
                  scope='原版桥面绘制偏移、固定相机数学片段、底盘矩阵与合成标记像素；不是完整原版渲染器逐像素比较')
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
