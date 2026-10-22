#include "voxel_internal.h"
#include <stdlib.h>

#define RA_VOXEL_LIMIT ((size_t)16 * 1024 * 1024)

static bool read_spans(ra_vxl_section *section, ra_view body, const uint8_t *footer, bool decode, ra_error *error)
{
    size_t starts = ra_le32(footer), ends = ra_le32(footer + 4), data = ra_le32(footer + 8);
    size_t columns = (size_t)section->size[0] * section->size[1], column, used = 0;
    if (starts > body.size || ends > body.size || data > body.size || columns > (body.size - starts) / 4 || columns > (body.size - ends) / 4)
        return ra_fail(error, RA_FORMAT, 0, "VXL section %s has invalid span tables", section->name);
    for (column = 0; column < columns; ++column) {
        uint32_t start = ra_le32(body.data + starts + column * 4), end = ra_le32(body.data + ends + column * 4);
        size_t cursor, limit, z = 0;
        if (start == UINT32_MAX) {
            if (end != UINT32_MAX) return ra_fail(error, RA_FORMAT, 0, "VXL empty span has a nonempty end");
            continue;
        }
        if (start > end || end >= body.size - data) return ra_fail(error, RA_FORMAT, 0, "VXL span points outside body data");
        cursor = data + start;
        limit = data + (size_t)end + 1;
        while (cursor < limit && z < section->size[2]) {
            unsigned skip, run, j;
            if (limit - cursor < 3) return ra_fail(error, RA_FORMAT, 0, "VXL span run is truncated");
            skip = body.data[cursor++];
            run = body.data[cursor++];
            if ((!skip && !run) || skip > section->size[2] - z) return ra_fail(error, RA_FORMAT, 0, "VXL span does not advance or skips beyond Z");
            z += skip;
            if (run > section->size[2] - z || (size_t)run * 2 + 1 > limit - cursor) return ra_fail(error, RA_FORMAT, 0, "VXL span exceeds Z or available bytes");
            for (j = 0; j < run; ++j) {
                uint8_t color = body.data[cursor++], normal = body.data[cursor++];
                /* 原版存在 244/255 等未定义方向索引，保留原值并报告，禁止拿它直接访问方向表。 */
                if (!decode && normal >= (section->normal_type == 2 ? 36 : 244)) ++section->unmapped_normals;
                if (decode) {
                    ra_voxel *voxel = &section->voxels[used];
                    voxel->x = (uint8_t)(column % section->size[0]);
                    voxel->y = (uint8_t)(column / section->size[0]);
                    voxel->z = (uint8_t)z;
                    voxel->color = color;
                    voxel->normal = normal;
                }
                ++used;
                ++z;
            }
            if (body.data[cursor++] != run) return ra_fail(error, RA_FORMAT, 0, "VXL span duplicate run count does not match");
        }
        if (cursor != limit || z != section->size[2]) return ra_fail(error, RA_FORMAT, 0, "VXL span does not match its end or Z height");
    }
    section->voxel_count = used;
    return true;
}

bool ra_vxl_parse(ra_vxl *vxl, ra_view bytes, ra_error *error)
{
    ra_vxl result = {0};
    ra_view body;
    size_t sections, body_size, body_start, footer_start, i, j;
    if (!vxl || !bytes.data) return ra_fail(error, RA_ARGUMENT, 0, "VXL requires output and input bytes");
    if (bytes.size < 802 || memcmp(bytes.data, "Voxel Animation\0", 16) || ra_le32(bytes.data + 16) != 1)
        return ra_fail(error, RA_FORMAT, 0, "invalid VXL signature or version");
    sections = ra_le32(bytes.data + 20);
    body_size = ra_le32(bytes.data + 28);
    if (!sections || sections > 1024 || sections != ra_le32(bytes.data + 24)) return ra_fail(error, RA_FORMAT, 0, "invalid VXL section counts");
    body_start = 802 + sections * 28;
    if (body_start > bytes.size || body_size > bytes.size - body_start || sections * 92 != bytes.size - body_start - body_size)
        return ra_fail(error, RA_FORMAT, 0, "VXL body or footer size does not match file");
    result.remap_start = bytes.data[32];
    result.remap_end = bytes.data[33];
    if (result.remap_start > result.remap_end) return ra_fail(error, RA_FORMAT, 0, "invalid VXL remap interval");
    memcpy(result.palette, bytes.data + 34, 768);
    result.section_count = sections;
    result.sections = calloc(sections, sizeof(*result.sections));
    if (!result.sections) return ra_fail(error, RA_MEMORY, 0, "VXL section allocation failed");
    body = (ra_view){bytes.data + body_start, body_size};
    footer_start = body_start + body_size;
    for (i = 0; i < sections; ++i) {
        ra_vxl_section *section = &result.sections[i];
        const uint8_t *header = bytes.data + 802 + i * 28, *footer = bytes.data + footer_start + i * 92;
        if (!voxel_name(section->name, header)) goto malformed;
        for (j = 0; j < i; ++j) if (ra_equal(section->name, result.sections[j].name)) goto malformed;
        section->id = ra_le32(header + 16);
        section->header_one = ra_le32(header + 20);
        section->header_zero = ra_le32(header + 24);
        section->scale = voxel_float(footer + 12);
        if (!voxel_number(section->scale) || section->scale < 0) goto malformed;
        for (j = 0; j < 12; ++j) {
            section->transform[j] = voxel_float(footer + 16 + j * 4);
            if (!voxel_number(section->transform[j])) goto malformed;
        }
        for (j = 0; j < 6; ++j) {
            section->bounds[j] = voxel_float(footer + 64 + j * 4);
            if (!voxel_number(section->bounds[j])) goto malformed;
        }
        memcpy(section->size, footer + 88, 3);
        section->normal_type = footer[91];
        for (j = 0; j < 3; ++j) if (!section->size[j] || section->bounds[j] >= section->bounds[j + 3]) goto malformed;
        if (section->normal_type != 2 && section->normal_type != 4) goto malformed;
        if (!read_spans(section, body, footer, false, error)) goto fail;
        if (section->voxel_count > RA_VOXEL_LIMIT - result.voxel_count) {
            ra_fail(error, RA_RANGE, 0, "VXL exceeds decoded voxel limit");
            goto fail;
        }
        result.voxel_count += section->voxel_count;
        section->voxels = calloc(section->voxel_count ? section->voxel_count : 1, sizeof(*section->voxels));
        if (!section->voxels) {
            ra_fail(error, RA_MEMORY, 0, "VXL voxel allocation failed");
            goto fail;
        }
        if (!read_spans(section, body, footer, true, error)) goto fail;
    }
    *vxl = result;
    return true;
malformed:
    ra_fail(error, RA_FORMAT, 0, "VXL section %zu has invalid names, dimensions, bounds or numeric fields", i);
fail:
    ra_vxl_close(&result);
    return false;
}

void ra_vxl_close(ra_vxl *vxl)
{
    size_t i;
    if (!vxl) return;
    for (i = 0; i < vxl->section_count; ++i) free(vxl->sections[i].voxels);
    free(vxl->sections);
    memset(vxl, 0, sizeof(*vxl));
}
