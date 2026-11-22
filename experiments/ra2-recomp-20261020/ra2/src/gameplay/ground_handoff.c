#include "ground_handoff.h"
#include "ground_bridge_plane.h"

unsigned ra2_ground_prepare_upper_layer(uint32_t cell_flags, int8_t cell_level,
    int32_t z, int32_t height_per_level)
{
    if (!ra2_ground_bridge_cell_flag_present(cell_flags))
        return 0;

    return ra2_ground_upper_layer_at_height(cell_level, z, height_per_level);
}
