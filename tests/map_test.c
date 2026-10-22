#define _CRT_SECURE_NO_WARNINGS
#include "internal.h"
#include "map_scene.h"
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
static void put16(uint8_t *p, unsigned n)
{
    p[0] = (uint8_t)n;
    p[1] = (uint8_t)(n >> 8);
}
static void put32(uint8_t *p, uint32_t n)
{
    put16(p, n & 65535);
    put16(p + 2, n >> 16);
}

static void compression_tests(void)
{
    static const uint8_t vectors[][16] = {
        {20, 'a', 'b', 'c', 0x48, 0, 17, 0, 0}, {20, 'a', 'b', 'c', 33, 8, 0, 17, 0, 0}, {18, 'a', 0, 0, 17, 0, 0}, {18, 'a', 32, 1, 0, 0, 17, 0, 0}};
    static const size_t sizes[] = {9, 10, 7, 9}, plain[] = {6, 6, 3, 35};
    uint8_t output[20000], stream[20000];
    ra_error error = {0};
    size_t i, j, pos, seed;
    for (i = 0; i < 4; ++i)
    {
        CHECK(ra_lzo_decode((ra_view){vectors[i], sizes[i]}, output, plain[i], &error));
        for (j = 0; j < plain[i]; ++j) CHECK(output[j] == (i < 2 ? (uint8_t)"abc"[j % 3] : 'a'));
        for (j = 0; j < sizes[i]; ++j) CHECK(!ra_lzo_decode((ra_view){vectors[i], j}, output, plain[i], &error));
        CHECK(!ra_lzo_decode((ra_view){vectors[i], sizes[i]}, output, plain[i] - 1, &error));
    }
    /* 覆盖 2 KiB 与 16 KiB 远距离指令，并验证重叠复制的边界。 */
    for (seed = 2049; seed <= 16385; seed += 14336)
    {
        size_t extension = seed - 18;
        pos = 0;
        stream[pos++] = 0;
        while (extension > 255)
        {
            stream[pos++] = 0;
            extension -= 255;
        }
        stream[pos++] = (uint8_t)extension;
        for (i = 0; i < seed; ++i) stream[pos++] = (uint8_t)i;
        stream[pos++] = seed == 2049 ? 0 : 17;
        stream[pos++] = seed == 2049 ? 0 : 4;
        if (seed != 2049) stream[pos++] = 0;
        stream[pos++] = 17;
        stream[pos++] = 0;
        stream[pos++] = 0;
        CHECK(ra_lzo_decode((ra_view){stream, pos}, output, seed + 3, &error));
        CHECK(output[seed] == 0 && output[seed + 1] == 1 && output[seed + 2] == 2);
        stream[pos - (seed == 2049 ? 4 : 5)] = 255;
        CHECK(!ra_lzo_decode((ra_view){stream, pos}, output, seed + 3, &error));
    }
    {
        static const uint8_t lcw[] = {0x83, 'a', 'b', 'c', 0x00, 3, 0xfe, 4, 0, 'x', 0xff, 4, 0, 6, 0, 0xc0, 0, 0, 0x80};
        static const uint8_t relative[] = {0, 0x81, 'z', 0xff, 8, 0, 1, 0, 0x80};
        CHECK(ra_lcw_decode((ra_view){lcw, sizeof(lcw)}, output, 17, &error));
        CHECK(!memcmp(output, "abcabcxxxxxxxxabc", 17));
        CHECK(ra_lcw_decode((ra_view){relative, sizeof(relative)}, output, 9, &error));
        CHECK(!memcmp(output, "zzzzzzzzz", 9));
        for (i = 0; i < sizeof(lcw); ++i) CHECK(!ra_lcw_decode((ra_view){lcw, i}, output, 17, &error));
        CHECK(!ra_lcw_decode((ra_view){lcw, sizeof(lcw)}, output, 16, &error));
    }
    CHECK(!ra_lzo_decode((ra_view){NULL, 4}, output, 4, &error));
    CHECK(!ra_lcw_decode((ra_view){NULL, 4}, output, 4, &error));
}

static size_t tmp_fixture(uint8_t *data)
{
    size_t i;
    memset(data, 0, 1880);
    put32(data, 1);
    put32(data + 4, 1);
    put32(data + 8, 60);
    put32(data + 12, 30);
    put32(data + 16, 20);
    put32(data + 28, 1852);
    put32(data + 32, 952);
    put32(data + 36, 1856);
    put32(data + 40, UINT32_MAX);
    put32(data + 44, UINT32_MAX);
    put32(data + 48, 2);
    put32(data + 52, 2);
    put32(data + 56, 3);
    for (i = 0; i < 900; ++i) data[72 + i] = (uint8_t)(i % 254 + 1);
    data[1872] = 7;
    data[1873] = 0;
    data[1874] = 8;
    data[1875] = 9;
    return 1880;
}

static void tmp_tests(void)
{
    uint8_t data[1880];
    size_t size = tmp_fixture(data), i;
    ra_tmp tmp = {0};
    ra_error error = {0};
    ra_palette palette = {0};
    map_image image = {0};
    CHECK(ra_tmp_open(&tmp, (ra_view){data, size}, &error));
    CHECK(tmp.count == 1 && tmp.tiles[0].pixels.size == 900 && tmp.tiles[0].extra.size == 4 && tmp.tiles[0].extra_x == -1);
    palette.colors[7] = (ra_rgb){255, 0, 0};
    CHECK(map_tmp_render(&tmp, &palette, &image, &error));
    CHECK(image.drawn == 903 && image.width == 93 && image.height == 63);
    map_image_close(&image);
    ra_tmp_close(&tmp);
    for (i = 0; i < size; ++i) CHECK(!ra_tmp_open(&tmp, (ra_view){data, i}, &error));
    put32(data + 28, UINT32_MAX);
    CHECK(!ra_tmp_open(&tmp, (ra_view){data, size}, &error));
    tmp_fixture(data);
    put32(data + 48, 4097);
    CHECK(!ra_tmp_open(&tmp, (ra_view){data, size}, &error));
    tmp_fixture(data);
    put32(data + 16, 0);
    CHECK(ra_tmp_open(&tmp, (ra_view){data, size}, &error) && !tmp.tiles[0].present);
    ra_tmp_close(&tmp);
    put32(data, UINT32_MAX);
    CHECK(!ra_tmp_open(&tmp, (ra_view){data, size}, &error));
}

static char *base64(const uint8_t *bytes, size_t count)
{
    static const char alphabet[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
    char *text = calloc((count + 2) / 3 * 4 + 1, 1);
    size_t i, pos = 0;
    if (!text) return NULL;
    for (i = 0; i < count; i += 3)
    {
        uint32_t n = (uint32_t)bytes[i] << 16;
        if (i + 1 < count) n |= (uint32_t)bytes[i + 1] << 8;
        if (i + 2 < count) n |= bytes[i + 2];
        text[pos++] = alphabet[n >> 18];
        text[pos++] = alphabet[(n >> 12) & 63];
        text[pos++] = i + 1 < count ? alphabet[(n >> 6) & 63] : '=';
        text[pos++] = i + 2 < count ? alphabet[n & 63] : '=';
    }
    return text;
}

static void map_tests(void)
{
    uint8_t block[48] = {0};
    char text[4096], *encoded;
    ra_map map = {0};
    ra_ini ini = {0};
    ra_error error = {0};
    uint8_t *packed = NULL;
    size_t size = 0;
    /* 一个真实布局记录，带终止坐标；打乱 Base64 行顺序并重复第一行。 */
    put16(block, 19);
    put16(block + 2, 15);
    block[4] = 32;
    put16(block + 5, 1);
    put16(block + 7, 1);
    block[14] = 2;
    block[20] = 17;
    encoded = base64(block, 23);
    CHECK(encoded != NULL);
    snprintf(text, sizeof(text),
             "CampaignMoneyDeltaEasy=0\n[Map]\nTheater=TEMPERATE\nSize=0,0,1,1\nLocalSize=0,0,1,1\n[Waypoints]\n0=1001\n9=-13844\n[Structures]\n0=Neutral,"
             "GAPOWR,256,1,1,0\n[IsoMapPack5]\n2=%s\n1=WRONG\n1=%.16s\n",
             encoded + 16, encoded);
    CHECK(ra_map_open(&map, (ra_view){(const uint8_t *)text, strlen(text)}, "fixture.map", &error));
    CHECK(map.cell_count == 1 && map.cells[0].height == 2 && map.trailing_bytes == 4 && map.preamble_entries == 1);
    CHECK(map.object_count == 3 && map.outside_objects == 1 && map.objects[1].x == 156 && map.objects[1].y == -14);
    CHECK(ra_map_at(&map, 1, 1) == &map.cells[0] && !ra_map_at(&map, -1, 1) && !ra_map_at(&map, 512, 0));
    CHECK(ra_ini_get(&map.ini, "__RA2_Map_Preamble", "CampaignMoneyDeltaEasy") != NULL);
    ra_map_close(&map);
    snprintf(text, sizeof(text), "[p]\n2=%s\n1=%.16s\n", encoded + 16, encoded);
    CHECK(ra_ini_parse(&ini, (ra_view){(const uint8_t *)text, strlen(text)}, "test", &error));
    CHECK(ra_map_pack(&ini, "p", true, &packed, &size, &error) && size == 15);
    CHECK(packed[9] == 2);
    free(packed);
    ra_ini_close(&ini);
    snprintf(text, sizeof(text), "[p]\n2=%s\n", encoded);
    CHECK(ra_ini_parse(&ini, (ra_view){(const uint8_t *)text, strlen(text)}, "test", &error));
    CHECK(!ra_map_pack(&ini, "p", true, &packed, &size, &error));
    ra_ini_close(&ini);
    snprintf(text, sizeof(text), "[p]\n1=%s!\n", encoded);
    CHECK(ra_ini_parse(&ini, (ra_view){(const uint8_t *)text, strlen(text)}, "test", &error));
    CHECK(!ra_map_pack(&ini, "p", true, &packed, &size, &error));
    ra_ini_close(&ini);
    free(encoded);
    snprintf(text, sizeof(text), "[Map]\nTheater=SNOW\nSize=0,0,2,3\nLocalSize=0,0,2,3\n");
    CHECK(ra_map_open(&map, (ra_view){(const uint8_t *)text, strlen(text)}, "blank.map", &error));
    CHECK(map.cell_count == 9 && map.stored_cells == 0 && map.defaulted_cells == 9);
    ra_map_close(&map);
}

static int app_main(int argc, char **argv)
{
    (void)argc;
    (void)argv;
    compression_tests();
    tmp_tests();
    map_tests();
    printf("{\"checks\":%u,\"failures\":%u}\n", checks, failures);
    return failures ? 1 : 0;
}
