#include "internal.h"
#include "ra2/assets.h"

bool ra_palette_parse(ra_palette *palette, ra_view bytes, ra_error *error)
{
    ra_palette result;
    size_t i;
    if (!palette || !bytes.data) return ra_fail(error, RA_ARGUMENT, 0, "PAL requires an output and input bytes");
    if (bytes.size != 768) return ra_fail(error, RA_FORMAT, 0, "PAL must contain exactly 768 bytes");
    for (i = 0; i < 256; ++i) {
        unsigned r = bytes.data[i * 3], g = bytes.data[i * 3 + 1], b = bytes.data[i * 3 + 2];
        if (r > 63 || g > 63 || b > 63) return ra_fail(error, RA_FORMAT, 0, "PAL color %zu exceeds six-bit range", i);
        result.colors[i].r = (uint8_t)((r << 2) | (r >> 4));
        result.colors[i].g = (uint8_t)((g << 2) | (g >> 4));
        result.colors[i].b = (uint8_t)((b << 2) | (b >> 4));
    }
    *palette = result;
    return true;
}
