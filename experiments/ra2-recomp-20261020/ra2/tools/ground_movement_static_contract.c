/*
 * Opt-in C17 compile-only contract for the ground movement value boundary.
 * From this ra2 directory with an x86 MSVC environment:
 *   cl /nologo /std:c17 /W4 /WX /utf-8 /Isrc\gameplay /c tools\ground_movement_static_contract.c
 * Do not link this translation unit. It declares no entry point or fixture.
 * These assertions check types and constants, not gameplay execution.
 */
#include "ground_bridge_plane.h"
#include "ground_cell_coordinates.h"
#include "ground_direction_rules.h"
#include "ground_handoff.h"
#include "ground_sampling.h"
#include "ground_surface_class.h"
#include "ground_world_point.h"

#define CHECK_TYPE(value, type) _Static_assert(_Generic((value), type: 1, default: 0), #value)
#define CHECK_VALUE(name, value) _Static_assert((name) == (value), #name)

CHECK_TYPE(((Ra2WorldPoint){0}).x, int32_t);
CHECK_TYPE(((Ra2WorldPoint){0}).y, int32_t);
CHECK_TYPE(((Ra2WorldPoint){0}).z, int32_t);
CHECK_TYPE(&ra2_ground_world_cell_quotient, int32_t (*)(int32_t));
CHECK_TYPE(&ra2_ground_same_map_cell, int (*)(Ra2WorldPoint, Ra2WorldPoint));
CHECK_TYPE(&ra2_ground_same_world_point, int (*)(Ra2WorldPoint, Ra2WorldPoint));
CHECK_TYPE(&ra2_ground_pack_cell_components, uint32_t (*)(uint16_t, uint16_t));
CHECK_TYPE(&ra2_ground_pack_world_cell, uint32_t (*)(int32_t, int32_t));
CHECK_TYPE(&ra2_ground_heading_octant, unsigned (*)(uint8_t));
CHECK_TYPE(&ra2_ground_opposite_heading, unsigned (*)(int32_t));
CHECK_TYPE(&ra2_ground_template_selector_bits, uint32_t (*)(uint32_t, uint32_t));
CHECK_TYPE(&ra2_ground_folded_axis_magnitude, uint32_t (*)(int32_t, int32_t));
CHECK_TYPE(&ra2_ground_levels_separated, int (*)(int32_t, int32_t));
CHECK_TYPE(&ra2_ground_upper_layer_at_height, int (*)(int32_t, int32_t, int32_t));
CHECK_TYPE(&ra2_ground_bridge_height_matches, int (*)(int32_t, int32_t));
CHECK_TYPE(&ra2_ground_is_tube_land, int (*)(int32_t));

CHECK_VALUE(RA2_PATH_SWAP_XY, 1);
CHECK_VALUE(RA2_PATH_FLIP_X, 2);
CHECK_VALUE(RA2_PATH_FLIP_Y, 4);
CHECK_VALUE(RA2_PATH_SAMPLE_PROGRESS_QUANTUM, 7);
CHECK_VALUE(RA2_SAMPLING_DONE, 0);
CHECK_VALUE(RA2_SAMPLING_FULL_STEP, 1);
CHECK_VALUE(RA2_SAMPLING_REMAINDER, 2);
CHECK_VALUE(RA2_SAMPLING_INVALID_DIRECTION, 3);
CHECK_VALUE(RA2_SAMPLING_INTERPOLATE, 4);

#undef CHECK_TYPE
#undef CHECK_VALUE
