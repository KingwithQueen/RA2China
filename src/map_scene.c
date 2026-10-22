#define _CRT_SECURE_NO_WARNINGS
#include "internal.h"
#include "map_scene.h"
#include <stdlib.h>
#include <string.h>
#ifdef _WIN32
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#endif

int map_theater_id(const char *name)
{
    return ra_equal(name, "SNOW") ? 1 : ra_equal(name, "URBAN") ? 2 : 0;
}

static bool has_pack(ra_view bytes)
{
    static const char pattern[] = "[IsoMapPack5]";
    size_t i;
    for (i = 0; i + sizeof(pattern) - 1 <= bytes.size; ++i)
        if (!memcmp(bytes.data + i, pattern, sizeof(pattern) - 1)) return true;
    return false;
}

static void map_name(const map_context *context, uint32_t id, char name[64])
{
    size_t i;
    int n, variant;
    for (i = 0; i < context->missions.entry_count; ++i)
    {
        const ra_ini_entry *e = &context->missions.entries[i];
        if (!ra_equal(e->section, "MultiMaps")) continue;
        snprintf(name, 64, "%s.map", e->value);
        if (ra_mix_id(name, RA_HASH_CRC32) == id) return;
    }
    for (variant = 0; variant < 6; ++variant)
        for (n = 1; n <= 20; ++n)
        {
            snprintf(name, 64, "%s%02d%c.map", variant < 3 ? "all" : "sov", n, "tsu"[variant % 3]);
            if (ra_mix_id(name, RA_HASH_CRC32) == id) return;
        }
    snprintf(name, 64, "ID-%08x.map", id);
}

bool map_context_open(map_context *context, const char *original, const char *mod, ra_error *error)
{
    static const char *terrain[] = {"isogen.mix", "isotemp.mix", "isosnow.mix", "isourb.mix", "temperat.mix", "snow.mix", "urban.mix"};
    static const char *archives[] = {"MULTI.MIX", "MAPS01.MIX", "MAPS02.MIX"};
    map_context result = {0};
    ra_resource text = {0};
    char path[32768];
    size_t i, j, capacity = 0;
    const char *maps_root = mod ? mod : original;
    if (!ra_asset_mount(&result.vfs, original, mod, error)) goto fail;
    snprintf(path, sizeof(path), "%s/ra2.mix", maps_root);
    if (!ra_file_open(&result.terrain_file, path, error) || !ra_mix_open(&result.terrain_root, result.terrain_file.view, RA_HASH_CRC32, error)) goto fail;
    for (i = 0; i < 7; ++i)
    {
        ra_view archive;
        if (!ra_mix_get(&result.terrain_root, terrain[i], &archive, error) || !ra_mix_open(&result.terrain_archives[i], archive, RA_HASH_CRC32, error))
            goto fail;
        snprintf(path, sizeof(path), "%s/ra2.mix|%s", maps_root, terrain[i]);
        if (!ra_vfs_mount_mix(&result.vfs, path, i < 4 ? 20 + (int)i : 14 + (int)i - 4, RA_HASH_CRC32, error)) goto fail;
    }
    if (!ra_vfs_read(&result.vfs, "missions.pkt", &text, error) || !ra_ini_parse(&result.missions, text.view, text.source, error)) goto fail;
    ra_resource_close(&text);
    if (!ra_vfs_read(&result.vfs, "rules.ini", &text, error) || !ra_ini_parse(&result.rules, text.view, text.source, error)) goto fail;
    ra_resource_close(&text);
    for (i = 0; i < result.rules.entry_count && result.overlay_name_count < 256; ++i)
    {
        const ra_ini_entry *entry = &result.rules.entries[i];
        if (ra_equal(entry->section, "OverlayTypes") && ra_ini_get(&result.rules, entry->section, entry->key) == entry)
            result.overlay_names[result.overlay_name_count++] = entry->value;
    }
    if (!ra_vfs_read(&result.vfs, "ra2.csf", &text, error) || !ra_csf_parse(&result.strings, text.view, error)) goto fail;
    ra_resource_close(&text);
    for (i = 0; i < 3; ++i)
    {
        snprintf(path, sizeof(path), "%s/%s", maps_root, archives[i]);
        if (!ra_file_open(&result.archives[i], path, error) || !ra_mix_open(&result.maps[i], result.archives[i].view, RA_HASH_CRC32, error)) goto fail;
        capacity += result.maps[i].count;
    }
    result.sources = calloc(capacity ? capacity : 1, sizeof(*result.sources));
    if (!result.sources)
    {
        ra_fail(error, RA_MEMORY, 0, "map catalogue allocation failed");
        goto fail;
    }
    for (i = 0; i < 3; ++i)
        for (j = 0; j < result.maps[i].count; ++j)
        {
            ra_view view;
            map_source *entry = &result.sources[result.source_count];
            if (!ra_mix_get_id(&result.maps[i], result.maps[i].entries[j].id, &view, error)) goto fail;
            if (!has_pack(view)) continue;
            map_name(&result, result.maps[i].entries[j].id, entry->name);
            snprintf(path, sizeof(path), "%s/%s|%s", maps_root, archives[i], entry->name);
            entry->source = ra_copy(path, strlen(path));
            if (!entry->source)
            {
                ra_fail(error, RA_MEMORY, 0, "map source allocation failed");
                goto fail;
            }
            entry->bytes = view;
            ++result.source_count;
        }
    *context = result;
    return true;
fail:
    ra_resource_close(&text);
    map_context_close(&result);
    return false;
}

bool map_theater_open(map_context *context, int theater, ra_error *error)
{
    static const char *names[] = {"temperat.ini", "snow.ini", "urban.ini"};
    static const char *palettes[] = {"isotem.pal", "isosno.pal", "isourb.pal"};
    static const char *extensions[] = {"tem", "sno", "urb"};
    map_theater result = {0};
    ra_resource text = {0};
    size_t set, i, total = 0;
    char section[32];
    if (!context || theater < 0 || theater > 2) return ra_fail(error, RA_ARGUMENT, 0, "invalid theater id");
    if (context->theaters[theater].templates) return true;
    if (!ra_vfs_read(&context->vfs, names[theater], &text, error) || !ra_ini_parse(&result.ini, text.view, text.source, error)) goto fail;
    ra_resource_close(&text);
    if (!ra_asset_palette(&context->vfs, palettes[theater], &result.palette, error)) goto fail;
    for (set = 0; set < 4096; ++set)
    {
        const ra_ini_entry *count;
        int64_t n;
        snprintf(section, sizeof(section), "TileSet%04zu", set);
        count = ra_ini_get(&result.ini, section, "TilesInSet");
        if (!count) break;
        if (!ra_ini_integer(count, &n, error) || n < 0 || n > 999 || (size_t)n > 65536 - total) goto fail;
        total += (size_t)n;
    }
    result.templates = calloc(total ? total : 1, sizeof(*result.templates));
    if (!result.templates)
    {
        ra_fail(error, RA_MEMORY, 0, "terrain catalogue allocation failed");
        goto fail;
    }
    result.count = total;
    total = 0;
    for (i = 0; i < set; ++i)
    {
        const ra_ini_entry *count, *name;
        int64_t n, number;
        snprintf(section, sizeof(section), "TileSet%04zu", i);
        count = ra_ini_get(&result.ini, section, "TilesInSet");
        name = ra_ini_get(&result.ini, section, "FileName");
        if (!ra_ini_integer(count, &n, error) || (n && (!name || strlen(name->value) > 48))) goto fail;
        for (number = 1; number <= n; ++number)
            snprintf(result.templates[total++].name, 64, "%s%02lld.%s", name->value, (long long)number, extensions[theater]);
    }
    context->theaters[theater] = result;
    return true;
fail:
    ra_resource_close(&text);
    ra_ini_close(&result.ini);
    free(result.templates);
    return false;
}

bool map_template_get(map_context *context, int theater, uint32_t id, map_template **tile, ra_error *error)
{
    map_template *entry;
    if (!map_theater_open(context, theater, error)) return false;
    /* 编辑器以 -1/65535 表示自动选取的普通地表，基础变体采用 clear01。 */
    if (id == UINT32_MAX || id == 65535) id = 0;
    if (id >= context->theaters[theater].count) return ra_fail(error, RA_NOT_FOUND, 0, "tile id %u is absent from theater", id);
    entry = &context->theaters[theater].templates[id];
    if (!entry->loaded)
    {
        if (!ra_vfs_read(&context->vfs, entry->name, &entry->resource, error)) return false;
        if (!ra_tmp_open(&entry->tmp, entry->resource.view, error))
        {
            ra_resource_close(&entry->resource);
            return false;
        }
        entry->loaded = true;
    }
    *tile = entry;
    return true;
}

void map_context_close(map_context *context)
{
    size_t i, j;
    if (!context) return;
    for (i = 0; i < 3; ++i)
    {
        map_theater *t = &context->theaters[i];
        for (j = 0; j < t->count; ++j)
        {
            ra_tmp_close(&t->templates[j].tmp);
            ra_resource_close(&t->templates[j].resource);
        }
        free(t->templates);
        ra_ini_close(&t->ini);
        ra_mix_close(&context->maps[i]);
        ra_file_close(&context->archives[i]);
    }
    for (i = 0; i < context->source_count; ++i) free(context->sources[i].source);
    free(context->sources);
    ra_csf_close(&context->strings);
    ra_ini_close(&context->missions);
    ra_ini_close(&context->rules);
    for (i = 0; i < 7; ++i) ra_mix_close(&context->terrain_archives[i]);
    ra_mix_close(&context->terrain_root);
    ra_file_close(&context->terrain_file);
    ra_vfs_close(&context->vfs);
    memset(context, 0, sizeof(*context));
}

bool map_image_bmp(const map_image *image, const char *path, ra_error *error)
{
    uint8_t header[54] = {0};
    uint32_t fields[10];
    FILE *file = NULL;
    size_t bytes = (size_t)image->width * image->height * 4;
#ifdef _WIN32
    int count = MultiByteToWideChar(CP_UTF8, MB_ERR_INVALID_CHARS, path, -1, NULL, 0);
    wchar_t *wide = count ? malloc((size_t)count * sizeof(*wide)) : NULL;
    if (wide)
    {
        MultiByteToWideChar(CP_UTF8, MB_ERR_INVALID_CHARS, path, -1, wide, count);
        file = _wfopen(wide, L"wb");
    }
    free(wide);
#else
    file = fopen(path, "wb");
#endif
    if (!file) return ra_fail(error, RA_IO, 0, "cannot create preview BMP");
    header[0] = 'B';
    header[1] = 'M';
    fields[0] = (uint32_t)bytes + 54;
    memcpy(header + 2, fields, 4);
    fields[0] = 54;
    memcpy(header + 10, fields, 4);
    fields[0] = 40;
    fields[1] = (uint32_t)image->width;
    fields[2] = (uint32_t)-image->height;
    fields[3] = 0x00200001;
    fields[4] = 0;
    fields[5] = (uint32_t)bytes;
    memcpy(header + 14, fields, 24);
    if (fwrite(header, 1, 54, file) != 54 || fwrite(image->pixels, 1, bytes, file) != bytes)
    {
        fclose(file);
        return ra_fail(error, RA_IO, 0, "preview BMP write failed");
    }
    return fclose(file) == 0 ? true : ra_fail(error, RA_IO, 0, "preview BMP close failed");
}

void map_image_close(map_image *image)
{
    if (!image) return;
    free(image->pixels);
    free(image->picked);
    memset(image, 0, sizeof(*image));
}
