"""Original 1.006 direct call sites; adapter compatibility is measured, not inferred from names."""
from run_batch_v68 import *
sys.path.insert(0,str(R/'python_lib'))
import capstone,pefile
pe=pefile.PE(str(R/'ra2/game/game.exe'));raw=pe.get_memory_mapped_image();base=pe.OPTIONAL_HEADER.ImageBase
md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_32);calls={}
for f in read(R/'ra2/work/game/functions.json')['functions']:
    if 0x55A660 not in f.get('calls_to',[]):continue
    ins=list(md.disasm(raw[f['address']-base:f['end']-base],f['address']))
    for i,q in enumerate(ins):
        if q.mnemonic=='call' and q.op_str=='0x55a660':
            calls[q.address]=dict(address=hex(q.address),caller=f['name'],next_instructions=[dict(address=hex(a.address),mnemonic=a.mnemonic,operands=a.op_str) for a in ins[i+1:i+5]])
assert len(calls)==108
write(S/'map-area-original-calls.json',dict(passed=True,original_sha256=sha(R/'ra2/game/game.exe'),function_address='0x0055A660',function_bytes_sha256=hashlib.sha256(raw[0x55A660-base:0x55A737-base]).hexdigest(),direct_calls=len(calls),calls=list(calls.values()),scope='Original decoded direct callers; native probe separately checks full EAX/ECX/EDX, nonvolatile registers, flags, stack, fallback and control word. Not a fabricated alias entry.'))
print(dict(passed=True,direct_calls=108))
