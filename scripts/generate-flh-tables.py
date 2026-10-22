"""读取原版平地炮口矩阵的 32 个方向系数，保持生成物只含数值。"""
import sys
sys.dont_write_bytecode=True
import struct
from pathlib import Path
from native_reference import *
n=Native()
weapon, facing, center = ARG+0x200, ARG+0x300, ARG+0x400
for offset, value, cleanup, stub in ((0x39c,weapon,4,STOP+0x400),(0x288,facing,4,STOP+0x420),(0xa8,center,4,STOP+0x440)):
    n.put(TABLE+offset,stub)
    n.uc.mem_write(stub,b'\xb8'+u32(value)+b'\xc2'+struct.pack('<H',cleanup))
rows=[]
for d in range(32):
    n.put(facing,d*2048)
    n.run(0x6c1830,0x6c198d,args=u32(ARG)+u32(0),registers={UC_X86_REG_ECX:OBJ})
    rows.append(struct.unpack('<12I',n.uc.mem_read(STACK-0x90,48)))
text=['/* 平地炮口的原版 32 向 float 矩阵；生成器校验原版文件指纹。 */','static const uint32_t flh_matrix[32][12] = {']
for row in rows: text.append('    {'+', '.join(f'0x{x:08x}u' for x in row)+'},')
text+=['};','']
Path('src/battle_flh.inc').write_text('\n'.join(text),encoding='utf-8',newline='\n')
print('generated muzzle matrices',len(rows))
