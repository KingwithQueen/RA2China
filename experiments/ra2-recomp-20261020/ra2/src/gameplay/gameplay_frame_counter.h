#pragma once
#include <stdint.h>

/* Integer constant expressions shared with the opt-in frame value contract. */
#define RA2_GAMEPLAY_ELAPSED_FRAME_VALUE(now, start) ((uint32_t)(now) - (uint32_t)(start))
#define RA2_GAMEPLAY_FRAME_DEADLINE_VALUE(elapsed, duration) \
    (((uint32_t)(elapsed) ^ UINT32_C(0x80000000)) >= ((uint32_t)(duration) ^ UINT32_C(0x80000000)))
#define RA2_GAMEPLAY_RESIDUAL_FRAME_VALUE(duration, elapsed) ((uint32_t)(duration) - (uint32_t)(elapsed))

static inline uint32_t ra2_gameplay_elapsed_frames(uint32_t now, uint32_t start)
{
    return RA2_GAMEPLAY_ELAPSED_FRAME_VALUE(now, start);
}

/* Bias both bit patterns to reproduce signed 32-bit ordering in unsigned C. */
static inline int ra2_gameplay_frame_deadline_reached(uint32_t elapsed, uint32_t duration)
{
    return RA2_GAMEPLAY_FRAME_DEADLINE_VALUE(elapsed, duration);
}

/* Residual frame bits after the caller's deadline decision. */
static inline uint32_t ra2_gameplay_countdown_residual(uint32_t duration, uint32_t elapsed)
{
    return RA2_GAMEPLAY_RESIDUAL_FRAME_VALUE(duration, elapsed);
}
