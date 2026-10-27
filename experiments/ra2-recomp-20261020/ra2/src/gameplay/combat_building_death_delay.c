#include "combat_building_death_delay.h"
#define Q(q) s->query(s->context, RA2_BDD_##q)
#define DO(op, value) s->perform(s->context, RA2_BDD_##op, value)

Ra2BuildingDeathTimer ra2_building_death_timer(uint32_t start, uint32_t duration, uint32_t now)
{
    Ra2BuildingDeathTimer result = {duration, 0, start != UINT32_MAX, 0, 0};
    if (result.running) {
        /* 模拟帧减法按32位环绕，比较按有符号数；不用宿主墙钟。 */
        result.elapsed = now - start;
        result.expired = (int32_t)result.elapsed >= (int32_t)duration;
        if (!result.expired) result.value -= result.elapsed;
    }
    result.pending = !result.expired && (int32_t)result.value > 0;
    return result;
}

void ra2_initialize_building_death_delay(const Ra2BuildingDeathDelayServices *s)
{
    /* Selling(19)短路，不读取Explodes；其他任务在回调后读当前类型。 */
    unsigned immediate_timer = Q(MISSION) == 19;
    if (!immediate_timer) immediate_timer = Q(EXPLODES) != 0;
    DO(START_TIMER, immediate_timer ? 0 : 8);
    if (immediate_timer) DO(CLEAR_MISSION_TIMER, 0);
}

int ra2_handoff_building_death(const Ra2BuildingDeathDelayServices *s)
{
    /* 原受伤返回路径在计数仍为正时直接移除，到期/零计数留给建筑AI。 */
    if (!Q(TIMER_PENDING)) return 0;
    DO(UNINIT, 0);
    DO(POST_UNINIT, 0);
    return 1;
}
