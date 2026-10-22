#include "ground_passage_entry.h"
int32_t ra2_ground_classify_entry(const Ra2PassageEntryServices *s)
{
    void *c=s->context;
    if(s->delegate(c)==7)return 7;
    int32_t level=s->level(c);
    if(level!=-1){
        Ra2PassageEntryCell cell=s->cell(c);
        if((cell.flags&0x100u)&&level==cell.level+4)s->import_upper(c,cell);
    }
    if(!s->special_mode(c)&&!(s->visible(c)&255u)
        &&!(s->ignores_visibility(c)&255u)&&s->requires_visibility(c))return 7;
    /* 之前的回调可以改写层高和调用参数，基础分类服务负责重新读取。 */
    return s->foot_classify(c);
}
