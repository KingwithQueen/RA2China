#include "combat_building_cleanup.h"
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
