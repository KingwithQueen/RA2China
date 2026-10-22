#include "ground_terrain.h"

int ra2_ground_terrain_speed_is_blocked(unsigned upper_layer, uint32_t speed_factor_bits)
{
    if (upper_layer) return 0;
    uint32_t magnitude = speed_factor_bits & UINT32_C(0x7FFFFFFF);
    /* 原版 fcomp 0 的 C3 位在相等和 NaN 时均为 1；不能简化成宿主 == 0。 */
    return magnitude == 0 || magnitude > UINT32_C(0x7F800000);
}

int ra2_ground_terrain_is_blocked(const Ra2TerrainConstraint *terrain)
{
    if (terrain->required_land == -1)
    {
        return 0;
    }
    if (terrain->cell_land == 10)
    {
        if ((terrain->tile_property_2b4 == 5 || terrain->tile_property_2b4 == 4)
            && terrain->tile_property_2b8 == 3 && terrain->cell_subposition != 2)
        {
            return 1;
        }
        if (terrain->tile_property_2b4 == 3
            && (terrain->tile_property_2b8 == 4 || terrain->tile_property_2b8 == 5)
            && terrain->cell_subposition != 6)
        {
            return 1;
        }
    }
    if (terrain->cell_land == terrain->required_land || terrain->cell_land == 10)
    {
        return 0;
    }
    return terrain->overlay_index < 237 || terrain->overlay_index > 238
        || terrain->reference_level == terrain->cell_level;
}
