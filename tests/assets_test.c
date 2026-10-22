#define _CRT_SECURE_NO_WARNINGS
#include "internal.h"
#include "ra2/assets.h"
#include <stdlib.h>
#include <string.h>
#include "entry.h"

static unsigned checks, failures;
#define CHECK(expr)                                                                                                                                            \
    do                                                                                                                                                         \
    {                                                                                                                                                          \
        ++checks;                                                                                                                                              \
        if (!(expr))                                                                                                                                           \
        {                                                                                                                                                      \
            ++failures;                                                                                                                                        \
            fprintf(stderr, "FAIL %s:%d: %s\n", __FILE__, __LINE__, #expr);                                                                                    \
            return;                                                                                                                                            \
        }                                                                                                                                                      \
    } while (0)

static void put16(uint8_t *p, unsigned value)
{
    p[0] = (uint8_t)value;
    p[1] = (uint8_t)(value >> 8);
}

static void put32(uint8_t *p, uint32_t value)
{
    size_t i;
    for (i = 0; i < 4; ++i) p[i] = (uint8_t)(value >> (i * 8));
}

static void palette_tests(void)
{
    uint8_t data[769] = {0};
    ra_palette palette;
    ra_error error = {0};
    ra_view view = {data, 768};
    data[0] = 63;
    data[1] = 16;
    data[2] = 32;
    CHECK(ra_palette_parse(&palette, view, &error));
    CHECK(palette.colors[0].r == 255 && palette.colors[0].g == 65 && palette.colors[0].b == 130);
    view.size = 767;
    CHECK(!ra_palette_parse(&palette, view, &error));
    view.size = 769;
    CHECK(!ra_palette_parse(&palette, view, &error));
    view.size = 768;
    data[767] = 64;
    CHECK(!ra_palette_parse(&palette, view, &error));
    CHECK(!ra_palette_parse(NULL, view, &error));
}

static void shp_tests(void)
{
    uint8_t data[160] = {0}, pixels[24], expected[24] = {0};
    ra_view view = {data, 116};
    ra_shp shp = {0};
    ra_error error = {0};
    size_t i;
    put16(data + 2, 6);
    put16(data + 4, 4);
    put16(data + 6, 4);
    /* 第一帧为带偏移的原始像素；第二帧为零游程；第三帧共享第二帧数据。 */
    for (i = 0; i < 3; ++i)
    {
        uint8_t *f = data + 8 + i * 24;
        put16(f, 1);
        put16(f + 2, 1);
        put16(f + 4, 4);
        put16(f + 6, 1);
        put32(f + 8, i ? 0xcccc0003u : 1u);
        put32(f + 20, i ? 108 : 104);
    }
    data[104] = 5;
    data[105] = 6;
    data[106] = 0;
    data[107] = 7;
    put16(data + 108, 7);
    data[110] = 8;
    data[111] = 0;
    data[112] = 2;
    data[113] = 9;
    data[114] = 0; /* 先使用不完整游程验证失败路径。 */
    CHECK(!ra_shp_open(&shp, view, &error));
    put16(data + 108, 6);
    CHECK(ra_shp_open(&shp, view, &error));
    CHECK(shp.count == 4 && shp.frames[1].flags == 0xcccc0003u);
    expected[7] = 5;
    expected[8] = 6;
    expected[10] = 7;
    CHECK(ra_shp_decode(&shp, 0, pixels, sizeof(pixels), &error));
    CHECK(!memcmp(pixels, expected, sizeof(pixels)));
    CHECK(ra_shp_decode(&shp, 1, pixels, sizeof(pixels), &error));
    CHECK(pixels[7] == 8 && pixels[8] == 0 && pixels[9] == 0 && pixels[10] == 9);
    CHECK(ra_shp_decode(&shp, 2, pixels, sizeof(pixels), &error));
    CHECK(pixels[7] == 8);
    CHECK(ra_shp_decode(&shp, 3, pixels, sizeof(pixels), &error));
    for (i = 0; i < sizeof(pixels); ++i) CHECK(!pixels[i]);
    CHECK(!ra_shp_decode(&shp, 4, pixels, sizeof(pixels), &error));
    CHECK(!ra_shp_decode(&shp, 0, pixels, sizeof(pixels) - 1, &error));
    ra_shp_close(&shp);
    data[112] = 0;
    CHECK(!ra_shp_open(&shp, view, &error));
    data[112] = 5;
    CHECK(!ra_shp_open(&shp, view, &error));
    data[112] = 2;
    put32(data + 28, 103);
    CHECK(!ra_shp_open(&shp, view, &error));
    put32(data + 28, 107);
    CHECK(!ra_shp_open(&shp, view, &error));
    put32(data + 28, 104);
    put16(data + 8, 4);
    CHECK(!ra_shp_open(&shp, view, &error));
    put16(data + 8, 1);
    view.size = 109;
    CHECK(!ra_shp_open(&shp, view, &error));
    view.size = 7;
    CHECK(!ra_shp_open(&shp, view, &error));
    for (i = 8; i < 114; ++i)
    {
        view.size = i;
        CHECK(!ra_shp_open(&shp, view, &error));
    }
    view.size = 116;
    put16(data + 2, 65535);
    put16(data + 4, 65535);
    CHECK(!ra_shp_open(&shp, view, &error) && error.code == RA_RANGE);
    /* null.shp 采用零尺寸画布和无数据帧，不能当成损坏文件。 */
    memset(data, 0, sizeof(data));
    put16(data + 6, 2);
    view.size = 56;
    CHECK(ra_shp_open(&shp, view, &error));
    CHECK(ra_shp_decode(&shp, 0, pixels, 0, &error));
    ra_shp_close(&shp);
    put16(data + 2, 4);
    put16(data + 4, 1);
    put16(data + 6, 1);
    put16(data + 12, 4);
    put16(data + 14, 1);
    put32(data + 16, 2);
    put32(data + 28, 32);
    put16(data + 32, 5);
    data[34] = 7;
    data[35] = 0;
    data[36] = 4;
    view.size = 37;
    CHECK(ra_shp_open(&shp, view, &error));
    CHECK(shp.clipped_zero_runs == 1 && shp.short_rows == 0);
    CHECK(ra_shp_decode(&shp, 0, pixels, sizeof(pixels), &error));
    CHECK(pixels[0] == 7 && !pixels[1] && !pixels[3]);
    ra_shp_close(&shp);
}

static size_t add_label(uint8_t *data, size_t at, const char *name, unsigned count)
{
    size_t n = strlen(name);
    memcpy(data + at, " LBL", 4);
    put32(data + at + 4, count);
    put32(data + at + 8, (uint32_t)n);
    memcpy(data + at + 12, name, n);
    return at + 12 + n;
}

static size_t add_value(uint8_t *data, size_t at, const uint16_t *text, size_t count, bool extra)
{
    size_t i;
    memcpy(data + at, extra ? "WRTS" : " RTS", 4);
    put32(data + at + 4, (uint32_t)count);
    at += 8;
    for (i = 0; i < count; ++i) put16(data + at + i * 2, text[i] ^ 0xffffu);
    at += count * 2;
    if (extra)
    {
        put32(data + at, 3);
        memcpy(data + at + 4, "a\0b", 3);
        at += 7;
    }
    return at;
}

static void csf_tests(void)
{
    uint8_t data[256] = {0};
    uint16_t text[] = {0x4e2d, 0x56fd, 0xd83d, 0xde80}, zero[] = {'a', 0, 'b'};
    size_t size = 24, first_text, i;
    ra_csf csf = {0};
    ra_error error = {0};
    ra_view view;
    const ra_csf_label *label;
    memcpy(data, " FSC", 4);
    put32(data + 4, 3);
    put32(data + 8, 3);
    put32(data + 12, 3);
    put32(data + 20, 9);
    size = add_label(data, size, "NAME:CN", 2);
    first_text = size + 8;
    size = add_value(data, size, text, 4, true);
    size = add_value(data, size, zero, 3, false);
    size = add_label(data, size, "Empty", 0);
    size = add_label(data, size, "name:cn", 1);
    size = add_value(data, size, text, 2, false);
    view.data = data;
    view.size = size;
    CHECK(ra_csf_parse(&csf, view, &error));
    CHECK(csf.label_count == 3 && csf.value_count == 3 && csf.duplicate_count == 1 && csf.language == 9);
    CHECK(!strcmp(csf.values[0].text, "中国🚀"));
    CHECK(csf.values[0].length == 10 && csf.values[0].has_extra);
    CHECK(csf.values[0].extra.size == 3 && !memcmp(csf.values[0].extra.data, "a\0b", 3));
    CHECK(csf.values[1].length == 3 && !memcmp(csf.values[1].text, "a\0b", 3));
    label = ra_csf_get(&csf, "Name:Cn");
    CHECK(label == &csf.labels[2] && !strcmp(csf.values[label->first_value].text, "中国"));
    CHECK(ra_csf_get(&csf, "EMPTY")->value_count == 0);
    CHECK(!ra_csf_get(&csf, "missing"));
    ra_csf_close(&csf);
    /* 每个截断位置都应失败，覆盖逐步分配后的清理路径。 */
    for (i = 0; i < size; ++i)
    {
        view.size = i;
        CHECK(!ra_csf_parse(&csf, view, &error));
    }
    view.size = size;
    put16(data + first_text, 0xd800 ^ 0xffffu);
    CHECK(!ra_csf_parse(&csf, view, &error));
    put16(data + first_text, 0x4e2d ^ 0xffffu);
    put32(data + 12, 4);
    CHECK(!ra_csf_parse(&csf, view, &error));
    put32(data + 12, 3);
    data[24] = 'X';
    CHECK(!ra_csf_parse(&csf, view, &error));
    data[24] = ' ';
    put32(data + 4, 2);
    CHECK(ra_csf_parse(&csf, view, &error));
    ra_csf_close(&csf);
    put32(data + 4, 4);
    CHECK(!ra_csf_parse(&csf, view, &error));
}

static int app_main(int argc, char **argv)
{
    (void)argc;
    (void)argv;
    palette_tests();
    shp_tests();
    csf_tests();
    printf("{\"checks\":%u,\"failures\":%u}\n", checks, failures);
    return failures ? 1 : 0;
}
