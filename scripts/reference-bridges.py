"""只读原版桥段分支、邻段帧和 R250；显式替代显示、世界通知及桥面对象链。"""
import sys
sys.dont_write_bytecode=True
from native_reference import *
from unicorn import UC_HOOK_CODE

def stub(n,at,cleanup=0,value=0):
    n.uc.mem_write(at,b'\xb8'+u32(value)+(b'\xc2'+struct.pack('<H',cleanup) if cleanup else b'\xc3'))
    n.uc.ctl_remove_cache(at,at+32)

def world():
    n=Native(); n.uc.mem_map(0x17000000,0x100000); n.put(0x832618,0x17000000)
    n.put(0x17000000+(10*512+10)*4,OBJ)
    n.put(OBJ+0x24,10 | (10<<16)); n.put(OBJ+0x38,0); n.put(OBJ+0x44,24); n.put(OBJ+0x140,0x180)
    n.put(0xa52c74,1000); n.put(0xa6cb7c,2000); n.put(0xa52e70,3000)
    n.put(ARG,10 | (10<<16))
    for direction,(x,y) in enumerate(((0,-1),(1,-1),(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1))):
        n.uc.mem_write(0x851a70+4*direction,struct.pack('<hh',x,y))
    for at in (0x631570,0x558bd0,0x5501a0):stub(n,at,4)
    stub(n,0x4732d0,8)
    return n

import json
import subprocess

def compare(exe, option, inputs, expected):
    run = subprocess.run([str(exe), option], input='\n'.join(inputs)+'\n', text=True, capture_output=True, encoding='utf-8')
    assert run.returncode == 0, run.stderr
    actual = run.stdout.splitlines()
    assert len(actual) == len(expected), (option, len(actual), len(expected))
    for i, (a, e) in enumerate(zip(actual, expected)):
        assert a == e, (option, i, inputs[i], a, e)
    return len(inputs)

def main():
    exe, output = Path(sys.argv[1]), Path(sys.argv[2])
    counts = {}
    n = world()
    for at in (0x554750,0x554850,0x554960,0x554d00,0x5550a0,0x5551b0,0x5552c0,0x555690): stub(n,at,8)
    inputs, expected = [], []
    for f in range(18):
        n.uc.mem_write(OBJ+0x11e,bytes((f,))); n.put(OBJ+0x44,24)
        n.run(0x559000,args=u32(ARG),registers={UC_X86_REG_ECX:0x8324e0})
        result = 255 if n.integer(OBJ+0x44) == 0xffffffff else n.uc.mem_read(OBJ+0x11e,1)[0]
        inputs.append(str(f)); expected.append(str(result))
    counts['high_segment_damage'] = compare(exe,'--bridge-damage',inputs,expected)
    n = world(); inputs, expected = [], []
    for base in (0,9):
        for first in (0,1):
            for removal in (0,1):
                at = ({(0,0):0x554850,(1,0):0x554750,(0,1):0x554d00,(1,1):0x554960} if not base else
                      {(0,0):0x5551b0,(1,0):0x5550a0,(0,1):0x555690,(1,1):0x5552c0})[(first,removal)]
                for f in range(base,base+9):
                    n.put(ARG,9 | (10<<16)); n.uc.mem_write(OBJ+0x11e,bytes((f,))); n.put(OBJ+0x44,24)
                    n.run(at,args=u32(ARG)+u32(2),registers={UC_X86_REG_ECX:0x8324e0})
                    result = 255 if n.integer(OBJ+0x44) == 0xffffffff else n.uc.mem_read(OBJ+0x11e,1)[0]
                    inputs.append(f'{f} {first} {removal}'); expected.append(str(result))
    counts['high_neighbor_frames'] = compare(exe,'--bridge-frames',inputs,expected)
    n = Native(); inputs, expected = [], []
    seed=0x1badf00d
    n.put(OBJ,0); n.put(OBJ+4,0); n.put(OBJ+8,103)
    for i in range(250):
        seed=(seed*1664525+1013904223)&0xffffffff; n.put(OBJ+12+i*4,seed)
    for cycle in range(80):
        for low,high in ((0,2),(1,1500),(1,1),(1,65),(1,1501),(0,255),(15,104),(0,0x7ffffffe)):
            value=n.run(0x6388a0,args=u32(low)+u32(high),registers={UC_X86_REG_ECX:OBJ})
            inputs.append(f'{low} {high}'); expected.append(f'{value} {n.integer(OBJ+4)} {n.integer(OBJ+8)}')
    counts['bridge_random_ranges'] = compare(exe,'--random-ranges',inputs,expected)
    n = Native(); inputs,expected=[],[]; accepted=[False]; current_low=[False]
    n.put(0x850ce8,104);n.put(0x850cd8,416);n.put(RULES+0x13a8,1500)
    n.put(ARG+12,TYPE);n.put(STACK+0x34,FACE)
    def reject(uc,address,size,user):
        if address == 0x47f1ed and current_low[0]: return
        accepted[0]=False;uc.reg_write(UC_X86_REG_EIP,STOP)
    def accept(uc,address,size,user):
        accepted[0]=True;uc.reg_write(UC_X86_REG_EIP,STOP)
    n.uc.hook_add(UC_HOOK_CODE,reject,begin=0x47f1ed,end=0x47f1ed)
    n.uc.hook_add(UC_HOOK_CODE,reject,begin=0x47f243,end=0x47f243)
    n.uc.hook_add(UC_HOOK_CODE,accept,begin=0x47f158,end=0x47f158)
    n.uc.hook_add(UC_HOOK_CODE,accept,begin=0x47f229,end=0x47f229)
    for low in (0,1):
        for height in (0,2,8,123):
            for offset in (207,208,209,415,416,520,521):
                for wall in (0,1):
                    for demolition in (0,1):
                        for damage,roll in ((0,1),(1,1),(64,65),(65,65),(66,65),(1500,1500),(1501,1500)):
                            current_low[0]=bool(low)
                            z=height*104+offset
                            n.put(OBJ+0x140,0x100);n.put(OBJ+0x44,74);n.uc.mem_write(OBJ+0x11b,bytes((height,)))
                            n.uc.mem_write(TYPE+0x144,bytes((wall,)));n.put(RULES+0xca8,TYPE if demolition else TYPE+0x100)
                            n.put(FACE+8,z);n.put(STACK+0x30,damage);stub(n,0x6388a0,8,roll)
                            accepted[0]=False
                            n.run(0x47f1ed if low else 0x47f0d2,registers={UC_X86_REG_EDI:OBJ,UC_X86_REG_EBP:ARG})
                            inputs.append(f'{height} {z} {low} {wall} {demolition} {damage} {roll}');expected.append(str(int(accepted[0])))
    counts['bridge_damage_height_wall_random_boundaries']=compare(exe,'--bridge-gates',inputs,expected)
    # 原版撤销桥面时首先对桥面对象链调用强制致命伤害，地面对象链不在此循环中。
    n=Native(); victim,table=TYPE,ARG+0x1000
    n.put(OBJ+0xe4,victim);n.put(OBJ+0xe8,0);n.put(victim,table);n.put(victim+0x30,0);n.put(victim+0x6c,300)
    n.put(table+0x158,STOP+0x800);stub(n,STOP+0x800,24)
    arguments=[]
    def damage_call(uc,address,size,user):
        sp=uc.reg_read(UC_X86_REG_ESP)
        words=struct.unpack('<6I',uc.mem_read(sp+4,24))
        arguments.append({'health':n.integer(words[0]),'distance':words[1],'ignore_defenses':words[4],'prevent_passenger_escape':words[5]})
    n.uc.hook_add(UC_HOOK_CODE,damage_call,begin=STOP+0x800,end=STOP+0x800)
    n.run(0x473000,0x473063,registers={UC_X86_REG_ECX:OBJ})
    assert arguments==[{'health':300,'distance':0,'ignore_defenses':1,'prevent_passenger_escape':1}],arguments
    result={'engine_sha256':ENGINE_HASH,'checks':sum(counts.values()),'cases':counts,'failures':0,'bridge_deck_removal_calls':arguments,
            'scope':'isolated original instructions with explicit world, rendering and object-chain fixtures; live scene acceptance pending'}
    output.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(result))

if __name__=='__main__':main()
