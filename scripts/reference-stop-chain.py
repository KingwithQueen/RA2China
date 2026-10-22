"""在隔离内存中执行原版 1.006 的窄指令路径；产品不依赖此验证工具。"""
import sys
sys.dont_write_bytecode = True
sys.path.insert(0, r'H:\开发\研究资料\工具\python_lib')
import hashlib, json, struct, subprocess
from pathlib import Path
import pefile
from unicorn import Uc, UC_ARCH_X86, UC_MODE_32
from unicorn.x86_const import *

ENGINE_HASH = 'fe67fdac5073530a79baec14c4e072b5e7e4c0c462cee9659870c5330e9e6e3e'
OBJ, TYPE, RULES, TABLE = 0x14000000, 0x14002000, 0x14004000, 0x14006000
FACE, ARG, LOC = 0x14008000, 0x14009000, 0x1400a000
STACK, STOP, GET_TYPE = 0x15008000, 0x16000000, 0x16000100
def u32(x): return struct.pack('<I', x & 0xffffffff)
def integer(uc, at): return struct.unpack('<I', uc.mem_read(at, 4))[0]
def double(uc, at): return struct.unpack('<d', uc.mem_read(at, 8))[0]

def main():
    exe = Path(sys.argv[1]); output = Path(sys.argv[2])
    raw = exe.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == ENGINE_HASH, '原版指纹不符，拒绝固定地址'
    pe = pefile.PE(data=raw); mapped = pe.get_memory_mapped_image()
    uc = Uc(UC_ARCH_X86, UC_MODE_32)
    uc.mem_map(0x400000, (pe.OPTIONAL_HEADER.SizeOfImage + 4095) & ~4095); uc.mem_write(0x400000, mapped)
    for at in (OBJ, 0x15000000, STOP): uc.mem_map(at, 0x10000)
    uc.mem_write(OBJ, u32(TABLE)); uc.mem_write(TABLE+0x80, u32(GET_TYPE)); uc.mem_write(TABLE+0x338, u32(0x6d8e90))
    uc.mem_write(TABLE+0x2c, u32(0x70a2d0)); uc.mem_write(GET_TYPE, b'\xb8' + u32(TYPE) + b'\xc3')
    # 只替代外部国家速度修正，固定为 1；原版速度换算和浮点取整代码完整执行。
    uc.mem_write(0x4f5a20, bytes.fromhex('d9e8c20400'))
    uc.mem_write(OBJ+0x470, struct.pack('<d',1.0)); uc.mem_write(OBJ+0x5b4,u32(-1))
    uc.mem_write(0x839848,u32(RULES)); uc.mem_write(LOC+0xc,u32(OBJ)); uc.mem_write(TYPE+0x5a4,u32(1))
    uc.mem_write(RULES+0x690,struct.pack('<dd',1.0,1.2))
    def run(start, end=STOP, args=b''):
        uc.reg_write(UC_X86_REG_ESP, STACK); uc.mem_write(STACK,u32(STOP)+args)
        uc.reg_write(UC_X86_REG_FPCW,0xe7f); uc.emu_start(start,end,count=10000)
        assert uc.reg_read(UC_X86_REG_EIP)==end, f'指令预算耗尽 {start:x}'
    import math
    cases=[]
    for base in (15,17):
        factor=1.0
        uc.mem_write(TYPE+0x5a0,u32(base))
        uc.mem_write(TYPE+0x2c8,u32(500)); uc.mem_write(TYPE+0x2d0,struct.pack('<d',.002))
        trace=[]
        for tick in range(1,33):
            uc.mem_write(STACK+0x30,u32(base)); uc.mem_write(STACK+0x24,struct.pack('<d',factor))
            uc.reg_write(UC_X86_REG_ESI,TYPE); uc.reg_write(UC_X86_REG_EDI,256); uc.reg_write(UC_X86_REG_EBP,LOC)
            run(0x4a1196,0x4a1223)
            factor=double(uc,STACK+0x24)
            uc.mem_write(OBJ+0x468,struct.pack('<d',factor)); uc.reg_write(UC_X86_REG_ECX,OBJ)
            run(0x4c9b10)
            ideal=max(3000,10000-tick*base*20)
            trace.append({'update':tick,'native_factor':factor,'native_factor_bits':struct.pack('<d',factor).hex(),
                          'native_leptons':uc.reg_read(UC_X86_REG_EAX),'fixed_decimal_factor':ideal,
                          'ideal_fraction_leptons':base*ideal//10000})
        cases.append({'base':base,'rows':trace})
    report={'engine_sha256':ENGINE_HASH,'scope':'原版连续减速窄路径：距离固定256 lepton、基础速度15或17、国家修正1；不是完整移动轨迹',
            'sites':['0x4a1196..0x4a1223','0x4c9b10'],'status':'采样完成，完整连续减速的C校准仍待实施',
            'cases':cases}
    with output.open('w',encoding='utf-8',newline='\n') as f: json.dump(report,f,ensure_ascii=False,indent=2)
    print(json.dumps({'sampled':True,'samples':sum(len(c['rows']) for c in cases),
                      'integer_boundary_differences':sum(r['native_leptons']!=r['ideal_fraction_leptons'] for c in cases for r in c['rows'])}))
if __name__=='__main__': main()
