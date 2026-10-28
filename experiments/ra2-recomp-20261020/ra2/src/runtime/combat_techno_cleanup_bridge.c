#include "combat_techno_cleanup_base.h"
#include "combat_techno_cleanup_base_bridge.h"
#include "combat_techno_cleanup_containers.h"
#include "combat_techno_cleanup_containers_bridge.h"
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

typedef struct ContainersCleanupContext { uint32_t caller; } ContainersCleanupContext;
static const uint32_t container_offsets[] = {0x3C0, 0x3A8, 0x390};

static void containers_begin(void *opaque, uint32_t member)
{
    ContainersCleanupContext *c = opaque;
    g_ecx = g_esi + container_offsets[member];
    MEM32(g_ecx) = member == 2 ? 0x79D9D4 : 0x7A179C;
    /* 保留原两个容器入口的保存帧和调用归属，释放回调仍遵循原cdecl接口。 */
    g_esp -= 4; MEM32(g_esp) = RECOMP_RETADDR;
    c->caller = g_cur_func; g_cur_func = member == 2 ? 0x46D160 : 0x4CE0D0;
    g_esp -= 4; MEM32(g_esp) = g_ebx; g_esp -= 4; MEM32(g_esp) = g_esi;
    g_esi = g_ecx; g_ebx = 0;
    g_flag_k = FK_TEST; g_flag_a = g_flag_b = g_flag_cf = 0;
    g_eax = MEM32(g_esi + 4);
}

static int32_t containers_has_data(void *opaque)
{
    (void)opaque;
    g_flag_k = FK_CMP; g_flag_a = g_eax; g_flag_b = g_ebx; g_flag_cf = g_eax < g_ebx;
    return g_eax != g_ebx;
}

static int32_t containers_owns_data(void *opaque)
{
    (void)opaque;
    uint32_t owned = MEM8(g_esi + 0x0D);
    g_flag_k = FK_NARROW(FK_CMP, 24); g_flag_a = owned << 24;
    g_flag_b = (uint32_t)(uint8_t)g_ebx << 24; g_flag_cf = owned < (uint8_t)g_ebx;
    return owned != (uint8_t)g_ebx;
}

static void containers_free_data(void *opaque)
{
    (void)opaque;
    g_esp -= 4; MEM32(g_esp) = g_eax;
    registry_invoke(0x781D3B, g_esp);
    g_flag_k = FK_ADD; g_flag_a = g_esp; g_flag_b = 4;
    g_flag_cf = g_esp + 4 < g_esp; g_esp += 4;
    /* 回调换入的数据也在返回后清槽，不重复释放新指针。 */
    MEM32(g_esi + 4) = g_ebx;
}

static void containers_end(void *opaque, uint32_t member)
{
    ContainersCleanupContext *c = opaque; (void)member;
    MEM8(g_esi + 0x0D) = 0; MEM32(g_esi + 8) = g_ebx;
    g_esi = MEM32(g_esp); g_esp += 4; g_ebx = MEM32(g_esp); g_esp += 4;
    g_esp += 4; g_cur_func = c->caller;
}

static void containers_finish_member118(void *opaque)
{
    (void)opaque;
    /* 1.006的713350只有RET；只保留this定位和空调用帧，不引入相邻函数的重置。 */
    g_ecx = g_esi + 0x118;
    g_esp -= 4; MEM32(g_esp) = RECOMP_RETADDR; g_esp += 4;
}

void ra2_techno_cleanup_containers_bridge(void)
{
    ContainersCleanupContext c = {0};
    Ra2TechnoContainersServices s = {&c, containers_begin, containers_has_data, containers_owns_data,
        containers_free_data, containers_end, containers_finish_member118};
    ra2_cleanup_techno_containers(&s);
}

static void base_begin_radio(void *opaque)
{
    (void)opaque;
    MEM32(g_esi) = 0x7A88E8; MEM32(g_esi + 4) = 0x7A88CC;
    MEM32(g_esi + 8) = 0x7A88C4; MEM32(g_esi + 0x0C) = 0x7A88BC;
    /* 原序列先读数据，再切换C8表；后续释放使用这次读取的指针。 */
    g_eax = MEM32(g_esi + 0xCC); MEM32(g_esi + 0xC8) = 0x79A7FC;
}

static int32_t base_has_data(void *opaque)
{
    (void)opaque;
    g_flag_k = FK_CMP; g_flag_a = g_eax; g_flag_b = g_ebx; g_flag_cf = g_eax < g_ebx;
    return g_eax != g_ebx;
}

static int32_t base_owns_data(void *opaque)
{
    (void)opaque;
    uint32_t owned = MEM8(g_esi + 0xD5);
    g_flag_k = FK_NARROW(FK_CMP, 24); g_flag_a = owned << 24;
    g_flag_b = (uint32_t)(uint8_t)g_ebx << 24; g_flag_cf = owned < (uint8_t)g_ebx;
    return owned != (uint8_t)g_ebx;
}

static void base_free_data(void *opaque)
{
    (void)opaque;
    g_esp -= 4; MEM32(g_esp) = g_eax;
    registry_invoke(0x781D3B, g_esp);
    g_flag_k = FK_ADD; g_flag_a = g_esp; g_flag_b = 4;
    g_flag_cf = g_esp + 4 < g_esp; g_esp += 4;
    /* 与原版相同，回调替换原槽后仍清槽，只释放最初传入的一次。 */
    MEM32(g_esi + 0xCC) = g_ebx;
}

static void base_reset_storage(void *opaque)
{
    (void)opaque;
    MEM8(g_esi + 0xD5) = (uint8_t)g_ebx; MEM32(g_esi + 0xD0) = g_ebx;
}

static void base_begin_mission(void *opaque)
{
    (void)opaque;
    g_ecx = g_esi;
    MEM32(g_esi) = 0x7A6200; MEM32(g_esi + 4) = 0x7A61E4;
    MEM32(g_esi + 8) = 0x7A61DC; MEM32(g_esi + 0x0C) = 0x7A61D4;
}

static void base_destroy_object(void *opaque)
{
    (void)opaque;
    registry_invoke(0x5D2530, g_esp);
}

void ra2_techno_cleanup_base_bridge(void)
{
    Ra2TechnoBaseCleanupServices s = {NULL, base_begin_radio, base_has_data, base_owns_data,
        base_free_data, base_reset_storage, base_begin_mission, base_destroy_object};
    ra2_cleanup_techno_base(&s);
}
