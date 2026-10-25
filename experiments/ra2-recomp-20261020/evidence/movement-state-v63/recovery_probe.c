#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>
#include "recomp_types.h"
#include "ground_recovery_bridge.h"
#include "native_probe_host.h"

uint32_t g_eax, g_ecx, g_edx, g_esp, g_ebx, g_esi, g_edi, g_ebp, g_cur_func;
enum Operation { STOP_EMPTY, STOP_TARGET, CANCEL, SOUND, MOVING, ACCEPT_OBJECT, LINKED, NOTIFY_OWNER, OP_COUNT };
static const unsigned argument_count[OP_COUNT] = { 2,2,0,2,1,1,0,1 };
static unsigned char drive[128], owner[0x700], linked[0x100], rules[0x700], private_stack[4096];
static uint32_t owner_vtable[0x500 / 4], locomotion_vtable[0x100 / 4], fixture, stub_base;
static uint32_t operations[32][12], operation_count, cleanup_bytes;
static uint32_t frame_stack, host_stack, native_eax, native_esp, native_flags, entry_address;
static uint32_t native_ebx, native_esi, native_edi, native_ebp;
static unsigned finish_only;
#define POINTER(value) ((uint32_t)(uintptr_t)(value))
#define FIELD32(buffer,offset) (*(uint32_t *)((buffer) + (offset)))

static uint32_t operation(unsigned id, uint32_t object, const uint32_t *arguments, uint32_t edx)
{
    if (operation_count == 32) exit(2);
    uint32_t *record = operations[operation_count++];
    record[0] = id; record[5] = FIELD32(drive, 0x40); record[6] = FIELD32(drive, 0x58);
    record[7] = drive[0x61]; record[8] = drive[0x63]; record[9] = FIELD32(owner, 0x53C);
    record[10] = owner[0x578]; record[11] = owner[0x57A];
    if (id == STOP_EMPTY || id == STOP_TARGET) memcpy(record + 1, arguments, 8);
    if (id == MOVING || id == ACCEPT_OBJECT || id == NOTIFY_OWNER) record[1] = arguments[0];
    if (id == LINKED) record[1] = object;
    switch (id)
    {
        case STOP_EMPTY:
        case STOP_TARGET:
            if (fixture & (1u << 8)) owner[0x7D] = 0;
            if (fixture & (1u << 9)) FIELD32(drive, 0x40) = 999;
            return (fixture & 1) ? 0xFF : 0;
        case CANCEL:
            FIELD32(owner, 0x488) = 0;
            if (fixture & (1u << 12)) drive[0x63] = 1;
            return 0;
        case SOUND:
            record[1] = object; record[2] = edx; record[3] = arguments[0]; record[4] = arguments[1];
            if (fixture & (1u << 13)) { FIELD32(owner, 0x53C) = 42; owner[0x57A] = 7; }
            return 0;
        case MOVING: return (fixture >> 1) & 1;
        case ACCEPT_OBJECT: return (fixture >> 2) & 1;
        case LINKED:
            FIELD32(drive, 0x58) = 5; drive[0x61] = 1;
            return 0;
        case NOTIFY_OWNER:
            if (fixture & (1u << 14)) owner[0x578] = 0;
            return 0;
        default: exit(2);
    }
}
static uint32_t native_operation(unsigned id, uint32_t object, const uint32_t *arguments, uint32_t edx)
{
    cleanup_bytes = argument_count[id] * 4;
    return operation(id, object, arguments, edx);
}
static __declspec(naked) void native_stub(void)
{
    __asm
    {
        pushad
        mov ebp, esp
        push dword ptr [ebp + 20]
        lea eax, [ebp + 40]
        push eax
        push dword ptr [ebp + 24]
        push dword ptr [ebp + 32]
        call native_operation
        add esp, 16
        mov dword ptr [ebp + 28], eax
        mov esp, ebp
        popad
        add esp, 4
        pop edx
        add esp, cleanup_bytes
        jmp edx
    }
}
#define LIFTED(name,id) static void name(void) { g_eax = operation(id, g_ecx, (const uint32_t *)(uintptr_t)(g_esp + 4), g_edx); \
    g_esp += 4 + argument_count[id] * 4; }
LIFTED(l_empty,STOP_EMPTY) LIFTED(l_target,STOP_TARGET) LIFTED(l_cancel,CANCEL) LIFTED(l_sound,SOUND)
LIFTED(l_moving,MOVING) LIFTED(l_accept,ACCEPT_OBJECT) LIFTED(l_linked,LINKED) LIFTED(l_notify,NOTIFY_OWNER)
static recomp_func_t lifted[OP_COUNT] = { l_empty,l_target,l_cancel,l_sound,l_moving,l_accept,l_linked,l_notify };
recomp_func_t recomp_lookup_manual(uint32_t address)
{
    if (address >= stub_base && address < stub_base + OP_COUNT * 16) return lifted[(address - stub_base) / 16];
    if (address == 0x4CD9B0) return l_cancel;
    if (address == 0x713DB0) return l_sound;
    return address == 0x6BAA30 ? l_linked : NULL;
}
recomp_func_t recomp_lookup(uint32_t address) { (void)address; return NULL; }
recomp_func_t recomp_lookup_import(uint32_t address) { (void)address; return NULL; }
static void patch_jump(uint32_t address, uint32_t destination)
{
    MEM8(address) = 0xE9; MEM32(address + 1) = destination - address - 5;
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
        mov dword ptr [esp + 5Ch], eax
        lea ebp, drive
        jmp entry_address
    returned:
        mov native_esp, esp
        pushfd
        pop native_flags
        mov native_eax, eax
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
    memset(drive, 0, sizeof(drive)); memset(owner, 0, sizeof(owner)); memset(rules, 0, sizeof(rules));
    memset(private_stack, 0xA5, sizeof(private_stack)); memset(operations, 0, sizeof(operations)); operation_count = 0;
    FIELD32(drive, 4) = POINTER(locomotion_vtable); FIELD32(drive, 0xC) = POINTER(owner);
    FIELD32(owner, 0) = POINTER(owner_vtable);
    const int32_t position[3] = { 1234,4567,416 };
    memcpy(drive + 0x40, (fixture & 16) ? (void *)0x852998 : position, 12);
    FIELD32(drive, 0x58) = 4; drive[0x61] = 0x81; drive[0x63] = (uint8_t)((fixture >> 5) & 1);
    const int32_t failures[] = { -1,0,1,2,10,INT_MIN,INT_MAX };
    FIELD32(owner, 0x53C) = (uint32_t)failures[number % 7];
    owner[0x578] = (fixture & 64) ? 3 : 0; owner[0x57A] = (fixture & 128) ? 2 : 0;
    owner[0x7D] = (uint8_t)((fixture >> 10) & 1);
    FIELD32(owner, 0x488) = (fixture & 8) ? POINTER(linked) : 0;
    FIELD32(owner, 0x228) = (fixture & (1u << 11)) ? POINTER(linked) : 0;
    FIELD32(owner, 0x4C4) = (fixture & (1u << 15)) ? POINTER(linked) : 0;
    FIELD32(rules, 0x620) = 123; MEM32(0x839848) = POINTER(rules);
    frame_stack = POINTER(private_stack + 2048);
    MEM32(frame_stack) = 0x12345678; MEM32(frame_stack + 4) = 0x23456789;
    MEM32(frame_stack + 8) = 0x3456789A; MEM32(frame_stack + 12) = 0x456789AB;
    MEM32(frame_stack + 0x14) = POINTER(drive + 4);
}
int main(int argc, char **argv)
{
    if (argc != 2) return 2;
    hold_image(); map_original_image(argv[1]);
    unsigned char *stubs = VirtualAlloc(NULL, 4096, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);
    if (!stubs) return 2;
    stub_base = POINTER(stubs);
    for (unsigned id = 0; id < OP_COUNT; ++id)
    {
        unsigned char *stub = stubs + id * 16;
        stub[0] = 0x68; memcpy(stub + 1, &id, 4); stub[5] = 0xE9;
        uint32_t relative = POINTER(native_stub) - POINTER(stub + 10); memcpy(stub + 6, &relative, 4);
    }
    patch_jump(0x4CD9B0, stub_base + CANCEL * 16);
    patch_jump(0x713DB0, stub_base + SOUND * 16);
    patch_jump(0x6BAA30, stub_base + LINKED * 16);
    owner_vtable[0x410 / 4] = stub_base + STOP_EMPTY * 16;
    owner_vtable[0x414 / 4] = stub_base + STOP_TARGET * 16;
    owner_vtable[0x354 / 4] = stub_base + ACCEPT_OBJECT * 16;
    owner_vtable[0x370 / 4] = stub_base + NOTIFY_OWNER * 16;
    locomotion_vtable[0x10 / 4] = stub_base + MOVING * 16;
    FlushInstructionCache(GetCurrentProcess(), NULL, 0);
    for (finish_only = 0; finish_only < 2; ++finish_only)
    {
        entry_address = finish_only ? 0x4A2EAC : 0x4A2DFD;
        for (unsigned number = 0; number < 65536; ++number)
        {
            initialize(number); execute_original();
            unsigned char expected_drive[sizeof(drive)], expected_owner[sizeof(owner)];
            uint32_t expected_ops[32][12], expected_count = operation_count;
            memcpy(expected_drive, drive, sizeof(drive)); memcpy(expected_owner, owner, sizeof(owner));
            memcpy(expected_ops, operations, sizeof(expected_ops));
            initialize(number);
            g_esp = frame_stack; g_ebp = POINTER(drive);
            ra2_ground_recover_path_bridge((int)finish_only);
            uint32_t flags = recomp_eflags(g_flag_k, g_flag_a, g_flag_b, g_flag_cf, 1);
            int state_diff = memcmp(expected_drive, drive, sizeof(drive)) || memcmp(expected_owner, owner, sizeof(owner));
            if (state_diff || expected_count != operation_count || memcmp(expected_ops, operations, sizeof(expected_ops))
                || (g_eax & 255u) != (native_eax & 255u) || g_esp != native_esp
                || g_ebx != native_ebx || g_esi != native_esi || g_edi != native_edi || g_ebp != native_ebp
                || (flags & 0x8D5) != (native_flags & 0x8D5))
            {
                printf("recovery mismatch finish=%u case=%u fixture=%x state=%d calls=%u/%u\n",
                    finish_only, number, fixture, state_diff, operation_count, expected_count);
                for (unsigned i = 0; i < operation_count || i < expected_count; ++i)
                    printf("  operation=%u/%u arg=%x,%x,%x,%x/%x,%x,%x,%x flags=%u,%u,%u/%u,%u,%u\n",
                        operations[i][0], expected_ops[i][0], operations[i][1], operations[i][2], operations[i][3], operations[i][4],
                        expected_ops[i][1], expected_ops[i][2], expected_ops[i][3], expected_ops[i][4],
                        operations[i][9], operations[i][10], operations[i][11], expected_ops[i][9], expected_ops[i][10], expected_ops[i][11]);
                return 1;
            }
        }
    }
    puts("{\"passed\":true,\"failure_budget_cases\":65536,\"shared_finish_cases\":65536,\"state_calls_abi_verified\":true}");
    return 0;
}
