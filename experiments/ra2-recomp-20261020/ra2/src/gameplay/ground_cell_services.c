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

static int32_t signed_bits(uint32_t bits)
{
    int32_t value; memcpy(&value,&bits,sizeof(value)); return value;
}

Ra2MapAreaEdge ra2_cell_area_boundary(const Ra2MapArea *area,Ra2ServiceCell cell,
    int32_t level,unsigned slope)
{
    int32_t sum=(int32_t)cell.x+cell.y;
    uint32_t top=(uint32_t)area->width+2u*(uint32_t)area->local_y;
    /* 坡面靠近上边时再补一层；边界比较仍是原版严格/非严格组合。 */
    if(slope && sum<signed_bits(top+4u+(uint32_t)level))
        level=signed_bits((uint32_t)level+1u);
    int32_t bottom=signed_bits((uint32_t)area->width
        +2u*((uint32_t)area->local_y+(uint32_t)area->local_height)+2u+(uint32_t)level);
    int32_t right=signed_bits(2u*((uint32_t)area->local_x+(uint32_t)area->local_width)-(uint32_t)area->width);
    int32_t left=signed_bits((uint32_t)area->width-2u*(uint32_t)area->local_x);
    if(sum<=signed_bits(top+(uint32_t)level))return RA2_MAP_AREA_ABOVE;
    if(sum>bottom)return RA2_MAP_AREA_BELOW;
    if((int32_t)cell.x-cell.y>=right)return RA2_MAP_AREA_RIGHT;
    if((int32_t)cell.y-cell.x>=left)return RA2_MAP_AREA_LEFT;
    return RA2_MAP_AREA_INSIDE;
}
int ra2_cell_usable_area(const Ra2MapArea *area,Ra2ServiceCell cell,int32_t level,unsigned slope)
{
    return ra2_cell_area_boundary(area,cell,level,slope)==RA2_MAP_AREA_INSIDE;
}
