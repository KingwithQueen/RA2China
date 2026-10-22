#define _CRT_SECURE_NO_WARNINGS
#include "internal.h"
#include "asset_profile.h"
#include "asset_catalog.h"
#include <stdlib.h>
#include <string.h>
#include <inttypes.h>
#include "entry.h"

static void json_bytes(const char *s, size_t length)
{
    size_t i;
    putchar('"');
    for (i = 0; i < length; ++i) {
        unsigned c = (uint8_t)s[i];
        if (c == '"' || c == '\\') printf("\\%c", c);
        else if (c < 32) printf("\\u%04x", c);
        else putchar((int)c);
    }
    putchar('"');
}

static void json_string(const char *s)
{
    json_bytes(s, strlen(s));
}

static uint64_t image_hash(uint64_t hash, const uint8_t *data, size_t size)
{
    size_t i;
    for (i = 0; i < size; ++i) hash = (hash ^ data[i]) * UINT64_C(1099511628211);
    return hash;
}

static void json_hex(ra_view bytes)
{
    size_t i;
    putchar('"');
    for (i = 0; i < bytes.size; ++i) printf("%02x", bytes.data[i]);
    putchar('"');
}

static bool reference_sample(const char *name)
{
    static const char *samples[] = {"gi.shp", "adog.shp", "mouse.shp", "harvestr.shp", "pla.shp", "plaicon.shp", "ls800cnpr.shp", "all.shp", "null.shp"};
    size_t i;
    for (i = 0; i < sizeof(samples) / sizeof(*samples); ++i) if (ra_equal(name, samples[i])) return true;
    return false;
}

static int app_main(int argc, char **argv)
{
    ra_vfs vfs = {0};
    ra_resource resource = {0};
    ra_csf csf = {0};
    ra_error error = {0};
    size_t i, images = 0, palettes = 0, frames = 0, missing = 0, failures = 0;
    bool first = true;
    bool samples = argc > 1 && !strcmp(argv[argc - 1], "--samples");
    if (samples) --argc;
    if (argc != 2 && argc != 3) {
        fputs("Usage: ra2assetcheck original-directory [china-mod-directory] [--samples]\n", stderr);
        return 2;
    }
    if (!ra_asset_mount(&vfs, argv[1], argc == 3 ? argv[2] : NULL, &error)) {
        fprintf(stderr, "%s\n", error.message);
        return 1;
    }
    fputs("{\"resources\":[", stdout);
    for (i = 0; i < sizeof(asset_names) / sizeof(*asset_names); ++i) {
        const char *name = asset_names[i];
        bool ok, pal = strstr(name, ".pal") != NULL;
        ra_shp shp = {0};
        ra_palette palette;
        uint8_t *pixels = NULL;
        uint64_t hash = UINT64_C(14695981039346656037);
        size_t n = 0, j;
        if (!ra_vfs_read(&vfs, name, &resource, &error)) {
            if (error.code == RA_NOT_FOUND) {
                ++missing;
                continue;
            }
            ok = false;
        } else if (pal) {
            ok = ra_palette_parse(&palette, resource.view, &error);
            if (ok) ++palettes;
        } else {
            ok = ra_shp_open(&shp, resource.view, &error);
            if (ok) {
                n = (size_t)shp.width * shp.height;
                pixels = malloc(n ? n : 1);
                if (!pixels) ok = ra_fail(&error, RA_MEMORY, 0, "corpus pixel allocation failed");
                for (j = 0; ok && j < shp.count; ++j) {
                    ok = ra_shp_decode(&shp, j, pixels, n, &error);
                    if (ok) hash = image_hash(hash, pixels, n);
                }
                if (ok) {
                    ++images;
                    frames += shp.count;
                }
            }
        }
        if (!first) putchar(',');
        first = false;
        fputs("{\"name\":", stdout);
        json_string(name);
        fputs(",\"source\":", stdout);
        json_string(resource.source ? resource.source : "");
        printf(",\"ok\":%s", ok ? "true" : "false");
        if (!ok) {
            ++failures;
            fputs(",\"error\":", stdout);
            json_string(error.message);
            fputs(",\"header_hex\":\"", stdout);
            for (j = 0; j < resource.view.size && j < 32; ++j) printf("%02x", resource.view.data[j]);
            putchar('"');
        } else if (!pal) {
            printf(",\"width\":%u,\"height\":%u,\"frames\":%u,\"pixel_fnv1a64\":\"%016" PRIx64 "\"", shp.width, shp.height, shp.count, hash);
            printf(",\"clipped_zero_runs\":%zu,\"short_rows\":%zu", shp.clipped_zero_runs, shp.short_rows);
        } else {
            fputs(",\"rgb_hex\":\"", stdout);
            for (j = 0; j < 256; ++j) printf("%02x%02x%02x", palette.colors[j].r, palette.colors[j].g, palette.colors[j].b);
            putchar('"');
        }
        if (samples && (pal || reference_sample(name))) {
            fputs(",\"raw_hex\":", stdout);
            json_hex(resource.view);
        }
        putchar('}');
        free(pixels);
        ra_shp_close(&shp);
        ra_resource_close(&resource);
    }
    fputs("],\"csf\":{", stdout);
    if (!ra_vfs_read(&vfs, "ra2.csf", &resource, &error) || !ra_csf_parse(&csf, resource.view, &error)) {
        ++failures;
        fputs("\"error\":", stdout);
        json_string(error.message);
    } else {
        fputs("\"source\":", stdout);
        json_string(resource.source);
        printf(",\"labels\":%zu,\"strings\":%zu,\"language\":%u,\"duplicates\":%zu,\"entries\":[", csf.label_count, csf.value_count, csf.language, csf.duplicate_count);
        for (i = 0; i < csf.label_count; ++i) {
            size_t j;
            const ra_csf_label *label = &csf.labels[i];
            if (i) putchar(',');
            fputs("{\"label\":", stdout);
            json_string(label->name);
            fputs(",\"values\":[", stdout);
            for (j = 0; j < label->value_count; ++j) {
                const ra_csf_value *value = &csf.values[label->first_value + j];
                if (j) putchar(',');
                json_bytes(value->text, value->length);
            }
            fputs("]}", stdout);
        }
        putchar(']');
        if (samples) {
            fputs(",\"raw_hex\":", stdout);
            json_hex(resource.view);
        }
    }
    printf("},\"summary\":{\"shp_files\":%zu,\"pal_files\":%zu,\"frames\":%zu,\"catalog_absent\":%zu,\"failures\":%zu}}\n", images, palettes, frames, missing, failures);
    ra_csf_close(&csf);
    ra_resource_close(&resource);
    ra_vfs_close(&vfs);
    return failures ? 1 : 0;
}
