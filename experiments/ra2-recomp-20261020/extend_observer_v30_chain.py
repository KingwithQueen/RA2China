"""Observe actual nonowner visits and both legal bridge object chains, read only."""
from pathlib import Path
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v30'
t=(R/'evidence/movement-state-v28/connection_observer.c').read_text(encoding='utf-8')
t=t.replace('if(id!=1022579&&','if(id!=1023362&&id!=1022579&&')
marker='    ra2_internal_observe(0,unit,18,(int32_t)upper,head?(int32_t)U32(head+0x10):0);'
assert t.count(marker)==1
t=t.replace(marker,marker+'''
    unsigned lengths[2]={0,0};
    for(unsigned layer=0;layer<2;++layer){
        uint32_t object=U32(cell+(layer?0xE8:0xE4));
        while(object){if(++lengths[layer]>128)fixture_fail("cyclic object chain");object=U32(object+0x30);}
    }
    ra2_internal_observe(0,unit,23,(int32_t)lengths[0],(int32_t)lengths[1]);
''')
marker='static void connection_tick(FILE *output,int original_mode)'
extra='''static uint32_t object_visit_trampoline;
void __cdecl ra2_object_visit(uint32_t unit,uint32_t object)
{
    uint32_t next=U32(object+0x30);
    ra2_internal_observe(0,unit,22,(int32_t)U32(object+0x10),next?(int32_t)U32(next+0x10):0);
}
static __declspec(naked) void object_visit_hook(void)
{
    __asm {
        pushfd
        pushad
        mov ebp,esp
        sub esp,528
        and esp,-16
        fxsave [esp]
        push dword ptr [ebp+4]
        push dword ptr [ebp+8]
        call ra2_object_visit
        add esp,8
        fxrstor [esp]
        mov esp,ebp
        popad
        popfd
        jmp dword ptr [object_visit_trampoline]
    }
}
static void install_object_visit_hook(void)
{
    uint8_t *site=(uint8_t *)(uintptr_t)0x703473;
    DWORD old;
    /* The unchanged production recorder already owns 703473. Chain its
       byte-checked audit hook so both observers execute in the same order. */
    if(site[0]!=0xE9||site[5]!=0x90)fixture_fail("missing production object audit hook");
    object_visit_trampoline=0x703478+*(uint32_t *)(site+1);
    static const uint8_t prefix[]={0x9C,0x60,0x8B,0xEC};
    if(memcmp((void *)(uintptr_t)object_visit_trampoline,prefix,4))fixture_fail("production audit hook prefix");
    if(!VirtualProtect(site,6,PAGE_EXECUTE_READWRITE,&old))fixture_fail("object visit protection");
    site[0]=0xE9;*(uint32_t *)(site+1)=(uint32_t)(uintptr_t)object_visit_hook-0x703478;site[5]=0x90;
    VirtualProtect(site,6,old,&old);FlushInstructionCache(GetCurrentProcess(),site,6);
}

'''
assert t.count(marker)==1;t=t.replace(marker,extra+marker).replace('    install_round28_hooks();','    install_round28_hooks();\n    install_object_visit_hook();')
(S/'connection_observer.c').write_text(t,encoding='utf-8',newline='\n')
p=R/'make_connection_fixture_v30.py';t=(R/'make_connection_fixture_v28.py').read_text(encoding='utf-8').replace('v28','v30')
marker="(S/'connection_objects_bridge.c').write_text(t,encoding='utf-8',newline='\\n')"
assert t.count(marker)==1
addition="t='extern void __cdecl ra2_object_visit(unsigned unit,unsigned object);\\n'+t\n"
addition+="t=t.replace('    if(entry==0 && c.owner!=c.object) ra2_state_movement_audit', '    if(entry==0 && c.owner!=c.object) ra2_object_visit(c.owner,c.object);\\n    if(entry==0 && c.owner!=c.object) ra2_state_movement_audit')\n"
t=t.replace(marker,addition+marker)
# Probe the resolver using the host's existing diagnostic facility. No forced alias calls.
p.write_text(t,encoding='utf-8',newline='\n')
p=R/'run_connection_v30.py';t=(R/'run_connection_v28.py').read_text(encoding='utf-8').replace('v28','v30')
needle="exec(compile(source,"
i=t.index(needle)
insert='source=source.replace("for order in args.order:", "probe_groups=[[\'4A1000\',\'4A2670\',\'703040\',\'4A12F1\',\'4A134F\',\'4A161D\',\'4A166A\',\'4A17A2\'],[\'4A1000\',\'4A2670\',\'703040\',\'4A32B4\',\'70346B\',\'70372C\',\'7038EF\']]\\n        probe_group=0 if any(order.endswith((\':72\',\':68\')) for order in args.order) else 1\\n        for address in probe_groups[probe_group]:\\n            cmd += [\'--probe\', \'0x\'+address]\\n        for order in args.order:")\n'
t=t[:i]+insert+t[i:];p.write_text(t,encoding='utf-8',newline='\n')
print('Object visit native hook and matching C read-only observer; bounded resolver probes')
