"""Observe actual enemy classification with checked original bytes and CALL relocation."""
from pathlib import Path
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v31'
t=(S/'baseline/evidence/movement-state-v30/connection_observer.c').read_text(encoding='utf-8')
extra='''
static uint32_t enemy_visit_trampoline;
void __cdecl ra2_enemy_visit(uint32_t unit,uint32_t object)
{
    ra2_internal_observe(0,unit,27,(int32_t)U32(object+0x10),(int32_t)U32(object));
}
static __declspec(naked) void enemy_visit_hook(void)
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
        call ra2_enemy_visit
        add esp,8
        fxrstor [esp]
        mov esp,ebp
        popad
        popfd
        jmp dword ptr [enemy_visit_trampoline]
    }
}
static void install_enemy_visit_hook(void)
{
    uint8_t *site=(uint8_t *)(uintptr_t)0x70397C;DWORD old;
    static const uint8_t expected[]={0x8B,0xCE,0xE8,0x4D,0xA2,0xD0,0xFF};
    if(memcmp(site,expected,7))fixture_fail("enemy classifier original bytes changed");
    uint8_t *trampoline=VirtualAlloc(NULL,32,MEM_COMMIT|MEM_RESERVE,PAGE_EXECUTE_READWRITE);
    if(!trampoline||!VirtualProtect(site,7,PAGE_EXECUTE_READWRITE,&old))fixture_fail("enemy observer protection");
    memcpy(trampoline,site,7);
    /* The copied CALL ends at +7. Relocate to its byte-verified original target. */
    *(uint32_t *)(trampoline+3)=0x40DBD0-(uint32_t)(uintptr_t)(trampoline+7);
    trampoline[7]=0xE9;*(uint32_t *)(trampoline+8)=0x703983-(uint32_t)(uintptr_t)(trampoline+12);
    enemy_visit_trampoline=(uint32_t)(uintptr_t)trampoline;
    site[0]=0xE9;*(uint32_t *)(site+1)=(uint32_t)(uintptr_t)enemy_visit_hook-0x703981;
    site[5]=site[6]=0x90;VirtualProtect(site,7,old,&old);FlushInstructionCache(GetCurrentProcess(),site,7);
}

'''
marker='static void connection_tick(FILE *output,int original_mode)';assert t.count(marker)==1
t=t.replace(marker,extra+marker).replace('    install_object_visit_hook();','    install_object_visit_hook();\n    install_enemy_visit_hook();')
(S/'connection_observer.c').write_text(t,encoding='utf-8',newline='\n')
print('Retained twelve replacements; added actual enemy classification observer')
