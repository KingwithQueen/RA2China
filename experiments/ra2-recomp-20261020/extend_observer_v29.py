"""Observe native layer/category boundaries and their main C service equivalents."""
from pathlib import Path
R = Path(__file__).resolve().parent
S = R / 'evidence/movement-state-v29'
p = S / 'connection_observer.c'
t = p.read_text(encoding='utf-8')
assert 'round28_trampolines' not in t
hooks = '\nstatic uint32_t round28_trampolines[2];\n'
for index, stage in enumerate([20, 21]):
    drive, unit = ('dword ptr [ebp+8]', '0') if stage == 20 else ('0', 'dword ptr [ebp+8]')
    hooks += f'''static __declspec(naked) void round28_hook_{stage}(void)
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
        push {unit}
        push {drive}
        call ra2_internal_observe
        add esp,20
        fxrstor [esp]
        mov esp,ebp
        popad
        popfd
        jmp dword ptr [round28_trampolines+{index*4}]
    }}
}}
'''
hooks += '''static void install_round28_hooks(void)
{
    static const uint32_t sites[]={0x4A18AB,0x7034BF};
    static const uint8_t expected[2][7]={{0x0F,0xBE,0x86,0x1B,1,0,0},{0x8A,0x46,0x14,0x8B,0xCD,0x24,1}};
    const uintptr_t callbacks[]={(uintptr_t)round28_hook_20,(uintptr_t)round28_hook_21};
    for(unsigned i=0;i<2;++i)
    {
        uint8_t *site=(uint8_t *)(uintptr_t)sites[i];DWORD old;
        if(memcmp(site,expected[i],7))fixture_fail("round28 native bytes changed");
        uint8_t *trampoline=VirtualAlloc(NULL,32,MEM_COMMIT|MEM_RESERVE,PAGE_EXECUTE_READWRITE);
        if(!trampoline||!VirtualProtect(site,7,PAGE_EXECUTE_READWRITE,&old))fixture_fail("round28 hook protection");
        memcpy(trampoline,site,7);trampoline[7]=0xE9;
        *(uint32_t *)(trampoline+8)=sites[i]+7-(uint32_t)(uintptr_t)(trampoline+12);
        round28_trampolines[i]=(uint32_t)(uintptr_t)trampoline;
        site[0]=0xE9;*(uint32_t *)(site+1)=(uint32_t)callbacks[i]-sites[i]-5;site[5]=site[6]=0x90;
        VirtualProtect(site,7,old,&old);FlushInstructionCache(GetCurrentProcess(),site,7);
    }
}
'''
marker = 'static void connection_tick(FILE *output,int original_mode)'
assert t.count(marker) == 1
t = t.replace(marker, hooks + '\n' + marker).replace('    install_overlap_hooks();', '    install_overlap_hooks();\n    install_round28_hooks();')
p.write_text(t, encoding='utf-8', newline='\n')

p = R / 'make_connection_fixture_v29.py'
t = p.read_text(encoding='utf-8')
marker = "commands=json.loads((R/'ra2/build-original-c/compile_commands.json').read_text(encoding='utf-8'))"
assert t.count(marker) == 1
addition = '''# Main Advance's new layer service observes before the first level query.
t=(S/'connection_advance_bridge.c').read_text(encoding='utf-8')
t+='\\nvoid __cdecl ra2_layer_from_context(void *opaque)\\n{ ra2_internal_observe(((AdvanceContext *)opaque)->drive,0,20,0,0); }\\n'
(S/'connection_advance_bridge.c').write_text(t,encoding='utf-8',newline='\\n')
t=(R/'ra2/src/gameplay/ground_advance.c').read_text(encoding='utf-8')
t='extern void __cdecl ra2_layer_from_context(void *opaque);\\n'+t
marker='    return services->query(services->context, RA2_ADVANCE_CELL_LEVEL, context->cells[next]);'
assert t.count(marker)==1
t=t.replace(marker,'    if(!next)ra2_layer_from_context(services->context);\\n'+marker)
(S/'connection_advance.c').write_text(t,encoding='utf-8',newline='\\n')
t=(R/'ra2/src/runtime/ground_objects_bridge.c').read_text(encoding='utf-8')
t='extern void __cdecl ra2_internal_observe(unsigned drive,unsigned unit,unsigned stage,int x,int y);\\n'+t
marker='        case RA2_OBJECT_OWNER_ACCEPTS_LINK:'
assert t.count(marker)==1
t=t.replace(marker,marker+'\\n            ra2_internal_observe(0,c->owner,21,0,0);')
(S/'connection_objects_bridge.c').write_text(t,encoding='utf-8',newline='\\n')

'''
t = t.replace(marker, addition + marker)
t = t.replace("('ground_overlap_bridge','connection_overlap_bridge')]:", "('ground_overlap_bridge','connection_overlap_bridge'),('ground_advance','connection_advance'),('ground_objects_bridge','connection_objects_bridge')]:")
t = t.replace("a.replace('\\\\','/').endswith('/src/runtime/'+original+'.c')", "a.replace('\\\\','/').endswith('/src/'+('gameplay' if original=='ground_advance' else 'runtime')+'/'+original+'.c')")
t = t.replace("replacements['CMakeFiles\\\\ra2.dir\\\\src\\\\runtime\\\\'+original+'.c.obj']", "replacements['CMakeFiles\\\\ra2.dir\\\\src\\\\'+('gameplay' if original=='ground_advance' else 'runtime')+'\\\\'+original+'.c.obj']")
t = t.replace('exactly ten diagnostic objects', 'exactly twelve diagnostic objects')
p.write_text(t, encoding='utf-8', newline='\n')
print('Prepared twelve diagnostic replacements and two additional native read-only boundaries')
