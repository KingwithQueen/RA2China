#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "recomp_types.h"
#include "ground_drive_bridge.h"
#include "native_probe_host.h"

uint32_t g_eax, g_ecx, g_edx, g_esp, g_ebx, g_esi, g_edi, g_ebp, g_cur_func;

enum Operation
{
    CELL, OWNER_KIND, TARGET_KIND, CELL_COORD, TARGET_COORD, MOVING, REALLY_MOVING, TURNING, ADVANCE, PREPARE,
    MOVE_TO, MARK, STOP_EMPTY, STOP_TARGET, CANCEL_TARGET, ACCEPT_DESTINATION, MISSION, SPEED_ZERO, ALLOCATE, ANIMATION, OP_COUNT
};
static const unsigned argument_count[OP_COUNT] = { 0,0,0,1,2,1,1,0,1,3,4,1,2,2,0,1,0,2,1,6 };
static unsigned char drive[128], owner[0x700], cell[0x200], target[0x300], rules[0x800], private_stack[4096];
static uint32_t owner_vtable[0x500 / 4], target_vtable[0x100 / 4], locomotion_vtable[0x100 / 4];
static uint32_t operation_trace[128][5], trace_count, cleanup_bytes, step_count;
static uint32_t fixture_bits, fixture_number, stub_base;
static uint32_t host_stack, input_stack, native_eax, native_esp, native_flags, native_ebx, native_esi, native_edi, native_ebp;

#define POINTER(value) ((uint32_t)(uintptr_t)(value))
#define FIELD32(buffer,offset) (*(uint32_t *)((buffer) + (offset)))

static uint32_t operation(unsigned id, uint32_t object, const uint32_t *arguments)
{
    (void)object;
    if (trace_count >= 128) { puts("operation trace overflow"); exit(2); }
    uint32_t *record = operation_trace[trace_count++];
    record[0] = id;
    if (id == ADVANCE || id == MARK || id == ALLOCATE) record[1] = arguments[0];
    if (id == MOVE_TO) memcpy(record + 1, arguments + 1, 12);
    switch (id)
    {
        case CELL: return POINTER(cell);
        case OWNER_KIND: return (fixture_bits & 1) ? 1 : 2;
        case TARGET_KIND: return (fixture_number % 4 == 0) ? 11 : ((fixture_number % 4 == 1) ? 15 : 6);
        case CELL_COORD:
            MEM32(arguments[0]) = 13u << 16 | 12u;
            return arguments[0];
        case TARGET_COORD:
            memcpy((void *)(uintptr_t)arguments[0], target + 0x88, 12);
            return arguments[0];
        case MOVING: return (fixture_bits >> 1) & 1;
        case REALLY_MOVING: return (fixture_bits >> 2) & 1;
        case TURNING: return (fixture_bits >> 3) & 1;
        case ADVANCE:
            ++step_count;
            if (fixture_bits & (1u << 4)) owner[0x7D] = 0;
            if (fixture_bits & (1u << 5))
            {
                FIELD32(drive, 0x58) = UINT32_MAX;
                drive[0x63] = 0;
            }
            return (fixture_bits >> 6) & 1;
        case PREPARE:
            MEM8(arguments[0]) = (uint8_t)((fixture_bits >> 7) & 1);
            if (fixture_bits & (1u << 8)) owner[0x7D] = 0;
            if (fixture_bits & (1u << 9))
            {
                FIELD32(drive, 0x58) = 4;
                drive[0x63] = 1;
            }
            return 0;
        case MOVE_TO:
            memcpy(drive + 0x34, arguments + 1, 12);
            return 0;
        case MARK:
            if (fixture_bits & (1u << 10)) owner[0x7A] = 1;
            return 1;
        case STOP_EMPTY:
        case STOP_TARGET:
            FIELD32(drive, 0x58) = UINT32_MAX;
            drive[0x63] = 0;
            return (fixture_bits >> 11) & 1;
        case CANCEL_TARGET: return 0;
        case ACCEPT_DESTINATION: return (fixture_bits >> 12) & 1;
        case MISSION: return FIELD32(owner, 0x98) == UINT32_MAX ? FIELD32(owner, 0xA0) : FIELD32(owner, 0x98);
        case SPEED_ZERO: FIELD32(owner, 0x468) = 0; FIELD32(owner, 0x46C) = 0; return 0;
        case ALLOCATE: return 0;
        case ANIMATION: return 0;
        default: exit(2);
    }
}

static uint32_t native_operation(unsigned id, uint32_t object, const uint32_t *arguments)
{
    cleanup_bytes = id == ALLOCATE ? 0 : argument_count[id] * 4;
    return operation(id, object, arguments);
}

static __declspec(naked) void native_stub(void)
{
    __asm
    {
        pushad
        mov ebp, esp
        lea eax, [ebp + 40]
        push eax
        push dword ptr [ebp + 24]
        push dword ptr [ebp + 32]
        call native_operation
        add esp, 12
        mov dword ptr [ebp + 28], eax
        mov esp, ebp
        popad
        add esp, 4
        pop edx
        add esp, cleanup_bytes
        jmp edx
    }
}

#define LIFTED(name,id) static void name(void) { g_eax = operation(id, g_ecx, (const uint32_t *)(uintptr_t)(g_esp + 4)); \
    g_esp += 4 + (id == ALLOCATE ? 0 : argument_count[id] * 4); }
LIFTED(l_cell,CELL) LIFTED(l_owner,OWNER_KIND) LIFTED(l_target,TARGET_KIND) LIFTED(l_cell_coord,CELL_COORD)
LIFTED(l_target_coord,TARGET_COORD) LIFTED(l_moving,MOVING) LIFTED(l_really_moving,REALLY_MOVING) LIFTED(l_turning,TURNING)
LIFTED(l_advance,ADVANCE) LIFTED(l_prepare,PREPARE) LIFTED(l_move,MOVE_TO) LIFTED(l_mark,MARK)
LIFTED(l_stop_empty,STOP_EMPTY) LIFTED(l_stop_target,STOP_TARGET) LIFTED(l_cancel,CANCEL_TARGET)
LIFTED(l_accept,ACCEPT_DESTINATION) LIFTED(l_mission,MISSION) LIFTED(l_zero,SPEED_ZERO)
LIFTED(l_allocate,ALLOCATE) LIFTED(l_animation,ANIMATION)
static recomp_func_t lifted[OP_COUNT] = { l_cell,l_owner,l_target,l_cell_coord,l_target_coord,l_moving,l_really_moving,l_turning,
    l_advance,l_prepare,l_move,l_mark,l_stop_empty,l_stop_target,l_cancel,l_accept,l_mission,l_zero,l_allocate,l_animation };

recomp_func_t recomp_lookup_manual(uint32_t address)
{
    if (address >= stub_base && address < stub_base + OP_COUNT * 16) return lifted[(address - stub_base) / 16];
    switch (address)
    {
        case 0x4A1000: return l_advance;
        case 0x4A2670: return l_prepare;
        case 0x4B8C90: return l_turning;
        case 0x4CD9B0: return l_cancel;
        case 0x782017: return l_allocate;
        case 0x420110: return l_animation;
        default: return NULL;
    }
}
recomp_func_t recomp_lookup(uint32_t address) { (void)address; return NULL; }
recomp_func_t recomp_lookup_import(uint32_t address) { (void)address; return NULL; }

static void patch_jump(uint32_t address, uint32_t destination)
{
    MEM8(address) = 0xE9;
    MEM32(address + 1) = destination - address - 5;
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
        mov esp, input_stack
        add esp, 4
        mov ebx, 12345678h
        mov esi, 23456789h
        mov edi, 3456789Ah
        mov ebp, 456789ABh
        mov eax, 004A05F0h
        call eax
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
    fixture_number = number;
    fixture_bits = number * 1664525u + 1013904223u;
    fixture_bits ^= fixture_bits << 13;
    fixture_bits ^= fixture_bits >> 17;
    fixture_bits ^= fixture_bits << 5;
    memset(drive, 0, sizeof(drive)); memset(owner, 0, sizeof(owner)); memset(cell, 0, sizeof(cell));
    memset(target, 0, sizeof(target)); memset(rules, 0, sizeof(rules)); memset(operation_trace, 0, sizeof(operation_trace));
    memset(private_stack, 0xA5, sizeof(private_stack));
    trace_count = step_count = 0;
    FIELD32(drive, 4) = POINTER(locomotion_vtable);
    FIELD32(drive, 0xC) = POINTER(owner);
    FIELD32(owner, 0) = POINTER(owner_vtable);
    FIELD32(target, 0) = POINTER(target_vtable);
    const int32_t position[3] = { 1280, 2560, 416 };
    const int32_t other_position[3] = { 1536, 2816, 416 };
    memcpy(owner + 0x88, position, 12);
    memcpy(drive + 0x34, (fixture_bits & (1u << 14)) ? position : other_position, 12);
    if (fixture_bits & (1u << 13)) memcpy(drive + 0x34, (void *)0x852998, 12);
    memcpy(drive + 0x40, (fixture_bits & (1u << 15)) ? (void *)0x852998 : position, 12);
    FIELD32(drive, 0x58) = (fixture_bits & (1u << 16)) ? 4 : UINT32_MAX;
    drive[0x63] = (uint8_t)((fixture_bits >> 17) & 1);
    drive[0x62] = (uint8_t)((fixture_bits >> 18) & 1);
    FIELD32(drive, 0x1C) = number % 3;
    cell[0x11C] = (uint8_t)((fixture_bits >> 19) & 1);
    owner[0x7D] = 1;
    owner[0x76] = (uint8_t)((fixture_bits >> 26) & 1);
    owner[0x79] = (uint8_t)((fixture_bits >> 27) & 1);
    owner[0x5B9] = (uint8_t)((fixture_bits >> 23) & 1);
    owner[0x325] = (uint8_t)((fixture_bits >> 24) & 1);
    owner[0x32D] = (uint8_t)((fixture_bits >> 25) & 1);
    FIELD32(owner, 0x488) = (fixture_bits & (1u << 20)) ? 1 : 0;
    FIELD32(owner, 0x494) = number % 4 == 3 ? 0 : POINTER(target);
    FIELD32(owner, 0x4D0) = (fixture_bits & (1u << 30)) ? 0 : UINT32_MAX;
    FIELD32(target, 0x24) = (13u << 16) | (12u + ((fixture_bits >> 22) & 1));
    memcpy(target + 0x88, (fixture_bits & (1u << 21)) ? (const void *)(drive + 0x34) : (const void *)other_position, 12);
    const uint32_t missions[] = { 5, 2, 7, 16, 13, UINT32_MAX };
    FIELD32(owner, 0x98) = missions[(number / 4) % 6];
    FIELD32(owner, 0xA0) = 5;
    double speed = 0.75;
    memcpy(owner + 0x468, &speed, 8); memcpy(drive + 0x50, &speed, 8);
    FIELD32(cell, 0xEC) = (fixture_bits & (1u << 29)) ? 2 : 0;
    FIELD32(rules, 0x9C) = (fixture_bits & (1u << 28)) ? 42 : 0;
    MEM32(0x839848) = POINTER(rules);
    MEM32(0xA40D2C) = 2190 + number % 11;
    input_stack = POINTER(private_stack + 2048);
    MEM32(input_stack + 4) = POINTER(drive + 4);
}

int main(int argc, char **argv)
{
    if (argc != 2) return 2;
    hold_image();
    map_original_image(argv[1]);
    unsigned char *stubs = VirtualAlloc(NULL, 4096, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);
    if (!stubs) return 2;
    stub_base = POINTER(stubs);
    for (unsigned id = 0; id < OP_COUNT; ++id)
    {
        unsigned char *stub = stubs + id * 16;
        stub[0] = 0x68;
        memcpy(stub + 1, &id, 4);
        stub[5] = 0xE9;
        uint32_t relative = POINTER(native_stub) - POINTER(stub + 10);
        memcpy(stub + 6, &relative, 4);
    }
    patch_jump(0x4A1000, stub_base + ADVANCE * 16);
    patch_jump(0x4A2670, stub_base + PREPARE * 16);
    patch_jump(0x4B8C90, stub_base + TURNING * 16);
    patch_jump(0x4CD9B0, stub_base + CANCEL_TARGET * 16);
    patch_jump(0x782017, stub_base + ALLOCATE * 16);
    patch_jump(0x420110, stub_base + ANIMATION * 16);
    owner_vtable[0x1A4 / 4] = stub_base + CELL * 16;
    owner_vtable[0x2C / 4] = stub_base + OWNER_KIND * 16;
    owner_vtable[0x1A0 / 4] = stub_base + CELL_COORD * 16;
    owner_vtable[0x16C / 4] = stub_base + MISSION * 16;
    owner_vtable[0x174 / 4] = stub_base + MARK * 16;
    owner_vtable[0x410 / 4] = stub_base + STOP_EMPTY * 16;
    owner_vtable[0x414 / 4] = stub_base + STOP_TARGET * 16;
    owner_vtable[0x2AC / 4] = stub_base + ACCEPT_DESTINATION * 16;
    owner_vtable[0x4C8 / 4] = stub_base + SPEED_ZERO * 16;
    target_vtable[0x2C / 4] = stub_base + TARGET_KIND * 16;
    target_vtable[0x4C / 4] = stub_base + TARGET_COORD * 16;
    locomotion_vtable[0x10 / 4] = stub_base + MOVING * 16;
    locomotion_vtable[0x80 / 4] = stub_base + REALLY_MOVING * 16;
    locomotion_vtable[0x44 / 4] = stub_base + MOVE_TO * 16;
    FlushInstructionCache(GetCurrentProcess(), NULL, 0);
    unsigned checked = 0;
    for (unsigned number = 0; number < 32768; ++number)
    {
        initialize(number);
        execute_original();
        unsigned char expected_drive[sizeof(drive)], expected_owner[sizeof(owner)];
        uint32_t expected_trace[128][5], expected_count = trace_count;
        memcpy(expected_drive, drive, sizeof(drive)); memcpy(expected_owner, owner, sizeof(owner));
        memcpy(expected_trace, operation_trace, sizeof(expected_trace));
        initialize(number);
        g_esp = input_stack; g_ebx = 0x12345678; g_esi = 0x23456789; g_edi = 0x3456789A; g_ebp = 0x456789AB;
        ra2_ground_drive_process_bridge();
        uint32_t flags = recomp_eflags(g_flag_k, g_flag_a, g_flag_b, g_flag_cf, 1);
        /* 原版计时器 +0x28 来自未初始化的填充；只比较已核实的有效字段。 */
        memcpy(expected_drive + 0x28, drive + 0x28, 4);
        int difference = memcmp(expected_drive, drive, sizeof(drive)) || memcmp(expected_owner, owner, sizeof(owner));
        if (difference || expected_count != trace_count || memcmp(expected_trace, operation_trace, sizeof(expected_trace))
            || (g_eax & 255u) != (native_eax & 255u) || g_esp != native_esp || (flags & 0x8D5) != (native_flags & 0x8D5)
            || g_ebx != native_ebx || g_esi != native_esi || g_edi != native_edi || g_ebp != native_ebp)
        {
            printf("process mismatch case=%u bits=%08x state=%d calls=%u/%u result=%u/%u\n", number, fixture_bits,
                difference, trace_count, expected_count, g_eax & 255u, native_eax & 255u);
            for (unsigned i = 0; i < trace_count || i < expected_count; ++i)
                printf("  operation[%u]=%u/%u arg=%u/%u\n", i, operation_trace[i][0], expected_trace[i][0],
                    operation_trace[i][1], expected_trace[i][1]);
            for (unsigned i = 0; i < sizeof(drive); ++i)
                if (expected_drive[i] != drive[i]) printf("  drive+%02x=%u/%u\n", i, drive[i], expected_drive[i]);
            return 1;
        }
        ++checked;
    }
    printf("{\"passed\":true,\"native_process_fixtures\":%u,\"service_call_order_and_state_verified\":true}\n", checked);
    return 0;
}
