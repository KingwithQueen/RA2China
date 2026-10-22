#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>
#include "recomp_types.h"
#include "ground_barrier_bridge.h"
#include "native_probe_host.h"

uint32_t g_eax, g_ecx, g_edx, g_esp, g_ebx, g_esi, g_edi, g_ebp, g_cur_func;
static unsigned char actor[0x700], actor_type[0xC00], cell[0x200], overlay[0x300], weapon[0xB0], warhead[0x200];
static unsigned char building[0x500], building_type[0x1400], private_stack[4096];
static uint32_t actor_vtable[0x400 / 4], overlay_pointer, weapon_holder, fixture, previous_result;
static uint32_t operations[16][3], operation_count;
static uint32_t host_stack, frame_stack, entry_address, native_eax, native_esp, native_flags, native_resume;
static uint32_t native_ebx, native_esi, native_edi, native_ebp, native_rank, native_next, native_type;
static uint32_t native_stack_result;
#define POINTER(value) ((uint32_t)(uintptr_t)(value))
#define FIELD32(buffer,offset) (*(uint32_t *)((buffer) + (offset)))

static void record(uint32_t operation, uint32_t object, uint32_t argument)
{
    if (operation_count == 16) exit(2);
    operations[operation_count][0] = operation;
    operations[operation_count][1] = object;
    operations[operation_count++][2] = argument;
}
static uint32_t __fastcall house_permission(uint32_t object, uint32_t ignored)
{
    (void)ignored; record(0, object, 0);
    if (fixture & (1u << 16)) MEM32(0xA3D298) = 1;
    return (fixture >> 9) & 1;
}
static uint32_t __fastcall ability(uint32_t object, uint32_t ignored, uint32_t value)
{
    (void)ignored; record(1, object, value); return (fixture >> 8) & 1;
}
static uint32_t __fastcall wall_allied(uint32_t object, uint32_t ignored, uint32_t value)
{
    (void)ignored; record(2, object, value); return (fixture >> 10) & 1;
}
static uint32_t __fastcall can_attack(uint32_t object, uint32_t ignored)
{
    (void)ignored; record(3, object, 0); return (fixture >> 11) & 1;
}
static uint32_t __fastcall get_weapon(uint32_t object, uint32_t ignored, uint32_t value)
{
    (void)ignored; record(4, object, value); return POINTER(&weapon_holder);
}
static uint32_t __fastcall gate_passable(uint32_t object, uint32_t ignored)
{
    (void)ignored; record(5, object, 0); return (fixture >> 12) & 1;
}
static uint32_t __fastcall gate_allied(uint32_t object, uint32_t ignored, uint32_t value)
{
    (void)ignored; record(6, object, value); return (fixture >> 13) & 1;
}
static void l_permission(void) { g_eax = house_permission(g_ecx, 0); g_esp += 4; }
static void l_ability(void) { g_eax = ability(g_ecx, 0, MEM32(g_esp + 4)); g_esp += 8; }
static void l_wall_allied(void) { g_eax = wall_allied(g_ecx, 0, MEM32(g_esp + 4)); g_esp += 8; }
static void l_can_attack(void) { g_eax = can_attack(g_ecx, 0); g_esp += 4; }
static void l_weapon(void) { g_eax = get_weapon(g_ecx, 0, MEM32(g_esp + 4)); g_esp += 8; }
static void l_gate(void) { g_eax = gate_passable(g_ecx, 0); g_esp += 4; }
static void l_gate_allied(void) { g_eax = gate_allied(g_ecx, 0, MEM32(g_esp + 4)); g_esp += 8; }
recomp_func_t recomp_lookup_manual(uint32_t address)
{
    if (address == 0x4F52F0) return l_permission;
    if (address == 0x6D7910) return l_ability;
    if (address == 0x4E5500) return l_wall_allied;
    if (address == 0x44D880) return l_gate;
    if (address == 0x4E5540) return l_gate_allied;
    if (address == POINTER(can_attack)) return l_can_attack;
    return address == POINTER(get_weapon) ? l_weapon : NULL;
}
recomp_func_t recomp_lookup(uint32_t address) { (void)address; return NULL; }
recomp_func_t recomp_lookup_import(uint32_t address) { (void)address; return NULL; }
static void patch_jump(uint32_t address, uint32_t destination)
{
    MEM8(address) = 0xE9; MEM32(address + 1) = destination - address - 5;
}
static __declspec(naked) void continue_trap(void)
{
    __asm
    {
        mov native_rank, edi
        mov native_next, esi
        mov native_type, eax
        mov eax, 0
        mov edi, dword ptr [esp]
        mov esi, dword ptr [esp + 4]
        mov ebp, dword ptr [esp + 8]
        mov ebx, dword ptr [esp + 12]
        add esp, 78h
        ret 14h
    }
}
static __declspec(naked) void execute_original(void)
{
    __asm
    {
        push ebp
        push ebx
        push esi
        push edi
        mov host_stack, esp
        mov esp, frame_stack
        lea eax, returned
        mov dword ptr [esp + 78h], eax
        lea ebp, actor
        lea ebx, cell
        lea esi, building
        mov edi, previous_result
        jmp entry_address
    returned:
        mov native_esp, esp
        mov native_eax, eax
        mov eax, frame_stack
        mov eax, dword ptr [eax + 8Ch]
        mov native_stack_result, eax
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
static void initialize(unsigned number)
{
    fixture = number * 1664525u + 1013904223u;
    fixture ^= fixture << 13; fixture ^= fixture >> 17; fixture ^= fixture << 5;
    memset(actor, 0, sizeof(actor)); memset(actor_type, 0, sizeof(actor_type)); memset(cell, 0, sizeof(cell));
    memset(overlay, 0, sizeof(overlay)); memset(building, 0, sizeof(building)); memset(building_type, 0, sizeof(building_type));
    memset(weapon, 0, sizeof(weapon)); memset(warhead, 0, sizeof(warhead));
    memset(private_stack, 0xA5, sizeof(private_stack)); memset(operations, 0, sizeof(operations));
    operation_count = native_resume = 0;
    FIELD32(actor, 0) = POINTER(actor_vtable); FIELD32(actor, 0x5AC) = POINTER(actor_type);
    FIELD32(actor, 0x1B4) = 0x12345678; FIELD32(building, 0x1B4) = 0x23456789;
    FIELD32(building, 0x418) = POINTER(building_type); FIELD32(building, 0x30) = 0x3456789A;
    FIELD32(cell, 0x44) = (fixture & 1) ? 0 : UINT32_MAX; FIELD32(cell, 0x50) = 7;
    overlay_pointer = POINTER(overlay); MEM32(0xA35DEC) = POINTER(&overlay_pointer);
    overlay[0x27A] = (uint8_t)((fixture >> 1) & 1); overlay[0x278] = (uint8_t)((fixture >> 2) & 1);
    overlay[0x1FD] = (uint8_t)((fixture >> 3) & 1); actor_type[0xAF3] = (uint8_t)((fixture >> 4) & 1);
    FIELD32(overlay, 0x9C) = (fixture & 32) ? 6 : 2;
    warhead[0x144] = (uint8_t)((fixture >> 6) & 1); warhead[0x146] = (uint8_t)((fixture >> 7) & 1);
    weapon_holder = POINTER(weapon); FIELD32(weapon, 0xAC) = POINTER(warhead);
    building_type[0x1351] = (uint8_t)((fixture >> 14) & 1); MEM32(0xA3D298) = (fixture >> 15) & 1;
    const int32_t ranks[] = { -1,0,1,2,3,4,5,6,7,INT_MAX,INT_MIN };
    previous_result = (uint32_t)ranks[number % 11];
    frame_stack = POINTER(private_stack + 2048);
    MEM32(frame_stack) = 0x12345678; MEM32(frame_stack + 4) = 0x23456789;
    MEM32(frame_stack + 8) = 0x3456789A; MEM32(frame_stack + 12) = 0x456789AB;
    MEM32(frame_stack + 0x8C) = 1234567;
}
int main(int argc, char **argv)
{
    if (argc != 2) return 2;
    hold_image(); map_original_image(argv[1]);
    patch_jump(0x4F52F0, POINTER(house_permission)); patch_jump(0x6D7910, POINTER(ability));
    patch_jump(0x4E5500, POINTER(wall_allied)); patch_jump(0x44D880, POINTER(gate_passable));
    patch_jump(0x4E5540, POINTER(gate_allied));
    actor_vtable[0x28C / 4] = POINTER(can_attack); actor_vtable[0x39C / 4] = POINTER(get_weapon);
    unsigned char *stubs = VirtualAlloc(NULL, 4096, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);
    if (!stubs) return 2;
    const uint32_t boundaries[] = { 0x703439,0x7035AC,0x7038FD };
    for (unsigned i = 0; i < 3; ++i)
    {
        unsigned char *stub = stubs + i * 16;
        stub[0] = 0xC7; stub[1] = 5; uint32_t destination = POINTER(&native_resume);
        memcpy(stub + 2, &destination, 4); memcpy(stub + 6, &boundaries[i], 4); stub[10] = 0xE9;
        uint32_t relative = POINTER(continue_trap) - POINTER(stub + 15); memcpy(stub + 11, &relative, 4);
        patch_jump(boundaries[i], POINTER(stub));
    }
    FlushInstructionCache(GetCurrentProcess(), NULL, 0);
    unsigned blocked[2] = { 0 }, continued[2] = { 0 };
    for (unsigned phase = 0; phase < 2; ++phase)
    {
        entry_address = phase ? 0x703536 : 0x703331;
        for (unsigned number = 0; number < 65536; ++number)
        {
            initialize(number); execute_original();
            uint32_t expected_ops[16][3], expected_count = operation_count, expected_resume = native_resume;
            uint32_t expected_stack_result = native_stack_result, expected_global = MEM32(0xA3D298);
            memcpy(expected_ops, operations, sizeof(expected_ops));
            initialize(number);
            g_esp = frame_stack; g_ebp = POINTER(actor); g_ebx = POINTER(cell); g_esi = POINTER(building); g_edi = previous_result;
            uint32_t resume = phase ? ra2_ground_gate_bridge() : ra2_ground_overlay_bridge();
            uint32_t flags = recomp_eflags(g_flag_k, g_flag_a, g_flag_b, g_flag_cf, 1);
            int abi_diff = resume ? (g_esp != frame_stack || g_ebp != POINTER(actor) || g_ebx != POINTER(cell) || g_edi != native_rank
                || (phase && (g_esi != native_next || (resume == 0x7035AC && g_eax != native_type))))
                : (g_eax != native_eax || g_esp != native_esp || g_ebx != native_ebx || g_esi != native_esi
                    || g_edi != native_edi || g_ebp != native_ebp || (flags & 0x8D5) != (native_flags & 0x8D5));
            if (abi_diff || resume != expected_resume || expected_count != operation_count
                || memcmp(expected_ops, operations, sizeof(expected_ops)) || expected_stack_result != MEM32(frame_stack + 0x8C)
                || expected_global != MEM32(0xA3D298))
            {
                printf("barrier mismatch phase=%u case=%u fixture=%x abi=%d resume=%x/%x calls=%u/%u\n",
                    phase, number, fixture, abi_diff, resume, expected_resume, operation_count, expected_count);
                printf("  stack=%x/%x global=%x/%x rank=%x/%x\n", MEM32(frame_stack + 0x8C), expected_stack_result,
                    MEM32(0xA3D298), expected_global, g_edi, native_rank);
                for (unsigned i = 0; i < operation_count || i < expected_count; ++i)
                    printf("  operation=%u/%u object=%x/%x arg=%x/%x\n", operations[i][0], expected_ops[i][0],
                        operations[i][1], expected_ops[i][1], operations[i][2], expected_ops[i][2]);
                return 1;
            }
            if (resume) ++continued[phase]; else ++blocked[phase];
        }
    }
    printf("{\"passed\":true,\"overlay_cases\":65536,\"gate_cases\":65536,\"blocked\":[%u,%u],\"continued\":[%u,%u],"
        "\"query_order_and_abi_verified\":true}\n", blocked[0], blocked[1], continued[0], continued[1]);
    return 0;
}
