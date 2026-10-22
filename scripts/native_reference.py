"""只读原版 1.006 的隔离指令执行环境，不导入旧项目生成或安装脚本。"""
import sys
sys.dont_write_bytecode = True
sys.path.insert(0, r'H:\开发\研究资料\工具\python_lib')
import hashlib
import struct
from pathlib import Path
import pefile
from unicorn import Uc, UC_ARCH_X86, UC_MODE_32
from unicorn.x86_const import *

ENGINE_HASH = 'fe67fdac5073530a79baec14c4e072b5e7e4c0c462cee9659870c5330e9e6e3e'
OBJ, TYPE, RULES, TABLE, FACE, ARG, LOC = [0x14000000 + i * 0x2000 for i in range(7)]
STACK, STOP, GET_TYPE, SET_FACTOR = 0x15008000, 0x16000000, 0x16000100, 0x16000200

def u32(value): return struct.pack('<I', value & 0xffffffff)
def bits(value): return struct.unpack('<Q', struct.pack('<d', value))[0]

class Native:
    def __init__(self, path=r'H:\开发\运行版本\原版1.006\game.exe'):
        raw = Path(path).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == ENGINE_HASH, '原版 SHA-256 不符，拒绝使用固定地址'
        pe = pefile.PE(data=raw)
        self.uc = uc = Uc(UC_ARCH_X86, UC_MODE_32)
        uc.mem_map(0x400000, (pe.OPTIONAL_HEADER.SizeOfImage + 4095) & ~4095)
        uc.mem_write(0x400000, pe.get_memory_mapped_image())
        for address in (OBJ, 0x15000000, STOP): uc.mem_map(address, 0x10000)
        uc.mem_write(OBJ, u32(TABLE))
        uc.mem_write(TABLE + 0x80, u32(GET_TYPE))
        uc.mem_write(TABLE + 0x338, u32(0x6d8e90))
        uc.mem_write(TABLE + 0x2c, u32(0x70a2d0))
        uc.mem_write(TABLE + 0x4c8, u32(SET_FACTOR))
        uc.mem_write(GET_TYPE, b'\xb8' + u32(TYPE) + b'\xc3')
        # 仅替代外部国家修正和虚函数写回，原版数值分支及转换仍完整执行。
        uc.mem_write(0x4f5a20, bytes.fromhex('d9e8c20400'))
        uc.mem_write(SET_FACTOR, bytes.fromhex('8b4424048981680400008b44240889816c040000c20800'))
        uc.mem_write(OBJ + 0x470, struct.pack('<d', 1.0))
        uc.mem_write(OBJ + 0x5b4, u32(-1))
        uc.mem_write(LOC + 0xc, u32(OBJ))
        uc.mem_write(0x839848, u32(RULES))
        uc.mem_write(TYPE + 0x5a4, u32(1))
        uc.mem_write(TYPE + 0x2c8, u32(500))
        uc.mem_write(TYPE + 0x2d0, struct.pack('<dd', .002, .03))
        uc.mem_write(RULES + 0x690, struct.pack('<dd', 1.0, 1.2))

    def put(self, address, value): self.uc.mem_write(address, u32(value))
    def real(self, address, value): self.uc.mem_write(address, struct.pack('<d', value))
    def integer(self, address): return struct.unpack('<I', self.uc.mem_read(address, 4))[0]
    def raw(self, address): return struct.unpack('<Q', self.uc.mem_read(address, 8))[0]
    def run(self, start, end=STOP, args=b'', registers=None, budget=200000):
        uc = self.uc
        uc.reg_write(UC_X86_REG_ESP, STACK)
        uc.mem_write(STACK, u32(STOP) + args)
        uc.reg_write(UC_X86_REG_FPCW, 0xe7f)
        uc.reg_write(UC_X86_REG_FPSW, 0)
        uc.reg_write(UC_X86_REG_FPTAG, 0xffff)
        if registers:
            for register, value in registers.items(): uc.reg_write(register, value)
        # 隔离片段的出口可能落在已翻译块中部；重建出口邻域，禁止沿旧块越过出口。
        if end != STOP: uc.ctl_remove_cache(end - 0x100, end + 0x100)
        uc.emu_start(start, end, count=budget)
        assert uc.reg_read(UC_X86_REG_EIP) == end, f'原版指令未到达出口：{start:x}, EIP={uc.reg_read(UC_X86_REG_EIP):x}'
        return uc.reg_read(UC_X86_REG_EAX)
