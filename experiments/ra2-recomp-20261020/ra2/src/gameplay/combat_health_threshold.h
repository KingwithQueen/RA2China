#pragma once
#include <stdint.h>

/* These constant expressions also support the opt-in combat value checks.
   Pass already-read scalar values for maximum and half. */
#define RA2_HEALTH_HALF_FLOOR_VALUE(maximum) \
    ((int32_t)(maximum) / 2 - ((int32_t)(maximum) < 0 && (int32_t)(maximum) % 2 != 0))

/* Keep the after-health expression on the short-circuited right side. */
#define RA2_HEALTH_CROSSES_HALF_VALUE(before, after, half) \
    ((int32_t)(before) >= (int32_t)(half) && (int32_t)(after) < (int32_t)(half))
