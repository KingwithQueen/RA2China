"""Record the requested object-chain layer and selected head's stable object ID."""
from pathlib import Path
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v37'
p=S/'connection_observer.c';t=p.read_text(encoding='utf-8')
marker='static __declspec(naked) void overlap_hook_18(void)'
a=t.index(marker);b=t.index('static __declspec(naked) void overlap_hook_19(void)',a)
part=t[a:b]
old='''        push 0
        push 0
        push 18
        push dword ptr [ebp+8]
        push 0
        call ra2_internal_observe
        add esp,20'''
new='''        mov eax,dword ptr [ebp+12]
        add eax,4
        push eax
        push dword ptr [ebp+16]
        push dword ptr [ebp+8]
        call ra2_chain_observe
        add esp,12'''
assert part.count(old)==1
part=part.replace(old,new);t=t[:a]+part+t[b:]
addition='''void __cdecl ra2_chain_observe(uint32_t unit,uint32_t cell,uint32_t frame)
{
    unsigned upper=*(uint8_t *)(uintptr_t)(frame+0x11);
    uint32_t head=U32(cell+(upper?0xE8:0xE4));
    ra2_internal_observe(0,unit,18,(int32_t)upper,head?(int32_t)U32(head+0x10):0);
}
'''
t=t.replace(marker,addition+marker)
p.write_text(t,encoding='utf-8',newline='\n')
p=R/'make_connection_fixture_v37.py';t=p.read_text(encoding='utf-8')
old=r'extern void __cdecl ra2_overlap_route(unsigned site,unsigned entry);\n'
assert t.count(old)==1
t=t.replace(old,old+r'extern void __cdecl ra2_chain_observe(unsigned unit,unsigned cell,unsigned frame);\n')
old='ra2_internal_observe(0,g_ebp,entry?19:18,0,0);'
assert t.count(old)==1
t=t.replace(old,'if(entry)ra2_internal_observe(0,g_ebp,19,0,0);else ra2_chain_observe(g_ebp,g_ebx,frame);')
p.write_text(t,encoding='utf-8',newline='\n')
print('Object-chain layer/head values retain native/C stable IDs')
