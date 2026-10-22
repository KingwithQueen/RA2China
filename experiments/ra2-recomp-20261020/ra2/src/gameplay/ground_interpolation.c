#include <string.h>
#include "ground_interpolation.h"

static int32_t signed_bits(uint32_t bits)
{ int32_t value; memcpy(&value, &bits, sizeof(value)); return value; }
static int32_t add(int32_t a, int32_t b)
{ return signed_bits((uint32_t)a + (uint32_t)b); }
static int32_t subtract(int32_t a, int32_t b)
{ return signed_bits((uint32_t)a - (uint32_t)b); }
static int same_cell(Ra2WorldPoint a, Ra2WorldPoint b)
{
    return (uint16_t)(a.x / 256) == (uint16_t)(b.x / 256)
        && (uint16_t)(a.y / 256) == (uint16_t)(b.y / 256);
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
    Ra2WorldPoint selected = current;
    if (partial_cell == end_cell || partial_cell == start_cell) selected = partial;
    else if (progress > 3) selected = endpoint;
    /* 第四次查询也必须保留；不能用前面的结果代替，世界可能已经改变。 */
    uintptr_t selected_cell = s->cell_at(c, selected);
    current = s->position(c);
    if (!same_cell(current, selected))
    {
        s->leave(c);
        s->place(c, selected);
        Ra2InterpolationSurface from = s->surface(c, start_cell);
        Ra2InterpolationSurface to = s->surface(c, selected_cell);
        if (to.level == subtract(from.level, 4) && to.bridge) s->set_bridge(c, 1);
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
