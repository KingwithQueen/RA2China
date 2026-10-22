#define _CRT_SECURE_NO_WARNINGS
#include "internal.h"
#include "battle_scene.h"
#include <stdlib.h>
#include <string.h>
static battle_scene scene;
static void put(uint8_t *p, uint32_t v)
{
    for (uint32_t i = 0; i < 4; ++i) p[i] = (uint8_t)(v >> (i * 8));
}
static int app_main(int argc, char **argv)
{
    if (argc != 3) return 2;
    ra_error error = {0};
    scene.scenario = scene.campaign_mode = true;
    if (!battle_scene_open(&scene, argv[1], &error)) goto fail;
    size_t map = 0;
    for (; map < scene.maps.source_count; ++map)
        if (ra_equal(scene.maps.sources[map].name, "all01t.map")) break;
    if (!battle_scene_map(&scene, map, false, &error)) goto fail;
    const char *ids[] = {"E1", "E2", "ENGINEER", "SENGINEER", "TANY"};
    uint32_t samples = 0, width = 512, height = 400;
    size_t size = 56 + (size_t)width * height * 4;
    uint8_t *bmp = calloc(size, 1);
    if (!bmp) goto fail;
    bmp[0] = 'B';
    bmp[1] = 'M';
    put(bmp + 2, (uint32_t)size);
    put(bmp + 10, 56);
    put(bmp + 14, 40);
    put(bmp + 18, width);
    put(bmp + 22, (uint32_t)-(int32_t)height);
    bmp[26] = 1;
    bmp[28] = 32;
    uint32_t *pixels = (uint32_t *)(void *)(bmp + 56);
    for (uint32_t i = 0; i < width * height; ++i) pixels[i] = 0x1d2934;
    for (uint32_t type = 0; type < 5; ++type)
        for (uint32_t mode = 0; mode < 3; ++mode)
            for (uint32_t direction = 0; direction < 8; ++direction)
                for (uint32_t tick = 0; tick < 6; ++tick)
                {
                    ra_battle_unit u = {0};
                    u.type = ra_economy_type(&scene.battle, ids[type]);
                    u.team = 1;
                    u.health = 1;
                    u.body = u.turret = (ra_battle_turn){direction * 8192, direction * 8192, 0, 0};
                    if (mode == 1) u.next = 1;
                    if (mode == 2) u.target = u.cooldown = 1;
                    scene.battle.tick = tick * 2;
                    const ra_voxel_image *image = battle_scene_infantry_sprite(&scene, &u, &error);
                    if (!image || image->max_x <= image->min_x)
                    {
                        free(bmp);
                        goto fail;
                    }
                    size_t opaque = 0;
                    for (size_t p = 0; p < image->width * image->height; ++p)
                        if (image->pixels[p] >> 24) ++opaque;
                    if (opaque != image->drawn_pixels)
                    {
                        fprintf(stderr, "nonzero transparent pixels in %s\n", ids[type]);
                        free(bmp);
                        goto fail;
                    }
                    ++samples;
                    if (!mode && !tick)
                        for (int y = image->min_y; y <= image->max_y; ++y)
                            for (int x = image->min_x; x <= image->max_x; ++x)
                            {
                                uint32_t color = image->pixels[(size_t)y * image->width + x];
                                if (!(color >> 24)) continue;
                                int px = (int)direction * 64 + 32 + (x - (int)image->origin_x) * 2;
                                int py = (int)type * 80 + 60 + (y - (int)image->origin_y) * 2;
                                for (int dy = 0; dy < 2; ++dy)
                                    for (int dx = 0; dx < 2; ++dx)
                                        if (px + dx >= 0 && py + dy >= 0 && px + dx < (int)width && py + dy < (int)height)
                                            pixels[(size_t)(py + dy) * width + (size_t)(px + dx)] = color & 0xffffff;
                            }
                }
    char path[32768];
    snprintf(path, sizeof(path), "%s/infantry-directions.bmp", argv[2]);
    if (!battle_file_write(path, bmp, size, &error))
    {
        free(bmp);
        goto fail;
    }
    free(bmp);
    battle_scene_close(&scene);
    printf("{\"types\":5,\"sequence_images\":%u,\"failures\":0}\n", samples);
    return 0;
fail:
    fprintf(stderr, "infantry asset failure: %s\n", error.message);
    battle_scene_close(&scene);
    return 1;
}

#include "entry.h"
