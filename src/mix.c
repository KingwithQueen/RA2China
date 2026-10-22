#include "internal.h"
#include <stdlib.h>
#include <string.h>

static uint8_t upper(uint8_t c) { return c >= 'a' && c <= 'z' ? (uint8_t)(c-32) : c; }
static uint32_t crc_byte(uint32_t crc, uint8_t b)
{
    unsigned i;
    crc ^= b;
    for (i = 0; i < 8; ++i) crc = (crc >> 1) ^ ((crc & 1) ? 0xedb88320u : 0);
    return crc;
}
uint32_t ra_mix_id(const char *name, ra_hash_kind kind)
{
    size_t i, length = strlen(name), remainder = length % 4;
    uint32_t result = kind == RA_HASH_CRC32 ? 0xffffffffu : 0;
    if (kind == RA_HASH_CLASSIC) {
        for (i = 0; i < length; i += 4) {
            uint32_t word = 0;
            unsigned j;
            for (j = 0; j < 4 && i+j < length; ++j) word |= (uint32_t)upper((uint8_t)name[i+j]) << (8*j);
            result = (result << 1 | result >> 31) + word;
        }
        return result;
    }
    for (i = 0; i < length; ++i) result = crc_byte(result, upper((uint8_t)name[i]));
    if (remainder) {
        result = crc_byte(result, (uint8_t)remainder);
        for (i = 0; i < 3-remainder; ++i) result = crc_byte(result, upper((uint8_t)name[length-remainder]));
    }
    return result ^ 0xffffffffu;
}

static int entry_compare(const void *a, const void *b)
{
    uint32_t x = ((const ra_mix_entry *)a)->id, y = ((const ra_mix_entry *)b)->id;
    return x > y ? 1 : x < y ? -1 : 0;
}

bool ra_mix_open(ra_mix *mix, ra_view bytes, ra_hash_kind kind, ra_error *error)
{
    ra_mix out = {0};
    size_t header_offset = 0, header_size, i;
    const uint8_t *header;
    uint8_t *decrypted = NULL;
    if (!mix || (!bytes.data && bytes.size) || (kind != RA_HASH_CRC32 && kind != RA_HASH_CLASSIC))
        return ra_fail(error, RA_ARGUMENT, 0, "invalid MIX arguments");
    if (bytes.size < 6) return ra_fail(error, RA_FORMAT, 0, "truncated MIX header");
    out.bytes = bytes; out.hash_kind = kind;
    if (ra_le16(bytes.data) == 0) {
        out.flags = ra_le32(bytes.data);
        if (out.flags & ~0x00030000u) return ra_fail(error, RA_FORMAT, 0, "unsupported MIX flags: %08x", out.flags);
        header_offset = 4;
    }
    if (out.flags & 0x20000) {
        uint8_t key[56], first[8];
        ra_blowfish cipher;
        if (bytes.size < 92) return ra_fail(error, RA_FORMAT, 0, "truncated encrypted MIX header");
        ra_mix_key(bytes.data + 4, key);
        ra_blowfish_init(&cipher, key, sizeof(key));
        memcpy(first, bytes.data + 84, 8); ra_blowfish_decrypt(&cipher, first);
        out.count = ra_le16(first);
        header_size = (6 + 12*out.count + 7) & ~(size_t)7;
        if (header_size > bytes.size-84) return ra_fail(error, RA_FORMAT, 0, "encrypted MIX index exceeds input");
        decrypted = malloc(header_size);
        if (!decrypted) return ra_fail(error, RA_MEMORY, 0, "MIX header allocation failed");
        memcpy(decrypted, bytes.data + 84, header_size);
        for (i = 0; i < header_size; i += 8) ra_blowfish_decrypt(&cipher, decrypted+i);
        header = decrypted; out.data_offset = 84+header_size;
    } else {
        if (bytes.size-header_offset < 6) return ra_fail(error, RA_FORMAT, 0, "truncated MIX header");
        header = bytes.data + header_offset;
        out.count = ra_le16(header);
        header_size = 6+12*out.count;
        if (header_size > bytes.size-header_offset) return ra_fail(error, RA_FORMAT, 0, "MIX index exceeds input");
        out.data_offset = header_offset+header_size;
    }
    out.data_size = ra_le32(header+2);
    if (out.data_size > bytes.size-out.data_offset) {
        free(decrypted); return ra_fail(error, RA_FORMAT, 0, "MIX body exceeds input");
    }
    if (out.count) {
        out.entries = malloc(out.count * sizeof(*out.entries));
        if (!out.entries) { free(decrypted); return ra_fail(error, RA_MEMORY, 0, "MIX index allocation failed"); }
    }
    for (i = 0; i < out.count; ++i) {
        const uint8_t *p = header + 6+12*i;
        ra_mix_entry *entry = out.entries+i;
        entry->id = ra_le32(p); entry->offset = ra_le32(p+4); entry->size = ra_le32(p+8);
        if (entry->offset > out.data_size || entry->size > out.data_size-entry->offset) {
            free(decrypted); ra_mix_close(&out);
            return ra_fail(error, RA_FORMAT, 0, "MIX entry %zu extends beyond declared body", i);
        }
    }
    free(decrypted);
    if (out.count > 1) qsort(out.entries, out.count, sizeof(*out.entries), entry_compare);
    for (i = 1; i < out.count; ++i) if (out.entries[i-1].id == out.entries[i].id) {
        ra_mix_close(&out); return ra_fail(error, RA_FORMAT, 0, "duplicate MIX entry ID");
    }
    if (out.flags & 0x10000) {
        uint8_t digest[20];
        size_t end = out.data_offset+out.data_size;
        ra_view body = { bytes.data+out.data_offset, out.data_size };
        if (bytes.size-end < 20) { ra_mix_close(&out); return ra_fail(error, RA_FORMAT, 0, "missing MIX checksum"); }
        ra_sha1(body, digest);
        if (memcmp(digest, bytes.data+end, 20)) {
            ra_mix_close(&out); return ra_fail(error, RA_FORMAT, 0, "MIX SHA-1 body checksum mismatch");
        }
        out.checksum_verified = true;
    }
    *mix = out;
    return true;
}

void ra_mix_close(ra_mix *mix)
{
    if (!mix) return;
    free(mix->entries); memset(mix, 0, sizeof(*mix));
}

bool ra_mix_get_id(const ra_mix *mix, uint32_t id, ra_view *result, ra_error *error)
{
    size_t lo = 0, hi;
    if (!mix || !result) return ra_fail(error, RA_ARGUMENT, 0, "invalid MIX lookup");
    hi = mix->count;
    while (lo < hi) {
        size_t mid = lo+(hi-lo)/2;
        const ra_mix_entry *entry = mix->entries+mid;
        if (entry->id < id) lo = mid+1;
        else if (entry->id > id) hi = mid;
        else {
            result->data = mix->bytes.data+mix->data_offset+entry->offset;
            result->size = entry->size;
            return true;
        }
    }
    return ra_fail(error, RA_NOT_FOUND, 0, "MIX ID %08x not found", id);
}
bool ra_mix_get(const ra_mix *mix, const char *name, ra_view *result, ra_error *error)
{
    if (!mix || !name) return ra_fail(error, RA_ARGUMENT, 0, "invalid MIX filename");
    return ra_mix_get_id(mix, ra_mix_id(name, mix->hash_kind), result, error);
}
