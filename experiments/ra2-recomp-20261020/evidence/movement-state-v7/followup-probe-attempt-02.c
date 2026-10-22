#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>
#include "recomp_types.h"
#include "ground_prepare_bridge.h"
#include "ground_followup_bridge.h"
#include "native_probe_host.h"

uint32_t g_eax, g_ecx, g_edx, g_esp, g_ebx, g_esi, g_edi, g_ebp, g_cur_func;
uint16_t g_fpu_cw;
double g_st[8]; int g_fp_top;
static double ratio_value;
static unsigned surface_reads;
enum Operation { MISSION, TEST_1BC, TEST_1C0, TEAM, TEST_324, TEST_328, TARGET_KIND, POSITION, VECTOR,
    LENGTH, STOP_EMPTY, STOP_TARGET, REBUILD, ACCEPT, PREDICATE, CANCEL, FACING, BOUNDS, HEIGHT, CELL, PASSAGE, GATE, SURFACE, BLOCKER, ALLY, TYPE, LAND, NOTIFY, ALLOW_SEGMENT, OCCUPATION, TURN, SOUND, FIND_OBJECT, ATTACK_OBJECT, RECURSE, NEIGHBOR, ACCEPT_CELL, START_SEGMENT, ZERO_SPEED, TARGET_POSITION, PREPARE_CANDIDATE, OWNER_KIND, SLOW_RATIO, OP_COUNT };
static const unsigned argument_count[OP_COUNT] = { 0,0,0,0,0,0,0,1,3,0,2,2,3,1,0,0,1,2,0,1,5,2,1,3,1,0,1,4,0,1,2,2,2,3,3,1,1,2,2,1,2,0,0 };
static unsigned char drive[128], owner[0x700], target[0x100], rules[0x1500], private_stack[8192], aborted;
static uint32_t owner_vtable[0x500 / 4], target_vtable[0x100 / 4], fixture, fixture_number, stub_base;
static uint32_t operations[64][7], operation_count, cleanup_bytes;
static uint32_t frame_stack, host_stack, native_eax, native_esp, native_flags, entry_address;
static uint32_t native_ebx, native_esi, native_edi, native_ebp, native_resume, native_head;
static uint16_t initial_control, native_control;
static unsigned phase;
static unsigned char cell_data[0x200], type_data[0x1000];
static unsigned facing_reads;
static uint32_t locomotion_vtable[0x100 / 4], native_cell, native_level;
static unsigned char overlay_data[0x300];
static uint32_t overlays_table[27];
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
        case FACING:
            ++facing_reads;
            MEM32(arguments[0]) = fixture_number & 1 ? ((FIELD32(owner, 0x4D0) << 13) & 0xFFFF) : fixture & 0xFFFF;
            return arguments[0];
        case BOUNDS:
            record[1] = MEM32(arguments[0]); record[2] = arguments[1];
            return (fixture >> 1) & 1;
        case HEIGHT: return 4;
        case CELL:
        case LAND:
            memcpy(record + 1, (void *)(uintptr_t)arguments[0], id == CELL ? 4 : 12);
            return POINTER(cell_data);
        case PASSAGE:
            record[1] = arguments[0] == POINTER(cell_data); record[2] = arguments[1];
            record[3] = arguments[2] | (arguments[3] << 8) | (arguments[4] << 16);
            return (fixture >> 2) & 7;
        case GATE:
            record[1] = arguments[0] == POINTER(owner); record[2] = MEM32(arguments[1]);
            return (fixture >> 2) & 1;
        case SURFACE:
            memcpy(record + 1, (void *)(uintptr_t)arguments[0], 12);
            return surface_reads++==0 ? ((fixture>>16)&3)*104 : ((fixture>>18)&3)*104;
        case BLOCKER:
            record[1] = object == POINTER(cell_data); record[2] = arguments[1] & 255u; record[3] = arguments[2];
            return (fixture & (1u << 6)) ? POINTER(target) : 0;
        case ALLY: record[1] = arguments[0] == POINTER(target); return (fixture >> 7) & 1;
        case TYPE: return POINTER(type_data);
        case NOTIFY:
            record[1] = arguments[0]; record[2] = arguments[1] | arguments[2] << 8;
            record[3] = arguments[3] & 255u;
            if (fixture & (1u << 28)) FIELD32(owner, 0x4D0) = 7;
            return 0;
        case ALLOW_SEGMENT: return (fixture >> 1) & 1;
        case OCCUPATION:
            record[1] = arguments[0];
            drive[0x61] = (uint8_t)arguments[0];
            if (fixture & (1u << 20)) owner[0x57B] = (uint8_t)arguments[0];
            return 0;
        case TURN:
            record[1] = arguments[0] == POINTER(drive + 4); record[2] = arguments[1] & 0xFFFFu;
            return 0;
        case SOUND:
            record[1] = object; record[2] = arguments[0]; record[3] = arguments[1];
            return 0;
        case FIND_OBJECT:
            record[1] = MEM32(arguments[0]); record[2] = MEM32(arguments[0] + 4); record[3] = arguments[1] & 255u;
            return (fixture & (1u << 6)) ? POINTER(target) : 0;
        case ATTACK_OBJECT:
            record[1] = arguments[0]; record[2] = arguments[1] == POINTER(cell_data) ? 1 : arguments[1] == POINTER(target) ? 2 : 3;
            record[3] = arguments[2]; owner[0x57A] = 1;
            return 0;
        case RECURSE:
            record[1] = arguments[0] == POINTER(&aborted); record[2] = arguments[1]; record[3] = arguments[2];
            FIELD32(drive, 0x58) = 7; drive[0x61] = 0;
            return (fixture >> 10) & 1;
        case NEIGHBOR:
            record[1]=arguments[0];
            return fixture & 8 ? POINTER(cell_data) : 0;
        case ACCEPT_CELL:
            record[1]=arguments[0]==POINTER(owner);
            if (fixture & 16) owner[0x7D]=0;
            if (fixture & 32) owner[0x76]=1;
            return fixture & 64 ? 1 : 0;
        case START_SEGMENT:
            memcpy(record+1,(void *)(uintptr_t)arguments[0],12);
            drive[0x61]=1; FIELD32(owner,0x4D0)=3;
            return 1;
        case ZERO_SPEED:
            record[1]=arguments[0]; record[2]=arguments[1];
            memcpy(owner+0x468,arguments,8);
            return 0;
        case TARGET_POSITION:
            memcpy((void *)(uintptr_t)arguments[0],owner+0x88,12);
            return arguments[0];
        case PREPARE_CANDIDATE:
            record[1]=MEM32(arguments[0]); record[2]=arguments[1];
            if (fixture & 16) FIELD32(owner,0x4D4)=UINT32_MAX;
            return 0;
        case OWNER_KIND: return fixture & 32 ? 1 : 6;
        case SLOW_RATIO: return 0;
        default: exit(2);
    }
}

static uint32_t native_operation(unsigned id, uint32_t object, const uint32_t *arguments)
{
    cleanup_bytes = argument_count[id] * 4;
    uint32_t result=operation(id,object,arguments);
    if (id==SLOW_RATIO) { __asm fld ratio_value }
    return result;
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
LIFTED(l_vector,VECTOR) static void l_length(void)
{
    uint32_t point = g_ecx, result, target_address = 0x41B780;
    uint16_t host_control, guest_control = g_fpu_cw;
    __asm
    {
        fnstcw host_control
        fldcw guest_control
        mov ecx, point
        call target_address
        mov result, eax
        fnstcw guest_control
        fldcw host_control
    }
    g_eax = result; g_fpu_cw = guest_control; g_esp += 4;
} LIFTED(l_empty,STOP_EMPTY) LIFTED(l_target,STOP_TARGET)
LIFTED(l_rebuild,REBUILD) LIFTED(l_accept,ACCEPT) LIFTED(l_predicate,PREDICATE) LIFTED(l_cancel,CANCEL)
LIFTED(l_facing,FACING) LIFTED(l_bounds,BOUNDS) LIFTED(l_height,HEIGHT) LIFTED(l_cell,CELL)
LIFTED(l_passage,PASSAGE) LIFTED(l_gate,GATE) LIFTED(l_surface,SURFACE) LIFTED(l_blocker,BLOCKER)
LIFTED(l_ally,ALLY) LIFTED(l_type,TYPE) LIFTED(l_land,LAND) LIFTED(l_notify,NOTIFY)
LIFTED(l_allow,ALLOW_SEGMENT) LIFTED(l_occupation,OCCUPATION) LIFTED(l_turn,TURN)
LIFTED(l_sound,SOUND) LIFTED(l_find,FIND_OBJECT) LIFTED(l_attack,ATTACK_OBJECT) LIFTED(l_recurse,RECURSE)
LIFTED(l_neighbor,NEIGHBOR) LIFTED(l_cell_accept,ACCEPT_CELL) LIFTED(l_start,START_SEGMENT) LIFTED(l_zero,ZERO_SPEED)
LIFTED(l_target_position,TARGET_POSITION) LIFTED(l_prepare_candidate,PREPARE_CANDIDATE) LIFTED(l_owner_kind,OWNER_KIND)
static void l_ratio(void)
{
    g_eax=operation(SLOW_RATIO,g_ecx,NULL);
    fp_push_impl(g_st,&g_fp_top,ratio_value); g_esp+=4;
}
static recomp_func_t lifted[OP_COUNT] = { l_mission,l_1bc,l_1c0,l_team,l_324,l_328,l_kind,l_position,
    l_vector,l_length,l_empty,l_target,l_rebuild,l_accept,l_predicate,l_cancel,l_facing,l_bounds,l_height,l_cell,l_passage,l_gate,l_surface,l_blocker,l_ally,l_type,l_land,l_notify,l_allow,l_occupation,l_turn,l_sound,l_find,l_attack,l_recurse,l_neighbor,l_cell_accept,l_start,l_zero,l_target_position,l_prepare_candidate,l_owner_kind,l_ratio };
recomp_func_t recomp_lookup_manual(uint32_t address)
{
    if (address >= stub_base && address < stub_base + OP_COUNT * 16) return lifted[(address - stub_base) / 16];
    switch (address)
    {
        case 0x475D60: return l_target_position;
        case 0x5D4540: return l_ratio;
        case 0x476AC0: return l_neighbor;
        case 0x476CC0: return l_cell_accept;
        case 0x4A0BC0: return l_start;
        case 0x713DB0: return l_sound;
        case 0x471830: return l_find;
        case 0x4A2670: return l_recurse;
        case 0x68A680: return l_team;
        case 0x41B630: return l_vector;
        case 0x41B780: return l_length;
        case 0x4C3000: return l_rebuild;
        case 0x4C8D60: return l_predicate;
        case 0x4CD9B0: return l_cancel;
        case 0x4B8BE0: return l_facing;
        case 0x55A660: return l_bounds;
        case 0x5D47D0: return l_height;
        case 0x548070: return l_cell;
        case 0x55ACD0: return l_gate;
        case 0x55A280: return l_surface;
        case 0x471660: return l_blocker;
        case 0x4E5580: return l_ally;
        case 0x636F10: return l_predicate;
        case 0x548000: return l_land;
        case 0x476920: return l_notify;
        default: return NULL;
    }
}
recomp_func_t recomp_lookup(uint32_t address) { (void)address; return NULL; }
recomp_func_t recomp_lookup_import(uint32_t address) { (void)address; return NULL; }
void ra2_state_math(uint32_t stack, uint32_t ebp, uint32_t output, uint32_t source)
{
    (void)stack; (void)ebp; (void)output; (void)source;
}
void ra2_state_movement_audit(uint32_t stage, uint32_t actor, uint32_t cell, uint32_t object)
{ (void)stage; (void)actor; (void)cell; (void)object; }
static void patch_jump(uint32_t address, uint32_t destination)
{
    MEM8(address) = 0xE9; MEM32(address + 1) = destination - address - 5;
}
static __declspec(naked) void continue_trap(void)
{
    __asm
    {
        mov native_head, ebx
        mov native_cell, esi
        mov native_level, edi
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
        mov ecx, eax
        mov eax, fixture_number
        and eax, 7
        mov ebx, eax
        mov esi, fixture_number
        and esi, 3
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
    facing_reads = 0;
    FIELD32(drive, 4) = POINTER(locomotion_vtable);
    owner[0x79] = (fixture >> 12) & 3;
    owner[0x57B] = (uint8_t)((fixture >> 14) & 1);
    memset(cell_data, 0, sizeof(cell_data)); memset(type_data, 0, sizeof(type_data));
    type_data[0xAA0] = (uint8_t)((fixture >> 5) & 1);
    type_data[0xAF3] = (uint8_t)((fixture >> 6) & 1);
    const uint32_t overlays[] = { 0,1,26,UINT32_MAX };
    FIELD32(cell_data, 0x44) = overlays[(fixture >> 9) & 3];
    FIELD32(cell_data, 0xEC) = (fixture & (1u << 17)) ? 10 : 0;
    FIELD32(cell_data, 0x140) = (fixture & (1u << 19)) ? 0x100 : 0;
    cell_data[0x11B] = (uint8_t)((fixture & (1u << 20)) ? 1 : 4);
    MEM32(0x8529D0) = 104;
    MEM32(0xA35DEC) = POINTER(overlays_table);
    for (unsigned i = 0; i < 27; ++i) overlays_table[i] = POINTER(overlay_data);
    overlay_data[0x278] = (uint8_t)((fixture >> 8) & 1);
    overlay_data[0x1FD] = (uint8_t)((fixture >> 8) & 1);
    owner[0x5A1] = (uint8_t)((fixture >> 1) & 1);
    FIELD32(owner, 0x558) = starts[(number / 7) % 6];
    FIELD32(owner, 0x560) = times[(number / 11) % 7];
    FIELD32(rules, 0x13D0) = times[(number / 13) % 7];
    MEM32(frame_stack + 0x14) = 0xFFF00010;
    MEM32(frame_stack + 0x18) = (fixture >> 2) & 7;
    MEM32(frame_stack + 0x28) = 0xA5A5A5A5;
    MEM8(frame_stack + 0x13) = (uint8_t)((fixture >> 7) & 1);
    FIELD32(owner, 0x53C) = 7;
    owner[0x57A] = (uint8_t)((fixture >> 7) & 1);
    MEM32(frame_stack + 0x64) = (fixture >> 9) & 1;
    FIELD32(rules, 0x620) = 123;
    surface_reads=0; g_fp_top=0; memset(g_st,0,sizeof(g_st));
    static const float factors[]={0.0f,0.01f,0.1f,0.33333334f,0.7f,1.0f,1.5f,-0.1f};
    float terrain=factors[(number/3)%8];
    for (unsigned i=0;i<36;++i) memcpy((void *)(uintptr_t)(0x850EA0+i*4),&terrain,4);
    FIELD32(type_data,0x5A4)=(number/24)%9;
    static const double slopes[]={0.1,0.3,0.7,1.0,1.1,1.3333333333333333,1.0000000000000002,0.0};
    for(unsigned i=0;i<4;++i) memcpy(rules+0x690+i*8,&slopes[((number/7)+i)%8],8);
    static const double ratios[]={0.0,0.5,0.5000000000000001,1.0};
    ratio_value=ratios[(number/17)%4];
    double limit=0.5; memcpy(rules+0x1368,&limit,8);
    double speed=slopes[(number/19)%8]; memcpy(owner+0x468,&speed,8);
    FIELD32(drive,0x58)=(number&1) ? 64 : 5;
    for (unsigned i=0;i<24;++i) FIELD32(owner,0x4D0+i*4)=i ^ fixture;
    MEM32(frame_stack+0x2C)=POINTER(cell_data);
    const int32_t second[]={-1,0,1,2,3,4,5,6,7,8};
    MEM32(frame_stack+0x24)=(uint32_t)second[(number/8)%10];
    MEM32(frame_stack+0x68)=(fixture>>9)&1;
    const int32_t candidates[4][3]={{0,0,0},{128,-257,416},{INT32_MIN,INT32_MAX,0},{17280,29312,416}};
    memcpy((void *)(uintptr_t)(frame_stack+0x38),candidates[(fixture>>10)&3],12);
    owner[0x76]=(uint8_t)((fixture>>12)&1);
    FIELD32(owner,0x4D4)=number&1 ? UINT32_MAX : number&7;
    static const int32_t offsets[]={0,1,511,512,513,6144,100000,INT32_MAX,INT32_MIN};
    FIELD32(drive,0x34)=FIELD32(owner,0x88)+(uint32_t)offsets[(number/8)%9];
    FIELD32(drive,0x38)=FIELD32(owner,0x8C)+(fixture>>20);
    FIELD32(drive,0x3C)=FIELD32(owner,0x90)+(fixture&255);
    if (phase==1) FIELD32(drive,0x58)=5;
}

int main(int argc, char **argv)
{
    if (argc != 3) return 2;
    phase = (unsigned)atoi(argv[2]);
    if (phase > 1) return 2;
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
    uint32_t extra_addresses[] = { 0x4B8BE0,0x55A660,0x5D47D0,0x548070,0x55ACD0,0x55A280,0x471660,0x4E5580,0x636F10,0x548000,0x476920 };
    unsigned extra_ids[] = { FACING,BOUNDS,HEIGHT,CELL,GATE,SURFACE,BLOCKER,ALLY,PREDICATE,LAND,NOTIFY };
    for (unsigned i = 0; i < sizeof(extra_ids) / sizeof(extra_ids[0]); ++i) patch_jump(extra_addresses[i], stub_base + extra_ids[i] * 16);
    patch_jump(0x475D60,stub_base+TARGET_POSITION*16);
    patch_jump(0x5D4540,stub_base+SLOW_RATIO*16);
    owner_vtable[0x4B8/4]=stub_base+PREPARE_CANDIDATE*16;
    owner_vtable[0x2C/4]=stub_base+OWNER_KIND*16;
    patch_jump(0x476AC0,stub_base+NEIGHBOR*16);
    patch_jump(0x476CC0,stub_base+ACCEPT_CELL*16);
    patch_jump(0x4A0BC0,stub_base+START_SEGMENT*16);
    owner_vtable[0x4C8/4]=stub_base+ZERO_SPEED*16;
    patch_jump(0x713DB0, stub_base + SOUND * 16);
    patch_jump(0x471830, stub_base + FIND_OBJECT * 16);
    patch_jump(0x4A2670, stub_base + RECURSE * 16);
    owner_vtable[0x1DC / 4] = stub_base + ATTACK_OBJECT * 16;
    owner_vtable[0x80 / 4] = stub_base + TYPE * 16;
    owner_vtable[0x194 / 4] = stub_base + PASSAGE * 16;
    owner_vtable[0x27C / 4] = stub_base + ALLOW_SEGMENT * 16;
    owner_vtable[0x11C / 4] = stub_base + OCCUPATION * 16;
    locomotion_vtable[0x4C / 4] = stub_base + TURN * 16;
    for (unsigned i = 0; i < 6; ++i) if (addresses[i]!=0x41B780) patch_jump(addresses[i], stub_base + ids[i] * 16);
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
    uint32_t boundaries[4] = { 0 };
    boundaries[0]=phase==0 ? 0x4A3E35 : 0x4A3F8B; boundaries[1]=0x4A3F9F;
    unsigned boundary_count=phase==0 ? 1 : 2;
    unsigned outcome_counts[5][6] = { 0 };
    for (unsigned once = 0; once < 1; ++once)
    {
        for (unsigned b = 0; b < boundary_count; ++b)
        {
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
            const uint32_t entries[] = { 0x4A3C9B,0x4A3E35 };
            entry_address = entries[phase];
            initialize(number); execute_original();
            unsigned char expected_drive[sizeof(drive)], expected_owner[sizeof(owner)], expected_abort = aborted;
            uint32_t expected_ops[64][7], expected_count = operation_count, expected_resume = native_resume;
            memcpy(expected_drive, drive, sizeof(drive)); memcpy(expected_owner, owner, sizeof(owner));
            memcpy(expected_ops, operations, sizeof(expected_ops));
            uint32_t expected_level = MEM32(frame_stack + 0x28);
            unsigned expected_crush = MEM8(frame_stack + 0x13);
            uint64_t expected_factor; memcpy(&expected_factor,(void *)(uintptr_t)(frame_stack+0x18),8);
            initialize(number);
            g_esp = frame_stack; g_ebp = POINTER(drive); g_edi = POINTER(drive + 0x34);
            g_ebx = FIELD32(owner, 0x4D0); g_eax = fixture & 1; g_fpu_cw = initial_control;
            g_ebx=number&7; g_esi=number&3;
            uint32_t resume;
            if (phase==0) { ra2_ground_speed_prepare_bridge(); resume=0x4A3E35; }
            else resume=ra2_ground_followup_bridge();
            uint32_t flags = recomp_eflags(g_flag_k, g_flag_a, g_flag_b, g_flag_cf, 1);
            int state_diff = memcmp(expected_drive, drive, sizeof(drive)) || memcmp(expected_owner, owner, sizeof(owner));
            int abi_diff = resume ? (g_esp != frame_stack || g_ebp != POINTER(drive)
                || g_ebx != native_head || (phase==1 && resume!=0x4A3F9F && g_esi!=native_cell))
                : ((g_eax & 255u) != (native_eax & 255u) || g_esp != native_esp
                    || g_ebx != native_ebx || g_esi != native_esi || g_edi != native_edi || g_ebp != native_ebp
                    || (flags & 0x8D5) != (native_flags & 0x8D5));
            uint64_t actual_factor; memcpy(&actual_factor,(void *)(uintptr_t)(frame_stack+0x18),8);
            int locals_diff=MEM8(frame_stack+0x13)!=expected_crush || MEM32(frame_stack+0x28)!=expected_level || (phase==0 && actual_factor!=expected_factor);
            if (locals_diff || state_diff || abi_diff || resume != expected_resume || aborted != expected_abort || g_fpu_cw != native_control
                || expected_count != operation_count || memcmp(expected_ops, operations, sizeof(expected_ops)))
            {
                printf("prepare mismatch phase=%u case=%u fixture=%08x state=%d abi=%d resume=%x/%x calls=%u/%u cw=%x/%x\n",
                    phase, number, fixture, state_diff, abi_diff, resume, expected_resume, operation_count, expected_count,
                    g_fpu_cw, native_control);
                for(unsigned i=0;i<sizeof(drive);++i) if(drive[i]!=expected_drive[i]) printf("drive %x: %x/%x\n",i,drive[i],expected_drive[i]);
                for(unsigned i=0;i<sizeof(owner);++i) if(owner[i]!=expected_owner[i]) printf("owner %x: %x/%x\n",i,owner[i],expected_owner[i]);
                printf("locals=%d factor=%llx/%llx\n",locals_diff,(unsigned long long)actual_factor,(unsigned long long)expected_factor);
                for (unsigned i = 0; i < operation_count || i < expected_count; ++i)
                    printf("  operation=%u/%u v=%x,%x,%x/%x,%x,%x\n", operations[i][0], expected_ops[i][0],
                        operations[i][1], operations[i][2], operations[i][3], expected_ops[i][1], expected_ops[i][2], expected_ops[i][3]);
                return 1;
            }
            unsigned outcome = 0;
            for (unsigned i = 0; i < boundary_count; ++i) if (resume == boundaries[i]) outcome = i + 1;
            ++outcome_counts[phase][outcome];
        }
    }
    printf("{\"phase\":%u,\"passed\":true,\"followup_cases\":65536,\"live_stack_locals_verified\":true,\"state_calls_abi_cw_verified\":true}\n", phase);
    return 0;
}
