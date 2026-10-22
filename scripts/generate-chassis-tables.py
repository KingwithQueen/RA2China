"""按原版指纹生成坡面基矩阵和转向三角系数；输出仅含数值表。"""
import sys
sys.dont_write_bytecode=True
import struct
from pathlib import Path
from native_reference import *

def initialize(n):
    # 原版高度单位为 104 lepton，格宽 256；只执行矩阵初始化的数学部分。
    n.real(0xaf7388,256.0)
    n.put(0xaf89f8,104)
    n.run(0x717df0)
    n.run(0x717e20)
    n.run(0x718060,0x718c02,budget=2000000)
    for i in range(17,21): n.run(0x590060,registers={UC_X86_REG_ECX:0xaf8608+i*48})

def float_rz(value):
    raw=struct.unpack('<I',struct.pack('<f',value))[0]
    result=struct.unpack('<f',u32(raw))[0]
    if abs(result)>abs(value):raw-=1
    return raw

def angle(n,d):
    n.put(ARG+0xf00,d)
    code=b'\xdb\x05'+u32(ARG+0xf00)+b'\xdc\x0d'+u32(0x79d090)+b'\xd9\x1d'+u32(ARG+0xf04)+b'\xc3'
    n.uc.mem_write(STOP+0x600,code)
    n.run(STOP+0x600)
    return bytes(n.uc.mem_read(ARG+0xf04,4))

if __name__=='__main__':
    n=Native(); initialize(n)
    out=['/* 原版 1.006 坡面基矩阵与 RZ 三角系数；由独立指令执行生成。 */','static const uint32_t ramp_matrix[21][12] = {']
    for i in range(21):out.append('    {'+', '.join(f'0x{x:08x}u' for x in struct.unpack('<12I',n.uc.mem_read(0xaf8608+i*48,48)))+'},')
    out+=['};','static const struct { uint64_t sine; uint32_t cosine; } matrix_rotation[63] = {']
    angles=[angle(n,d) for d in range(-31,32)]
    n=Native()
    n.uc.mem_write(STOP,b'\xdd\x1d'+u32(ARG+0xf10))
    n.uc.ctl_remove_cache(STOP, STOP+0x100)
    for d in range(-31,32):
        arg=struct.unpack('<f',angles[d+31])[0]
        n.run(0x4ba480,STOP+6,args=struct.pack('<d',arg)); sine=n.raw(ARG+0xf10)
        n.run(0x4ba4d0,STOP+6,args=struct.pack('<d',arg)); cosine=float_rz(struct.unpack('<d',n.uc.mem_read(ARG+0xf10,8))[0])
        out.append(f'    {{UINT64_C(0x{sine:016x}), 0x{cosine:08x}u}},')
    out+=['};','']
    Path('src/battle_matrix.inc').write_text('\n'.join(out),encoding='utf-8',newline='\n')
    print('generated 21 ramp matrices, 63 rotations')


