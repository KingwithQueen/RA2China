#include "internal.h"
#include "ra2/assets.h"
#include <stdlib.h>
#include <string.h>

/* 单帧画布上限为 64 Mi 像素，防止小文件声明极大图像后耗尽内存。 */
#define RA_SHP_MAX_PIXELS ((size_t)64 * 1024 * 1024)

static int offset_compare(const void *a, const void *b)
{
    uint32_t x = *(const uint32_t *)a, y = *(const uint32_t *)b;
    return (x > y) - (x < y);
}

static bool frame_read(const ra_shp *shp, size_t number, uint8_t *pixels, size_t *clipped, size_t *short_rows, ra_error *error)
{
    const ra_shp_frame *frame = &shp->frames[number];
    size_t cursor = frame->offset, row;
    if (!frame->offset || !frame->width || !frame->height) return true;
    if (!(frame->flags & 2u)) {
        size_t size = (size_t)frame->width * frame->height;
        if (size > frame->data_end - cursor) return ra_fail(error, RA_FORMAT, 0, "SHP frame %zu has truncated raw data", number);
        if (pixels) {
            for (row = 0; row < frame->height; ++row) {
                memcpy(pixels + ((size_t)frame->y + row) * shp->width + frame->x, shp->bytes.data + cursor, frame->width);
                cursor += frame->width;
            }
        }
        return true;
    }
    /* 仅检查低位压缩标志；原版部分帧的高位包含编码器遗留值。 */
    for (row = 0; row < frame->height; ++row) {
        size_t length, end, x = 0;
        if (frame->data_end - cursor < 2) return ra_fail(error, RA_FORMAT, 0, "SHP frame %zu row %zu lacks a length", number, row);
        length = ra_le16(shp->bytes.data + cursor);
        if (length < 2 || length > frame->data_end - cursor) return ra_fail(error, RA_FORMAT, 0, "SHP frame %zu row %zu has an invalid length", number, row);
        end = cursor + length;
        cursor += 2;
        while (cursor < end) {
            unsigned value = shp->bytes.data[cursor++];
            if (value) {
                if (x >= frame->width) return ra_fail(error, RA_FORMAT, 0, "SHP frame %zu row %zu exceeds its width", number, row);
                if (pixels) pixels[((size_t)frame->y + row) * shp->width + frame->x + x] = (uint8_t)value;
                ++x;
            } else {
                unsigned run;
                if (cursor == end) return ra_fail(error, RA_FORMAT, 0, "SHP frame %zu row %zu has an incomplete zero run", number, row);
                run = shp->bytes.data[cursor++];
                if (!run) return ra_fail(error, RA_FORMAT, 0, "SHP frame %zu row %zu has an empty zero run", number, row);
                if (run > frame->width - x) {
                    if (cursor != end) return ra_fail(error, RA_FORMAT, 0, "SHP frame %zu row %zu has an overflowing interior zero run", number, row);
                    /* 原版行末游程常多算一个透明像素，仅在行尾安全截断并计数。 */
                    if (clipped) ++*clipped;
                    run = (unsigned)(frame->width - x);
                }
                x += run;
            }
        }
        /* 省略的透明尾部由画布清零补齐，兼容次数单独保留。 */
        if (x < frame->width && short_rows) ++*short_rows;
    }
    return true;
}

bool ra_shp_open(ra_shp *shp, ra_view bytes, ra_error *error)
{
    ra_shp result = {0};
    uint32_t *offsets = NULL;
    size_t i, count = 0, table_end;
    if (!shp || !bytes.data) return ra_fail(error, RA_ARGUMENT, 0, "SHP requires an output and input bytes");
    if (bytes.size < 8 || ra_le16(bytes.data)) return ra_fail(error, RA_FORMAT, 0, "not a TS/RA2 SHP header");
    result.bytes = bytes;
    result.width = ra_le16(bytes.data + 2);
    result.height = ra_le16(bytes.data + 4);
    result.count = ra_le16(bytes.data + 6);
    table_end = 8 + (size_t)result.count * 24;
    if (!result.count || table_end > bytes.size) return ra_fail(error, RA_FORMAT, 0, "invalid SHP dimensions or frame table");
    if ((size_t)result.width * result.height > RA_SHP_MAX_PIXELS) return ra_fail(error, RA_RANGE, 0, "SHP canvas exceeds the pixel limit");
    result.frames = calloc(result.count, sizeof(*result.frames));
    offsets = malloc((size_t)result.count * sizeof(*offsets));
    if (!result.frames || !offsets) {
        ra_fail(error, RA_MEMORY, 0, "SHP frame table allocation failed");
        goto fail;
    }
    for (i = 0; i < result.count; ++i) {
        const uint8_t *p = bytes.data + 8 + i * 24;
        ra_shp_frame *f = &result.frames[i];
        f->x = ra_le16(p);
        f->y = ra_le16(p + 2);
        f->width = ra_le16(p + 4);
        f->height = ra_le16(p + 6);
        f->flags = ra_le32(p + 8);
        f->color = ra_le32(p + 12);
        f->reserved = ra_le32(p + 16);
        f->offset = ra_le32(p + 20);
        if (!f->offset) continue;
        if (f->offset < table_end || f->offset > bytes.size) {
            ra_fail(error, RA_FORMAT, 0, "SHP frame %zu points outside image data", i);
            goto fail;
        }
        if ((size_t)f->x + f->width > result.width || (size_t)f->y + f->height > result.height) {
            ra_fail(error, RA_FORMAT, 0, "SHP frame %zu extends outside the canvas", i);
            goto fail;
        }
        offsets[count++] = f->offset;
    }
    qsort(offsets, count, sizeof(*offsets), offset_compare);
    for (i = 0; i < result.count; ++i) {
        ra_shp_frame *f = &result.frames[i];
        size_t lo = 0, hi = count;
        /* 允许多帧共用相同数据，但不得读入下一个不同偏移的帧。 */
        while (lo < hi) {
            size_t mid = lo + (hi - lo) / 2;
            if (offsets[mid] <= f->offset) lo = mid + 1;
            else hi = mid;
        }
        f->data_end = lo < count ? offsets[lo] : bytes.size;
        if (!frame_read(&result, i, NULL, &result.clipped_zero_runs, &result.short_rows, error)) goto fail;
    }
    free(offsets);
    *shp = result;
    return true;
fail:
    free(offsets);
    ra_shp_close(&result);
    return false;
}

bool ra_shp_decode(const ra_shp *shp, size_t frame, uint8_t *pixels, size_t capacity, ra_error *error)
{
    size_t size;
    if (!shp || !shp->frames || !pixels) return ra_fail(error, RA_ARGUMENT, 0, "SHP decode requires an open image and output buffer");
    size = (size_t)shp->width * shp->height;
    if (frame >= shp->count || capacity < size) return ra_fail(error, RA_RANGE, 0, "SHP frame or output capacity is out of range");
    memset(pixels, 0, size);
    return frame_read(shp, frame, pixels, NULL, NULL, error);
}

void ra_shp_close(ra_shp *shp)
{
    if (!shp) return;
    free(shp->frames);
    memset(shp, 0, sizeof(*shp));
}
