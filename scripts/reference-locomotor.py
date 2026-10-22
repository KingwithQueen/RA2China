"""原版隔离指令与纯 C 数值路径对照；不启动、修改或安装旧游戏。"""
import sys
sys.dont_write_bytecode = True
import json
import random
import struct
import subprocess
from pathlib import Path
from native_reference import *

def compare(exe, mode, inputs, expected):
    actual = subprocess.check_output([str(exe), mode], input='\n'.join(inputs)+'\n', encoding='ascii').splitlines()
    assert len(actual) == len(expected), (mode, len(actual), len(expected))
    for index, (a, e) in enumerate(zip(actual, expected)):
        assert a == e, f'{mode} #{index}: {inputs[index]}, C={a}, native={e}'
    return len(actual)

def stub(n, address, result, cleanup=0):
    n.uc.mem_write(address, b'\xb8'+u32(result)+(b'\xc2'+struct.pack('<H',cleanup) if cleanup else b'\xc3'))

def main():
    exe, output = map(Path, sys.argv[1:3])
    counts = {}
    n = Native()
    inputs, expected = [], []
    for direction in range(8):
        for sr in range(21):
            for dr in range(21):
                for dh in (-2,-1,0,1,2):
                    src, dst, level, transition = ARG, ARG+0x200, ARG+0x400, ARG+0x404
                    n.uc.mem_write(src,bytes(0x180)); n.uc.mem_write(dst,bytes(0x180))
                    n.uc.mem_write(src+0x11b,bytes((4,sr))); n.uc.mem_write(dst+0x11b,bytes((4+dh,dr)))
                    n.put(level,4); n.put(transition,0)
                    result=n.run(0x4c8730,args=b''.join(u32(v) for v in (dst,direction,level,transition,src)))
                    inputs.append(f'4 {sr} {4+dh} {dr}'); expected.append(str(int(result==0)))
    counts['ground_ramp_edges']=compare(exe,'--slopes',inputs,expected)

    inputs, expected = [], []
    for control in range(64):
        raw = n.uc.mem_read(0x7a0180+control*12,1)[0]
        pointer = n.integer(0x7a00a0+raw*16)
        ended = not raw
        for index in range(72):
            inputs.append(f'{control} {index}')
            if ended: expected.append('0'); continue
            x,y,d=struct.unpack('<iiI',n.uc.mem_read(pointer+index*12,12))
            n.put(LOC+0x58,control); n.put(LOC+0x40,0); n.put(LOC+0x44,0)
            n.uc.mem_write(ARG+0x20,struct.pack('<ii',x,y)); n.put(ARG+0x40,d)
            n.run(0x4a4740,args=u32(ARG)+u32(ARG+0x20)+u32(ARG+0x40),registers={UC_X86_REG_ECX:LOC})
            sx,sy=struct.unpack('<ii',n.uc.mem_read(ARG,8))
            expected.append(f'1 {sx} {sy} {n.integer(ARG+0x40)}')
            if x==y==0: ended=True
    counts['track_points_and_mirrors']=compare(exe,'--tracks',inputs,expected)

    inputs,expected=[],[]
    for delta in range(-1024,1025,7):
        for remainder in range(8):
            n.put(LOC+0x4c,remainder)
            n.run(0x4a23f0,0x4a2422,registers={UC_X86_REG_EBP:LOC,UC_X86_REG_EDI:0})
            factor=n.integer(STACK-4)
            n.uc.mem_write(ARG+0x20,bytes(12)); n.uc.mem_write(ARG+0x40,struct.pack('<iii',delta,0,0))
            n.run(0x7220c0,args=u32(ARG+0x40)+u32(factor),registers={UC_X86_REG_ECX:ARG,UC_X86_REG_EDX:ARG+0x20})
            value=struct.unpack('<i',n.uc.mem_read(ARG,4))[0]
            inputs.append(f'{delta} {remainder}'); expected.append(str(value))
    counts['track_partial_interpolation']=compare(exe,'--partial',inputs,expected)

    n=Native(); inputs,expected=[],[]
    weapon,facing,center=ARG+0x200,ARG+0x300,ARG+0x400
    for offset,value,address in ((0x39c,weapon,STOP+0x400),(0x288,facing,STOP+0x420),(0xa8,center,STOP+0x440)):
        n.put(TABLE+offset,address);stub(n,address,value,4)
    for direction in list(range(0,65536,257))+[1023,1024,1025,64511,64512,64513,65535]:
        for flh in ((150,0,100),(0,0,0),(-150,37,52),(300,-64,-100)):
            n.put(facing,direction);n.uc.mem_write(weapon+4,struct.pack('<iii',*flh))
            n.run(0x6c1830,args=u32(ARG)+u32(0),registers={UC_X86_REG_ECX:OBJ})
            values=struct.unpack('<iii',n.uc.mem_read(ARG,12))
            inputs.append(f'{direction} '+' '.join(map(str,flh)));expected.append(' '.join(map(str,values)))
    counts['muzzle_flat_32_directions']=compare(exe,'--muzzle',inputs,expected)

    n=Native();inputs,expected=[],[]
    warhead=ARG+0x200
    n.put(0xa3d290,ARG+0x1000)
    for base in (1,2,3,65,90,500,10000):
        for radius in (0,1,76,256):
            n.uc.mem_write(warhead+0x124,struct.pack('<f',radius/256))
            for percent in (0.0,0.1,0.5,1.0):
                pbits=struct.unpack('<I',struct.pack('<f',percent))[0]
                n.put(warhead+0x12c,pbits)
                for verses in (0,100,2500,7500,10000):
                    n.real(warhead+0xa0,verses/10000)
                    for distance in sorted(set((0,max(0,radius-1),radius,radius+1))):
                        n.put(RULES+0x1330,10000)
                        value=n.run(0x47e1c0,args=u32(0)+u32(distance),registers={UC_X86_REG_ECX:base,UC_X86_REG_EDX:warhead})
                        # 原版 DamageArea 47ea75 的半径门限位于数值函数之外。
                        if distance>radius: value=0
                        inputs.append(f'{base} {radius*256} {distance} {pbits:x} {verses} 10000');expected.append(str(value))
    for maximum in (0,1,32,64,100,10000):
        n.uc.mem_write(warhead+0x124,struct.pack('<f',76/256))
        n.put(warhead+0x12c,0x3f000000);n.real(warhead+0xa0,1.0);n.put(RULES+0x1330,maximum)
        for distance in (0,1,75,76):
            value=n.run(0x47e1c0,args=u32(0)+u32(distance),registers={UC_X86_REG_ECX:65,UC_X86_REG_EDX:warhead})
            inputs.append(f'65 {76*256} {distance} 3f000000 10000 {maximum}');expected.append(str(value))
    counts['damage_boundaries']=compare(exe,'--damage',inputs,expected)

    n=Native();inputs,expected=[],[]
    other,other_type,other_table,house=0x20000000,0x20002000,0x20004000,0x20006000
    n.uc.mem_map(other,0x10000);n.put(other,other_table);n.put(OBJ+0x1b4,house);n.put(house+0x54f0,-1)
    own_weapon,enemy_weapon,own_warhead,enemy_warhead=ARG+0x200,ARG+0x400,ARG+0x600,ARG+0x800
    n.put(own_weapon,own_weapon+0x20);n.put(own_weapon+0x20+0xac,own_warhead)
    n.put(enemy_weapon,enemy_weapon+0x20);n.put(enemy_weapon+0x20+0xac,enemy_warhead)
    for offset in (0x80,0x84): n.put(TABLE+offset,GET_TYPE)
    for offset in (0x80,0x84): n.put(other_table+offset,STOP+0x500)
    stub(n,STOP+0x500,other_type)
    for table,weapon,coords,k in ((TABLE,own_weapon,OBJ+0x88,0),(other_table,enemy_weapon,other+0x88,1)):
        for offset,result,cleanup,part in ((0x2b8,0,4,0),(0x39c,weapon,4,0x20),(0x48,coords,4,0x40),(0x2c,1,0,0x60)):
            address=STOP+0x600+k*0x100+part;n.put(table+offset,address);stub(n,address,result,cleanup)
    for i in range(5): n.real(RULES+0xd28+i*8, -1.0 if i==4 else 200.0)
    n.uc.mem_write(STOP,b'\xdd\x1d'+u32(ARG+0x1000))
    rng=random.Random(1006)
    for index in range(1600):
        distance=rng.choice((0,255,256,1279,1280,1281,1535,1536,4096))
        strength=rng.choice((100,300,400));health=rng.randint(1,strength)
        verses=rng.choice((2500,7500,10000));enemy_verses=rng.choice((2500,7500,10000))
        attacking=rng.randrange(2);range_=rng.choice((1280,1472));special=rng.choice((0,5000,10000,20000))
        n.put(other+0x88,distance);n.put(other+0x6c,health);n.put(other_type+0xa0,strength)
        n.put(other+0x228,OBJ if attacking else 0);n.real(other_type+0x290,special/10000)
        n.real(own_warhead+0xa0,verses/10000);n.real(enemy_warhead+0xa0,enemy_verses/10000)
        n.put(own_weapon+0x20+0xb4,range_)
        n.run(0x6d7550,STOP+6,args=u32(other)+u32(0xac0188),registers={UC_X86_REG_ECX:OBJ})
        value=int(struct.unpack('<d',n.uc.mem_read(ARG+0x1000,8))[0])
        inputs.append(f'{distance} {health} {strength} {verses} {enemy_verses} {attacking} {range_} {special}')
        expected.append(str(max(1,value)))
    counts['ordinary_threat_scores']=compare(exe,'--threat',inputs,expected)
    result={'passed':True,'engine_sha256':ENGINE_HASH,'checks':sum(counts.values()),'categories':counts,
            'scope':'只读 x86 指令隔离对照；平地零 TurretOffset 的普通坦克；坡向为地面层，桥梁保持阻挡；不等同原版整场运行验收'}
    output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False))

if __name__=='__main__': main()
