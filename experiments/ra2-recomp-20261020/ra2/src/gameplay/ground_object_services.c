#include <string.h>
#include "ground_object_services.h"
static uintptr_t scan(int upper, int32_t kind, const Ra2ObjectScanServices *s)
{
    if(!s->enabled(s->context))return 0;
    uintptr_t object=s->head(s->context,upper);
    while(object)
    {
        if(s->kind(s->context,object)==kind)return object;
        /* 类别回调可能改变链；原版在查询之后才读取next。 */
        object=s->next(s->context,object);
    }
    return 0;
}
uintptr_t ra2_ground_find_kind(int upper, int32_t kind, const Ra2ObjectScanServices *s)
{return scan(upper,kind,s);}
uintptr_t ra2_ground_find_blocking_object(const Ra2ObjectScanServices *s)
{
    uintptr_t object=scan(0,2,s);
    if(object)return object;
    object=s->fallback(s->context);
    if(object)return object;
    return scan(0,36,s);
}
uintptr_t ra2_ground_cell_connection(int16_t index, int32_t count, const uint32_t *connections)
{return index>=0 && index<count?connections[index]:0;}
int32_t ra2_ground_surface_level(const Ra2HeightServices *s)
{
    int32_t level=s->cell_level(s->context);
    return level+(s->bridge_layer(s->context)?4:0);
}
static int32_t subtract(int32_t a, int32_t b)
{uint32_t bits=(uint32_t)a-(uint32_t)b;int32_t value;memcpy(&value,&bits,4);return value;}
int32_t ra2_ground_height_above_surface(const Ra2HeightServices *s)
{
    Ra2WorldPoint start=s->position(s->context);
    int32_t ground=s->ground_height(s->context,start);
    int32_t difference=subtract(s->position(s->context).z,ground);
    if(s->bridge_layer(s->context))difference=subtract(difference,s->bridge_height(s->context));
    return difference;
}
