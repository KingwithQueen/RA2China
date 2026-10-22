#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "recomp_types.h"
#include "ground_arrival.h"
#include "ground_arrival_bridge.h"

typedef struct ArrivalContext
{
    uint32_t drive;
    uint32_t owner;
    uint32_t frame;
    Ra2GroundArrivalState state;
} ArrivalContext;

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

static void read_state(ArrivalContext *context)
{
    context->state.destination = read_point(context->drive + 0x34);
    context->state.segment_end = read_point(context->drive + 0x40);
    context->state.path_selector = (int32_t)MEM32(context->drive + 0x58);
    context->state.sample_index = (int32_t)MEM32(context->drive + 0x5C);
    context->state.driving = MEM8(context->drive + 0x63);
}

static void write_state(ArrivalContext *context)
{
    write_point(context->drive + 0x34, context->state.destination);
    write_point(context->drive + 0x40, context->state.segment_end);
    MEM32(context->drive + 0x58) = (uint32_t)context->state.path_selector;
    MEM32(context->drive + 0x5C) = (uint32_t)context->state.sample_index;
    MEM8(context->drive + 0x63) = (uint8_t)context->state.driving;
}

static uint32_t engine_call(ArrivalContext *context, uint32_t address, uint32_t object, const uint32_t *arguments, unsigned count)
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
    recomp_func_t function = recomp_lookup_manual(address);
    if (!function)
    {
        function = recomp_lookup(address);
    }
    if (!function)
    {
        function = recomp_lookup_import(address);
    }
    if (!function)
    {
        fprintf(stderr, "[arrival-bridge-error] unresolved operation %08X\n", address);
        abort();
    }
    function();
    if (g_esp != stack)
    {
        fprintf(stderr, "[arrival-bridge-error] unbalanced operation %08X\n", address);
        abort();
    }
    g_cur_func = caller;
    uint32_t result = g_eax;
    read_state(context);
    context->owner = MEM32(context->drive + 0x0C);
    return result;
}

static uint32_t owner_call(ArrivalContext *context, uint32_t slot, const uint32_t *arguments, unsigned count)
{
    return engine_call(context, MEM32(MEM32(context->owner) + slot), context->owner, arguments, count);
}

static int32_t arrival_query(void *opaque, Ra2ArrivalQuery query)
{
    ArrivalContext *context = opaque;
    uint32_t owner = context->owner, scratch = context->frame - 0x80;
    uint32_t arguments[2] = { scratch, owner };
    write_state(context);
    switch (query)
    {
        case RA2_ARRIVAL_TARGET_IS_CURRENT_CELL:
        {
            uint32_t target = MEM32(owner + 0x494);
            if (!target)
            {
                return 0;
            }
            uint32_t address = engine_call(context, MEM32(MEM32(target) + 0x4C), target, arguments, 2);
            Ra2WorldPoint target_position = read_point(address);
            address = owner_call(context, 0x1A0, arguments, 1);
            return MEM16(address) == (uint16_t)(target_position.x / 256)
                && MEM16(address + 2) == (uint16_t)(target_position.y / 256);
        }
        case RA2_ARRIVAL_OWNER_REFERENCE_Z:
            return (int32_t)MEM32(owner_call(context, 0x4C, arguments, 2) + 8);
        case RA2_ARRIVAL_OWNER_USABLE:
            return MEM8(owner + 0x7D) && !MEM8(owner + 0x76) && !MEM8(owner + 0x7A);
        case RA2_ARRIVAL_EFFECTIVE_MISSION:
            return (int32_t)owner_call(context, 0x16C, NULL, 0);
        case RA2_ARRIVAL_OWNER_UPDATE:
            return (owner_call(context, 0x490, NULL, 0) & 255u) != 0;
        case RA2_ARRIVAL_OWNER_ALIVE:
            return MEM8(owner + 0x7D) != 0;
        default:
            fputs("[arrival-bridge-error] invalid query\n", stderr);
            abort();
    }
}

static void relocate(void *opaque, int crosses_cell)
{
    ArrivalContext *context = opaque;
    uint32_t zero = 0, one = 1, point = context->drive + 0x40;
    uint8_t saved_owner_flag = MEM8(context->owner + 0x74);
    if (crosses_cell)
    {
        owner_call(context, 0x11C, &zero, 1);
    }
    else
    {
        MEM8(context->owner + 0x74) = 0;
    }
    owner_call(context, 0x19C, &point, 1);
    owner_call(context, 0x1B4, &zero, 1);
    if (crosses_cell)
    {
        owner_call(context, 0x11C, &one, 1);
    }
    else
    {
        MEM8(context->owner + 0x74) = saved_owner_flag;
    }
}

static void refresh_owner(void *opaque)
{
    ArrivalContext *context = opaque;
    uint32_t argument = 2;
    owner_call(context, 0x174, &argument, 1);
}

static void cancel_target_and_path(void *opaque)
{
    ArrivalContext *context = opaque;
    engine_call(context, 0x4CD9B0, context->owner, NULL, 0);
    MEM32(context->owner + 0x4D0) = UINT32_MAX;
}

static int stop_move_mission(void *opaque)
{
    ArrivalContext *context = opaque;
    uint32_t arguments[2] = { 0, 1 };
    return (owner_call(context, 0x414, arguments, 2) & 255u) != 0;
}

uint32_t ra2_ground_finish_segment_bridge(void)
{
    ArrivalContext context = { 0 };
    context.drive = g_ebp;
    context.owner = MEM32(g_ebp + 0x0C);
    context.frame = g_esp;
    read_state(&context);
    MEM8(context.owner + 0x5A0) = 1;
    MEM32(context.frame + 0x3C) = g_ebx + g_eax;
    MEM8(context.owner + 0x5A1) = 0;
    /* 独立使用栈帧以下的 scratch，不能覆盖继续执行时需要的原版局部量。 */
    g_esp = context.frame - 0x100;
    Ra2ArrivalServices services = { &context, arrival_query, relocate, refresh_owner, cancel_target_and_path, stop_move_mission };
    Ra2ArrivalOutcome outcome = ra2_ground_finish_segment(&context.state, read_point(context.owner + 0x88),
        read_point(0x852998), (int32_t)MEM32(0x8529D0), &services);
    write_state(&context);
    if (outcome == RA2_ARRIVAL_CONTINUE)
    {
        g_ebp = context.drive;
        g_esp = context.frame;
        return 0x4A1FA1;
    }
    g_eax = (g_eax & 0xFFFFFF00u) | (outcome == RA2_ARRIVAL_RETURN_TRUE);
    g_edi = MEM32(context.frame);
    g_esi = MEM32(context.frame + 4);
    g_ebp = MEM32(context.frame + 8);
    g_ebx = MEM32(context.frame + 12);
    g_flag_k = FK_ADD;
    g_flag_a = context.frame + 16;
    g_flag_b = 0xE4;
    g_flag_cf = context.frame + 0xF4 < context.frame + 16;
    g_esp = context.frame + 0xFC;
    return 0;
}
