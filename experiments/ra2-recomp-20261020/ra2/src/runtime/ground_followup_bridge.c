#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "recomp_types.h"
#include "ground_prepare.h"
#include "ground_followup.h"
#include "ground_turn.h"
#include "ground_followup_bridge.h"
#include "state_trace.h"

typedef struct FollowupContext
{
    uint32_t drive;
    uint32_t frame;
    uint32_t obstacle_cell;
    Ra2GroundPrepareState state;
    int32_t last_followup_distance;
} FollowupContext;

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

static void read_state(FollowupContext *context)
{
    context->state.destination = read_point(context->drive + 0x34);
    context->state.segment_end = read_point(context->drive + 0x40);
    context->state.driving = MEM8(context->drive + 0x63);
    context->state.legacy_flag_61 = MEM8(context->drive + 0x61);
}

static void write_state(FollowupContext *context)
{
    write_point(context->drive + 0x34, context->state.destination);
    write_point(context->drive + 0x40, context->state.segment_end);
    MEM8(context->drive + 0x63) = (uint8_t)context->state.driving;
    MEM8(context->drive + 0x61) = (uint8_t)context->state.legacy_flag_61;
}

static uint32_t owner_address(FollowupContext *context)
{
    return MEM32(context->drive + 0x0C);
}

static uint32_t engine_call(FollowupContext *context, uint32_t target, uint32_t object, const uint32_t *arguments, unsigned count)
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

static uint32_t owner_call(FollowupContext *context, uint32_t slot, const uint32_t *arguments, unsigned count)
{
    uint32_t owner = owner_address(context);
    return engine_call(context, MEM32(MEM32(owner) + slot), owner, arguments, count);
}

static double read_double(uint32_t address)
{
    double value;
    memcpy(&value, (const void *)(uintptr_t)ADDR(address), sizeof(value));
    return value;
}

static void write_double(uint32_t address, double value)
{
    memcpy((void *)(uintptr_t)ADDR(address), &value, sizeof(value));
}

static int32_t speed_query(void *opaque, Ra2SpeedQuery query)
{
    FollowupContext *context = opaque;
    uint32_t arguments[2], point, cell;
    switch (query)
    {
        case RA2_SPEED_TARGET_SURFACE:
            arguments[0] = context->frame + 0x14;
            cell = engine_call(context, 0x548070, 0x8324E0, arguments, 1);
            arguments[0] = context->frame + 0x50;
            point = engine_call(context, 0x475D60, cell, arguments, 1);
            return (int32_t)engine_call(context, 0x55A280, 0x8324E0, &point, 1);
        case RA2_SPEED_CURRENT_SURFACE:
            point = context->frame + 0x44;
            write_point(point, read_point(owner_address(context) + 0x88));
            return (int32_t)engine_call(context, 0x55A280, 0x8324E0, &point, 1);
        case RA2_SPEED_OWNER_KIND: return (int32_t)owner_call(context, 0x2C, NULL, 0);
        case RA2_SPEED_CLASS: return (int32_t)MEM32(owner_call(context, 0x80, NULL, 0) + 0x5A4);
        case RA2_SPEED_TEMPLATE_SELECTOR: return (int32_t)MEM32(context->drive + 0x58);
        default: abort();
    }
}

static double speed_value(void *opaque, Ra2SpeedValue value)
{
    FollowupContext *context = opaque;
    uint32_t rules = MEM32(0x839848);
    switch (value)
    {
        case RA2_SPEED_TERRAIN_FACTOR:
        {
            uint32_t speed_class = MEM32(owner_call(context, 0x80, NULL, 0) + 0x5A4);
            uint32_t address = 0x850EA0 + ((uint32_t)context->obstacle_cell * 9u + speed_class) * 4u;
            float factor;
            memcpy(&factor, (const void *)(uintptr_t)ADDR(address), sizeof(factor));
            return factor;
        }
        case RA2_SPEED_UPHILL_CLASS_1: return read_double(rules + 0x690);
        case RA2_SPEED_DOWNHILL_CLASS_1: return read_double(rules + 0x698);
        case RA2_SPEED_UPHILL_OTHER: return read_double(rules + 0x6A0);
        case RA2_SPEED_DOWNHILL_OTHER: return read_double(rules + 0x6A8);
        case RA2_SPEED_OWNER_RATIO:
        {
            engine_call(context, 0x5D4540, owner_address(context), NULL, 0);
            double ratio = g_st[0];
            fp_pop_impl(g_st, &g_fp_top);
            return ratio;
        }
        case RA2_SPEED_SLOW_RATIO_LIMIT: return read_double(rules + 0x1368);
        case RA2_SPEED_CURRENT_UNIT_SPEED: return read_double(owner_address(context) + 0x468);
        default: abort();
    }
}

static uint16_t speed_control(void *opaque)
{
    (void)opaque;
    return g_fpu_cw;
}

static void speed_store(void *opaque, double factor)
{
    FollowupContext *context = opaque;
    write_double(context->frame + 0x18, factor);
}

static void speed_apply(void *opaque, double factor, int to_drive)
{
    FollowupContext *context = opaque;
    if (to_drive)
    {
        write_double(context->drive + 0x50, factor);
    }
    else
    {
        uint32_t arguments[2];
        memcpy(arguments, &factor, sizeof(arguments));
        owner_call(context, 0x4C8, arguments, 2);
    }
}

void ra2_ground_speed_prepare_bridge(void)
{
    ra2_state_movement_audit(16, g_ebp, 0, g_esi);
    FollowupContext context = { g_ebp, g_esp, g_esi, { 0 } };
    uint32_t head = g_ebx;
    read_state(&context);
    g_esp -= 0x200;
    Ra2GroundSpeedServices services = { &context, speed_query, speed_value, speed_control, speed_store, speed_apply };
    ra2_ground_prepare_speed(&services);
    write_state(&context);
    g_esp = context.frame;
    g_ebp = context.drive;
    g_ebx = head;
}

static void followup_candidate(void *opaque)
{
    FollowupContext *context = opaque;
    Ra2WorldPoint candidate = read_point(context->frame + 0x38);
    /* 原版压入参数后 ESP 改变，后续 [esp+40] 仍指候选点 y。 */
    uint32_t cell = (uint16_t)(candidate.x / 256) | ((uint32_t)(uint16_t)(candidate.y / 256) << 16);
    MEM32(context->frame + 0x18) = cell;
    uint32_t arguments[2] = { context->frame + 0x18, 1 };
    owner_call(context, 0x4B8, arguments, 2);
    ra2_state_movement_audit(22,context->drive,0,0);
}

static int32_t followup_next(void *opaque)
{
    return (int32_t)MEM32(owner_address(opaque) + 0x4D4);
}

static int32_t followup_distance(void *opaque)
{
    FollowupContext *context = opaque;
    uint32_t scratch = context->frame + 0x50;
    uint32_t position_address = owner_call(context, 0x48, &scratch, 1);
    Ra2WorldPoint position = read_point(position_address), destination = context->state.destination;
    Ra2WorldPoint reverse;
    uint32_t bits[3] = { (uint32_t)position.z - (uint32_t)destination.z,
        (uint32_t)position.y - (uint32_t)destination.y, (uint32_t)position.x - (uint32_t)destination.x };
    memcpy(&reverse, bits, sizeof(reverse));
    scratch = context->frame - 0x80;
    write_point(scratch, reverse);
    context->last_followup_distance=(int32_t)engine_call(context, 0x41B780, scratch, NULL, 0);
    return context->last_followup_distance;
}

static int followup_train(void *opaque)
{
    FollowupContext *context = opaque;
    ra2_state_movement_audit(23,context->drive,0,(uint32_t)context->last_followup_distance);
    return MEM8(owner_call(context, 0x80, NULL, 0) + 0xAA0) != 0;
}

static int followup_rebuild(void *opaque, int train_mode)
{
    FollowupContext *context = opaque;
    uint32_t cell = (uint16_t)(context->state.destination.x / 256)
        | ((uint32_t)(uint16_t)(context->state.destination.y / 256) << 16);
    MEM32(context->frame + 0x18) = cell;
    uint32_t arguments[3] = { cell, (uint32_t)train_mode, 0 };
    int rebuilt = (engine_call(context, 0x4C3000, owner_address(context), arguments, 3) & 255u) != 0;
    if (!rebuilt) ra2_state_movement_audit(18, context->drive, 0, 0);
    return rebuilt;
}

static int followup_owner(void *opaque)
{
    return owner_address(opaque) != 0;
}

static void followup_aborted(void *opaque)
{
    FollowupContext *context = opaque;
    MEM8(MEM32(context->frame + 0x60)) = 1;
}

static int followup_accepted(void *opaque)
{
    FollowupContext *context = opaque;
    uint32_t argument = context->drive + 0x34;
    return (owner_call(context, 0x2AC, &argument, 1) & 255u) != 0;
}

static void followup_stop(void *opaque)
{
    FollowupContext *context = opaque;
    uint32_t arguments[2] = { 0, 1 };
    owner_call(context, 0x410, arguments, 2);
}

static uint32_t finish_followup(FollowupContext *context, int result)
{
    write_state(context);
    g_eax = (g_eax & 0xFFFFFF00u) | (result != 0);
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

uint32_t ra2_ground_followup_bridge(void)
{
    ra2_state_movement_audit(17, g_ebp, 0, 0);
    FollowupContext context = { g_ebp, g_esp, 0, { 0 } };
    uint32_t direction = g_ebx;
    read_state(&context);
    g_esp -= 0x200;
    Ra2FollowupServices services = { &context, followup_candidate, followup_next, followup_distance,
        followup_train, followup_rebuild, followup_owner, followup_aborted, followup_accepted, followup_stop };
    Ra2FollowupResult result = ra2_ground_prepare_followup(&services);
    if (result.aborted) return finish_followup(&context, 0);
    write_state(&context);
    g_esp = context.frame;
    g_ebp = context.drive;
    g_ebx = direction;
    g_esi = (uint32_t)result.next_direction;
    return result.force_straight ? 0x4A3F9F : 0x4A3F8B;
}

typedef struct TurnContext
{
    FollowupContext base;
    Ra2TurnState state;
    uint32_t current_cell;
} TurnContext;

static void read_turn(TurnContext *context)
{
    read_state(&context->base);
    context->state.movement = context->base.state;
    uint32_t owner = owner_address(&context->base);
    context->state.candidate = read_point(context->base.frame + 0x38);
    context->state.selector = (int32_t)MEM32(context->base.drive + 0x58);
    if (owner)
    {
        memcpy(context->state.directions, (const void *)(uintptr_t)ADDR(owner + 0x4D0), sizeof(context->state.directions));
        context->state.bridge_transition_pending = MEM8(owner + 0x57B);
    }
}

static void write_turn(TurnContext *context)
{
    context->base.state = context->state.movement;
    write_state(&context->base);
    uint32_t owner = owner_address(&context->base);
    write_point(context->base.frame + 0x38, context->state.candidate);
    MEM32(context->base.drive + 0x58) = (uint32_t)context->state.selector;
    /* 递归准备可以在所有者消失后直接返回；原版此时不再访问单位队列。 */
    if (owner)
    {
        memcpy((void *)(uintptr_t)ADDR(owner + 0x4D0), context->state.directions, sizeof(context->state.directions));
        MEM8(owner + 0x57B) = (uint8_t)context->state.bridge_transition_pending;
    }
}

static uint32_t turn_call(TurnContext *context, uint32_t target, uint32_t object,
    const uint32_t *arguments, unsigned count)
{
    write_turn(context);
    uint32_t result = engine_call(&context->base, target, object, arguments, count);
    read_turn(context);
    return result;
}

static uint32_t turn_owner_call(TurnContext *context, uint32_t slot, const uint32_t *arguments, unsigned count)
{
    uint32_t owner = owner_address(&context->base);
    return turn_call(context, MEM32(MEM32(owner) + slot), owner, arguments, count);
}

static uint32_t turn_cell(TurnContext *context)
{
    uint32_t argument = context->base.frame + 0x14;
    context->current_cell = turn_call(context, 0x548070, 0x8324E0, &argument, 1);
    return context->current_cell;
}

static int32_t turn_distance(TurnContext *context)
{
    uint32_t argument = context->base.frame + 0x50;
    Ra2WorldPoint position = read_point(turn_owner_call(context, 0x48, &argument, 1));
    Ra2WorldPoint destination = context->state.movement.destination;
    uint32_t components[3] = { (uint32_t)position.x - (uint32_t)destination.x,
        (uint32_t)position.y - (uint32_t)destination.y, (uint32_t)position.z - (uint32_t)destination.z };
    argument = context->base.frame - 0x80;
    memcpy((void *)(uintptr_t)ADDR(argument), components, sizeof(components));
    /* 此分支按 x²+y²+z² 求和；前面的第二路径准备按 z²+y²+x² 求和。 */
    return (int32_t)turn_call(context, 0x41B780, argument, NULL, 0);
}

static int32_t turn_query(void *opaque, Ra2TurnQuery query)
{
    TurnContext *context = opaque;
    uint32_t owner = owner_address(&context->base);
    switch (query)
    {
        case RA2_TURN_OWNER_ALIVE: return MEM8(owner + 0x7D) != 0;
        case RA2_TURN_OWNER_FLAG_76: return MEM8(owner + 0x76) != 0;
        case RA2_TURN_IS_TRAIN: return MEM8(turn_owner_call(context, 0x80, NULL, 0) + 0xAA0) != 0;
        case RA2_TURN_IS_CRUSHER: return MEM8(turn_owner_call(context, 0x80, NULL, 0) + 0xAF3) != 0;
        case RA2_TURN_CELL_OVERLAY_INDEX: return (int32_t)MEM32(turn_cell(context) + 0x44);
        case RA2_TURN_DISTANCE_TO_DESTINATION: return turn_distance(context);
        case RA2_TURN_CLOSE_ENOUGH: return (int32_t)MEM32(MEM32(0x839848) + 0x1380);
        case RA2_TURN_HEIGHT_PER_LEVEL: return (int32_t)MEM32(0x8529D0);
        case RA2_TURN_CURRENT_LAND:
        {
            uint32_t point = context->base.frame + 0x44;
            write_point(point, read_point(owner + 0x88));
            return (int32_t)MEM32(turn_call(context, 0x548000, 0x8324E0, &point, 1) + 0xEC);
        }
        case RA2_TURN_CELL_HAS_BRIDGE: return (MEM32(turn_cell(context) + 0x140) & 0x100) != 0;
        case RA2_TURN_CELL_LEVEL: return (int8_t)MEM8(context->current_cell + 0x11B);
        case RA2_TURN_HAS_TARGET_488: return MEM32(owner + 0x488) != 0;
        default: abort();
    }
}

static int turn_accepts(void *opaque)
{
    TurnContext *context = opaque;
    uint32_t cell = turn_cell(context), argument = owner_address(&context->base);
    return (turn_call(context, 0x476CC0, cell, &argument, 1) & 255u) != 0;
}

static Ra2WorldPoint turn_offset(void *opaque, int32_t direction)
{
    (void)opaque;
    uint32_t address = 0x851AC0 + ((uint32_t)direction & 7u) * 8u;
    Ra2WorldPoint offset = { (int32_t)MEM32(address), (int32_t)MEM32(address + 4), 0 };
    return offset;
}

static int32_t turn_passage(void *opaque, int32_t direction)
{
    TurnContext *context = opaque;
    Ra2WorldPoint candidate = context->state.candidate;
    uint32_t packed = (uint16_t)(candidate.x / 256) | ((uint32_t)(uint16_t)(candidate.y / 256) << 16);
    MEM32(context->base.frame + 0x68) = packed;
    MEM32(context->base.frame + 0x14) = packed;
    uint32_t owner = owner_address(&context->base), method = MEM32(MEM32(owner) + 0x194);
    uint32_t cell = turn_cell(context);
    uint32_t arguments[5] = { cell, (uint32_t)direction, MEM32(context->base.frame + 0x28), 0, 1 };
    return (int32_t)turn_call(context, method, owner_address(&context->base), arguments, 5);
}

static void turn_classified(void *opaque, int32_t passage)
{
    TurnContext *context = opaque;
    write_turn(context);
    ra2_state_movement_audit(19, context->base.drive, context->base.frame, (uint32_t)passage);
}

static void turn_gate(void *opaque)
{
    TurnContext *context = opaque;
    MEM32(context->base.frame + 0x68) = MEM32(context->base.frame + 0x14);
    uint32_t arguments[2] = { owner_address(&context->base), context->base.frame + 0x68 };
    turn_call(context, 0x55ACD0, 0x8324E0, arguments, 2);
}

static int turn_retry(void *opaque, unsigned allow_recursive, unsigned prevent_turn, int restart_timer)
{
    TurnContext *context = opaque;
    write_turn(context);
    if (restart_timer)
    {
        uint32_t owner = owner_address(&context->base);
        MEM32(owner + 0x530) = MEM32(0xA40D2C);
        MEM32(owner + 0x534) = MEM32(context->base.frame + 0x54);
        MEM32(owner + 0x538) = 0;
    }
    uint32_t arguments[3] = { MEM32(context->base.frame + 0x60), allow_recursive, prevent_turn };
    return (turn_call(context, 0x4A2670, context->base.drive, arguments, 3) & 255u) != 0;
}

static Ra2WorldPoint turn_position(void *opaque)
{
    TurnContext *context = opaque;
    return read_point(owner_address(&context->base) + 0x88);
}

static void turn_notify(void *opaque, int bridge_layer)
{
    TurnContext *context = opaque;
    MEM8(context->base.frame + 0x68) = (uint8_t)bridge_layer;
    uint32_t arguments[4] = { 0x852998, 1, 1, MEM32(context->base.frame + 0x68) };
    turn_call(context, 0x476920, context->current_cell, arguments, 4);
}

static void turn_reveal(void *opaque)
{
    TurnContext *context = opaque;
    uint32_t cell = turn_cell(context);
    turn_call(context, 0x478740, cell, NULL, 0);
}

static void turn_cancel(void *opaque)
{
    TurnContext *context = opaque;
    turn_call(context, 0x4CD9B0, owner_address(&context->base), NULL, 0);
}

static int turn_stop(void *opaque, int target_variant)
{
    TurnContext *context = opaque;
    uint32_t arguments[2] = { 0, 1 };
    return (turn_owner_call(context, target_variant ? 0x414 : 0x410, arguments, 2) & 255u) != 0;
}

uint32_t ra2_ground_turn_prepare_bridge(void)
{
    TurnContext context = { 0 };
    context.base.drive = g_ebp;
    context.base.frame = g_esp;
    int32_t direction = (int32_t)g_esi;
    unsigned allow_recursive = MEM32(context.base.frame + 0x64);
    read_turn(&context);
    g_esp -= 0x200;
    Ra2TurnServices services = { &context, turn_query, turn_accepts, turn_offset, turn_passage, turn_classified, turn_gate,
        turn_retry, turn_position, turn_notify, turn_reveal, turn_cancel, turn_stop };
    Ra2TurnPhase phase = ra2_ground_prepare_turn(&context.state, read_point(0x852998), direction,
        allow_recursive, &services);
    write_turn(&context);
    if (phase!=RA2_TURN_COMMIT_WITHOUT_SHIFT) return finish_followup(&context.base, phase==RA2_TURN_RETURN_TRUE);
    g_esp = context.base.frame;
    g_ebp = context.base.drive;
    g_edi = UINT32_MAX;
    return 0x4A45D0;
}

