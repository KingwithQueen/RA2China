#include "ground_cell_services.h"
#include <string.h>
static int32_t index_of(int32_t x, int32_t y)
{
    uint32_t bits = (uint32_t)y * 512u + (uint32_t)x;
    int32_t index; memcpy(&index, &bits, sizeof(index)); return index;
}
static uintptr_t lookup(const Ra2CellGrid *g, int32_t x, int32_t y, int32_t count)
{
    int32_t index = index_of(x, y);
    if (index >= 0 && index < count && g->cells[index]) return g->cells[index];
    g->fallback_point->x = (int16_t)x;
    g->fallback_point->y = (int16_t)y;
    return g->fallback;
}
uintptr_t ra2_cell_at_world(const Ra2CellGrid *g, Ra2WorldPoint p)
{ return lookup(g, p.x / 256, p.y / 256, g->count); }
uintptr_t ra2_cell_at_point(const Ra2CellGrid *g, Ra2ServiceCell p)
{ return lookup(g, p.x, p.y, 262144); }
int ra2_cell_slot_present(const uint32_t *cells, Ra2ServiceCell p)
{ return cells[index_of(p.x, p.y)] != 0; }
int32_t ra2_cell_threat_index(Ra2ServiceCell p)
{
    /* 4x4 威胁块，每行 130 项；负坐标与原版一样向零除。 */
    return p.x / 4 + (p.y / 4) * 130;
}
