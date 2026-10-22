#include "ground_handoff.h"

unsigned ra2_ground_prepare_upper_layer(uint32_t cell_flags, int8_t cell_level,
    int32_t z, int32_t height_per_level)
{
    if (!(cell_flags & 0x100u))
        return 0;

    /* 原入口要求高度单位非零且除法可表示；有符号除法向零截断。 */
    int32_t divided = z / height_per_level;
    uint32_t difference = (uint32_t)divided - (uint32_t)(int32_t)cell_level;
    uint32_t absolute = difference & 0x80000000u ? 0u - difference : difference;
    return (int32_t)absolute > 2;
}
