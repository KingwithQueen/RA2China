#include <string.h>
#include "ground_entry.h"
#include "ground_cell_coordinates.h"
#include "ground_bridge_plane.h"
#include "ground_direction_rules.h"
#include "ground_collision.h"

Ra2EntryOutcome ra2_ground_check_entry(Ra2EntryState *state, Ra2CellLink link, const Ra2EntryServices *s)
{
    void *c=s->context;
    if (state->direction==8)
    {
        if (!link.present) return RA2_ENTRY_BLOCKED;
        uint32_t endpoint=ra2_ground_pack_cell_components((uint16_t)link.endpoint_x,(uint16_t)link.endpoint_y);
        memcpy(&state->reference_level,&endpoint,4);
        return endpoint ? RA2_ENTRY_CLEAR : RA2_ENTRY_BLOCKED;
    }
    if (link.present && ra2_ground_direction_conflicts(state->direction,link.direction) && state->direction!=-1)
        return RA2_ENTRY_BLOCKED;
    int32_t opposite=(int32_t)ra2_ground_opposite_heading(state->direction);
    Ra2CellLink neighbor=s->neighbor_link(c,opposite);
    if (neighbor.present && ra2_ground_direction_conflicts(opposite,neighbor.direction) && state->direction!=-1)
        return RA2_ENTRY_BLOCKED;
    if (s->check_placement(c,state)==RA2_CELL_BLOCKED) return RA2_ENTRY_BLOCKED;
    if (state->reference_level!=-1 && s->query(c,RA2_ENTRY_HAS_BRIDGE)
        && ra2_ground_bridge_height_matches(state->reference_level,s->query(c,RA2_ENTRY_CELL_LEVEL)))
    {
        state->occupation_flags=(uint8_t)s->query(c,RA2_ENTRY_UPPER_FLAGS);
        state->vehicle_present=(state->occupation_flags>>5)&1u;
        state->infantry_owner=s->query(c,RA2_ENTRY_UPPER_INFANTRY_OWNER);
    }
    if (!s->query(c,RA2_ENTRY_GLOBAL_VISIBILITY_OVERRIDE) && !s->query(c,RA2_ENTRY_CELL_VISIBLE)
        && !s->query(c,RA2_ENTRY_OWNER_VISIBILITY_EXEMPT) && s->query(c,RA2_ENTRY_OWNER_FLAG_32D))
        return RA2_ENTRY_BLOCKED;
    state->passage=s->base_passage(c,state);
    return state->passage==RA2_CELL_BLOCKED ? RA2_ENTRY_BLOCKED : RA2_ENTRY_CONTINUE;
}
