#define _CRT_SECURE_NO_WARNINGS
#include "internal.h"
#include "voxel_scene.h"
#include "voxel_catalog.h"
#include <inttypes.h>
#include <stdlib.h>
#include <string.h>
#include "entry.h"

static void json_string(const char *text)
{
    putchar('"');
    while (*text) {
        unsigned c = (uint8_t)*text++;
        if (c == '"' || c == '\\') printf("\\%c", c);
        else if (c < 32) printf("\\u%04x", c);
        else putchar((int)c);
    }
    putchar('"');
}

static void json_hex(ra_view bytes)
{
    size_t i;
    putchar('"');
    for (i = 0; i < bytes.size; ++i) printf("%02x", bytes.data[i]);
    putchar('"');
}

static uint64_t hash_bytes(uint64_t hash, const void *data, size_t size)
{
    const uint8_t *bytes = data;
    size_t i;
    for (i = 0; i < size; ++i) hash = (hash ^ bytes[i]) * UINT64_C(1099511628211);
    return hash;
}

static bool sample_name(const char *name)
{
    static const char *bases[] = {"htnk", "mtnk", "carrier", "beag", "shad", "hmec", "voxels"};
    size_t i;
    for (i = 0; i < sizeof(bases) / sizeof(*bases); ++i) if (!strncmp(name, bases[i], strlen(bases[i])) && name[strlen(bases[i])] == '.') return true;
    return false;
}

static int app_main(int argc, char **argv)
{
    voxel_context context = {0};
    ra_error error = {0};
    size_t i, vxl_count = 0, hva_count = 0, vpl_count = 0, total_voxels = 0, total_frames = 0, failures = 0, bindings = 0, binding_issues = 0;
    bool samples = argc > 1 && !strcmp(argv[argc - 1], "--samples");
    if (samples) --argc;
    if (argc >= 4 && !strcmp(argv[1], "--dump")) {
        ra_vfs vfs = {0};
        ra_resource bytes = {0};
        bool ok = ra_asset_mount(&vfs, argv[3], argc == 5 ? argv[4] : NULL, &error) && ra_vfs_read(&vfs, argv[2], &bytes, &error);
        if (ok) {
            fputs("{\"raw_hex\":", stdout);
            json_hex(bytes.view);
            puts("}");
        } else fprintf(stderr, "%s\n", error.message);
        ra_resource_close(&bytes);
        ra_vfs_close(&vfs);
        return ok ? 0 : 1;
    }
    if (argc != 2 && argc != 3) {
        fputs("Usage: ra2voxelcheck original-directory [mod-directory] [--samples]\n", stderr);
        return 2;
    }
    if (!voxel_context_open(&context, argv[1], argc == 3 ? argv[2] : NULL, &error)) {
        fprintf(stderr, "%s\n", error.message);
        return 1;
    }
    fputs("{\"resources\":[", stdout);
    for (i = 0; i < sizeof(voxel_names) / sizeof(*voxel_names); ++i) {
        ra_resource resource = {0};
        ra_vxl vxl = {0};
        ra_hva hva = {0};
        ra_vpl vpl = {0};
        const char *name = voxel_names[i], *extension = strrchr(name, '.');
        bool ok = ra_vfs_read(&context.vfs, name, &resource, &error);
        uint64_t hash = UINT64_C(14695981039346656037);
        size_t j;
        if (i) putchar(',');
        fputs("{\"name\":", stdout);
        json_string(name);
        fputs(",\"source\":", stdout);
        json_string(resource.source ? resource.source : "");
        if (ok && !strcmp(extension, ".vxl")) {
            ok = ra_vxl_parse(&vxl, resource.view, &error);
            if (ok) {
                char base[256];
                voxel_model paired = {0};
                ++vxl_count;
                total_voxels += vxl.voxel_count;
                printf(",\"sections\":%zu,\"voxels\":%zu,\"limbs\":[", vxl.section_count, vxl.voxel_count);
                for (j = 0; j < vxl.section_count; ++j) {
                    const ra_vxl_section *section = &vxl.sections[j];
                    hash = hash_bytes(hash, section->voxels, section->voxel_count * sizeof(*section->voxels));
                    if (j) putchar(',');
                    fputs("{\"name\":", stdout);
                    json_string(section->name);
                    printf(",\"count\":%zu,\"normal_type\":%u,\"unmapped_normals\":%zu}", section->voxel_count, section->normal_type, section->unmapped_normals);
                }
                printf("],\"voxel_fnv1a64\":\"%016" PRIx64 "\"", hash);
                snprintf(base, sizeof(base), "%.*s", (int)(extension - name), name);
                if (voxel_model_load(&paired, &context.vfs, base, &error)) {
                    ++bindings;
                    fputs(",\"binding\":true", stdout);
                    printf(",\"binding_by_index\":%s", paired.index_binding ? "true" : "false");
                    if (samples && sample_name(name)) {
                        size_t s, f;
                        bool first = true;
                        fputs(",\"transform_probes\":[", stdout);
                        for (s = 0; s < paired.vxl.section_count; ++s) {
                            const ra_vxl_section *section = &paired.vxl.sections[s];
                            float point[3] = {section->size[0] * 0.5f, section->size[1] * 0.5f, section->size[2] * 0.5f};
                            for (f = 0; f < paired.hva.frame_count; ++f) {
                                float output[3];
                                const float *matrix = paired.hva.matrices + (f * paired.hva.section_count + paired.mapping[s]) * 12;
                                if (!ra_voxel_transform(section, matrix, point, output, &error)) {
                                    ok = false;
                                    break;
                                }
                                if (!first) putchar(',');
                                first = false;
                                printf("{\"section\":%zu,\"frame\":%zu,\"input\":[%.9g,%.9g,%.9g],\"output\":[%.9g,%.9g,%.9g]}",
                                    s, f, point[0], point[1], point[2], output[0], output[1], output[2]);
                            }
                        }
                        putchar(']');
                    }
                } else {
                    ++binding_issues;
                    fputs(",\"binding\":false", stdout);
                    fputs(",\"binding_issue\":", stdout);
                    json_string(error.message);
                }
                voxel_model_close(&paired);
            }
        } else if (ok && !strcmp(extension, ".hva")) {
            ok = ra_hva_parse(&hva, resource.view, &error);
            if (ok) {
                ++hva_count;
                total_frames += hva.frame_count;
                printf(",\"frames\":%zu,\"sections\":%zu", hva.frame_count, hva.section_count);
                hash = hash_bytes(hash, hva.matrices, hva.frame_count * hva.section_count * 48);
                printf(",\"matrix_fnv1a64\":\"%016" PRIx64 "\"", hash);
            }
        } else if (ok) {
            ok = ra_vpl_parse(&vpl, resource.view, &error);
            if (ok) {
                ++vpl_count;
                printf(",\"shades\":%u,\"remap_start\":%u,\"remap_end\":%u", vpl.section_count, vpl.remap_start, vpl.remap_end);
                for (j = 0; j < (size_t)vpl.section_count * 256; ++j) {
                    uint8_t mapped;
                    if (!ra_vpl_lookup(&vpl, j / 256, (uint8_t)(j % 256), &mapped, &error)) {
                        ok = false;
                        break;
                    }
                    hash = hash_bytes(hash, &mapped, 1);
                }
                printf(",\"table_fnv1a64\":\"%016" PRIx64 "\"", hash);
            }
        }
        printf(",\"ok\":%s", ok ? "true" : "false");
        if (!ok) {
            ++failures;
            fputs(",\"error\":", stdout);
            json_string(error.message);
        }
        if (samples && sample_name(name)) {
            fputs(",\"raw_hex\":", stdout);
            json_hex(resource.view);
        }
        putchar('}');
        ra_vxl_close(&vxl);
        ra_hva_close(&hva);
        ra_resource_close(&resource);
    }
    fputs("],\"scenes\":[", stdout);
    {
        static const char *original[] = {"HTNK", "MTNK", "CARRIER", "BEAG", "SHAD", "hmec.vxl"};
        static const char *china[] = {"CNLTNK", "CNAPOC", "CARRIER2", "J10", "SEEK", "hmec.vxl"};
        const char **names = argc == 3 ? china : original;
        size_t n;
        for (n = 0; n < 6; ++n) {
            voxel_scene scene = {0};
            ra_voxel_image image = {0};
            ra_voxel_camera camera = {45, 30, 1, 225, true, true, {235,65,55}, -1, 0, 0, 0, false};
            bool ok = voxel_scene_load(&scene, &context, names[n], true, &error) && ra_voxel_image_create(&image, 256, 192, &error);
            size_t f, views = 0;
            uint64_t hash = UINT64_C(14695981039346656037);
            if (n) putchar(',');
            fputs("{\"id\":", stdout);
            json_string(names[n]);
            fputs(",\"image\":", stdout);
            json_string(scene.image);
            printf(",\"parts\":%zu,\"frames\":%zu", scene.count, scene.frames);
            for (f = 0; ok && f < scene.frames + 3; ++f) {
                camera.yaw = f < scene.frames ? 45 : (float)(f - scene.frames + 1) * 90;
                ok = ra_voxel_render(scene.parts, scene.count, f % scene.frames, &context.palette, &context.vpl, &camera, &image, &error);
                if (ok && !image.drawn_pixels) ok = ra_fail(&error, RA_FORMAT, 0, "voxel scene rendered no visible pixels");
                if (ok) {
                    ++views;
                    hash = hash_bytes(hash, image.pixels, image.width * image.height * 4);
                }
            }
            printf(",\"views\":%zu,\"render_fnv1a64\":\"%016" PRIx64 "\",\"ok\":%s", views, hash, ok ? "true" : "false");
            if (!ok) {
                ++failures;
                fputs(",\"error\":", stdout);
                json_string(error.message);
            }
            putchar('}');
            ra_voxel_image_close(&image);
            voxel_scene_close(&scene);
        }
    }
    printf("],\"summary\":{\"vxl\":%zu,\"hva\":%zu,\"vpl\":%zu,\"bindings\":%zu,\"binding_issues\":%zu,\"voxels\":%zu,\"hva_frames\":%zu,\"failures\":%zu}}\n",
        vxl_count, hva_count, vpl_count, bindings, binding_issues, total_voxels, total_frames, failures);
    voxel_context_close(&context);
    return failures ? 1 : 0;
}
