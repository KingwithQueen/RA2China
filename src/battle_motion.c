#include "internal.h"
#include "battle_internal.h"
#include <stdlib.h>

int32_t ra_battle_tile_height(const ra_battle_tile *tile, uint32_t local_x, uint32_t local_y)
{
    /* 20 种坡面的平面、截顶和半层偏移；整数分母 256 可精确表达原版的二进制系数。 */
    static const int16_t planes[20][5] = {{1, 0, 0, 104, 0},     {0, 1, 0, 104, 0},     {-1, 0, 104, 104, 0}, {0, -1, 104, 104, 0}, {1, 1, -104, 104, 0},
                                          {-1, 1, 0, 104, 0},    {-1, -1, 104, 104, 0}, {1, -1, 0, 104, 0},   {1, 1, 0, 104, 0},    {-1, 1, 104, 104, 0},
                                          {-1, -1, 208, 104, 0}, {1, -1, 104, 104, 0},  {1, 1, 0, 208, 0},    {-1, 1, 104, 208, 0}, {-1, -1, 208, 208, 0},
                                          {1, -1, 104, 208, 0},  {0, 0, 0, 52, 52},     {0, 0, 104, 52, -52}, {0, 0, 0, 52, 52},    {0, 0, 104, 52, -52}};
    if (!tile) return 0;
    int32_t result = (int32_t)tile->height * 104;
    if (tile->ramp && tile->ramp <= 20)
    {
        const int16_t *p = planes[tile->ramp - 1];
        int32_t value = (p[0] * (int32_t)(local_x & 255) + p[1] * (int32_t)(local_y & 255)) * 104 + (p[2] + p[4]) * 256;
        if (value < 0) value = 0;
        if (value > p[3] * 256) value = p[3] * 256;
        result += value / 256;
    }
    return result;
}
int32_t ra_battle_ground_height(const ra_battle *b, int32_t x, int32_t y)
{
    if (!b || !b->tiles) return 0;
    int64_t tx = (int64_t)x + RA_BATTLE_CELL / 2, ty = (int64_t)y + RA_BATTLE_CELL / 2;
    if (tx < 0 || ty < 0 || tx >= (int64_t)b->width * RA_BATTLE_CELL || ty >= (int64_t)b->height * RA_BATTLE_CELL) return 0;
    uint32_t cell = (uint32_t)(ty / RA_BATTLE_CELL) * b->width + (uint32_t)(tx / RA_BATTLE_CELL);
    return ra_battle_tile_height(&b->tiles[cell], (uint32_t)(tx % RA_BATTLE_CELL) / 256, (uint32_t)(ty % RA_BATTLE_CELL) / 256);
}

uint32_t ra_battle_native_speed(uint32_t speed)
{
    if (speed > 100) speed = 100;
    speed = speed * 256 / 100;
    return speed < 255 ? speed : 255;
}

static int32_t difference(uint32_t target, uint32_t initial)
{
    uint32_t value = (target - initial) & 65535;
    return value >= 32768 ? (int32_t)value - 65536 : (int32_t)value;
}

uint32_t ra_battle_turn_value(const ra_battle_turn *turn, uint32_t tick)
{
    uint32_t elapsed = tick - turn->started;
    int32_t delta;
    if (!turn->duration || elapsed >= turn->duration) return turn->target;
    delta = difference(turn->target, turn->initial);
    /* 原版先做整数除法再乘剩余步，不能交换运算顺序。 */
    return (uint32_t)((int32_t)turn->target - delta / (int32_t)turn->duration * (int32_t)(turn->duration - elapsed)) & 65535;
}

void ra_battle_turn_start(ra_battle_turn *turn, uint32_t target, uint32_t rot, uint32_t tick)
{
    int32_t delta;
    target &= 65535;
    if (target == turn->target) return;
    turn->initial = ra_battle_turn_value(turn, tick);
    turn->target = target;
    turn->started = tick;
    delta = difference(target, turn->initial);
    if (rot > 127) rot = 127;
    turn->duration = rot ? (uint32_t)abs(delta) / (rot * 256) : 0;
}

battle_real battle_motion_target(const ra_battle_type *type, uint32_t terrain, int slope)
{
    uint32_t coefficient = slope > 0 ? type->uphill : slope < 0 ? type->downhill : 10000;
    return battle_real_mul(battle_real_ratio(terrain, 100), battle_real_ratio(coefficient, 10000));
}
uint32_t battle_motion_rate(const ra_battle_type *type, battle_real factor)
{
    /* 国家与特殊速度修正当前均为一；连续系数在第二次原版整数截断处生效。 */
    int32_t leptons = battle_real_integer(battle_real_mul(battle_real_int((int32_t)(type->step / 256)), factor));
    return leptons > 0 ? (uint32_t)leptons * 256 : 0;
}
uint32_t ra_battle_motion_rate(const ra_battle_type *type, uint32_t terrain, int slope, uint32_t factor)
{
    return battle_motion_rate(type, battle_real_mul(battle_motion_target(type, terrain, slope), battle_real_ratio(factor, 10000)));
}
battle_real battle_motion_factor(const ra_battle_type *type, uint32_t distance, battle_real current, battle_real target)
{
    battle_real reduction = battle_real_mul(battle_real_int((int32_t)(type->step / 256)), battle_real_ratio(type->deceleration, 10000));
    if (type->slowdown && distance < type->slowdown)
    {
        battle_real minimum = UINT64_C(0x3fd3333340000000);
        battle_real value = battle_real_sub(current, reduction);
        return battle_real_compare(value, minimum) > 0 ? value : minimum;
    }
    if (battle_real_compare(current, target) < 0)
    {
        battle_real value = battle_real_add(current, battle_real_ratio(type->acceleration, 10000));
        return battle_real_compare(value, target) < 0 ? value : target;
    }
    if (battle_real_compare(current, target) > 0)
    {
        battle_real value = battle_real_sub(current, reduction);
        return battle_real_compare(value, target) > 0 ? value : target;
    }
    return current;
}
uint32_t ra_battle_slowdown(const ra_battle_type *type, uint32_t distance, uint32_t factor)
{
    battle_real value = battle_motion_factor(type, distance, battle_real_ratio(factor, 10000), BATTLE_ONE);
    /* 兼容诊断接口只报告最近万分比；连续模拟必须保留 motion_factor 的全部位。 */
    return (uint32_t)battle_real_integer(battle_real_add(battle_real_mul(value, battle_real_int(10000)), battle_real_ratio(1, 2)));
}

uint32_t battle_sqrt(uint64_t value)
{
    uint64_t result = 0, bit = (uint64_t)1 << 62;
    while (bit > value) bit >>= 2;
    while (bit)
    {
        if (value >= result + bit)
        {
            value -= result + bit;
            result = (result >> 1) + bit;
        }
        else result >>= 1;
        bit >>= 2;
    }
    return (uint32_t)result;
}

uint32_t battle_direction(int64_t dx, int64_t dy)
{
    /* 32 个方向使用固定整数正弦/余弦；浮点显示状态不进入模拟。 */
    static const int16_t xs[32] = {0, 1951,  3827,  5556,  7071,  8315,  9239,  9808,  10000,  9808,  9239,  8315,  7071,  5556,  3827,  1951,
                                   0, -1951, -3827, -5556, -7071, -8315, -9239, -9808, -10000, -9808, -9239, -8315, -7071, -5556, -3827, -1951};
    static const int16_t ys[32] = {-10000, -9808, -9239, -8315, -7071, -5556, -3827, -1951, 0, 1951,  3827,  5556,  7071,  8315,  9239,  9808,
                                   10000,  9808,  9239,  8315,  7071,  5556,  3827,  1951,  0, -1951, -3827, -5556, -7071, -8315, -9239, -9808};
    int64_t best = INT64_MIN;
    uint32_t direction = 0;
    for (uint32_t i = 0; i < 32; ++i)
    {
        int64_t dot = dx * xs[i] + dy * ys[i];
        if (dot > best)
        {
            best = dot;
            direction = i * 2048;
        }
    }
    return direction;
}
