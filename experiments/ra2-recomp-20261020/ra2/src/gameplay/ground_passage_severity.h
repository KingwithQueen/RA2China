#pragma once
#include <stdint.h>

/* A weaker or equal obstacle must not write the current passage class. */
static inline void ra2_ground_raise_passage_floor(int32_t *passage, int32_t minimum)
{
    if (*passage < minimum)
        *passage = minimum;
}
