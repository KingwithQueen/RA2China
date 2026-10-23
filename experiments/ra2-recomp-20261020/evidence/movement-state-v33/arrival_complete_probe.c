#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>
#include "recomp_types.h"
#include "ground_completion_bridge.h"
uint16_t g_fpu_cw;
static uint16_t get_control(void) { uint16_t value; __asm { fnstcw value } return value; }
static void set_control(uint16_t value) { __asm fldcw value }
#include "native_probe_host.h"

uint32_t g_eax, g_ecx, g_edx, g_esp, g_ebx, g_esi, g_edi, g_ebp, g_cur_func;
enum Operation { OCCUPY, SET_POSITION, UPDATE_POSITION, TARGET_POSITION, CELL_COORD, OWNER_POSITION,
    MARK, CANCEL, MISSION, STOP, UPDATE, OP_COUNT };
static const unsigned argument_count[OP_COUNT] = { 1,1,1,2,1,2,1,0,0,2,0 };
static unsigned char drive[128], owner[0x700], alternate[0x700], target[0x100], private_stack[4096];
static uint32_t owner_vtable[0x500 / 4], target_vtable[0x100 / 4], fixture, fixture_number, stub_base;
static uint32_t operations[64][5], operation_count, cleanup_bytes;
static uint32_t frame_stack, host_stack, native_eax, native_esp, native_flags;
static uint32_t native_ebx, native_esi, native_edi, native_ebp, native_continued;
#define POINTER(value) ((uint32_t)(uintptr_t)(value))
#define FIELD32(buffer,offset) (*(uint32_t *)((buffer) + (offset)))

static uint32_t operation(unsigned id, uint32_t object, const uint32_t *arguments)
{
    unsigned char *unit = (unsigned char *)(uintptr_t)(object == POINTER(target) ? FIELD32(drive, 0xC) : object);
    if ((fixture & (1u << 16)) && (id == OCCUPY || id == TARGET_POSITION || id == MARK || id == CANCEL))
        FIELD32(drive, 0xC) = FIELD32(drive, 0xC) == POINTER(owner) ? POINTER(alternate) : POINTER(owner);
    if (operation_count == 64) exit(2);
    uint32_t *record = operations[operation_count++];
    record[0] = id;
    /* 比较服务接收的有效状态，不能只比较函数编号。 */
    record[2] = unit[0x74];
    record[3] = FIELD32(drive, 0x58);
    record[4] = drive[0x63];
    if (id == OCCUPY || id == UPDATE_POSITION || id == MARK) record[1] = arguments[0];
    switch (id)
    {
        case OCCUPY: return 1;
        case SET_POSITION:
            memcpy(unit + 0x88, (void *)(uintptr_t)arguments[0], 12);
            if (fixture & (1u << 15)) drive[0x63] = 1;
            return 1;
        case UPDATE_POSITION: return 1;
        case TARGET_POSITION:
            memcpy((void *)(uintptr_t)arguments[0], target + 0x88, 12);
            return arguments[0];
        case CELL_COORD:
            MEM16(arguments[0]) = (uint16_t)((int32_t)FIELD32(unit, 0x88) / 256);
            MEM16(arguments[0] + 2) = (uint16_t)((int32_t)FIELD32(unit, 0x8C) / 256);
            return arguments[0];
        case OWNER_POSITION:
            memcpy((void *)(uintptr_t)arguments[0], unit + 0x88, 12);
            return arguments[0];
        case MARK:
            if (fixture & (1u << 3)) unit[0x7D] = 0;
            if (fixture & (1u << 4)) unit[0x76] = 1;
            return 1;
        case CANCEL:
            FIELD32(unit, 0x494) = 0;
            if (fixture & (1u << 14)) FIELD32(drive, 0x58) = 3;
            return 0;
        case MISSION: return (fixture & (1u << 5)) ? 2 : 13;
        case STOP: return (fixture >> 6) & 1;
        case UPDATE:
            if (fixture & (1u << 7)) unit[0x7D] = 0;
            return (fixture >> 8) & 1;
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
LIFTED(l_occupy,OCCUPY) LIFTED(l_set,SET_POSITION) LIFTED(l_update_pos,UPDATE_POSITION)
LIFTED(l_target,TARGET_POSITION) LIFTED(l_cell,CELL_COORD) LIFTED(l_owner,OWNER_POSITION)
LIFTED(l_mark,MARK) LIFTED(l_cancel,CANCEL) LIFTED(l_mission,MISSION) LIFTED(l_stop,STOP) LIFTED(l_update,UPDATE)
static recomp_func_t lifted[OP_COUNT] = { l_occupy,l_set,l_update_pos,l_target,l_cell,l_owner,l_mark,l_cancel,l_mission,l_stop,l_update };
recomp_func_t recomp_lookup_manual(uint32_t address)
{
    if (address >= stub_base && address < stub_base + OP_COUNT * 16) return lifted[(address - stub_base) / 16];
    return address == 0x4CD9B0 ? l_cancel : NULL;
}
recomp_func_t recomp_lookup(uint32_t address) { (void)address; return NULL; }
recomp_func_t recomp_lookup_import(uint32_t address) { (void)address; return NULL; }
static void patch_jump(uint32_t address, uint32_t destination)
{
    MEM8(address) = 0xE9;
    MEM32(address + 1) = destination - address - 5;
}

/* 在继续地址截停，确认原版选择继续还是返回；不让无关的下一采样段影响本分支测试。 */
static __declspec(naked) void continue_trap(void)
{
    __asm
    {
        mov native_continued, 1
        mov eax, 0
        mov edi, dword ptr [esp]
        mov esi, dword ptr [esp + 4]
        mov ebp, dword ptr [esp + 8]
        mov ebx, dword ptr [esp + 12]
        add esp, 0F4h
        ret 4
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
        mov dword ptr [esp + 0F4h], eax
        lea ebp, drive
        lea edi, owner
        lea esi, drive + 40h
        mov ebx, 17
        mov eax, 4
        mov ecx, 004A1FDCh
        jmp ecx
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
    fixture_number = number;
    fixture = number * 1664525u + 1013904223u;
    fixture ^= fixture << 13; fixture ^= fixture >> 17; fixture ^= fixture << 5;
    memset(drive, 0, sizeof(drive)); memset(owner, 0, sizeof(owner)); memset(target, 0, sizeof(target));
    memset(private_stack, 0xA5, sizeof(private_stack)); memset(operations, 0, sizeof(operations));
    operation_count = native_continued = 0;
    FIELD32(drive, 0xC) = POINTER(owner);
    FIELD32(owner, 0) = POINTER(owner_vtable); FIELD32(target, 0) = POINTER(target_vtable);
    const int32_t xs[] = { 0,128,-1,-255,-256,-257,INT_MIN,INT_MAX,16777216,-16777216 };
    int32_t point[3] = { xs[number % 10], xs[(number / 10) % 10], (fixture & 512) ? 416 : -416 };
    memcpy(owner + 0x88, point, 12); memcpy(drive + 0x40, point, 12);
    FIELD32(drive, 0x40) += (fixture & 1) ? 512 : 1;
    if (fixture & 2) memcpy(drive + 0x40, (void *)0x852998, 12);
    memcpy(target + 0x88, drive + 0x40, 12);
    if (fixture & (1u << 10)) FIELD32(target, 0x88) += 256;
    memcpy(drive + 0x34, drive + 0x40, 12);
    static const uint32_t dz[] = { 0,207,208,209,UINT32_MAX,0x80000000,0x7FFFFFFF };
    FIELD32(drive, 0x3C) += dz[(number / 100) % 7];
    FIELD32(drive, 0x58) = 4; FIELD32(drive, 0x5C) = 9;
    drive[0x63] = (uint8_t)((fixture >> 11) & 1);
    owner[0x74] = (uint8_t)((fixture >> 12) & 1); owner[0x7D] = 1;
    FIELD32(owner, 0x494) = (fixture & 4) ? POINTER(target) : 0;
    FIELD32(owner, 0x4D0) = 5;
    MEM32(0x8529D0) = 104;
    memcpy(alternate, owner, sizeof(owner));
    alternate[0x74] ^= 1;
    frame_stack = POINTER(private_stack + 2048);
    static const uint32_t progress[] = { 0, 7, 17, 0x7fffffff, 0x80000000 };
    MEM32(frame_stack + 0x3C) = progress[number % 5];
    static const uint16_t precision[] = { 0, 0x200, 0x300 };
    g_fpu_cw = (uint16_t)(0x7F | precision[(number / 1024) % 3] | (((number / 3072) % 4) << 10));
    set_control(g_fpu_cw);
    MEM32(frame_stack) = 0x12345678; MEM32(frame_stack + 4) = 0x23456789;
    MEM32(frame_stack + 8) = 0x3456789A; MEM32(frame_stack + 12) = 0x456789AB;
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
        uint32_t relative = POINTER(native_stub) - POINTER(stub + 10);
        memcpy(stub + 6, &relative, 4);
    }
    patch_jump(0x4CD9B0, stub_base + CANCEL * 16);
    patch_jump(0x4A1FA1, POINTER(continue_trap));
    owner_vtable[0x11C / 4] = stub_base + OCCUPY * 16;
    owner_vtable[0x19C / 4] = stub_base + SET_POSITION * 16;
    owner_vtable[0x1B4 / 4] = stub_base + UPDATE_POSITION * 16;
    owner_vtable[0x1A0 / 4] = stub_base + CELL_COORD * 16;
    owner_vtable[0x4C / 4] = stub_base + OWNER_POSITION * 16;
    target_vtable[0x4C / 4] = stub_base + TARGET_POSITION * 16;
    owner_vtable[0x174 / 4] = stub_base + MARK * 16;
    owner_vtable[0x16C / 4] = stub_base + MISSION * 16;
    owner_vtable[0x414 / 4] = stub_base + STOP * 16;
    owner_vtable[0x490 / 4] = stub_base + UPDATE * 16;
    FlushInstructionCache(GetCurrentProcess(), NULL, 0);
    unsigned continued = 0, returned = 0;
    for (unsigned number = 0; number < 65536; ++number)
    {
        initialize(number); execute_original();
        unsigned char expected_drive[sizeof(drive)], expected_owner[sizeof(owner)], expected_alternate[sizeof(alternate)];
        uint16_t expected_control = get_control();
        uint32_t expected_ops[64][5], expected_count = operation_count, expected_continued = native_continued;
        uint32_t expected_progress = MEM32(frame_stack + 0x3C);
        memcpy(expected_drive, drive, sizeof(drive)); memcpy(expected_owner, owner, sizeof(owner)); memcpy(expected_alternate, alternate, sizeof(alternate));
        memcpy(expected_ops, operations, sizeof(expected_ops));
        initialize(number);
        g_esp = frame_stack; g_ebp = POINTER(drive); g_edi = POINTER(owner); g_esi = POINTER(drive + 0x40);
        g_ebx = 17; g_eax = 4;
        uint32_t resume = ra2_ground_arrival_complete_bridge();
        uint32_t flags = recomp_eflags(g_flag_k, g_flag_a, g_flag_b, g_flag_cf, 1);
        int state_diff = memcmp(expected_drive, drive, sizeof(drive)) || memcmp(expected_owner, owner, sizeof(owner)) || memcmp(expected_alternate, alternate, sizeof(alternate));
        int abi_diff = resume ? (resume != 0x4A1FA1 || g_esp != frame_stack || g_ebp != POINTER(drive))
            : ((g_eax & 255u) != (native_eax & 255u) || g_esp != native_esp
                || g_ebx != native_ebx || g_esi != native_esi || g_edi != native_edi || g_ebp != native_ebp
                || (flags & 0x8D5) != (native_flags & 0x8D5));
        if (state_diff || abi_diff || expected_control != g_fpu_cw || (resume != 0) != (expected_continued != 0)
            || expected_count != operation_count || memcmp(expected_ops, operations, sizeof(expected_ops))
            || expected_progress != MEM32(frame_stack + 0x3C))
        {
            printf("arrival mismatch case=%u fixture=%08x state=%d abi=%d calls=%u/%u continue=%u/%u\n",
                number, fixture, state_diff, abi_diff, operation_count, expected_count, resume != 0, expected_continued);
            for (unsigned i = 0; i < operation_count || i < expected_count; ++i)
                printf("  op=%u/%u arg=%u/%u flag=%u/%u selector=%u/%u driving=%u/%u\n", operations[i][0], expected_ops[i][0],
                    operations[i][1], expected_ops[i][1], operations[i][2], expected_ops[i][2], operations[i][3], expected_ops[i][3],
                    operations[i][4], expected_ops[i][4]);
            return 1;
        }
        if (resume) ++continued; else ++returned;
    }
    printf("{\"passed\":true,\"cases\":65536,\"continued\":%u,\"returned\":%u,\"original_stack_cleanup_verified\":true}\n", continued, returned);
    return 0;
}
