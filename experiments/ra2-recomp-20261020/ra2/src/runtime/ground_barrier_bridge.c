#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include "recomp_types.h"
#include "ground_barrier.h"
#include "ground_barrier_bridge.h"

typedef struct BarrierContext
{
    uint32_t actor;
    uint32_t cell;
    uint32_t overlay_type;
    uint32_t building;
} BarrierContext;

static uint32_t engine_call(uint32_t target, uint32_t object, const uint32_t *arguments, unsigned count)
{
    uint32_t stack = g_esp, caller = g_cur_func;
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
        fprintf(stderr, "[barrier-bridge-error] unresolved operation %08X\n", target);
        abort();
    }
    function();
    if (g_esp != stack)
    {
        fprintf(stderr, "[barrier-bridge-error] unbalanced operation %08X\n", target);
        abort();
    }
    g_cur_func = caller;
    return g_eax;
}

static int barrier_query(void *opaque, Ra2BarrierQuery query)
{
    BarrierContext *context = opaque;
    uint32_t actor = context->actor, argument, holder, weapon, warhead;
    switch (query)
    {
        case RA2_BARRIER_HOUSE_CRATE_PERMISSION:
            return (engine_call(0x4F52F0, MEM32(actor + 0x1B4), NULL, 0) & 255u) != 0;
        case RA2_BARRIER_GLOBAL_CRATE_MODE: return MEM32(0xA3D298) != 0;
        case RA2_BARRIER_CRUSHER_ABILITY:
            argument = 17;
            return (engine_call(0x6D7910, actor, &argument, 1) & 255u) != 0;
        case RA2_BARRIER_WALL_OWNER_ALLIED:
            argument = MEM32(context->cell + 0x50);
            return (engine_call(0x4E5500, MEM32(actor + 0x1B4), &argument, 1) & 255u) != 0;
        case RA2_BARRIER_ACTOR_CAN_ATTACK:
            return (engine_call(MEM32(MEM32(actor) + 0x28C), actor, NULL, 0) & 255u) != 0;
        case RA2_BARRIER_WEAPON_WALL_FLAGS:
            argument = 0;
            holder = engine_call(MEM32(MEM32(actor) + 0x39C), actor, &argument, 1);
            weapon = MEM32(holder);
            warhead = MEM32(weapon + 0xAC);
            /* 字段名称尚未核实，保留本机原版条件；不能套用其他版本的 INI 命名。 */
            return (MEM8(warhead + 0x144) != 0) | ((MEM8(warhead + 0x146) != 0) << 1);
        case RA2_BARRIER_GATE_PASSABLE:
            return (engine_call(0x44D880, context->building, NULL, 0) & 255u) != 0;
        case RA2_BARRIER_GATE_OWNER_ALLIED:
            argument = MEM32(actor + 0x1B4);
            return (engine_call(0x4E5540, MEM32(context->building + 0x1B4), &argument, 1) & 255u) != 0;
        default:
            fputs("[barrier-bridge-error] invalid query\n", stderr);
            abort();
    }
}

static uint32_t return_blocked(uint32_t frame)
{
    g_eax = 7;
    g_edi = MEM32(frame);
    g_esi = MEM32(frame + 4);
    g_ebp = MEM32(frame + 8);
    g_ebx = MEM32(frame + 12);
    g_flag_k = FK_ADD;
    g_flag_a = frame + 16;
    g_flag_b = 0x68;
    g_flag_cf = frame + 0x78 < frame + 16;
    g_esp = frame + 0x90;
    return 0;
}

uint32_t ra2_ground_overlay_bridge(void)
{
    uint32_t frame = g_esp;
    int32_t previous = (int32_t)g_edi;
    BarrierContext context = { g_ebp,g_ebx,0,0 };
    Ra2OverlayBarrier overlay = { 0 };
    int32_t index = (int32_t)MEM32(context.cell + 0x44);
    if (index != -1)
    {
        context.overlay_type = MEM32(MEM32(0xA35DEC) + (uint32_t)index * 4u);
        overlay.present = 1;
        overlay.is_crate = MEM8(context.overlay_type + 0x27A);
        overlay.is_wall = MEM8(context.overlay_type + 0x278);
        overlay.is_crushable = MEM8(context.overlay_type + 0x1FD);
        overlay.actor_is_crusher = MEM8(MEM32(context.actor + 0x5AC) + 0xAF3);
        overlay.armor = (int32_t)MEM32(context.overlay_type + 0x9C);
    }
    g_esp = frame - 0x80;
    Ra2BarrierResult result = ra2_ground_check_overlay(overlay, previous, &context, barrier_query);
    if (result.outcome == RA2_BARRIER_BLOCKED)
    {
        return return_blocked(frame);
    }
    if (result.passage != previous)
    {
        MEM32(frame + 0x8C) = (uint32_t)result.passage;
    }
    g_esp = frame;
    g_ebp = context.actor;
    g_ebx = context.cell;
    g_edi = (uint32_t)result.passage;
    return 0x703439;
}

uint32_t ra2_ground_gate_bridge(void)
{
    uint32_t frame = g_esp, building = g_esi, type = MEM32(building + 0x418);
    int32_t previous = (int32_t)g_edi;
    BarrierContext context = { g_ebp,g_ebx,0,building };
    g_esp = frame - 0x80;
    Ra2BarrierResult result = ra2_ground_check_gate(MEM8(type + 0x1351), previous, &context, barrier_query);
    if (result.outcome == RA2_BARRIER_BLOCKED)
    {
        return return_blocked(frame);
    }
    if (result.passage != previous)
    {
        MEM32(frame + 0x8C) = (uint32_t)result.passage;
    }
    g_esp = frame;
    g_ebp = context.actor;
    g_ebx = context.cell;
    g_edi = (uint32_t)result.passage;
    if (result.outcome == RA2_BARRIER_NOT_GATE)
    {
        g_eax = type;
        g_esi = building;
        return 0x7035AC;
    }
    g_esi = MEM32(building + 0x30);
    return 0x7038FD;
}
