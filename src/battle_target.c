#include "internal.h"
#include "battle_internal.h"
#include "battle_flh.inc"

static battle_real as_float(battle_real value)
{
    return battle_real_float(battle_real_float_bits(value));
}

void battle_muzzle(const ra_battle_type *type, uint32_t facing, int32_t position[3])
{
    const uint32_t *m = flh_matrix[((facing + 1024) & 65535) / 2048];
    battle_real forward = battle_real_int(type->flh[0]), lateral = battle_real_int(type->flh[1]), height = battle_real_int(type->flh[2]);
    for (unsigned row = 0; row < 3; ++row)
    {
        /* Translate 的前两项求和顺序与原版 float 矩阵一致；最终坐标逐轴向零截断。 */
        battle_real a = battle_real_mul(lateral, battle_real_float(m[row * 4 + 1]));
        battle_real b = battle_real_mul(height, battle_real_float(m[row * 4 + 2]));
        battle_real c = battle_real_mul(forward, battle_real_float(m[row * 4]));
        battle_real value = as_float(battle_real_add(battle_real_add(a, b), c));
        if (row == 1) value ^= UINT64_C(0x8000000000000000);
        position[row] += battle_real_integer(value);
    }
}

uint32_t battle_damage(const ra_battle_weapon *weapon, uint32_t armor, uint32_t distance)
{
    if (!weapon->damage || armor >= 11) return 0;
    uint32_t radius = weapon->spread / 256;
    if (distance > radius) return 0;
    battle_real damage = battle_real_int((int32_t)weapon->damage);
    battle_real percent = weapon->percent_bits ? battle_real_float(weapon->percent_bits) : as_float(battle_real_ratio(weapon->percent_at_max, 10000));
    battle_real edge = as_float(battle_real_mul(damage, percent));
    int32_t value = (int32_t)weapon->damage;
    if (radius && battle_real_compare(edge, damage))
    {
        battle_real part =
            battle_real_div(battle_real_mul(battle_real_sub(damage, edge), battle_real_int((int32_t)(radius - distance))), battle_real_int((int32_t)radius));
        value = battle_real_integer(battle_real_add(part, edge));
    }
    if (value <= 0) return 0;
    value = battle_real_integer(battle_real_mul(battle_real_int(value), battle_real_ratio(weapon->verses[armor], 10000)));
    uint32_t maximum = weapon->max_damage;
    return value > 0 ? ((uint32_t)value < maximum ? (uint32_t)value : maximum) : 0;
}

int32_t battle_threat_score(const ra_battle *b, const ra_battle_unit *u, const ra_battle_unit *v)
{
    const ra_battle_type *own = &b->types[u->type], *other = &b->types[v->type];
    battle_real coefficients[5];
    for (unsigned i = 0; i < 5; ++i) coefficients[i] = battle_real_div(battle_real_int(own->threat_coefficients[i]), battle_real_int(10000));
    battle_real score = battle_real_mul(coefficients[1], battle_real_ratio(other->weapon.verses[own->armor], 10000));
    if (!other->weapon.id[0] && !other->weapon.damage) score = 0;
    if (v->target == u->id && score) score ^= UINT64_C(0x8000000000000000);
    score = battle_real_add(score, battle_real_mul(coefficients[2], battle_real_div(battle_real_int(other->special_threat), battle_real_int(10000))));
    score = battle_real_add(score, battle_real_mul(coefficients[0], battle_real_ratio(own->weapon.verses[other->armor], 10000)));
    score = battle_real_add(score,
                            battle_real_mul(battle_real_div(battle_real_int((int32_t)v->health), battle_real_int((int32_t)other->strength)), coefficients[3]));
    uint32_t cells = battle_sqrt(battle_distance_squared(u, v)) / RA_BATTLE_CELL, range = own->weapon.range / RA_BATTLE_CELL;
    score = battle_real_add(score, battle_real_mul(battle_real_int((int32_t)(cells > range ? cells - range : 0)), coefficients[4]));
    score = battle_real_add(score, battle_real_int(100000));
    int32_t result = battle_real_integer(score);
    return result > 0 ? result : 1;
}
