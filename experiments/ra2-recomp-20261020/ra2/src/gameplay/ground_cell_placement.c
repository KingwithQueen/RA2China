#include "ground_cell_placement.h"

Ra2CellPlacementResult ra2_ground_place_cell(const Ra2CellPlacementServices *s,
    unsigned needs_leave)
{
    void *context=s->context;
    Ra2CellPlacementResult result={0,0};
    if(needs_leave) s->leave(context);
    s->place(context);
    s->update_layer(context);
    if(s->before_enter && !s->before_enter(context)) return result;
    result.value=s->enter(context);
    result.entered=1;
    return result;
}
