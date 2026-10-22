"""为状态字段、命令布局与本次数值修复保存对应原版指令证据。"""
import hashlib
import json
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'python_lib'))
import capstone
import pefile

source = ROOT / 'ra2/game/game.exe'
fingerprint = hashlib.sha256(source.read_bytes()).hexdigest()
if fingerprint != 'fe67fdac5073530a79baec14c4e072b5e7e4c0c462cee9659870c5330e9e6e3e':
    raise RuntimeError('输入版本不符')
image = pefile.PE(str(source)).get_memory_mapped_image()
regions = [(0x540676, 0x30, '真实模拟帧递增'), (0x53D890, 0x90, '对象逻辑更新边界'),
           (0x40FFD0, 0x25, '对象编号赋值'), (0x663170, 0xE, '场景编号递增'),
           (0x6C11E1, 0x53, 'Techno 全局列表'), (0x638790, 0xA8, '模拟 RNG 构造'),
           (0x638840, 0x51, '模拟 RNG 推进'), (0x4B89D0, 0x54, '方向字段与填充范围'),
           (0x4B6170, 0x7D, 'MEGAMISSION 构造'), (0x6B54A0, 0x66, '对象和地图格稳定目标编码'),
           (0x4B6AB8, 0x164, 'MEGAMISSION 执行与生命字段'), (0x4C61A0, 0x16E, '原版事件入队片段'),
           (0x4A23F0, 0x3C, '发生差异的整数乘系数和单精度存储'),
           (0x7220C0, 0x72, '三维向量插值'), (0x4C9B10, 0xA6, '后续差异可继续调查的移动速度入口')]
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
evidence = ROOT / 'evidence/state-step-v1'
with (evidence / 'verified-layout.asm').open('w', encoding='utf-8', newline='\n') as out:
    for va, size, role in regions:
        out.write('\n; %s 0x%08X\n' % (role, va))
        for ins in md.disasm(image[va - 0x400000:va - 0x400000 + size], va):
            out.write('%08X  %-25s %-9s %s\n' % (ins.address, ins.bytes.hex(' '), ins.mnemonic, ins.op_str))
coefficient = struct.unpack_from('<Q', image, 0x7A05C0 - 0x400000)[0]
if coefficient != 0x3FC2492492492492:
    raise RuntimeError('移动系数不符')
report = {'input_sha256': fingerprint, 'regions': [{'address': hex(a), 'length': n, 'role': s} for a, n, s in regions],
          'move_coefficient_bits': '%016x' % coefficient, 'frame_counter': '0x00A40D2C', 'boundary': '0x0053D890 entry',
          'object_key': 'AbstractClass +0x10, sorted; owner normalized to HouseClass vector index',
          'fields': {'health': 'ObjectClass +0x6C', 'position': 'ObjectClass +0x88/+0x8C/+0x90',
                     'mission': 'MissionClass +0x98/+0x9C/+0xA0', 'facings': 'Techno +0x2C8/+0x2E0/+0x2F8; 16/16/32/32/16 bit fields',
                     'rng': 'Scenario +0x218 flag, +0x21C/+0x220 indices, +0x224 250 uint32 words',
                     'house_24c': 'raw scalar at +0x24C; full resource semantics not claimed'},
          'excluded_proven_padding': {'rng': '+1..+3', 'facing': '+2..+3, +6..+7, timer +0xC, +0x16..+0x17',
                                       'x87_control': 'reserved bits, compared mask 0x1F3F'},
          'not_yet_covered': ['all object targets', 'production queues', 'full resource accounting', 'selection/attack/production commands',
                              'original CRC coverage', 'whole game state', 'all x87 operations'],
          'unsupported_instruction_failure_guards_retained': 37}
(evidence / 'verified-layout.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print('Verified regions:', len(regions), 'move coefficient:', '%016x' % coefficient)
