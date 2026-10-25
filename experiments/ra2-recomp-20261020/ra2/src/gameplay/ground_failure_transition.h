#pragma once
#include "ground_prepare.h"
/* 清除有效路段；原本已无路段时，不额外改变 driving。 */
void ra2_ground_invalidate_segment(Ra2WorldPoint *end, unsigned *driving, Ra2WorldPoint invalid);
/* 调用者在清除路段后查询实时目标。取消目标服务可改变对象，随后再调用停止服务。 */
int ra2_ground_stop_target(int variant, void *context, void (*cancel)(void *),
    int (*stop)(void *, int));

/* CloseEnough与两层高度均采用严格小于；无符号计算保留32位差值位模式。 */
int ra2_ground_within_stop_distance(int32_t distance,int32_t close_enough);
int32_t ra2_ground_axis_distance(int32_t left,int32_t right);
int ra2_ground_within_stop_height(int32_t left,int32_t right,int32_t level_height);
