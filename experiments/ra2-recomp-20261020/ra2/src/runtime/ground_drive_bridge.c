#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "recomp_types.h"
#include "ground_drive.h"
#include "ground_drive_bridge.h"

typedef struct DriveContext
{
    uint32_t drive;
    uint32_t interface_address;
    uint32_t owner;
    uint32_t scratch;
    Ra2GroundDriveState state;
} DriveContext;

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

static int same_point(Ra2WorldPoint left, Ra2WorldPoint right)
{
    return left.x == right.x && left.y == right.y && left.z == right.z;
}

static void read_state(DriveContext *context)
{
    uint32_t drive = context->drive;
    Ra2GroundDriveState *state = &context->state;
    state->surface_current = (int32_t)MEM32(drive + 0x1C);
    state->surface_previous = (int32_t)MEM32(drive + 0x20);
    state->destination = read_point(drive + 0x34);
    state->segment_end = read_point(drive + 0x40);
    state->sample_progress = (int32_t)MEM32(drive + 0x4C);
    memcpy(&state->desired_speed, (const void *)(uintptr_t)ADDR(drive + 0x50), 8);
    state->path_selector = (int32_t)MEM32(drive + 0x58);
    state->sample_index = (int32_t)MEM32(drive + 0x5C);
    state->turn_update_pending = MEM8(drive + 0x62);
    state->driving = MEM8(drive + 0x63);
}

static void write_state(DriveContext *context)
{
    uint32_t drive = context->drive;
    const Ra2GroundDriveState *state = &context->state;
    MEM32(drive + 0x1C) = (uint32_t)state->surface_current;
    MEM32(drive + 0x20) = (uint32_t)state->surface_previous;
    write_point(drive + 0x34, state->destination);
    write_point(drive + 0x40, state->segment_end);
    MEM32(drive + 0x4C) = (uint32_t)state->sample_progress;
    memcpy((void *)(uintptr_t)ADDR(drive + 0x50), &state->desired_speed, 8);
    MEM32(drive + 0x58) = (uint32_t)state->path_selector;
    MEM32(drive + 0x5C) = (uint32_t)state->sample_index;
    MEM8(drive + 0x62) = (uint8_t)state->turn_update_pending;
    MEM8(drive + 0x63) = (uint8_t)state->driving;
}

static uint32_t engine_call(DriveContext *context, uint32_t target, uint32_t object, const uint32_t *arguments,
    unsigned count, int caller_cleans)
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
        fprintf(stderr, "[drive-bridge-error] unresolved operation %08X\n", target);
        abort();
    }
    function();
    if (caller_cleans)
    {
        g_esp += count * 4;
    }
    if (g_esp != stack)
    {
        fprintf(stderr, "[drive-bridge-error] unbalanced operation %08X: %08X != %08X\n", target, g_esp, stack);
        abort();
    }
    g_cur_func = caller;
    uint32_t result = g_eax;
    read_state(context);
    return result;
}

static uint32_t owner_call(DriveContext *context, uint32_t slot, const uint32_t *arguments, unsigned count)
{
    return engine_call(context, MEM32(MEM32(context->owner) + slot), context->owner, arguments, count, 0);
}

static uint32_t locomotion_call(DriveContext *context, uint32_t slot, const uint32_t *extra, unsigned count)
{
    uint32_t arguments[5];
    arguments[0] = context->interface_address;
    for (unsigned i = 0; i < count; ++i)
    {
        arguments[i + 1] = extra[i];
    }
    return engine_call(context, MEM32(MEM32(context->interface_address) + slot), 0, arguments, count + 1, 0);
}

static int32_t drive_query(void *opaque, Ra2DriveQuery query)
{
    DriveContext *context = opaque;
    uint32_t owner = context->owner, target = MEM32(owner + 0x494), result;
    uint32_t arguments[2];
    write_state(context);
    switch (query)
    {
        case RA2_DRIVE_CELL_SURFACE:
            result = owner_call(context, 0x1A4, NULL, 0);
            return MEM8(result + 0x11C);
        case RA2_DRIVE_OWNER_ALIVE: return MEM8(owner + 0x7D) != 0;
        case RA2_DRIVE_OWNER_USABLE: return MEM8(owner + 0x7D) && !MEM8(owner + 0x76) && !MEM8(owner + 0x7A);
        case RA2_DRIVE_OWNER_CATEGORY: return (int32_t)owner_call(context, 0x2C, NULL, 0);
        case RA2_DRIVE_OWNER_FLAG_5B9: return MEM8(owner + 0x5B9) != 0;
        case RA2_DRIVE_OWNER_FLAG_325: return MEM8(owner + 0x325) != 0;
        case RA2_DRIVE_OWNER_FLAG_32D: return MEM8(owner + 0x32D) != 0;
        case RA2_DRIVE_PATH_HEAD: return (int32_t)MEM32(owner + 0x4D0);
        case RA2_DRIVE_CURRENT_MISSION: return (int32_t)MEM32(owner + 0x98);
        case RA2_DRIVE_EFFECTIVE_MISSION: return (int32_t)owner_call(context, 0x16C, NULL, 0);
        case RA2_DRIVE_IS_MOVING: return (locomotion_call(context, 0x10, NULL, 0) & 255u) != 0;
        case RA2_DRIVE_IS_TURNING: return (engine_call(context, 0x4B8C90, owner + 0x2E0, NULL, 0, 0) & 255u) != 0;
        case RA2_DRIVE_TARGET_CATEGORY:
            return target ? (int32_t)engine_call(context, MEM32(MEM32(target) + 0x2C), target, NULL, 0, 0) : -1;
        case RA2_DRIVE_HAS_TARGET: return target != 0;
        case RA2_DRIVE_TARGET_IS_CURRENT_CELL:
            arguments[0] = context->scratch;
            result = owner_call(context, 0x1A0, arguments, 1);
            return MEM16(result) == MEM16(target + 0x24) && MEM16(result + 2) == MEM16(target + 0x26);
        case RA2_DRIVE_DESTINATION_ACCEPTED:
            arguments[0] = context->drive + 0x34;
            return (owner_call(context, 0x2AC, arguments, 1) & 255u) != 0;
        case RA2_DRIVE_POSITION_IS_DESTINATION:
            return same_point(read_point(owner + 0x88), context->state.destination);
        default:
            fputs("[drive-bridge-error] invalid query\n", stderr);
            abort();
    }
}

static void restart_surface_timer(void *opaque)
{
    DriveContext *context = opaque;
    write_state(context);
    MEM32(context->drive + 0x24) = MEM32(0xA40D2C);
    MEM32(context->drive + 0x2C) = 3;
    MEM32(context->drive + 0x30) = 3;
}

static int advance_segment(void *opaque, int skip_speed_increment)
{
    DriveContext *context = opaque;
    uint32_t argument = (uint32_t)skip_speed_increment;
    return (engine_call(context, 0x4A1000, context->drive, &argument, 1, 0) & 255u) != 0;
}

static int prepare_segment(void *opaque)
{
    DriveContext *context = opaque;
    uint32_t arguments[3] = { context->scratch + 32, 1, 0 };
    MEM8(arguments[0]) = 0;
    engine_call(context, 0x4A2670, context->drive, arguments, 3, 0);
    return MEM8(arguments[0]) != 0;
}

static void target_position(void *opaque, Ra2WorldPoint *position)
{
    DriveContext *context = opaque;
    uint32_t target = MEM32(context->owner + 0x494), arguments[2] = { context->scratch, context->owner };
    uint32_t result = engine_call(context, MEM32(MEM32(target) + 0x4C), target, arguments, 2, 0);
    *position = read_point(result);
}

static void set_destination(void *opaque, Ra2WorldPoint position)
{
    DriveContext *context = opaque;
    uint32_t arguments[3] = { (uint32_t)position.x, (uint32_t)position.y, (uint32_t)position.z };
    locomotion_call(context, 0x44, arguments, 3);
}

static void refresh_owner_after_turn(void *opaque)
{
    DriveContext *context = opaque;
    uint32_t argument = 0;
    owner_call(context, 0x174, &argument, 1);
}

static int stop_navigation(void *opaque)
{
    DriveContext *context = opaque;
    uint32_t arguments[2] = { 0, 1 };
    if (!MEM32(context->owner + 0x488))
    {
        owner_call(context, 0x410, arguments, 2);
        return 0;
    }
    engine_call(context, 0x4CD9B0, context->owner, NULL, 0, 0);
    return (owner_call(context, 0x414, arguments, 2) & 255u) != 0;
}

static int finish_frame(void *opaque)
{
    DriveContext *context = opaque;
    uint32_t owner = context->owner;
    /* 原版逐十帧的水面尾迹属于表现服务；不改变路径状态机的分支顺序。 */
    if ((locomotion_call(context, 0x80, NULL, 0) & 255u) && (int32_t)MEM32(0xA40D2C) % 10 == 0 && !MEM8(owner + 0x79))
    {
        uint32_t cell = owner_call(context, 0x1A4, NULL, 0), rules = MEM32(0x839848);
        if (MEM32(cell + 0xEC) == 2 && MEM32(rules + 0x9C))
        {
            uint32_t bytes = 0x1A8;
            uint32_t animation = engine_call(context, 0x782017, 0, &bytes, 1, 1);
            if (animation)
            {
                write_point(context->scratch, read_point(owner + 0x88));
                uint32_t arguments[6] = { MEM32(rules + 0x9C), context->scratch, 0, 1, 0x600, 0 };
                engine_call(context, 0x420110, animation, arguments, 6, 0);
            }
        }
    }
    Ra2WorldPoint invalid = read_point(0x852998);
    double speed;
    memcpy(&speed, (const void *)(uintptr_t)ADDR(owner + 0x468), 8);
    double zero_speed;
    memcpy(&zero_speed, (const void *)(uintptr_t)ADDR(0x79B610), 8);
    if (same_point(context->state.destination, invalid) && same_point(context->state.segment_end, invalid)
        && MEM32(owner + 0x4D0) == UINT32_MAX && speed > zero_speed)
    {
        uint32_t arguments[2] = { 0, 0 };
        owner_call(context, 0x4C8, arguments, 2);
    }
    return (locomotion_call(context, 0x10, NULL, 0) & 255u) != 0;
}

void ra2_ground_drive_process_bridge(void)
{
    uint32_t stack = g_esp, saved_ebx = g_ebx, saved_esi = g_esi, saved_edi = g_edi, saved_ebp = g_ebp;
    DriveContext context;
    context.interface_address = MEM32(stack + 4);
    context.drive = context.interface_address - 4;
    context.owner = MEM32(context.drive + 0xC);
    context.scratch = stack - 0x100;
    read_state(&context);
    Ra2DriveServices services = { &context, drive_query, restart_surface_timer, advance_segment, prepare_segment,
        target_position, set_destination, refresh_owner_after_turn, stop_navigation, finish_frame };
    g_esp = stack - 0x200;
    g_cur_func = 0x4A05F0;
    int result = ra2_ground_drive_process(&context.state, read_point(0x852998), &services);
    write_state(&context);
    g_eax = (g_eax & 0xFFFFFF00u) | (result != 0);
    g_ebx = saved_ebx;
    g_esi = saved_esi;
    g_edi = saved_edi;
    g_ebp = saved_ebp;
    g_flag_k = FK_ADD;
    g_flag_a = stack - 16;
    g_flag_b = 16;
    g_flag_cf = stack < stack - 16;
    g_esp = stack + 8;
}
