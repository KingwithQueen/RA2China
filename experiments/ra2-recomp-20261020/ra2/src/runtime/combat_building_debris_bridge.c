#include <stdio.h>
#include <stdlib.h>
#include "recomp_types.h"
#include "combat_building_debris.h"
#include "combat_building_debris_bridge.h"

typedef struct DebrisContext {
    uint32_t building, frame, upper, lower, maximum_slot;
} DebrisContext;

static uint32_t call(uint32_t target, uint32_t self, const uint32_t *args,
                     unsigned count, unsigned caller_cleanup)
{
    uint32_t stack = g_esp, caller = g_cur_func;
    for (unsigned i = count; i; --i) { g_esp -= 4; MEM32(g_esp) = args[i - 1]; }
    g_esp -= 4; MEM32(g_esp) = RECOMP_RETADDR; g_ecx = self;
    recomp_func_t fn = recomp_lookup_manual(target);
    if (!fn) fn = recomp_lookup(target);
    if (!fn) fn = recomp_lookup_import(target);
    if (!fn) { fprintf(stderr, "[building debris] unresolved %08X\n", target); abort(); }
    fn();
    if (caller_cleanup) g_esp += count * 4;
    if (g_esp != stack) { fputs("[building debris] stack imbalance\n", stderr); abort(); }
    g_cur_func = caller;
    return g_eax;
}

static uint32_t vcall(DebrisContext *c, unsigned slot, const uint32_t *args, unsigned count)
{ return call(MEM32(MEM32(c->building) + slot), c->building, args, count, 0); }
static uint32_t current_type(DebrisContext *c) { return vcall(c, 0x80, NULL, 0); }
static uint32_t random_object(void) { return MEM32(0xA3D290) + 0x218; }
static uint32_t ranged(uint32_t lower, uint32_t upper)
{ uint32_t args[] = {lower, upper}; return call(0x6388A0, random_object(), args, 2, 0); }
static uint32_t allocate(uint32_t size) { return call(0x782017, g_ecx, &size, 1, 1); }

static int32_t query(void *opaque, Ra2BuildingDebrisQuery q)
{
    DebrisContext *c = opaque;
    switch (q) {
        case RA2_BD_MAXIMUM_GATE: return (int32_t)MEM32(current_type(c) + 0x508);
        case RA2_BD_MAXIMUM_UPPER:
            c->upper = g_edi = MEM32(current_type(c) + 0x508) - 1u;
            return (int32_t)c->upper;
        case RA2_BD_MINIMUM:
            c->lower = MEM32(current_type(c) + 0x50C); return (int32_t)c->lower;
        case RA2_BD_DRAW_TOTAL:
            g_ebx = ranged(c->lower, c->upper); MEM32(c->frame + 0x14) = g_ebx;
            return (int32_t)g_ebx;
        case RA2_BD_VOXEL_COUNT: return (int32_t)MEM32(current_type(c) + 0x2F4);
        case RA2_BD_VOXEL_RANDOM: {
            /* RNG对象先于类型回调捕获，配额槽先于抽样捕获，槽值在抽样后读取。 */
            uint32_t rng = random_object(); MEM32(c->frame + 0x24) = rng;
            uint32_t type = current_type(c); g_ebp = g_edi * 4u;
            c->maximum_slot = g_edi = MEM32(type + 0x304) + g_ebp;
            return (int32_t)call(0x638840, rng, NULL, 0, 0);
        }
        case RA2_BD_CAPTURED_VOXEL_MAXIMUM: return (int32_t)MEM32(c->maximum_slot);
        case RA2_BD_CUSTOM_COUNT: return (int32_t)MEM32(current_type(c) + 0x520);
        case RA2_BD_DEFAULT_ALLOWED: return MEM32(current_type(c) + 0x2F4) == 0;
    }
    abort();
}

static void emit_voxels(DebrisContext *c, uint32_t count)
{
    MEM32(c->frame + 0x54) = count;
    do {
        g_ebx = allocate(0x130);
        if (g_ebx) {
            uint32_t type = current_type(c);
            g_edi = MEM32(type + 0x2E8) + g_ebp;
            uint32_t house = MEM32(c->building + 0x1B4);
            /* 原调用在坐标回调前将归属压栈；类型槽值在坐标回调后读取。 */
            g_esp -= 4; MEM32(g_esp) = house;
            uint32_t out = c->frame + 0xAC, position = vcall(c, 0x48, &out, 1);
            g_esp += 4;
            uint32_t args[] = {MEM32(g_edi), position, house};
            call(0x70C800, g_ebx, args, 3, 0);
        }
        --count; MEM32(c->frame + 0x54) = count;
    } while (count);
}

static void emit_animation(DebrisContext *c, unsigned use_default)
{
    uint32_t storage = allocate(0x1A8);
    if (use_default) g_edi = storage; else g_ebx = storage;
    if (storage) {
        uint32_t out = c->frame + (use_default ? 0x30 : 0xB8);
        uint32_t position = vcall(c, 0x48, &out, 1);
        uint32_t copy = c->frame + (use_default ? 0x94 : 0x88);
        MEM32(copy) = MEM32(position); MEM32(copy + 4) = MEM32(position + 4);
        MEM32(copy + 8) = MEM32(position + 8) + 20u;
        uint32_t upper = use_default ? MEM32(MEM32(0x839848) + 0x144) - 1u
                                     : MEM32(current_type(c) + 0x520) - 1u;
        uint32_t index = ranged(0, upper), list;
        if (use_default) list = MEM32(MEM32(0x839848) + 0x138);
        else { g_edi = index; list = MEM32(current_type(c) + 0x514); }
        uint32_t args[] = {MEM32(list + index * 4u), copy, 0, 1, 0x600, 0};
        call(0x420110, storage, args, 6, 0);
    }
    if (use_default) --g_ebx; else --g_ebp;
}

static void perform(void *opaque, Ra2BuildingDebrisOperation op, int32_t value)
{
    DebrisContext *c = opaque;
    switch (op) {
        case RA2_BD_BEGIN_VOXELS: g_edi = 0; MEM32(c->frame + 0x2C) = 0; break;
        case RA2_BD_PUBLISH_QUOTA: MEM32(c->frame + 0x24) = (uint32_t)value; break;
        case RA2_BD_EMIT_VOXELS: emit_voxels(c, (uint32_t)value); break;
        case RA2_BD_ADVANCE_VOXEL: {
            g_ebx = (uint32_t)value; g_edi = MEM32(c->frame + 0x2C) + 1u;
            MEM32(c->frame + 0x14) = g_ebx; MEM32(c->frame + 0x2C) = g_edi;
            int32_t count = (int32_t)MEM32(current_type(c) + 0x2F4);
            if ((int32_t)g_edi >= count) { g_edi = 0; MEM32(c->frame + 0x2C) = 0; }
            break;
        }
        case RA2_BD_BEGIN_CUSTOM: g_ebp = (uint32_t)value; break;
        case RA2_BD_EMIT_CUSTOM: emit_animation(c, 0); break;
        case RA2_BD_EMIT_DEFAULT: emit_animation(c, 1); break;
    }
}

void ra2_building_debris_bridge(void)
{
    DebrisContext c = {g_esi, g_esp, 0, 0, 0};
    Ra2BuildingDebrisServices s = {&c, query, perform};
    ra2_generate_building_debris(&s);
}
