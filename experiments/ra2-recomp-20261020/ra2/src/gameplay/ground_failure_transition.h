#pragma once
#include "ground_prepare.h"
/* 清除有效路段；原本已无路段时，不额外改变 driving。 */
void ra2_ground_invalidate_segment(Ra2WorldPoint *end, unsigned *driving, Ra2WorldPoint invalid);
/* 调用者在清除路段后查询实时目标。取消目标服务可改变对象，随后再调用停止服务。 */
int ra2_ground_stop_target(int variant, void *context, void (*cancel)(void *),
    int (*stop)(void *, int));
