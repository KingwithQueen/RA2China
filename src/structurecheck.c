#define _CRT_SECURE_NO_WARNINGS
#include "internal.h"
#include "battle_scene.h"
#include <stdlib.h>
#include <string.h>

static battle_scene scene;
static const char *source_directory;
static void string(const char *text)
{
    putchar('"');
    while (*text)
    {
        unsigned c = (uint8_t)*text++;
        if (c == '"' || c == '\\') printf("\\%c", c);
        else if (c < 32) printf("\\u%04x", c);
        else putchar((int)c);
    }
    putchar('"');
}
static size_t entries(const ra_ini *ini, const char *section)
{
    size_t result = 0;
    for (size_t i = 0; i < ini->entry_count; ++i)
        if (ra_equal(ini->entries[i].section, section) && ra_ini_get(ini, section, ini->entries[i].key) == &ini->entries[i]) ++result;
    return result;
}
static bool report(size_t index, bool images, const char *directory, ra_error *error)
{
    if (!battle_scene_map(&scene, index, false, error)) return false;
    char source_path[32768] = {0};
    if (source_directory)
    {
        snprintf(source_path, sizeof(source_path), "%s/%03zu-%s.ini", source_directory, index, scene.maps.sources[index].name);
        if (!battle_file_write(source_path, scene.maps.sources[index].bytes.data, scene.maps.sources[index].bytes.size, error)) return false;
    }
    ra_battle *b = &scene.battle;
    const ra_ini_entry *multi = ra_ini_get(&scene.map.ini, "Basic", "MultiplayerOnly");
    printf("{\"map\":");
    string(scene.maps.sources[index].name);
    printf(",\"theater\":");
    string(scene.map.theater);
    printf(",\"multiplayer_only\":%s,\"structures\":%zu,\"tanks\":%zu,\"pending_weapons\":%zu,\"houses\":[",
           multi && ra_equal(multi->value, "yes") ? "true" : "false", scene.structure_count, scene.imported_units, scene.pending_weapons);
    for (uint32_t i = 0; i < scene.house_count; ++i)
    {
        uint32_t output, drain;
        ra_battle_power(b, i + 1, &output, &drain);
        if (i) putchar(',');
        printf("{\"id\":");
        string(scene.houses[i].id);
        printf(",\"country\":");
        string(scene.houses[i].country);
        printf(",\"team\":%u,\"allies\":%u,\"initial_credits\":%u,\"power\":%u,\"drain\":%u}", i + 1, b->allies[i], scene.houses[i].credits, output, drain);
    }
    printf("],\"source_file\":");
    string(source_path);
    printf(",\"objects\":[");
    for (uint32_t i = 0; i < b->count; ++i)
    {
        const ra_battle_unit *unit = &b->units[i];
        if (i) putchar(',');
        printf("{\"id\":%u,\"line\":%zu,\"type\":", unit->id, scene.unit_source_lines[i]);
        string(b->types[unit->type].id);
        printf(",\"owner\":");
        string(scene.houses[unit->team - 1].id);
        printf(",\"x\":%u,\"y\":%u,\"health\":%u,\"strength\":%u,\"facing\":%u,\"structure\":%s}", unit->cell % b->width, ra_battle_cell_y(b, unit->cell),
               unit->health, b->types[unit->type].strength, unit->body.initial / 256, b->types[unit->type].structure ? "true" : "false");
    }
    printf("],\"pending_objects\":[");
    for (size_t i = 0; i < scene.issue_count; ++i)
    {
        if (i) putchar(',');
        printf("{\"line\":%zu,\"type\":", scene.issues[i].line);
        string(scene.issues[i].type);
        printf(",\"reason\":");
        string(scene.issues[i].reason);
        putchar('}');
    }
    uint8_t before[20], after[20];
    ra_battle_hash(b, before);
    printf("],\"visuals\":[");
    size_t missing = 0, partial = 0, total = 0;
    for (uint32_t type = 2; images && type < b->type_count; ++type)
    {
        ra_battle_unit *unit = NULL;
        for (uint32_t j = 0; j < b->count; ++j)
            if (b->units[j].type == type)
            {
                unit = &b->units[j];
                break;
            }
        if (!unit) continue;
        if (total++) putchar(',');
        printf("{\"id\":");
        string(b->types[type].id);
        ra_error failure = {0};
        uint32_t source_health = unit->health;
        unit->health = b->types[type].strength;
        const ra_voxel_image *image = battle_scene_structure_sprite(&scene, unit, &failure);
        unit->health = source_health;
        if (!image)
        {
            ++missing;
            printf(",\"missing\":true,\"reason\":");
            string(failure.message);
        }
        else
        {
            uint32_t saved = unit->health;
            size_t normal_pixels = image->drawn_pixels;
            uint8_t image_digest[20];
            char normal_hash[41], damaged_hash[41] = {0};
            ra_sha1((ra_view){(const uint8_t *)image->pixels, image->width * image->height * sizeof(*image->pixels)}, image_digest);
            ra_hex(image_digest, 20, normal_hash);
            if (directory)
            {
                char path[32768];
                snprintf(path, sizeof(path), "%s/%s-%s.bmp", directory, scene.maps.sources[index].name, b->types[type].id);
                map_image output = {0};
                output.width = (int)image->width;
                output.height = (int)image->height;
                output.pixels = image->pixels;
                if (!map_image_bmp(&output, path, error)) return false;
            }
            unit->health = b->types[type].strength / 2;
            image = battle_scene_structure_sprite(&scene, unit, &failure);
            unit->health = saved;
            if (!image)
            {
                if (error) *error = failure;
                return false;
            }
            ra_sha1((ra_view){(const uint8_t *)image->pixels, image->width * image->height * sizeof(*image->pixels)}, image_digest);
            ra_hex(image_digest, 20, damaged_hash);
            structure_visual *visual = &scene.structure_visuals[type];
            partial += visual->missing_layers;
            printf(",\"normal_sha1\":\"%s\",\"damaged_sha1\":\"%s\"", normal_hash, damaged_hash);
            printf(",\"missing\":false,\"layers\":%zu,\"missing_layers\":%zu,\"normal_pixels\":%zu,\"damaged_pixels\":%zu,\"files\":[", visual->count,
                   visual->missing_layers, normal_pixels, image ? image->drawn_pixels : 0);
            for (size_t layer = 0; layer < visual->count; ++layer)
            {
                if (layer) putchar(',');
                string(visual->layers[layer].filename);
            }
            putchar(']');
        }
        putchar('}');
    }
    ra_battle_hash(b, after);
    if (memcmp(before, after, 20)) return ra_fail(error, RA_FORMAT, 0, "visual checks changed simulation");
    printf("],\"missing_visuals\":%zu,\"missing_layers\":%zu,\"triggers\":%zu,\"events\":%zu,\"actions\":%zu,\"teams\":%zu,\"scripts\":%zu,\"taskforces\":%zu,"
           "\"script_runtime\":false,\"complete_campaign\":false,\"complete_skirmish\":false,\"simulation_unchanged\":true}",
           missing, partial, entries(&scene.map.ini, "Triggers"), entries(&scene.map.ini, "Events"), entries(&scene.map.ini, "Actions"),
           entries(&scene.map.ini, "TeamTypes"), entries(&scene.map.ini, "ScriptTypes"), entries(&scene.map.ini, "TaskForces"));
    return true;
}
static int app_main(int argc, char **argv)
{
    const char *original = "H:/开发/运行版本/原版1.006", *map = "ALL01T.map", *directory = NULL;
    bool corpus = false, images = false;
    ra_error error = {0};
    for (int i = 1; i < argc; ++i)
    {
        if (!strcmp(argv[i], "--corpus")) corpus = true;
        else if (!strcmp(argv[i], "--validate-images")) images = true;
        else if (i + 1 < argc && !strcmp(argv[i], "--images"))
        {
            directory = argv[++i];
            images = true;
        }
        else if (i + 1 < argc && !strcmp(argv[i], "--original")) original = argv[++i];
        else if (i + 1 < argc && !strcmp(argv[i], "--sources")) source_directory = argv[++i];
        else if (i + 1 < argc && !strcmp(argv[i], "--map")) map = argv[++i];
        else return 2;
    }
    scene.scenario = true;
    if (!battle_scene_open(&scene, original, &error)) goto fail;
    uint8_t digest[20];
    char rules_hash[41], art_hash[41];
    ra_sha1(scene.voxels.rule_bytes.view, digest);
    ra_hex(digest, 20, rules_hash);
    ra_sha1(scene.voxels.art_bytes.view, digest);
    ra_hex(digest, 20, art_hash);
    if (source_directory)
    {
        char path[32768];
        snprintf(path, sizeof(path), "%s/rules.ini", source_directory);
        if (!battle_file_write(path, scene.voxels.rule_bytes.view.data, scene.voxels.rule_bytes.view.size, &error)) goto fail;
        snprintf(path, sizeof(path), "%s/art.ini", source_directory);
        if (!battle_file_write(path, scene.voxels.art_bytes.view.data, scene.voxels.art_bytes.view.size, &error)) goto fail;
    }
    printf("{\"simulation_version\":%u,\"rules_sha1\":\"%s\",\"art_sha1\":\"%s\",\"maps\":[", RA_BATTLE_VERSION, rules_hash, art_hash);
    size_t count = 0;
    for (size_t i = 0; i < scene.maps.source_count; ++i)
    {
        if (!corpus && !ra_equal(scene.maps.sources[i].name, map)) continue;
        if (count++) putchar(',');
        if (!report(i, images, directory, &error)) goto fail;
    }
    if (!count)
    {
        ra_fail(&error, RA_NOT_FOUND, 0, "scenario map was not found");
        goto fail;
    }
    printf("],\"map_count\":%zu,\"complete_game\":false}\n", count);
    battle_scene_close(&scene);
    return 0;
fail:
    fprintf(stderr, "%s\n", error.message);
    battle_scene_close(&scene);
    return 1;
}
#include "entry.h"
