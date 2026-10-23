"""Add read-only observation of new boundaries and identify actual generated entry routes."""
from pathlib import Path
R = Path(__file__).resolve().parent
S = R / 'evidence/movement-state-v35'
path = S / 'connection_observer.c'
t = path.read_text(encoding='utf-8')
assert 'overlap_trampolines' not in t
blocks = ['static uint32_t overlap_trampolines[4];\n']
for index, stage in enumerate(range(16, 20)):
    unit = 'push 0\n        push dword ptr [ebp+8]' if stage < 18 else 'push dword ptr [ebp+8]\n        push 0'
    blocks.append(f'''static __declspec(naked) void overlap_hook_{stage}(void)
{{
    __asm {{
        pushfd
        pushad
        mov ebp,esp
        sub esp,528
        and esp,-16
        fxsave [esp]
        push 0
        push 0
        push {stage}
        {unit}
        call ra2_internal_observe
        add esp,20
        fxrstor [esp]
        mov esp,ebp
        popad
        popfd
        jmp dword ptr [overlap_trampolines+{index * 4}]
    }}
}}
''')
blocks.append('''static void install_overlap_hooks(void)
{
    static const uint32_t sites[]={0x4A17FE,0x4A3502,0x703439,0x7038EF};
    static const unsigned lengths[]={6,5,12,7};
    static const uint8_t expected[4][16]={{0x8D,0x91,0x88,0,0,0},{0x83,0x7C,0x24,0x18,7},{0x8A,0x44,0x24,0x11,0xC6,0x84,0x24,0x88,0,0,0,0},{0x8B,0x76,0x30,0x8B,0x5C,0x24,0x7C}};
    const uintptr_t hooks[]={(uintptr_t)overlap_hook_16,(uintptr_t)overlap_hook_17,(uintptr_t)overlap_hook_18,(uintptr_t)overlap_hook_19};
    for(unsigned i=0;i<4;++i){
        uint8_t *site=(uint8_t *)(uintptr_t)sites[i];unsigned length=lengths[i];DWORD old;
        if(memcmp(site,expected[i],length))fixture_fail("overlap hook bytes changed");
        uint8_t *trampoline=VirtualAlloc(NULL,32,MEM_COMMIT|MEM_RESERVE,PAGE_EXECUTE_READWRITE);
        if(!trampoline||!VirtualProtect(site,length,PAGE_EXECUTE_READWRITE,&old))fixture_fail("overlap hook protection");
        memcpy(trampoline,site,length);trampoline[length]=0xE9;
        *(uint32_t *)(trampoline+length+1)=sites[i]+length-(uint32_t)(uintptr_t)(trampoline+length+5);overlap_trampolines[i]=(uint32_t)(uintptr_t)trampoline;
        site[0]=0xE9;*(uint32_t *)(site+1)=(uint32_t)hooks[i]-sites[i]-5;for(unsigned j=5;j<length;++j)site[j]=0x90;
        VirtualProtect(site,length,old,&old);FlushInstructionCache(GetCurrentProcess(),site,length);
    }
}
void __cdecl ra2_overlap_route(unsigned site,unsigned entry)
{
    static uint32_t seen[64][2];static unsigned count;
    for(unsigned i=0;i<count;++i)if(seen[i][0]==site&&seen[i][1]==entry)return;
    if(count>=64)fixture_fail("overlap route inventory overflow");
    seen[count][0]=site;seen[count++][1]=entry;
    fprintf(stderr,"[overlap-route] site=%u return=%08X frame=%u\\n",site,entry,U32(0xA40D2C));
}
''')
marker = 'static void connection_tick(FILE *output,int original_mode)'
assert t.count(marker) == 1
t = t.replace(marker, ''.join(blocks) + '\n' + marker)
t = t.replace('    install_internal_hooks();', '    install_internal_hooks();\n    install_overlap_hooks();')
path.write_text(t, encoding='utf-8', newline='\n')

path = R / 'make_connection_fixture_v35.py'
t = path.read_text(encoding='utf-8')
marker = "(S/'connection_advance_bridge.c').write_text(t,encoding='utf-8',newline='\\n')"
assert t.count(marker) == 1
t = t.replace(marker, '''marker='static Ra2WorldPoint raw_position(void *opaque)\\n{ return read_point(owner(opaque)+0x88); }';assert t.count(marker)==1
t=t.replace(marker,'static Ra2WorldPoint raw_position(void *opaque)\\n{ ra2_internal_observe(((AdvanceContext *)opaque)->drive,0,16,0,0); return read_point(owner(opaque)+0x88); }')
''' + marker)
marker = "(S/'connection_prepare_bridge.c').write_text(t,encoding='utf-8',newline='\\n')"
assert t.count(marker) == 1
t = t.replace(marker, '''start=t.index('static int32_t segment_classify_cell(');end=t.index('uint32_t ra2_ground_prepare_segment_bridge',start)
piece=t[start:end];marker='    return passage;';assert piece.count(marker)==1
piece=piece.replace(marker,'    ra2_internal_observe(context->drive,0,17,0,0);\\n'+marker)
t=t[:start]+piece+t[end:]
''' + marker)
marker = "commands=json.loads("
index = t.index(marker)
t = t[:index] + '''t=(R/'ra2/src/runtime/ground_overlap_bridge.c').read_text(encoding='utf-8')
t='#include <intrin.h>\\nextern void __cdecl ra2_internal_observe(unsigned drive,unsigned unit,unsigned stage,int x,int y);\\nextern void __cdecl ra2_overlap_route(unsigned site,unsigned entry);\\n'+t
marker='    uint32_t frame = g_esp;';assert t.count(marker)==2
start=t.index('uint32_t ra2_ground_template_transition_bridge(');end=t.index('uint32_t ra2_ground_object_chain_bridge(',start)
piece=t[start:end].replace(marker,marker+'\\n    ra2_internal_observe(g_ebp,0,entry?17:16,0,0); ra2_overlap_route(entry?17:16,(unsigned)(uintptr_t)_ReturnAddress());')
t=t[:start]+piece+t[end:]
start=t.index('uint32_t ra2_ground_object_chain_bridge(');end=t.index('void ra2_ground_passage_return_bridge(',start)
piece=t[start:end].replace(marker,marker+'\\n    ra2_internal_observe(0,g_ebp,entry?19:18,0,0); ra2_overlap_route(entry?19:18,(unsigned)(uintptr_t)_ReturnAddress());')
t=t[:start]+piece+t[end:]
(S/'connection_overlap_bridge.c').write_text(t,encoding='utf-8',newline='\\n')

''' + t[index:]
t = t.replace("('ground_prepare_bridge','connection_prepare_bridge')", "('ground_prepare_bridge','connection_prepare_bridge'),('ground_overlap_bridge','connection_overlap_bridge')")
t = t.replace('exactly nine diagnostic objects', 'exactly ten diagnostic objects')
t = t.replace("'/MANIFESTUAC:NO','/out:'", "'/MANIFESTUAC:NO','/MAP:'+str(S/'connection-fixture.map'),'/out:'")
path.write_text(t, encoding='utf-8', newline='\n')
print('Prepared ten diagnostic replacements and four additional native boundaries')
