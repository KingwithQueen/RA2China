"""按当前 1.006 输入指纹提取小范围汇编及数据引用，不加载完整巨型清单。"""
import argparse
import bisect
import json
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'python_lib'))
import capstone
import pefile

pe = pefile.PE(str(ROOT / 'ra2/game/game.exe'))
image = pe.get_memory_mapped_image()
base = pe.OPTIONAL_HEADER.ImageBase
funcs = json.loads((ROOT / 'ra2/work/game/functions.json').read_text())['functions']
starts = [f['address'] for f in funcs]
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)


def owner(va):
    return funcs[bisect.bisect_right(starts, va) - 1]


def disasm(va, size=None):
    f = owner(va)
    if size is None:
        va, size = f['address'], min(f['end'] - f['address'], 10000)
    print('\n%s 0x%08X size=%d' % (f['name'], va, size))
    for ins in md.disasm(image[va-base:va-base+size], va):
        print('%08X  %-24s %-8s %s' % (ins.address, ins.bytes.hex(' '), ins.mnemonic, ins.op_str))


ap = argparse.ArgumentParser()
ap.add_argument('addresses', nargs='+', type=lambda x: int(x, 0))
ap.add_argument('--xref', action='store_true')
ap.add_argument('--size', type=lambda x: int(x, 0))
args = ap.parse_args()
for va in args.addresses:
    if not args.xref:
        disasm(va, args.size)
        continue
    needle = struct.pack('<I', va)
    pos = image.find(needle, 0x1000, 0x39A000)
    while pos >= 0:
        at = pos + base
        f = owner(at)
        print('ref %08X in %s %08X' % (at, f['name'], f['address']))
        # 从已知函数入口解码，避免把操作数中间当成指令。
        for ins in md.disasm(image[f['address']-base:pos+4], f['address']):
            if ins.address + ins.size > at and ins.address <= at:
                print('  %08X %s %s' % (ins.address, ins.mnemonic, ins.op_str))
        pos = image.find(needle, pos+1, 0x39A000)
