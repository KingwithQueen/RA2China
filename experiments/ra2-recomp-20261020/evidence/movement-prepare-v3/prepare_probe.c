#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>
#include "recomp_types.h"
#include "ground_prepare_bridge.h"
#include "native_probe_host.h"

uint32_t g_eax, g_ecx, g_edx, g_esp, g_ebx, g_esi, g_edi, g_ebp, g_cur_func;
uint16_t g_fpu_cw;
enum Operation { MISSION, TEST_1BC, TEST_1C0, TEAM, TEST_324, TEST_328, TARGET_KIND, POSITION, VECTOR,
    LENGTH, STOP_EMPTY, STOP_TARGET, REBUILD, ACCEPT, PREDICATE, CANCEL, OP_COUNT };
static const unsigned argument_count[OP_COUNT] = { 0,0,0,0,0,0,0,1,3,0,2,2,3,1,0,0 };
static unsigned char drive[128], owner[0x700], target[0x100], rules[0x1500], private_stack[8192], aborted;
static uint32_t owner_vtable[0x500 / 4], target_vtable[0x100 / 4], fixture, fixture_number, stub_base;
static uint32_t operations[64][7], operation_count, cleanup_bytes;
static uint32_t frame_stack, host_stack, native_eax, native_esp, native_flags, entry_address;
static uint32_t native_ebx, native_esi, native_edi, native_ebp, native_resume, native_head;
static uint16_t initial_control, native_control;
static unsigned phase;
#define POINTER(value) ((uint32_t)(uintptr_t)(value))
#define FIELD32(buffer,offset) (*(uint32_t *)((buffer) + (offset)))

static uint32_t operation(unsigned id, uint32_t object, const uint32_t *arguments)
{
    if (operation_count == 64) exit(2);
    uint32_t *record = operations[operation_count++];
    record[0] = id;
    record[4] = FIELD32(drive, 0x40); record[5] = drive[0x61]; record[6] = drive[0x63];
    if (id == STOP_EMPTY || id == STOP_TARGET || id == REBUILD) memcpy(record + 1, arguments, argument_count[id] * 4);
    switch (id)
    {
        case MISSION:
        {
            const uint32_t missions[] = { 2,11,5,7 };
            return missions[(fixture >> 16) & 3];
        }
        case TEST_1BC: return (fixture >> 1) & 1;
        case TEST_1C0: return (fixture >> 2) & 1;
        case TEAM: return (fixture >> 3) & 1;
        case TEST_324: return (fixture >> 4) & 1;
        case TEST_328: return (fixture >> 5) & 1;
        case TARGET_KIND:
        {
            const uint32_t kinds[] = { 1,15,6,11 };
            return kinds[(fixture >> 6) & 3];
        }
        case POSITION:
            memcpy((void *)(uintptr_t)arguments[0], owner + 0x88, 12);
            return arguments[0];
        case VECTOR:
            memcpy((void *)(uintptr_t)object, arguments, 12);
            memcpy(record + 1, arguments, 12);
            return object;
        case LENGTH:
        {
            const int32_t distances[] = { -256,-1,0,1,255,256,511,512,6143,6144,6145,10000 };
            memcpy(record + 1, (void *)(uintptr_t)object, 12);
            return (uint32_t)distances[(fixture_number / 4) % 12];
        }
        case STOP_EMPTY:
        case STOP_TARGET:
            if (fixture & (1u << 8)) owner[0x7D] = 0;
            if (fixture & (1u << 9)) memcpy(drive + 0x40, (void *)0x852998, 12);
            return (fixture & (1u << 10)) ? 1 : 0;
        case REBUILD:
            if (fixture & (1u << 11)) FIELD32(drive, 0xC) = 0;
            if (fixture & (1u << 12)) memcpy(drive + 0x34, (void *)0x852998, 12);
            FIELD32(owner, 0x4D0) = (fixture & (1u << 13)) ? 3 : UINT32_MAX;
            return (fixture >> 14) & 1;
        case ACCEPT: return (fixture >> 15) & 1;
        case PREDICATE: return (fixture >> 18) & 1;
        case CANCEL: FIELD32(owner, 0x488) = 0; return 0;
        default: exit(2);
    }
}

static uint32_t native_operation(unsigned id, uint32_t object, const uint32_t *arguments)
{
    cleanup_bytes = argument_count[id] * 4;
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
    g_esp += 4 + argument_count[id] * 4; }
LIFTED(l_mission,MISSION) LIFTED(l_1bc,TEST_1BC) LIFTED(l_1c0,TEST_1C0) LIFTED(l_team,TEAM)
LIFTED(l_324,TEST_324) LIFTED(l_328,TEST_328) LIFTED(l_kind,TARGET_KIND) LIFTED(l_position,POSITION)
LIFTED(l_vector,VECTOR) LIFTED(l_length,LENGTH) LIFTED(l_empty,STOP_EMPTY) LIFTED(l_target,STOP_TARGET)
LIFTED(l_rebuild,REBUILD) LIFTED(l_accept,ACCEPT) LIFTED(l_predicate,PREDICATE) LIFTED(l_cancel,CANCEL)
static recomp_func_t lifted[OP_COUNT] = { l_mission,l_1bc,l_1c0,l_team,l_324,l_328,l_kind,l_position,
    l_vector,l_length,l_empty,l_target,l_rebuild,l_accept,l_predicate,l_cancel };
recomp_func_t recomp_lookup_manual(uint32_t address)
{
    if (address >= stub_base && address < stub_base + OP_COUNT * 16) return lifted[(address - stub_base) / 16];
    switch (address)
    {
        case 0x68A680: return l_team;
        case 0x41B630: return l_vector;
        case 0x41B780: return l_length;
        case 0x4C3000: return l_rebuild;
        case 0x4C8D60: return l_predicate;
        case 0x4CD9B0: return l_cancel;
        default: return NULL;
    }
}
recomp_func_t recomp_lookup(uint32_t address) { (void)address; return NULL; }
recomp_func_t recomp_lookup_import(uint32_t address) { (void)address; return NULL; }
void ra2_state_math(uint32_t stack, uint32_t ebp, uint32_t output, uint32_t source)
{
    (void)stack; (void)ebp; (void)output; (void)source;
}
static void patch_jump(uint32_t address, uint32_t destination)
{
    MEM8(address) = 0xE9; MEM32(address + 1) = destination - address - 5;
}
static __declspec(naked) void continue_trap(void)
{
    __asm
    {
        mov native_head, ebx
        mov eax, 0
        mov edi, dword ptr [esp]
        mov esi, dword ptr [esp + 4]
        mov ebp, dword ptr [esp + 8]
        mov ebx, dword ptr [esp + 12]
        add esp, 5Ch
        ret 0Ch
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
        fninit
        fldcw initial_control
        mov esp, frame_stack
        lea eax, returned
        mov dword ptr [esp + 5Ch], eax
        lea ebp, drive
        lea edi, drive + 34h
        lea eax, owner
        mov ebx, dword ptr [eax + 4D0h]
        mov eax, fixture
        and eax, 1
        jmp entry_address
    returned:
        mov native_esp, esp
        pushfd
        pop native_flags
        fnstcw native_control
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
    fixture = number * 1664525u + 1013904223u;
    fixture ^= fixture << 13; fixture ^= fixture >> 17; fixture ^= fixture << 5;
    memset(drive, 0, sizeof(drive)); memset(owner, 0, sizeof(owner)); memset(target, 0, sizeof(target));
    memset(rules, 0, sizeof(rules)); memset(private_stack, 0xA5, sizeof(private_stack));
    memset(operations, 0, sizeof(operations)); operation_count = native_resume = 0;
    FIELD32(drive, 0xC) = POINTER(owner);
    FIELD32(owner, 0) = POINTER(owner_vtable); FIELD32(target, 0) = POINTER(target_vtable);
    const int32_t position[3] = { 1280,-256,416 }, destination[3] = { 4352,-257,320 };
    memcpy(owner + 0x88, position, 12); memcpy(drive + 0x34, destination, 12);
    if (phase == 0 && (fixture & (1u << 20))) memcpy(drive + 0x34, (void *)0x852998, 12);
    memcpy(drive + 0x40, (fixture & (1u << 21)) ? (void *)0x852998 : position, 12);
    drive[0x61] = 1; drive[0x63] = (uint8_t)((fixture >> 22) & 1); owner[0x7D] = 1;
    FIELD32(owner, 0x238) = (fixture & (1u << 23)) ? POINTER(target) : 0;
    FIELD32(owner, 0x488) = (fixture & (1u << 24)) ? POINTER(target) : 0;
    FIELD32(owner, 0x494) = (fixture & (1u << 25)) ? POINTER(target) : 0;
    const uint32_t heads[] = { UINT32_MAX,0,3,8 };
    FIELD32(owner, 0x4D0) = heads[(fixture >> 26) & 3];
    MEM32(0xA40D2C) = (number & 128) ? 0x80000010 : 2300;
    const uint32_t starts[] = { UINT32_MAX,2299,2300,2310,0x7FFFFFFF,0x80000000 };
    const uint32_t times[] = { 0,1,2,10,UINT32_MAX,0x7FFFFFFF,0x80000000 };
    FIELD32(owner, 0x530) = starts[number % 6];
    FIELD32(owner, 0x538) = times[(number / 6) % 7];
    const double delays[] = { 0.0,0.1,0.9,1.0,1.1,0.0011111111111111111,0.00001,1000.0,0.01 };
    memcpy(rules + 0x13C8, &delays[(number / 42) % (sizeof(delays) / sizeof(delays[0]))], 8);
    FIELD32(rules, 0x1380) = 512;
    MEM32(0x839848) = POINTER(rules); MEM32(0x7D8964) = 0xE7F;
    static const unsigned precisions[] = { 0,2,3 };
    initial_control = (uint16_t)(0x7F | (precisions[number % 3] << 8) | (((number / 3) % 4) << 10));
    frame_stack = POINTER(private_stack + 4096);
    MEM32(frame_stack) = 0x12345678; MEM32(frame_stack + 4) = 0x23456789;
    MEM32(frame_stack + 8) = 0x3456789A; MEM32(frame_stack + 12) = 0x456789AB;
    MEM32(frame_stack + 0x14) = POINTER(drive + 4); MEM32(frame_stack + 0x60) = POINTER(&aborted);
    aborted = 0xA5;
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
    uint32_t addresses[] = { 0x68A680,0x41B630,0x41B780,0x4C3000,0x4C8D60,0x4CD9B0 };
    unsigned ids[] = { TEAM,VECTOR,LENGTH,REBUILD,PREDICATE,CANCEL };
    for (unsigned i = 0; i < 6; ++i) patch_jump(addresses[i], stub_base + ids[i] * 16);
    owner_vtable[0x16C / 4] = stub_base + MISSION * 16;
    owner_vtable[0x1BC / 4] = stub_base + TEST_1BC * 16;
    owner_vtable[0x1C0 / 4] = stub_base + TEST_1C0 * 16;
    owner_vtable[0x324 / 4] = stub_base + TEST_324 * 16;
    owner_vtable[0x328 / 4] = stub_base + TEST_328 * 16;
    owner_vtable[0x48 / 4] = stub_base + POSITION * 16;
    owner_vtable[0x410 / 4] = stub_base + STOP_EMPTY * 16;
    owner_vtable[0x414 / 4] = stub_base + STOP_TARGET * 16;
    owner_vtable[0x2AC / 4] = stub_base + ACCEPT * 16;
    target_vtable[0x2C / 4] = stub_base + TARGET_KIND * 16;
    uint32_t boundaries[] = { 0x4A285E,0x4A32CA,0x4A2A83,0x4A2F7A,0x4A2EAC };
    unsigned char saved_retry[5]; memcpy(saved_retry, (void *)0x4A285E, 5);
    unsigned outcome_counts[2][6] = { 0 };
    for (phase = 0; phase < 2; ++phase)
    {
        for (unsigned b = 0; b < 5; ++b)
        {
            if (phase == 1 && b == 0) { memcpy((void *)0x4A285E, saved_retry, 5); continue; }
            unsigned char *stub = stubs + (OP_COUNT + b) * 16;
            stub[0] = 0xC7; stub[1] = 5;
            uint32_t destination = POINTER(&native_resume); memcpy(stub + 2, &destination, 4);
            memcpy(stub + 6, &boundaries[b], 4); stub[10] = 0xE9;
            uint32_t relative = POINTER(continue_trap) - POINTER(stub + 15); memcpy(stub + 11, &relative, 4);
            patch_jump(boundaries[b], POINTER(stub));
        }
        FlushInstructionCache(GetCurrentProcess(), NULL, 0);
        for (unsigned number = 0; number < 65536; ++number)
        {
            entry_address = phase == 0 ? 0x4A2690 : 0x4A285E;
            initialize(number); execute_original();
            unsigned char expected_drive[sizeof(drive)], expected_owner[sizeof(owner)], expected_abort = aborted;
            uint32_t expected_ops[64][7], expected_count = operation_count, expected_resume = native_resume;
            memcpy(expected_drive, drive, sizeof(drive)); memcpy(expected_owner, owner, sizeof(owner));
            memcpy(expected_ops, operations, sizeof(expected_ops));
            initialize(number);
            g_esp = frame_stack; g_ebp = POINTER(drive); g_edi = POINTER(drive + 0x34);
            g_ebx = FIELD32(owner, 0x4D0); g_eax = fixture & 1; g_fpu_cw = initial_control;
            uint32_t resume = phase == 0 ? ra2_ground_prepare_entry_bridge() : ra2_ground_retry_path_bridge();
            uint32_t flags = recomp_eflags(g_flag_k, g_flag_a, g_flag_b, g_flag_cf, 1);
            int state_diff = memcmp(expected_drive, drive, sizeof(drive)) || memcmp(expected_owner, owner, sizeof(owner));
            int abi_diff = resume ? (g_esp != frame_stack || g_ebp != POINTER(drive)
                || (resume == 0x4A32CA && g_ebx != native_head))
                : ((g_eax & 255u) != (native_eax & 255u) || g_esp != native_esp
                    || g_ebx != native_ebx || g_esi != native_esi || g_edi != native_edi || g_ebp != native_ebp
                    || (flags & 0x8D5) != (native_flags & 0x8D5));
            if (state_diff || abi_diff || resume != expected_resume || aborted != expected_abort || g_fpu_cw != native_control
                || expected_count != operation_count || memcmp(expected_ops, operations, sizeof(expected_ops)))
            {
                printf("prepare mismatch phase=%u case=%u fixture=%08x state=%d abi=%d resume=%x/%x calls=%u/%u cw=%x/%x\n",
                    phase, number, fixture, state_diff, abi_diff, resume, expected_resume, operation_count, expected_count,
                    g_fpu_cw, native_control);
                for (unsigned i = 0; i < operation_count || i < expected_count; ++i)
                    printf("  operation=%u/%u v=%x,%x,%x/%x,%x,%x\n", operations[i][0], expected_ops[i][0],
                        operations[i][1], operations[i][2], operations[i][3], expected_ops[i][1], expected_ops[i][2], expected_ops[i][3]);
                return 1;
            }
            unsigned outcome = 0;
            for (unsigned i = 0; i < 5; ++i) if (resume == boundaries[i]) outcome = i + 1;
            ++outcome_counts[phase][outcome];
        }
    }
    printf("{\"passed\":true,\"entry_cases\":65536,\"retry_cases\":65536,\"state_calls_abi_cw_verified\":true,"
        "\"entry_outcomes\":[%u,%u,%u],\"retry_outcomes\":[%u,%u,%u,%u]}\n",
        outcome_counts[0][0], outcome_counts[0][1], outcome_counts[0][2], outcome_counts[1][0], outcome_counts[1][3],
        outcome_counts[1][4], outcome_counts[1][5]);
    return 0;
}
