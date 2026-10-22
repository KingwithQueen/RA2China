#include "battle_internal.h"
#include "battle_matrix.inc"
#include <string.h>

static void rotate(uint32_t m[12], int direction)
{
    battle_real sine = matrix_rotation[direction + 31].sine, cosine = battle_real_float(matrix_rotation[direction + 31].cosine);
    for (unsigned row = 0; row < 3; ++row)
    {
        battle_real x = battle_real_float(m[row * 4]), y = battle_real_float(m[row * 4 + 1]);
        /* 原版 5909a0 保留 sine 为 double，cosine 先存 float，每个矩阵元素再向零舍入。 */
        m[row * 4] = battle_real_float_bits(battle_real_add(battle_real_mul(y, sine), battle_real_mul(x, cosine)));
        m[row * 4 + 1] = battle_real_float_bits(battle_real_sub(battle_real_mul(y, cosine), battle_real_mul(x, sine)));
    }
}

bool ra_battle_chassis(uint32_t ramp, uint32_t facing, uint32_t matrix[12])
{
    if (ramp > 20 || !matrix) return false;
    memcpy(matrix, ramp_matrix[ramp], 12 * sizeof(*matrix));
    rotate(matrix, (int)(((facing + 1024) & 65535) / 2048) - 8);
    return true;
}

static void translate(uint32_t m[12], const int32_t value[3])
{
    for (unsigned row = 0; row < 3; ++row)
    {
        battle_real a = battle_real_mul(battle_real_int(value[1]), battle_real_float(m[row * 4 + 1]));
        battle_real b = battle_real_mul(battle_real_int(value[2]), battle_real_float(m[row * 4 + 2]));
        battle_real c = battle_real_mul(battle_real_int(value[0]), battle_real_float(m[row * 4]));
        m[row * 4 + 3] = battle_real_float_bits(battle_real_add(battle_real_add(battle_real_add(a, b), c), battle_real_float(m[row * 4 + 3])));
    }
}

void battle_chassis_muzzle(const ra_battle_type *type, uint32_t ramp, uint32_t body, uint32_t turret, int32_t position[3])
{
    uint32_t m[12];
    if (!ra_battle_chassis(ramp, body, m)) return;
    int32_t offset[3] = {type->turret_offset, 0, 0};
    translate(m, offset);
    int difference = (int)(((turret + 1024) & 65535) / 2048) - (int)(((body + 1024) & 65535) / 2048);
    rotate(m, difference);
    translate(m, type->flh);
    for (unsigned row = 0; row < 3; ++row)
    {
        battle_real value = battle_real_float(m[row * 4 + 3]);
        if (row == 1) value ^= UINT64_C(0x8000000000000000);
        position[row] += battle_real_integer(value);
    }
}
