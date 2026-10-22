#include "internal.h"
#include "asset_profile.h"
#include <stdlib.h>
#include <string.h>

static bool mount_at(ra_vfs *vfs, const char *root, const char *tail, int priority, ra_error *error)
{
    size_t a = strlen(root), b = strlen(tail);
    char *path;
    bool ok;
    if (a > SIZE_MAX - b - 2) return ra_fail(error, RA_RANGE, 0, "asset path is too long");
    path = malloc(a + b + 2);
    if (!path) return ra_fail(error, RA_MEMORY, 0, "asset path allocation failed");
    snprintf(path, a + b + 2, "%s/%s", root, tail);
    ok = ra_vfs_mount_mix(vfs, path, priority, RA_HASH_CRC32, error);
    free(path);
    return ok;
}

bool ra_asset_mount(ra_vfs *vfs, const char *original, const char *mod, ra_error *error)
{
    static const char *packages[] = {"cache.mix", "conquer.mix", "generic.mix", "local.mix", "temperat.mix", "snow.mix", "urban.mix"};
    ra_vfs result = {0};
    size_t i;
    char tail[128];
    if (!vfs || !original) return ra_fail(error, RA_ARGUMENT, 0, "asset mount requires a VFS and original directory");
    for (i = 0; i < sizeof(packages) / sizeof(*packages); ++i) {
        snprintf(tail, sizeof(tail), "ra2.mix|%s", packages[i]);
        if (!mount_at(&result, original, tail, 10 + (int)i, error)) goto fail;
    }
    if (!mount_at(&result, original, "LANGUAGE.MIX|cameo.mix", 30, error)) goto fail;
    if (!mount_at(&result, original, "LANGUAGE.MIX", 40, error)) goto fail;
    if (!ra_vfs_mount_directory(&result, original, 50, error)) goto fail;
    if (mod) {
        if (!mount_at(&result, mod, "ecache91.mix", 100, error)) goto fail;
        if (!ra_vfs_mount_directory(&result, mod, 200, error)) goto fail;
    }
    *vfs = result;
    return true;
fail:
    ra_vfs_close(&result);
    return false;
}

bool ra_asset_palette(const ra_vfs *vfs, const char *name, ra_palette *palette, ra_error *error)
{
    ra_resource resource = {0};
    bool ok = ra_vfs_read(vfs, name, &resource, error) && ra_palette_parse(palette, resource.view, error);
    ra_resource_close(&resource);
    return ok;
}
