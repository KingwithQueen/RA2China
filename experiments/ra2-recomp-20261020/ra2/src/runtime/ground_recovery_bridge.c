#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "recomp_types.h"
#include "ground_recovery.h"
#include "ground_recovery_bridge.h"

typedef struct RecoveryContext
{
    uint32_t drive;
    uint32_t frame;
    Ra2GroundRecoveryState state;
} RecoveryContext;

static uint32_t owner_address(RecoveryContext *context)
{
    return MEM32(context->drive + 0x0C);
}

static void read_state(RecoveryContext *context)
{
    uint32_t owner = owner_address(context);
    memcpy(&context->state.segment_end, (const void *)(uintptr_t)ADDR(context->drive + 0x40), 12);
    context->state.path_selector = (int32_t)MEM32(context->drive + 0x58);
    context->state.remaining_failures = (int32_t)MEM32(owner + 0x53C);
    context->state.driving = MEM8(context->drive + 0x63);
    context->state.legacy_flag_61 = MEM8(context->drive + 0x61);
    context->state.legacy_flag_578 = MEM8(owner + 0x578);
    context->state.failure_sound_pending = MEM8(owner + 0x57A);
}

static void write_state(RecoveryContext *context)
{
    uint32_t owner = owner_address(context);
    memcpy((void *)(uintptr_t)ADDR(context->drive + 0x40), &context->state.segment_end, 12);
    MEM32(context->drive + 0x58) = (uint32_t)context->state.path_selector;
    MEM32(owner + 0x53C) = (uint32_t)context->state.remaining_failures;
    MEM8(context->drive + 0x63) = (uint8_t)context->state.driving;
    MEM8(context->drive + 0x61) = (uint8_t)context->state.legacy_flag_61;
    MEM8(owner + 0x578) = (uint8_t)context->state.legacy_flag_578;
    MEM8(owner + 0x57A) = (uint8_t)context->state.failure_sound_pending;
}

static uint32_t engine_call(RecoveryContext *context, uint32_t target, uint32_t ecx, uint32_t edx,
    const uint32_t *arguments, unsigned count)
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
    g_ecx = ecx;
    g_edx = edx;
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
        fprintf(stderr, "[recovery-bridge-error] unresolved operation %08X\n", target);
        abort();
    }
    function();
    if (g_esp != stack)
    {
        fprintf(stderr, "[recovery-bridge-error] unbalanced operation %08X\n", target);
        abort();
    }
    g_cur_func = caller;
    uint32_t result = g_eax;
    read_state(context);
    return result;
}

static uint32_t owner_call(RecoveryContext *context, uint32_t slot, const uint32_t *arguments, unsigned count)
{
    uint32_t owner = owner_address(context);
    return engine_call(context, MEM32(MEM32(owner) + slot), owner, g_edx, arguments, count);
}

static int recovery_query(void *opaque, Ra2RecoveryQuery query)
{
    RecoveryContext *context = opaque;
    uint32_t owner = owner_address(context), argument, interface_address;
    switch (query)
    {
        case RA2_RECOVERY_HAS_TARGET_488: return MEM32(owner + 0x488) != 0;
        case RA2_RECOVERY_OWNER_ALIVE: return MEM8(owner + 0x7D) != 0;
        case RA2_RECOVERY_IS_MOVING:
            interface_address = MEM32(context->frame + 0x14);
            return (engine_call(context, MEM32(MEM32(interface_address) + 0x10), g_ecx, g_edx, &interface_address, 1) & 255u) != 0;
        case RA2_RECOVERY_HAS_OBJECT_228: return MEM32(owner + 0x228) != 0;
        case RA2_RECOVERY_ACCEPTS_OBJECT_228:
            argument = MEM32(owner + 0x228);
            return (owner_call(context, 0x354, &argument, 1) & 255u) != 0;
        default:
            fputs("[recovery-bridge-error] invalid query\n", stderr);
            abort();
    }
}

static int stop_navigation(void *opaque, int target_variant)
{
    RecoveryContext *context = opaque;
    uint32_t arguments[2] = { 0,1 };
    return (int)(owner_call(context, target_variant ? 0x414 : 0x410, arguments, 2) & 255u);
}

static void cancel_target(void *opaque)
{
    RecoveryContext *context = opaque;
    engine_call(context, 0x4CD9B0, owner_address(context), g_edx, NULL, 0);
}

static void play_failure_sound(void *opaque)
{
    RecoveryContext *context = opaque;
    uint32_t arguments[2] = { 0x3F800000,0 };
    engine_call(context, 0x713DB0, MEM32(MEM32(0x839848) + 0x620), 0x2000, arguments, 2);
}

static void notify_linked_objects(void *opaque)
{
    RecoveryContext *context = opaque;
    uint32_t linked = MEM32(owner_address(context) + 0x4C4), zero = 0;
    if (linked)
    {
        engine_call(context, 0x6BAA30, linked, g_edx, NULL, 0);
    }
    owner_call(context, 0x370, &zero, 1);
}

void ra2_ground_recover_path_bridge(int finish_only)
{
    RecoveryContext context = { 0 };
    context.drive = g_ebp;
    context.frame = g_esp;
    read_state(&context);
    Ra2WorldPoint invalid;
    memcpy(&invalid, (const void *)(uintptr_t)ADDR(0x852998), 12);
    g_esp -= 0x100;
    Ra2RecoveryServices services = { &context, recovery_query, stop_navigation, cancel_target, play_failure_sound, notify_linked_objects };
    int result = ra2_ground_recover_path(&context.state, invalid, finish_only, &services);
    write_state(&context);
    g_eax = (g_eax & 0xFFFFFF00u) | (result != 0);
    g_edi = MEM32(context.frame);
    g_esi = MEM32(context.frame + 4);
    g_ebp = MEM32(context.frame + 8);
    g_ebx = MEM32(context.frame + 12);
    g_flag_k = FK_ADD;
    g_flag_a = context.frame + 16;
    g_flag_b = 0x4C;
    g_flag_cf = context.frame + 0x5C < context.frame + 16;
    g_esp = context.frame + 0x6C;
}
