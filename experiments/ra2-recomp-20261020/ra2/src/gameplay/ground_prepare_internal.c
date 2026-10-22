#include "ground_prepare_internal.h"

uint32_t ra2_ground_prepare_destination_cell(Ra2WorldPoint destination)
{
    uint32_t x = (uint16_t)(destination.x / 256);
    uint32_t y = (uint16_t)(destination.y / 256);
    return x | (y << 16);
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
