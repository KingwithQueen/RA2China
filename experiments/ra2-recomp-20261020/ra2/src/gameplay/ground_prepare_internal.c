#include "ground_prepare_internal.h"
#include "ground_cell_coordinates.h"

uint32_t ra2_ground_prepare_destination_cell(Ra2WorldPoint destination)
{
    return ra2_ground_pack_world_cell(destination.x, destination.y);
}
uint32_t ra2_ground_prepare_rebuild_internal(Ra2WorldPoint destination, unsigned retry,
    const Ra2PrepareInternalServices *s)
{
    return s->rebuild(s->context, ra2_ground_prepare_destination_cell(destination), retry ? 2u : 1u);
}
void ra2_ground_prepare_clear_internal(int32_t first_coordinate, const Ra2PrepareInternalServices *s)
{
    s->clear_segment(s->context, first_coordinate);
}
