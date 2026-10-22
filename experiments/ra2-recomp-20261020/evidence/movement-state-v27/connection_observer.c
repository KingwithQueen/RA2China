/* Test-only observer: reads a legal map's TubeClass branch. Never linked into production. */
static FILE *connection_output;
static uint32_t connection_trampolines[10];
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
static __declspec(naked) void connection_exit_hook(void)
{
    __asm {
        pushfd
        pushad
        mov ebp,esp
        sub esp,528
        and esp,-16
        fxsave [esp]
        mov eax,[ebp+4]
        mov eax,[eax+564h]
        sub eax,4
        push 2
        push eax
        call ra2_connection_observe
        add esp,8
        fxrstor [esp]
        mov esp,ebp
        popad
        popfd
        jmp dword ptr [connection_trampolines+8]
    }
}
static __declspec(naked) void connection_occupied_hook(void)
{
    __asm {
        pushfd
        pushad
        mov ebp,esp
        sub esp,528
        and esp,-16
        fxsave [esp]
        mov eax,[ebp+4]
        mov eax,[eax+564h]
        sub eax,4
        push 3
        push eax
        call ra2_connection_observe
        add esp,8
        fxrstor [esp]
        mov esp,ebp
        popad
        popfd
        jmp dword ptr [connection_trampolines+12]
    }
}
static __declspec(naked) void connection_approach_hook(void)
{
    __asm {
        pushfd
        pushad
        mov ebp,esp
        sub esp,528
        and esp,-16
        fxsave [esp]
        mov eax,[ebp+4]
        mov eax,[eax+564h]
        sub eax,4
        push 4
        push eax
        call ra2_connection_observe
        add esp,8
        fxrstor [esp]
        mov esp,ebp
        popad
        popfd
        jmp dword ptr [connection_trampolines+16]
    }
}
static __declspec(naked) void connection_remaining_height_hook(void)
{
    __asm {
        pushfd
        pushad
        mov ebp,esp
        sub esp,528
        and esp,-16
        fxsave [esp]
        mov eax,[ebp+4]
        mov eax,[eax+564h]
        sub eax,4
        push 5
        push eax
        call ra2_connection_observe
        add esp,8
        fxrstor [esp]
        mov esp,ebp
        popad
        popfd
        jmp dword ptr [connection_trampolines+20]
    }
}
static __declspec(naked) void connection_step_height_hook(void)
{
    __asm {
        pushfd
        pushad
        mov ebp,esp
        sub esp,528
        and esp,-16
        fxsave [esp]
        mov eax,[ebp+4]
        mov eax,[eax+564h]
        sub eax,4
        push 6
        push eax
        call ra2_connection_observe
        add esp,8
        fxrstor [esp]
        mov esp,ebp
        popad
        popfd
        jmp dword ptr [connection_trampolines+24]
    }
}
static __declspec(naked) void connection_entry_hook(void)
{
    __asm {
        pushfd
        pushad
        mov ebp,esp
        sub esp,528
        and esp,-16
        fxsave [esp]
        mov eax,[ebp+4]
        mov eax,[eax+564h]
        sub eax,4
        push 7
        push eax
        call ra2_connection_observe
        add esp,8
        fxrstor [esp]
        mov esp,ebp
        popad
        popfd
        jmp dword ptr [connection_trampolines+28]
    }
}
static __declspec(naked) void connection_remaining_horizontal_hook(void)
{
    __asm {
        pushfd
        pushad
        mov ebp,esp
        sub esp,528
        and esp,-16
        fxsave [esp]
        mov eax,[ebp+4]
        mov eax,[eax+564h]
        sub eax,4
        push 8
        push eax
        call ra2_connection_observe
        add esp,8
        fxrstor [esp]
        mov esp,ebp
        popad
        popfd
        jmp dword ptr [connection_trampolines+32]
    }
}
static __declspec(naked) void connection_regular_horizontal_hook(void)
{
    __asm {
        pushfd
        pushad
        mov ebp,esp
        sub esp,528
        and esp,-16
        fxsave [esp]
        mov eax,[ebp+4]
        mov eax,[eax+564h]
        sub eax,4
        push 9
        push eax
        call ra2_connection_observe
        add esp,8
        fxrstor [esp]
        mov esp,ebp
        popad
        popfd
        jmp dword ptr [connection_trampolines+36]
    }
}

static uint32_t internal_trampolines[6];
void __cdecl ra2_internal_observe(uint32_t drive,uint32_t unit,unsigned stage,int32_t x,int32_t y)
{
 if(!connection_output)return;
 if(!unit)unit=U32(drive+0xC);
 uint32_t id=U32(unit+0x10);
 if(id!=1022579&&id!=1022581&&id!=1032259&&id!=1032262)return;
 if(!drive&&U32(unit+0x564))drive=U32(unit+0x564)-4;
 if(drive&&U32(drive+0xC)!=unit)drive=0;
 fprintf(connection_output,"{\"kind\":\"fixture-internal-hit\",\"frame\":%u,\"id\":%u,\"stage\":%u,\"value\":[%d,%d],\"position\":[%d,%d,%d],\"budget\":%d,\"path_direction\":%d,\"selector\":%d,\"sample\":%d,\"destination\":[%d,%d,%d]}\n",
 U32(0xA40D2C),id,stage,x,y,(int32_t)U32(unit+0x88),(int32_t)U32(unit+0x8C),(int32_t)U32(unit+0x90),(int32_t)U32(unit+0x53C),(int32_t)U32(unit+0x4D0),drive?(int32_t)U32(drive+0x58):0,drive?(int32_t)U32(drive+0x5C):0,drive?(int32_t)U32(drive+0x34):0,drive?(int32_t)U32(drive+0x38):0,drive?(int32_t)U32(drive+0x3C):0);
}
static __declspec(naked) void internal_hook_10(void)
{
    __asm {
        pushfd
        pushad
        mov ebp,esp
        sub esp,528
        and esp,-16
        fxsave [esp]
        push 0
        push 0
        push 10
        push 0
        push dword ptr [ebp+8]
        call ra2_internal_observe
        add esp,20
        fxrstor [esp]
        mov esp,ebp
        popad
        popfd
        jmp dword ptr [internal_trampolines+0]
    }
}
static __declspec(naked) void internal_hook_11(void)
{
    __asm {
        pushfd
        pushad
        mov ebp,esp
        sub esp,528
        and esp,-16
        fxsave [esp]
        push 0
        push 0
        push 11
        push 0
        push dword ptr [ebp+8]
        call ra2_internal_observe
        add esp,20
        fxrstor [esp]
        mov esp,ebp
        popad
        popfd
        jmp dword ptr [internal_trampolines+4]
    }
}
static __declspec(naked) void internal_hook_12(void)
{
    __asm {
        pushfd
        pushad
        mov ebp,esp
        sub esp,528
        and esp,-16
        fxsave [esp]
        push dword ptr [ebp]
        push dword ptr [ebp+24]
        push 12
        push 0
        push dword ptr [ebp+8]
        call ra2_internal_observe
        add esp,20
        fxrstor [esp]
        mov esp,ebp
        popad
        popfd
        jmp dword ptr [internal_trampolines+8]
    }
}
static __declspec(naked) void internal_hook_13(void)
{
    __asm {
        pushfd
        pushad
        mov ebp,esp
        sub esp,528
        and esp,-16
        fxsave [esp]
        push 0
        push 0
        push 13
        push 0
        push dword ptr [ebp+8]
        call ra2_internal_observe
        add esp,20
        fxrstor [esp]
        mov esp,ebp
        popad
        popfd
        jmp dword ptr [internal_trampolines+12]
    }
}
static __declspec(naked) void internal_hook_14(void)
{
    __asm {
        pushfd
        pushad
        mov ebp,esp
        sub esp,528
        and esp,-16
        fxsave [esp]
        push 0
        push 0
        push 14
        push dword ptr [ebp+8]
        push 0
        call ra2_internal_observe
        add esp,20
        fxrstor [esp]
        mov esp,ebp
        popad
        popfd
        jmp dword ptr [internal_trampolines+16]
    }
}
static __declspec(naked) void internal_hook_15(void)
{
    __asm {
        pushfd
        pushad
        mov ebp,esp
        sub esp,528
        and esp,-16
        fxsave [esp]
        push 0
        push 0
        push 15
        push 0
        push dword ptr [ebp+8]
        call ra2_internal_observe
        add esp,20
        fxrstor [esp]
        mov esp,ebp
        popad
        popfd
        jmp dword ptr [internal_trampolines+20]
    }
}

static void install_internal_hooks(void)
{
 static const uint32_t sites[]={0x4A17A2,0x4A1725,0x4A17D5,0x4A3486,0x70323E,0x4A263A};
 static const unsigned lengths[]={6,7,6,8,7,5};
 static const uint8_t expected[6][8]={{0x8B,0x45,0x5C,0x8D,0x14,0x40},{0x8D,0x0C,0x40,0x8B,0x54,0x8E,0xFC},{0x33,0xC0,0x89,0x4C,0x24,0x48},{0x8B,0x44,0x24,0x38,0x8D,0x4C,0x24,0x14},{0x8B,0xB4,0x24,0x88,0,0,0},{0x5F,0x5E,0x5D,0x32,0xC0}};
 const uintptr_t hooks[]={(uintptr_t)internal_hook_10,(uintptr_t)internal_hook_11,(uintptr_t)internal_hook_12,(uintptr_t)internal_hook_13,(uintptr_t)internal_hook_14,(uintptr_t)internal_hook_15};
 for(unsigned i=0;i<6;++i){
  uint8_t *site=(uint8_t *)(uintptr_t)sites[i];unsigned length=lengths[i];DWORD old;
  if(memcmp(site,expected[i],length))fixture_fail("internal hook bytes changed");
  uint8_t *trampoline=VirtualAlloc(NULL,32,MEM_COMMIT|MEM_RESERVE,PAGE_EXECUTE_READWRITE);
  if(!trampoline||!VirtualProtect(site,length,PAGE_EXECUTE_READWRITE,&old))fixture_fail("internal hook protection");
  memcpy(trampoline,site,length);trampoline[length]=0xE9;*(uint32_t *)(trampoline+length+1)=sites[i]+length-(uint32_t)(uintptr_t)(trampoline+length+5);internal_trampolines[i]=(uint32_t)(uintptr_t)trampoline;
  site[0]=0xE9;*(uint32_t *)(site+1)=(uint32_t)hooks[i]-sites[i]-5;for(unsigned j=5;j<length;++j)site[j]=0x90;
  VirtualProtect(site,length,old,&old);FlushInstructionCache(GetCurrentProcess(),site,length);
 }
}
static uint32_t overlap_trampolines[4];
static __declspec(naked) void overlap_hook_16(void)
{
    __asm {
        pushfd
        pushad
        mov ebp,esp
        sub esp,528
        and esp,-16
        fxsave [esp]
        push 0
        push 0
        push 16
        push 0
        push dword ptr [ebp+8]
        call ra2_internal_observe
        add esp,20
        fxrstor [esp]
        mov esp,ebp
        popad
        popfd
        jmp dword ptr [overlap_trampolines+0]
    }
}
static __declspec(naked) void overlap_hook_17(void)
{
    __asm {
        pushfd
        pushad
        mov ebp,esp
        sub esp,528
        and esp,-16
        fxsave [esp]
        push 0
        push 0
        push 17
        push 0
        push dword ptr [ebp+8]
        call ra2_internal_observe
        add esp,20
        fxrstor [esp]
        mov esp,ebp
        popad
        popfd
        jmp dword ptr [overlap_trampolines+4]
    }
}
static __declspec(naked) void overlap_hook_18(void)
{
    __asm {
        pushfd
        pushad
        mov ebp,esp
        sub esp,528
        and esp,-16
        fxsave [esp]
        push 0
        push 0
        push 18
        push dword ptr [ebp+8]
        push 0
        call ra2_internal_observe
        add esp,20
        fxrstor [esp]
        mov esp,ebp
        popad
        popfd
        jmp dword ptr [overlap_trampolines+8]
    }
}
static __declspec(naked) void overlap_hook_19(void)
{
    __asm {
        pushfd
        pushad
        mov ebp,esp
        sub esp,528
        and esp,-16
        fxsave [esp]
        push 0
        push 0
        push 19
        push dword ptr [ebp+8]
        push 0
        call ra2_internal_observe
        add esp,20
        fxrstor [esp]
        mov esp,ebp
        popad
        popfd
        jmp dword ptr [overlap_trampolines+12]
    }
}
static void install_overlap_hooks(void)
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
    fprintf(stderr,"[overlap-route] site=%u return=%08X frame=%u\n",site,entry,U32(0xA40D2C));
}

static void connection_tick(FILE *output,int original_mode)
{
    if(connection_output) return;
    connection_output=output;
    if(!original_mode) return;
    install_internal_hooks();
    install_overlap_hooks();
    static const uint32_t sites[]={0x4A1470,0x4A1564,0x6FAFE1,0x6FAEB4,0x6FABAA,0x6FAD1C,0x6FAE1D,0x6FAA66,0x6FAC70,0x6FAD75};
    static const unsigned lengths[]={6,7,7,8,8,6,6,6,6,7};
    static const uint8_t expected[10][8]={{0x8B,0x53,0x30,0x8B,0x43,0x24,0,0},{0xC7,0x45,0x58,0xFF,0xFF,0xFF,0xFF,0},{0x0F,0xBE,0x86,0x74,0x05,0x00,0x00,0},{0x6A,0x00,0x6A,0x00,0x8D,0x4C,0x24,0x64},{0x8B,0xCB,0x8B,0x6F,0x04,0x8B,0x57,0x08},{0x81,0xE3,0x01,0x00,0x00,0x80,0,0},{0x81,0xE5,0x01,0x00,0x00,0x80,0,0},{0x8B,0x16,0x8D,0x44,0x24,0x74,0,0},{0x8D,0x8E,0x88,0,0,0,0,0},{0x0F,0xBE,0x8E,0x75,0x05,0,0,0}};
    const uintptr_t hooks[]={(uintptr_t)connection_start_hook,(uintptr_t)connection_finish_hook,(uintptr_t)connection_exit_hook,(uintptr_t)connection_occupied_hook,(uintptr_t)connection_approach_hook,(uintptr_t)connection_remaining_height_hook,(uintptr_t)connection_step_height_hook,(uintptr_t)connection_entry_hook,(uintptr_t)connection_remaining_horizontal_hook,(uintptr_t)connection_regular_horizontal_hook};
    for(unsigned i=0;i<10;++i)
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
