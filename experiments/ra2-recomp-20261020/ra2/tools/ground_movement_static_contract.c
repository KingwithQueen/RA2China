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

/* Evaluate the very same direction expressions used by the inline wrappers. */
#define CHECK_OCTANT_BLOCK(base, expected) \
    CHECK_VALUE(RA2_GROUND_HEADING_OCTANT_BITS((base) + 0u), (expected)); \
    CHECK_VALUE(RA2_GROUND_HEADING_OCTANT_BITS((base) + 1u), (expected)); \
    CHECK_VALUE(RA2_GROUND_HEADING_OCTANT_BITS((base) + 2u), (expected)); \
    CHECK_VALUE(RA2_GROUND_HEADING_OCTANT_BITS((base) + 3u), (expected)); \
    CHECK_VALUE(RA2_GROUND_HEADING_OCTANT_BITS((base) + 4u), (expected)); \
    CHECK_VALUE(RA2_GROUND_HEADING_OCTANT_BITS((base) + 5u), (expected)); \
    CHECK_VALUE(RA2_GROUND_HEADING_OCTANT_BITS((base) + 6u), (expected)); \
    CHECK_VALUE(RA2_GROUND_HEADING_OCTANT_BITS((base) + 7u), (expected)); \
    CHECK_VALUE(RA2_GROUND_HEADING_OCTANT_BITS((base) + 8u), (expected)); \
    CHECK_VALUE(RA2_GROUND_HEADING_OCTANT_BITS((base) + 9u), (expected)); \
    CHECK_VALUE(RA2_GROUND_HEADING_OCTANT_BITS((base) + 10u), (expected)); \
    CHECK_VALUE(RA2_GROUND_HEADING_OCTANT_BITS((base) + 11u), (expected)); \
    CHECK_VALUE(RA2_GROUND_HEADING_OCTANT_BITS((base) + 12u), (expected)); \
    CHECK_VALUE(RA2_GROUND_HEADING_OCTANT_BITS((base) + 13u), (expected)); \
    CHECK_VALUE(RA2_GROUND_HEADING_OCTANT_BITS((base) + 14u), (expected)); \
    CHECK_VALUE(RA2_GROUND_HEADING_OCTANT_BITS((base) + 15u), (expected))
CHECK_OCTANT_BLOCK(0x00u, 0u);
CHECK_OCTANT_BLOCK(0x10u, 1u);
CHECK_OCTANT_BLOCK(0x20u, 1u);
CHECK_OCTANT_BLOCK(0x30u, 2u);
CHECK_OCTANT_BLOCK(0x40u, 2u);
CHECK_OCTANT_BLOCK(0x50u, 3u);
CHECK_OCTANT_BLOCK(0x60u, 3u);
CHECK_OCTANT_BLOCK(0x70u, 4u);
CHECK_OCTANT_BLOCK(0x80u, 4u);
CHECK_OCTANT_BLOCK(0x90u, 5u);
CHECK_OCTANT_BLOCK(0xa0u, 5u);
CHECK_OCTANT_BLOCK(0xb0u, 6u);
CHECK_OCTANT_BLOCK(0xc0u, 6u);
CHECK_OCTANT_BLOCK(0xd0u, 7u);
CHECK_OCTANT_BLOCK(0xe0u, 7u);
CHECK_OCTANT_BLOCK(0xf0u, 0u);
#undef CHECK_OCTANT_BLOCK

#define CHECK_SELECTOR_ROW(row, first) \
    CHECK_VALUE(RA2_GROUND_TEMPLATE_SELECTOR_BITS((row), 0u), (first) + 0u); \
    CHECK_VALUE(RA2_GROUND_TEMPLATE_SELECTOR_BITS((row), 1u), (first) + 1u); \
    CHECK_VALUE(RA2_GROUND_TEMPLATE_SELECTOR_BITS((row), 2u), (first) + 2u); \
    CHECK_VALUE(RA2_GROUND_TEMPLATE_SELECTOR_BITS((row), 3u), (first) + 3u); \
    CHECK_VALUE(RA2_GROUND_TEMPLATE_SELECTOR_BITS((row), 4u), (first) + 4u); \
    CHECK_VALUE(RA2_GROUND_TEMPLATE_SELECTOR_BITS((row), 5u), (first) + 5u); \
    CHECK_VALUE(RA2_GROUND_TEMPLATE_SELECTOR_BITS((row), 6u), (first) + 6u); \
    CHECK_VALUE(RA2_GROUND_TEMPLATE_SELECTOR_BITS((row), 7u), (first) + 7u)
CHECK_SELECTOR_ROW(0u, 0u);
CHECK_SELECTOR_ROW(1u, 8u);
CHECK_SELECTOR_ROW(2u, 16u);
CHECK_SELECTOR_ROW(3u, 24u);
CHECK_SELECTOR_ROW(4u, 32u);
CHECK_SELECTOR_ROW(5u, 40u);
CHECK_SELECTOR_ROW(6u, 48u);
CHECK_SELECTOR_ROW(7u, 56u);
#undef CHECK_SELECTOR_ROW

#undef CHECK_TYPE
#undef CHECK_VALUE
