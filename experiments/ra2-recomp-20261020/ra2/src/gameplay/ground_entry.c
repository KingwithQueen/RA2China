#include <string.h>
#include "ground_entry.h"

static int direction_conflicts(int32_t direction, int32_t link_direction)
{
    uint32_t bits=(uint32_t)direction-(uint32_t)link_direction;
    if (bits&UINT32_C(0x80000000)) bits=0u-bits;
    int32_t distance; memcpy(&distance,&bits,4);
    return distance>2 && distance<6;
}
Ra2EntryOutcome ra2_ground_check_entry(Ra2EntryState *state, Ra2CellLink link, const Ra2EntryServices *s)
{
    void *c=s->context;
    if (state->direction==8)
    {
        if (!link.present) return RA2_ENTRY_BLOCKED;
        uint32_t endpoint=(uint16_t)link.endpoint_x|((uint32_t)(uint16_t)link.endpoint_y<<16);
        memcpy(&state->reference_level,&endpoint,4);
        return endpoint ? RA2_ENTRY_CLEAR : RA2_ENTRY_BLOCKED;
    }
    if (link.present && direction_conflicts(state->direction,link.direction) && state->direction!=-1)
        return RA2_ENTRY_BLOCKED;
    int32_t opposite=(int32_t)(((uint32_t)state->direction-4u)&7u);
    Ra2CellLink neighbor=s->neighbor_link(c,opposite);
    if (neighbor.present && direction_conflicts(opposite,neighbor.direction) && state->direction!=-1)
        return RA2_ENTRY_BLOCKED;
    if (s->check_placement(c,state)==7) return RA2_ENTRY_BLOCKED;
    if (state->reference_level!=-1 && s->query(c,RA2_ENTRY_HAS_BRIDGE)
        && state->reference_level==s->query(c,RA2_ENTRY_CELL_LEVEL)+4)
    {
        state->occupation_flags=(uint8_t)s->query(c,RA2_ENTRY_UPPER_FLAGS);
        state->vehicle_present=(state->occupation_flags>>5)&1u;
        state->infantry_owner=s->query(c,RA2_ENTRY_UPPER_INFANTRY_OWNER);
    }
    if (!s->query(c,RA2_ENTRY_GLOBAL_VISIBILITY_OVERRIDE) && !s->query(c,RA2_ENTRY_CELL_VISIBLE)
        && !s->query(c,RA2_ENTRY_OWNER_VISIBILITY_EXEMPT) && s->query(c,RA2_ENTRY_OWNER_FLAG_32D))
        return RA2_ENTRY_BLOCKED;
    state->passage=s->base_passage(c,state);
    return state->passage==7 ? RA2_ENTRY_BLOCKED : RA2_ENTRY_CONTINUE;
}
