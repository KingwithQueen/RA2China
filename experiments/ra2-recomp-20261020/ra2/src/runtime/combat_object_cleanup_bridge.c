#include "combat_control_set_bridge.h"
#include "combat_control_tail_bridge.h"
#include "combat_control_dispatch_bridge.h"
#include "combat_reference_count_bridge.h"
#include "combat_reference_exit_bridge.h"
#include "combat_reference_list_bridge.h"
#include "combat_reference_controller_bridge.h"
#include "combat_reference_prefix_bridge.h"
#include "combat_object_cleanup_base.h"
#include "combat_object_cleanup_base_bridge.h"
#include "combat_object_cleanup_members.h"
#include "combat_object_cleanup_members_bridge.h"
#include "combat_object_cleanup_tables.h"
#include "combat_object_cleanup_tables_bridge.h"
#include "combat_object_cleanup.h"
#include "combat_object_cleanup_bridge.h"
#include "recomp_types.h"
#include <stdio.h>
#include <stdlib.h>

static void object_base_invoke(recomp_func_t fn);

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

static void object_members_invoke(uint32_t target)
{
    uint32_t stack = g_esp, caller = g_cur_func;
    recomp_func_t fn = recomp_lookup_manual(target);
    if (!fn) fn = recomp_lookup(target);
    if (!fn) fn = recomp_lookup_import(target);
    if (!fn) { fprintf(stderr, "[object members] unresolved %08X\n", target); abort(); }
    g_esp -= 4; MEM32(g_esp) = RECOMP_RETADDR; fn();
    if (g_esp != stack) { fputs("[object members] stack imbalance\n", stderr); abort(); }
    g_cur_func = caller;
}

static void object_members_begin(void *opaque)
{
    (void)opaque;
    g_esp -= 4; MEM32(g_esp) = g_ebp; g_esp -= 4; MEM32(g_esp) = g_edi;
    g_edi = g_esi + 0x3C;
    MEM32(g_esi + 0x30) = 0; g_ecx = g_edi; MEM8(g_esi + 0x7D) = 0;
}

static void object_members_step(void *opaque, uint32_t step)
{
    (void)opaque;
    /* 后续成员的地址与当前寄存器均按原调用点读取。 */
    if (step == 1) { g_ebp = g_esi + 0x50; g_ecx = g_ebp; }
    else if (step == 2) g_ecx = g_edi;
    else if (step == 3) g_ecx = g_ebp;
    object_members_invoke(step < 2 ? 0x405D50 : 0x405C10);
}

static int32_t object_members_restore_has_optional(void *opaque)
{
    (void)opaque;
    g_ecx = MEM32(g_esi + 0x94);
    g_edi = MEM32(g_esp); g_esp += 4;
    g_flag_k = FK_TEST; g_flag_a = g_ecx; g_flag_b = g_ecx; g_flag_cf = 0;
    g_ebp = MEM32(g_esp); g_esp += 4;
    return g_ecx != 0;
}

static void object_members_cleanup_optional(void *opaque)
{
    (void)opaque;
    object_base_invoke(ra2_object_detach_association_bridge);
}

static void object_members_clear_optional(void *opaque)
{
    (void)opaque;
    /* 回调返回后清原槽，即使回调换入了另一成员也不追加清理。 */
    MEM32(g_esi + 0x94) = 0;
}

static void object_members_cleanup_abstract(void *opaque)
{
    (void)opaque;
    g_ecx = g_esi;
    object_base_invoke(ra2_object_abstract_tables_bridge);
}

void ra2_object_cleanup_members_bridge(void)
{
    Ra2ObjectMembersCleanupServices s = {NULL, object_members_begin, object_members_step,
        object_members_restore_has_optional, object_members_cleanup_optional,
        object_members_clear_optional, object_members_cleanup_abstract};
    ra2_cleanup_object_members(&s);
}

static uint32_t object_association_owner(void *opaque)
{
    (void)opaque;
    g_eax = MEM32(g_ecx + 4); g_edx = 0;
    (void)object_compare(g_eax, g_edx);
    return g_eax;
}

static void object_clear_owner_link(void *opaque, uint32_t owner)
{
    (void)opaque;
    MEM32(owner + 0x94) = g_edx;
}

static void object_clear_member_link(void *opaque)
{
    (void)opaque;
    MEM32(g_ecx + 4) = g_edx;
}

static void object_write_abstract_table(void *opaque, uint32_t offset, uint32_t table)
{
    (void)opaque;
    MEM32(g_ecx + offset) = table;
}

static const Ra2ObjectBaseCleanupServices object_base_services = {
    NULL, object_association_owner, object_clear_owner_link,
    object_clear_member_link, object_write_abstract_table};

void ra2_object_detach_association_bridge(void)
{
    g_cur_func = 0x5394F0;
#ifdef RECOMP_TRACE
    recomp_trace_enter(0x5394F0);
#endif
    ra2_detach_object_association(&object_base_services);
    g_esp += 4;
}

void ra2_object_abstract_tables_bridge(void)
{
    g_cur_func = 0x40FF90;
#ifdef RECOMP_TRACE
    recomp_trace_enter(0x40FF90);
#endif
    ra2_reset_abstract_tables(&object_base_services);
    g_esp += 4;
}

static void object_base_invoke(recomp_func_t fn)
{
    uint32_t stack = g_esp, caller = g_cur_func;
    g_esp -= 4; MEM32(g_esp) = RECOMP_RETADDR; fn();
    if (g_esp != stack) { fputs("[object base] stack imbalance\n", stderr); abort(); }
    g_cur_func = caller;
}

static void reference_prefix_begin(void *opaque)
{
    (void)opaque;
    g_esp -= 4; MEM32(g_esp) = g_ecx; g_eax = g_ecx;
    g_esp -= 4; MEM32(g_esp) = g_ebp;
    g_ecx = MEM32(0x830FB8); g_ebp = 0;
    (void)object_compare(g_ecx, g_ebp);
    g_esp -= 4; MEM32(g_esp) = g_esi; MEM32(g_esp + 8) = g_eax;
}

static int32_t reference_prefix_active(void *opaque)
{
    (void)opaque;
    return g_ecx != g_ebp;
}

static int32_t reference_prefix_manager(void *opaque)
{
    (void)opaque;
    uint32_t manager = MEM32(g_eax + 0xC);
    (void)object_compare(manager, 0x830FAC);
    return manager == 0x830FAC;
}

static int32_t reference_prefix_has_reference(void *opaque)
{
    (void)opaque;
    g_esi = MEM32(g_eax);
    (void)object_compare(g_esi, g_ebp);
    return g_esi != g_ebp;
}

static int32_t reference_prefix_first_stamp(void *opaque)
{
    (void)opaque;
    g_ecx = MEM32(g_eax + 8); g_edx = MEM32(g_esi + 0x24);
    (void)object_compare(g_ecx, g_edx);
    return g_ecx == g_edx;
}

static int32_t reference_prefix_second_stamp(void *opaque)
{
    (void)opaque;
    g_edx = MEM32(g_eax + 4); g_ecx = MEM32(g_esi + 0x138);
    (void)object_compare(g_edx, g_ecx);
    return g_edx == g_ecx;
}

static int32_t reference_prefix_is_dead(void *opaque)
{
    (void)opaque;
    g_flag_a = (uint32_t)MEM8(g_esi + 0x18) << 24; g_flag_b = 1u << 24;
    g_flag_cf = 0; g_flag_k = FK_NARROW(FK_TEST, 24);
    return (g_flag_a & g_flag_b) != 0;
}

uint32_t ra2_reference_prefix_bridge(uint32_t variant)
{
    (void)variant;
    const Ra2ReferencePrefixServices s = {NULL, reference_prefix_begin, reference_prefix_active,
        reference_prefix_manager, reference_prefix_has_reference, reference_prefix_first_stamp,
        reference_prefix_second_stamp, reference_prefix_is_dead};
    return ra2_check_reference_prefix(&s);
}

void sub_004025B0(void);
void sub_004026F0(void);

static int32_t reference_controller_present(void *opaque)
{
    (void)opaque;
    g_ecx = MEM32(g_esi + 0xB0);
    (void)object_compare(g_ecx, g_ebp);
    return g_ecx != g_ebp;
}

static int32_t reference_controller_owns(void *opaque)
{
    (void)opaque;
    uint32_t owner = MEM32(g_ecx + 0xC0);
    (void)object_compare(g_esi, owner);
    return g_esi == owner;
}

static int32_t reference_controller_needs_cancel(void *opaque)
{
    (void)opaque;
    g_flag_a = (uint32_t)MEM8(g_esi + 0x18) << 24; g_flag_b = 2u << 24;
    g_flag_cf = 0; g_flag_k = FK_NARROW(FK_TEST, 24);
    return (g_flag_a & g_flag_b) != 0;
}

static void reference_controller_cancel(void *opaque)
{
    (void)opaque;
    object_base_invoke(sub_004025B0);
}

static void reference_controller_release(void *opaque)
{
    (void)opaque;
    g_ecx = MEM32(g_esi + 0xB0);
    object_base_invoke(sub_004026F0);
}

static void reference_controller_clear_field(void *opaque, uint32_t offset)
{
    (void)opaque;
    /* 前一存储也可能与+B0重叠；逐项重读并保留原寄存器写入顺序。 */
    uint32_t controller = MEM32(g_esi + 0xB0);
    if (offset == 0xC0 || offset == 0xB8 || offset == 0x9C) g_eax = controller;
    else if (offset == 0xBC || offset == 0x90) g_ecx = controller;
    else g_edx = controller;
    MEM32(controller + offset) = g_ebp;
}

static void reference_controller_clear_link(void *opaque)
{
    (void)opaque;
    g_eax = MEM32(g_esp + 8);
    MEM32(g_esi + 0xB0) = g_ebp;
}

void ra2_reference_controller_bridge(void)
{
    const Ra2ReferenceControllerServices s = {NULL, reference_controller_present,
        reference_controller_owns, reference_controller_needs_cancel, reference_controller_cancel,
        reference_controller_release, reference_controller_clear_field, reference_controller_clear_link};
    ra2_cleanup_reference_controller(&s);
}

void sub_00401F90(void);

static int32_t reference_list_begin(void *opaque)
{
    (void)opaque;
    g_ecx = MEM32(g_esi + 0xA8);
    g_esp -= 4; MEM32(g_esp) = g_ebx; g_ebx = 0;
    (void)object_compare(g_ecx, g_ebp);
    return (int32_t)g_ecx > (int32_t)g_ebp;
}

static void reference_list_begin_items(void *opaque)
{
    (void)opaque;
    g_esp -= 4; MEM32(g_esp) = g_edi;
    g_edi = g_esi + 0x28;
}

static void reference_list_release(void *opaque)
{
    (void)opaque;
    g_ecx = MEM32(g_edi);
    object_base_invoke(sub_00401F90);
}

static int32_t reference_list_advance(void *opaque)
{
    (void)opaque;
    uint32_t prior_kind = g_flag_k, prior_left = g_flag_a, prior_right = g_flag_b, prior_carry = g_flag_cf;
    MEM32(g_edi) = g_ebp;
    g_eax = MEM32(g_esi + 0xA8);
    ++g_ebx; g_edi += 4;
    int32_t following = object_compare(g_ebx, g_eax);
    if (++g_backedges >= RECOMP_YIELD_EVERY && recomp_yield_hook) {
        uint32_t left = g_flag_a, right = g_flag_b, carry = g_flag_cf;
        /* 原backedge不刷新全局标志，分支仍使用让出前的局部CMP结果。 */
        g_flag_k = prior_kind; g_flag_a = prior_left; g_flag_b = prior_right; g_flag_cf = prior_carry;
        g_backedges = 0; recomp_yield_hook();
        g_flag_k = FK_CMP; g_flag_a = left; g_flag_b = right; g_flag_cf = carry;
    }
    return following;
}

static void reference_list_end_items(void *opaque)
{
    (void)opaque;
    g_eax = MEM32(g_esp + 0x10);
    g_edi = MEM32(g_esp); g_esp += 4;
}

static void reference_list_clear_field(void *opaque, uint32_t offset)
{
    (void)opaque;
    MEM32(g_esi + offset) = g_ebp;
}

static void reference_list_write_state(void *opaque, uint32_t state)
{
    (void)opaque;
    MEM32(g_esi + 0x1C) = state;
}

static void reference_list_mark_dead(void *opaque)
{
    (void)opaque;
    g_ecx = MEM32(g_esi + 0x18) | 1u;
    g_flag_k = FK_TEST; g_flag_a = g_ecx; g_flag_b = g_ecx; g_flag_cf = 0;
    MEM32(g_esi + 0x18) = g_ecx;
}

static void reference_list_restore_counter(void *opaque)
{
    (void)opaque;
    g_ebx = MEM32(g_esp); g_esp += 4;
}

void ra2_reference_list_bridge(void)
{
    const Ra2ReferenceListServices s = {NULL, reference_list_begin, reference_list_begin_items,
        reference_list_release, reference_list_advance, reference_list_end_items,
        reference_list_clear_field, reference_list_write_state, reference_list_mark_dead,
        reference_list_restore_counter};
    ra2_cleanup_reference_list(&s);
}

static void reference_exit_clear_field(void *opaque, uint32_t offset)
{
    (void)opaque;
    MEM32(g_eax + offset) = g_ebp;
}

static void reference_exit_restore(void *opaque)
{
    (void)opaque;
    /* 清槽可能改写保存值；按原顺序逐项弹出，不提前缓存保存帧。 */
    g_esi = MEM32(g_esp); g_esp += 4;
    g_ebp = MEM32(g_esp); g_esp += 4;
    g_ecx = MEM32(g_esp); g_esp += 4;
    g_esp += 4;
}

void ra2_reference_exit_bridge(uint32_t variant, uint32_t clear_reference)
{
    const Ra2ReferenceExitServices s = {NULL, reference_exit_clear_field, reference_exit_restore};
    ra2_finish_reference_cleanup(&s, clear_reference, variant);
}

static uint32_t reference_count_read(void *opaque)
{
    (void)opaque;
    g_eax = MEM32(g_ecx + 0xC);
    return g_eax;
}

static void reference_count_result(void *opaque, uint32_t value)
{
    (void)opaque;
    g_eax = value;
    g_flag_k = FK_TEST; g_flag_a = value; g_flag_b = value; g_flag_cf = 0;
}

static void reference_count_write(void *opaque, uint32_t value)
{
    (void)opaque;
    MEM32(g_ecx + 0xC) = value;
}

void ra2_reference_count_bridge(void)
{
    const Ra2ReferenceCountServices s = {NULL, reference_count_read, reference_count_result,
        reference_count_write};
    ra2_decrement_reference_count(&s);
    g_esp += 4;
}

typedef struct ControlDispatchContext { uint32_t kind, left, right, carry; } ControlDispatchContext;

static void control_dispatch_sync(ControlDispatchContext *c)
{
    c->kind = g_flag_k; c->left = g_flag_a; c->right = g_flag_b; c->carry = g_flag_cf;
}

static void control_dispatch_flags(const ControlDispatchContext *c)
{
    g_flag_k = c->kind; g_flag_a = c->left; g_flag_b = c->right; g_flag_cf = c->carry;
}

static void control_dispatch_invoke(ControlDispatchContext *c, uint32_t target)
{
    ControlDispatchContext live;
    control_dispatch_sync(&live);
    g_icall_trace[g_icall_trace_idx & (ICALL_TRACE_SIZE - 1)] = target;
    g_icall_from[g_icall_trace_idx & (ICALL_TRACE_SIZE - 1)] = g_cur_func;
    ++g_icall_trace_idx; ++g_icall_count;
    /* 原ICALL在解析成功后才刷新局部标志；未解析时FLAGS_IN读旧全局状态。 */
    control_dispatch_flags(c);
    recomp_func_t fn = recomp_lookup_manual(target);
    if (!fn) fn = recomp_lookup(target);
    if (!fn) fn = recomp_lookup_import(target);
    if (fn) {
        uint32_t stack = g_esp, caller = g_cur_func;
        g_esp -= 4; MEM32(g_esp) = RECOMP_RETADDR;
        control_dispatch_flags(&live);
        fn();
        if (g_esp != stack) { fputs("[control dispatch] stack imbalance\n", stderr); abort(); }
        g_cur_func = caller;
    } else {
        fprintf(stderr, "ICALL: unresolved VA 0x%08X from 0x%08X\n", target, g_cur_func);
        g_eax = 0;
    }
    control_dispatch_sync(c);
}

static void control_dispatch_begin(void *opaque)
{
    (void)opaque;
    g_esp -= 4; MEM32(g_esp) = g_esi; g_esi = g_ecx;
}

static void control_dispatch_first(void *opaque)
{
    g_eax = MEM32(g_esi + 0xD4);
    control_dispatch_invoke(opaque, MEM32(g_eax + 0x28));
}

static int32_t control_dispatch_needs_optional(void *opaque)
{
    (void)opaque;
    g_flag_k = FK_NARROW(FK_TEST, 24);
    g_flag_a = (uint32_t)MEM8(g_esi + 0xA4) << 24; g_flag_b = 5u << 24; g_flag_cf = 0;
    return (g_flag_a & g_flag_b) != 0;
}

static void control_dispatch_optional(void *opaque)
{
    g_edx = MEM32(g_esi + 0xD4); g_ecx = g_esi;
    control_dispatch_invoke(opaque, MEM32(g_edx + 0x10));
}

static void control_dispatch_last(void *opaque)
{
    g_eax = MEM32(g_esi + 0xD4); g_ecx = g_esi;
    control_dispatch_invoke(opaque, MEM32(g_eax + 0x2C));
}

static int32_t control_dispatch_has_callback(void *opaque)
{
    (void)opaque;
    g_eax = MEM32(g_esi + 0xBC);
    g_flag_k = FK_TEST; g_flag_a = g_eax; g_flag_b = g_eax; g_flag_cf = 0;
    return g_eax != 0;
}

static void control_dispatch_callback(void *opaque)
{
    g_ecx = g_esi;
    control_dispatch_invoke(opaque, g_eax);
}

static void control_dispatch_finish(void *opaque)
{
    (void)opaque;
    MEM32(g_esi + 0x168) = 0;
    g_esi = MEM32(g_esp); g_esp += 4;
    g_esp += 4;
}

void ra2_control_dispatch_bridge(void)
{
    ControlDispatchContext context;
    control_dispatch_sync(&context);
    const Ra2ControlDispatchServices s = {&context, control_dispatch_begin, control_dispatch_first,
        control_dispatch_needs_optional, control_dispatch_optional, control_dispatch_last,
        control_dispatch_has_callback, control_dispatch_callback, control_dispatch_finish};
    ra2_dispatch_control_cleanup(&s);
}

typedef struct ControlTailContext {
    ControlDispatchContext synced;
    uint32_t *deferred_flags;
} ControlTailContext;

static void control_tail_clear(void *opaque)
{
    (void)opaque;
    g_ecx = MEM32(g_esi + 0xA4);
    g_flag_k = FK_TEST; g_flag_a = g_ecx; g_flag_b = 0xFFFFFFEFu; g_flag_cf = 0;
    g_ecx &= 0xFFFFFFEFu;
    MEM32(g_esi + 0xA4) = g_ecx;
}

static uint32_t control_tail_restore_and_jump(void *opaque)
{
    ControlTailContext *c = opaque;
    g_edx = MEM32(g_esi + 0xD4); g_ecx = g_esi;
    g_esi = MEM32(g_esp); g_esp += 4;
    uint32_t target = MEM32(g_edx + 0x2C);
    /* 原_ljump先处理本函数标签，不登记间接调用，也不刷新旧全局标志。 */
    switch (target) {
    case 0x004026F0u: case 0x004026F1u: case 0x004026F3u: case 0x004026F9u:
    case 0x004026FCu: case 0x00402702u: case 0x00402705u: case 0x0040270Bu:
    case 0x00402711u: case 0x00402713u: case 0x00402714u:
        c->deferred_flags[0] = c->synced.kind; c->deferred_flags[1] = c->synced.left;
        c->deferred_flags[2] = c->synced.right; c->deferred_flags[3] = c->synced.carry;
        return target;
    default: break;
    }
    ControlDispatchContext live;
    control_dispatch_sync(&live);
    g_icall_trace[g_icall_trace_idx & (ICALL_TRACE_SIZE - 1)] = target;
    g_icall_from[g_icall_trace_idx & (ICALL_TRACE_SIZE - 1)] = g_cur_func;
    ++g_icall_trace_idx; ++g_icall_count;
    control_dispatch_flags(&c->synced);
    recomp_func_t fn = recomp_lookup_manual(target);
    if (!fn) fn = recomp_lookup(target);
    if (!fn) fn = recomp_lookup_import(target);
    if (fn) {
        /* ITAIL不新增返回槽，不在尾被调方返回后恢复调用归属。 */
        control_dispatch_flags(&live);
        fn();
    } else if (target != RECOMP_RETADDR) {
        fprintf(stderr, "ITAIL: unresolved VA 0x%08X from 0x%08X\n", target, g_cur_func);
    }
    return 0;
}

uint32_t ra2_control_tail_bridge(uint32_t deferred_flags[4])
{
    ControlTailContext context;
    control_dispatch_sync(&context.synced); context.deferred_flags = deferred_flags;
    const Ra2ControlTailServices s = {&context, control_dispatch_begin, control_dispatch_first,
        control_tail_clear, control_tail_restore_and_jump};
    return ra2_clear_control_state_and_tail(&s);
}

static void control_set_state(void *opaque)
{
    (void)opaque;
    g_ecx = MEM32(g_esi + 0xA4);
    g_ecx |= 0x10u;
    /* 原OR以结果的TEST表示标志，不能复用清位AND的两操作数。 */
    g_flag_k = FK_TEST; g_flag_a = g_ecx; g_flag_b = g_ecx; g_flag_cf = 0;
    MEM32(g_esi + 0xA4) = g_ecx;
}

static uint32_t control_set_restore_and_jump(void *opaque)
{
    ControlTailContext *c = opaque;
    g_edx = MEM32(g_esi + 0xD4); g_ecx = g_esi;
    g_esi = MEM32(g_esp); g_esp += 4;
    uint32_t target = MEM32(g_edx + 0x2C);
    /* 本函数内部标签先交回原_ljump，保持当前局部与旧全局标志分离。 */
    switch (target) {
    case 0x004026C0u: case 0x004026C1u: case 0x004026C3u: case 0x004026C9u:
    case 0x004026CCu: case 0x004026D2u: case 0x004026D5u: case 0x004026DBu:
    case 0x004026E1u: case 0x004026E3u: case 0x004026E4u:
        c->deferred_flags[0] = c->synced.kind; c->deferred_flags[1] = c->synced.left;
        c->deferred_flags[2] = c->synced.right; c->deferred_flags[3] = c->synced.carry;
        return target;
    default: break;
    }
    ControlDispatchContext live;
    control_dispatch_sync(&live);
    g_icall_trace[g_icall_trace_idx & (ICALL_TRACE_SIZE - 1)] = target;
    g_icall_from[g_icall_trace_idx & (ICALL_TRACE_SIZE - 1)] = g_cur_func;
    ++g_icall_trace_idx; ++g_icall_count;
    control_dispatch_flags(&c->synced);
    recomp_func_t fn = recomp_lookup_manual(target);
    if (!fn) fn = recomp_lookup(target);
    if (!fn) fn = recomp_lookup_import(target);
    if (fn) {
        control_dispatch_flags(&live);
        fn();
    } else if (target != RECOMP_RETADDR) {
        fprintf(stderr, "ITAIL: unresolved VA 0x%08X from 0x%08X\n", target, g_cur_func);
    }
    return 0;
}

uint32_t ra2_control_set_bridge(uint32_t deferred_flags[4])
{
    ControlTailContext context;
    control_dispatch_sync(&context.synced); context.deferred_flags = deferred_flags;
    const Ra2ControlSetServices s = {&context, control_dispatch_begin, control_dispatch_first,
        control_set_state, control_set_restore_and_jump};
    return ra2_set_control_state_and_tail(&s);
}
