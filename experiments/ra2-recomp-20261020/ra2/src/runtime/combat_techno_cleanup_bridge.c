#include "combat_techno_cleanup_member_registry.h"
#include "combat_techno_cleanup_member_registry_bridge.h"
#include "combat_techno_cleanup_registry.h"
#include "combat_techno_cleanup_registry_bridge.h"
#include <stdio.h>
#include <stdlib.h>
#include "recomp_types.h"
#include "combat_techno_cleanup.h"
#include "combat_techno_cleanup_bridge.h"

typedef struct TechnoCleanupContext { uint32_t owner; } TechnoCleanupContext;
static const uint32_t member_offsets[] = {0x408, 0x230, 0x238, 0x208};

static void reset_tables(void *opaque)
{
    TechnoCleanupContext *c = opaque;
    /* 第一个成员先读入 ECX，再切换四张虚表；原函数的保存帧保留在调用处。 */
    g_ecx = MEM32(c->owner + 0x408);
    MEM32(c->owner) = 0x7ACB80; MEM32(c->owner + 4) = 0x7ACB64;
    MEM32(c->owner + 8) = 0x7ACB5C; MEM32(c->owner + 12) = 0x7ACB54;
}

static int32_t has_member(void *opaque, uint32_t member)
{
    TechnoCleanupContext *c = opaque;
    if (member) g_ecx = MEM32(c->owner + member_offsets[member]);
    g_flag_k = FK_CMP; g_flag_a = g_ecx; g_flag_b = g_ebx; g_flag_cf = g_ecx < g_ebx;
    return g_ecx != g_ebx;
}

static void cleanup_member(void *opaque, uint32_t member)
{
    (void)opaque;
    uint32_t stack = g_esp, caller = g_cur_func, target;
    if (!member) target = 0x6130B0;
    else {
        /* 各成员进入时读取当前虚表；不能提前缓存后续成员或其清理目标。 */
        if (member == 2) { g_edx = MEM32(g_ecx); target = MEM32(g_edx + 0x20); }
        else { g_eax = MEM32(g_ecx); target = MEM32(g_eax + 0x20); }
        g_esp -= 4; MEM32(g_esp) = 1;
    }
    g_esp -= 4; MEM32(g_esp) = RECOMP_RETADDR;
    recomp_func_t fn = recomp_lookup_manual(target);
    if (!fn) fn = recomp_lookup(target);
    if (!fn) fn = recomp_lookup_import(target);
    if (!fn) { fprintf(stderr, "[techno cleanup] unresolved %08X\n", target); abort(); }
    fn();
    if (g_esp != stack) { fputs("[techno cleanup] stack imbalance\n", stderr); abort(); }
    g_cur_func = caller;
}

static void clear_member(void *opaque, uint32_t member)
{
    TechnoCleanupContext *c = opaque;
    /* 回调换入原槽的指针也只清槽，不追加一次清理。 */
    MEM32(c->owner + member_offsets[member]) = g_ebx;
}

void ra2_techno_cleanup_prefix_bridge(void)
{
    TechnoCleanupContext c = {g_esi};
    Ra2TechnoCleanupServices s = {&c, reset_tables, has_member, cleanup_member, clear_member};
    ra2_cleanup_techno_prefix(&s);
}

static void registry_invoke(uint32_t target, uint32_t expected_stack)
{
    uint32_t caller = g_cur_func;
    g_esp -= 4; MEM32(g_esp) = RECOMP_RETADDR;
    recomp_func_t fn = recomp_lookup_manual(target);
    if (!fn) fn = recomp_lookup(target);
    if (!fn) fn = recomp_lookup_import(target);
    if (!fn) { fprintf(stderr, "[techno registry] unresolved %08X\n", target); abort(); }
    fn();
    if (g_esp != expected_stack) { fputs("[techno registry] stack imbalance\n", stderr); abort(); }
    g_cur_func = caller;
}

static void registry_perform(void *opaque, Ra2TechnoRegistryOperation op)
{
    TechnoCleanupContext *c = opaque;
    switch (op) {
        case RA2_TCR_BEGIN:
            g_esp -= 4; MEM32(g_esp) = g_edi; g_edi = c->owner + 0x3D8; break;
        case RA2_TCR_CLEAR_AUXILIARY:
            g_ecx = g_edi; registry_invoke(0x405FE0, g_esp); break;
        case RA2_TCR_RELEASE_AUXILIARY:
            g_ecx = g_edi; registry_invoke(0x405C10, g_esp); break;
        case RA2_TCR_CLEAR_STATE:
            g_ecx = g_esp + 0x0C;
            MEM32(c->owner + 0x1B4) = g_ebx; MEM8(c->owner + 0x372) = (uint8_t)g_ebx; break;
        case RA2_TCR_RESTORE_SAVED:
            /* 原流程在第一次查询返回后、第一次移除之前恢复 EDI，不能推迟到末尾。 */
            g_edi = MEM32(g_esp); g_esp += 4; break;
    }
}

static int32_t registry_find(void *opaque, uint32_t which)
{
    TechnoCleanupContext *c = opaque;
    uint32_t stack = g_esp, table = which ? 0xAC0D08 : 0xA40C20;
    g_edx = MEM32(table);
    /* 两次查询共用原保存帧内的对象临时槽，第二次在 EDI 恢复后重新定位。 */
    if (which) g_eax = g_esp + 8;
    uint32_t argument = which ? g_eax : g_ecx;
    g_esp -= 4; MEM32(g_esp) = argument; g_ecx = table;
    MEM32(g_esp + (which ? 0x0C : 0x10)) = c->owner;
    registry_invoke(MEM32(g_edx + 0x10), stack);
    g_flag_k = FK_CMP; g_flag_a = g_eax; g_flag_b = UINT32_MAX; g_flag_cf = g_eax < UINT32_MAX;
    return (int32_t)g_eax;
}

static void registry_remove(void *opaque, uint32_t which, int32_t index)
{
    (void)opaque;
    uint32_t stack = g_esp;
    g_esp -= 4; MEM32(g_esp) = (uint32_t)index; g_ecx = which ? 0xAC0D08 : 0xA40C20;
    registry_invoke(which ? 0x454B20 : 0x61BDC0, stack);
}

void ra2_techno_cleanup_registry_bridge(void)
{
    TechnoCleanupContext c = {g_esi};
    Ra2TechnoRegistryServices s = {&c, registry_perform, registry_find, registry_remove};
    ra2_cleanup_techno_registries(&s);
}

static int32_t member_registry_has(void *opaque)
{
    TechnoCleanupContext *c = opaque;
    g_ecx = MEM32(c->owner + 0x108);
    g_flag_k = FK_CMP; g_flag_a = g_ecx; g_flag_b = g_ebx; g_flag_cf = g_ecx < g_ebx;
    return g_ecx != g_ebx;
}

static void member_registry_cleanup(void *opaque)
{
    (void)opaque;
    g_eax = MEM32(g_ecx);
    registry_invoke(MEM32(g_eax + 0xF0), g_esp);
}

static void member_registry_clear(void *opaque)
{
    TechnoCleanupContext *c = opaque;
    /* 即使回调换入新成员，也只在返回后清原槽，不追加一次虚调用。 */
    MEM32(c->owner + 0x108) = g_ebx;
}

static int32_t member_registry_find(void *opaque)
{
    TechnoCleanupContext *c = opaque;
    uint32_t stack = g_esp;
    /* 成员回调可改变登记表；在此重新读表，并重写原保存帧中的对象临时槽。 */
    g_edx = MEM32(0xAC0BF8); g_ecx = g_esp + 8;
    g_esp -= 4; MEM32(g_esp) = g_ecx; g_ecx = 0xAC0BF8;
    MEM32(g_esp + 0x0C) = c->owner;
    registry_invoke(MEM32(g_edx + 0x10), stack);
    g_flag_k = FK_CMP; g_flag_a = g_eax; g_flag_b = UINT32_MAX; g_flag_cf = g_eax < UINT32_MAX;
    return (int32_t)g_eax;
}

static void member_registry_remove(void *opaque, int32_t index)
{
    (void)opaque; uint32_t stack = g_esp;
    g_esp -= 4; MEM32(g_esp) = (uint32_t)index; g_ecx = 0xAC0BF8;
    registry_invoke(0x454B20, stack);
}

void ra2_techno_cleanup_member_registry_bridge(void)
{
    TechnoCleanupContext c = {g_esi};
    Ra2TechnoMemberRegistryServices s = {&c, member_registry_has, member_registry_cleanup,
        member_registry_clear, member_registry_find, member_registry_remove};
    ra2_cleanup_techno_member_registry(&s);
}
