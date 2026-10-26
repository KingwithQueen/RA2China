#include <limits.h>
#include "combat_building_shake.h"

Ra2ShakeAmplitude ra2_building_shake_amplitude(int32_t cost, int32_t divisor)
{
    Ra2ShakeAmplitude result = {0, 0, 0};
    /* 非法配置沿用已有生成宿主的有界结果，不在C中执行未定义除法。
       原机器码的除零/商溢出异常单独保留，不计为原版等价通过。 */
    if (!divisor) return result;
    if (cost == INT32_MIN && divisor == -1) { result.quotient = INT32_MIN; return result; }
    result.quotient = cost / divisor;
    result.remainder = cost % divisor;
    result.division_valid = 1;
    return result;
}

void ra2_schedule_building_shake(const Ra2BuildingShakeServices *s)
{
    int32_t cost = s->cost(s->context);
    /* 原版在归属相关的造价回调返回后，重新读取全局Rules与ShakeScreen。 */
    int32_t divisor = s->divisor(s->context);
    Ra2ShakeAmplitude amplitude = ra2_building_shake_amplitude(cost, divisor);
    s->publish(s->context, amplitude);
    if (amplitude.quotient > s->threshold) s->dispatch(s->context, amplitude.quotient);
}

void ra2_legacy_screen_shake(int32_t amplitude)
{
    (void)amplitude;
}
