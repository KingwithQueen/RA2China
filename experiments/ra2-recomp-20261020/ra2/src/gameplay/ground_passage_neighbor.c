#include "ground_passage_neighbor.h"
#include "ground_direction_rules.h"
int ra2_ground_neighbor_blocks(int32_t direction,const Ra2NeighborPassageServices *s)
{
    unsigned opposite=((uint32_t)direction-4u)&7u;
    uintptr_t cell=s->neighbor(s->context,opposite);
    uintptr_t object=s->obstacle(s->context,cell);
    if(!object) return 0;
    int32_t orientation=s->orientation(s->context,object);
    return ra2_ground_direction_conflicts((int32_t)opposite,orientation) && direction!=-1;
}
