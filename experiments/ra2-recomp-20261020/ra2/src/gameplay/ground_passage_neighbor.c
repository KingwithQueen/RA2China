#include "ground_passage_neighbor.h"
int ra2_ground_neighbor_blocks(int32_t direction,const Ra2NeighborPassageServices *s)
{
    unsigned opposite=((uint32_t)direction-4u)&7u;
    uintptr_t cell=s->neighbor(s->context,opposite);
    uintptr_t object=s->obstacle(s->context,cell);
    if(!object) return 0;
    int32_t delta=(int32_t)(opposite-(uint32_t)s->orientation(s->context,object));
    uint32_t magnitude=delta<0?0u-(uint32_t)delta:(uint32_t)delta;
    return (int32_t)magnitude>2 && (int32_t)magnitude<6 && direction!=-1;
}
