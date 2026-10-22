#define _CRT_SECURE_NO_WARNINGS
#include "internal.h"
#include "map_scene.h"
#include <stdlib.h>
#include <string.h>
#include "entry.h"

static void json(const char *s)
{
    putchar('"');
    for (; *s; ++s)
    {
        unsigned c = (uint8_t)*s;
        if (c == '"' || c == '\\') printf("\\%c", c);
        else if (c < 32) printf("\\u%04x", c);
        else putchar((int)c);
    }
    putchar('"');
}

static void digest(ra_view bytes)
{
    uint8_t hash[20];
    char hex[41];
    ra_sha1(bytes, hash);
    ra_hex(hash, 20, hex);
    json(hex);
}

static int app_main(int argc, char **argv)
{
    map_context context = {0};
    ra_error error = {0};
    size_t i, failures = 0, cells = 0, objects = 0, overlays = 0, references = 0, missing = 0, tmp_count = 0, tmp_failures = 0, subtiles = 0;
    size_t issue_maps = 0, named = 0, declared_absent = 0, present = 0, extras = 0, unknown = 0;
    const char *original = NULL, *mod = NULL, *samples = NULL, *dump_name = NULL;
    bool strict = false;
    int arg;
    for (arg = 1; arg < argc; ++arg)
    {
        if (!strcmp(argv[arg], "--strict")) strict = true;
        else if (!strcmp(argv[arg], "--samples") && arg + 1 < argc) samples = argv[++arg];
        else if (!strcmp(argv[arg], "--dump") && arg + 1 < argc) dump_name = argv[++arg];
        else if (!original) original = argv[arg];
        else if (!mod) mod = argv[arg];
        else return 2;
    }
    if (!original) original = "H:/开发/运行版本/原版1.006";
    if (!map_context_open(&context, original, mod, &error))
    {
        fprintf(stderr, "%s\n", error.message);
        return 1;
    }
    if (dump_name)
    {
        ra_resource resource = {0};
        ra_view view = {0};
        for (i = 0; i < context.source_count; ++i)
            if (ra_equal(dump_name, context.sources[i].name))
            {
                view = context.sources[i].bytes;
                break;
            }
        if (!view.data && !ra_vfs_read(&context.vfs, dump_name, &resource, &error))
        {
            fprintf(stderr, "%s\n", error.message);
            map_context_close(&context);
            return 1;
        }
        if (!view.data) view = resource.view;
        fputs("{\"raw_hex\":\"", stdout);
        for (i = 0; i < view.size; ++i) printf("%02x", view.data[i]);
        puts("\"}");
        ra_resource_close(&resource);
        map_context_close(&context);
        return 0;
    }
    printf("{\"maps\":[");
    for (i = 0; i < context.source_count; ++i)
    {
        ra_map map = {0};
        bool ok = ra_map_open(&map, context.sources[i].bytes, context.sources[i].source, &error);
        size_t j, bad = 0;
        printf("%s{\"name\":", i ? "," : "");
        json(context.sources[i].name);
        fputs(",\"source\":", stdout);
        json(context.sources[i].source);
        fputs(",\"sha1\":", stdout);
        digest(context.sources[i].bytes);
        fputs(",\"issues\":[", stdout);
        if (ok)
            for (j = 0; j < map.cell_count; ++j)
            {
                map_template *entry = NULL;
                ra_map_cell *cell = &map.cells[j];
                uint8_t sub = cell->tile == 65535 || cell->tile == UINT32_MAX ? 0 : cell->subtile;
                bool valid;
                ++references;
                valid = map_template_get(&context, map_theater_id(map.theater), cell->tile, &entry, &error);
                if (valid && (sub >= entry->tmp.count || !entry->tmp.tiles[sub].present))
                    valid = ra_fail(&error, RA_NOT_FOUND, 0, "%s has no subtile %u", entry->name, sub);
                if (!valid)
                {
                    printf("%s{\"x\":%u,\"y\":%u,\"tile\":%u,\"sub\":%u,\"reason\":", bad ? "," : "", cell->x, cell->y, cell->tile, cell->subtile);
                    json(error.message);
                    putchar('}');
                    ++bad;
                }
            }
        printf("],\"ok\":%s,\"cells\":%zu,\"stored_cells\":%zu,\"defaulted_cells\":%zu,\"theater\":\"%s\",\"missing\":%zu,\"objects\":%zu,\"outside_objects\":%"
               "zu,\"overlays\":%zu,\"preamble\":%zu",
               ok ? "true" : "false", map.cell_count, map.stored_cells, map.defaulted_cells, map.theater, bad, map.object_count, map.outside_objects,
               map.overlay_count, map.preamble_entries);
        fputs(",\"overlay_sha1\":", stdout);
        digest((ra_view){map.overlay, map.overlay ? 262144 : 0});
        fputs(",\"data_sha1\":", stdout);
        digest((ra_view){map.overlay_data, map.overlay_data ? 262144 : 0});
        fputs(",\"preview_sha1\":", stdout);
        digest((ra_view){map.preview, map.preview_size});
        fputs(",\"probes\":[", stdout);
        if (ok)
            for (j = 0; j < 17; ++j)
            {
                const ra_map_cell *cell = &map.cells[j * (map.cell_count - 1) / 16];
                printf("%s[%u,%u,%u,%u,%u,%u]", j ? "," : "", cell->x, cell->y, cell->tile, cell->subtile, cell->height, cell->ice);
            }
        fputs("]}", stdout);
        if (!ok)
        {
            ++failures;
            fprintf(stderr, "%s line %zu: %s\n", context.sources[i].name, error.line, error.message);
        }
        missing += bad;
        if (bad) ++issue_maps;
        if (ok && samples &&
            (ra_equal(context.sources[i].name, "MP02T2.map") || ra_equal(context.sources[i].name, "MP21S2.map") ||
             ra_equal(context.sources[i].name, "MP29U2.map")))
        {
            map_image image = {0};
            char path[32768];
            snprintf(path, sizeof(path), "%s/%s.bmp", samples, context.sources[i].name);
            if (!map_render(&context, &map, &image, true, true, true, &error) || !map_image_bmp(&image, path, &error))
            {
                ++failures;
                fprintf(stderr, "render: %s\n", error.message);
            }
            map_image_close(&image);
        }
        cells += map.cell_count;
        objects += map.object_count;
        overlays += map.overlay_count;
        ra_map_close(&map);
    }
    printf("],\"theaters\":[");
    for (i = 0; i < 3; ++i)
    {
        size_t j, absent = 0;
        if (!map_theater_open(&context, (int)i, &error))
        {
            ++failures;
            fprintf(stderr, "%s\n", error.message);
            continue;
        }
        for (j = 0; j < context.theaters[i].count; ++j)
        {
            map_template *entry;
            if (map_template_get(&context, (int)i, (uint32_t)j, &entry, &error)) ++named;
            else if (error.code == RA_NOT_FOUND) ++absent;
            else
            {
                ++tmp_failures;
                fprintf(stderr, "%s: %s\n", context.theaters[i].templates[j].name, error.message);
            }
        }
        printf("%s{\"id\":%zu,\"declared\":%zu,\"absent\":%zu,\"absent_names\":[", i ? "," : "", i, context.theaters[i].count, absent);
        absent = 0;
        for (j = 0; j < context.theaters[i].count; ++j)
            if (!context.theaters[i].templates[j].loaded)
            {
                if (absent++) putchar(',');
                json(context.theaters[i].templates[j].name);
            }
        fputs("]}", stdout);
        declared_absent += absent;
    }
    fputs("],\"tmp_resources\":[", stdout);
    /* 包内直接枚举，覆盖未出现在地形 INI 名称表中的变体。 */
    for (i = 0; i < 7; ++i)
    {
        static const char *packages[] = {"isogen.mix", "isotemp.mix", "isosnow.mix", "isourb.mix", "temperat.mix", "snow.mix", "urban.mix"};
        size_t j;
        for (j = 0; j < context.terrain_archives[i].count; ++j)
        {
            ra_view view;
            ra_tmp tmp = {0};
            size_t k, tile_present = 0, tile_extra = 0, base_bytes = 0, extra_bytes = 0, depth_bytes = 0;
            bool ok;
            if (!ra_mix_get_id(&context.terrain_archives[i], context.terrain_archives[i].entries[j].id, &view, &error))
            {
                ++tmp_failures;
                continue;
            }
            if (view.size < 16 || ra_le32(view.data + 8) != 60 || ra_le32(view.data + 12) != 30)
            {
                ++unknown;
                continue;
            }
            ok = ra_tmp_open(&tmp, view, &error);
            printf("%s{\"archive\":\"%s\",\"id\":\"%08x\",\"ok\":%s,\"tiles\":%zu", tmp_count ? "," : "", packages[i],
                   context.terrain_archives[i].entries[j].id, ok ? "true" : "false", tmp.count);
            if (!ok)
            {
                ++tmp_failures;
                fputs(",\"error\":", stdout);
                json(error.message);
            }
            for (k = 0; k < tmp.count; ++k)
                if (tmp.tiles[k].present)
                {
                    ++tile_present;
                    base_bytes += tmp.tiles[k].pixels.size;
                    extra_bytes += tmp.tiles[k].extra.size;
                    depth_bytes += tmp.tiles[k].depth.size + tmp.tiles[k].extra_depth.size;
                    if (tmp.tiles[k].extra.size) ++tile_extra;
                }
            printf(",\"present\":%zu,\"extras\":%zu,\"base_bytes\":%zu,\"extra_bytes\":%zu,\"depth_bytes\":%zu,\"sha1\":", tile_present, tile_extra, base_bytes,
                   extra_bytes, depth_bytes);
            digest(view);
            putchar('}');
            ++tmp_count;
            subtiles += tmp.count;
            present += tile_present;
            extras += tile_extra;
            ra_tmp_close(&tmp);
        }
    }
    printf("],\"summary\":{\"maps\":%zu,\"cells\":%zu,\"objects\":%zu,\"overlays\":%zu,\"references\":%zu,\"reference_issue_maps\":%zu,\"missing_references\":%"
           "zu,\"named_tmp\":%zu,\"declared_absent_tmp\":%zu,\"tmp\":%zu,\"subtiles\":%zu,\"present_subtiles\":%zu,\"extra_images\":%zu,\"unclassified_"
           "members\":%zu,\"tmp_failures\":%zu,\"parse_failures\":%zu}}\n",
           context.source_count, cells, objects, overlays, references, issue_maps, missing, named, declared_absent, tmp_count, subtiles, present, extras,
           unknown, tmp_failures, failures);
    map_context_close(&context);
    return failures || tmp_failures ? 1 : strict && missing ? 2 : 0;
}
