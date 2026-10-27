#include <stdio.h>
#include <stdlib.h>
#include "recomp_types.h"
#include "combat_building_cleanup.h"
#include "combat_building_cleanup_bridge.h"
#include "combat_building_cleanup_rules.h"
#include "combat_building_cleanup_rules_bridge.h"

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
