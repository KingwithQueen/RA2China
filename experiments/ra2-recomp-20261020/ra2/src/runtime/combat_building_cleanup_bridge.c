#include "combat_building_cleanup_tail.h"
#include "combat_building_cleanup_tail_bridge.h"
#include <stdio.h>
#include <stdlib.h>
#include "recomp_types.h"
#include "combat_building_cleanup.h"
#include "combat_building_cleanup_bridge.h"
#include "combat_building_cleanup_rules.h"
#include "combat_building_cleanup_rules_bridge.h"
#include "combat_building_cleanup_registry.h"
#include "combat_building_cleanup_registry_bridge.h"
#include "combat_building_cleanup_pairs.h"
#include "combat_building_cleanup_pairs_bridge.h"

typedef struct CleanupContext { uint32_t owner, frame; } CleanupContext;

static uint32_t call(uint32_t target, uint32_t self, const uint32_t *args, unsigned count, int caller_pop)
{
    uint32_t stack = g_esp, caller = g_cur_func;
    for (unsigned i = count; i; --i) { g_esp -= 4; MEM32(g_esp) = args[i - 1]; }
    g_esp -= 4; MEM32(g_esp) = RECOMP_RETADDR; g_ecx = self;
    recomp_func_t fn = recomp_lookup_manual(target);
    if (!fn) fn = recomp_lookup(target);
    if (!fn) fn = recomp_lookup_import(target);
    if (!fn) { fprintf(stderr, "[building cleanup] unresolved %08X\n", target); abort(); }
    fn();
    if (caller_pop) {
        g_flag_k = FK_ADD; g_flag_a = g_esp; g_flag_b = count * 4;
        g_flag_cf = g_esp + count * 4 < g_esp; g_esp += count * 4;
    }
    if (g_esp != stack) { fputs("[building cleanup] stack imbalance\n", stderr); abort(); }
    g_cur_func = caller; return g_eax;
}

static int32_t query(void *opaque, Ra2BuildingCleanupQuery q, uint32_t index)
{
    CleanupContext *c = opaque; (void)index;
    switch (q) {
        case RA2_BC_DELETE_FLAG:
            g_flag_k = FK_NARROW(FK_TEST, 24); g_flag_a = (uint32_t)MEM8(c->frame + 8) << 24;
            g_flag_b = 1u << 24; g_flag_cf = 0; return (MEM8(c->frame + 8) & 1) != 0;
        case RA2_BC_HAS_MEMBER:
            g_ecx = MEM32(c->owner + 0x4E8); g_ebp = 0; return g_ecx != 0;
        case RA2_BC_FIND_BUILDING: {
            g_edx = MEM32(0xA40AF8); g_ecx = c->frame + 0x10; uint32_t out = g_ecx;
            MEM32(out) = c->owner;
            return (int32_t)call(MEM32(g_edx + 0x10), 0xA40AF8, &out, 1, 0);
        }
        case RA2_BC_HAS_SLOT: g_ecx = MEM32(g_edi); return g_ecx != 0;
    }
    abort();
}

static void perform(void *opaque, Ra2BuildingCleanupOperation op, uint32_t index)
{
    CleanupContext *c = opaque; (void)index;
    switch (op) {
        case RA2_BC_CLEANUP_BODY: call(0x439240, c->owner, NULL, 0, 0); break;
        case RA2_BC_FREE_OBJECT: {
            uint32_t pointer = g_esi; call(0x781D3B, g_ecx, &pointer, 1, 1); break;
        }
        case RA2_BC_RESET_TABLES:
            MEM32(c->owner) = 0x79CBBC; g_ecx = g_edi;
            MEM32(c->owner + 4) = 0x79CBA0; MEM32(c->owner + 8) = 0x79CB98; MEM32(c->owner + 12) = 0x79CB90; break;
        case RA2_BC_CLEAR_CONTAINER_A: call(0x406070, g_edi, NULL, 0, 0); break;
        case RA2_BC_CLEAR_CONTAINER_B:
            g_ebx = c->owner + 0x570; call(0x406070, g_ebx, NULL, 0, 0); break;
        case RA2_BC_RELEASE_CONTAINER_A: call(0x405C10, g_edi, NULL, 0, 0); break;
        case RA2_BC_RELEASE_CONTAINER_B: call(0x405C10, g_ebx, NULL, 0, 0); break;
        case RA2_BC_CANCEL_MEMBER: {
            uint32_t zero = g_ebp; call(0x537560, g_ecx, &zero, 1, 0); break;
        }
        case RA2_BC_DELETE_MEMBER: {
            g_eax = MEM32(g_ecx); uint32_t one = 1; call(MEM32(g_eax + 0x20), g_ecx, &one, 1, 0); break;
        }
        case RA2_BC_CLEAR_MEMBER: MEM32(c->owner + 0x4E8) = g_ebp; break;
        case RA2_BC_DETACH_REFERENCES:
            g_edx = (g_edx & 0xFFFFFF00u) | 1; call(0x6ECB90, c->owner, NULL, 0, 0); break;
        case RA2_BC_BUILDING_CLEANUP: call(0x442060, c->owner, NULL, 0, 0); break;
        case RA2_BC_REMOVE_BUILDING: {
            uint32_t found = g_eax; call(0x454B60, 0xA40AF8, &found, 1, 0); break;
        }
        case RA2_BC_RESET_MODE: {
            uint32_t mode = UINT32_MAX - 1; call(0x44CFD0, c->owner, &mode, 1, 0); break;
        }
        case RA2_BC_RELEASE_TYPE: call(0x45E920, MEM32(c->owner + 0x418), NULL, 0, 0); break;
        case RA2_BC_BEGIN_SLOTS: g_edi = c->owner + 0x49C; g_ebx = 8; break;
        case RA2_BC_UNINIT_SLOT:
            g_eax = MEM32(g_ecx); call(MEM32(g_eax + 0xF0), g_ecx, NULL, 0, 0); break;
        case RA2_BC_CLEAR_SLOT: MEM32(g_edi) = g_ebp; break;
        case RA2_BC_NEXT_SLOT: g_edi += 4; --g_ebx; RECOMP_BACKEDGE(); break;
    }
}

void ra2_building_delete_bridge(void)
{
    CleanupContext c = {g_ecx, g_esp - 4};
    g_esp -= 4; MEM32(g_esp) = g_esi; g_esi = c.owner;
    Ra2BuildingCleanupServices s = {&c, query, perform}; ra2_delete_building(&s);
    /* 清理/释放后只返回保存的指针值，saved ESI仍从当前guest栈读取。 */
    g_eax = g_esi; g_esi = MEM32(g_esp); g_esp += 12;
}

void ra2_building_cleanup_prefix_bridge(void)
{
    uint32_t owner = g_ecx;
    g_esp -= 4; MEM32(g_esp) = g_ecx;
    g_esp -= 4; MEM32(g_esp) = g_ebx;
    g_esp -= 4; MEM32(g_esp) = g_ebp;
    g_esp -= 4; MEM32(g_esp) = g_esi; g_esi = owner;
    g_esp -= 4; MEM32(g_esp) = g_edi; g_edi = owner + 0x584;
    CleanupContext c = {owner, g_esp}; Ra2BuildingCleanupServices s = {&c, query, perform};
    ra2_cleanup_building_prefix(&s);
}

static int32_t rules_query(void *opaque, Ra2BuildingCleanupRuleQuery q, uint32_t slot)
{
    CleanupContext *c = opaque;
    switch (q) {
        case RA2_BCR_ACTIVE:
            g_eax = (g_eax & 0xFFFFFF00u) | MEM8(0xA40958); return (uint8_t)g_eax != 0;
        case RA2_BCR_CLOAK_TYPE: g_eax = MEM32(c->owner + 0x418); return g_eax != 0;
        case RA2_BCR_CLOAK_GENERATOR:
            g_ecx = (g_ecx & 0xFFFFFF00u) | MEM8(g_eax + 0x1361); return (uint8_t)g_ecx != 0;
        case RA2_BCR_SUPER_INDEX:
            if (!slot) { g_edx = MEM32(c->owner + 0x418); g_edi = UINT32_MAX; g_eax = MEM32(g_edx + 0x1374); }
            else { g_eax = MEM32(c->owner + 0x418); g_eax = MEM32(g_eax + 0x1378); }
            return (int32_t)g_eax;
        case RA2_BCR_AUX_BUILDING:
            /* 原版使用 SuperClass 实例列表，经实例+24读取规则，不能换成类型列表。 */
            g_ecx = MEM32(0xA35D2C); g_edx = MEM32(g_ecx + g_eax * 4);
            g_eax = MEM32(g_edx + 0x24); g_eax = MEM32(g_eax + 0xC0); return g_eax != 0;
        case RA2_BCR_OWNER_AUX_COUNT: {
            g_ecx = MEM32(g_eax + 0xB90); uint32_t index = g_ecx;
            g_ecx = MEM32(c->owner + 0x1B4); g_ecx += 0x5460;
            return (int32_t)call(0x491D10, g_ecx, &index, 1, 0);
        }
        case RA2_BCR_CURRENT_SUPER:
            g_edx = MEM32(c->owner + 0x418); return MEM32(g_edx + 0x1374 + slot * 4) != UINT32_MAX;
        case RA2_BCR_HEALTH_CHANGED:
            g_eax = MEM32(c->owner + 0x6C); g_ecx = MEM32(c->owner + 0x43C); return g_eax != g_ecx;
        case RA2_BCR_CURRENT_TYPE: return MEM32(c->owner + 0x418) != 0;
        case RA2_BCR_OWNER: g_ecx = MEM32(c->owner + 0x1B4); return g_ecx != 0;
    }
    abort();
}

static void rules_perform(void *opaque, Ra2BuildingCleanupRuleOperation op, uint32_t index)
{
    CleanupContext *c = opaque; (void)index;
    switch (op) {
        case RA2_BCR_DISABLE_CLOAK: {
            g_ecx = (g_ecx & 0xFFFFFF00u) | MEM8(c->owner + 0x5BC); MEM8(c->owner + 0x5BB) = 0xFF;
            if (!(uint8_t)g_ecx) {
                g_ecx = (g_ecx & 0xFFFFFF00u) | MEM8(g_eax + 0x138B); MEM8(c->owner + 0x5BC) = (uint8_t)g_ecx;
            }
            uint32_t one = 1; MEM8(c->owner + 0x75) = 1; MEM8(c->owner + 0x5BC) = 1;
            call(0x44FB50, c->owner, &one, 1, 0); break;
        }
        case RA2_BCR_REFRESH_SUPERS: call(0x4F4B20, MEM32(c->owner + 0x1B4), NULL, 0, 0); break;
        case RA2_BCR_MARK_OWNER:
            g_ecx = MEM32(c->owner + 0x1B4); MEM8(g_ecx + 0x5668) = 1; break;
        case RA2_BCR_REMOVE_OWNER_BUILDING:
            call(0x4EA800, g_ecx, &c->owner, 1, 0); break;
        case RA2_BCR_CLEANUP_BUILDING: perform(c, RA2_BC_BUILDING_CLEANUP, 0); break;
    }
}

void ra2_building_cleanup_rules_bridge(void)
{
    CleanupContext c = {g_esi, g_esp};
    Ra2BuildingCleanupRuleServices s = {&c, rules_query, rules_perform};
    ra2_cleanup_building_rules(&s);
}

static uint32_t cleanup_registry_address(uint32_t table)
{
    return table ? 0xAC0C80 : 0xAC0BF8;
}

static int32_t registry_query(void *opaque, Ra2BuildingRegistryQuery q, uint32_t table)
{
    CleanupContext *c = opaque;
    switch (q) {
        case RA2_BCG_HAS_MEMBER: g_ecx = MEM32(c->owner + 0x41C); return g_ecx != 0;
        case RA2_BCG_FIND: {
            uint32_t address = cleanup_registry_address(table);
            /* 每次重读当前表的虚函数，并重写原guest局部参数，不能缓存上一表的状态。 */
            g_edx = MEM32(address); g_eax = c->frame + 0x10; g_ecx = address;
            MEM32(g_eax) = c->owner; uint32_t key = g_eax;
            return (int32_t)call(MEM32(g_edx + 0x10), address, &key, 1, 0);
        }
    }
    abort();
}

static void registry_perform(void *opaque, Ra2BuildingRegistryOperation op, uint32_t table)
{
    CleanupContext *c = opaque;
    switch (op) {
        case RA2_BCG_DELETE_MEMBER: {
            g_edx = MEM32(g_ecx); uint32_t one = 1;
            call(MEM32(g_edx + 0x20), g_ecx, &one, 1, 0); break;
        }
        case RA2_BCG_CLEAR_MEMBER: MEM32(c->owner + 0x41C) = g_ebp; break;
        case RA2_BCG_REMOVE: {
            uint32_t index = g_eax; call(0x454B20, cleanup_registry_address(table), &index, 1, 0); break;
        }
    }
}

void ra2_building_cleanup_registry_bridge(void)
{
    CleanupContext c = {g_esi, g_esp};
    Ra2BuildingRegistryServices s = {&c, registry_query, registry_perform};
    ra2_cleanup_building_registries(&s);
}

typedef struct PairCleanupContext { CleanupContext base; int more; } PairCleanupContext;

static int32_t pair_query(void *opaque, Ra2BuildingPairQuery q)
{
    PairCleanupContext *c = opaque;
    switch (q) {
        case RA2_BCP_FIND: {
            MEM32(c->base.frame + 0x10) = g_eax; g_eax = c->base.frame + 0x10;
            uint32_t key = g_eax; return call(0x41B990, 0xABFF58, &key, 1, 0) != 0;
        }
        case RA2_BCP_VALID_INDEX: {
            /* 先按32位地址相减，再算术右移3位；基址在查找返回后读取。 */
            uint32_t offset = g_eax - MEM32(0xABFF58);
            g_eax = (offset >> 3) | ((offset & 0x80000000u) ? 0xE0000000u : 0);
            return g_eax != UINT32_MAX;
        }
        case RA2_BCP_MORE: return c->more;
    }
    abort();
}

static void pair_perform(void *opaque, Ra2BuildingPairOperation op)
{
    PairCleanupContext *c = opaque;
    switch (op) {
        case RA2_BCP_READ_KEY: {
            g_eax = c->base.owner + 4; uint32_t interface_pointer = g_eax;
            call(0x40FFC0, g_ecx, &interface_pointer, 1, 0); break;
        }
        case RA2_BCP_BEGIN_SHIFT:
            g_ecx = g_eax + 1; g_eax = MEM32(0xABFF5C);
            c->more = (int32_t)g_ecx < (int32_t)g_eax; break;
        case RA2_BCP_SHIFT_NEXT:
            g_edx = MEM32(0xABFF58); g_eax = g_edx + g_ecx * 8; ++g_ecx;
            g_edx = MEM32(g_eax); MEM32(g_eax - 8) = g_edx;
            g_edx = MEM32(g_eax + 4); MEM32(g_eax - 4) = g_edx;
            g_eax = MEM32(0xABFF5C); c->more = (int32_t)g_ecx < (int32_t)g_eax;
            /* 与原生成循环相同：先比较，再让出；下一轮重新读取当前存储。 */
            RECOMP_BACKEDGE(); break;
        case RA2_BCP_TRIM_LAST:
            g_edi = MEM32(0xABFF58); --g_eax; g_ecx = 0; MEM32(0xABFF5C) = g_eax;
            MEM32(g_edi + g_eax * 8) = g_ecx;
            g_eax = MEM32(0xABFF5C); g_ecx = MEM32(0xABFF58); g_edx = 0;
            MEM32(g_ecx + g_eax * 8 + 4) = g_edx; MEM32(0xABFF68) = g_ebp; break;
    }
}

void ra2_building_cleanup_pairs_bridge(void)
{
    PairCleanupContext c = {{g_esi, g_esp}, 0};
    Ra2BuildingPairServices s = {&c, pair_query, pair_perform};
    ra2_cleanup_building_pair(&s);
}

static uint32_t tail_member(uint32_t member)
{
    return member ? g_edi : g_ebp;
}

static int32_t tail_query(void *opaque, Ra2BuildingTailQuery q, uint32_t member)
{
    (void)opaque;
    switch (q) {
        case RA2_BCT_HAS_DATA: return g_eax != g_ebx;
        case RA2_BCT_OWNS_DATA:
            g_ecx = (g_ecx & 0xFFFFFF00u) | MEM8(tail_member(member) + 0x0D);
            return (uint8_t)g_ecx != 0;
    }
    abort();
}

static void tail_perform(void *opaque, Ra2BuildingTailOperation op, uint32_t member)
{
    CleanupContext *c = opaque;
    uint32_t pointer;
    switch (op) {
        case RA2_BCT_CLEAR_STATE:
            MEM32(c->owner + 0x418) = g_ebp; g_ebp = c->owner + 0x53C;
            MEM8(c->owner + 0x7D) = 0; break;
        case RA2_BCT_CLEAR_CONTAINER:
            if (!member) {
                g_ecx = g_ebp; g_edx = MEM32(g_ebp); g_edi = MEM32(g_ebp + 8);
            } else {
                g_edx = MEM32(c->owner + 0x554); g_ebx = MEM32(c->owner + 0x55C);
                g_edi = c->owner + 0x554; g_ecx = g_edi;
            }
            call(MEM32(g_edx + 0x0C), g_ecx, NULL, 0, 0); break;
        case RA2_BCT_RESIZE_CONTAINER: {
            /* 清理回调可改变当前虚表，但容量参数取清理前保存的值。 */
            pointer = tail_member(member); g_eax = MEM32(pointer);
            uint32_t args[] = {member ? g_ebx : g_edi, 0};
            call(MEM32(g_eax + 8), pointer, args, 2, 0); break;
        }
        case RA2_BCT_BEGIN_RELEASE:
            pointer = tail_member(member); g_eax = MEM32(pointer + 4);
            if (member) g_ebx = 0;
            MEM32(pointer) = 0x79D074; break;
        case RA2_BCT_FREE_DATA:
            pointer = g_eax; call(0x781D3B, g_ecx, &pointer, 1, 1);
            /* 原接口返回后才清原成员槽；不重复释放回调换入的指针。 */
            MEM32(tail_member(member) + 4) = g_ebx; break;
        case RA2_BCT_END_RELEASE:
            pointer = tail_member(member); MEM8(pointer + 0x0D) = 0; MEM32(pointer + 8) = g_ebx; break;
        case RA2_BCT_BASE_DESTRUCTOR:
            g_ecx = c->owner; call(0x6C20B0, c->owner, NULL, 0, 0); break;
    }
}

void ra2_building_cleanup_tail_bridge(void)
{
    CleanupContext c = {g_esi, g_esp};
    Ra2BuildingTailServices s = {&c, tail_query, tail_perform};
    ra2_cleanup_building_tail(&s);
}
