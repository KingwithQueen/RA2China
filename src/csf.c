#include "internal.h"
#include "ra2/assets.h"
#include <stdlib.h>
#include <string.h>

static uint64_t label_hash(const char *name)
{
    uint64_t hash = UINT64_C(14695981039346656037);
    while (*name) {
        unsigned c = (uint8_t)*name++;
        if (c >= 'A' && c <= 'Z') c += 'a' - 'A';
        hash = (hash ^ c) * UINT64_C(1099511628211);
    }
    return hash;
}

static bool read_u32(ra_view bytes, size_t *cursor, uint32_t *value, ra_error *error)
{
    if (bytes.size - *cursor < 4) return ra_fail(error, RA_FORMAT, 0, "CSF integer is truncated at byte %zu", *cursor);
    *value = ra_le32(bytes.data + *cursor);
    *cursor += 4;
    return true;
}

static bool read_text(ra_view bytes, size_t *cursor, ra_csf_value *value, ra_error *error)
{
    uint32_t units;
    size_t i, used = 0;
    char *text;
    if (!read_u32(bytes, cursor, &units, error)) return false;
    if (units > (bytes.size - *cursor) / 2 || units > (SIZE_MAX - 1) / 3) return ra_fail(error, RA_FORMAT, 0, "CSF UTF-16 text is truncated or too long");
    text = malloc((size_t)units * 3 + 1);
    if (!text) return ra_fail(error, RA_MEMORY, 0, "CSF text allocation failed");
    for (i = 0; i < units; ++i) {
        uint32_t c = ra_le16(bytes.data + *cursor + i * 2) ^ 0xffffu;
        if (c >= 0xd800 && c <= 0xdbff) {
            uint32_t low;
            if (++i == units) goto invalid;
            low = ra_le16(bytes.data + *cursor + i * 2) ^ 0xffffu;
            if (low < 0xdc00 || low > 0xdfff) goto invalid;
            c = 0x10000 + ((c - 0xd800) << 10) + low - 0xdc00;
        } else if (c >= 0xdc00 && c <= 0xdfff) goto invalid;
        if (c < 0x80) text[used++] = (char)c;
        else if (c < 0x800) {
            text[used++] = (char)(0xc0 | (c >> 6));
            text[used++] = (char)(0x80 | (c & 63));
        } else if (c < 0x10000) {
            text[used++] = (char)(0xe0 | (c >> 12));
            text[used++] = (char)(0x80 | ((c >> 6) & 63));
            text[used++] = (char)(0x80 | (c & 63));
        } else {
            text[used++] = (char)(0xf0 | (c >> 18));
            text[used++] = (char)(0x80 | ((c >> 12) & 63));
            text[used++] = (char)(0x80 | ((c >> 6) & 63));
            text[used++] = (char)(0x80 | (c & 63));
        }
    }
    text[used] = 0;
    value->text = text;
    value->length = used;
    *cursor += (size_t)units * 2;
    return true;
invalid:
    free(text);
    return ra_fail(error, RA_FORMAT, 0, "CSF contains an unpaired UTF-16 surrogate");
}

bool ra_csf_parse(ra_csf *csf, ra_view bytes, ra_error *error)
{
    ra_csf result = {0};
    size_t cursor = 24, i, used = 0, capacity = 1;
    uint32_t labels, values;
    if (!csf || !bytes.data) return ra_fail(error, RA_ARGUMENT, 0, "CSF requires an output and input bytes");
    if (bytes.size < 24 || memcmp(bytes.data, " FSC", 4)) return ra_fail(error, RA_FORMAT, 0, "invalid CSF header");
    result.version = ra_le32(bytes.data + 4);
    result.reserved = ra_le32(bytes.data + 16);
    result.language = ra_le32(bytes.data + 20);
    labels = ra_le32(bytes.data + 8);
    values = ra_le32(bytes.data + 12);
    if (result.version != 2 && result.version != 3) return ra_fail(error, RA_FORMAT, 0, "unsupported CSF version %u", result.version);
    if (labels > (bytes.size - 24) / 12 || values > (bytes.size - 24) / 8) return ra_fail(error, RA_FORMAT, 0, "CSF counts exceed the available bytes");
    result.label_count = labels;
    result.value_count = values;
    result.labels = calloc(labels ? labels : 1, sizeof(*result.labels));
    result.values = calloc(values ? values : 1, sizeof(*result.values));
    while (capacity < (size_t)labels * 2) {
        if (capacity > SIZE_MAX / 2) goto memory;
        capacity *= 2;
    }
    result.index_capacity = capacity;
    result.index = calloc(capacity, sizeof(*result.index));
    if (!result.labels || !result.values || !result.index) goto memory;
    for (i = 0; i < labels; ++i) {
        uint32_t tag, count, length, j;
        size_t slot;
        ra_csf_label *label = &result.labels[i];
        if (!read_u32(bytes, &cursor, &tag, error) || !read_u32(bytes, &cursor, &count, error) || !read_u32(bytes, &cursor, &length, error)) goto fail;
        if (tag != 0x4c424c20u || !length || length > bytes.size - cursor || count > values - used) goto malformed;
        /* 标签按 ASCII 标识符处理，拒绝内嵌零及依赖本地代码页的名称。 */
        for (j = 0; j < length; ++j) if (!bytes.data[cursor + j] || bytes.data[cursor + j] > 127) goto malformed;
        label->name = ra_copy((const char *)bytes.data + cursor, length);
        if (!label->name) goto memory;
        cursor += length;
        label->first_value = used;
        label->value_count = count;
        for (j = 0; j < count; ++j) {
            ra_csf_value *value = &result.values[used++];
            if (!read_u32(bytes, &cursor, &tag, error)) goto fail;
            if (tag != 0x53545220u && tag != 0x53545257u) goto malformed;
            value->has_extra = tag == 0x53545257u;
            if (!read_text(bytes, &cursor, value, error)) goto fail;
            if (value->has_extra) {
                if (!read_u32(bytes, &cursor, &length, error)) goto fail;
                if (length > bytes.size - cursor) goto malformed;
                value->extra.data = bytes.data + cursor;
                value->extra.size = length;
                cursor += length;
            }
        }
        slot = (size_t)label_hash(label->name) & (capacity - 1);
        while (result.index[slot] && !ra_equal(result.labels[result.index[slot] - 1].name, label->name)) slot = (slot + 1) & (capacity - 1);
        if (result.index[slot]) ++result.duplicate_count;
        result.index[slot] = i + 1;
    }
    if (used != values || cursor != bytes.size) goto malformed;
    *csf = result;
    return true;
memory:
    ra_fail(error, RA_MEMORY, 0, "CSF table allocation failed");
    goto fail;
malformed:
    ra_fail(error, RA_FORMAT, 0, "invalid CSF chunk, counts or trailing bytes at byte %zu", cursor);
fail:
    ra_csf_close(&result);
    return false;
}

const ra_csf_label *ra_csf_get(const ra_csf *csf, const char *name)
{
    size_t slot;
    if (!csf || !csf->index || !name) return NULL;
    slot = (size_t)label_hash(name) & (csf->index_capacity - 1);
    while (csf->index[slot]) {
        const ra_csf_label *label = &csf->labels[csf->index[slot] - 1];
        if (ra_equal(label->name, name)) return label;
        slot = (slot + 1) & (csf->index_capacity - 1);
    }
    return NULL;
}

void ra_csf_close(ra_csf *csf)
{
    size_t i;
    if (!csf) return;
    if (csf->labels) for (i = 0; i < csf->label_count; ++i) free(csf->labels[i].name);
    if (csf->values) for (i = 0; i < csf->value_count; ++i) free(csf->values[i].text);
    free(csf->labels);
    free(csf->values);
    free(csf->index);
    memset(csf, 0, sizeof(*csf));
}
