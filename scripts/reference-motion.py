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
    rows=[]
    for speed in (0,1,2,5,6,7,10,25,50,99,100,101):
        uc.reg_write(UC_X86_REG_EAX,speed); uc.reg_write(UC_X86_REG_EBP,TYPE)
        run(0x6dcc06,0x6dcc41); native=integer(uc,TYPE+0x5a0)
        assert native == min(255,min(100,max(0,speed))*256//100)
        rows.append({'speed':speed,'native_leptons':native})
    scaled=[]
    for base in (15,17):
        uc.mem_write(TYPE+0x5a0,u32(base))
        for pct in (1.0,.7,.8,1.2,.84,.3):
            uc.mem_write(OBJ+0x468,struct.pack('<d',pct)); uc.reg_write(UC_X86_REG_ECX,OBJ)
            run(0x4c9b10); scaled.append({'base':base,'factor':pct,'native_leptons':uc.reg_read(UC_X86_REG_EAX)})
    turns=[]
    for rot in (1,5,8,127):
        for initial,target in ((0,16384),(0,32768),(65000,1000),(16000,0)):
            uc.mem_write(0xa40d2c,u32(100)); uc.reg_write(UC_X86_REG_ECX,FACE); run(0x4b89f0,args=u32(rot))
            uc.mem_write(FACE,struct.pack('<I',initial)); uc.mem_write(FACE+4,struct.pack('<I',initial)); uc.mem_write(ARG,u32(target))
            uc.reg_write(UC_X86_REG_ECX,FACE); run(0x4b8a30,args=u32(ARG))
            duration=integer(uc,FACE+0x10); values=[]
            for tick in range(duration+2):
                uc.mem_write(0xa40d2c,u32(100+tick)); uc.reg_write(UC_X86_REG_ECX,FACE); run(0x4b8be0,args=u32(ARG+8))
                values.append(integer(uc,ARG+8)&65535)
            turns.append({'rot':rot,'initial':initial,'target':target,'duration':duration,'values':values})
    slopes=[]
    for origin,dest in ((0,0),(0,1),(1,0)):
        for terrain in (1.0,.7):
            uc.mem_write(STACK+0x18,struct.pack('<d',terrain)); uc.reg_write(UC_X86_REG_ESI,dest); uc.reg_write(UC_X86_REG_EDI,origin)
            uc.reg_write(UC_X86_REG_EBP,LOC); run(0x4a3d2f,0x4a3dbe)
            slopes.append({'from':origin,'to':dest,'terrain':terrain,'native_factor':double(uc,STACK+0x18)})
    stops=[]
    uc.mem_write(TYPE+0x2c8,u32(500)); uc.mem_write(TYPE+0x2d0,struct.pack('<d',.002))
    for speed in (15,17):
        for distance in (501,500,499,256,64,0):
            uc.mem_write(STACK+0x30,u32(speed)); uc.mem_write(STACK+0x24,struct.pack('<d',1.0))
            uc.reg_write(UC_X86_REG_ESI,TYPE); uc.reg_write(UC_X86_REG_EDI,distance); uc.reg_write(UC_X86_REG_EBP,LOC)
            run(0x4a1196,0x4a1223)
            stops.append({'speed':speed,'distance':distance,'native_factor':double(uc,STACK+0x24)})
    delays=[]
    rng=0x1400b000
    seed=0x1badf00d
    uc.mem_write(rng, b'\0'*1012)
    uc.mem_write(rng+8,u32(103))
    for i in range(250):
        seed=(seed*1664525+1013904223)&0xffffffff
        uc.mem_write(rng+12+i*4,u32(seed))
    for i in range(512):
        uc.reg_write(UC_X86_REG_ECX,rng); run(0x6388a0,args=u32(0)+u32(2))
        delays.append(uc.reg_read(UC_X86_REG_EAX))
    reference={'speed':[r['native_leptons'] for r in rows], 'scaled':[r['native_leptons'] for r in scaled],
               'turns':[{'duration':r['duration'],'values':r['values']} for r in turns],
               'slopes':[round(r['native_factor']*10000) for r in slopes], 'slowdown':[round(r['native_factor']*10000) for r in stops],
               'random':delays}
    comparisons={}
    if len(sys.argv)>3:
        actual=json.loads(subprocess.check_output([sys.argv[3]],encoding='utf-8'))
        for key,values in reference.items():
            assert actual[key]==values, f'C 与原版数值不同: {key}'
            comparisons[key]=len(values)
    report={'engine':str(exe),'sha256':ENGINE_HASH,'scope':'原版窄指令路径；对象和国家速度修正为显式夹具，不是完整游戏行走验收',
            'sites':{'speed': '0x6dcc06..0x6dcc41','scaled_speed':'0x4c9b10','facing':'0x4b89f0/0x4b8a30/0x4b8be0','slope':'0x4a3d2f..0x4a3dbe','slowdown':'0x4a1196..0x4a1223'},
            'speed':rows,'scaled':scaled,'turns':turns,'slopes':slopes,'slowdown':stops,'random_delays':delays,'c_comparisons':comparisons,
            'random_scope':'显式相同 250 字状态下的原版抽取与 0..2 拒绝采样；没有复刻原版全局种子初始化'}
    output.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'passed':True,'speed_cases':len(rows),'scaled_cases':len(scaled),'turn_cases':len(turns),'slope_cases':len(slopes),'stop_cases':len(stops),'random_cases':len(delays),'c_comparisons':comparisons}))
if __name__=='__main__': main()
