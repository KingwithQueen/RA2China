#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>
#include "recomp_types.h"
#include "ground_collision.h"
#include "ground_collision_bridge.h"
#include "native_probe_host.h"

uint32_t g_eax, g_ecx, g_edx, g_esp, g_ebx, g_esi, g_edi, g_ebp, g_cur_func;
static unsigned char actor[0x700], actor_type[0xC00], cell[0x200], vehicle[0x600], vehicle_type[0x200];
static unsigned char weapon[0xB0], projectile[0x300], private_stack[4096];
static uint32_t actor_vtable[0x400 / 4], weapon_holder, fixture;
static uint32_t operations[8], operation_count;
static uint32_t saved_stack, frame_stack, native_eax, native_esp, native_flags;
static uint32_t native_ebx, native_esi, native_edi, native_ebp, layer_resume, layer_result, layer_reference;

#define POINTER(value) ((uint32_t)(uintptr_t)(value))

static void record(unsigned operation)
{
    if (operation_count >= 8) exit(2);
    operations[operation_count++] = operation;
}
static uint32_t __fastcall allied(uint32_t object, uint32_t ignored, int32_t owner_index)
{
    (void)object; (void)ignored; (void)owner_index; record(0); return fixture & 1;
}
static uint32_t __fastcall ability(uint32_t object, uint32_t ignored, int32_t value)
{
    (void)object; (void)ignored;
    if (value != 17) exit(2);
    record(1); return (fixture >> 1) & 1;
}
static uint32_t __fastcall get_weapon(uint32_t object, uint32_t ignored, int32_t value)
{
    (void)object; (void)ignored; (void)value; record(2); return POINTER(&weapon_holder);
}
static uint32_t __fastcall get_vehicle(uint32_t object, uint32_t ignored, int32_t value)
{
    (void)object; (void)ignored; (void)value; record(3); return (fixture & 4) ? POINTER(vehicle) : 0;
}

static void lifted_allied(void) { g_eax = allied(g_ecx, 0, (int32_t)MEM32(g_esp + 4)); g_esp += 8; }
static void lifted_ability(void) { g_eax = ability(g_ecx, 0, (int32_t)MEM32(g_esp + 4)); g_esp += 8; }
static void lifted_weapon(void) { g_eax = get_weapon(g_ecx, 0, (int32_t)MEM32(g_esp + 4)); g_esp += 8; }
static void lifted_vehicle(void) { g_eax = get_vehicle(g_ecx, 0, (int32_t)MEM32(g_esp + 4)); g_esp += 8; }
recomp_func_t recomp_lookup_manual(uint32_t address)
{
    if (address == 0x4E5500) return lifted_allied;
    if (address == 0x6D7910) return lifted_ability;
    if (address == 0x473E30) return lifted_vehicle;
    if (address == POINTER(get_weapon)) return lifted_weapon;
    return NULL;
}
recomp_func_t recomp_lookup(uint32_t address) { (void)address; return NULL; }
recomp_func_t recomp_lookup_import(uint32_t address) { (void)address; return NULL; }

static void patch_jump(uint32_t address, uint32_t destination)
{
    MEM8(address) = 0xE9;
    MEM32(address + 1) = destination - address - 5;
}

static __declspec(naked) void execute_tail(void)
{
    __asm
    {
        push ebp
        push ebx
        push esi
        push edi
        mov saved_stack, esp
        lea ebp, actor
        lea ebx, cell
        mov esp, frame_stack
        mov edi, dword ptr [esp + 8Ch]
        lea eax, returned
        mov dword ptr [esp + 78h], eax
        mov eax, 00703AA9h
        jmp eax
    returned:
        mov native_esp, esp
        pushfd
        pop native_flags
        mov native_eax, eax
        mov native_ebx, ebx
        mov native_esi, esi
        mov native_edi, edi
        mov native_ebp, ebp
        mov esp, saved_stack
        pop edi
        pop esi
        pop ebx
        pop ebp
        ret
    }
}

static LONG CALLBACK layer_trap(EXCEPTION_POINTERS *exception)
{
    if (exception->ExceptionRecord->ExceptionCode != EXCEPTION_BREAKPOINT
        || (uintptr_t)exception->ExceptionRecord->ExceptionAddress != 0x703087) return EXCEPTION_CONTINUE_SEARCH;
    layer_result = MEM8(exception->ContextRecord->Esp + 0x11);
    exception->ContextRecord->Esp = saved_stack;
    exception->ContextRecord->Eip = layer_resume;
    return EXCEPTION_CONTINUE_EXECUTION;
}

static __declspec(naked) void execute_layer(void)
{
    __asm
    {
        push ebp
        push ebx
        push esi
        push edi
        mov saved_stack, esp
        lea eax, returned
        mov layer_resume, eax
        push 1
        push 0
        push layer_reference
        push 8
        lea eax, cell
        push eax
        lea ecx, actor
        mov eax, 00703040h
        call eax
    returned:
        mov esp, saved_stack
        pop edi
        pop esi
        pop ebx
        pop ebp
        ret
    }
}

static void initialize(unsigned value, int32_t previous)
{
    fixture = value;
    memset(operations, 0, sizeof(operations)); operation_count = 0;
    memset(private_stack, 0xA5, sizeof(private_stack));
    frame_stack = POINTER(private_stack + 2048);
    MEM32(frame_stack) = 0x3456789A;
    MEM32(frame_stack + 4) = 0x23456789;
    MEM32(frame_stack + 8) = 0x456789AB;
    MEM32(frame_stack + 12) = 0x12345678;
    MEM8(frame_stack + 0x12) = (uint8_t)((value >> 3) & 63);
    MEM8(frame_stack + 0x13) = (uint8_t)((value >> 9) & 1);
    MEM32(frame_stack + 0x18) = (value & 1024) ? 3 : UINT32_MAX;
    MEM8(frame_stack + 0x88) = (uint8_t)((value >> 11) & 1);
    MEM32(frame_stack + 0x8C) = (uint32_t)previous;
    MEM32(POINTER(actor)) = POINTER(actor_vtable);
    MEM32(POINTER(actor) + 0x5AC) = POINTER(actor_type);
    MEM32(POINTER(vehicle) + 0x5AC) = POINTER(vehicle_type);
    MEM32(POINTER(weapon) + 0xA0) = POINTER(projectile);
    actor_type[0xAF3] = (uint8_t)((value >> 12) & 1);
    actor_type[0xAA0] = (uint8_t)((value >> 13) & 1);
    vehicle_type[0x1FD] = (uint8_t)((value >> 14) & 1);
    weapon_holder = (value & 32768) ? POINTER(weapon) : 0;
    projectile[0x275] = (uint8_t)((value >> 16) & 1);
}

int main(int argc, char **argv)
{
    if (argc != 2) return 2;
    hold_image(); map_original_image(argv[1]);
    patch_jump(0x4E5500, POINTER(allied)); patch_jump(0x6D7910, POINTER(ability)); patch_jump(0x473E30, POINTER(get_vehicle));
    actor_vtable[0x39C / 4] = POINTER(get_weapon);
    FlushInstructionCache(GetCurrentProcess(), NULL, 0);
    unsigned checked = 0;
    for (unsigned value = 0; value < 131072; ++value)
    {
        int32_t previous = (value % 3) ? 0 : (int32_t)((value >> 3) % 8);
        initialize(value, previous); execute_tail();
        uint32_t expected_operations[8], expected_count = operation_count;
        memcpy(expected_operations, operations, sizeof(operations));
        initialize(value, previous);
        g_esp = frame_stack; g_ebp = POINTER(actor); g_ebx = POINTER(cell); g_edi = (uint32_t)previous;
        ra2_ground_collision_finish_bridge();
        uint32_t flags = recomp_eflags(g_flag_k, g_flag_a, g_flag_b, g_flag_cf, 1);
        if (g_eax != native_eax || g_esp != native_esp || g_ebx != native_ebx || g_esi != native_esi || g_edi != native_edi
            || g_ebp != native_ebp || (flags & 0x8D5) != (native_flags & 0x8D5) || operation_count != expected_count
            || memcmp(expected_operations, operations, sizeof(operations)))
        {
            printf("collision mismatch case=%u previous=%d result=%u/%u calls=%u/%u\n", value, previous, g_eax, native_eax,
                operation_count, expected_count);
            return 1;
        }
        ++checked;
    }
    MEM8(0x703087) = 0xCC;
    FlushInstructionCache(GetCurrentProcess(), NULL, 0);
    void *handler = AddVectoredExceptionHandler(1, layer_trap);
    if (!handler) return 2;
    const int32_t reference_values[] = { INT32_MIN, -256, -129, -128, -127, -2, -1, 0, 1, 2, 126, 127, 128, 129, 256, INT32_MAX };
    unsigned layer_cases = 0;
    for (int32_t level = -128; level <= 127; ++level)
    {
        cell[0x11B] = (uint8_t)level;
        for (unsigned bridge = 0; bridge < 2; ++bridge)
        {
            MEM32(POINTER(cell) + 0x140) = bridge ? 0x100 : 0;
            for (unsigned i = 0; i < sizeof(reference_values) / sizeof(*reference_values); ++i)
            {
                layer_reference = (uint32_t)reference_values[i]; execute_layer();
                int actual = ra2_ground_uses_bridge_occupation(bridge, reference_values[i], level);
                if (actual != (int)layer_result) { printf("layer mismatch %u/%d/%d\n", bridge, reference_values[i], level); return 1; }
                ++layer_cases;
            }
        }
    }
    RemoveVectoredExceptionHandler(handler);
    printf("{\"passed\":true,\"native_occupation_cases\":%u,\"native_bridge_layer_cases\":%u,\"query_order_and_abi_verified\":true}\n",
        checked, layer_cases);
    return 0;
}
