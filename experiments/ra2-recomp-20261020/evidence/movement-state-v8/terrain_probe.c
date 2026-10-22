#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "recomp_types.h"
#include "ground_collision_bridge.h"
#include "native_probe_host.h"

uint32_t g_eax, g_ecx, g_edx, g_esp, g_ebx, g_esi, g_edi, g_ebp, g_cur_func;
static unsigned char actor[0x700], actor_type[0xC00], cell[0x200], tile[0x300], stack_data[4096];
static uint32_t tiles[1], frame, host_stack, native_eax, native_esp, native_flags;
static uint32_t native_ebx, native_esi, native_edi, native_ebp, continued;
#define PTR(value) ((uint32_t)(uintptr_t)(value))
recomp_func_t recomp_lookup_manual(uint32_t a) { (void)a; return NULL; }
recomp_func_t recomp_lookup(uint32_t a) { (void)a; return NULL; }
recomp_func_t recomp_lookup_import(uint32_t a) { (void)a; return NULL; }

static __declspec(naked) void continuation(void)
{
    __asm
    {
        mov continued, 1
        xor eax, eax
        mov edi, dword ptr [esp]
        mov esi, dword ptr [esp + 4]
        mov ebp, dword ptr [esp + 8]
        mov ebx, dword ptr [esp + 12]
        add esp, 78h
        ret 14h
    }
}

static __declspec(naked) void original(void)
{
    __asm
    {
        push ebp
        push ebx
        push esi
        push edi
        mov host_stack, esp
        mov esp, frame
        lea eax, returned
        mov dword ptr [esp + 78h], eax
        lea ebp, actor
        lea ebx, cell
        lea ecx, actor_type
        mov esi, 13579BDFh
        mov edi, 2468ACE0h
        mov eax, 7030B6h
        jmp eax
    returned:
        mov native_eax, eax
        mov native_esp, esp
        pushfd
        pop native_flags
        mov native_ebx, ebx
        mov native_esi, esi
        mov native_edi, edi
        mov native_ebp, ebp
        mov esp, host_stack
        pop edi
        pop esi
        pop ebx
        pop ebp
        ret
    }
}

static void initialize(unsigned n)
{
    memset(stack_data, 0xA5, sizeof(stack_data));
    frame = PTR(stack_data + 2048);
    for (unsigned i = 0; i < 4; ++i) MEM32(frame + i * 4) = 0x12345678u + i;
    MEM32(PTR(actor) + 0x5AC) = PTR(actor_type);
    MEM32(PTR(actor_type) + 0xB94) = (n % 7 == 0) ? UINT32_MAX : (n / 7) % 12;
    MEM32(PTR(cell) + 0xEC) = n % 12;
    MEM32(PTR(cell) + 0x44) = (n / 12) % 5 + 235;
    cell[0x11B] = (uint8_t)(n / 60);
    cell[0x11A] = (uint8_t)((n / 17) % 8);
    MEM32(frame + 0x84) = (uint32_t)((int8_t)cell[0x11B] + (int32_t)((n / 11) % 5) - 2);
    MEM32(PTR(tile) + 0x2B4) = (n / 13) % 7;
    MEM32(PTR(tile) + 0x2B8) = (n / 19) % 7;
    tiles[0] = PTR(tile); MEM32(0xA40CD4) = PTR(tiles);
    continued = 0;
}

int main(int argc, char **argv)
{
    if (argc != 2) return 2;
    hold_image(); map_original_image(argv[1]);
    MEM8(0x703182) = 0xE9;
    MEM32(0x703183) = PTR(continuation) - 0x703187;
    FlushInstructionCache(GetCurrentProcess(), NULL, 0);
    unsigned pass = 0, blocked = 0;
    for (unsigned n = 0; n < 524288; ++n)
    {
        initialize(n); original();
        unsigned expected_continue = continued;
        initialize(n);
        g_esp = frame; g_ebp = PTR(actor); g_ebx = PTR(cell); g_esi = 0x13579BDF; g_edi = 0x2468ACE0;
        int actual_continue = ra2_ground_terrain_bridge();
        uint32_t flags = recomp_eflags(g_flag_k, g_flag_a, g_flag_b, g_flag_cf, 1);
        int abi_bad = actual_continue ? (g_esp != frame || g_ebp != PTR(actor) || g_ebx != PTR(cell) || g_esi != 0x13579BDF)
            : (g_eax != native_eax || g_esp != native_esp || g_ebx != native_ebx || g_esi != native_esi
                || g_edi != native_edi || g_ebp != native_ebp || (flags & 0x8D5) != (native_flags & 0x8D5));
        if (actual_continue != (int)expected_continue || abi_bad)
        {
            printf("terrain mismatch %u continue=%u/%u abi=%d\n", n, actual_continue, expected_continue, abi_bad);
            return 1;
        }
        if (actual_continue) ++pass; else ++blocked;
    }
    printf("{\"passed\":true,\"native_cases\":524288,\"allowed\":%u,\"blocked\":%u,\"abi_verified\":true}\n", pass, blocked);
    return 0;
}
