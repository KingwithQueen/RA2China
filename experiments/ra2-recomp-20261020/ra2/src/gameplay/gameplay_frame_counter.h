#pragma once
#include <stdint.h>

static inline uint32_t ra2_gameplay_elapsed_frames(uint32_t now, uint32_t start)
{
    return now - start;
}

/* Bias both bit patterns to reproduce signed 32-bit ordering in unsigned C. */
static inline int ra2_gameplay_frame_deadline_reached(uint32_t elapsed, uint32_t duration)
{
    return (elapsed ^ UINT32_C(0x80000000)) >= (duration ^ UINT32_C(0x80000000));
}
