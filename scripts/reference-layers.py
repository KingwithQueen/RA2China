"""桥层、底盘和炮口的原版隔离指令对照，不代替原版整局验收。"""
import sys
sys.dont_write_bytecode=True
import json,struct,subprocess,runpy
from pathlib import Path
from native_reference import *
from unicorn import UC_HOOK_CODE
from importlib.machinery import SourceFileLoader
chassis=SourceFileLoader('chassis_generator',str(Path(__file__).with_name('generate-chassis-tables.py'))).load_module()

def stub(n,address,result,cleanup=0):
    n.uc.mem_write(address,b'\xb8'+u32(result)+(b'\xc2'+struct.pack('<H',cleanup) if cleanup else b'\xc3'))

    n.uc.ctl_remove_cache(address,address+32)

def compare(exe,mode,inputs,expected):
    actual=subprocess.check_output([str(exe),mode],input='\n'.join(inputs)+'\n',encoding='ascii').splitlines()
    assert len(actual)==len(expected),(mode,len(actual),len(expected))
    for i,(a,e) in enumerate(zip(actual,expected)):assert a==e,f'{mode} #{i}: {inputs[i]}, C={a}, native={e}'
    return len(actual)

def main():
    exe,output=map(Path,sys.argv[1:3]);counts={}
    n=Native();chassis.initialize(n)
    cell=ARG+0x1200
    stub(n,0x548000,cell,4);stub(n,0x4b8be0,FACE,4);n.put(LOC+8,OBJ)
    inputs=[];expected=[]
    for ramp in range(21):
        n.uc.mem_write(cell+0x11c,bytes((ramp,)))
        for facing in list(range(0,65536,1024))+[1023,1025,64511,64513,65535]:
            n.put(FACE,facing)
            n.run(0x53d0d0,args=u32(LOC)+u32(ARG)+u32(0))
            values=struct.unpack('<12I',n.uc.mem_read(ARG,48))
            inputs.append(f'{ramp} {facing}');expected.append(' '.join(f'{v if v&0x7fffffff else 0:08x}' for v in values))
    counts['chassis_matrices']=compare(exe,'--chassis',inputs,expected)
    weapon,turret,center,comtable=ARG+0x200,ARG+0x300,ARG+0x400,ARG+0x1600
    for offset,value,address in ((0x39c,weapon,STOP+0x400),(0x288,turret,STOP+0x420),(0xa8,center,STOP+0x440)):
        n.put(TABLE+offset,address);stub(n,address,value,4)
    n.put(OBJ+0x14,4);n.put(OBJ+0x564,LOC);n.put(LOC,comtable);n.put(comtable+0x24,0x53d0d0)
    inputs=[];expected=[]
    for ramp in range(21):
        n.uc.mem_write(cell+0x11c,bytes((ramp,)))
        for body in range(32):
            for target in range(32):
                offset=37 if (body+target)%2 else 0
                flh=(150,0,100) if (body+target)%3 else (-257,37,-100)
                n.put(FACE,body*2048);n.put(turret,target*2048);n.put(TYPE+0x63c,offset);n.uc.mem_write(weapon+4,struct.pack('<iii',*flh))
                n.run(0x6c1830,args=u32(ARG)+u32(0),registers={UC_X86_REG_ECX:OBJ})
                values=struct.unpack('<iii',n.uc.mem_read(ARG,12))
                inputs.append(f'{ramp} {body*2048} {target*2048} {offset} '+' '.join(map(str,flh)));expected.append(' '.join(map(str,values)))
    counts['chassis_muzzles']=compare(exe,'--chassis-muzzle',inputs,expected)
    n=Native();inputs=[];expected=[]
    src,dst,level,transition=ARG,ARG+0x200,ARG+0x400,ARG+0x404
    for height in range(9):
        for sr in (0,1,20):
            for dr in (0,1,20):
                for ff in (0,0x100,0x300):
                    for tf in (0,0x100,0x300):
                        for initial in (0,1):
                            for lev in (-1,0,4,8):
                                n.uc.mem_write(src+0x11b,bytes((4,sr)));n.uc.mem_write(dst+0x11b,bytes((height,dr)))
                                n.put(src+0x140,ff);n.put(dst+0x140,tf);n.put(level,lev);n.put(transition,0)
                                result=n.run(0x4c8730,args=b''.join(u32(v) for v in (dst,-1 if initial else 0,level,transition,src)))
                                result_level=struct.unpack('<i',n.uc.mem_read(level,4))[0]
                                inputs.append(f'4 {sr} {height} {dr} {ff} {tf} {lev} {initial}');expected.append(f'{result} {result_level} {n.integer(transition)&255}')
    counts['bridge_height_transitions']=compare(exe,'--bridges',inputs,expected)
    n=Native();inputs=[];expected=[]
    cell=ARG+0x1200
    stub(n,0x548000,cell,4);stub(n,0x4717b0,0);stub(n,0x475840,0,8)
    def surface_stop(uc,address,size,user):
        if address==0x460761:result=0
        else:
            upward=n.uc.mem_read(STACK+0x16,1)[0];downward=n.uc.mem_read(STACK+0x17,1)[0]
            result=2 if upward else 3 if downward else 1
        uc.reg_write(UC_X86_REG_EAX,result);uc.reg_write(UC_X86_REG_EIP,STOP)
    handles=[n.uc.hook_add(UC_HOOK_CODE,surface_stop,begin=a,end=a) for a in (0x4605b0,0x460761)]
    for ground in (0,104,416):
        deck=ground+416
        for oldz in (ground-1,ground,ground+1,deck-1,deck,deck+1):
            for z in (ground-1,ground,ground+1,deck-1,deck,deck+1):
                for bridge in (0,1):
                    n.put(cell+0x140,0x100 if bridge else 0)
                    n.put(STACK+0x10,ground);n.put(STACK+0x50,deck);n.put(STACK+0x4c,z);n.put(STACK+0xb0,oldz);n.real(STACK+0x88,z)
                    result=n.run(0x46046b,registers={UC_X86_REG_ESI:cell,UC_X86_REG_EDI:deck,UC_X86_REG_EBX:0x100})
                    inputs.append(f'{oldz} {z} {ground} {deck} {bridge}');expected.append(str(result))
    counts['projectile_surface_boundaries']=compare(exe,'--surfaces',inputs,expected)
    n=Native();inputs=[];expected=[]
    fuse=ARG+0x1000
    n.put(fuse+0xc,-1);n.put(fuse+0x14,0)
    for distance in range(0,1100,3):
        for previous in (0,31,32,63,64,127,128,255,256,0x7fffffff):
            n.put(fuse+0x24,previous);n.uc.mem_write(ARG,struct.pack('<iii',distance,distance%7,distance%11))
            result=n.run(0x4ceee0,args=u32(ARG),registers={UC_X86_REG_ECX:fuse})
            inputs.append(f'{distance} {distance%7} {distance%11} {previous}');expected.append(f'{result} {n.integer(fuse+0x24)}')
    counts['projectile_fuse']=compare(exe,'--fuses',inputs,expected)
    n=Native();inputs=[];expected=[]
    target,target_table,coords=ARG+0x1800,ARG+0x1900,ARG+0x1e00
    n.put(OBJ+0x98,TYPE);n.put(OBJ+0xf4,target);n.put(target,target_table)
    for offset in (0x48,0x58):n.put(target_table+offset,STOP+0x400)
    stub(n,STOP+0x400,coords,4);n.put(TABLE+0x19c,STOP+0x600)
    n.uc.mem_write(STOP+0x600,bytes.fromhex('8b4424048b108991880000008b500489918c0000008b5008899190000000c20400'))
    snap=[False]
    def snapped(uc,address,size,user):snap[0]=True
    n.uc.hook_add(UC_HOOK_CODE,snapped,begin=0x460e7c,end=0x460e7c)
    for x in (-1024,-769,-768,-385,-384,-383,-128,-1,0,1,128,383,384,385,768,769,1024):
        for y in (-257,0,257):
            for z in (-101,0,101):
                for speed in (0,17,40,100):
                    n.put(STACK+0x50,0);n.uc.mem_write(STACK+0x1f,b'\1');n.uc.mem_write(STACK+0x24,struct.pack('<iii',x,y,z))
                    n.uc.mem_write(OBJ+0x88,struct.pack('<iii',x,y,z));n.uc.mem_write(OBJ+0xd0,struct.pack('<ddd',speed,0,-6))
                    snap[0]=False;n.run(0x460cee,0x460e98,registers={UC_X86_REG_EBP:OBJ})
                    values=struct.unpack('<iii',n.uc.mem_read(OBJ+0x88,12))
                    inputs.append(f'{x} {y} {z} {speed} 0 {-6 & 0xffffffff}');expected.append(f'{int(snap[0])} '+' '.join(map(str,values)))
    counts['projectile_target_snap']=compare(exe,'--hitpoints',inputs,expected)
    n=Native();inputs=[];expected=[]
    target,target_table,weapon_entry,weapon,visible,house,other_house=ARG+0x1000,ARG+0x1600,ARG+0x200,ARG+0x300,ARG+0x1e00,ARG+0x1c00,ARG+0x1d00
    n.put(target,target_table);n.put(OBJ+0x1b4,house);n.put(weapon_entry,weapon)
    for table,offset,value,cleanup,address in ((TABLE,0x304,0,0,STOP+0x400),(TABLE,0x2b8,0,4,STOP+0x420),(TABLE,0x39c,weapon_entry,4,STOP+0x440),(TABLE,0x364,0,8,STOP+0x460),(target_table,0x48,ARG+0x1f00,4,STOP+0x480)):
        n.put(table+offset,address);stub(n,address,value,cleanup)
    n.put(target_table+0x1b0,STOP+0x4a0);stub(n,0x5950d0,visible);stub(n,0x548000,ARG+0x2000,4)
    def accepted(uc,address,size,user):
        uc.reg_write(UC_X86_REG_EAX,1);uc.reg_write(UC_X86_REG_EIP,STOP)
    n.uc.hook_add(UC_HOOK_CODE,accepted,begin=0x6c56c2,end=0x6c56c2)
    for traits in range(128):
        if traits & (8|32):continue
        for hidden in (0,1):
            for detected in (0,1):
                for friendly in (0,1):
                    for health in (0,1):
                        n.uc.mem_write(target+0x76,bytes((int(bool(traits&3)),)));n.put(target+0x6c,health)
                        n.put(target+0x1b8,2 if traits&4 else 0);n.uc.mem_write(target+0x32d,bytes((int(not traits&16),)))
                        n.uc.mem_write(visible+4,bytes((hidden,)));n.put(target+0x1b4,house if friendly else other_house)
                        stub(n,0x47c2e0,detected,4);stub(n,STOP+0x4a0,-21 if traits&64 else 0)
                        result=n.run(0x6c5570,args=b''.join(u32(v) for v in (0,0,0,target,ARG+0x2100,-1,0)),registers={UC_X86_REG_ECX:OBJ})&255
                        inputs.append(f'{traits} {hidden} {detected} {friendly} {health}');expected.append(str(result))
    counts['ordinary_candidate_early_filters']=compare(exe,'--candidates',inputs,expected)
    result={'engine_sha256':ENGINE_HASH,'cases':counts,'checks':sum(counts.values()),'failures':0,'scope':'isolated original instructions; world lookup and object virtual calls use explicit fixtures'}
    output.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(result))
if __name__=='__main__':main()


