#include "voxel_internal.h"
#include <stdlib.h>

bool ra_hva_parse(ra_hva *hva, ra_view bytes, ra_error *error)
{
    ra_hva result = {0};
    size_t frames, sections, count, start, i, j;
    if (!hva || !bytes.data) return ra_fail(error, RA_ARGUMENT, 0, "HVA requires output and input bytes");
    if (bytes.size < 24) return ra_fail(error, RA_FORMAT, 0, "truncated HVA header");
    frames = ra_le32(bytes.data + 16);
    sections = ra_le32(bytes.data + 20);
    if (!frames || frames > 16384 || sections > 1024 || (sections && frames > SIZE_MAX / sections / 48) || frames * sections > 1048576)
        return ra_fail(error, RA_RANGE, 0, "HVA counts exceed supported limits");
    start = 24 + sections * 16;
    count = frames * sections * 12;
    if (start > bytes.size || count > (bytes.size - start) / 4 || count * 4 != bytes.size - start)
        return ra_fail(error, RA_FORMAT, 0, "HVA matrix count or file size mismatch");
    memcpy(result.name, bytes.data, 16);
    result.name[16] = 0;
    result.frame_count = frames;
    result.section_count = sections;
    result.sections = calloc(sections ? sections : 1, sizeof(*result.sections));
    result.matrices = malloc(count ? count * sizeof(*result.matrices) : 1);
    if (!result.sections || !result.matrices) {
        ra_fail(error, RA_MEMORY, 0, "HVA allocation failed");
        goto fail;
    }
    for (i = 0; i < sections; ++i) {
        if (!voxel_name(result.sections[i], bytes.data + 24 + i * 16)) goto malformed;
        for (j = 0; j < i; ++j) if (ra_equal(result.sections[i], result.sections[j])) goto malformed;
    }
    for (i = 0; i < count; ++i) {
        result.matrices[i] = voxel_float(bytes.data + start + i * 4);
        if (!voxel_number(result.matrices[i])) goto malformed;
    }
    *hva = result;
    return true;
malformed:
    ra_fail(error, RA_FORMAT, 0, "HVA contains invalid section names or nonfinite matrix values");
fail:
    ra_hva_close(&result);
    return false;
}

bool ra_hva_bind(const ra_vxl *vxl, const ra_hva *hva, size_t *mapping, size_t capacity, ra_error *error)
{
    size_t i, j;
    if (!vxl || !hva || !mapping || !vxl->sections || !hva->matrices || capacity < vxl->section_count)
        return ra_fail(error, RA_ARGUMENT, 0, "HVA binding requires valid objects and mapping capacity");
    if (vxl->section_count != hva->section_count) return ra_fail(error, RA_FORMAT, 0, "VXL/HVA section counts differ");
    for (i = 0; i < vxl->section_count; ++i) {
        for (j = 0; j < hva->section_count; ++j) if (ra_equal(vxl->sections[i].name, hva->sections[j])) break;
        if (j == hva->section_count) return ra_fail(error, RA_NOT_FOUND, 0, "HVA section missing: %s", vxl->sections[i].name);
    }
    for (i = 0; i < vxl->section_count; ++i) {
        for (j = 0; j < hva->section_count; ++j) if (ra_equal(vxl->sections[i].name, hva->sections[j])) break;
        mapping[i] = j;
    }
    return true;
}

void ra_hva_close(ra_hva *hva)
{
    if (!hva) return;
    free(hva->sections);
    free(hva->matrices);
    memset(hva, 0, sizeof(*hva));
}
