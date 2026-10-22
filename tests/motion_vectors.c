#include "internal.h"
#include "battle_internal.h"
#include <stdio.h>

/* 只输出 C 实现结果；原版指令结果由独立验证工具产生并逐项比较。 */
int main(void)
{
    const uint32_t speeds[] = {0, 1, 2, 5, 6, 7, 10, 25, 50, 99, 100, 101};
    const uint32_t factors[] = {10000, 7000, 8000, 12000, 8400, 3000};
    const uint32_t rotations[] = {1, 5, 8, 127}, starts[] = {0, 0, 65000, 16000}, targets[] = {16384, 32768, 1000, 0};
    const uint32_t distances[] = {501, 500, 499, 256, 64, 0};
    ra_battle_type type = {0};
    ra_battle b = {0};
    type.uphill = 10000;
    type.downhill = 12000;
    type.slowdown = 500;
    type.deceleration = 20;
    printf("{\"speed\":[");
    for (unsigned i = 0; i < 12; ++i) printf("%s%u", i ? "," : "", ra_battle_native_speed(speeds[i]));
    printf("],\"scaled\":[");
    for (unsigned base = 15; base <= 17; base += 2)
        for (unsigned i = 0; i < 6; ++i)
        {
            type.step = base * 256;
            printf("%s%u", base == 15 && !i ? "" : ",", ra_battle_motion_rate(&type, 100, 0, factors[i]) / 256);
        }
    printf("],\"turns\":[");
    for (unsigned i = 0; i < 4; ++i)
        for (unsigned j = 0; j < 4; ++j)
        {
            ra_battle_turn turn = {starts[j], starts[j], 0, 0};
            ra_battle_turn_start(&turn, targets[j], rotations[i], 100);
            printf("%s{\"duration\":%u,\"values\":[", i || j ? "," : "", turn.duration);
            for (uint32_t tick = 0; tick < turn.duration + 2; ++tick) printf("%s%u", tick ? "," : "", ra_battle_turn_value(&turn, 100 + tick));
            printf("]}");
        }
    printf("],\"slopes\":[");
    for (unsigned i = 0; i < 3; ++i)
        for (unsigned j = 0; j < 2; ++j)
        {
            uint32_t slope = i == 2 ? type.downhill : type.uphill;
            printf("%s%u", i || j ? "," : "", slope * (j ? 70 : 100) / 100);
        }
    printf("],\"slowdown\":[");
    for (unsigned base = 15; base <= 17; base += 2)
        for (unsigned i = 0; i < 6; ++i)
        {
            type.step = base * 256;
            printf("%s%u", base == 15 && !i ? "" : ",", ra_battle_slowdown(&type, distances[i], 10000));
        }
    printf("],\"random\":[");
    battle_random_reset(&b);
    for (unsigned i = 0; i < 512; ++i) printf("%s%u", i ? "," : "", battle_random_delay(&b));
    puts("]}");
    return 0;
}
