#include "voxel_internal.h"

bool ra_vpl_parse(ra_vpl *vpl, ra_view bytes, ra_error *error)
{
    ra_vpl result = {0};
    if (!vpl || !bytes.data) return ra_fail(error, RA_ARGUMENT, 0, "VPL requires output and input bytes");
    if (bytes.size < 784) return ra_fail(error, RA_FORMAT, 0, "truncated VPL header or palette");
    result.remap_start = ra_le32(bytes.data);
    result.remap_end = ra_le32(bytes.data + 4);
    result.section_count = ra_le32(bytes.data + 8);
    result.reserved = ra_le32(bytes.data + 12);
    if (result.remap_start > result.remap_end || result.remap_end > 255 || !result.section_count || result.section_count > 256 ||
        (size_t)result.section_count * 256 != bytes.size - 784) return ra_fail(error, RA_FORMAT, 0, "invalid VPL remap interval, section count or size");
    memcpy(result.palette, bytes.data + 16, 768);
    result.tables = (ra_view){bytes.data + 784, bytes.size - 784};
    *vpl = result;
    return true;
}

bool ra_vpl_lookup(const ra_vpl *vpl, size_t shade, uint8_t color, uint8_t *result, ra_error *error)
{
    if (!vpl || !vpl->tables.data || !result) return ra_fail(error, RA_ARGUMENT, 0, "VPL lookup requires an open table and output");
    if (shade >= vpl->section_count) return ra_fail(error, RA_RANGE, 0, "VPL shade is out of range");
    *result = vpl->tables.data[shade * 256 + color];
    return true;
}
