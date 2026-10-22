#define _CRT_SECURE_NO_WARNINGS
#include "internal.h"
#include <stdlib.h>
#include <string.h>
#include "crypto_fixture.h"
#include "entry.h"

static unsigned checks, failures;
#define CHECK(expr)                                                                                                                                            \
    do                                                                                                                                                         \
    {                                                                                                                                                          \
        ++checks;                                                                                                                                              \
        if (!(expr))                                                                                                                                           \
        {                                                                                                                                                      \
            ++failures;                                                                                                                                        \
            fprintf(stderr, "FAIL %s:%d: %s\n", __FILE__, __LINE__, #expr);                                                                                    \
            return;                                                                                                                                            \
        }                                                                                                                                                      \
    } while (0)
static ra_view text_view(const char *text)
{
    ra_view view = {(const uint8_t *)text, strlen(text)};
    return view;
}
static void put16(uint8_t *p, uint16_t x)
{
    p[0] = (uint8_t)x;
    p[1] = (uint8_t)(x >> 8);
}
static void put32(uint8_t *p, uint32_t x)
{
    unsigned i;
    for (i = 0; i < 4; ++i) p[i] = (uint8_t)(x >> (i * 8));
}

static void crypto_tests(void)
{
    uint8_t digest[20], key[56], zero[8] = {0}, cipher[8] = {0x4e, 0xf9, 0x97, 0x45, 0x61, 0x98, 0xdd, 0x78};
    uint8_t ff[8], other[8] = {0x51, 0x86, 0x6f, 0xd5, 0xb8, 0x5e, 0xcb, 0x8a};
    char hex[41];
    ra_blowfish bf;
    uint8_t *million = malloc(1000000);
    ra_view big_input;
    CHECK(million != NULL);
    ra_sha1(text_view(""), digest);
    ra_hex(digest, 20, hex);
    CHECK(!strcmp(hex, "da39a3ee5e6b4b0d3255bfef95601890afd80709"));
    ra_sha1(text_view("abc"), digest);
    ra_hex(digest, 20, hex);
    CHECK(!strcmp(hex, "a9993e364706816aba3e25717850c26c9cd0d89d"));
    ra_sha1(text_view("abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq"), digest);
    ra_hex(digest, 20, hex);
    CHECK(!strcmp(hex, "84983e441c3bd26ebaae4aa1f95129e5e54670f1"));
    memset(million, 'a', 1000000);
    big_input.data = million;
    big_input.size = 1000000;
    ra_sha1(big_input, digest);
    ra_hex(digest, 20, hex);
    free(million);
    CHECK(!strcmp(hex, "34aa973cd4c4daa4f61eeb2bdbad27316534016f"));
    ra_blowfish_init(&bf, zero, 8);
    ra_blowfish_decrypt(&bf, cipher);
    CHECK(!memcmp(cipher, zero, 8));
    memset(ff, 255, sizeof(ff));
    ra_blowfish_init(&bf, ff, 8);
    ra_blowfish_decrypt(&bf, other);
    CHECK(!memcmp(other, ff, 8));
    ra_mix_key(encrypted_fixture + 4, key);
    CHECK(!memcmp(key, rsa_expected, 56));
    CHECK(ra_mix_id("local.mix", RA_HASH_CRC32) == 0xa8548fd9u);
    CHECK(ra_mix_id("SMCV.VXL", RA_HASH_CRC32) == 0x801c2db4u);
    CHECK(ra_mix_id("smcv.vxl", RA_HASH_CRC32) == 0x801c2db4u);
    CHECK(ra_mix_id("ABCD", RA_HASH_CLASSIC) == 0x44434241u);
    CHECK(ra_mix_id("ABCDE", RA_HASH_CLASSIC) == 0x888684c7u);
}

static size_t simple_mix(uint8_t bytes[64], bool modern, bool checksum)
{
    size_t h = modern ? 4 : 0, end;
    memset(bytes, 0, 64);
    if (modern) put32(bytes, checksum ? 0x10000u : 0);
    put16(bytes + h, 2);
    put32(bytes + h + 2, 3);
    put32(bytes + h + 6, 0xf0000001u);
    put32(bytes + h + 10, 2);
    put32(bytes + h + 14, 1);
    put32(bytes + h + 18, 0x12345678u);
    put32(bytes + h + 22, 0);
    put32(bytes + h + 26, 2);
    memcpy(bytes + h + 30, "abc", 3);
    end = h + 33;
    if (checksum)
    {
        ra_view body = {bytes + h + 30, 3};
        ra_sha1(body, bytes + end);
        end += 20;
    }
    return end;
}
static void mix_tests(void)
{
    uint8_t bytes[64], altered[sizeof(encrypted_fixture)];
    size_t size, i;
    ra_mix mix = {0};
    ra_view input, result;
    ra_error error = {0};
    input.data = encrypted_fixture;
    input.size = sizeof(encrypted_fixture);
    CHECK(ra_mix_open(&mix, input, RA_HASH_CRC32, &error));
    CHECK(mix.count == 1 && mix.flags == 0x20000 && mix.data_size == 3);
    CHECK(ra_mix_get_id(&mix, 0x12345678, &result, &error));
    CHECK(result.size == 3 && !memcmp(result.data, "abc", 3));
    CHECK(!ra_mix_get_id(&mix, 7, &result, &error) && error.code == RA_NOT_FOUND);
    ra_mix_close(&mix);
    for (i = 0; i < sizeof(encrypted_fixture); ++i)
    {
        input.size = i;
        CHECK(!ra_mix_open(&mix, input, RA_HASH_CRC32, &error));
        CHECK(mix.entries == NULL);
    }
    memcpy(altered, encrypted_fixture, sizeof(altered));
    altered[0] = 0;
    altered[3] = 8;
    input.data = altered;
    input.size = sizeof(altered);
    CHECK(!ra_mix_open(&mix, input, RA_HASH_CRC32, &error));
    size = simple_mix(bytes, false, false);
    input.data = bytes;
    input.size = size;
    CHECK(ra_mix_open(&mix, input, RA_HASH_CRC32, &error));
    CHECK(mix.count == 2 && mix.entries[0].id == 0x12345678 && mix.data_offset == 30);
    CHECK(ra_mix_get_id(&mix, 0xf0000001u, &result, &error));
    CHECK(result.size == 1 && result.data[0] == 'c');
    ra_mix_close(&mix);
    for (i = 0; i < size; ++i)
    {
        input.size = i;
        CHECK(!ra_mix_open(&mix, input, RA_HASH_CRC32, &error));
    }
    input.size = size;
    put32(bytes + 10, 0xffffffffu);
    CHECK(!ra_mix_open(&mix, input, RA_HASH_CRC32, &error));
    size = simple_mix(bytes, true, true);
    input.size = size;
    CHECK(ra_mix_open(&mix, input, RA_HASH_CRC32, &error));
    CHECK(mix.checksum_verified);
    ra_mix_close(&mix);
    bytes[34] ^= 1;
    CHECK(!ra_mix_open(&mix, input, RA_HASH_CRC32, &error));
    CHECK(strstr(error.message, "checksum") != NULL);
    size = simple_mix(bytes, true, false);
    input.size = size;
    put32(bytes + 22, 0xf0000001u);
    CHECK(!ra_mix_open(&mix, input, RA_HASH_CRC32, &error));
    memset(bytes, 0, sizeof(bytes));
    input.size = 10;
    CHECK(ra_mix_open(&mix, input, RA_HASH_CRC32, &error));
    CHECK(mix.count == 0);
    ra_mix_close(&mix);
}

static void ini_tests(void)
{
    const char *text = "\xef\xbb\xbf; comment\r\n[ Unit ]\r\nCost=200 ; test\r\nEmpty=\nName=a=b\r"
                       "[UNIT]\n cost = 400\nEnabled=yEs\nQuoted=\"a;b\"\n";
    const char *invalid[] = {"Key=1", "[x\na=1", "[]=x", "[x] trailing", "[x]\n=1", "[x]\nbroken"};
    const uint8_t utf16le[] = {0xff, 0xfe, '[', 0, 'X', 0, ']', 0, 10, 0, 'K', 0, '=', 0, 0x2d, 0x4e, 0x3d, 0xd8, 0, 0xde};
    const uint8_t utf16be[] = {0xfe, 0xff, 0, '[', 0, 'X', 0, ']', 0, 10, 0, 'K', 0, '=', 0x4e, 0x2d, 0xd8, 0x3d, 0xde, 0};
    const uint8_t broken[] = {0xff, 0xfe, '[', 0, 'x'};
    const uint8_t legacy[] = {'[', 'x', ']', '\n', 'k', '=', 0xb0, 0xa1};
    const uint8_t bad_utf8[] = {0xef, 0xbb, 0xbf, 0xc0, 0x80};
    ra_ini ini = {0};
    ra_error error = {0};
    const ra_ini_entry *entry;
    int64_t number;
    bool flag;
    size_t i;
    CHECK(ra_ini_parse(&ini, text_view(text), "synthetic.ini", &error));
    CHECK(ini.section_count == 2 && ini.entry_count == 6 && ini.duplicate_count == 1);
    entry = ra_ini_get(&ini, "unit", "COST");
    CHECK(entry && !strcmp(entry->value, "400") && entry->line == 7);
    CHECK(ra_ini_integer(entry, &number, &error) && number == 400);
    CHECK(ra_ini_boolean(ra_ini_get(&ini, "unit", "enabled"), &flag, &error) && flag);
    CHECK(ra_ini_get(&ini, "unit", "empty") && !*ra_ini_get(&ini, "unit", "empty")->value);
    CHECK(!strcmp(ra_ini_get(&ini, "unit", "name")->value, "a=b"));
    CHECK(!strcmp(ra_ini_get(&ini, "unit", "quoted")->value, "\"a"));
    CHECK(ra_ini_get(&ini, "missing", "cost") == NULL);
    CHECK(!strcmp(ini.entries[0].value, "200"));
    ra_ini_close(&ini);
    for (i = 0; i < sizeof(invalid) / sizeof(*invalid); ++i)
    {
        CHECK(!ra_ini_parse_ex(&ini, text_view(invalid[i]), "invalid.ini", RA_INI_STRICT, &error));
        CHECK(error.code == RA_SYNTAX && error.line > 0);
        CHECK(ini.entries == NULL);
    }
    CHECK(ra_ini_parse(&ini, text_view("[x]\n***legacy prose***\nk=3"), "compat", &error));
    CHECK(ini.ignored_count == 1 && ini.ignored_lines[0].line == 2);
    CHECK(!strcmp(ra_ini_get(&ini, "x", "k")->value, "3"));
    ra_ini_close(&ini);
    CHECK(ra_ini_parse(&ini, text_view("[x] // legacy note\nk=4"), "compat-header", &error));
    CHECK(ini.ignored_count == 1 && ini.ignored_lines[0].line == 1);
    CHECK(!strcmp(ra_ini_get(&ini, "x", "k")->value, "4"));
    ra_ini_close(&ini);
    {
        ra_view v = {utf16le, sizeof(utf16le)};
        CHECK(ra_ini_parse(&ini, v, "utf16le.ini", &error));
        CHECK(!strcmp(ra_ini_get(&ini, "x", "k")->value, "\xe4\xb8\xad\xf0\x9f\x98\x80"));
        ra_ini_close(&ini);
    }
    {
        ra_view v = {utf16be, sizeof(utf16be)};
        CHECK(ra_ini_parse(&ini, v, "utf16be.ini", &error));
        CHECK(!strcmp(ra_ini_get(&ini, "x", "k")->value, "\xe4\xb8\xad\xf0\x9f\x98\x80"));
        ra_ini_close(&ini);
    }
    {
        ra_view v = {broken, sizeof(broken)};
        CHECK(!ra_ini_parse(&ini, v, "broken", &error));
    }
    {
        ra_view v = {bad_utf8, sizeof(bad_utf8)};
        CHECK(!ra_ini_parse(&ini, v, "broken", &error));
    }
    {
        ra_view v = {legacy, sizeof(legacy)};
        CHECK(ra_ini_parse(&ini, v, "legacy", &error));
        CHECK(!strcmp(ini.encoding, "bytes"));
        CHECK(!memcmp(ra_ini_get(&ini, "x", "k")->value, legacy + 6, 2));
        ra_ini_close(&ini);
    }
    {
        const uint8_t nul[] = {'[', 'x', ']', 0, 'k', '=', '1'};
        ra_view v = {nul, sizeof(nul)};
        CHECK(!ra_ini_parse(&ini, v, "nul", &error));
    }
    CHECK(
        ra_ini_parse(&ini, text_view("[x]\nMax=9223372036854775807\nMin=-9223372036854775808\nOver=9223372036854775808\nBad=3x\nNo=off\n"), "numbers", &error));
    CHECK(ra_ini_integer(ra_ini_get(&ini, "x", "Max"), &number, &error) && number == INT64_MAX);
    CHECK(ra_ini_integer(ra_ini_get(&ini, "x", "Min"), &number, &error) && number == INT64_MIN);
    CHECK(!ra_ini_integer(ra_ini_get(&ini, "x", "Over"), &number, &error));
    CHECK(!ra_ini_integer(ra_ini_get(&ini, "x", "Bad"), &number, &error));
    CHECK(ra_ini_boolean(ra_ini_get(&ini, "x", "No"), &flag, &error) && !flag);
    CHECK(!ra_ini_boolean(ra_ini_get(&ini, "x", "Bad"), &flag, &error));
    ra_ini_close(&ini);
    {
        ra_view empty = {NULL, 0};
        CHECK(ra_ini_parse(&ini, empty, "empty", &error));
        CHECK(ini.entry_count == 0);
        ra_ini_close(&ini);
    }
}

static void stress_tests(void)
{
    ra_ini ini = {0};
    ra_mix mix = {0};
    ra_error error = {0};
    size_t cap = 1200000, used = 0, i;
    char *data = malloc(cap);
    uint32_t random = 0x7cbadc31;
    CHECK(data != NULL);
    used += (size_t)snprintf(data + used, cap - used, "[Large]\n");
    for (i = 0; i < 50000; ++i) used += (size_t)snprintf(data + used, cap - used, "Key%zu=%zu\n", i, i);
    {
        ra_view v = {(const uint8_t *)data, used};
        CHECK(ra_ini_parse(&ini, v, "large", &error));
    }
    CHECK(ini.entry_count == 50000 && ini.duplicate_count == 0);
    for (i = 0; i < 50000; i += 97)
    {
        char name[32];
        int64_t value;
        snprintf(name, sizeof(name), "kEy%zu", i);
        CHECK(ra_ini_integer(ra_ini_get(&ini, "LARGE", name), &value, &error) && value == (int64_t)i);
    }
    ra_ini_close(&ini);
    for (i = 0; i < 3000; ++i)
    {
        uint8_t bytes[256];
        size_t j, n = i % sizeof(bytes);
        ra_view v = {bytes, n};
        for (j = 0; j < n; ++j)
        {
            random ^= random << 13;
            random ^= random >> 17;
            random ^= random << 5;
            bytes[j] = (uint8_t)random;
        }
        (void)ra_mix_open(&mix, v, RA_HASH_CRC32, &error);
        ra_mix_close(&mix);
        (void)ra_ini_parse(&ini, v, "random", &error);
        ra_ini_close(&ini);
    }
    free(data);
    CHECK(true);
}

static char *path_join(const char *base, const char *suffix)
{
    size_t n = strlen(base) + strlen(suffix) + 2;
    char *p = malloc(n);
    if (p) snprintf(p, n, "%s/%s", base, suffix);
    return p;
}
static void corpus_tests(const char *baseline, const char *mod, const char *extracted)
{
    const char *names[] = {"rules.ini",    "art.ini",          "ai.ini",       "sound.ini",    "eva.ini",      "theme.ini",    "battle.ini",
                           "coopcamp.ini", "key.ini",          "keyboard.ini", "mapsel.ini",   "mission.ini",  "mpbattle.ini", "mpcoop.ini",
                           "mpduel.ini",   "mpfreeforall.ini", "mpmeat.ini",   "mpmodes.ini",  "mpmw.ini",     "mpnaval.ini",  "mpsiege.ini",
                           "mpunholy.ini", "rmg.ini",          "snow.ini",     "temperat.ini", "tutorial.ini", "ui.ini",       "urban.ini"};
    ra_vfs vfs = {0};
    ra_resource resource = {0};
    ra_file expected = {0};
    ra_ini ini = {0};
    ra_error error = {0};
    char *archive = path_join(baseline, "ra2.mix"), *spec;
    size_t i, n;
    int64_t strength;
    CHECK(archive != NULL);
    n = strlen(archive) + 11;
    spec = malloc(n);
    CHECK(spec != NULL);
    snprintf(spec, n, "%s|local.mix", archive);
    CHECK(ra_vfs_mount_mix(&vfs, spec, 10, RA_HASH_CRC32, &error));
    for (i = 0; i < sizeof(names) / sizeof(*names); ++i)
    {
        char *path = path_join(extracted, names[i]);
        CHECK(path != NULL);
        CHECK(ra_vfs_read(&vfs, names[i], &resource, &error));
        CHECK(ra_file_open(&expected, path, &error));
        CHECK(expected.view.size == resource.view.size && !memcmp(expected.view.data, resource.view.data, resource.view.size));
        CHECK(ra_ini_parse(&ini, resource.view, resource.source, &error));
        if (!strcmp(names[i], "mpsiege.ini")) CHECK(ini.entry_count == 0);
        else CHECK(ini.entry_count > 0);
        printf("CORPUS %s: %zu bytes, %zu entries\n", names[i], resource.view.size, ini.entry_count);
        ra_ini_close(&ini);
        ra_file_close(&expected);
        ra_resource_close(&resource);
        free(path);
    }
    CHECK(ra_vfs_mount_directory(&vfs, mod, 100, &error));
    CHECK(ra_vfs_read(&vfs, "RULES.INI", &resource, &error));
    CHECK(resource.priority == 100 && strstr(resource.source, "|local.mix") == NULL);
    CHECK(ra_ini_parse(&ini, resource.view, resource.source, &error));
    CHECK(ra_ini_integer(ra_ini_get(&ini, "CNLTNK", "Strength"), &strength, &error) && strength == 400);
    CHECK(ra_ini_get(&ini, "CNAPOC", "Primary") != NULL);
    ra_ini_close(&ini);
    ra_resource_close(&resource);
    CHECK(ra_vfs_read(&vfs, "ai.ini", &resource, &error));
    CHECK(resource.priority == 10);
    ra_resource_close(&resource);
    CHECK(ra_vfs_mount_directory(&vfs, extracted, 100, &error));
    CHECK(ra_vfs_read(&vfs, "rules.ini", &resource, &error));
    CHECK(strstr(resource.source, extracted) == resource.source);
    CHECK(ra_ini_parse(&ini, resource.view, resource.source, &error));
    CHECK(ra_ini_get(&ini, "CNLTNK", "Strength") == NULL);
    ra_ini_close(&ini);
    ra_resource_close(&resource);
    CHECK(ra_vfs_mount_directory(&vfs, mod, 50, &error));
    CHECK(ra_vfs_read(&vfs, "rules.ini", &resource, &error));
    CHECK(resource.priority == 100);
    ra_resource_close(&resource);
    CHECK(!ra_vfs_read(&vfs, "missing-resource-928374.ini", &resource, &error) && error.code == RA_NOT_FOUND);
    CHECK(!ra_vfs_read(&vfs, "../rules.ini", &resource, &error) && error.code == RA_ARGUMENT);
    CHECK(!ra_vfs_read(&vfs, ".. /rules.ini", &resource, &error) && error.code == RA_ARGUMENT);
    CHECK(!ra_vfs_read(&vfs, "C:/rules.ini", &resource, &error) && error.code == RA_ARGUMENT);
    CHECK(!ra_vfs_mount_mix(&vfs, "Z:/missing-resource-928374.mix", 1, RA_HASH_CRC32, &error));
    CHECK(ra_vfs_read(&vfs, "rules.ini", &resource, &error));
    ra_resource_close(&resource);
    ra_vfs_close(&vfs);
    free(spec);
    free(archive);
}
static int app_main(int argc, char **argv)
{
    crypto_tests();
    mix_tests();
    ini_tests();
    stress_tests();
    if (argc == 4) corpus_tests(argv[1], argv[2], argv[3]);
    else if (argc != 1)
    {
        fputs("Usage: ra2tests [baseline-directory mod-directory extracted-local-directory]\n", stderr);
        return 2;
    }
    printf("{\"checks\":%u,\"failures\":%u,\"corpus\":%s}\n", checks, failures, argc == 4 ? "true" : "false");
    return failures ? 1 : 0;
}
