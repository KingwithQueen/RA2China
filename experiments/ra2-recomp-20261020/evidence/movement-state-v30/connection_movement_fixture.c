#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "native32.h"
#include "movement_fixture.h"
#include "ground_recovery_bridge.h"
#include "state_trace.h"

#define U32(address) (*(uint32_t *)(uintptr_t)(address))
#define U8(address) (*(uint8_t *)(uintptr_t)(address))

static uint32_t fixture_frame, fixture_id;
static uint32_t fixture_radius=1;
static int requested, applied;
static uint32_t recovery_host_stack;
static unsigned char recovery_stack[65536];

/* 实景局部入口试验：使用真实单位、原版停止/通知服务和原版栈布局。
 * 它不表示普通移动任务已经自然走到此入口；运行报告必须分别说明。 */
#pragma warning(push)
#pragma warning(disable: 4100) /* 裸函数按实际栈偏移读取参数，编译器不识别该引用。 */
static __declspec(naked) uint32_t invoke_original_recovery(uint32_t object, uint32_t frame)
{
    __asm
    {
        pushad
        mov recovery_host_stack, esp
        mov ebp, dword ptr [esp + 36]
        mov ecx, dword ptr [esp + 40]
        lea eax, returned
        mov dword ptr [ecx + 5Ch], eax
        mov esp, ecx
        mov eax, 4A2DFDh
        jmp eax
    returned:
        mov esp, recovery_host_stack
        mov dword ptr [esp + 28], eax
        popad
        ret
    }
}
#pragma warning(pop)

static void fixture_fail(const char *reason)
{
    fprintf(stderr, "[state-error] wall-ring fixture: %s\n", reason);
    fflush(stderr);
    ExitProcess(7);
}

int ra2_movement_fixture_arg(int argc, char **argv, int index)
{
    int unit_ring = !strcmp(argv[index], "--state-unit-ring");
    int budget_entry = !strcmp(argv[index], "--state-budget-entry");
    if (strcmp(argv[index], "--state-wall-ring") && !unit_ring && !budget_entry) return 0;
    char tail;
    int fields=0,valid=0;
    if (index+1<argc)
    {
        fields=sscanf(argv[index+1],"%u:%u:%u%c",&fixture_frame,&fixture_id,&fixture_radius,&tail);
        if (fields==3) valid=1;
        else if (fields==2) valid=sscanf(argv[index+1],"%u:%u%c",&fixture_frame,&fixture_id,&tail)==2;
    }
    if (requested || !valid || fixture_radius<1 || fixture_radius>3
        || (budget_entry && fixture_radius!=1))
    {
        fixture_fail("expected one FRAME:UID[:RADIUS], radius 1..3");
    }
    requested = budget_entry ? 3 : unit_ring ? 2 : 1;
    return 2;
}

int ra2_movement_fixture_requested(void)
{
    return requested;
}

/* 按原版 43C438..43C46D 的 new(0x9C) + OverlayClass 构造流程建墙。
 * 此辅助器只在显式试验参数开启时运行，不直接写路径队列、失败计数或碰撞结果。 */
#pragma optimize("y", off)
static uint32_t invoke_original(uint32_t target, uint32_t object, const uint32_t *arguments, unsigned count)
{
    uint32_t result;
    __asm
    {
        push ebx
        push esi
        push edi
        mov ebx, esp
        mov esi, arguments
        mov edi, count
    push_arguments:
        test edi, edi
        jz invoke
        dec edi
        push dword ptr [esi + edi * 4]
        jmp push_arguments
    invoke:
        mov ecx, object
        call target
        mov result, eax
        mov esp, ebx
        pop edi
        pop esi
        pop ebx
    }
    return result;
}
#pragma optimize("y", on)

static uint32_t fixture_call(int original_mode, uint32_t target, uint32_t object, const uint32_t *arguments, unsigned count)
{
    uint32_t saved[] = { g_eax,g_ecx,g_edx,g_esp,g_ebx,g_esi,g_edi,g_ebp,g_cur_func,
        g_flag_k,g_flag_a,g_flag_b,g_flag_cf,g_fs_base,g_gs_base,g_mxcsr };
    double floating[8];
    uint64_t mm[8];
    xmm_t xmm[8];
    memcpy(floating, g_st, sizeof(floating));
    memcpy(mm, g_mm, sizeof(mm));
    memcpy(xmm, g_xmm, sizeof(xmm));
    int top = g_fp_top;
    uint16_t control = g_fpu_cw;
    uint32_t result;
    if (target == 0x4A2DFD)
    {
        uint32_t frame = (uint32_t)(uintptr_t)(recovery_stack + 32768);
        memset(recovery_stack, 0, sizeof(recovery_stack));
        U32(frame + 0x14) = object + 4;
        if (original_mode)
        {
            result = invoke_original_recovery(object, frame);
        }
        else
        {
            g_esp = frame;
            g_ebp = object;
            ra2_state_movement_audit(3, object, 0, 0);
            ra2_ground_recover_path_bridge(0);
            result = g_eax;
        }
    }
    else if (original_mode)
    {
        result = invoke_original(target, object, arguments, count);
    }
    else
    {
        g_ecx = object;
        g_esp -= 0x100;
        native32_call_guest(target, (int)count, arguments);
        result = g_eax;
    }
    g_eax = saved[0]; g_ecx = saved[1]; g_edx = saved[2]; g_esp = saved[3];
    g_ebx = saved[4]; g_esi = saved[5]; g_edi = saved[6]; g_ebp = saved[7]; g_cur_func = saved[8];
    g_flag_k = saved[9]; g_flag_a = saved[10]; g_flag_b = saved[11]; g_flag_cf = saved[12];
    g_fs_base = saved[13]; g_gs_base = saved[14]; g_mxcsr = saved[15];
    memcpy(g_st, floating, sizeof(floating)); memcpy(g_mm, mm, sizeof(mm)); memcpy(g_xmm, xmm, sizeof(xmm));
    g_fp_top = top; g_fpu_cw = control;
    return result;
}

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
 if(id!=1023363&&id!=1023362&&id!=1022579&&id!=1022581&&id!=1032259&&id!=1032262)return;
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
void __cdecl ra2_chain_observe(uint32_t unit,uint32_t cell,uint32_t frame)
{
    unsigned upper=*(uint8_t *)(uintptr_t)(frame+0x11);
    uint32_t head=U32(cell+(upper?0xE8:0xE4));
    ra2_internal_observe(0,unit,18,(int32_t)upper,head?(int32_t)U32(head+0x10):0);
    unsigned lengths[2]={0,0};
    for(unsigned layer=0;layer<2;++layer){
        uint32_t object=U32(cell+(layer?0xE8:0xE4));
        while(object){if(++lengths[layer]>128)fixture_fail("cyclic object chain");object=U32(object+0x30);}
    }
    ra2_internal_observe(0,unit,23,(int32_t)lengths[0],(int32_t)lengths[1]);

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
        mov eax,dword ptr [ebp+12]
        add eax,4
        push eax
        push dword ptr [ebp+16]
        push dword ptr [ebp+8]
        call ra2_chain_observe
        add esp,12
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


static uint32_t round28_trampolines[2];
static __declspec(naked) void round28_hook_20(void)
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
        push 20
        push 0
        push dword ptr [ebp+8]
        call ra2_internal_observe
        add esp,20
        fxrstor [esp]
        mov esp,ebp
        popad
        popfd
        jmp dword ptr [round28_trampolines+0]
    }
}
static __declspec(naked) void round28_hook_21(void)
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
        push 21
        push dword ptr [ebp+8]
        push 0
        call ra2_internal_observe
        add esp,20
        fxrstor [esp]
        mov esp,ebp
        popad
        popfd
        jmp dword ptr [round28_trampolines+4]
    }
}
static void install_round28_hooks(void)
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

static uint32_t object_visit_trampoline;
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

static void connection_tick(FILE *output,int original_mode)
{
    if(connection_output) return;
    connection_output=output;
    if(!original_mode) return;
    install_internal_hooks();
    install_overlap_hooks();
    install_round28_hooks();
    install_object_visit_hook();
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

void ra2_movement_fixture_tick(uint32_t frame, FILE *output, int original_mode)
{
    connection_tick(output,original_mode);
    if (!requested || frame < fixture_frame || (requested != 3 && applied) || (requested == 3 && applied == 11)) return;
    if (frame != fixture_frame + (requested == 3 ? (uint32_t)applied : 0)) fixture_fail("frame skipped");
    uint32_t actor = 0, count = U32(0xA40C30), data = U32(0xA40C24);
    if (count > 16384) fixture_fail("invalid object vector");
    for (uint32_t i = 0; i < count; ++i)
    {
        uint32_t object = U32(data + i * 4);
        if (U32(object + 0x10) == fixture_id) actor = object;
    }
    if (!actor || U32(actor) != 0x7ADDF8) fixture_fail("missing UnitClass actor");
    uint32_t locomotion = U32(actor + 0x564);
    if (!locomotion || U32(locomotion) != 0x7A04CC) fixture_fail("actor is not a ground driver");
    uint32_t drive = locomotion - 4;
    if (requested == 3)
    {
        int32_t before = (int32_t)U32(actor + 0x53C);
        int32_t expected = applied < 10 ? 10 - applied : 0;
        if (before != expected) fixture_fail("unexpected natural initial failure budget");
        uint32_t result = fixture_call(original_mode, 0x4A2DFD, drive, NULL, 0) & 255u;
        int32_t after = (int32_t)U32(actor + 0x53C);
        if (after != (before > 0 ? before - 1 : 0)) fixture_fail("recovery entry budget transition failed");
        fprintf(output, "{\"kind\":\"fixture-budget-entry\",\"frame\":%u,\"id\":%u,\"before\":%d,\"after\":%d,\"result\":%u}\n",
            frame, fixture_id, before, after, result);
        ++applied;
        return;
    }
    if (!U32(drive + 0x34) && !U32(drive + 0x38) && !U32(drive + 0x3C)) fixture_fail("move was not accepted before wall placement");
    uint32_t destination_argument = drive + 0x34;
    uint32_t accepted_before = fixture_call(original_mode, U32(U32(actor) + 0x2AC), actor, &destination_argument, 1) & 255u;
    uint32_t type = U32(U32(0xA35DEC) + 26 * 4);
    if (strcmp((const char *)(uintptr_t)(type + 0x24), "NAWALL") || !U8(type + 0x278)) fixture_fail("unexpected overlay type");
    int32_t x = (int32_t)U32(actor + 0x88) / 256, y = (int32_t)U32(actor + 0x8C) / 256;
    uint32_t house = U32(actor + 0x1B4), wall_owner = U32(house + 0x30);
    uint32_t cells[24], coordinates[24], placed = 0;
    /* 先核实全部位置，避免遇到已有对象/覆盖物后留下半个试验条件。 */
    int radius=(int)fixture_radius;
    for (int dy = -radius; dy <= radius; ++dy)
    {
        for (int dx = -radius; dx <= radius; ++dx)
        {
            if (abs(dx)!=radius && abs(dy)!=radius) continue;
            int32_t cx = x + dx, cy = y + dy;
            if (cx < 0 || cx >= 512 || cy < 0 || cy >= 512) fixture_fail("cell outside vector");
            uint32_t cell = U32(U32(0x832618) + (cy * 512 + cx) * 4);
            if (!cell || U32(cell + 0x44) != UINT32_MAX || U32(cell + 0xE4) || U32(cell + 0xE8))
                fixture_fail("ring cell is not empty");
            cells[placed] = cell;
            coordinates[placed++] = (uint16_t)cx | (uint32_t)(uint16_t)cy << 16;
        }
    }
    for (uint32_t i = 0; i < placed; ++i)
    {
        if (requested == 2)
        {
            /* 临时单位障碍不重分地形通行区，适合检验重寻路失败的有限预算。 */
            if (U32(0xA322A8) < 2) fixture_fail("missing blocker house");
            uint32_t enemy_house = U32(U32(0xA3229C) + 4);
            if (enemy_house == house) fixture_fail("blocker house equals actor house");
            uint32_t unit_type = U32(actor + 0x5AC), size = 0x7D0;
            uint32_t blocker = fixture_call(original_mode, 0x782017, 0, &size, 1);
            if (!blocker) fixture_fail("unit allocation failed");
            uint32_t constructor_arguments[2] = { unit_type, enemy_house };
            fixture_call(original_mode, 0x6FA400, blocker, constructor_arguments, 2);
            int32_t point[3] = { (int16_t)(coordinates[i] & 0xFFFF) * 256 + 128,
                (int16_t)(coordinates[i] >> 16) * 256 + 128, (int32_t)U32(actor + 0x90) };
            uint32_t placement_arguments[2] = { (uint32_t)(uintptr_t)point, 0 };
            uint32_t success = fixture_call(original_mode, U32(U32(blocker) + 0xD4), blocker, placement_arguments, 2);
            if (!(success & 255u) || !U8(blocker + 0x74) || U32(blocker + 0x88) != (uint32_t)point[0]
                || U32(blocker + 0x8C) != (uint32_t)point[1]) fixture_fail("engine did not place blocker unit");
            fprintf(output, "{\"kind\":\"fixture-unit\",\"frame\":%u,\"id\":%u,\"blocker_id\":%u,\"cell\":[%u,%u]}\n",
                frame, fixture_id, U32(blocker + 0x10), coordinates[i] & 0xFFFF, coordinates[i] >> 16);
            continue;
        }
        uint32_t size = 0x9C;
        uint32_t overlay = fixture_call(original_mode, 0x782017, 0, &size, 1);
        if (!overlay) fixture_fail("engine allocation failed");
        uint32_t arguments[3] = { type, (uint32_t)(uintptr_t)&coordinates[i], wall_owner };
        fixture_call(original_mode, 0x5DA7D0, overlay, arguments, 3);
        if (U32(cells[i] + 0x44) != 26)
        {
            fprintf(stderr, "[state-fixture-detail] cell=%u,%u overlay=%d owner=%d expected-owner=%u flags=%u,%u active=%u\n",
                coordinates[i] & 0xFFFF, coordinates[i] >> 16, (int32_t)U32(cells[i] + 0x44),
                (int32_t)U32(cells[i] + 0x50), wall_owner, U8(overlay + 0x74), U8(overlay + 0x76), U8(0xA40958));
            fixture_fail("engine did not place the wall");
        }
        /* 原版运行中建墙采用其当前墙体归属全局量，可能得到无主墙；如实记录，不代改归属。 */
        fprintf(output, "{\"kind\":\"fixture-wall\",\"frame\":%u,\"id\":%u,\"cell\":[%u,%u],\"overlay\":26,\"owner\":%d}\n",
            frame, fixture_id, coordinates[i] & 0xFFFF, coordinates[i] >> 16, (int32_t)U32(cells[i] + 0x50));
    }
    applied = 1;
    uint32_t accepted_after = fixture_call(original_mode, U32(U32(actor) + 0x2AC), actor, &destination_argument, 1) & 255u;
    uint32_t rebuilt = UINT32_MAX;
    if (requested == 2 && fixture_radius == 1)
    {
        /* 保留早期一格压力试验的显式重建步骤。新增两/三格包围不调用这里，
           让正常移动更新自行发现障碍；不得提前清掉正在观察的残余路径。 */
        int32_t destination_x = (int32_t)U32(drive + 0x34) / 256;
        int32_t destination_y = (int32_t)U32(drive + 0x38) / 256;
        uint32_t rebuild_arguments[3] = { (uint16_t)destination_x | (uint32_t)(uint16_t)destination_y << 16, 0, 0 };
        rebuilt = fixture_call(original_mode, 0x4C3000, actor, rebuild_arguments, 3) & 255u;
    }
    fprintf(output, "{\"kind\":\"fixture-constraints\",\"frame\":%u,\"id\":%u,\"accepted_before\":%u,\"accepted_after\":%u,"
        "\"close_enough\":%d,\"explicit_rebuild_result\":%u,\"path_head\":%d}\n", frame, fixture_id, accepted_before, accepted_after,
        (int32_t)U32(U32(0x839848) + 0x1380), rebuilt, (int32_t)U32(actor + 0x4D0));
    fprintf(stderr, "[state-fixture] frame=%u actor=%u kind=%s count=%u engine-created\n",
        frame, fixture_id, requested == 2 ? "units" : "walls", placed);
}
