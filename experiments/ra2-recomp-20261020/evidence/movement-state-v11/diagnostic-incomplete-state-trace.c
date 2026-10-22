#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "state_trace.h"
#include "movement_fixture.h"
#include "recomp_target.h"

/* 这些地址仅对应 fe67fdac... 的本机 RA2 1.006；依据及字段范围保存在 state-step-v1 报告。 */
#define U32(va) (*(uint32_t *)(uintptr_t)(va))
#define I32(va) (*(int32_t *)(uintptr_t)(va))
#define U8(va) (*(uint8_t *)(uintptr_t)(va))
#define U16(va) (*(uint16_t *)(uintptr_t)(va))
#define FRAME_ADDRESS 0x00A40D2Cu
#define MAX_OBJECTS 16384
#define MAX_ORDERS 128

typedef struct FrameOrder
{
    uint32_t frame, id, mission, x, y;
    int submitted, executed;
} FrameOrder;

static char state_path[MAX_PATH];
static char cell_catalog_path[MAX_PATH];
static int cell_catalog_written;
static FILE *state_file;
static uint32_t first_frame = 2200, last_frame = 2300, previous_frame;
static int started;
static FrameOrder orders[MAX_ORDERS];
static int order_count;
static void *tick_trampoline, *event_trampoline, *math_trampoline;
static uint32_t detail_id;
static uint32_t detail_locomotive;
static uint16_t original_cw;
static int original_mode;
static int movement_audit_enabled;
static void *advance_sample_trampoline;
static void *object_filter_trampoline;
static void *continuation_classified_trampoline,*followup_candidate_trampoline,*followup_search_trampoline;
static void *speed_prepare_trampoline, *followup_prepare_trampoline, *followup_failure_trampoline, *turn_classified_trampoline;
static void *special_temporary_trampoline, *special_cloaked_trampoline, *template_select_trampoline, *template_commit_trampoline, *prepare_identity_trampoline;
static void *terrain_trampoline, *clearance_trampoline, *traffic_trampoline;
static void *wall_trampoline, *gate_trampoline, *failure_trampoline, *retry_result_trampoline;
static uint32_t phase_ftol = 0x0077F110u;
extern uint16_t g_fpu_cw;

static void fail(const char *reason)
{
    fprintf(stderr, "[state-error] %s\n", reason);
    if (state_file) fflush(state_file);
    fflush(stderr);
    TerminateProcess(GetCurrentProcess(), 7);
}

int ra2_state_arg(int argc, char **argv, int i)
{
    int fixture_arguments = ra2_movement_fixture_arg(argc, argv, i);
    if (fixture_arguments) return fixture_arguments;
    const char *name = argv[i];
    if (!strcmp(name, "--state-movement-audit"))
    {
        movement_audit_enabled = 1;
        return 1;
    }
    char tail;
    if (strcmp(name, "--state-log") && strcmp(name, "--state-range") && strcmp(name, "--frame-order")
        && strcmp(name, "--state-detail-id") && strcmp(name, "--state-cell-catalog")) return 0;
    if (i + 1 >= argc) fail("missing argument");
    if (!strcmp(name, "--state-log"))
    {
        DWORD length = GetFullPathNameA(argv[i + 1], sizeof(state_path), state_path, NULL);
        if (!length || length >= sizeof(state_path)) fail("invalid state path");
    }
    else if (!strcmp(name, "--state-cell-catalog"))
    {
        DWORD length = GetFullPathNameA(argv[i + 1], sizeof(cell_catalog_path), cell_catalog_path, NULL);
        if (!length || length >= sizeof(cell_catalog_path)) fail("invalid cell catalog path");
    }
    else if (!strcmp(name, "--state-detail-id"))
    {
        if (sscanf(argv[i + 1], "%u%c", &detail_id, &tail) != 1) fail("expected object ID");
    }
    else if (!strcmp(name, "--state-range"))
    {
        if (sscanf(argv[i + 1], "%u:%u%c", &first_frame, &last_frame, &tail) != 2 || last_frame < first_frame)
            fail("expected --state-range FIRST:LAST");
    }
    else
    {
        FrameOrder *order;
        if (order_count == MAX_ORDERS) fail("too many frame orders");
        order = &orders[order_count++];
        if (sscanf(argv[i + 1], "%u:%u:%u:%u:%u%c", &order->frame, &order->id, &order->mission, &order->x, &order->y, &tail) != 5)
            fail("expected --frame-order FRAME:UID:MISSION:CELL_X:CELL_Y");
        /* 第一闭环限定移动与停止，后续命令须先核实构造器和执行路径。 */
        if ((order->mission != 2 && order->mission != 13) || order->x >= 1000 || order->y >= 1000) fail("unsupported mission or cell");
    }
    return 2;
}

void ra2_state_validate(void)
{
#ifndef RA2_TARGET_GAME
    if (state_path[0]) fail("state tracing requires the verified RA2 1.006 target");
#endif
    if (!last_frame) fail("last state frame must be positive");
    if (movement_audit_enabled && !state_path[0]) fail("movement audit requires --state-log");
    if (ra2_movement_fixture_requested() && (!state_path[0] || !movement_audit_enabled))
        fail("wall fixture requires --state-log and --state-movement-audit");
    if (order_count && !state_path[0]) fail("frame orders require --state-log");
    if (cell_catalog_path[0] && !state_path[0]) fail("cell catalog requires --state-log");
    for (int i = 0; i < order_count; ++i)
        if (orders[i].frame < first_frame || orders[i].frame >= last_frame) fail("order outside trace range");
}

static void open_trace(void)
{
    if (state_file) return;
    /* 拒绝覆盖已有证据；运行器负责创建唯一目录。 */
    HANDLE handle = CreateFileA(state_path, GENERIC_WRITE, FILE_SHARE_READ, NULL, CREATE_NEW, FILE_ATTRIBUTE_NORMAL, NULL);
    if (handle == INVALID_HANDLE_VALUE) fail("state log already exists or cannot be created");
    CloseHandle(handle);
    state_file = fopen(state_path, "wb");
    if (!state_file) fail("cannot open state log");
    fprintf(state_file, "{\"kind\":\"header\",\"schema\":12,\"boundary\":\"LogicClass_0053D890_entry\",\"first\":%u,\"last\":%u}\n",
        first_frame, last_frame);
}

static int compare_objects(const void *a, const void *b)
{
    uint32_t left = U32(*(const uint32_t *)a + 0x10), right = U32(*(const uint32_t *)b + 0x10);
    return (left > right) - (left < right);
}

static uint32_t find_object(uint32_t id)
{
    uint32_t data = U32(0xA40C24), count = U32(0xA40C30), found = 0;
    if (count > MAX_OBJECTS) fail("invalid TechnoClass count");
    for (uint32_t i = 0; i < count; ++i)
    {
        uint32_t object = U32(data + i * 4);
        if (U32(object + 0x10) == id)
        {
            if (found) fail("ambiguous object ID");
            found = object;
        }
    }
    return found;
}

static int house_index(uint32_t house)
{
    uint32_t count = U32(0xA322A8), data = U32(0xA3229C);
    if (count > 64) fail("invalid HouseClass count");
    for (uint32_t i = 0; i < count; ++i) if (U32(data + 4 * i) == house) return (int)i;
    return -1;
}

static void hex_bytes(uint32_t address, uint32_t count)
{
    static const char digits[] = "0123456789abcdef";
    for (uint32_t i = 0; i < count; ++i)
    {
        uint8_t value = U8(address + i);
        fputc(digits[value >> 4], state_file);
        fputc(digits[value & 15], state_file);
    }
}

static void write_cell_catalog(uint32_t frame)
{
    if (!cell_catalog_path[0] || cell_catalog_written) return;
    HANDLE handle = CreateFileA(cell_catalog_path, GENERIC_WRITE, FILE_SHARE_READ, NULL, CREATE_NEW, FILE_ATTRIBUTE_NORMAL, NULL);
    if (handle == INVALID_HANDLE_VALUE) fail("cell catalog already exists or cannot be created");
    CloseHandle(handle);
    FILE *output = fopen(cell_catalog_path, "wb");
    if (!output) fail("cannot open cell catalog");
    /* 原版 0x548070 明确以 y*512+x 索引 MapClass+0x138，范围为 0x40000；这里只读数据，不调用游戏服务。 */
    uint32_t cells = U32(0x8324E0 + 0x138), count = 0;
    if (!cells) fail("missing map cell vector");
    fprintf(output, "{\"frame\":%u,\"cells\":[", frame);
    for (uint32_t slot = 0; slot < 0x40000; ++slot)
    {
        uint32_t cell = U32(cells + slot * 4);
        if (!cell) continue;
        fprintf(output, "%s{\"cell\":[%u,%u],\"land\":%d,\"level\":%d,\"overlay\":%d,\"bridge\":%u}",
            count++ ? "," : "", slot & 511, slot >> 9, I32(cell + 0xEC), (int)(int8_t)U8(cell + 0x11B),
            I32(cell + 0x44), (U32(cell + 0x140) & 0x100) != 0);
    }
    fprintf(output, "]}\n");
    if (fclose(output)) fail("cannot finish cell catalog");
    cell_catalog_written = 1;
}

static void snapshot(uint32_t frame)
{
    write_cell_catalog(frame);
    static uint32_t objects[MAX_OBJECTS];
    uint32_t data = U32(0xA40C24), count = U32(0xA40C30), scenario = U32(0xA3D290);
    if (count > MAX_OBJECTS || !scenario) fail("invalid world at simulation boundary");
    memcpy(objects, (void *)(uintptr_t)data, count * sizeof(objects[0]));
    qsort(objects, count, sizeof(objects[0]), compare_objects);
    fprintf(state_file, "{\"kind\":\"state\",\"frame\":%u,\"next_id\":%u,\"fpu_cw\":%u,\"rng\":{\"disabled\":%u,\"indices\":[%u,%u],\"table\":\"",
        frame, U32(scenario + 0x214), (original_mode ? original_cw : g_fpu_cw) & 0x1F3Fu,
        U8(scenario + 0x218), U32(scenario + 0x21C), U32(scenario + 0x220));
    /* 0x638790/0x638840 仅使用标志、双索引与 250 个状态字；偏移 1..3 是未初始化填充，旧原始记录保留。 */
    hex_bytes(scenario + 0x224, 250 * 4);
    fprintf(state_file, "\"},\"objects\":[");
    for (uint32_t i = 0; i < count; ++i)
    {
        uint32_t object = objects[i], id = U32(object + 0x10);
        if (i && id == U32(objects[i - 1] + 0x10)) fail("duplicate object ID");
        fprintf(state_file, "%s{\"id\":%u,\"class\":%u,\"owner\":%d,\"health\":%d,\"position\":[%d,%d,%d],\"mission\":[%d,%d,%d],\"facings\":[",
            i ? "," : "", id, U32(object), house_index(U32(object + 0x1B4)), I32(object + 0x6C),
            I32(object + 0x88), I32(object + 0x8C), I32(object + 0x90), I32(object + 0x98), I32(object + 0x9C), I32(object + 0xA0));
        /* 0x4B89D0/0x4B89F0 核实了三个方向结构；仅读取有效宽度，排除 DirStruct 和计时器中的填充。 */
        for (uint32_t k = 0; k < 3; ++k)
        {
            uint32_t facing = object + 0x2C8 + k * 24;
            fprintf(state_file, "%s[%u,%u,%d,%d,%u]", k ? "," : "", U16(facing), U16(facing + 4),
                I32(facing + 8), I32(facing + 16), U16(facing + 20));
        }
        fprintf(state_file, "]");
        if (U32(object) == 0x7ADDF8)
        {
            uint32_t locomotive = U32(object + 0x564);
            fprintf(state_file, ",\"locomotor_vtable\":%u,\"cloak_state\":%d",
                locomotive ? U32(locomotive) : 0, I32(object + 0x1B8));
            if (locomotive && U32(locomotive) == 0x7A04CC)
            {
                uint32_t drive = locomotive - 4;
                fprintf(state_file, ",\"ground_drive\":{\"destination\":[%d,%d,%d],\"segment_end\":[%d,%d,%d],"
                    "\"sample_progress\":%d,\"path_selector\":%d,\"sample_index\":%d,\"flags_60_64\":[%u,%u,%u,%u,%u],\"drive_speed_bits\":\"",
                    I32(drive + 0x34), I32(drive + 0x38), I32(drive + 0x3C), I32(drive + 0x40), I32(drive + 0x44), I32(drive + 0x48),
                    I32(drive + 0x4C), I32(drive + 0x58), I32(drive + 0x5C), U8(drive + 0x60), U8(drive + 0x61), U8(drive + 0x62),
                    U8(drive + 0x63), U8(drive + 0x64));
                hex_bytes(drive + 0x50, 8);
                fprintf(state_file, "\",\"unit_speed_bits\":\"");
                hex_bytes(object + 0x468, 8);
                fprintf(state_file, "\",\"speed_multiplier_bits\":\"");
                hex_bytes(object + 0x470, 8);
                fprintf(state_file, "\",\"surfaces\":[%d,%d],\"surface_timer\":[%d,%d,%d],"
                    "\"owner_flags_74_79\":[%u,%u],\"navigation_flags\":[%u,%u],\"path_directions\":[",
                    I32(drive + 0x1C), I32(drive + 0x20), I32(drive + 0x24), I32(drive + 0x2C), I32(drive + 0x30),
                    U8(object + 0x74), U8(object + 0x79), U8(object + 0x5A0), U8(object + 0x5A1));
                /* 0x4A143D/0x4A1453 确认 24 槽队列；只比较 -1 终止符前的有效方向，忽略已失效的尾槽。 */
                for (uint32_t slot = 0; slot < 24 && I32(object + 0x4D0 + slot * 4) != -1; ++slot)
                {
                    fprintf(state_file, "%s%d", slot ? "," : "", I32(object + 0x4D0 + slot * 4));
                }
                fprintf(state_file, "],\"path_retry_timer\":[%d,%d],\"path_failure_counter\":%d,\"prepare_flags_578_57a\":[%u,%u],"
                    "\"bridge_transition_pending\":%u,\"obstruction_wait_timer\":[%d,%d]}",
                    I32(object + 0x530), I32(object + 0x538), I32(object + 0x53C), U8(object + 0x578), U8(object + 0x57A),
                    U8(object + 0x57B), I32(object + 0x558), I32(object + 0x560));
            }
        }
        if (U32(object) == 0x79CBBC && U8(U32(object + 0x418) + 0x1351))
        {
            /* 原版 44D880 + 496B30：开闸任务 24 且动画双标志为 0/1 时允许穿过。 */
            int32_t mission = I32(object + 0x98) == -1 ? I32(object + 0xA0) : I32(object + 0x98);
            fprintf(state_file, ",\"gate\":{\"animation_flags\":[%u,%u],\"passable\":%s}", U8(object + 0x2C0), U8(object + 0x2C1),
                mission == 24 && !U8(object + 0x2C0) && U8(object + 0x2C1) == 1 ? "true" : "false");
        }
        fprintf(state_file, "}");
    }
    fprintf(state_file, "],\"houses\":[");
    count = U32(0xA322A8);
    data = U32(0xA3229C);
    if (count > 64) fail("invalid house vector");
    for (uint32_t i = 0; i < count; ++i)
    {
        uint32_t house = U32(data + 4 * i);
        /* 原版资源字段仍以偏移保存，待与读写函数逐一核实时再完善命名。 */
        fprintf(state_file, "%s{\"index\":%u,\"id\":%u,\"field_24c\":%d}", i ? "," : "", i, U32(house + 0x10), I32(house + 0x24C));
    }
    fprintf(state_file, "],\"out_count\":%u}\n", U32(0xA32338));
    if (detail_id)
    {
        detail_locomotive = 0;
        uint32_t object = find_object(detail_id);
        if (object && U32(object) == 0x7ADDF8)
        {
            uint32_t locomotive = U32(object + 0x564);
            if (locomotive && U32(locomotive) == 0x7A04CC)
            {
                /* 此诊断保留 DriveLocomotion 的原始标量；跳过 +0x28 填充及 +0x68 接口指针，不纳入正式对象等价范围。 */
                uint32_t base = locomotive - 4;
                detail_locomotive = base;
                fprintf(state_file, "{\"kind\":\"drive\",\"frame\":%u,\"id\":%u,\"fields\":[", frame, detail_id);
                for (uint32_t offset = 0x1C; offset <= 0x5C; offset += 4)
                {
                    if (offset == 0x28) continue;
                    fprintf(state_file, "%s[%u,%u]", offset == 0x1C ? "" : ",", offset, U32(base + offset));
                }
                fprintf(state_file, "]}\n");
                fprintf(state_file, "{\"kind\":\"speed\",\"frame\":%u,\"id\":%u,\"factor_bits\":\"", frame, detail_id);
                hex_bytes(object + 0x468, 8);
                fprintf(state_file, "\",\"multiplier_bits\":\"");
                hex_bytes(object + 0x470, 8);
                fprintf(state_file, "\"}\n");
            }
        }
    }
    if (ferror(state_file)) fail("state log write failed");
    fflush(state_file);
}

void ra2_state_math(uint32_t stack, uint32_t caller_frame, uint32_t output, uint32_t source)
{
    (void)output;
    if (!state_file || !detail_id || !detail_locomotive || caller_frame != detail_locomotive) return;
    uint32_t target = U32(stack + 4);
    fprintf(state_file, "{\"kind\":\"arithmetic\",\"frame\":%u,\"id\":%u,\"source\":[%d,%d,%d],\"target\":[%d,%d,%d],\"float_bits\":%u}\n",
        U32(FRAME_ADDRESS), detail_id, I32(source), I32(source + 4), I32(source + 8),
        I32(target), I32(target + 4), I32(target + 8), U32(stack + 8));
}

/* 在原版 __ftol 入口前记录减速补偿的实际操作数；只采样显式指定的单位。 */
void ra2_state_phase(uint32_t caller_stack, uint32_t caller_frame, const void *extended, const double *translated)
{
    if (!state_file || !detail_id || caller_frame != detail_locomotive || !detail_locomotive) return;
    fprintf(state_file, "{\"kind\":\"brake\",\"frame\":%u,\"id\":%u,\"distance\":%d,\"progress_before\":%d,\"value_bits\":\"",
        U32(FRAME_ADDRESS), detail_id, I32(caller_stack + 0x34), I32(caller_stack + 0x3C));
    hex_bytes((uint32_t)(uintptr_t)(extended ? extended : (const void *)translated), extended ? 10 : 8);
    fprintf(state_file, "\",\"format\":%d}\n", extended ? 80 : 64);
}

void ra2_state_speed(uint32_t caller_stack, uint32_t unit, const void *extended, const double *translated)
{
    if (!state_file || !detail_id || U32(unit + 0x10) != detail_id) return;
    fprintf(state_file, "{\"kind\":\"speed_calculation\",\"frame\":%u,\"id\":%u,\"base_speed\":%d,\"factor_bits\":\"",
        U32(FRAME_ADDRESS), detail_id, I32(caller_stack + 8));
    hex_bytes(unit + 0x468, 8);
    fprintf(state_file, "\",\"value_bits\":\"");
    hex_bytes((uint32_t)(uintptr_t)(extended ? extended : (const void *)translated), extended ? 10 : 8);
    fprintf(state_file, "\",\"format\":%d}\n", extended ? 80 : 64);
}

static void submit_order(FrameOrder *order)
{
    uint8_t event[111] = { 0 };
    uint32_t object = find_object(order->id), count = U32(0xA32338), slot = U32(0xA32340);
    int owner;
    if (!object) fail("order object does not exist");
    owner = house_index(U32(object + 0x1B4));
    if (owner < 0 || count >= 128 || slot >= 128) fail("invalid owner or full event queue");
    /* 精确复用 0x004B6170 的 MEGAMISSION 布局及 OutList 的 111 字节环形槽。 */
    event[0] = 4;
    event[2] = (uint8_t)owner;
    memcpy(event + 3, &order->frame, 4);
    memcpy(event + 7, &order->id, 4);
    event[11] = 0x34;
    event[12] = (uint8_t)order->mission;
    if (order->mission == 2)
    {
        uint32_t cell = order->x + 1000 * order->y;
        memcpy(event + 0x13, &cell, 4);
        event[0x17] = 0x0B;
    }
    memcpy((void *)(uintptr_t)(0xA32344 + slot * 111), event, sizeof(event));
    U32(0xA35AC4 + slot * 4) = GetTickCount();
    U32(0xA32340) = (slot + 1) & 127;
    U32(0xA32338) = count + 1;
    order->submitted = 1;
    fprintf(state_file, "{\"kind\":\"submit\",\"frame\":%u,\"id\":%u,\"mission\":%u,\"cell\":[%u,%u]}\n",
        order->frame, order->id, order->mission, order->x, order->y);
    fprintf(stderr, "[state-order] frame=%u id=%u mission=%u cell=%u,%u\n", order->frame, order->id, order->mission, order->x, order->y);
}

void ra2_state_event(uint32_t address)
{
    if (!state_path[0] || !started || !state_file) return;
    if (U8(address) != 4) return;
    uint32_t id = U32(address + 7), mission = U8(address + 12), frame = U32(FRAME_ADDRESS);
    fprintf(state_file, "{\"kind\":\"execute\",\"frame\":%u,\"event_frame\":%u,\"id\":%u,\"mission\":%u}\n",
        frame, U32(address + 3), id, mission);
    for (int i = 0; i < order_count; ++i)
        if (orders[i].submitted && !orders[i].executed && orders[i].frame == U32(address + 3) && orders[i].id == id && orders[i].mission == mission)
        {
            if (frame != orders[i].frame) fail("order executed at a different simulation frame");
            orders[i].executed = 1;
            break;
        }
}

/* 显式启用后才记录；该函数不调用游戏服务、不写游戏内存。 */
void ra2_state_movement_audit(uint32_t stage, uint32_t actor, uint32_t cell, uint32_t object)
{
    if (!movement_audit_enabled || !state_file || !started) return;
    uint32_t caller_drive = actor, observation_frame = stage==19 ? cell : 0;
    if (stage==19) cell=0;
    int32_t x = 0, y = 0, value = 0, auxiliary = 0;
    if (stage == 1)
    {
        int32_t overlay = I32(cell + 0x44);
        if (overlay < 0) return;
        uint32_t type = U32(U32(0xA35DEC) + (uint32_t)overlay * 4);
        if (!U8(type + 0x278)) return;
        value = overlay;
        auxiliary = I32(cell + 0x50);
    }
    else if (stage == 2)
    {
        if (!U8(U32(object + 0x418) + 0x1351)) return;
        value = (int32_t)U32(object + 0x10);
        auxiliary = I32(object + 0x98);
    }
    else if (stage >= 11 && stage <= 23)
    {
        uint32_t drive = actor;
        actor = U32(drive + 0x0C);
        if (!actor) return; /* 寻路服务可能销毁所有者；观测不能再解引用它。 */
        if (stage == 15)
        {
            uint32_t active = U32(actor + 0x564);
            if (active == drive + 4) return;
            value = active ? (int32_t)U32(active) : 0;
            auxiliary = I32(drive + 0x58);
        }
        else if (stage>=16)
        {
            value = stage==16 || stage==19 || stage==20 || stage==21 || stage==23 ? (int32_t)object : stage==17 || stage==22 ? I32(actor+0x4D4) : 0;
            auxiliary = stage==16 || stage==17 || stage==20 || stage==21 ? I32(drive+0x58) : I32(actor+0x4D0);
        }
        else
        {
            value = stage == 11 ? 6 : stage == 12 ? 1 : stage == 13 ? (int32_t)object : I32(drive + 0x58);
            auxiliary = stage == 13 ? U8(drive + 0x64) : stage == 14 ? I32(drive + 0x5C) : I32(actor + 0x4D0);
        }
    }
    else if (stage == 24 || stage == 25 || stage == 26)
    {
        /* 只记录本对象扫描实际测试的两个分类位，不把其它位当作通行状态。 */
        value=(int32_t)U32(object+0x10);auxiliary=U8(object+0x14)&0x05;
    }
    else if (stage == 27)
    {
        auxiliary=U8(object+0x11);
        value=auxiliary ? 0 : I32(0x850EA0+(U32(cell+0xEC)*9u+U32(U32(actor+0x5AC)+0x5A4))*4u);
    }
    else if (stage == 7)
    {
        value = I32(U32(actor + 0x5AC) + 0xB94);
        if (value == -1) return;
        auxiliary = I32(cell + 0xEC);
    }
    else if (stage == 8 || stage == 9)
    {
        actor = U32(actor + 0x0C);
        if (!actor) return;
        value = stage == 8 ? U8(actor + 0x5A1) : (int32_t)object;
        auxiliary = stage == 8 ? I32(actor + 0x560) : I32(cell + 0x44);
    }
    else
    {
        actor = U32(actor + 0x0C);
        if (!actor) return;
        value = stage == 6 ? (int32_t)(object & 255u) : I32(actor + 0x53C);
        auxiliary = stage == 6 ? I32(actor + 0x4D0) : I32(actor + 0x98);
    }
    if (observation_frame)
    {
        x=(int16_t)U16(observation_frame+0x14);
        y=(int16_t)U16(observation_frame+0x16);
    }
    if (cell)
    {
        x = (int16_t)U16(cell + 0x24);
        y = (int16_t)U16(cell + 0x26);
    }
    fprintf(state_file, "{\"kind\":\"movement-audit\",\"frame\":%u,\"stage\":%u,\"id\":%u,"
        "\"cell\":[%d,%d],\"value\":%d,\"auxiliary\":%d", U32(FRAME_ADDRESS), stage, U32(actor + 0x10), x, y, value, auxiliary);
    if (observation_frame)
    {
        fprintf(state_file, ",\"candidate\":[%d,%d,%d],\"next_direction\":%d,\"allow_recursive\":%u",
            I32(observation_frame+0x38),I32(observation_frame+0x3C),I32(observation_frame+0x40),
            I32(actor+0x4D4),U32(observation_frame+0x64));
    }
    if (stage == 27) { fprintf(state_file,",\"land\":%d,\"speed_class\":%d",I32(cell+0xEC),I32(U32(actor+0x5AC)+0x5A4)); }
    if (stage == 6 || stage == 18)
    {
        uint32_t active = U32(actor + 0x564);
        /* 原版重建失败后是否仍有有效行进目标；只读观察，不强行保留目标。 */
        int active_drive = active && U32(active) == 0x7A04CC;
        fprintf(state_file, ",\"active_is_caller\":%s,\"caller_goal_valid\":%s",
            active == caller_drive + 4 ? "true" : "false",
            U32(caller_drive+0x34)!=U32(0x852998) || U32(caller_drive+0x38)!=U32(0x85299C)
                || U32(caller_drive+0x3C)!=U32(0x8529A0) ? "true" : "false");
        int goal_valid = active_drive && (U32(active + 0x30) != U32(0x852998)
            || U32(active + 0x34) != U32(0x85299C) || U32(active + 0x38) != U32(0x8529A0));
        fprintf(state_file, ",\"active_ground_drive\":%s,\"active_goal_valid\":%s",
            active_drive ? "true" : "false", goal_valid ? "true" : "false");
    }
    fputs("}\n", state_file);
}

void ra2_state_tick(void)
{
    uint32_t frame;
    if (!state_path[0]) return;
    frame = U32(FRAME_ADDRESS);
    if (!started && !first_frame) first_frame = frame;
    if (frame < first_frame) return;
    open_trace();
    if ((!started && frame != first_frame) || (started && frame != previous_frame + 1)) fail("simulation boundary skipped or repeated a frame");
    started = 1;
    previous_frame = frame;
    ra2_movement_fixture_tick(frame, state_file, original_mode);
    snapshot(frame);
    if (frame == last_frame)
    {
        for (int i = 0; i < order_count; ++i) if (!orders[i].submitted || !orders[i].executed) fail("order was not submitted and executed");
        fprintf(state_file, "{\"kind\":\"complete\",\"frame\":%u,\"orders\":%d}\n", frame, order_count);
        fflush(state_file);
        fprintf(stderr, "[state-complete] first=%u last=%u orders=%d\n", first_frame, last_frame, order_count);
        fflush(stderr);
        ExitProcess(0);
    }
    for (int i = 0; i < order_count; ++i) if (orders[i].frame == frame) submit_order(&orders[i]);
}

/* 原始机器码探针保全通用寄存器、标志及 x87/SSE 状态，再进入只读快照与显式发令入口。 */
static __declspec(naked) void tick_hook(void)
{
    __asm
    {
        pushfd
        pushad
        fnstcw word ptr [original_cw]
        mov ebp, esp
        sub esp, 528
        and esp, -16
        fxsave [esp]
        call ra2_state_tick
        fxrstor [esp]
        mov esp, ebp
        popad
        popfd
        jmp dword ptr [tick_trampoline]
    }
}

static __declspec(naked) void event_hook(void)
{
    __asm
    {
        pushfd
        pushad
        mov ebp, esp
        sub esp, 528
        and esp, -16
        fxsave [esp]
        push ecx
        call ra2_state_event
        add esp, 4
        fxrstor [esp]
        mov esp, ebp
        popad
        popfd
        jmp dword ptr [event_trampoline]
    }
}

static __declspec(naked) void math_hook(void)
{
    __asm
    {
        pushfd
        pushad
        mov ebp, esp
        sub esp, 528
        and esp, -16
        fxsave [esp]
        push dword ptr [ebp + 20]
        push dword ptr [ebp + 24]
        push dword ptr [ebp + 8]
        lea eax, [ebp + 36]
        push eax
        call ra2_state_math
        add esp, 16
        fxrstor [esp]
        mov esp, ebp
        popad
        popfd
        jmp dword ptr [math_trampoline]
    }
}

static __declspec(naked) void phase_hook(void)
{
    __asm
    {
        pushfd
        pushad
        mov ebp, esp
        sub esp, 528
        and esp, -16
        fxsave [esp]
        mov edx, dword ptr [ebp + 8]
        lea eax, [esp + 32]
        lea ecx, [ebp + 40]
        push 0
        push eax
        push edx
        push ecx
        call ra2_state_phase
        add esp, 16
        fxrstor [esp]
        mov esp, ebp
        popad
        popfd
        jmp dword ptr [phase_ftol]
    }
}

static __declspec(naked) void speed_hook(void)
{
    __asm
    {
        pushfd
        pushad
        mov ebp, esp
        sub esp, 528
        and esp, -16
        fxsave [esp]
        mov edx, dword ptr [ebp + 4]
        lea eax, [esp + 32]
        lea ecx, [ebp + 40]
        push 0
        push eax
        push edx
        push ecx
        call ra2_state_speed
        add esp, 16
        fxrstor [esp]
        mov esp, ebp
        popad
        popfd
        jmp dword ptr [phase_ftol]
    }
}

static __declspec(naked) void wall_audit_hook(void)
{
    __asm
    {
        pushfd
        pushad
        mov ebp, esp
        sub esp, 528
        and esp, -16
        fxsave [esp]
        push 0
        push dword ptr [ebp + 16]
        push dword ptr [ebp + 8]
        push 1
        call ra2_state_movement_audit
        add esp, 16
        fxrstor [esp]
        mov esp, ebp
        popad
        popfd
        jmp dword ptr [wall_trampoline]
    }
}

static __declspec(naked) void gate_audit_hook(void)
{
    __asm
    {
        pushfd
        pushad
        mov ebp, esp
        sub esp, 528
        and esp, -16
        fxsave [esp]
        push dword ptr [ebp + 4]
        push dword ptr [ebp + 16]
        push dword ptr [ebp + 8]
        push 2
        call ra2_state_movement_audit
        add esp, 16
        fxrstor [esp]
        mov esp, ebp
        popad
        popfd
        jmp dword ptr [gate_trampoline]
    }
}

static __declspec(naked) void failure_audit_hook(void)
{
    __asm
    {
        pushfd
        pushad
        mov ebp, esp
        sub esp, 528
        and esp, -16
        fxsave [esp]
        push 0
        push 0
        push dword ptr [ebp + 8]
        push 3
        call ra2_state_movement_audit
        add esp, 16
        fxrstor [esp]
        mov esp, ebp
        popad
        popfd
        jmp dword ptr [failure_trampoline]
    }
}

static __declspec(naked) void retry_result_audit_hook(void)
{
    __asm
    {
        pushfd
        pushad
        mov ebp, esp
        sub esp, 528
        and esp, -16
        fxsave [esp]
        push dword ptr [ebp + 28]
        push 0
        push dword ptr [ebp + 8]
        push 6
        call ra2_state_movement_audit
        add esp, 16
        fxrstor [esp]
        mov esp, ebp
        popad
        popfd
        jmp dword ptr [retry_result_trampoline]
    }
}

static __declspec(naked) void terrain_audit_hook(void)
{
    __asm
    {
        pushfd
        pushad
        mov ebp, esp
        sub esp, 528
        and esp, -16
        fxsave [esp]
        push 0
        push dword ptr [ebp + 16]
        push dword ptr [ebp + 8]
        push 7
        call ra2_state_movement_audit
        add esp, 16
        fxrstor [esp]
        mov esp, ebp
        popad
        popfd
        jmp dword ptr [terrain_trampoline]
    }
}

static __declspec(naked) void clearance_audit_hook(void)
{
    __asm
    {
        pushfd
        pushad
        mov ebp, esp
        sub esp, 528
        and esp, -16
        fxsave [esp]
        mov eax, dword ptr [ebp + 12]
        mov eax, dword ptr [eax + 1Ch]
        push eax
        push dword ptr [ebp + 4]
        push dword ptr [ebp + 8]
        push 9
        call ra2_state_movement_audit
        add esp, 16
        fxrstor [esp]
        mov esp, ebp
        popad
        popfd
        jmp dword ptr [clearance_trampoline]
    }
}

static __declspec(naked) void traffic_audit_hook(void)
{
    __asm
    {
        pushfd
        pushad
        mov ebp, esp
        sub esp, 528
        and esp, -16
        fxsave [esp]
        push 0
        push 0
        push dword ptr [ebp + 8]
        push 8
        call ra2_state_movement_audit
        add esp, 16
        fxrstor [esp]
        mov esp, ebp
        popad
        popfd
        jmp dword ptr [traffic_trampoline]
    }
}

static __declspec(naked) void special_temporary_audit_hook(void)
{
    __asm
    {
        pushfd
        pushad
        mov ebp, esp
        sub esp, 528
        and esp, -16
        fxsave [esp]
        push 0
        push 0
        push dword ptr [ebp + 8]
        push 11
        call ra2_state_movement_audit
        add esp, 16
        fxrstor [esp]
        mov esp, ebp
        popad
        popfd
        jmp dword ptr [special_temporary_trampoline]
    }
}

static __declspec(naked) void special_cloaked_audit_hook(void)
{
    __asm
    {
        pushfd
        pushad
        mov ebp, esp
        sub esp, 528
        and esp, -16
        fxsave [esp]
        push 0
        push 0
        push dword ptr [ebp + 8]
        push 12
        call ra2_state_movement_audit
        add esp, 16
        fxrstor [esp]
        mov esp, ebp
        popad
        popfd
        jmp dword ptr [special_cloaked_trampoline]
    }
}

static __declspec(naked) void template_select_audit_hook(void)
{
    __asm
    {
        pushfd
        pushad
        mov ebp, esp
        sub esp, 528
        and esp, -16
        fxsave [esp]
        mov eax, dword ptr [ebp + 4]
        mov edx, dword ptr [ebp + 16]
        lea eax, [eax + edx*8]
        push eax
        push 0
        push dword ptr [ebp + 8]
        push 13
        call ra2_state_movement_audit
        add esp, 16
        fxrstor [esp]
        mov esp, ebp
        popad
        popfd
        jmp dword ptr [template_select_trampoline]
    }
}

static __declspec(naked) void template_commit_audit_hook(void)
{
    __asm
    {
        pushfd
        pushad
        mov ebp, esp
        sub esp, 528
        and esp, -16
        fxsave [esp]
        push 0
        push 0
        push dword ptr [ebp + 8]
        push 14
        call ra2_state_movement_audit
        add esp, 16
        fxrstor [esp]
        mov esp, ebp
        popad
        popfd
        jmp dword ptr [template_commit_trampoline]
    }
}

static __declspec(naked) void prepare_identity_audit_hook(void)
{
    __asm
    {
        pushfd
        pushad
        mov ebp, esp
        sub esp, 528
        and esp, -16
        fxsave [esp]
        push 0
        push 0
        push dword ptr [ebp + 24]
        push 15
        call ra2_state_movement_audit
        add esp, 16
        fxrstor [esp]
        mov esp, ebp
        popad
        popfd
        jmp dword ptr [prepare_identity_trampoline]
    }
}

static __declspec(naked) void speed_prepare_audit_hook(void)
{
    __asm
    {
        pushfd
        pushad
        mov ebp, esp
        sub esp, 528
        and esp, -16
        fxsave [esp]
        push dword ptr [ebp + 4]
        push 0
        push dword ptr [ebp + 8]
        push 16
        call ra2_state_movement_audit
        add esp, 16
        fxrstor [esp]
        mov esp, ebp
        popad
        popfd
        jmp dword ptr [speed_prepare_trampoline]
    }
}

static __declspec(naked) void followup_prepare_audit_hook(void)
{
    __asm
    {
        pushfd
        pushad
        mov ebp, esp
        sub esp, 528
        and esp, -16
        fxsave [esp]
        push 0
        push 0
        push dword ptr [ebp + 8]
        push 17
        call ra2_state_movement_audit
        add esp, 16
        fxrstor [esp]
        mov esp, ebp
        popad
        popfd
        jmp dword ptr [followup_prepare_trampoline]
    }
}

static __declspec(naked) void followup_failure_audit_hook(void)
{
    __asm
    {
        pushfd
        pushad
        mov ebp, esp
        sub esp, 528
        and esp, -16
        fxsave [esp]
        push 0
        push 0
        push dword ptr [ebp + 8]
        push 18
        call ra2_state_movement_audit
        add esp, 16
        fxrstor [esp]
        mov esp, ebp
        popad
        popfd
        jmp dword ptr [followup_failure_trampoline]
    }
}

static __declspec(naked) void continuation_classified_audit_hook(void)
{
    __asm
    {
        pushfd
        pushad
        mov ebp,esp
        sub esp,528
        and esp,-16
        fxsave [esp]
        push dword ptr [ebp + 28]
        push 0
        push dword ptr [ebp + 8]
        push 21
        call ra2_state_movement_audit
        add esp,16
        fxrstor [esp]
        mov esp,ebp
        popad
        popfd
        jmp dword ptr [continuation_classified_trampoline]
    }
}

static __declspec(naked) void followup_candidate_audit_hook(void)
{
    __asm
    {
        pushfd
        pushad
        mov ebp,esp
        sub esp,528
        and esp,-16
        fxsave [esp]
        push 0
        push 0
        push dword ptr [ebp + 8]
        push 22
        call ra2_state_movement_audit
        add esp,16
        fxrstor [esp]
        mov esp,ebp
        popad
        popfd
        jmp dword ptr [followup_candidate_trampoline]
    }
}

static __declspec(naked) void followup_search_audit_hook(void)
{
    __asm
    {
        pushfd
        pushad
        mov ebp,esp
        sub esp,528
        and esp,-16
        fxsave [esp]
        push dword ptr [ebp + 28]
        push 0
        push dword ptr [ebp + 8]
        push 23
        call ra2_state_movement_audit
        add esp,16
        fxrstor [esp]
        mov esp,ebp
        popad
        popfd
        jmp dword ptr [followup_search_trampoline]
    }
}


void ra2_path_diag(uint32_t stage,uint32_t frame,uint32_t context,uint32_t value)
{
    uint32_t node,cell,parent,index;
    if (!movement_audit_enabled || !state_file || !started || U32(FRAME_ADDRESS)!=52) return;
    if(stage==1) {
        cell=value; node=U32(frame+0x14);
        index=(uint32_t)(int32_t)(int16_t)U16(cell+0x24)+(uint32_t)(int32_t)(int16_t)U16(cell+0x26)*U32(0x84E804);
        fprintf(state_file,"{\"kind\":\"path-detail\",\"stage\":1,\"cell\":[%d,%d],\"dir\":%u,\"g\":%u,\"f\":%u,\"cache\":[%u,%u],\"mark\":[%u,%u],\"epoch\":%u}\n",
            (int16_t)U16(cell+0x24),(int16_t)U16(cell+0x26),U32(frame+0x18),U32(node+4),U32(node+8),
            U32(U32(context+0x20)+index*4),U32(U32(context+0x24)+index*4),
            U32(U32(context+0x18)+index*4),U32(U32(context+0x1c)+index*4),U32(context+0x28));
    } else {
        node=value; cell=U32(U32(U32(node))); parent=U32(frame+0x14);
        fprintf(state_file,"{\"kind\":\"path-detail\",\"stage\":2,\"cell\":[%d,%d],\"dir\":%u,\"g\":%u,\"f\":%u,\"edge\":%u,\"parent_g\":%u}\n",
            (int16_t)U16(cell+0x24),(int16_t)U16(cell+0x26),U32(frame+0x18),U32(node+4),U32(node+8),U32(frame+0x34),U32(parent+4));
    }
}
static void *path_candidate_diag_trampoline;
static __declspec(naked) void path_candidate_diag_hook(void)
{
    __asm
    {
        pushfd
        pushad
        mov ebp,esp
        sub esp,528
        and esp,-16
        fxsave [esp]
        push dword ptr [ebp + 16]
        push dword ptr [ebp + 4]
        lea eax,[ebp + 36]
        push eax
        push 1
        call ra2_path_diag
        add esp,16
        fxrstor [esp]
        mov esp,ebp
        popad
        popfd
        jmp dword ptr [path_candidate_diag_trampoline]
    }
}

static void *path_score_diag_trampoline;
static __declspec(naked) void path_score_diag_hook(void)
{
    __asm
    {
        pushfd
        pushad
        mov ebp,esp
        sub esp,528
        and esp,-16
        fxsave [esp]
        push dword ptr [ebp + 28]
        push dword ptr [ebp + 4]
        lea eax,[ebp + 36]
        push eax
        push 2
        call ra2_path_diag
        add esp,16
        fxrstor [esp]
        mov esp,ebp
        popad
        popfd
        jmp dword ptr [path_score_diag_trampoline]
    }
}

static __declspec(naked) void object_filter_audit_hook(void)
{
    __asm
    {
        pushfd
        pushad
        mov ebp,esp
        sub esp,528
        and esp,-16
        fxsave [esp]
        push dword ptr [ebp + 4]
        push dword ptr [ebp + 16]
        push dword ptr [ebp + 8]
        push 24
        call ra2_state_movement_audit
        add esp,16
        fxrstor [esp]
        mov esp,ebp
        popad
        popfd
        jmp dword ptr [object_filter_trampoline]
    }
}

static uint32_t allied_entry_trampoline;
static __declspec(naked) void allied_entry_audit_hook(void)
{
    __asm
    {
        pushfd
        pushad
        mov ebp,esp
        sub esp,528
        and esp,-16
        fxsave [esp]
        push dword ptr [ebp + 4]
        push dword ptr [ebp + 16]
        push dword ptr [ebp + 8]
        push 25
        call ra2_state_movement_audit
        add esp,16
        fxrstor [esp]
        mov esp,ebp
        popad
        popfd
        jmp dword ptr [allied_entry_trampoline]
    }
}

static uint32_t allied_geometry_trampoline;
static __declspec(naked) void allied_geometry_audit_hook(void)
{
    __asm
    {
        pushfd
        pushad
        mov ebp,esp
        sub esp,528
        and esp,-16
        fxsave [esp]
        push dword ptr [ebp + 4]
        push dword ptr [ebp + 160]
        push dword ptr [ebp + 56]
        push 26
        call ra2_state_movement_audit
        add esp,16
        fxrstor [esp]
        mov esp,ebp
        popad
        popfd
        jmp dword ptr [allied_geometry_trampoline]
    }
}

static uint32_t terrain_tail_trampoline;
static __declspec(naked) void terrain_tail_audit_hook(void)
{
    __asm
    {
        pushfd
        pushad
        mov ebp,esp
        sub esp,528
        and esp,-16
        fxsave [esp]
        lea eax,[ebp + 36]
        push eax
        push dword ptr [ebp + 16]
        push dword ptr [ebp + 8]
        push 27
        call ra2_state_movement_audit
        add esp,16
        fxrstor [esp]
        mov esp,ebp
        popad
        popfd
        jmp dword ptr [terrain_tail_trampoline]
    }
}

static __declspec(naked) void advance_sample_audit_hook(void)
{
    __asm
    {
        pushfd
        pushad
        mov ebp, esp
        sub esp, 528
        and esp, -16
        fxsave [esp]
        mov eax, dword ptr [ebp + 8]
        push dword ptr [eax + 5Ch]
        push 0
        push eax
        push 20
        call ra2_state_movement_audit
        add esp, 16
        fxrstor [esp]
        mov esp, ebp
        popad
        popfd
        jmp dword ptr [advance_sample_trampoline]
    }
}

static __declspec(naked) void turn_classified_audit_hook(void)
{
    __asm
    {
        pushfd
        pushad
        mov ebp, esp
        sub esp, 528
        and esp, -16
        fxsave [esp]
        push dword ptr [ebp + 4]
        mov eax, dword ptr [ebp + 12]
        add eax, 4
        push eax
        push dword ptr [ebp + 8]
        push 19
        call ra2_state_movement_audit
        add esp, 16
        fxrstor [esp]
        mov esp, ebp
        popad
        popfd
        jmp dword ptr [turn_classified_trampoline]
    }
}

static void install_hook(uint32_t address, const uint8_t *expected, size_t length, void (*hook)(void), void **trampoline)
{
    uint8_t *at = (uint8_t *)(uintptr_t)address;
    DWORD old;
    if (memcmp(at, expected, length)) fail("original hook instruction signature mismatch");
    *trampoline = VirtualAlloc(NULL, length + 5, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);
    if (!*trampoline) fail("cannot allocate original trampoline");
    memcpy(*trampoline, at, length);
    uint8_t *back = (uint8_t *)*trampoline + length;
    back[0] = 0xE9;
    *(int32_t *)(back + 1) = (int32_t)((uintptr_t)(at + length) - (uintptr_t)(back + 5));
    if (!VirtualProtect(at, length, PAGE_EXECUTE_READWRITE, &old)) fail("cannot protect original hook");
    at[0] = 0xE9;
    *(int32_t *)(at + 1) = (int32_t)((uintptr_t)hook - (uintptr_t)(at + 5));
    memset(at + 5, 0x90, length - 5);
    FlushInstructionCache(GetCurrentProcess(), at, length);
    FlushInstructionCache(GetCurrentProcess(), *trampoline, length + 5);
}

void ra2_state_install_original(uint32_t base)
{
    static const uint8_t tick_bytes[] = { 0x83, 0xEC, 0x28, 0x8B, 0x15, 0x18, 0xEB, 0xA6, 0x00 };
    static const uint8_t event_bytes[] = { 0x81, 0xEC, 0x70, 0x03, 0x00, 0x00 };
    static const uint8_t math_bytes[] = { 0x83, 0xEC, 0x0C, 0xD9, 0x44, 0x24, 0x14 };
    if (!state_path[0]) return;
    original_mode = 1;
    if (base != 0x00400000) fail("unsupported image base");
    install_hook(0x0053D890, tick_bytes, sizeof(tick_bytes), tick_hook, &tick_trampoline);
    install_hook(0x004B65C0, event_bytes, sizeof(event_bytes), event_hook, &event_trampoline);
    if (movement_audit_enabled)
    {
        /* 仅搬移完整且不含相对转移的指令；分类处是原版绝对地址间接跳转。 */
        static const uint8_t continuation_classified_bytes[] = {0xFF,0x24,0x85,0x4C,0x26,0x4A,0x00};
        install_hook(0x4A1CA8,continuation_classified_bytes,sizeof(continuation_classified_bytes),continuation_classified_audit_hook,&continuation_classified_trampoline);
        static const uint8_t followup_candidate_bytes[] = {0x8B,0x4D,0x0C,0x8B,0xB1,0xD4,0x04,0x00,0x00};
        install_hook(0x4A3E79,followup_candidate_bytes,sizeof(followup_candidate_bytes),followup_candidate_audit_hook,&followup_candidate_trampoline);
        static const uint8_t followup_search_bytes[] = {0x8B,0x4D,0x0C,0x8B,0x11};
        install_hook(0x4A3EFB,followup_search_bytes,sizeof(followup_search_bytes),followup_search_audit_hook,&followup_search_trampoline);
        static const unsigned char path_candidate_diag_bytes[]={0x8B,0x44,0x24,0x18,0x8D,0x4B,0x24};
        static const unsigned char path_score_diag_bytes[]={0x8B,0xD8,0x8B,0x44,0x24,0x1C};
        install_hook(0x427704,path_candidate_diag_bytes,sizeof(path_candidate_diag_bytes),path_candidate_diag_hook,&path_candidate_diag_trampoline);
        install_hook(0x427912,path_score_diag_bytes,sizeof(path_score_diag_bytes),path_score_diag_hook,&path_score_diag_trampoline);
        static const unsigned char allied_entry_bytes[]={0x8B,0x55,0x00,0x8B,0xCD};
        install_hook(0x703693,allied_entry_bytes,sizeof(allied_entry_bytes),allied_entry_audit_hook,&allied_entry_trampoline);
        static const unsigned char allied_geometry_bytes[]={0x8B,0x5C,0x24,0x14,0x8D,0x54,0x24,0x34};
        install_hook(0x703748,allied_geometry_bytes,sizeof(allied_geometry_bytes),allied_geometry_audit_hook,&allied_geometry_trampoline);
        static const unsigned char terrain_tail_bytes[]={0x8A,0x44,0x24,0x11,0x84,0xC0};
        install_hook(0x703905,terrain_tail_bytes,sizeof(terrain_tail_bytes),terrain_tail_audit_hook,&terrain_tail_trampoline);
        static const uint8_t object_filter_bytes[]={0x8B,0x85,0x88,0x05,0x00,0x00};
        install_hook(0x703473,object_filter_bytes,sizeof(object_filter_bytes),object_filter_audit_hook,&object_filter_trampoline);
        static const uint8_t advance_sample_bytes[] = { 0x8b,0x4d,0xc,0x8b,0x11 };
        install_hook(0x4A16A6, advance_sample_bytes, sizeof(advance_sample_bytes), advance_sample_audit_hook, &advance_sample_trampoline);
        static const uint8_t speed_prepare_bytes[] = { 0x8b,0x4d,0xc,0x8b,0x11 };
        install_hook(0x4A3C9B, speed_prepare_bytes, sizeof(speed_prepare_bytes), speed_prepare_audit_hook, &speed_prepare_trampoline);
        static const uint8_t followup_prepare_bytes[] = { 0x8b,0x44,0x24,0x38,0x8b,0x4d,0xc };
        install_hook(0x4A3E35, followup_prepare_bytes, sizeof(followup_prepare_bytes), followup_prepare_audit_hook, &followup_prepare_trampoline);
        static const uint8_t followup_failure_bytes[] = { 0x8b,0x4d,0xc,0x85,0xc9 };
        install_hook(0x4A3F4E, followup_failure_bytes, sizeof(followup_failure_bytes), followup_failure_audit_hook, &followup_failure_trampoline);
        static const uint8_t turn_classified_bytes[] = { 0x8b,0x4d,0xc,0x8a,0x41,0x7d };
        install_hook(0x4A413D, turn_classified_bytes, sizeof(turn_classified_bytes), turn_classified_audit_hook, &turn_classified_trampoline);
        static const uint8_t special_temporary_bytes[] = { 0x8b,0x4d,0xc,0x8b,0x1 };
        install_hook(0x4A36F6, special_temporary_bytes, sizeof(special_temporary_bytes), special_temporary_audit_hook, &special_temporary_trampoline);
        static const uint8_t special_cloaked_bytes[] = { 0x8d,0x4c,0x24,0x14,0x51 };
        install_hook(0x4A3944, special_cloaked_bytes, sizeof(special_cloaked_bytes), special_cloaked_audit_hook, &special_cloaked_trampoline);
        static const uint8_t template_select_bytes[] = { 0x8d,0x4,0xde,0xc6,0x45,0x60,0x0 };
        install_hook(0x4A3FE3, template_select_bytes, sizeof(template_select_bytes), template_select_audit_hook, &template_select_trampoline);
        static const uint8_t template_commit_bytes[] = { 0x8b,0x55,0xc,0x52,0x50 };
        install_hook(0x4A469E, template_commit_bytes, sizeof(template_commit_bytes), template_commit_audit_hook, &template_commit_trampoline);
        static const uint8_t prepare_identity_bytes[] = { 0x83,0xec,0x4c,0x53,0x55 };
        install_hook(0x4A2670, prepare_identity_bytes, sizeof(prepare_identity_bytes), prepare_identity_audit_hook, &prepare_identity_trampoline);
        static const uint8_t terrain_bytes[] = { 0x8B,0x81,0x94,0x0B,0,0 };
        static const uint8_t clearance_bytes[] = { 0x8B,0x46,0x44,0x8B,0x4C,0x24,0x18 };
        static const uint8_t traffic_bytes[] = { 0x8B,0x45,0x0C,0x8A,0x88,0xA1,0x05,0,0 };
        install_hook(0x7030B6, terrain_bytes, sizeof(terrain_bytes), terrain_audit_hook, &terrain_trampoline);
        install_hook(0x4A3550, clearance_bytes, sizeof(clearance_bytes), clearance_audit_hook, &clearance_trampoline);
        install_hook(0x4A364F, traffic_bytes, sizeof(traffic_bytes), traffic_audit_hook, &traffic_trampoline);
        static const uint8_t wall_bytes[] = { 0x8B, 0x43, 0x44, 0x83, 0xF8, 0xFF };
        static const uint8_t gate_bytes[] = { 0x8B, 0x86, 0x18, 0x04, 0x00, 0x00 };
        static const uint8_t failure_bytes[] = { 0x8B, 0x4D, 0x0C, 0x8B, 0x81, 0x3C, 0x05, 0x00, 0x00 };
        install_hook(0x703331, wall_bytes, sizeof(wall_bytes), wall_audit_hook, &wall_trampoline);
        install_hook(0x703536, gate_bytes, sizeof(gate_bytes), gate_audit_hook, &gate_trampoline);
        install_hook(0x4A2DFD, failure_bytes, sizeof(failure_bytes), failure_audit_hook, &failure_trampoline);
        static const uint8_t retry_bytes[] = { 0x8B, 0x4D, 0x0C, 0x84, 0xC0 };
        install_hook(0x4A28E7, retry_bytes, sizeof(retry_bytes), retry_result_audit_hook, &retry_result_trampoline);
    }
    if (detail_id) install_hook(0x007220C0, math_bytes, sizeof(math_bytes), math_hook, &math_trampoline);
    if (detail_id)
    {
        uint8_t *call = (uint8_t *)(uintptr_t)0x004A202B;
        static const uint8_t expected[] = { 0xE8, 0xE0, 0xD0, 0x2D, 0x00 };
        if (memcmp(call, expected, sizeof(expected))) fail("brake call signature mismatch");
        *(int32_t *)(call + 1) = (int32_t)((uintptr_t)phase_hook - (uintptr_t)(call + 5));
        FlushInstructionCache(GetCurrentProcess(), call, 5);
        call = (uint8_t *)(uintptr_t)0x004C9B83;
        static const uint8_t speed_bytes[] = { 0xE8, 0x88, 0x55, 0x2B, 0x00 };
        if (memcmp(call, speed_bytes, sizeof(speed_bytes))) fail("speed call signature mismatch");
        *(int32_t *)(call + 1) = (int32_t)((uintptr_t)speed_hook - (uintptr_t)(call + 5));
        FlushInstructionCache(GetCurrentProcess(), call, 5);
    }
}
