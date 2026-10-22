#define _CRT_SECURE_NO_WARNINGS
#include "battle_scene.h"
#include <float.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static unsigned checks, failures;
static battle_scene scene;
static unsigned moving_samples;
#define CHECK(value)                                                                                                                                           \
    do                                                                                                                                                         \
    {                                                                                                                                                          \
        ++checks;                                                                                                                                              \
        if (!(value))                                                                                                                                          \
        {                                                                                                                                                      \
            ++failures;                                                                                                                                        \
            fprintf(stderr, "FAIL %s:%d: %s\n", __FILE__, __LINE__, #value);                                                                                   \
            return false;                                                                                                                                      \
        }                                                                                                                                                      \
    } while (0)

static void chassis_matrix(uint32_t ramp, uint32_t facing, float matrix[12])
{
    uint32_t bits[12];
    ra_battle_chassis(ramp, facing, bits);
    memcpy(matrix, bits, sizeof(bits));
}

static bool centroid(const ra_voxel_image *image, bool green, float *x, float *y)
{
    double sx = 0, sy = 0;
    size_t count = 0;
    for (size_t row = 0; row < image->height; ++row)
        for (size_t column = 0; column < image->width; ++column)
        {
            size_t at = row * image->width + column;
            unsigned red = (image->pixels[at] >> 16) & 255, g = (image->pixels[at] >> 8) & 255;
            if (image->depth[at] == -FLT_MAX || (green ? g <= red : red <= g)) continue;
            sx += (double)column + 0.5;
            sy += (double)row + 0.5;
            ++count;
        }
    if (!count) return false;
    *x = (float)(sx / count) - image->origin_x;
    *y = (float)(sy / count) - image->origin_y;
    return true;
}

static bool geometry_tests(bool print_projections)
{
    ra_voxel voxel = {30, 0, 0, 5, 0}, turret_voxel = {30, 0, 0, 6, 0};
    ra_vxl_section section = {0}, turret_section;
    ra_vxl model = {0}, turret_model;
    ra_voxel_part parts[2] = {0};
    ra_voxel_camera camera = {0};
    ra_voxel_image image = {0}, larger = {0};
    ra_palette palette = {0};
    ra_error error = {0};
    float matrix[12], x, y;
    section.scale = 1.0f / 12;
    section.bounds[0] = 0;
    section.bounds[1] = section.bounds[2] = -0.5f;
    section.bounds[3] = 40;
    section.bounds[4] = section.bounds[5] = 0.5f;
    section.size[0] = 40;
    section.size[1] = section.size[2] = 1;
    section.normal_type = 4;
    section.voxels = &voxel;
    section.voxel_count = 1;
    section.transform[0] = section.transform[5] = section.transform[10] = 1;
    model.sections = &section;
    model.section_count = 1;
    turret_section = section;
    turret_section.voxels = &turret_voxel;
    turret_model = model;
    turret_model.sections = &turret_section;
    parts[0].vxl = &model;
    parts[1].vxl = &turret_model;
    palette.colors[5] = (ra_rgb){255, 0, 0};
    palette.colors[6] = (ra_rgb){0, 255, 0};
    camera.yaw = 45;
    camera.pitch = 30;
    camera.zoom = 1;
    camera.section = -1;
    camera.pixels_per_unit = 12;
    camera.origin_x = camera.origin_y = 64;
    camera.world_axes = true;
    CHECK(ra_voxel_image_create(&image, 128, 128, &error));
    CHECK(ra_voxel_image_create(&larger, 256, 256, &error));
    for (uint32_t body = 0; body < 32; ++body)
    {
        chassis_matrix(0, body * 2048, matrix);
        CHECK(ra_voxel_render_chassis(parts, 1, 0, &palette, NULL, &camera, matrix, &image, &error));
        CHECK(centroid(&image, false, &x, &y));
        for (size_t at = 0; at < image.width * image.height; ++at)
            if (image.depth[at] != -FLT_MAX)
            {
                /* 标记体素的已知竖直范围不随车身朝向变化，可独立核对像素高度逆变换。 */
                float height = battle_sprite_height(&image, at, 6 * 104);
                CHECK(height >= 5.9710f && height <= 6.0290f);
            }
        if (print_projections) printf("%u %.6f %.6f\n", body, x, y);
        float angle = (float)body * 6.283185307179586f / 32;
        float expected_x = (sinf(angle) + cosf(angle)) * 30.5f * 0.7071067811865475f;
        float expected_y = (sinf(angle) - cosf(angle)) * 30.5f * 0.3535533905932738f;
        /* 独立地图投影约定验证可见像素，能拦下平地旧方向和错误炮塔旋转符号。 */
        CHECK(fabsf(x - expected_x) < 0.8f && fabsf(y - expected_y) < 0.8f);
        CHECK(ra_voxel_render_chassis(parts, 1, 0, &palette, NULL, &camera, matrix, &larger, &error));
        for (size_t row = 0; row < image.height; ++row)
            CHECK(!memcmp(image.pixels + row * image.width, larger.pixels + row * larger.width, image.width * sizeof(*image.pixels)));
        for (uint32_t target = 0; target < 32; target += 4)
        {
            uint32_t distance = (target - body) & 31;
            if (distance < 8 || distance > 24) continue;
            parts[1].yaw = ((float)body - (float)target) * 11.25f;
            CHECK(ra_voxel_render_chassis(parts, 2, 0, &palette, NULL, &camera, matrix, &image, &error));
            CHECK(centroid(&image, true, &x, &y));
            angle = (float)target * 6.283185307179586f / 32;
            expected_x = (sinf(angle) + cosf(angle)) * 30.5f * 0.7071067811865475f;
            expected_y = (sinf(angle) - cosf(angle)) * 30.5f * 0.3535533905932738f;
            CHECK(fabsf(x - expected_x) < 0.8f && fabsf(y - expected_y) < 0.8f);
        }
    }
    chassis_matrix(0, 16384, matrix);
    CHECK(ra_voxel_render_chassis(parts, 1, 0, &palette, NULL, &camera, matrix, &image, &error));
    CHECK(centroid(&image, false, &x, &y));
    float previous_x = x, previous_y = y;
    parts[0].offset[0] = 1;
    CHECK(ra_voxel_render_chassis(parts, 1, 0, &palette, NULL, &camera, matrix, &image, &error));
    CHECK(centroid(&image, false, &x, &y));
    CHECK(fabsf(x - previous_x - 8.485281f) < 0.8f && fabsf(y - previous_y - 4.242641f) < 0.8f);
    camera.pixels_per_unit = -1;
    CHECK(!ra_voxel_render_chassis(parts, 1, 0, &palette, NULL, &camera, matrix, &image, &error));
    ra_voxel_image_close(&image);
    ra_voxel_image_close(&larger);
    return true;
}

static void number(map_image *image, int x, int y, uint32_t value)
{
    static const uint8_t font[10][7] = {{14, 17, 19, 21, 25, 17, 14}, {4, 12, 4, 4, 4, 4, 14},    {14, 17, 1, 2, 4, 8, 31},     {30, 1, 1, 14, 1, 1, 30},
                                        {2, 6, 10, 18, 31, 2, 2},     {31, 16, 16, 30, 1, 1, 30}, {14, 16, 16, 30, 17, 17, 14}, {31, 1, 2, 4, 8, 8, 8},
                                        {14, 17, 17, 14, 17, 17, 14}, {14, 17, 17, 15, 1, 1, 14}};
    char text[16];
    snprintf(text, sizeof(text), "%u", value);
    for (unsigned i = 0; text[i]; ++i)
        for (int row = 0; row < 14; ++row)
            for (int column = 0; column < 10; ++column)
                if (font[text[i] - '0'][row / 2] & (16 >> (column / 2))) image->pixels[(size_t)(y + row) * image->width + x + i * 12 + column] = 0xdce8ef;
}

static bool movement_tests(void)
{
    static const int dx[8] = {0, 1, 1, 1, 0, -1, -1, -1}, dy[8] = {-1, -1, 0, 1, 1, 1, 0, -1};
    ra_battle *b = &scene.battle;
    ra_error error = {0};
    uint32_t center = 0;
    for (uint32_t y = 5; y < 507 && !center; ++y)
        for (uint32_t x = 5; x < 507 && !center; ++x)
        {
            bool clear = true;
            uint32_t cell = y * 512 + x;
            for (int row = -3; row <= 3 && clear; ++row)
                for (int column = -3; column <= 3; ++column)
                {
                    uint32_t at = (uint32_t)((int)y + row) * 512 + (uint32_t)((int)x + column);
                    if (!ra_battle_passable(b, at) || b->tiles[at].ramp || b->tiles[at].height != b->tiles[cell].height) clear = false;
                }
            if (clear) center = cell;
        }
    CHECK(center != 0);
    for (unsigned direction = 0; direction < 8; ++direction)
    {
        /* 每个方向是独立夹具；清除封存标志和初态数量，不能把上一例的坦克恢复到出生格。 */
        b->terrain_sealed = false;
        b->count = b->initial_count = b->command_count = 0;
        ra_battle_reset(b);
        CHECK(ra_battle_spawn_team(b, 0, 1, center % 512, center / 512, &error));
        b->initial[0].body = b->initial[0].turret = (ra_battle_turn){direction * 8192, direction * 8192, 0, 0};
        ra_battle_reset(b);
        uint32_t goal = (uint32_t)((int)(center / 512) + dy[direction] * 3) * 512 + (uint32_t)((int)(center % 512) + dx[direction] * 3);
        CHECK(ra_battle_command_add(b, 1, 1, goal, &error));
        unsigned samples = 0;
        for (unsigned tick = 0; tick < 900; ++tick)
        {
            int32_t old_x = b->units[0].x, old_y = b->units[0].y;
            ra_battle_step(b);
            ra_battle_unit *unit = &b->units[0];
            int32_t vx = unit->x - old_x, vy = unit->y - old_y;
            if (vx || vy)
            {
                float angle = (float)ra_battle_turn_value(&unit->body, b->tick) * 6.283185307179586f / 65536;
                float forward = (vx * sinf(angle) - vy * cosf(angle)) / sqrtf((float)vx * vx + (float)vy * vy);
                CHECK(forward > 0.98f);
                ++samples;
                ++moving_samples;
                if (samples == 10) CHECK(battle_scene_sprite(&scene, unit, &error) != NULL);
            }
            if (unit->cell == goal && !unit->track_active && !unit->progress) break;
        }
        CHECK(samples >= 10 && b->units[0].health && b->units[0].cell == goal);
    }
    return true;
}

static bool original_tests(const char *original, const char *directory)
{
    ra_error error = {0};
    map_image atlas = {0};
    char path[1024];
    size_t source;
    CHECK(battle_scene_open(&scene, original, &error));
    for (source = 0; source < scene.maps.source_count; ++source)
        if (!strcmp(scene.maps.sources[source].name, "MP06T2.map")) break;
    CHECK(source < scene.maps.source_count && battle_scene_map(&scene, source, false, &error));
    atlas.width = 1024;
    atlas.height = 768;
    atlas.pixels = malloc((size_t)atlas.width * atlas.height * sizeof(*atlas.pixels));
    CHECK(atlas.pixels != NULL);
    for (int i = 0; i < atlas.width * atlas.height; ++i) atlas.pixels[i] = 0x24313c;
    ra_battle_unit unit = scene.battle.units[0];
    uint8_t before[20], after[20];
    ra_battle_hash(&scene.battle, before);
    for (unsigned row = 0; row < 6; ++row)
        for (unsigned direction = 0; direction < 8; ++direction)
        {
            unit.type = row / 3;
            uint32_t body = row % 3 == 2 ? 0 : direction * 8192, turret = row % 3 == 1 ? 0 : direction * 8192;
            unit.body = (ra_battle_turn){body, body, 0, 0};
            unit.turret = (ra_battle_turn){turret, turret, 0, 0};
            const ra_voxel_image *sprite = battle_scene_sprite(&scene, &unit, &error);
            CHECK(sprite && sprite->drawn_pixels && sprite->origin_x == 64 && sprite->origin_y == 80);
            CHECK(sprite->min_x > 0 && sprite->min_y > 0 && sprite->max_x < (int)sprite->width - 1 && sprite->max_y < (int)sprite->height - 1);
            int ox = (int)direction * 128, oy = (int)row * 128;
            /* 地面原点保持可见，能直接核对旋转时模型是否漂移。 */
            for (int delta = -3; delta <= 3; ++delta)
            {
                atlas.pixels[(size_t)(oy + 80) * atlas.width + ox + 64 + delta] = 0x62ff87;
                atlas.pixels[(size_t)(oy + 80 + delta) * atlas.width + ox + 64] = 0x62ff87;
            }
            for (size_t y = 0; y < sprite->height; ++y)
                for (size_t x = 0; x < sprite->width; ++x)
                    if (sprite->pixels[y * sprite->width + x] >> 24)
                        atlas.pixels[(size_t)(oy + y) * atlas.width + ox + x] = sprite->pixels[y * sprite->width + x] & 0xffffff;
            number(&atlas, ox + 8, oy + 110, direction * 45);
        }
    ra_battle_hash(&scene.battle, after);
    CHECK(!memcmp(before, after, sizeof(before)));
    snprintf(path, sizeof(path), "%s/unit-directions.bmp", directory);
    CHECK(map_image_bmp(&atlas, path, &error));
    /* 仅在显示夹具内覆盖坡号，检查全部原版坡面矩阵的固定原点和裁剪边界。 */
    uint8_t old_ramp = scene.battle.tiles[unit.cell].ramp;
    for (int i = 0; i < atlas.width * atlas.height; ++i) atlas.pixels[i] = 0x24313c;
    for (unsigned type = 0; type < 2; ++type)
        for (unsigned ramp = 0; ramp < 21; ++ramp)
        {
            unit.type = type;
            unit.body = unit.turret = (ra_battle_turn){16384, 16384, 0, 0};
            scene.battle.tiles[unit.cell].ramp = (uint8_t)ramp;
            const ra_voxel_image *sprite = battle_scene_sprite(&scene, &unit, &error);
            CHECK(sprite && sprite->drawn_pixels && sprite->origin_x == 64 && sprite->origin_y == 80);
            CHECK(sprite->min_x > 0 && sprite->min_y > 0 && sprite->max_x < (int)sprite->width - 1 && sprite->max_y < (int)sprite->height - 1);
            int ox = (int)(ramp % 7) * 128, oy = (int)(type * 3 + ramp / 7) * 128;
            for (size_t y = 0; y < sprite->height; ++y)
                for (size_t x = 0; x < sprite->width; ++x)
                    if (sprite->pixels[y * sprite->width + x] >> 24)
                        atlas.pixels[(size_t)(oy + y) * atlas.width + ox + x] = sprite->pixels[y * sprite->width + x] & 0xffffff;
            number(&atlas, ox + 8, oy + 110, ramp);
        }
    scene.battle.tiles[unit.cell].ramp = old_ramp;
    ra_battle_hash(&scene.battle, after);
    CHECK(!memcmp(before, after, sizeof(before)));
    snprintf(path, sizeof(path), "%s/unit-slopes.bmp", directory);
    CHECK(map_image_bmp(&atlas, path, &error));
    map_image_close(&atlas);
    CHECK(movement_tests());
    battle_scene_close(&scene);
    return true;
}

static int app_main(int argc, char **argv)
{
    if (argc == 2 && !strcmp(argv[1], "--bridge-offsets"))
    {
        for (unsigned kind = 0; kind < 4; ++kind)
            for (unsigned frame = 0; frame < 18; ++frame) printf("%u %u %d\n", kind, frame, battle_bridge_draw_offset(kind, frame));
        return 0;
    }
    bool projections = argc == 2 && !strcmp(argv[1], "--projections");
    if (argc != 1 && argc != 3 && !projections) return 2;
    if (!geometry_tests(projections)) return 1;
    if (argc == 3 && !original_tests(argv[1], argv[2])) return 1;
    if (!projections)
        printf("{\"checks\":%u,\"failures\":%u,\"fixed_scale\":true,\"moving_samples\":%u,\"original_resources\":%s}\n", checks, failures, moving_samples,
               argc == 3 ? "true" : "false");
    return failures ? 1 : 0;
}
#include "entry.h"
