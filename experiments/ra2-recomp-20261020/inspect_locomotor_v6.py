"""只读检索本机原版 RTTI 和传送 locomotor 的 GUID，不套用尤复地址。"""
from pathlib import Path
import json
import struct
import sys
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'python_lib'))
import pefile
image=pefile.PE(str(ROOT/'ra2/game/game.exe')).get_memory_mapped_image()
def occurrences(needle):
    start=0
    while True:
        index=image.find(needle,start)
        if index<0: return
        yield index+0x400000
        start=index+1
result={}
for name in ('DriveLocomotionClass','TeleportLocomotionClass'):
    types=[]
    for string in occurrences(name.encode('ascii')):
        beginning=image.rfind(b'\0',max(0,string-0x400000-10),string-0x400000)+1
        typedesc=beginning+0x400000-8
        locators=[]
        for ref in occurrences(struct.pack('<I',typedesc)):
            locator=ref-12
            for pointer in occurrences(struct.pack('<I',locator)):
                vtable=pointer+4
                if 0x790000<=vtable<0x840000:
                    methods=struct.unpack_from('<48I',image,vtable-0x400000)
                    locators.append(dict(vtable=hex(vtable),methods=[hex(a) for a in methods]))
        types.append(dict(string=hex(string),type_descriptor=hex(typedesc),locators=locators))
    result[name]=types
result['teleport_guid_addresses']=[hex(a) for a in occurrences(bytes.fromhex('4727584a3998d111b70900a024ddafd1'))]
out=ROOT/'evidence/movement-state-v6/locomotor-layout.json'
out.write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
