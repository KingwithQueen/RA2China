#include <stdio.h>
#include <stdlib.h>
#include "recomp_types.h"
#include "combat_building_resources.h"
#include "combat_building_resources_bridge.h"

typedef struct ResourceContext { uint32_t building, frame; } ResourceContext;

static uint32_t call(uint32_t target, uint32_t self, const uint32_t *args,
                     unsigned count, unsigned pending)
{
    uint32_t stack = g_esp, caller = g_cur_func;
    for (unsigned i = count; i; --i) { g_esp -= 4; MEM32(g_esp) = args[i - 1]; }
    g_esp -= 4; MEM32(g_esp) = RECOMP_RETADDR; g_ecx = self;
    recomp_func_t fn = recomp_lookup_manual(target);
    if (!fn) fn = recomp_lookup(target);
    if (!fn) fn = recomp_lookup_import(target);
    if (!fn) { fprintf(stderr, "[building resources] unresolved %08X\n", target); abort(); }
    fn();
    if (g_esp != stack + pending * 4u) { fputs("[building resources] stack imbalance\n", stderr); abort(); }
    g_cur_func = caller;
    return g_eax;
}

static int32_t query(void *opaque, Ra2BuildingResourceQuery q)
{
    (void)opaque;
    switch (q) {
        case RA2_BR_HAS_UNIT:
            call(0x69AE10, g_ebp, NULL, 0, 0);
            /* 原查询返回整数值的x87数；小于一或无序比较均跳过。 */
            return fp_pop_impl(g_st, &g_fp_top) >= 1.0;
        case RA2_BR_FIRST_TYPE:
            g_edi = call(0x69AFE0, g_ebp, NULL, 0, 0); return (int32_t)g_edi;
        case RA2_BR_RADIUS: {
            uint32_t args[] = {0x100, 0x300};
            return (int32_t)call(0x6388A0, MEM32(0xA3D290) + 0x218, args, 2, 0);
        }
    }
    abort();
}

static void perform(void *opaque, Ra2BuildingResourceOperation op, int32_t value)
{
    ResourceContext *c = opaque;
    switch (op) {
        case RA2_BR_BEGIN: g_ebx = c->building + 0x88; break;
        case RA2_BR_REMOVE_BUILDING:
        case RA2_BR_REMOVE_OWNER: {
            uint32_t self = op == RA2_BR_REMOVE_BUILDING ? g_ebp : MEM32(c->building + 0x1B4) + 0x23C;
            uint32_t args[] = {0x3F800000u, (uint32_t)value};
            call(0x69AE70, self, args, 2, 0); fp_pop_impl(g_st, &g_fp_top); break;
        }
        case RA2_BR_SCATTER: {
            /* 源地址在循环外捕获，内容在本次RNG之后读取。 */
            uint32_t source = c->frame + 0x1C;
            MEM32(source) = MEM32(g_ebx); MEM32(source + 4) = MEM32(g_ebx + 4);
            MEM32(source + 8) = MEM32(g_ebx + 8);
            uint32_t args[] = {(uint32_t)value, 1}; g_edx = source;
            call(0x491750, c->frame + 0x40, args, 2, 0); break;
        }
        case RA2_BR_PLACE: {
            uint32_t out = g_eax, position = c->frame + 0x10;
            MEM32(position) = MEM32(out); MEM32(position + 4) = MEM32(out + 4);
            MEM32(position + 8) = MEM32(out + 8);
            /* GetCell回调可见已压栈的类型、数量；最终由IncreaseTiberium消费。 */
            g_esp -= 4; MEM32(g_esp) = 1;
            g_esp -= 4; MEM32(g_esp) = (uint32_t)value;
            uint32_t cell = call(0x548000, 0x8324E0, &position, 1, 0);
            call(0x47C3A0, cell, NULL, 0, 2); break;
        }
        case RA2_BR_END: g_ebx = 0; break;
    }
}

void ra2_building_resources_bridge(void)
{
    ResourceContext c = {g_esi, g_esp};
    Ra2BuildingResourceServices s = {&c, query, perform};
    g_ebp = c.building + 0x294;
    ra2_scatter_building_resources(&s);
}
