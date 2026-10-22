#define _CRT_SECURE_NO_WARNINGS
#include "internal.h"
#include "battle_scene.h"
#include <stdlib.h>
#include <string.h>

static battle_scene scene;
static void put(uint8_t *p, uint32_t value)
{
    for (uint32_t i = 0; i < 4; ++i) p[i] = (uint8_t)(value >> (8 * i));
}
static int run(int argc, char **argv)
{
    if (argc < 3) return 2;
    ra_error error = {0};
    scene.scenario = scene.campaign_mode = true;
    if (!battle_scene_open(&scene, argv[1], &error)) goto fail;
    size_t map;
    for (map = 0; map < scene.maps.source_count; ++map)
        if (ra_equal(scene.maps.sources[map].name, "all01t.map")) break;
    if (map == scene.maps.source_count || !battle_scene_map(&scene, map, false, &error)) goto fail;
    const ra_battle_type *v3 = &scene.battle.types[ra_economy_type(&scene.battle, "V3")];
    const ra_battle_type *dred = &scene.battle.types[ra_economy_type(&scene.battle, "DRED")];
    const ra_battle_type *jet = &scene.battle.types[ra_economy_type(&scene.battle, "ORCA")];
    if (v3->weapon.damage != 200 || v3->weapon.range != 18 * RA_BATTLE_CELL || v3->weapon.minimum != 5 * RA_BATTLE_CELL || v3->weapon.altitude != 1550 ||
        v3->weapon.verses[9] != 5000000 || dred->weapon.damage != 300 || dred->weapon.burst != 2 || dred->weapon.missile_health != 75 ||
        dred->weapon.verses[9] != 200 || !dred->naval || !jet->flying || jet->ammo != 1)
    {
        fprintf(stderr, "original first mission weapon or motion override differs\n");
        goto fail;
    }
    const char *names[] = {"V3",       "DRED",  "SAPC", "LCRF",  "ORCA",   "ZEP",   "SHAD",  "CARGOPLANE",
                           "V3ROCKET", "DMISL", "ADOG", "GHOST", "CIVBFM", "CIVBF", "CIVBTM"};
    uint32_t width = 192 * 8, height = 160 * 15, samples = 0, clipped = 0;
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
    for (uint32_t type = 0; type < 15; ++type)
        for (uint32_t direction = 0; direction < 8; ++direction)
            for (uint32_t frame = 0; frame < 2; ++frame)
            {
                ra_battle_unit u = {0};
                u.id = 1;
                u.type = ra_economy_type(&scene.battle, names[type]);
                if (u.type == UINT32_MAX)
                {
                    free(bmp);
                    goto fail;
                }
                u.team = 1;
                u.health = 1;
                u.body = u.turret = (ra_battle_turn){direction * 8192, direction * 8192, 0, 0};
                scene.battle.tick = frame * 2;
                const ra_voxel_image *image = battle_scene_sprite(&scene, &u, &error);
                if (!image || !image->drawn_pixels)
                {
                    free(bmp);
                    goto fail;
                }
                size_t opaque = 0;
                for (size_t py = 0; py < image->height; ++py)
                    for (size_t px = 0; px < image->width; ++px)
                    {
                        uint32_t color = image->pixels[py * image->width + px];
                        if (!(color >> 24)) continue;
                        ++opaque;
                        if (!px || !py || px + 1 == image->width || py + 1 == image->height) ++clipped;
                        int x = (int)(direction * 192 + 96 + px) - (int)image->origin_x;
                        int y = (int)(type * 160 + 120 + py) - (int)image->origin_y;
                        if (!frame && x >= 0 && y >= 0 && x < (int)width && y < (int)height) pixels[(size_t)y * width + x] = color & 0xffffff;
                    }
                if (!opaque)
                {
                    free(bmp);
                    goto fail;
                }
                ++samples;
            }
    char path[32768];
    snprintf(path, sizeof(path), "%s/sea-air-models.bmp", argv[2]);
    bool saved = battle_file_write(path, bmp, size, &error);
    free(bmp);
    printf("{\"model_types\":15,\"render_samples\":%u,\"edge_pixels\":%u,\"missing_initial_objects\":%zu}\n", samples, clipped, scene.issue_count);
    battle_scene_close(&scene);
    return saved && !clipped ? 0 : 1;
fail:
    fprintf(stderr, "sea/air resource check failed: %s\n", error.message);
    battle_scene_close(&scene);
    return 1;
}
#define app_main run
#include "entry.h"
