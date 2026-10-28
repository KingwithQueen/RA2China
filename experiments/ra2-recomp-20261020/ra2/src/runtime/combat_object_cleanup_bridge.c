#include "combat_object_cleanup_tables.h"
#include "combat_object_cleanup_tables_bridge.h"
#include "combat_object_cleanup.h"
#include "combat_object_cleanup_bridge.h"
#include "recomp_types.h"
#include <stdio.h>
#include <stdlib.h>

static int32_t object_compare(uint32_t left, uint32_t right)
{
    g_flag_k = FK_CMP; g_flag_a = left; g_flag_b = right; g_flag_cf = left < right;
    return (int32_t)left < (int32_t)right;
}

static void object_begin(void *opaque)
{
    (void)opaque;
    /* 保留Object原保存帧，后续登记表仍共用原对象临时槽。 */
    g_esp -= 4; MEM32(g_esp) = g_ecx; g_esp -= 4; MEM32(g_esp) = g_esi;
    g_esi = g_ecx; g_eax = g_esp + 4; g_ecx = 0xAC0CD8;
    MEM32(g_esi) = 0x7A7498; MEM32(g_esi + 4) = 0x7A747C;
    MEM32(g_esi + 8) = 0x7A7474; MEM32(g_esi + 0x0C) = 0x7A746C;
}

static int32_t object_find(void *opaque)
{
    (void)opaque;
    g_edx = MEM32(0xAC0CD8);
    g_esp -= 4; MEM32(g_esp) = g_eax; MEM32(g_esp + 8) = g_esi;
    uint32_t argument_frame = g_esp, caller = g_cur_func, target = MEM32(g_edx + 0x10);
    g_icall_trace[g_icall_trace_idx & (ICALL_TRACE_SIZE - 1)] = target;
    g_icall_from[g_icall_trace_idx & (ICALL_TRACE_SIZE - 1)] = caller;
    ++g_icall_trace_idx; ++g_icall_count;
    recomp_func_t fn = recomp_lookup_manual(target);
    if (!fn) fn = recomp_lookup(target);
    if (!fn) fn = recomp_lookup_import(target);
    if (!fn) { fprintf(stderr, "[object registry] unresolved %08X\n", target); abort(); }
    g_esp -= 4; MEM32(g_esp) = RECOMP_RETADDR; fn();
    if (g_esp != argument_frame + 4) { fputs("[object registry] stack imbalance\n", stderr); abort(); }
    g_cur_func = caller;
    (void)object_compare(g_eax, UINT32_MAX);
    return (int32_t)g_eax;
}

static int32_t object_can_remove(void *opaque)
{
    (void)opaque;
    g_ecx = MEM32(0xAC0CE8);
    return object_compare(g_eax, g_ecx);
}

static int32_t object_shrink_has_following(void *opaque)
{
    (void)opaque;
    --g_ecx;
    int32_t following = object_compare(g_eax, g_ecx);
    MEM32(0xAC0CE8) = g_ecx;
    return following;
}

static int32_t object_shift_next(void *opaque)
{
    (void)opaque;
    /* 与原循环一致：每次重读表数据和计数，不缓存或清尾槽。 */
    g_ecx = MEM32(0xAC0CDC); ++g_eax;
    g_edx = MEM32(g_ecx + g_eax * 4); MEM32(g_ecx + g_eax * 4 - 4) = g_edx;
    g_ecx = MEM32(0xAC0CE8);
    int32_t following = object_compare(g_eax, g_ecx);
    if (++g_backedges >= RECOMP_YIELD_EVERY && recomp_yield_hook) {
        uint32_t kind = g_flag_k, left = g_flag_a, right = g_flag_b, carry = g_flag_cf;
        g_backedges = 0; recomp_yield_hook();
        /* 原backedge只同步通用寄存器，分支仍使用让出前的局部比较结果。 */
        g_flag_k = kind; g_flag_a = left; g_flag_b = right; g_flag_cf = carry;
    }
    return following;
}

void ra2_object_cleanup_registry_bridge(void)
{
    Ra2ObjectCleanupServices s = {NULL, object_begin, object_find, object_can_remove,
        object_shrink_has_following, object_shift_next};
    ra2_cleanup_object_registry(&s);
}

typedef struct ObjectTablesContext { uint32_t registry, index; } ObjectTablesContext;
static const uint32_t object_tables_addresses[] = {0xA40368, 0xAC0D60, 0xAC0CB0, 0xAC0C58};

static void object_tables_select(void *opaque, uint32_t table)
{
    ObjectTablesContext *c = opaque;
    c->registry = object_tables_addresses[table]; c->index = table;
}

static void object_tables_begin(void *opaque)
{
    (void)opaque;
    /* 首表已建立Object保存帧，后四表不重复保存或切Object虚表。 */
}

static int32_t object_tables_find(void *opaque)
{
    ObjectTablesContext *c = opaque;
    /* 按当前表的原顺序读虚表、定位参数并重写对象临时槽。 */
    g_edx = MEM32(c->registry); g_eax = g_esp + 4;
    g_esp -= 4; MEM32(g_esp) = g_eax; g_ecx = c->registry; MEM32(g_esp + 8) = g_esi;
    uint32_t argument_frame = g_esp, caller = g_cur_func, target = MEM32(g_edx + 0x10);
    g_icall_trace[g_icall_trace_idx & (ICALL_TRACE_SIZE - 1)] = target;
    g_icall_from[g_icall_trace_idx & (ICALL_TRACE_SIZE - 1)] = caller;
    ++g_icall_trace_idx; ++g_icall_count;
    recomp_func_t fn = recomp_lookup_manual(target);
    if (!fn) fn = recomp_lookup(target);
    if (!fn) fn = recomp_lookup_import(target);
    if (!fn) { fprintf(stderr, "[object tables] unresolved %08X\n", target); abort(); }
    g_esp -= 4; MEM32(g_esp) = RECOMP_RETADDR; fn();
    if (g_esp != argument_frame + 4) { fputs("[object tables] stack imbalance\n", stderr); abort(); }
    g_cur_func = caller;
    /* 后四表的原查找返回点。 */
    (void)object_compare(g_eax, 0xFFFFFFFFu);
    return (int32_t)g_eax;
}

static int32_t object_tables_can_remove(void *opaque)
{
    ObjectTablesContext *c = opaque;
    g_ecx = MEM32(c->registry + 0x10);
    return object_compare(g_eax, g_ecx);
}

static int32_t object_tables_shrink(void *opaque)
{
    ObjectTablesContext *c = opaque;
    --g_ecx;
    int32_t following = object_compare(g_eax, g_ecx);
    MEM32(c->registry + 0x10) = g_ecx;
    return following;
}

static int32_t object_tables_shift(void *opaque)
{
    ObjectTablesContext *c = opaque;
    g_ecx = MEM32(c->registry + 4); ++g_eax;
    g_edx = MEM32(g_ecx + g_eax * 4); MEM32(g_ecx + g_eax * 4 - 4) = g_edx;
    g_ecx = MEM32(c->registry + 0x10);
    int32_t following = object_compare(g_eax, g_ecx);
    if (++g_backedges >= RECOMP_YIELD_EVERY && recomp_yield_hook) {
        uint32_t kind = g_flag_k, left = g_flag_a, right = g_flag_b, carry = g_flag_cf;
        g_backedges = 0; recomp_yield_hook();
        g_flag_k = kind; g_flag_a = left; g_flag_b = right; g_flag_cf = carry;
    }
    return following;
}

void ra2_object_cleanup_tables_bridge(void)
{
    ObjectTablesContext c = {0, 0};
    Ra2ObjectTablesCleanupServices s = {&c, object_tables_select,
        {&c, object_tables_begin, object_tables_find, object_tables_can_remove,
        object_tables_shrink, object_tables_shift}};
    ra2_cleanup_object_tables(&s);
}
