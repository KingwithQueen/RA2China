#include "ground_passage_entry.h"
#include "ground_bridge_plane.h"
#include "ground_collision.h"
int32_t ra2_ground_classify_entry(const Ra2PassageEntryServices *s)
{
    void *c=s->context;
    if(s->delegate(c)==RA2_CELL_BLOCKED)return RA2_CELL_BLOCKED;
    int32_t level=s->level(c);
    if(level!=-1){
        Ra2PassageEntryCell cell=s->cell(c);
        if((cell.flags&0x100u)&&ra2_ground_bridge_height_matches(level,cell.level))s->import_upper(c,cell);
    }
    if(!s->special_mode(c)&&!(s->visible(c)&255u)
        &&!(s->ignores_visibility(c)&255u)&&s->requires_visibility(c))return RA2_CELL_BLOCKED;
    /* 之前的回调可以改写层高和调用参数，基础分类服务负责重新读取。 */
    return s->foot_classify(c);
}
