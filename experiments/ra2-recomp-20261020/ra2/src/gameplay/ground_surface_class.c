#include "ground_surface_class.h"

int ra2_ground_is_tube_entrance(int16_t connection, int32_t count, int32_t land)
{
    return connection >= 0 && connection < count && land == 10;
}

int ra2_ground_is_tile_family(int32_t tile, int32_t first)
{
    /* 上界采用原32位回绕，再进行有符号比较。 */
    return tile >= first && tile < (int32_t)((uint32_t)first + 14u);
}

int32_t ra2_ground_surface_support_height(const Ra2SurfaceSupportServices *services)
{
    void *context = services->context;
    int32_t height = services->base_height(context);

    /* 先计算坡面高度，再读取开关及对象链；计算回调可能改变二者。 */
    if (services->scan_objects(context)) {
        for (uintptr_t object = services->first_object(context); object;
             object = services->next_object(context, object)) {
            if (services->object_kind(context, object) == 6)
                return (int32_t)((uint32_t)height +
                    (uint32_t)services->support_height(context, object));
        }
    }
    if (services->fallback_support(context))
        height = (int32_t)((uint32_t)height + 85u);
    return height;
}
