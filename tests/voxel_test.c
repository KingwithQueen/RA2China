#define _CRT_SECURE_NO_WARNINGS
#include "voxel_internal.h"
#include <stdlib.h>
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

static void put32(uint8_t *p, uint32_t value)
{
    size_t i;
    for (i = 0; i < 4; ++i) p[i] = (uint8_t)(value >> (i * 8));
}

static void put_float(uint8_t *p, float value)
{
    uint32_t bits;
    memcpy(&bits, &value, sizeof(bits));
    put32(p, bits);
}

static size_t make_vxl(uint8_t bytes[1024])
{
    uint8_t *footer = bytes + 848;
    static const uint8_t runs[] = {1, 2, 5, 0, 6, 1, 2, 1, 0, 0};
    size_t i;
    memset(bytes, 0, 1024);
    memcpy(bytes, "Voxel Animation", 15);
    put32(bytes + 16, 1);
    put32(bytes + 20, 1);
    put32(bytes + 24, 1);
    put32(bytes + 28, 18);
    bytes[32] = 16;
    bytes[33] = 31;
    memcpy(bytes + 802, "Limb", 4);
    put32(bytes + 822, 1);
    put32(bytes + 830, 0);
    put32(bytes + 834, 9);
    memcpy(bytes + 838, runs, sizeof(runs));
    put32(footer + 4, 4);
    put32(footer + 8, 8);
    put_float(footer + 12, 1);
    for (i = 0; i < 3; ++i) put_float(footer + 16 + (i * 4 + i) * 4, 1);
    put_float(footer + 76, 1);
    put_float(footer + 80, 1);
    put_float(footer + 84, 4);
    footer[88] = 1;
    footer[89] = 1;
    footer[90] = 4;
    footer[91] = 4;
    return 940;
}

static size_t make_hva(uint8_t bytes[136])
{
    size_t i;
    memset(bytes, 0, 136);
    put32(bytes + 16, 2);
    put32(bytes + 20, 1);
    memcpy(bytes + 24, "Limb", 4);
    for (i = 0; i < 3; ++i) put_float(bytes + 40 + (i * 4 + i) * 4, 1);
    put_float(bytes + 88 + 4, -1);
    put_float(bytes + 88 + 12, 2);
    put_float(bytes + 88 + 16, 1);
    put_float(bytes + 88 + 40, 1);
    return 136;
}

static void parser_tests(void)
{
    uint8_t data[1024], animation[136], tables[1296] = {0};
    size_t size = make_vxl(data), i, mapping[1];
    ra_vxl vxl = {0};
    ra_hva hva = {0};
    ra_vpl vpl = {0};
    ra_error error = {0};
    uint8_t mapped;
    CHECK(sizeof(ra_voxel) == 5);
    CHECK(ra_vxl_parse(&vxl, (ra_view){data, size}, &error));
    CHECK(vxl.section_count == 1 && vxl.voxel_count == 2);
    CHECK(vxl.sections[0].voxels[0].z == 1 && vxl.sections[0].voxels[1].z == 2 && vxl.sections[0].voxels[1].color == 6);
    make_hva(animation);
    CHECK(ra_hva_parse(&hva, (ra_view){animation, sizeof(animation)}, &error));
    CHECK(hva.frame_count == 2 && hva.section_count == 1);
    CHECK(ra_hva_bind(&vxl, &hva, mapping, 1, &error) && mapping[0] == 0);
    memcpy(hva.sections[0], "Other", 6);
    CHECK(!ra_hva_bind(&vxl, &hva, mapping, 1, &error));
    memcpy(hva.sections[0], "limb", 5);
    CHECK(ra_hva_bind(&vxl, &hva, mapping, 1, &error));
    CHECK(!ra_hva_bind(&vxl, &hva, mapping, 0, &error));
    ra_vxl_close(&vxl);
    ra_hva_close(&hva);
    for (i = 0; i < size; ++i) CHECK(!ra_vxl_parse(&vxl, (ra_view){data, i}, &error));
    for (i = 0; i < sizeof(animation); ++i) CHECK(!ra_hva_parse(&hva, (ra_view){animation, i}, &error));
    data[844] = 1;
    CHECK(!ra_vxl_parse(&vxl, (ra_view){data, size}, &error));
    make_vxl(data);
    data[839] = 4;
    CHECK(!ra_vxl_parse(&vxl, (ra_view){data, size}, &error));
    make_vxl(data);
    data[838] = 0;
    data[839] = 0;
    CHECK(!ra_vxl_parse(&vxl, (ra_view){data, size}, &error));
    make_vxl(data);
    data[841] = 244;
    CHECK(ra_vxl_parse(&vxl, (ra_view){data, size}, &error));
    CHECK(vxl.sections[0].unmapped_normals == 1);
    ra_vxl_close(&vxl);
    make_vxl(data);
    put32(data + 848 + 12, 0x7fc00000u);
    CHECK(!ra_vxl_parse(&vxl, (ra_view){data, size}, &error));
    make_vxl(data);
    put32(data + 834, 18);
    CHECK(!ra_vxl_parse(&vxl, (ra_view){data, size}, &error));
    make_hva(animation);
    put32(animation + 40, 0x7f800000u);
    CHECK(!ra_hva_parse(&hva, (ra_view){animation, sizeof(animation)}, &error));
    put32(animation + 16, UINT32_MAX);
    CHECK(!ra_hva_parse(&hva, (ra_view){animation, sizeof(animation)}, &error));
    make_hva(animation);
    put32(animation + 16, 1);
    put32(animation + 20, 0);
    CHECK(ra_hva_parse(&hva, (ra_view){animation, 24}, &error));
    CHECK(hva.frame_count == 1 && hva.section_count == 0);
    ra_hva_close(&hva);
    put32(tables, 16);
    put32(tables + 4, 31);
    put32(tables + 8, 2);
    tables[784 + 256 + 5] = 99;
    CHECK(ra_vpl_parse(&vpl, (ra_view){tables, sizeof(tables)}, &error));
    CHECK(ra_vpl_lookup(&vpl, 1, 5, &mapped, &error) && mapped == 99);
    CHECK(!ra_vpl_lookup(&vpl, 2, 5, &mapped, &error));
    CHECK(!ra_vpl_parse(&vpl, (ra_view){tables, sizeof(tables) - 1}, &error));
    put32(tables + 4, 256);
    CHECK(!ra_vpl_parse(&vpl, (ra_view){tables, sizeof(tables)}, &error));
}

static void binding_order_tests(void)
{
    ra_vxl_section sections[2] = {0};
    char names[2][17] = {"Second", "First"};
    float matrices[24] = {0};
    ra_vxl vxl = {0};
    ra_hva hva = {0};
    size_t mapping[2];
    ra_error error = {0};
    memcpy(sections[0].name, "First", 6);
    memcpy(sections[1].name, "Second", 7);
    vxl.sections = sections;
    vxl.section_count = 2;
    hva.sections = names;
    hva.section_count = 2;
    hva.matrices = matrices;
    CHECK(ra_hva_bind(&vxl, &hva, mapping, 2, &error));
    CHECK(mapping[0] == 1 && mapping[1] == 0);
}

static void render_tests(void)
{
    uint8_t data[1024], animation[136], digest[20], other[20];
    ra_vxl vxl = {0};
    ra_hva hva = {0};
    ra_voxel_image image = {0};
    ra_palette palette = {0};
    ra_voxel_part part = {0};
    ra_voxel_camera camera = {45, 30, 1, 225, false, false, {255, 0, 0}, -1, 0, 0, 0, false};
    ra_error error = {0};
    size_t mapping[1], size = make_vxl(data);
    float point[3] = {0.25f, 0.75f, 2}, result[3], normal[3];
    make_hva(animation);
    palette.colors[5] = (ra_rgb){255, 0, 0};
    palette.colors[6] = (ra_rgb){0, 255, 0};
    CHECK(ra_vxl_parse(&vxl, (ra_view){data, size}, &error));
    CHECK(ra_hva_parse(&hva, (ra_view){animation, sizeof(animation)}, &error));
    CHECK(ra_hva_bind(&vxl, &hva, mapping, 1, &error));
    CHECK(ra_voxel_transform(&vxl.sections[0], hva.matrices + 12, point, result, &error));
    CHECK(fabsf(result[0] - 1.25f) < 0.0001f && fabsf(result[1] - 0.25f) < 0.0001f && result[2] == 2);
    CHECK(ra_voxel_normal(4, 243, normal));
    CHECK(!ra_voxel_normal(4, 244, normal));
    CHECK(ra_voxel_normal(2, 35, normal));
    CHECK(!ra_voxel_normal(2, 36, normal));
    CHECK(ra_voxel_image_create(&image, 128, 96, &error));
    part.vxl = &vxl;
    part.hva = &hva;
    part.mapping = mapping;
    CHECK(ra_voxel_render(&part, 1, 0, &palette, NULL, &camera, &image, &error));
    CHECK(image.drawn_pixels > 100);
    ra_sha1((ra_view){(uint8_t *)image.pixels, image.width * image.height * 4}, digest);
    CHECK(ra_voxel_render(&part, 1, 1, &palette, NULL, &camera, &image, &error));
    ra_sha1((ra_view){(uint8_t *)image.pixels, image.width * image.height * 4}, other);
    CHECK(memcmp(digest, other, 20));
    CHECK(ra_voxel_render(&part, 1, 0, &palette, NULL, &camera, &image, &error));
    ra_sha1((ra_view){(uint8_t *)image.pixels, image.width * image.height * 4}, other);
    CHECK(!memcmp(digest, other, 20));
    camera.zoom = 0;
    CHECK(!ra_voxel_render(&part, 1, 0, &palette, NULL, &camera, &image, &error));
    camera.zoom = 1;
    mapping[0] = 2;
    CHECK(!ra_voxel_render(&part, 1, 0, &palette, NULL, &camera, &image, &error));
    CHECK(!ra_voxel_image_create(NULL, 128, 96, &error));
    CHECK(!ra_voxel_image_create(NULL, 4097, 96, &error));
    ra_voxel_image_close(&image);
    ra_hva_close(&hva);
    ra_vxl_close(&vxl);
}

static int app_main(int argc, char **argv)
{
    (void)argc;
    (void)argv;
    parser_tests();
    binding_order_tests();
    render_tests();
    printf("{\"checks\":%u,\"failures\":%u}\n", checks, failures);
    return failures ? 1 : 0;
}
