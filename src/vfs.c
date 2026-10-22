#include "internal.h"
#include <stdlib.h>
#include <string.h>

struct ra_mount {
    char *source;
    int priority;
    bool directory;
    ra_file file;
    ra_mix mix;
};

static void mount_close(ra_mount *mount)
{ free(mount->source); ra_mix_close(&mount->mix); ra_file_close(&mount->file); memset(mount, 0, sizeof(*mount)); }

static bool add_mount(ra_vfs *vfs, ra_mount *mount, ra_error *error)
{
    size_t at;
    if (vfs->count == vfs->capacity) {
        size_t cap = vfs->capacity ? vfs->capacity*2 : 8;
        ra_mount *p;
        if (cap < vfs->capacity || cap > SIZE_MAX/sizeof(*p)) return ra_fail(error, RA_MEMORY, 0, "too many mounts");
        p = realloc(vfs->mounts, cap*sizeof(*p));
        if (!p) return ra_fail(error, RA_MEMORY, 0, "mount allocation failed");
        vfs->mounts = p; vfs->capacity = cap;
    }
    /* Ordered high to low; insert before equal priority so newest wins. */
    at = 0;
    while (at < vfs->count && vfs->mounts[at].priority > mount->priority) ++at;
    memmove(vfs->mounts+at+1, vfs->mounts+at, (vfs->count-at)*sizeof(*vfs->mounts));
    vfs->mounts[at] = *mount; ++vfs->count;
    return true;
}

bool ra_vfs_mount_mix(ra_vfs *vfs, const char *spec, int priority, ra_hash_kind kind, ra_error *error)
{
    ra_mount mount = {0};
    char *parts, *next, *cursor;
    bool ok = false;
    if (!vfs || !spec || !*spec) return ra_fail(error, RA_ARGUMENT, 0, "invalid MIX mount");
    parts = ra_copy(spec, strlen(spec)); mount.source = ra_copy(spec, strlen(spec));
    if (!parts || !mount.source) { free(parts); mount_close(&mount); return ra_fail(error, RA_MEMORY, 0, "mount name allocation failed"); }
    next = strchr(parts, '|');
    if (next) *next++ = 0;
    if (!ra_file_open(&mount.file, parts, error)) goto done;
    if (!ra_mix_open(&mount.mix, mount.file.view, kind, error)) goto done;
    while (next) {
        ra_view child;
        ra_mix nested = {0};
        cursor = next; next = strchr(cursor, '|');
        if (next) *next++ = 0;
        if (!*cursor) { ra_fail(error, RA_ARGUMENT, 0, "empty nested MIX name"); goto done; }
        if (!ra_mix_get(&mount.mix, cursor, &child, error) || !ra_mix_open(&nested, child, kind, error)) goto done;
        ra_mix_close(&mount.mix); mount.mix = nested;
    }
    mount.priority = priority;
    ok = add_mount(vfs, &mount, error);
done:
    free(parts);
    if (!ok) mount_close(&mount);
    return ok;
}

bool ra_vfs_mount_directory(ra_vfs *vfs, const char *directory, int priority, ra_error *error)
{
    ra_mount mount = {0};
    if (!vfs || !directory || !*directory) return ra_fail(error, RA_ARGUMENT, 0, "invalid directory mount");
    if (!ra_directory_exists(directory)) return ra_fail(error, RA_NOT_FOUND, 0, "directory not found: %s", directory);
    mount.source = ra_copy(directory, strlen(directory)); mount.priority = priority; mount.directory = true;
    if (!mount.source) return ra_fail(error, RA_MEMORY, 0, "directory name allocation failed");
    if (!add_mount(vfs, &mount, error)) { mount_close(&mount); return false; }
    return true;
}

static bool relative_name(const char *name)
{
    const char *p = name, *segment = name;
    if (!*name) return false;
    for (;;) {
        unsigned c = (uint8_t)*p;
        if (c == ':' || c == '*' || c == '?' || c == '"' || c == '<' || c == '>' || c == '|' || (c && c < 32)) return false;
        if (!c || c == '/' || c == '\\') {
            size_t length = (size_t)(p-segment);
            if (!length || (length == 1 && segment[0] == '.') ||
                (length == 2 && segment[0] == '.' && segment[1] == '.')) return false;
            if (segment[length-1] == '.' || segment[length-1] == ' ') return false;
            if (!c) break;
            segment = p+1;
        }
        ++p;
    }
    return true;
}

static char *join_source(const char *a, const char *b, char separator)
{
    size_t na = strlen(a), nb = strlen(b);
    char *p;
    if (nb > SIZE_MAX-2 || na > SIZE_MAX-nb-2) return NULL;
    p = malloc(na+nb+2);
    if (p) { memcpy(p, a, na); p[na] = separator; memcpy(p+na+1, b, nb+1); }
    return p;
}

bool ra_vfs_read(const ra_vfs *vfs, const char *name, ra_resource *resource, ra_error *error)
{
    size_t i;
    if (!vfs || !name || !resource || !relative_name(name))
        return ra_fail(error, RA_ARGUMENT, 0, "resource name must be a relative path without . or .. segments");
    for (i = 0; i < vfs->count; ++i) {
        const ra_mount *mount = vfs->mounts+i;
        ra_resource out = {0};
        ra_error local = {0};
        out.priority = mount->priority;
        if (mount->directory) {
            out.source = join_source(mount->source, name, '/');
            if (!out.source) return ra_fail(error, RA_MEMORY, 0, "resource name allocation failed");
            if (!ra_file_open(&out.loose_file, out.source, &local)) {
                free(out.source);
                if (local.code == RA_NOT_FOUND) continue;
                if (error) *error = local;
                return false;
            }
            out.view = out.loose_file.view;
        } else {
            if (!ra_mix_get(&mount->mix, name, &out.view, &local)) {
                if (local.code == RA_NOT_FOUND) continue;
                if (error) *error = local;
                return false;
            }
            out.source = join_source(mount->source, name, '|');
            if (!out.source) return ra_fail(error, RA_MEMORY, 0, "resource name allocation failed");
        }
        *resource = out;
        return true;
    }
    return ra_fail(error, RA_NOT_FOUND, 0, "resource not found: %s", name);
}
void ra_resource_close(ra_resource *resource)
{
    if (!resource) return;
    ra_file_close(&resource->loose_file); free(resource->source); memset(resource, 0, sizeof(*resource));
}
void ra_vfs_close(ra_vfs *vfs)
{
    size_t i;
    if (!vfs) return;
    for (i = 0; i < vfs->count; ++i) mount_close(vfs->mounts+i);
    free(vfs->mounts); memset(vfs, 0, sizeof(*vfs));
}
