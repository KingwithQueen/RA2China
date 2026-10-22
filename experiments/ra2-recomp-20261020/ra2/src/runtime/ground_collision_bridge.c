#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include "recomp_types.h"
#include "ground_collision.h"
#include "ground_terrain.h"
#include "state_trace.h"
#include "ground_collision_bridge.h"

typedef struct OccupationContext
{
    uint32_t owner;
    uint32_t cell;
    int32_t infantry_owner_index;
} OccupationContext;

int ra2_ground_terrain_tail_bridge(void)
{
    ra2_state_movement_audit(27,g_ebp,g_ebx,g_esp);
    unsigned upper_layer=MEM8(g_esp+0x11);
    uint32_t factor=0;
    if (!upper_layer)
    {
        uint32_t land=MEM32(g_ebx+0xEC), speed_class=MEM32(MEM32(g_ebp+0x5AC)+0x5A4);
        factor=MEM32(0x850EA0+(land*9u+speed_class)*4u);
    }
    return ra2_ground_terrain_speed_is_blocked(upper_layer,factor);
}

int ra2_ground_terrain_bridge(void)
{
    ra2_state_movement_audit(7, g_ebp, g_ebx, 0);
    uint32_t frame = g_esp, cell = g_ebx, type = MEM32(g_ebp + 0x5AC);
    Ra2TerrainConstraint terrain = { (int32_t)MEM32(type + 0xB94), (int32_t)MEM32(cell + 0xEC),
        (int32_t)MEM32(cell + 0x44), (int32_t)MEM32(frame + 0x84), (int8_t)MEM8(cell + 0x11B), 0, 0, MEM8(cell + 0x11A) };
    if (terrain.required_land != -1 && terrain.cell_land == 10)
    {
        uint32_t tile = MEM32(MEM32(0xA40CD4) + MEM32(cell + 0x38) * 4u);
        terrain.tile_property_2b4 = (int32_t)MEM32(tile + 0x2B4);
        terrain.tile_property_2b8 = (int32_t)MEM32(tile + 0x2B8);
    }
    if (!ra2_ground_terrain_is_blocked(&terrain))
    {
        if (terrain.required_land != -1)
        {
            g_edi = (uint32_t)terrain.cell_land;
        }
        return 1;
    }
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

static uint32_t engine_call(uint32_t target, uint32_t object, uint32_t argument)
{
    uint32_t stack = g_esp, caller = g_cur_func;
    g_esp -= 4;
    MEM32(g_esp) = argument;
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
        fprintf(stderr, "[collision-bridge-error] unresolved operation %08X\n", target);
        abort();
    }
    function();
    if (g_esp != stack)
    {
        fprintf(stderr, "[collision-bridge-error] unbalanced operation %08X\n", target);
        abort();
    }
    g_cur_func = caller;
    return g_eax;
}

static int occupation_query(void *opaque, Ra2OccupationQuery query)
{
    OccupationContext *context = opaque;
    uint32_t owner = context->owner, holder, weapon, unit;
    switch (query)
    {
        case RA2_OCCUPATION_INFANTRY_ALLIED:
            return (engine_call(0x4E5500, MEM32(owner + 0x1B4), (uint32_t)context->infantry_owner_index) & 255u) != 0;
        case RA2_OCCUPATION_CRUSHER_ABILITY:
            return (engine_call(0x6D7910, owner, 17) & 255u) != 0;
        case RA2_OCCUPATION_HAS_WEAPON:
            holder = engine_call(MEM32(MEM32(owner) + 0x39C), owner, 0);
            return MEM32(holder) != 0;
        case RA2_OCCUPATION_WEAPON_CAN_CLEAR:
            holder = engine_call(MEM32(MEM32(owner) + 0x39C), owner, 0);
            weapon = MEM32(holder);
            return MEM8(MEM32(weapon + 0xA0) + 0x275) != 0;
        case RA2_OCCUPATION_VEHICLE_CRUSHABLE:
            unit = engine_call(0x473E30, context->cell, 0);
            if (!unit)
            {
                return 0;
            }
            /* 原版会再次查询，保留查询顺序，而不是把第一次的结果直接复用。 */
            unit = engine_call(0x473E30, context->cell, 0);
            return MEM8(MEM32(unit + 0x5AC) + 0x1FD) != 0;
        default:
            fputs("[collision-bridge-error] invalid occupation query\n", stderr);
            abort();
    }
}

void ra2_ground_collision_finish_bridge(void)
{
    uint32_t stack = g_esp, owner = g_ebp, type = MEM32(owner + 0x5AC);
    OccupationContext context = { owner, g_ebx, (int32_t)MEM32(stack + 0x18) };
    Ra2CellOccupation occupation = { (int32_t)g_edi, MEM8(stack + 0x12), MEM8(stack + 0x13), context.infantry_owner_index,
        MEM8(stack + 0x88), MEM8(type + 0xAF3), MEM8(type + 0xAA0) };
    Ra2CellPassage result = ra2_ground_resolve_occupation(&occupation, &context, occupation_query);
    g_eax = (uint32_t)result;
    g_edi = MEM32(stack);
    g_esi = MEM32(stack + 4);
    g_ebp = MEM32(stack + 8);
    g_ebx = MEM32(stack + 12);
    g_flag_k = FK_ADD;
    g_flag_a = stack + 16;
    g_flag_b = 0x68;
    g_flag_cf = stack + 0x78 < stack + 16;
    g_esp = stack + 0x90;
}
