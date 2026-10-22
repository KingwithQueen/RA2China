#include <string.h>
#include "ground_landing.h"

int ra2_ground_land_connection(const Ra2LandingServices *s)
{
    void *c = s->context;
    if (s->selector(c) != -1) return 1;
    s->leave_cell(c);
    s->clear_segment(c);
    int32_t index = s->connection_index(c);
    if (!s->connection_exists(c, index))
    {
        s->reject_connection(c);
        return 0;
    }
    s->start_connection(c, index);
    s->set_approach_point(c);
    int32_t start = s->current_ground_height(c), duration;
    int32_t finish = s->target_ground_height(c, &duration);
    uint32_t difference = (uint32_t)finish - (uint32_t)start;
    int32_t signed_difference;
    memcpy(&signed_difference, &difference, sizeof(difference));
    /* 原版连接时长必须非零，并满足x86有符号除法的有效范围。 */
    uint32_t result = (uint32_t)(signed_difference / duration) + (uint32_t)start;
    int32_t height;
    memcpy(&height, &result, sizeof(height));
    s->finish_connection(c, height);
    return 0;
}

void ra2_ground_reject_direction(int32_t *path_head, int32_t rejected_value)
{ *path_head = rejected_value; }
