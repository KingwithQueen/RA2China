extern void __cdecl ra2_internal_observe(unsigned drive,unsigned unit,unsigned stage,int x,int y);
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "recomp_types.h"
#include "ground_prepare.h"
#include "ground_obstacle.h"
#include "ground_segment.h"
#include "ground_wait.h"
#include "ground_reaction.h"
#include "ground_special.h"
#include "ground_template.h"
#include "ground_prepare_bridge.h"
#include "state_trace.h"

typedef struct PrepareContext
{
    uint32_t drive;
    uint32_t frame;
    uint32_t obstacle_cell;
    Ra2GroundPrepareState state;
} PrepareContext;

static Ra2WorldPoint read_point(uint32_t address)
{
    Ra2WorldPoint point;
    memcpy(&point, (const void *)(uintptr_t)ADDR(address), sizeof(point));
    return point;
}

static void write_point(uint32_t address, Ra2WorldPoint point)
{
    memcpy((void *)(uintptr_t)ADDR(address), &point, sizeof(point));
}

static void read_state(PrepareContext *context)
{
    context->state.destination = read_point(context->drive + 0x34);
    context->state.segment_end = read_point(context->drive + 0x40);
    context->state.driving = MEM8(context->drive + 0x63);
    context->state.legacy_flag_61 = MEM8(context->drive + 0x61);
}

static void write_state(PrepareContext *context)
{
    write_point(context->drive + 0x34, context->state.destination);
    write_point(context->drive + 0x40, context->state.segment_end);
    MEM8(context->drive + 0x63) = (uint8_t)context->state.driving;
    MEM8(context->drive + 0x61) = (uint8_t)context->state.legacy_flag_61;
}

static uint32_t owner_address(PrepareContext *context)
{
    return MEM32(context->drive + 0x0C);
}

static uint32_t engine_call(PrepareContext *context, uint32_t target, uint32_t object, const uint32_t *arguments, unsigned count)
{
    uint32_t stack = g_esp, caller = g_cur_func;
    write_state(context);
    for (unsigned i = count; i; --i)
    {
        g_esp -= 4;
        MEM32(g_esp) = arguments[i - 1];
    }
    g_esp -= 4;
    MEM32(g_esp) = RECOMP_RETADDR;
    g_ecx = object;
    recomp_func_t function = recomp_lookup_manual(target);
    if (!function)
    {
        function = recomp_lookup(target);
    }
    if (!function)
    {
        function = recomp_lookup_import(target);
    }
    if (!function)
    {
        fprintf(stderr, "[prepare-bridge-error] unresolved operation %08X\n", target);
        abort();
    }
    function();
    if (g_esp != stack)
    {
        fprintf(stderr, "[prepare-bridge-error] unbalanced operation %08X\n", target);
        abort();
    }
    g_cur_func = caller;
    uint32_t result = g_eax;
    read_state(context);
    return result;
}

static uint32_t owner_call(PrepareContext *context, uint32_t slot, const uint32_t *arguments, unsigned count)
{
    uint32_t owner = owner_address(context);
    return engine_call(context, MEM32(MEM32(owner) + slot), owner, arguments, count);
}

static int32_t prepare_query(void *opaque, Ra2PrepareQuery query)
{
    PrepareContext *context = opaque;
    uint32_t owner = owner_address(context), target, argument, result;
    uint32_t scratch = context->frame - 0x80;
    write_state(context);
    switch (query)
    {
        case RA2_PREPARE_EFFECTIVE_MISSION: return (int32_t)owner_call(context, 0x16C, NULL, 0);
        case RA2_PREPARE_OWNER_VIRTUAL_1BC: return (owner_call(context, 0x1BC, NULL, 0) & 255u) != 0;
        case RA2_PREPARE_OWNER_VIRTUAL_1C0: return (owner_call(context, 0x1C0, NULL, 0) & 255u) != 0;
        case RA2_PREPARE_TEAM_BUSY:
            target = MEM32(owner + 0x238);
            return target && engine_call(context, 0x68A680, target, NULL, 0) != 0;
        case RA2_PREPARE_OWNER_VIRTUAL_324: return (owner_call(context, 0x324, NULL, 0) & 255u) != 0;
        case RA2_PREPARE_OWNER_VIRTUAL_328: return (owner_call(context, 0x328, NULL, 0) & 255u) != 0;
        case RA2_PREPARE_TARGET_CATEGORY:
            target = MEM32(owner + 0x494);
            return target ? (int32_t)engine_call(context, MEM32(MEM32(target) + 0x2C), target, NULL, 0) : -1;
        case RA2_PREPARE_DISTANCE_TO_DESTINATION:
        {
            argument = scratch;
            result = owner_call(context, 0x48, &argument, 1);
            Ra2WorldPoint position = read_point(result);
            /* 原版先构造 32 位回绕差向量，再交给原版长度函数；数值算法在本批保持原实现。 */
            uint32_t components[3] = { (uint32_t)position.x - (uint32_t)context->state.destination.x,
                (uint32_t)position.y - (uint32_t)context->state.destination.y,
                (uint32_t)position.z - (uint32_t)context->state.destination.z };
            result = engine_call(context, 0x41B630, scratch + 32, components, 3);
            return (int32_t)engine_call(context, 0x41B780, result, NULL, 0);
        }
        case RA2_PREPARE_PATH_HEAD: return (int32_t)MEM32(owner + 0x4D0);
        case RA2_PREPARE_RETRY_DELAY_FRAMES:
        {
            double factor;
            memcpy(&factor, (const void *)(uintptr_t)ADDR(MEM32(0x839848) + 0x13C8), sizeof(factor));
            /* 本机原版常量 0x79B608 为 900；__ftol 随后永久切换控制字。 */
            int32_t delay = ra2_ground_scale_speed(900, factor, g_fpu_cw);
            g_fpu_cw = MEM16(0x7D8964);
            return delay;
        }
        case RA2_PREPARE_OWNER_EXISTS: return owner != 0;
        case RA2_PREPARE_DESTINATION_ACCEPTED:
            argument = context->drive + 0x34;
            return (owner_call(context, 0x2AC, &argument, 1) & 255u) != 0;
        case RA2_PREPARE_OWNER_PREDICATE_4C8D60:
            return (engine_call(context, 0x4C8D60, owner, NULL, 0) & 255u) != 0;
        case RA2_PREPARE_CLOSE_ENOUGH_DISTANCE: return (int32_t)MEM32(MEM32(0x839848) + 0x1380);
        case RA2_PREPARE_HAS_TARGET_488: return MEM32(owner + 0x488) != 0;
        case RA2_PREPARE_OWNER_ALIVE: return MEM8(owner + 0x7D) != 0;
        default:
            fputs("[prepare-bridge-error] invalid query\n", stderr);
            abort();
    }
}

static void trim_path(void *opaque, int32_t end_index)
{
    PrepareContext *context = opaque;
    /* 不在纯 C 核心里对负索引做数组访问；此处保留原版 guest 地址的 32 位算术。 */
    MEM32(owner_address(context) + 0x4D0 + (uint32_t)end_index * 4u) = UINT32_MAX;
}

static int stop_navigation(void *opaque, int target_variant)
{
    PrepareContext *context = opaque;
    uint32_t arguments[2] = { 0, 1 };
    return (int)(owner_call(context, target_variant ? 0x414 : 0x410, arguments, 2) & 255u);
}

static void write_aborted(void *opaque, unsigned aborted)
{
    PrepareContext *context = opaque;
    MEM8(MEM32(context->frame + 0x60)) = (uint8_t)aborted;
}

static void restart_retry_timer(void *opaque, int32_t frame, int32_t duration)
{
    PrepareContext *context = opaque;
    uint32_t owner = owner_address(context);
    MEM32(owner + 0x530) = (uint32_t)frame;
    MEM32(owner + 0x534) = MEM32(context->frame + 0x48);
    MEM32(owner + 0x538) = (uint32_t)duration;
}

static int rebuild_path(void *opaque)
{
    PrepareContext *context = opaque;
    uint32_t cell = (uint16_t)(context->state.destination.x / 256)
        | ((uint32_t)(uint16_t)(context->state.destination.y / 256) << 16);
    uint32_t arguments[3] = { cell, 0, 0 };
    uint32_t result = engine_call(context, 0x4C3000, owner_address(context), arguments, 3);
    ra2_state_movement_audit(6, context->drive, 0, result);
    return (result & 255u) != 0;
}

static void cancel_target(void *opaque)
{
    PrepareContext *context = opaque;
    engine_call(context, 0x4CD9B0, owner_address(context), NULL, 0);
}

static Ra2PrepareServices services_for(PrepareContext *context)
{
    Ra2PrepareServices services = { context, prepare_query, trim_path, stop_navigation, write_aborted,
        restart_retry_timer, rebuild_path, cancel_target };
    return services;
}

static uint32_t finish(PrepareContext *context, Ra2PreparePhase phase, int32_t cached_path_head)
{
    write_state(context);
    g_ebp = context->drive;
    g_esp = context->frame;
    g_edi = context->drive + 0x34;
    switch (phase)
    {
        case RA2_PREPARE_RETRY_PATH: g_ebx = (uint32_t)cached_path_head; return 0x4A285E;
        case RA2_PREPARE_USE_QUEUED_PATH: g_ebx = (uint32_t)cached_path_head; return 0x4A32CA;
        case RA2_PREPARE_PATH_REBUILT: g_ecx = owner_address(context); return 0x4A2F7A;
        case RA2_PREPARE_INSPECT_OBSTACLE: return 0x4A2A83;
        case RA2_PREPARE_FINISH_FAILED_ATTEMPT: return 0x4A2EAC;
        default: break;
    }
    g_eax = (g_eax & 0xFFFFFF00u) | (phase == RA2_PREPARE_RETURN_TRUE);
    g_edi = MEM32(context->frame);
    g_esi = MEM32(context->frame + 4);
    g_ebp = MEM32(context->frame + 8);
    g_ebx = MEM32(context->frame + 12);
    g_flag_k = FK_ADD;
    g_flag_a = context->frame + 16;
    g_flag_b = 0x4C;
    g_flag_cf = context->frame + 0x5C < context->frame + 16;
    g_esp = context->frame + 0x6C;
    return 0;
}

uint32_t ra2_ground_prepare_entry_bridge(void)
{
    ra2_state_movement_audit(15,g_ebp,0,0);
    PrepareContext context = { 0 };
    context.drive = g_ebp;
    context.frame = g_esp;
    int32_t path_head = (int32_t)g_ebx;
    int is_moving = (g_eax & 255u) != 0;
    read_state(&context);
    g_esp -= 0x200;
    Ra2PrepareServices services = services_for(&context);
    Ra2PreparePhase phase = ra2_ground_prepare_entry(&context.state, read_point(0x852998), is_moving, &path_head, &services);
    return finish(&context, phase, path_head);
}

uint32_t ra2_ground_retry_path_bridge(void)
{
    PrepareContext context = { 0 };
    context.drive = g_ebp;
    context.frame = g_esp;
    read_state(&context);
    uint32_t owner = owner_address(&context);
    Ra2PathRetryTimer timer = { (int32_t)MEM32(owner + 0x530), (int32_t)MEM32(owner + 0x538) };
    int32_t frame = (int32_t)MEM32(0xA40D2C);
    g_esp -= 0x200;
    Ra2PrepareServices services = services_for(&context);
    Ra2PreparePhase phase = ra2_ground_retry_path(&context.state, read_point(0x852998), timer, frame, &services);
    return finish(&context, phase, -1);
}

static int32_t obstacle_query(void *opaque, Ra2ObstacleQuery query)
{
    PrepareContext *context = opaque;
    uint32_t owner = owner_address(context), argument, result, scratch = context->frame - 0x80;
    switch (query)
    {
        case RA2_OBSTACLE_PATH_HEAD: return (int32_t)MEM32(owner + 0x4D0);
        case RA2_OBSTACLE_FACING_DIRECTION:
            argument = scratch;
            result = engine_call(context, 0x4B8BE0, owner + 0x2E0, &argument, 1);
            return (int32_t)(((MEM32(result) >> 12) + 1u) >> 1) & 7;
        case RA2_OBSTACLE_TRAIN:
            result = owner_call(context, 0x80, NULL, 0);
            return MEM8(result + 0xAA0) != 0;
        case RA2_OBSTACLE_DISTANCE_TO_DESTINATION:
            return prepare_query(context, RA2_PREPARE_DISTANCE_TO_DESTINATION);
        case RA2_OBSTACLE_CLOSE_ENOUGH_DISTANCE:
            return prepare_query(context, RA2_PREPARE_CLOSE_ENOUGH_DISTANCE);
        case RA2_OBSTACLE_PREDICATE_636F10:
            return (engine_call(context, 0x636F10, owner, NULL, 0) & 255u) != 0;
        case RA2_OBSTACLE_HEIGHT_PER_LEVEL: return (int32_t)MEM32(0x8529D0);
        case RA2_OBSTACLE_CURRENT_LAND:
        {
            Ra2WorldPoint position = read_point(owner + 0x88);
            write_point(scratch, position);
            argument = scratch;
            result = engine_call(context, 0x548000, 0x8324E0, &argument, 1);
            return (int32_t)MEM32(result + 0xEC);
        }
        case RA2_OBSTACLE_CELL_HAS_BRIDGE: return (MEM32(context->obstacle_cell + 0x140) & 0x100) != 0;
        case RA2_OBSTACLE_CELL_LEVEL: return (int8_t)MEM8(context->obstacle_cell + 0x11B);
        case RA2_OBSTACLE_HAS_TARGET_488: return MEM32(owner + 0x488) != 0;
        default: abort();
    }
}

static Ra2WorldPoint obstacle_position(void *opaque, int virtual_position)
{
    PrepareContext *context = opaque;
    uint32_t argument = context->frame - 0x80;
    return read_point(virtual_position ? owner_call(context, 0x48, &argument, 1) : owner_address(context) + 0x88);
}

static Ra2GroundCell obstacle_neighbor(void *opaque, Ra2GroundCell cell, unsigned direction)
{
    (void)opaque;
    uint32_t delta = 0x851A70 + direction * 4;
    cell.x = (int16_t)((uint16_t)cell.x + MEM16(delta));
    cell.y = (int16_t)((uint16_t)cell.y + MEM16(delta + 2));
    return cell;
}

static uint32_t cell_argument(PrepareContext *context, Ra2GroundCell cell)
{
    uint32_t scratch = context->frame - 0x80;
    memcpy((void *)(uintptr_t)ADDR(scratch), &cell, sizeof(cell));
    return scratch;
}

static int obstacle_inside_map(void *opaque, Ra2GroundCell cell)
{
    PrepareContext *context = opaque;
    uint32_t arguments[2] = { cell_argument(context, cell), 1 };
    return (engine_call(context, 0x55A660, 0x8324E0, arguments, 2) & 255u) != 0;
}

static int obstacle_can_enter(void *opaque, Ra2GroundCell cell, int32_t direction)
{
    PrepareContext *context = opaque;
    uint32_t height = engine_call(context, 0x5D47D0, owner_address(context), NULL, 0);
    uint32_t argument = cell_argument(context, cell);
    uint32_t target_cell = engine_call(context, 0x548070, 0x8324E0, &argument, 1);
    uint32_t arguments[5] = { target_cell, (uint32_t)direction, height, 0, 1 };
    return (int)owner_call(context, 0x194, arguments, 5);
}

static void obstacle_request_gate(void *opaque, Ra2GroundCell cell)
{
    PrepareContext *context = opaque;
    uint32_t arguments[2] = { owner_address(context), cell_argument(context, cell) };
    engine_call(context, 0x55ACD0, 0x8324E0, arguments, 2);
}

static int obstacle_find_allied_blocker(void *opaque, Ra2GroundCell cell)
{
    PrepareContext *context = opaque;
    uint32_t argument = cell_argument(context, cell);
    context->obstacle_cell = engine_call(context, 0x548070, 0x8324E0, &argument, 1);
    Ra2WorldPoint position = read_point(owner_address(context) + 0x88);
    Ra2WorldPoint center = { (int32_t)cell.x * 256 + 128, (int32_t)cell.y * 256 + 128, 0 };
    uint32_t scratch = context->frame - 0x80;
    write_point(scratch, center);
    argument = scratch;
    int32_t surface = (int32_t)engine_call(context, 0x55A280, 0x8324E0, &argument, 1);
    int32_t upper_surface = (int32_t)((uint32_t)surface + MEM32(0x8529D0) * 2u);
    write_point(scratch + 16, (Ra2WorldPoint){ 0, 0, 0 });
    uint32_t arguments[3] = { scratch + 16, position.z > upper_surface, 0 };
    uint32_t blocker = engine_call(context, 0x471660, context->obstacle_cell, arguments, 3);
    if (!blocker)
    {
        return 0;
    }
    return (engine_call(context, 0x4E5580, MEM32(owner_address(context) + 0x1B4), &blocker, 1) & 255u) != 0;
}

static void obstacle_notify_blocker(void *opaque, int bridge_layer)
{
    PrepareContext *context = opaque;
    uint32_t arguments[4] = { 0x852998, 1, 1, bridge_layer != 0 };
    engine_call(context, 0x476920, context->obstacle_cell, arguments, 4);
}

static void obstacle_reset_failure_budget(void *opaque, int32_t remaining)
{
    PrepareContext *context = opaque;
    MEM32(owner_address(context) + 0x53C) = (uint32_t)remaining;
}

uint32_t ra2_ground_observe_obstacle_bridge(int rebuilt)
{
    PrepareContext context = { 0 };
    context.drive = g_ebp;
    context.frame = g_esp;
    read_state(&context);
    g_esp -= 0x200;
    int32_t path_head = -1;
    Ra2ObstacleServices services = { &context, obstacle_query, obstacle_position, obstacle_neighbor, obstacle_inside_map,
        obstacle_can_enter, obstacle_request_gate, obstacle_find_allied_blocker, obstacle_notify_blocker,
        cancel_target, stop_navigation, obstacle_reset_failure_budget };
    Ra2PreparePhase phase = ra2_ground_observe_obstacle(&context.state, read_point(0x852998), rebuilt, &path_head, &services);
    if (phase == RA2_PREPARE_FINISH_FAILED_ATTEMPT)
    {
        write_state(&context);
        g_ebp = context.drive;
        g_esp = context.frame;
        return 0x4A2DFD;
    }
    return finish(&context, phase, path_head);
}

static int32_t segment_query(void *opaque, Ra2SegmentQuery query)
{
    PrepareContext *context = opaque;
    uint32_t result, argument = context->frame - 0x80;
    switch (query)
    {
        case RA2_SEGMENT_OWNER_BRIDGE_FLAG: return MEM8(owner_address(context) + 0x79);
        case RA2_SEGMENT_OWNER_PREDICATE_27C: return (owner_call(context, 0x27C, NULL, 0) & 255u) != 0;
        case RA2_SEGMENT_FACING_RAW:
            result = engine_call(context, 0x4B8BE0, owner_address(context) + 0x2E0, &argument, 1);
            return MEM16(result);
        case RA2_SEGMENT_ACTOR_IS_TRAIN:
            result = owner_call(context, 0x80, NULL, 0);
            return MEM8(result + 0xAA0) != 0;
        case RA2_SEGMENT_ACTOR_IS_CRUSHER:
            result = owner_call(context, 0x80, NULL, 0);
            return MEM8(result + 0xAF3) != 0;
        case RA2_SEGMENT_CELL_OVERLAY_INDEX: return (int32_t)MEM32(context->obstacle_cell + 0x44);
        default: abort();
    }
}

static Ra2WorldPoint segment_candidate_point(void *opaque, unsigned direction)
{
    PrepareContext *context = opaque;
    Ra2WorldPoint position = read_point(owner_address(context) + 0x88);
    uint32_t delta = 0x851AC0 + direction * 8;
    uint32_t arguments[3] = { (uint32_t)position.x + MEM32(delta), (uint32_t)position.y + MEM32(delta + 4), (uint32_t)position.z };
    return read_point(engine_call(context, 0x41B630, context->frame - 0x80, arguments, 3));
}

static Ra2CellSurface segment_surface_at(void *opaque, Ra2WorldPoint position)
{
    PrepareContext *context = opaque;
    uint32_t argument = context->frame - 0x80;
    write_point(argument, position);
    uint32_t cell = engine_call(context, 0x548000, 0x8324E0, &argument, 1);
    Ra2CellSurface surface = { (int8_t)MEM8(cell + 0x11B), (MEM32(cell + 0x140) & 0x100) != 0 };
    return surface;
}

static Ra2CellSurface segment_current_surface(void *opaque)
{
    PrepareContext *context = opaque;
    return segment_surface_at(context, read_point(owner_address(context) + 0x88));
}

static void segment_mark_bridge_transition(void *opaque)
{
    PrepareContext *context = opaque;
    MEM8(owner_address(context) + 0x57B) = 1;
}

static int segment_request_gate(void *opaque, Ra2GroundCell cell)
{
    PrepareContext *context = opaque;
    uint32_t arguments[2] = { owner_address(context), cell_argument(context, cell) };
    return (engine_call(context, 0x55ACD0, 0x8324E0, arguments, 2) & 255u) != 0;
}

static void segment_turn_toward(void *opaque, uint16_t direction)
{
    PrepareContext *context = opaque;
    uint32_t interface_address = MEM32(context->frame + 0x14);
    uint32_t arguments[2] = { interface_address, direction };
    engine_call(context, MEM32(MEM32(interface_address) + 0x4C), g_ecx, arguments, 2);
}

static int32_t segment_classify_cell(void *opaque, Ra2GroundCell cell, int32_t direction, int32_t reference_level)
{
    PrepareContext *context = opaque;
    ra2_internal_observe(context->drive,0,13,0,0);
    uint32_t argument = cell_argument(context, cell);
    context->obstacle_cell = engine_call(context, 0x548070, 0x8324E0, &argument, 1);
    MEM8(context->frame + 0x13) = 0;
    MEM32(context->frame + 0x2C) = context->obstacle_cell;
    /* 暂时移除自身占用后检查下一格，再恢复占用；三次服务的顺序与原版相同。 */
    argument = 0;
    owner_call(context, 0x11C, &argument, 1);
    uint32_t arguments[5] = { context->obstacle_cell, (uint32_t)direction, (uint32_t)reference_level, 0, 1 };
    int32_t passage = (int32_t)owner_call(context, 0x194, arguments, 5);
    argument = 1;
    owner_call(context, 0x11C, &argument, 1);
    return passage;
}

uint32_t ra2_ground_prepare_segment_bridge(void)
{
    PrepareContext context = { 0 };
    context.drive = g_ebp;
    context.frame = g_esp;
    int32_t path_head = (int32_t)g_ebx;
    read_state(&context);
    g_esp -= 0x200;
    Ra2SegmentServices services = { &context, segment_query, segment_candidate_point, segment_current_surface,
        segment_surface_at, segment_mark_bridge_transition, segment_request_gate, segment_turn_toward, segment_classify_cell };
    Ra2SegmentPreparation preparation = { 0 };
    Ra2SegmentPhase phase = ra2_ground_prepare_segment(path_head, &preparation, &services);
    if (phase != RA2_SEGMENT_CLASSIFIED)
    {
        return finish(&context, phase == RA2_SEGMENT_WAIT ? RA2_PREPARE_RETURN_TRUE : RA2_PREPARE_RETURN_FALSE, path_head);
    }
    write_state(&context);
    write_point(context.frame + 0x38, preparation.candidate);
    memcpy((void *)(uintptr_t)ADDR(context.frame + 0x14), &preparation.cell, sizeof(preparation.cell));
    MEM32(context.frame + 0x18) = (uint32_t)preparation.passage;
    g_ebp = context.drive;
    g_esp = context.frame;
    g_ebx = (uint32_t)path_head;
    g_esi = context.obstacle_cell;
    g_edi = (uint32_t)preparation.reference_level;
    return 0x4A3550;
}

static uint32_t clearance_cell(PrepareContext *context)
{
    uint32_t argument = context->frame + 0x14;
    return engine_call(context, 0x548070, 0x8324E0, &argument, 1);
}

static int32_t clearance_query(void *opaque, Ra2ClearanceQuery query)
{
    PrepareContext *context = opaque;
    uint32_t index;
    switch (query)
    {
        case RA2_CLEARANCE_OVERLAY_INDEX: return (int32_t)MEM32(context->obstacle_cell + 0x44);
        case RA2_CLEARANCE_OVERLAY_CRUSHABLE:
            index = MEM32(context->obstacle_cell + 0x44);
            return MEM8(MEM32(MEM32(0xA35DEC) + index * 4u) + 0x1FD) != 0;
        case RA2_CLEARANCE_CELL_LEVEL: return (int8_t)MEM8(clearance_cell(context) + 0x11B);
        case RA2_CLEARANCE_CELL_LAND: return (int32_t)MEM32(clearance_cell(context) + 0xEC);
        default: abort();
    }
}

static void clearance_request_gate(void *opaque)
{
    PrepareContext *context = opaque;
    MEM32(context->frame + 0x68) = MEM32(context->frame + 0x14);
    uint32_t arguments[2] = { owner_address(context), context->frame + 0x68 };
    engine_call(context, 0x55ACD0, 0x8324E0, arguments, 2);
}

uint32_t ra2_ground_clearance_bridge(int clear_only)
{
    PrepareContext context = { 0 };
    context.drive = g_ebp;
    context.frame = g_esp;
    context.obstacle_cell = g_esi;
    if (!clear_only) ra2_state_movement_audit(9, context.drive, context.obstacle_cell, MEM32(context.frame + 0x18));
    uint32_t cached_head = g_ebx;
    int32_t reference_level = (int32_t)g_edi, passage = (int32_t)MEM32(context.frame + 0x18);
    read_state(&context);
    g_esp -= 0x200;
    Ra2ClearanceServices services = { &context, clearance_query, clearance_request_gate };
    Ra2ClearanceResult result = { 0, 0, MEM8(context.frame + 0x13) };
    Ra2ClearancePhase phase = ra2_ground_check_clearance(&context.state, read_point(0x852998),
        passage, reference_level, clear_only, &result, &services);
    write_state(&context);
    g_esp = context.frame;
    g_ebp = context.drive;
    g_ebx = cached_head;
    MEM8(context.frame + 0x13) = (uint8_t)result.crush_overlay;
    if (phase == RA2_CLEARANCE_TERRAIN_SPEED)
    {
        MEM32(context.frame + 0x28) = (uint32_t)result.target_level;
        g_esi = (uint32_t)result.land;
        return 0x4A3C9B;
    }
    g_esi = clear_only ? context.obstacle_cell : UINT32_MAX;
    g_ecx = (uint32_t)passage;
    g_edi = (uint32_t)reference_level;
    if (phase == RA2_CLEARANCE_SPECIAL_OBSTACLE)
    {
        return 0x4A36ED;
    }
    g_edi = 0;
    g_ebx = context.drive + 0x40;
    g_eax = (uint32_t)passage;
    return phase == RA2_CLEARANCE_WAIT_FOR_TRAFFIC ? 0x4A364F : 0x4A3A8E;
}

static int32_t traffic_frame(void *opaque)
{
    (void)opaque;
    return (int32_t)MEM32(0xA40D2C);
}

static int32_t traffic_duration(void *opaque)
{
    (void)opaque;
    return (int32_t)MEM32(MEM32(0x839848) + 0x13D0);
}

static void traffic_start_wait(void *opaque, int32_t frame, int32_t duration)
{
    PrepareContext *context = opaque;
    uint32_t owner = owner_address(context);
    MEM8(owner + 0x5A1) = 1;
    MEM32(owner + 0x558) = (uint32_t)frame;
    MEM32(owner + 0x55C) = MEM32(context->frame + 0x54);
    MEM32(owner + 0x560) = (uint32_t)duration;
}

static int traffic_rebuild(void *opaque, int mode)
{
    PrepareContext *context = opaque;
    uint32_t cell = (uint16_t)(context->state.destination.x / 256)
        | ((uint32_t)(uint16_t)(context->state.destination.y / 256) << 16);
    MEM32(context->frame + 0x68) = cell;
    uint32_t arguments[3] = { cell, 0, (uint32_t)mode };
    return (engine_call(context, 0x4C3000, owner_address(context), arguments, 3) & 255u) != 0;
}

static int traffic_owner_exists(void *opaque)
{
    return prepare_query(opaque, RA2_PREPARE_OWNER_EXISTS);
}

static int traffic_accepted(void *opaque)
{
    return prepare_query(opaque, RA2_PREPARE_DESTINATION_ACCEPTED);
}

static void traffic_aborted(void *opaque)
{
    write_aborted(opaque, 1);
}

static void traffic_stop(void *opaque)
{
    stop_navigation(opaque, 0);
}

static int32_t traffic_retry_delay(void *opaque)
{
    return prepare_query(opaque, RA2_PREPARE_RETRY_DELAY_FRAMES);
}

static void traffic_restart_retry(void *opaque, int32_t frame, int32_t duration)
{
    PrepareContext *context = opaque;
    uint32_t owner = owner_address(context);
    MEM32(owner + 0x530) = (uint32_t)frame;
    MEM32(owner + 0x534) = MEM32(context->frame + 0x54);
    MEM32(owner + 0x538) = (uint32_t)duration;
}

uint32_t ra2_ground_traffic_wait_bridge(void)
{
    ra2_state_movement_audit(8, g_ebp, 0, 0);
    PrepareContext context = { 0 };
    context.drive = g_ebp;
    context.frame = g_esp;
    read_state(&context);
    uint32_t owner = owner_address(&context);
    Ra2TrafficWaitState state = { MEM8(owner + 0x5A1),
        { (int32_t)MEM32(owner + 0x530), (int32_t)MEM32(owner + 0x538) },
        { (int32_t)MEM32(owner + 0x558), (int32_t)MEM32(owner + 0x560) } };
    Ra2TrafficWaitServices services = { &context, traffic_frame, traffic_duration, traffic_start_wait,
        traffic_rebuild, traffic_owner_exists, traffic_accepted, traffic_aborted, traffic_stop,
        traffic_retry_delay, traffic_restart_retry };
    g_esp -= 0x200;
    Ra2TrafficWaitPhase phase = ra2_ground_wait_for_traffic(&state, &services);
    if (phase == RA2_TRAFFIC_REPORT_OBSTACLE)
    {
        write_state(&context);
        g_esp = context.frame;
        g_ebp = context.drive;
        g_ebx = context.drive + 0x40;
        return 0x4A3A98;
    }
    return finish(&context, phase == RA2_TRAFFIC_RETURN_TRUE ? RA2_PREPARE_RETURN_TRUE : RA2_PREPARE_RETURN_FALSE, -1);
}

static int reaction_sound_pending(void *opaque)
{
    return MEM8(owner_address(opaque) + 0x57A) != 0;
}

static void reaction_play_sound(void *opaque)
{
    PrepareContext *context = opaque;
    uint32_t arguments[2] = { 0x3F800000, 0 };
    g_edx = 0x2000;
    engine_call(context, 0x713DB0, MEM32(MEM32(0x839848) + 0x620), arguments, 2);
}

static int reaction_retry(void *opaque, int32_t path_head, uint32_t flags)
{
    PrepareContext *context = opaque;
    MEM32(owner_address(context) + 0x4D0) = (uint32_t)path_head;
    traffic_restart_retry(context, traffic_frame(context), 0);
    uint32_t arguments[3] = { MEM32(context->frame + 0x60), flags, flags };
    return (engine_call(context, 0x4A2670, context->drive, arguments, 3) & 255u) != 0;
}

static uint32_t reaction_find_object(void *opaque, uint32_t flags)
{
    PrepareContext *context = opaque;
    MEM32(context->frame + 0x2C) = flags;
    MEM32(context->frame + 0x30) = flags;
    uint32_t arguments[2] = { context->frame + 0x2C, flags };
    return engine_call(context, 0x471830, clearance_cell(context), arguments, 2);
}

static int reaction_allied(void *opaque, uint32_t object)
{
    PrepareContext *context = opaque;
    return (engine_call(context, 0x4E5580, MEM32(owner_address(context) + 0x1B4), &object, 1) & 255u) != 0;
}

static void reaction_attack_object(void *opaque, uint32_t flags)
{
    PrepareContext *context = opaque;
    uint32_t target = MEM32(MEM32(owner_address(context)) + 0x1DC);
    uint32_t object = reaction_find_object(context, flags);
    uint32_t arguments[3] = { 1, object, flags };
    engine_call(context, target, owner_address(context), arguments, 3);
}

static int reaction_has_overlay(void *opaque, int32_t missing_index)
{
    return (int32_t)MEM32(clearance_cell(opaque) + 0x44) != missing_index;
}

static int reaction_wall(void *opaque)
{
    uint32_t index = MEM32(clearance_cell(opaque) + 0x44);
    return MEM8(MEM32(MEM32(0xA35DEC) + index * 4u) + 0x278) != 0;
}

static void reaction_attack_wall(void *opaque, uint32_t flags)
{
    PrepareContext *context = opaque;
    uint32_t target = MEM32(MEM32(owner_address(context)) + 0x1DC);
    uint32_t arguments[3] = { 1, clearance_cell(context), flags };
    engine_call(context, target, owner_address(context), arguments, 3);
}

static int reaction_has_target(void *opaque)
{
    return prepare_query(opaque, RA2_PREPARE_HAS_TARGET_488);
}

static void reaction_clear_pending(void *opaque)
{
    PrepareContext *context = opaque;
    MEM8(owner_address(context) + 0x57A) = 0;
    MEM32(context->drive + 0x58) = UINT32_MAX;
}

void ra2_ground_reaction_bridge(unsigned entry)
{
    PrepareContext context = { 0 };
    context.drive = g_ebp;
    context.frame = g_esp;
    int32_t dispatch_code = (int32_t)g_eax, path_head = (int32_t)g_esi;
    uint32_t flags = g_edi;
    int32_t passage = (int32_t)MEM32(context.frame + 0x18);
    int allow_recursive = MEM8(context.frame + 0x64) != 0;
    read_state(&context);
    g_esp -= 0x200;
    Ra2ReactionServices services = { &context, reaction_sound_pending, reaction_play_sound, reaction_retry,
        reaction_find_object, reaction_allied, reaction_attack_object, reaction_has_overlay, reaction_wall,
        reaction_attack_wall, reaction_has_target, cancel_target, stop_navigation, reaction_clear_pending };
    int result = ra2_ground_react_to_obstacle(&context.state, read_point(0x852998), (Ra2ReactionEntry)entry,
        dispatch_code, passage, allow_recursive, path_head, flags, &services);
    finish(&context, result ? RA2_PREPARE_RETURN_TRUE : RA2_PREPARE_RETURN_FALSE, -1);
}

static int32_t special_distance(PrepareContext *context)
{
    uint32_t scratch = context->frame - 0x80, argument = scratch;
    Ra2WorldPoint position = read_point(owner_call(context, 0x48, &argument, 1));
    uint32_t components[3] = { (uint32_t)position.x - (uint32_t)context->state.destination.x,
        (uint32_t)position.y - (uint32_t)context->state.destination.y,
        (uint32_t)position.z - (uint32_t)context->state.destination.z };
    uint32_t vector = engine_call(context, 0x41B630, scratch + 32, components, 3);
    Ra2WorldPoint difference = read_point(vector);
    /* 本分支按 z²+y²+x² 累加，而通用长度函数按 x²+y²+z²。
       反转送入数值服务的轴顺序，保留原版近似开方表、__ftol 与控制字副作用。 */
    write_point(scratch + 48, (Ra2WorldPoint){ difference.z, difference.y, difference.x });
    return (int32_t)engine_call(context, 0x41B780, scratch + 48, NULL, 0);
}

static int32_t special_query(void *opaque, Ra2SpecialQuery query)
{
    PrepareContext *context = opaque;
    switch (query)
    {
        case RA2_SPECIAL_IS_TRAIN: return obstacle_query(context, RA2_OBSTACLE_TRAIN);
        case RA2_SPECIAL_DISTANCE_TO_TARGET: return special_distance(context);
        case RA2_SPECIAL_CLOSE_ENOUGH: return prepare_query(context, RA2_PREPARE_CLOSE_ENOUGH_DISTANCE);
        case RA2_SPECIAL_HEIGHT_PER_LEVEL: return (int32_t)MEM32(0x8529D0);
        case RA2_SPECIAL_CURRENT_LAND: return obstacle_query(context, RA2_OBSTACLE_CURRENT_LAND);
        case RA2_SPECIAL_CELL_HAS_BRIDGE: return (MEM32(clearance_cell(context) + 0x140) & 0x100) != 0;
        case RA2_SPECIAL_CELL_LEVEL: return (int8_t)MEM8(clearance_cell(context) + 0x11B);
        case RA2_SPECIAL_HAS_TARGET_488: return prepare_query(context, RA2_PREPARE_HAS_TARGET_488);
        default: abort();
    }
}

static Ra2WorldPoint special_position(void *opaque)
{
    return read_point(owner_address(opaque) + 0x88);
}

static int special_retry(void *opaque, int32_t path_head, int restart_timer)
{
    PrepareContext *context = opaque;
    MEM32(owner_address(context) + 0x4D0) = (uint32_t)path_head;
    if (restart_timer)
    {
        uint32_t owner = owner_address(context);
        MEM32(owner + 0x530) = MEM32(0xA40D2C);
        MEM32(owner + 0x534) = MEM32(context->frame + 0x48);
        MEM32(owner + 0x538) = 0;
    }
    uint32_t arguments[3] = { MEM32(context->frame + 0x60), 0, 0 };
    return (engine_call(context, 0x4A2670, context->drive, arguments, 3) & 255u) != 0;
}

static void special_reveal(void *opaque)
{
    PrepareContext *context = opaque;
    engine_call(context, 0x478740, clearance_cell(context), NULL, 0);
}

static void special_notify(void *opaque, int bridge_layer)
{
    PrepareContext *context = opaque;
    uint32_t arguments[4] = { 0x852998, 1, 1, bridge_layer != 0 };
    engine_call(context, 0x476920, clearance_cell(context), arguments, 4);
}

uint32_t ra2_ground_special_obstacle_bridge(void)
{
    PrepareContext context = { 0 };
    context.drive = g_ebp;
    context.frame = g_esp;
    uint32_t path_head = g_esi, passage = g_ecx, cached_head = g_ebx;
    read_state(&context);
    if (passage==6 || passage==1) ra2_state_movement_audit(passage==6 ? 11 : 12,context.drive,0,0);
    g_esp -= 0x200;
    Ra2SpecialServices services = { &context, special_query, special_position, special_retry, special_reveal,
        special_notify, cancel_target, stop_navigation };
    Ra2SpecialPhase phase = ra2_ground_handle_special_obstacle(&context.state, read_point(0x852998),
        (int32_t)passage, MEM8(context.frame + 0x64) != 0, (int32_t)path_head, &services);
    if (phase != RA2_SPECIAL_CLEAR_SEGMENT)
    {
        return finish(&context, phase == RA2_SPECIAL_RETURN_TRUE ? RA2_PREPARE_RETURN_TRUE : RA2_PREPARE_RETURN_FALSE, -1);
    }
    write_state(&context);
    g_esp = context.frame;
    g_ebp = context.drive;
    g_ebx = cached_head;
    g_esi = path_head;
    return 0x4A35FE;
}

static int template_crushable(void *opaque, int32_t direction)
{
    PrepareContext *context = opaque;
    uint32_t argument = (uint32_t)direction;
    uint32_t neighbor = engine_call(context,0x476AC0,MEM32(context->frame+0x2C),&argument,1);
    if (!neighbor || MEM32(neighbor+0x44)==UINT32_MAX) return 0;
    return MEM8(MEM32(MEM32(0xA35DEC)+MEM32(neighbor+0x44)*4u)+0x1FD)!=0;
}

static uint8_t template_byte(void *opaque, int32_t selector, Ra2TemplateByte field)
{
    (void)opaque;
    return MEM8(0x7A0180+(uint32_t)selector*12u+(field==RA2_TEMPLATE_FLAGS ? 8u : 0u));
}

uint32_t ra2_ground_template_select_bridge(unsigned entry)
{
    PrepareContext context = { 0 };
    context.drive = g_ebp;
    context.frame = g_esp;
    int32_t direction = (int32_t)g_ebx, next_direction = (int32_t)g_esi;
    if (entry == 1) next_direction = direction;
    read_state(&context);
    g_esp -= 0x200;
    Ra2TemplateServices services = { &context,template_crushable,template_byte };
    Ra2TemplateSelection result = ra2_ground_choose_template(direction,next_direction,
        MEM8(context.frame+0x68)!=0,MEM8(context.frame+0x13)!=0,entry==0,&services);
    write_state(&context);
    MEM8(context.drive+0x64) = (uint8_t)result.crushing;
    ra2_state_movement_audit(13,context.drive,0,(uint32_t)result.next_direction+(uint32_t)direction*8u);
    MEM8(context.drive+0x60) = 0;
    MEM32(context.drive+0x58) = (uint32_t)result.selector;
    g_esp = context.frame;
    g_ebp = context.drive;
    g_ebx = (uint32_t)direction;
    g_esi = (uint32_t)result.next_direction;
    return result.flags & 8u ? 0x4A4015 : 0x4A45B7;
}

typedef struct CommitContext
{
    PrepareContext prepare;
    Ra2SegmentCommitState state;
} CommitContext;

static void read_commit(CommitContext *context)
{
    read_state(&context->prepare);
    context->state.movement = context->prepare.state;
    uint32_t drive = context->prepare.drive, owner = owner_address(&context->prepare);
    memcpy(context->state.directions,(void *)(uintptr_t)ADDR(owner+0x4D0),sizeof(context->state.directions));
    context->state.selector = (int32_t)MEM32(drive+0x58);
    context->state.sample_index = (int32_t)MEM32(drive+0x5C);
    context->state.sound_pending = MEM8(owner+0x57A);
    context->state.target_cell_x = (int16_t)MEM16(owner+0x450);
    context->state.target_cell_y = (int16_t)MEM16(owner+0x452);
}

static void write_commit(CommitContext *context)
{
    context->prepare.state = context->state.movement;
    write_state(&context->prepare);
    uint32_t drive = context->prepare.drive, owner = owner_address(&context->prepare);
    memcpy((void *)(uintptr_t)ADDR(owner+0x4D0),context->state.directions,sizeof(context->state.directions));
    MEM32(drive+0x58) = (uint32_t)context->state.selector;
    MEM32(drive+0x5C) = (uint32_t)context->state.sample_index;
    MEM8(owner+0x57A) = (uint8_t)context->state.sound_pending;
    MEM16(owner+0x450) = (uint16_t)context->state.target_cell_x;
    MEM16(owner+0x452) = (uint16_t)context->state.target_cell_y;
}

static int commit_accepts(void *opaque, Ra2WorldPoint position)
{
    CommitContext *context = opaque;
    write_commit(context);
    ra2_state_movement_audit(14,context->prepare.drive,0,0);
    uint32_t argument = context->prepare.frame+0x38;
    write_point(argument,position);
    uint32_t cell = engine_call(&context->prepare,0x548000,0x8324E0,&argument,1);
    argument = owner_address(&context->prepare);
    int accepted = (engine_call(&context->prepare,0x476CC0,cell,&argument,1)&255u)!=0;
    read_commit(context);
    return accepted;
}

static int commit_flag_76(void *opaque)
{
    CommitContext *context = opaque;
    return MEM8(owner_address(&context->prepare)+0x76)!=0;
}

static int commit_alive(void *opaque)
{
    CommitContext *context = opaque;
    return MEM8(owner_address(&context->prepare)+0x7D)!=0;
}

static void commit_start(void *opaque, Ra2WorldPoint position)
{
    CommitContext *context = opaque;
    write_commit(context);
    uint32_t point = context->prepare.frame+0x38;
    write_point(point,position);
    uint32_t arguments[2] = { point,1 };
    engine_call(&context->prepare,0x4A0BC0,context->prepare.drive,arguments,2);
    read_commit(context);
}

static void commit_zero_speed(void *opaque)
{
    CommitContext *context = opaque;
    write_commit(context);
    uint32_t arguments[2] = { 0,0 };
    owner_call(&context->prepare,0x4C8,arguments,2);
    read_commit(context);
}

void ra2_ground_template_commit_bridge(int skip_shift)
{
    int32_t terminal_direction = (int32_t)g_edi;
    CommitContext context = { 0 };
    context.prepare.drive = g_ebp;
    context.prepare.frame = g_esp;
    read_commit(&context);
    g_esp -= 0x200;
    Ra2SegmentCommitServices services = { &context,commit_accepts,commit_flag_76,commit_alive,commit_start,commit_zero_speed };
    ra2_ground_commit_segment(&context.state,read_point(0x852998),read_point(context.prepare.frame+0x38),
        skip_shift,terminal_direction,&services);
    write_commit(&context);
    finish(&context.prepare,RA2_PREPARE_RETURN_FALSE,-1);
}
