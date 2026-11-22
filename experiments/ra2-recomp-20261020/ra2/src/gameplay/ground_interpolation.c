#include <string.h>
#include "ground_interpolation.h"
#include "ground_bridge_plane.h"
#include "ground_cell_coordinates.h"

static int32_t signed_bits(uint32_t bits)
{ int32_t value; memcpy(&value, &bits, sizeof(value)); return value; }
static int32_t add(int32_t a, int32_t b)
{ return signed_bits((uint32_t)a + (uint32_t)b); }
static int32_t subtract(int32_t a, int32_t b)
{ return signed_bits((uint32_t)a - (uint32_t)b); }

/* Prefer the partial step within either endpoint cell, then apply the progress cutoff. */
static Ra2WorldPoint choose_interpolation_position(int partial_in_endpoint_cell, int32_t progress,
    Ra2WorldPoint current, Ra2WorldPoint partial, Ra2WorldPoint endpoint)
{
    if (partial_in_endpoint_cell) return partial;
    if (progress > 3) return endpoint;
    return current;
}

void ra2_ground_interpolate_advance(Ra2WorldPoint start, int32_t old_x, int32_t old_y,
    int32_t progress, const Ra2InterpolationServices *s)
{
    void *c = s->context;
    Ra2WorldPoint transformed = s->transform(c);
    Ra2WorldPoint delta = { subtract(transformed.x, old_x), subtract(transformed.y, old_y), 0 };
    Ra2WorldPoint current = s->position(c);
    Ra2WorldPoint endpoint = { add(current.x, delta.x), add(current.y, delta.y), current.z };
    uintptr_t end_cell = s->cell_at(c, endpoint);
    Ra2WorldPoint partial = s->blend_delta(c, delta);
    partial.x = add(partial.x, start.x);
    partial.y = add(partial.y, start.y);
    partial.z = add(partial.z, start.z);
    uintptr_t start_cell = s->cell_at(c, start);
    uintptr_t partial_cell = s->cell_at(c, partial);
    current = s->position(c);
    Ra2WorldPoint selected = choose_interpolation_position(partial_cell == end_cell || partial_cell == start_cell,
        progress, current, partial, endpoint);
    /* 第四次查询也必须保留；不能用前面的结果代替，世界可能已经改变。 */
    uintptr_t selected_cell = s->cell_at(c, selected);
    current = s->position(c);
    if (!ra2_ground_same_map_cell(current, selected))
    {
        s->leave(c);
        s->place(c, selected);
        Ra2InterpolationSurface from = s->surface(c, start_cell);
        Ra2InterpolationSurface to = s->surface(c, selected_cell);
        if (ra2_ground_bridge_height_matches(from.level, to.level) && to.bridge) s->set_bridge(c, 1);
        if (!to.bridge && from.bridge) s->set_bridge(c, 0);
        s->enter(c);
    }
    else
    {
        uint8_t flag = s->placement_flag(c);
        s->set_placement_flag(c, 0);
        s->place(c, selected);
        s->set_placement_flag(c, flag);
    }
}
