#include "combat_building_cleanup.h"
#include "combat_building_cleanup_rules.h"
#define Q(q, index) s->query(s->context, RA2_BC_##q, index)
#define DO(op, index) s->perform(s->context, RA2_BC_##op, index)

void ra2_delete_building(const Ra2BuildingCleanupServices *s)
{
    DO(CLEANUP_BODY, 0);
    if (Q(DELETE_FLAG, 0)) DO(FREE_OBJECT, 0);
}

void ra2_cleanup_building_prefix(const Ra2BuildingCleanupServices *s)
{
    DO(RESET_TABLES, 0);
    DO(CLEAR_CONTAINER_A, 0); DO(CLEAR_CONTAINER_B, 0);
    DO(RELEASE_CONTAINER_A, 0); DO(RELEASE_CONTAINER_B, 0);
    if (Q(HAS_MEMBER, 0)) {
        DO(CANCEL_MEMBER, 0);
        if (Q(HAS_MEMBER, 0)) DO(DELETE_MEMBER, 0);
        DO(CLEAR_MEMBER, 0);
    }
    DO(DETACH_REFERENCES, 0); DO(BUILDING_CLEANUP, 0);
    if (Q(FIND_BUILDING, 0) != -1) DO(REMOVE_BUILDING, 0);
    DO(RESET_MODE, 0);
    /* 当前类型在前面所有回调返回后读取，各附属槽也逐个实时读取。 */
    DO(RELEASE_TYPE, 0); DO(BEGIN_SLOTS, 0);
    for (uint32_t i = 0; i < 8; ++i) {
        if (Q(HAS_SLOT, i)) { DO(UNINIT_SLOT, i); DO(CLEAR_SLOT, i); }
        DO(NEXT_SLOT, i);
    }
}

#undef Q
#undef DO
#define Q(q, index) s->query(s->context, RA2_BCR_##q, index)
#define DO(op) s->perform(s->context, RA2_BCR_##op, 0)

void ra2_cleanup_building_cloak_rules(const Ra2BuildingCleanupRuleServices *s)
{
    if (Q(ACTIVE, 0) && Q(CLOAK_TYPE, 0) && Q(CLOAK_GENERATOR, 0)) DO(DISABLE_CLOAK);
}

static int super_qualifies(const Ra2BuildingCleanupRuleServices *s, uint32_t slot)
{
    /* 辅助建筑计数为零时直接跳过本槽的类型重读，再考虑下一槽。 */
    if (Q(SUPER_INDEX, slot) != -1 && Q(AUX_BUILDING, slot) && !Q(OWNER_AUX_COUNT, slot)) return 0;
    return Q(CURRENT_SUPER, slot) != 0;
}

void ra2_cleanup_building_super_rules(const Ra2BuildingCleanupRuleServices *s)
{
    if (super_qualifies(s, 0) || super_qualifies(s, 1)) DO(REFRESH_SUPERS);
}

void ra2_cleanup_building_owner_rules(const Ra2BuildingCleanupRuleServices *s)
{
    if (!Q(ACTIVE, 0)) return;
    if (Q(HEALTH_CHANGED, 0)) DO(MARK_OWNER);
    if (!Q(ACTIVE, 0) || !Q(CURRENT_TYPE, 0)) return;
    if (Q(OWNER, 0)) DO(REMOVE_OWNER_BUILDING);
    /* 归属通知后直接清理，不重新检查可能已被回调更改的开关或类型。 */
    DO(CLEANUP_BUILDING);
}

void ra2_cleanup_building_rules(const Ra2BuildingCleanupRuleServices *s)
{
    ra2_cleanup_building_cloak_rules(s);
    ra2_cleanup_building_super_rules(s);
    ra2_cleanup_building_owner_rules(s);
}
