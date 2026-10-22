#include "internal.h"
#include "battle_internal.h"
#include "battle_trig_tables.h"

#define BATTLE_PI UINT64_C(0x400921fb54442d18)
#define BATTLE_HALF_PI UINT64_C(0x3ff921fb54442d18)
#define BATTLE_ANGLE_SCALE UINT64_C(0xc0c45f07af68ecef)
#define BATTLE_RADIAN_SCALE UINT64_C(0xbf19222d989f5e57)

battle_real battle_legacy_sqrt(battle_real value)
{
    /* 原版先截为单精度，再按尾数每 1024 个编码取同一个平方根。直接计算同一采样点，免存 16384 项表。 */
    uint32_t sample = battle_real_float_bits(value & UINT64_C(0x7fffffffffffffff)) & ~1023u;
    return battle_real_float(battle_real_float_bits(battle_real_sqrt(battle_real_float(sample))));
}
static battle_real sine_index(uint32_t index)
{
    uint32_t sign = 0, at;
    /* 保留原版对整圆周参数约简留下的极小残值，避免其符号进入后续取整边界。 */
    if (index == 4096) return battle_real_float(0x250d3000u);
    if (index == 8192) return battle_real_float(0xa58d3000u);
    index %= 8192;
    if (index <= 2048) at = index;
    else if (index <= 4096) at = 4096 - index;
    else if (index <= 6144)
    {
        at = index - 4096;
        sign = 0x80000000u;
    }
    else
    {
        at = 8192 - index;
        sign = 0x80000000u;
    }
    return battle_real_float(battle_sine_table[at] ^ sign);
}
battle_real battle_legacy_trig(battle_real value, bool cosine)
{
    int32_t encoded = battle_real_integer(battle_real_mul(value, battle_real_float(0x4522f983u))), index = encoded / 2 % 8192;
    if (index < 0) index += 8192;
    if (cosine) index += 2048;
    if ((encoded & 1) && index < (cosine ? 10239 : 8191)) ++index;
    return sine_index((uint32_t)index);
}
battle_real battle_legacy_acos(battle_real value)
{
    int32_t index = battle_real_integer(battle_real_mul(battle_real_add(value, BATTLE_ONE), battle_real_int(2048))) - 2048;
    uint32_t at = (uint32_t)(index < 0 ? -index : index);
    if (at > 2048) at = 2048;
    battle_real angle = battle_real_float(battle_arcsine_table[at] ^ (index < 0 ? 0x80000000u : 0));
    return battle_real_sub(BATTLE_HALF_PI, angle);
}
battle_real battle_legacy_atan(battle_real y, battle_real x)
{
    y = battle_real_float(battle_real_float_bits(y));
    x = battle_real_float(battle_real_float_bits(x));
    if (!x) return !y ? 0 : battle_real_float(y >> 63 ? 0xbfc90fdbu : 0x3fc90fdbu);
    int32_t index = battle_real_integer(battle_real_div(battle_real_div(y, x), battle_real_float(0x3cc7fe84u)));
    uint32_t at = (uint32_t)(index < 0 ? -(int64_t)index : index);
    battle_real angle = battle_real_float(at <= 4096 ? battle_arctangent_table[at] : 0x3fc90fdbu);
    if (x >> 63) angle = battle_real_sub(BATTLE_PI, angle);
    return y >> 63 ? angle ^ UINT64_C(0x8000000000000000) : angle;
}
bool battle_arc_angle(uint32_t distance, int32_t height, uint32_t speed, battle_real gravity, bool high, battle_real *angle)
{
    battle_real x = battle_real_int((int32_t)distance), y = battle_real_int(height), v = battle_real_int((int32_t)speed);
    if (height > 0)
    {
        *angle = UINT64_C(0x3fe921d9f4d37c12);
        return true;
    }
    if (!distance || !speed) return false;
    battle_real q = battle_real_mul(v, v), xx = battle_real_mul(x, x), a = battle_real_sub(q, battle_real_mul(y, gravity));
    battle_real d =
        battle_real_sub(battle_real_sub(battle_real_mul(q, q), battle_real_mul(battle_real_mul(battle_real_mul(q, y), gravity), battle_real_int(2))),
                        battle_real_mul(battle_real_mul(gravity, gravity), xx));
    if (battle_real_compare(d, 0) < 0) return false;
    battle_real denominator = battle_real_mul(battle_real_add(battle_real_div(battle_real_mul(y, y), xx), BATTLE_ONE), battle_real_int(2));
    battle_real root = battle_legacy_sqrt(d), r = battle_real_div(high ? battle_real_sub(a, root) : battle_real_add(a, root), denominator);
    if (battle_real_compare(r, 0) < 0) return false;
    *angle = battle_legacy_acos(battle_real_div(battle_legacy_sqrt(r), v));
    return true;
}
bool battle_arc_direction(uint32_t distance, int32_t height, uint32_t speed, battle_real gravity, bool high, uint32_t *direction)
{
    battle_real angle, next;
    if (!battle_arc_angle(distance, height, speed, gravity, high, &angle)) return false;
    if (!high && battle_arc_angle(distance + 1, height, speed, gravity, false, &next) && battle_real_compare(next, angle) < 0)
        angle ^= UINT64_C(0x8000000000000000);
    *direction = (uint32_t)battle_real_integer(battle_real_mul(battle_real_sub(angle, BATTLE_HALF_PI), BATTLE_ANGLE_SCALE)) & 65535;
    return true;
}
uint32_t battle_projectile_speed(uint32_t distance, battle_real gravity)
{
    return (uint32_t)battle_real_integer(
        battle_legacy_sqrt(battle_real_mul(battle_real_mul(battle_real_int((int32_t)distance), gravity), battle_real_ratio(6, 5))));
}
uint32_t battle_native_direction(int32_t dx, int32_t dy)
{
    battle_real angle = battle_legacy_atan(battle_real_int(-dy), battle_real_int(dx));
    return (uint32_t)battle_real_integer(battle_real_mul(battle_real_sub(angle, BATTLE_HALF_PI), BATTLE_ANGLE_SCALE)) & 65535;
}
static battle_real direction_radians(uint32_t direction)
{
    int32_t signed_direction = direction >= 32768 ? (int32_t)direction - 65536 : (int32_t)direction;
    return battle_real_mul(battle_real_int(signed_direction - 16383), BATTLE_RADIAN_SCALE);
}
bool battle_projectile_launch(const ra_battle_weapon *w, int32_t dx, int32_t dy, int32_t height, battle_real velocity[3])
{
    battle_real gravity = battle_real_ratio(w->gravity, w->floater ? 512 : 256);
    battle_real x = battle_real_int(dx), y = battle_real_int(dy);
    uint32_t distance = (uint32_t)battle_real_integer(battle_legacy_sqrt(battle_real_add(battle_real_mul(x, x), battle_real_mul(y, y))));
    uint32_t speed = w->projectile_rot ? w->speed : battle_projectile_speed(distance, gravity), direction;
    if (!speed || !battle_arc_direction(distance, height, speed, gravity, w->high, &direction)) return false;
    battle_real horizontal = direction_radians(battle_native_direction(dx, dy));
    battle_real initial = battle_real_mul(battle_real_div(battle_real_int((int32_t)speed), battle_real_int(100)), battle_real_int(100));
    initial = battle_legacy_sqrt(battle_real_mul(initial, initial));
    velocity[0] = battle_real_mul(battle_legacy_trig(horizontal, true), initial);
    velocity[1] = battle_real_mul(battle_legacy_trig(horizontal, false), initial) ^ UINT64_C(0x8000000000000000);
    battle_real magnitude = battle_legacy_sqrt(battle_real_add(battle_real_mul(velocity[0], velocity[0]), battle_real_mul(velocity[1], velocity[1])));
    battle_real vertical = direction_radians(direction), cosine = battle_legacy_trig(vertical, true);
    velocity[0] = battle_real_mul(cosine, velocity[0]);
    velocity[1] = battle_real_mul(cosine, velocity[1]);
    velocity[2] = battle_real_mul(battle_legacy_trig(vertical, false), magnitude);
    return true;
}
void battle_projectile_step(int32_t position[3], battle_real velocity[3], battle_real gravity)
{
    /* 原版先从竖直速度扣重力，再推进位置；每步坐标取整，不保留位置的小数余量。 */
    velocity[2] = battle_real_sub(velocity[2], gravity);
    for (unsigned i = 0; i < 3; ++i) position[i] = battle_real_integer(battle_real_add(battle_real_int(position[i]), velocity[i]));
}
