#include "internal.h"
#include "ra2/map.h"
#include <stdlib.h>
#include <string.h>

typedef struct
{
    ra_view in;
    uint8_t *out;
    size_t ip, op, limit;
} pack_cursor;

static bool literal(pack_cursor *c, size_t n)
{
    if (n > c->in.size - c->ip || n > c->limit - c->op) return false;
    memcpy(c->out + c->op, c->in.data + c->ip, n);
    c->ip += n;
    c->op += n;
    return true;
}

static bool repeat(pack_cursor *c, size_t distance, size_t n)
{
    size_t i;
    if (!distance || distance > c->op || n > c->limit - c->op) return false;
    for (i = 0; i < n; ++i) c->out[c->op + i] = c->out[c->op + i - distance];
    c->op += n;
    return true;
}

static bool length_code(pack_cursor *c, size_t *n, size_t mask)
{
    if (*n) return true;
    *n = mask;
    while (c->ip < c->in.size && !c->in.data[c->ip])
    {
        if (*n > c->limit || c->limit - *n < 255) return false;
        *n += 255;
        ++c->ip;
    }
    if (c->ip == c->in.size || *n > c->limit || c->in.data[c->ip] > c->limit - *n) return false;
    *n += c->in.data[c->ip++];
    return true;
}

/* 按 LZO1X v0 的指令类别实现有界状态机，不使用未对齐读写或外部库。 */
bool ra_lzo_decode(ra_view input, uint8_t *output, size_t size, ra_error *error)
{
    pack_cursor c = {input, output, 0, 0, size};
    unsigned state = 0;
    if ((!input.data && input.size) || (!output && size) || !input.size) return ra_fail(error, RA_ARGUMENT, 0, "invalid LZO buffers");
    if (input.data[0] > 17)
    {
        size_t n = input.data[c.ip++] - 17;
        if (!literal(&c, n)) goto bad;
        state = n < 4 ? (unsigned)n : 4;
    }
    while (c.ip < input.size)
    {
        unsigned token = input.data[c.ip++], tail;
        size_t n, distance;
        if (token < 16 && !state)
        {
            n = token;
            if (!length_code(&c, &n, 15) || n > SIZE_MAX - 3 || !literal(&c, n + 3)) goto bad;
            state = 4;
            continue;
        }
        if (token < 16)
        {
            if (c.ip == input.size) goto bad;
            distance = 1 + (token >> 2) + ((size_t)input.data[c.ip++] << 2) + (state == 4 ? 2048 : 0);
            n = state == 4 ? 3 : 2;
            tail = token & 3;
        }
        else if (token >= 64)
        {
            if (c.ip == input.size) goto bad;
            distance = 1 + ((token >> 2) & 7) + ((size_t)input.data[c.ip++] << 3);
            n = (token >> 5) + 1;
            tail = token & 3;
        }
        else
        {
            unsigned word;
            n = token & (token >= 32 ? 31u : 7u);
            if (!length_code(&c, &n, token >= 32 ? 31 : 7) || input.size - c.ip < 2) goto bad;
            word = ra_le16(input.data + c.ip);
            c.ip += 2;
            distance = word >> 2;
            tail = word & 3;
            if (token >= 32) ++distance;
            else
            {
                distance += (size_t)(token & 8) << 11;
                if (!distance)
                {
                    if (n == 1 && !tail && c.ip == input.size && c.op == size) return true;
                    goto bad;
                }
                distance += 16384;
            }
            n += 2;
        }
        if (!repeat(&c, distance, n) || !literal(&c, tail)) goto bad;
        state = tail;
    }
bad:
    return ra_fail(error, RA_FORMAT, 0, "invalid LZO stream at input %zu, output %zu/%zu", c.ip, c.op, size);
}

bool ra_lcw_decode(ra_view input, uint8_t *output, size_t size, ra_error *error)
{
    pack_cursor c = {input, output, 0, 0, size};
    bool relative = false;
    if ((!input.data && input.size) || (!output && size) || !input.size) return ra_fail(error, RA_ARGUMENT, 0, "invalid LCW buffers");
    if (!input.data[0])
    {
        relative = true;
        ++c.ip;
    }
    while (c.ip < input.size)
    {
        unsigned token = input.data[c.ip++];
        size_t n, source;
        if (!(token & 128))
        {
            if (c.ip == input.size) goto bad;
            n = (token >> 4) + 3;
            source = ((size_t)(token & 15) << 8) + input.data[c.ip++];
            if (!repeat(&c, source, n)) goto bad;
        }
        else if (token < 192)
        {
            n = token & 63;
            if (!n)
            {
                if (c.ip == input.size && c.op == size) return true;
                goto bad;
            }
            if (!literal(&c, n)) goto bad;
        }
        else if (token == 254)
        {
            if (input.size - c.ip < 3) goto bad;
            n = ra_le16(input.data + c.ip);
            if (!n || n > size - c.op) goto bad;
            memset(output + c.op, input.data[c.ip + 2], n);
            c.ip += 3;
            c.op += n;
        }
        else
        {
            n = (token & 63) + 3;
            if (token == 255)
            {
                if (input.size - c.ip < 2) goto bad;
                n = ra_le16(input.data + c.ip);
                c.ip += 2;
            }
            if (!n || input.size - c.ip < 2) goto bad;
            source = ra_le16(input.data + c.ip);
            c.ip += 2;
            if (!relative)
            {
                if (source >= c.op) goto bad;
                source = c.op - source;
            }
            if (!repeat(&c, source, n)) goto bad;
        }
    }
bad:
    return ra_fail(error, RA_FORMAT, 0, "invalid LCW stream at input %zu, output %zu/%zu", c.ip, c.op, size);
}

static int base64_digit(unsigned char c)
{
    if (c >= 'A' && c <= 'Z') return c - 'A';
    if (c >= 'a' && c <= 'z') return c - 'a' + 26;
    if (c >= '0' && c <= '9') return c - '0' + 52;
    return c == '+' ? 62 : c == '/' ? 63 : -1;
}

bool ra_map_pack(const ra_ini *ini, const char *section, bool lzo, uint8_t **output, size_t *size, ra_error *error)
{
    const ra_ini_entry **lines = NULL;
    uint8_t *binary = NULL, *decoded = NULL;
    size_t i, max = 0, chars = 0, used = 0, total = 0, pos;
    unsigned bits = 0, accumulator = 0, padding = 0;
    bool ok = false;
    if (!ini || !section || !output || !size) return ra_fail(error, RA_ARGUMENT, 0, "invalid pack arguments");
    *output = NULL;
    *size = 0;
    /* 数字键必须从一连续编号，重复键沿用 INI 的末次赋值语义。 */
    for (i = 0; i < ini->entry_count; ++i)
        if (ra_equal(ini->entries[i].section, section))
        {
            int64_t key;
            ra_ini_entry number = ini->entries[i];
            number.value = number.key;
            if (!ra_ini_integer(&number, &key, error) || key < 1 || key > 1000000) return ra_fail(error, RA_FORMAT, number.line, "invalid pack line key");
            if ((size_t)key > max) max = (size_t)key;
        }
    if (!max) return true;
    lines = calloc(max, sizeof(*lines));
    if (!lines) goto memory;
    for (i = 0; i < ini->entry_count; ++i)
        if (ra_equal(ini->entries[i].section, section)) lines[strtoul(ini->entries[i].key, NULL, 10) - 1] = &ini->entries[i];
    for (i = 0; i < max; ++i)
    {
        if (!lines[i])
        {
            ra_fail(error, RA_FORMAT, 0, "missing [%s] line %zu", section, i + 1);
            goto done;
        }
        if (strlen(lines[i]->value) > 32 * 1024 * 1024 - chars) goto range;
        chars += strlen(lines[i]->value);
    }
    binary = malloc(chars + 1);
    if (!binary) goto memory;
    for (i = 0; i < max; ++i)
    {
        const unsigned char *p = (const unsigned char *)lines[i]->value;
        for (; *p; ++p)
        {
            int digit = base64_digit(*p);
            if (*p == '=')
            {
                if (++padding > 2) goto invalid;
                continue;
            }
            if (digit < 0 || padding) goto invalid;
            accumulator = (accumulator << 6) | (unsigned)digit;
            bits += 6;
            if (bits >= 8)
            {
                bits -= 8;
                binary[used++] = (uint8_t)(accumulator >> bits);
            }
        }
    }
    if (chars % 4 || (padding == 1 && bits != 2) || (padding == 2 && bits != 4) || (!padding && bits) || (accumulator & ((1u << bits) - 1))) goto invalid;
    for (pos = 0; pos < used;)
    {
        size_t compressed, plain;
        if (used - pos < 4) goto invalid;
        compressed = ra_le16(binary + pos);
        plain = ra_le16(binary + pos + 2);
        pos += 4;
        if (!compressed || !plain || compressed > used - pos) goto invalid;
        if (plain > 16 * 1024 * 1024 - total) goto range;
        total += plain;
        pos += compressed;
    }
    decoded = malloc(total ? total : 1);
    if (!decoded) goto memory;
    total = 0;
    for (pos = 0; pos < used;)
    {
        size_t compressed = ra_le16(binary + pos), plain = ra_le16(binary + pos + 2);
        ra_view block = {binary + pos + 4, compressed};
        if (!(lzo ? ra_lzo_decode(block, decoded + total, plain, error) : ra_lcw_decode(block, decoded + total, plain, error))) goto done;
        total += plain;
        pos += compressed + 4;
    }
    *output = decoded;
    *size = total;
    decoded = NULL;
    ok = true;
    goto done;
memory:
    ra_fail(error, RA_MEMORY, 0, "map pack allocation failed");
    goto done;
range:
    ra_fail(error, RA_RANGE, 0, "map pack exceeds size limit");
    goto done;
invalid:
    ra_fail(error, RA_FORMAT, 0, "invalid base64/chunk framing in [%s]", section);
done:
    free(decoded);
    free(binary);
    free(lines);
    return ok;
}
