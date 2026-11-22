#pragma once
#include <stdint.h>

enum {
    RA2_CREW_TECHNICIAN_PERCENT = 15,
    RA2_BUILDING_CREW_ENGINEER_PERCENT = 25
};

/* The cutoff itself is excluded from a successful integer percent draw. */
static inline int ra2_crew_percent_roll_below(int32_t draw, int32_t cutoff)
{ return draw < cutoff; }
