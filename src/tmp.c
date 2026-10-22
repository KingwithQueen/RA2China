#include "internal.h"
#include "ra2/map.h"
#include <stdlib.h>
#include <string.h>

static bool slice(ra_view in, size_t offset, size_t size, ra_view *out)
{
    if (offset > in.size || size > in.size - offset) return false;
    *out = (ra_view){in.data + offset, size};
    return true;
}

bool ra_tmp_open(ra_tmp *tmp, ra_view input, ra_error *error)
{
    ra_tmp result = {0};
    size_t i, diamond, table;
    if (!tmp || !input.data || input.size < 16) return ra_fail(error, RA_FORMAT, 0, "truncated TMP header");
    result.columns = ra_le32(input.data);
    result.rows = ra_le32(input.data + 4);
    result.width = ra_le32(input.data + 8);
    result.height = ra_le32(input.data + 12);
    if (!result.columns || !result.rows || result.columns > 64 || result.rows > 64 || (result.width != 60 && result.width != 48) ||
        result.height != result.width / 2)
        return ra_fail(error, RA_RANGE, 0, "unsupported TMP dimensions");
    result.count = (size_t)result.columns * result.rows;
    table = 16 + result.count * 4;
    if (table > input.size) return ra_fail(error, RA_FORMAT, 0, "truncated TMP offset table");
    result.tiles = calloc(result.count, sizeof(*result.tiles));
    if (!result.tiles) return ra_fail(error, RA_MEMORY, 0, "TMP tile allocation failed");
    diamond = (size_t)result.width * result.height / 2;
    for (i = 0; i < result.count; ++i)
    {
        size_t offset = ra_le32(input.data + 16 + i * 4), extra_size;
        const uint8_t *p;
        uint32_t extra_offset, depth_offset, extra_depth_offset;
        ra_tmp_tile *tile = &result.tiles[i];
        if (!offset) continue;
        if (offset < table || offset > input.size || input.size - offset < 52) goto invalid;
        p = input.data + offset;
        tile->present = true;
        tile->x = (int32_t)ra_le32(p);
        tile->y = (int32_t)ra_le32(p + 4);
        extra_offset = ra_le32(p + 8);
        depth_offset = ra_le32(p + 12);
        extra_depth_offset = ra_le32(p + 16);
        tile->extra_x = (int32_t)ra_le32(p + 20);
        tile->extra_y = (int32_t)ra_le32(p + 24);
        tile->extra_width = (int32_t)ra_le32(p + 28);
        tile->extra_height = (int32_t)ra_le32(p + 32);
        tile->flags = ra_le32(p + 36);
        tile->height = p[40];
        tile->terrain = p[41];
        tile->ramp = p[42];
        tile->radar_left = (ra_rgb){p[43], p[44], p[45]};
        tile->radar_right = (ra_rgb){p[46], p[47], p[48]};
        if (tile->x < -4096 || tile->x > 4096 || tile->y < -4096 || tile->y > 4096 || !slice(input, offset + 52, diamond, &tile->pixels)) goto invalid;
        if ((tile->flags & 2) && (depth_offset < 52 + diamond || !slice(input, offset + depth_offset, diamond, &tile->depth))) goto invalid;
        if (tile->flags & 1)
        {
            if (tile->extra_width < 1 || tile->extra_height < 1 || tile->extra_width > 4096 || tile->extra_height > 4096 || tile->extra_x < -8192 ||
                tile->extra_x > 8192 || tile->extra_y < -8192 || tile->extra_y > 8192)
                goto invalid;
            extra_size = (size_t)tile->extra_width * tile->extra_height;
            if (extra_offset < 52 + diamond || !slice(input, offset + extra_offset, extra_size, &tile->extra)) goto invalid;
            if ((tile->flags & 2) && (extra_depth_offset < 52 + diamond || !slice(input, offset + extra_depth_offset, extra_size, &tile->extra_depth)))
                goto invalid;
        }
    }
    *tmp = result;
    return true;
invalid:
    ra_tmp_close(&result);
    return ra_fail(error, RA_FORMAT, 0, "invalid TMP tile %zu offset, dimensions or pixel extent", i);
}

void ra_tmp_close(ra_tmp *tmp)
{
    if (!tmp) return;
    free(tmp->tiles);
    memset(tmp, 0, sizeof(*tmp));
}
