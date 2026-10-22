#define _CRT_SECURE_NO_WARNINGS
#include "internal.h"
#include "ra2/rules.h"
#include <limits.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include "entry.h"

static void json_string(FILE *f, const char *s)
{
    ra_view bytes = {(const uint8_t *)s, strlen(s)};
    bool utf8 = ra_utf8_valid(bytes);
    fputc('"', f);
    while (*s) {
        unsigned c = (uint8_t)*s++;
        if (c == '"' || c == '\\') { fputc('\\', f); fputc((int)c, f); }
        else if (c < 32 || (!utf8 && c >= 128)) fprintf(f, "\\u%04x", c);
        else fputc((int)c, f);
    }
    fputc('"', f);
}
static int failure(const ra_error *error)
{
    fputs("{\"error\":", stderr); json_string(stderr, ra_status_name(error->code));
    fprintf(stderr, ",\"line\":%zu,\"message\":", error->line);
    json_string(stderr, error->message); fputs("}\n", stderr);
    return error->code == RA_NOT_FOUND ? 3 : 1;
}
static bool inspect_open(const char *spec, ra_hash_kind kind, ra_file *file, ra_mix *mix, ra_error *error)
{
    char *parts = ra_copy(spec, strlen(spec)), *next, *cursor;
    bool ok = false;
    if (!parts) return ra_fail(error, RA_MEMORY, 0, "spec allocation failed");
    next = strchr(parts, '|'); if (next) *next++ = 0;
    if (!ra_file_open(file, parts, error) || !ra_mix_open(mix, file->view, kind, error)) goto done;
    while (next) {
        ra_view view;
        ra_mix child = {0};
        cursor = next; next = strchr(cursor, '|'); if (next) *next++ = 0;
        if (!*cursor) { ra_fail(error, RA_ARGUMENT, 0, "empty nested MIX name"); goto done; }
        if (!ra_mix_get(mix, cursor, &view, error) || !ra_mix_open(&child, view, kind, error)) goto done;
        ra_mix_close(mix); *mix = child;
    }
    ok = true;
done:
    free(parts); return ok;
}
static bool mount_args(ra_vfs *vfs, int argc, char **argv, int start, ra_error *error)
{
    int i;
    ra_hash_kind kind = RA_HASH_CRC32;
    for (i = start; i < argc; ++i) if (!strcmp(argv[i], "--classic")) kind = RA_HASH_CLASSIC;
    for (i = start; i < argc; ++i) {
        bool directory;
        long priority;
        char *end;
        if (!strcmp(argv[i], "--classic")) continue;
        directory = !strcmp(argv[i], "--dir");
        if (!directory && strcmp(argv[i], "--mix")) return ra_fail(error, RA_ARGUMENT, 0, "unknown mount option: %s", argv[i]);
        if (argc-i < 3) return ra_fail(error, RA_ARGUMENT, 0, "mount requires priority and path/spec");
        errno = 0; priority = strtol(argv[i+1], &end, 10);
        if (errno || *end || end == argv[i+1] || priority < INT_MIN || priority > INT_MAX)
            return ra_fail(error, RA_ARGUMENT, 0, "invalid mount priority");
        if (directory) {
            if (!ra_vfs_mount_directory(vfs, argv[i+2], (int)priority, error)) return false;
        } else if (!ra_vfs_mount_mix(vfs, argv[i+2], (int)priority, kind, error)) return false;
        i += 2;
    }
    return true;
}
static void ini_summary(const ra_ini *ini)
{
    size_t i;
    fputs("{\"source\":", stdout); json_string(stdout, ini->source);
    fputs(",\"encoding\":", stdout); json_string(stdout, ini->encoding);
    printf(",\"section_declarations\":%zu,\"entries\":%zu,\"duplicates\":%zu,\"ignored_lines\":[",
           ini->section_count, ini->entry_count, ini->duplicate_count);
    for (i = 0; i < ini->ignored_count; ++i) {
        printf("%s{\"line\":%zu,\"text\":", i ? "," : "", ini->ignored_lines[i].line);
        json_string(stdout, ini->ignored_lines[i].text); fputc('}', stdout);
    }
    puts("]}");
}
static void help(void)
{
    puts("ra2tool - read-only C17 resource tools\n"
         "  mix <archive[|nested.mix...]> [--classic]\n"
         "  ini <file>\n"
         "  resolve <resource> [mounts]\n"
         "  scan-ini <resource> [mounts]\n"
         "  query <resource> <section> <key> [mounts]\n"
         "  compare <resource> <expected-file> [mounts]\n"
         "  rules-check [--strict] [mounts]\n"
         "Mounts: --mix <priority> <archive[|nested.mix...]>\n"
         "        --dir <priority> <directory> [--classic]\n"
         "Higher priority wins; equal priority uses the last mounted source.\n"
         "Paths use UTF-8. Quote specs containing | in the shell. Output is JSON.");
}

/* 规则检查复用现有挂载顺序；严格模式仅改变发现问题后的退出码。 */
static int rules_command(int argc, char **argv)
{
    ra_vfs vfs = {0};
    ra_resource logic_resource = {0};
    ra_resource art_resource = {0};
    ra_ini logic = {0};
    ra_ini art = {0};
    ra_rules rules = {0};
    ra_error error = {0};
    char **mounts = malloc((size_t)argc * sizeof(*mounts));
    int mount_count = 0;
    int result = 1;
    int i;
    bool strict = false;
    bool art_loaded = false;
    if (!mounts) {
        ra_fail(&error, RA_MEMORY, 0, "command argument allocation failed");
        return failure(&error);
    }
    for (i = 2; i < argc; ++i) {
        if (!strcmp(argv[i], "--strict")) strict = true;
        else mounts[mount_count++] = argv[i];
    }
    if (!mount_args(&vfs, mount_count, mounts, 0, &error)) goto done;
    if (!ra_vfs_read(&vfs, "rules.ini", &logic_resource, &error)) goto done;
    if (!ra_ini_parse(&logic, logic_resource.view, logic_resource.source, &error)) goto done;
    art_loaded = ra_vfs_read(&vfs, "art.ini", &art_resource, &error);
    if (!art_loaded && error.code != RA_NOT_FOUND) goto done;
    if (art_loaded && !ra_ini_parse(&art, art_resource.view, art_resource.source, &error)) goto done;
    if (!ra_rules_build(&rules, &logic, art_loaded ? &art : NULL, &error)) goto done;
    if (!ra_rules_write_json(&rules, stdout, &error)) goto done;
    result = strict && ra_rules_has_errors(&rules) ? 2 : 0;
done:
    if (result == 1) failure(&error);
    free(mounts);
    ra_rules_close(&rules);
    ra_ini_close(&art);
    ra_ini_close(&logic);
    ra_resource_close(&art_resource);
    ra_resource_close(&logic_resource);
    ra_vfs_close(&vfs);
    return result;
}
static int app_main(int argc, char **argv)
{
    ra_error error = {0};
    if (argc == 1 || !strcmp(argv[1], "--help")) { help(); return 0; }
    if (!strcmp(argv[1], "rules-check")) return rules_command(argc, argv);
    if (!strcmp(argv[1], "mix")) {
        ra_file file = {0}; ra_mix mix = {0}; size_t i;
        bool ok;
        if (argc < 3 || argc > 4 || (argc == 4 && strcmp(argv[3], "--classic"))) {
            ra_fail(&error, RA_ARGUMENT, 0, "mix requires spec and optional --classic"); return failure(&error);
        }
        ok = inspect_open(argv[2], argc == 4 ? RA_HASH_CLASSIC : RA_HASH_CRC32, &file, &mix, &error);
        if (ok) {
            fputs("{\"source\":", stdout); json_string(stdout, argv[2]);
            printf(",\"flags\":%u,\"encrypted\":%s,\"checksum_present\":%s,\"checksum_verified\":%s,\"data_offset\":%zu,\"data_size\":%u,\"count\":%zu,\"entries\":[",
                mix.flags, mix.flags & 0x20000 ? "true" : "false", mix.flags & 0x10000 ? "true" : "false",
                mix.checksum_verified ? "true" : "false", mix.data_offset, mix.data_size, mix.count);
            for (i = 0; i < mix.count; ++i) printf("%s{\"id\":\"%08x\",\"offset\":%u,\"size\":%u}",
                i ? "," : "", mix.entries[i].id, mix.entries[i].offset, mix.entries[i].size);
            puts("]}");
        }
        ra_mix_close(&mix); ra_file_close(&file); return ok ? 0 : failure(&error);
    }
    if (!strcmp(argv[1], "ini")) {
        ra_file file = {0}; ra_ini ini = {0}; bool ok;
        if (argc != 3) { ra_fail(&error, RA_ARGUMENT, 0, "ini requires a file"); return failure(&error); }
        ok = ra_file_open(&file, argv[2], &error) && ra_ini_parse(&ini, file.view, argv[2], &error);
        if (ok) ini_summary(&ini);
        ra_ini_close(&ini); ra_file_close(&file); return ok ? 0 : failure(&error);
    }
    {
        bool query = !strcmp(argv[1], "query"), compare = !strcmp(argv[1], "compare");
        bool scan = !strcmp(argv[1], "scan-ini"), resolve = !strcmp(argv[1], "resolve"), ok;
        int start = query ? 5 : compare ? 4 : 3;
        ra_vfs vfs = {0}; ra_resource resource = {0}; ra_ini ini = {0}; ra_file expected = {0};
        if ((!query && !compare && !scan && !resolve) || argc < start) {
            ra_fail(&error, RA_ARGUMENT, 0, "unknown command or missing arguments; use --help"); return failure(&error);
        }
        ok = mount_args(&vfs, argc, argv, start, &error) && ra_vfs_read(&vfs, argv[2], &resource, &error);
        if (ok && (query || scan)) ok = ra_ini_parse(&ini, resource.view, resource.source, &error);
        if (ok && query) {
            const ra_ini_entry *entry = ra_ini_get(&ini, argv[3], argv[4]);
            if (!entry) ok = ra_fail(&error, RA_NOT_FOUND, 0, "INI key not found: [%s] %s", argv[3], argv[4]);
            else {
                fputs("{\"source\":", stdout); json_string(stdout, resource.source);
                printf(",\"priority\":%d,\"line\":%zu,\"ignored_lines\":%zu,\"section\":", resource.priority, entry->line, ini.ignored_count); json_string(stdout, entry->section);
                fputs(",\"key\":", stdout); json_string(stdout, entry->key); fputs(",\"value\":", stdout); json_string(stdout, entry->value); puts("}");
            }
        } else if (ok && scan) ini_summary(&ini);
        else if (ok && compare) {
            ok = ra_file_open(&expected, argv[3], &error);
            if (ok && (expected.view.size != resource.view.size ||
                (resource.view.size && memcmp(expected.view.data, resource.view.data, resource.view.size))))
                ok = ra_fail(&error, RA_FORMAT, 0, "resource bytes differ from reference");
            if (ok) { fputs("{\"equal\":true,\"source\":", stdout); json_string(stdout, resource.source); printf(",\"bytes\":%zu}\n", resource.view.size); }
        } else if (ok) {
            uint8_t digest[20]; char hex[41]; ra_sha1(resource.view, digest); ra_hex(digest, 20, hex);
            fputs("{\"source\":", stdout); json_string(stdout, resource.source);
            printf(",\"priority\":%d,\"bytes\":%zu,\"sha1\":\"%s\"}\n", resource.priority, resource.view.size, hex);
        }
        ra_file_close(&expected); ra_ini_close(&ini); ra_resource_close(&resource); ra_vfs_close(&vfs);
        return ok ? 0 : failure(&error);
    }
}
