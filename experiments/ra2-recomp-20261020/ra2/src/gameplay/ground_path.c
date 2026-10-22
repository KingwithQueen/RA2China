#include <stdint.h>
#include <string.h>
#include "ground_path.h"

static int32_t signed_bits(uint32_t bits)
{
    int32_t value;
    memcpy(&value, &bits, sizeof(value));
    return value;
}

Ra2PathSampleOutcome ra2_ground_consume_path_sample(Ra2PathCursor *cursor, Ra2PathSample sample)
{
    /* 使用无符号运算保留原版 32 位回绕语义，避免极值时 C 的有符号溢出。 */
    cursor->remaining_progress = signed_bits((uint32_t)cursor->remaining_progress - 7u);
    if (sample.x == 0 && sample.y == 0 && cursor->sample_index != 0)
    {
        return RA2_PATH_SAMPLE_REACHES_END;
    }
    return RA2_PATH_SAMPLE_CONTINUES;
}

int32_t ra2_ground_next_sample_index(int32_t current_index)
{
    return signed_bits((uint32_t)current_index + 1u);
}
