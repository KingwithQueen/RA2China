/*
 * Opt-in C17 checks of ordinary crew percentages and nonlethal health transitions.
 * From the ra2 directory in an x86 MSVC developer shell:
 *   cl /nologo /std:c17 /W4 /WX /utf-8 /Isrc\gameplay /c tools\crew_percent_static_contract.c
 * This translation unit has no entry point and must not be linked or run.
 */
#include "combat_crew_percent.h"

#define CHECK_VALUE(value, expected) _Static_assert((value) == (expected), #value)
_Static_assert(_Generic(&ra2_crew_percent_roll_below, int (*)(int32_t, int32_t): 1, default: 0),
    "The crew percent checker accepts signed integer draws and cutoffs");
CHECK_VALUE(RA2_CREW_TECHNICIAN_PERCENT, 15);
CHECK_VALUE(RA2_BUILDING_CREW_ENGINEER_PERCENT, 25);

#define CHECK_CREW_DRAW(draw, tech, engineer) \
    CHECK_VALUE(RA2_CREW_ROLL_BELOW_VALUE((draw), RA2_CREW_TECHNICIAN_PERCENT), (tech)); \
    CHECK_VALUE(RA2_CREW_ROLL_BELOW_VALUE((draw), RA2_BUILDING_CREW_ENGINEER_PERCENT), (engineer))
#define CHECK_FIVE_DRAWS(first, tech, engineer) \
    CHECK_CREW_DRAW((first) + 0, (tech), (engineer)); \
    CHECK_CREW_DRAW((first) + 1, (tech), (engineer)); \
    CHECK_CREW_DRAW((first) + 2, (tech), (engineer)); \
    CHECK_CREW_DRAW((first) + 3, (tech), (engineer)); \
    CHECK_CREW_DRAW((first) + 4, (tech), (engineer))
CHECK_FIVE_DRAWS(0, 1, 1);
CHECK_FIVE_DRAWS(5, 1, 1);
CHECK_FIVE_DRAWS(10, 1, 1);
CHECK_FIVE_DRAWS(15, 0, 1);
CHECK_FIVE_DRAWS(20, 0, 1);
CHECK_FIVE_DRAWS(25, 0, 0);
CHECK_FIVE_DRAWS(30, 0, 0);
CHECK_FIVE_DRAWS(35, 0, 0);
CHECK_FIVE_DRAWS(40, 0, 0);
CHECK_FIVE_DRAWS(45, 0, 0);
CHECK_FIVE_DRAWS(50, 0, 0);
CHECK_FIVE_DRAWS(55, 0, 0);
CHECK_FIVE_DRAWS(60, 0, 0);
CHECK_FIVE_DRAWS(65, 0, 0);
CHECK_FIVE_DRAWS(70, 0, 0);
CHECK_FIVE_DRAWS(75, 0, 0);
CHECK_FIVE_DRAWS(80, 0, 0);
CHECK_FIVE_DRAWS(85, 0, 0);
CHECK_FIVE_DRAWS(90, 0, 0);
CHECK_FIVE_DRAWS(95, 0, 0);
#undef CHECK_FIVE_DRAWS
#undef CHECK_CREW_DRAW
#undef CHECK_VALUE

/* Ordinary nonlethal hits, at and around the legacy half-health mark. */
#include "combat_health_threshold.h"
#define CHECK_HEALTH_MARK(maximum, expected) \
    _Static_assert(RA2_HEALTH_HALF_FLOOR_VALUE(maximum) == (expected), #maximum)
#define CHECK_HEALTH_HIT(maximum, before, after, expected) \
    _Static_assert(RA2_HEALTH_CROSSES_HALF_VALUE((before), (after), \
        RA2_HEALTH_HALF_FLOOR_VALUE(maximum)) == (expected), #maximum ": " #before " to " #after)

CHECK_HEALTH_MARK(7, 3);
CHECK_HEALTH_HIT(7, 2, 1, 0);
CHECK_HEALTH_HIT(7, 3, 2, 1);
CHECK_HEALTH_HIT(7, 4, 3, 0);
CHECK_HEALTH_HIT(7, 4, 2, 1);
CHECK_HEALTH_HIT(7, 5, 4, 0);
CHECK_HEALTH_HIT(7, 7, 1, 1);

CHECK_HEALTH_MARK(8, 4);
CHECK_HEALTH_HIT(8, 3, 2, 0);
CHECK_HEALTH_HIT(8, 4, 3, 1);
CHECK_HEALTH_HIT(8, 5, 4, 0);
CHECK_HEALTH_HIT(8, 5, 3, 1);
CHECK_HEALTH_HIT(8, 6, 5, 0);
CHECK_HEALTH_HIT(8, 8, 1, 1);

CHECK_HEALTH_MARK(9, 4);
CHECK_HEALTH_HIT(9, 3, 2, 0);
CHECK_HEALTH_HIT(9, 4, 3, 1);
CHECK_HEALTH_HIT(9, 5, 4, 0);
CHECK_HEALTH_HIT(9, 5, 3, 1);
CHECK_HEALTH_HIT(9, 6, 5, 0);
CHECK_HEALTH_HIT(9, 9, 1, 1);

CHECK_HEALTH_MARK(10, 5);
CHECK_HEALTH_HIT(10, 4, 3, 0);
CHECK_HEALTH_HIT(10, 5, 4, 1);
CHECK_HEALTH_HIT(10, 6, 5, 0);
CHECK_HEALTH_HIT(10, 6, 4, 1);
CHECK_HEALTH_HIT(10, 7, 6, 0);
CHECK_HEALTH_HIT(10, 10, 1, 1);

CHECK_HEALTH_MARK(127, 63);
CHECK_HEALTH_HIT(127, 62, 61, 0);
CHECK_HEALTH_HIT(127, 63, 62, 1);
CHECK_HEALTH_HIT(127, 64, 63, 0);
CHECK_HEALTH_HIT(127, 64, 62, 1);
CHECK_HEALTH_HIT(127, 65, 64, 0);
CHECK_HEALTH_HIT(127, 127, 1, 1);

CHECK_HEALTH_MARK(128, 64);
CHECK_HEALTH_HIT(128, 63, 62, 0);
CHECK_HEALTH_HIT(128, 64, 63, 1);
CHECK_HEALTH_HIT(128, 65, 64, 0);
CHECK_HEALTH_HIT(128, 65, 63, 1);
CHECK_HEALTH_HIT(128, 66, 65, 0);
CHECK_HEALTH_HIT(128, 128, 1, 1);
#undef CHECK_HEALTH_HIT
#undef CHECK_HEALTH_MARK
