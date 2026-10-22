/* Test-only observer: reads a legal map's TubeClass branch. Never linked into production. */
static FILE *connection_output;
static uint32_t connection_trampolines[2];
void __cdecl ra2_connection_observe(uint32_t drive, unsigned stage)
{
    if (!connection_output) return;
    uint32_t unit=U32(drive+0xC), index=U8(unit+0x574), count=U32(0x8661D8);
    if(index>=count) fixture_fail("connection observer: invalid index");
    uint32_t tube=U32(U32(0x8661CC)+index*4);
    fprintf(connection_output,"{\"kind\":\"fixture-connection-hit\",\"frame\":%u,\"id\":%u,\"stage\":%u,\"connection\":%u,\"tube_count\":%u,\"entrance\":[%d,%d],\"exit\":[%d,%d],\"duration\":%u,\"segment\":[%d,%d,%d],\"position\":[%d,%d,%d],\"landing_height\":%d,\"driving\":%u,\"selector\":%d,\"flags\":[%u,%u]}\n",
        U32(0xA40D2C),U32(unit+0x10),stage,index,count,
        *(int16_t *)(uintptr_t)(tube+0x24),*(int16_t *)(uintptr_t)(tube+0x26),
        *(int16_t *)(uintptr_t)(tube+0x28),*(int16_t *)(uintptr_t)(tube+0x2A),U32(tube+0x1C0),
        (int32_t)U32(drive+0x40),(int32_t)U32(drive+0x44),(int32_t)U32(drive+0x48),
        (int32_t)U32(unit+0x88),(int32_t)U32(unit+0x8C),(int32_t)U32(unit+0x90),
        (int32_t)U32(unit+0x464),U8(drive+0x63),(int32_t)U32(drive+0x58),U8(unit+0x574),U8(unit+0x575));
}
static __declspec(naked) void connection_start_hook(void)
{
    __asm {
        pushfd
        pushad
        mov ebp,esp
        sub esp,528
        and esp,-16
        fxsave [esp]
        push 0
        push dword ptr [ebp+8]
        call ra2_connection_observe
        add esp,8
        fxrstor [esp]
        mov esp,ebp
        popad
        popfd
        jmp dword ptr [connection_trampolines]
    }
}
static __declspec(naked) void connection_finish_hook(void)
{
    __asm {
        pushfd
        pushad
        mov ebp,esp
        sub esp,528
        and esp,-16
        fxsave [esp]
        push 1
        push dword ptr [ebp+8]
        call ra2_connection_observe
        add esp,8
        fxrstor [esp]
        mov esp,ebp
        popad
        popfd
        jmp dword ptr [connection_trampolines+4]
    }
}
static void connection_tick(FILE *output,int original_mode)
{
    if(connection_output) return;
    connection_output=output;
    if(!original_mode) return;
    static const uint32_t sites[]={0x4A1470,0x4A1564};
    static const unsigned lengths[]={6,7};
    static const uint8_t expected[2][7]={{0x8B,0x53,0x30,0x8B,0x43,0x24,0},{0xC7,0x45,0x58,0xFF,0xFF,0xFF,0xFF}};
    const uintptr_t hooks[]={(uintptr_t)connection_start_hook,(uintptr_t)connection_finish_hook};
    for(unsigned i=0;i<2;++i)
    {
        uint8_t *site=(uint8_t *)(uintptr_t)sites[i];unsigned length=lengths[i];DWORD old;
        if(memcmp(site,expected[i],length)) fixture_fail("connection hook bytes changed");
        uint8_t *trampoline=VirtualAlloc(NULL,32,MEM_COMMIT|MEM_RESERVE,PAGE_EXECUTE_READWRITE);
        if(!trampoline || !VirtualProtect(site,length,PAGE_EXECUTE_READWRITE,&old)) fixture_fail("connection hook protection failed");
        memcpy(trampoline,site,length);trampoline[length]=0xE9;
        *(uint32_t *)(trampoline+length+1)=sites[i]+length-(uint32_t)(uintptr_t)(trampoline+length+5);
        connection_trampolines[i]=(uint32_t)(uintptr_t)trampoline;
        site[0]=0xE9;*(uint32_t *)(site+1)=(uint32_t)hooks[i]-sites[i]-5;
        for(unsigned j=5;j<length;++j) site[j]=0x90;
        VirtualProtect(site,length,old,&old);FlushInstructionCache(GetCurrentProcess(),site,length);
    }
}
