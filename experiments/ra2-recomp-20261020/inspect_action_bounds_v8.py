"""仅以本机 1.006 机器码核实触发动作范围，避免误用其他版本的动作号。"""
from pathlib import Path
import hashlib,json,sys,struct
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'python_lib'))
import pefile,capstone
data=(ROOT/'ra2/game/game.exe').read_bytes()
im=pefile.PE(data=data).get_memory_mapped_image()
def raw(a,n): return im[a-0x400000:a-0x400000+n]
assert raw(0x6ADB04,13).hex()=='8b562c4a83fa740f87361c0000'
md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_32)
result=dict(input_exe_sha256=hashlib.sha256(data).hexdigest(),dispatcher='0x6ADAE0',
    enum_load='0x6ADB04',decrement='0x6ADB07',unsigned_upper_bound='0x6ADB08',
    original_action_min=1,original_action_max=117,action_128_supported=False,
    conclusion='Action 128 is outside this original 1.006 dispatcher; it cannot validate a legal TeleportAll trigger here.',
    instructions=[dict(address=hex(x.address),bytes=x.bytes.hex(),mnemonic=x.mnemonic,operands=x.op_str) for x in md.disasm(raw(0x6ADB04,20),0x6ADB04)],
    chrono_reinforcement_action=107,chrono_reinforcement_target=hex(struct.unpack('<I',raw(0x6AF754+(107-1)*4,4))[0]),
    boundary='This excludes only action 128, not every legal Chronosphere or locomotor-replacement route.')
p=ROOT/'evidence/movement-state-v8/action-bounds.json'; assert not p.exists()
p.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
