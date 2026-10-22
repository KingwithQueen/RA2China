#ifndef RA2_RA2_H
#define RA2_RA2_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/* All paths and diagnostic source names are UTF-8. APIs never write inputs.
 * Zero-initialize owning structs before first use; close/free before reuse.
 * Borrowed views are valid only while their owning file/VFS remains open.
 * Readers are immutable after construction. Do not mutate a VFS concurrently. */
typedef enum { RA_OK, RA_IO, RA_FORMAT, RA_MEMORY, RA_NOT_FOUND, RA_ARGUMENT,
               RA_SYNTAX, RA_RANGE } ra_status;
typedef struct { ra_status code; size_t line; char message[512]; } ra_error;
typedef struct { const uint8_t *data; size_t size; } ra_view;
typedef struct {
    ra_view view;
    void *handle, *mapping;
    uint8_t *owned;
} ra_file;

bool ra_file_open(ra_file *file, const char *path, ra_error *error);
void ra_file_close(ra_file *file);
const char *ra_status_name(ra_status status);
void ra_sha1(ra_view input, uint8_t digest[20]);
void ra_hex(const uint8_t *bytes, size_t count, char *output);

typedef enum { RA_HASH_CRC32, RA_HASH_CLASSIC } ra_hash_kind;
typedef struct { uint32_t id, offset, size; } ra_mix_entry;
typedef struct {
    ra_view bytes;
    ra_mix_entry *entries; /* sorted by unsigned ID; duplicates rejected */
    size_t count, data_offset;
    uint32_t flags, data_size;
    ra_hash_kind hash_kind;
    bool checksum_verified;
} ra_mix;

uint32_t ra_mix_id(const char *name, ra_hash_kind kind);
bool ra_mix_open(ra_mix *mix, ra_view bytes, ra_hash_kind kind, ra_error *error);
void ra_mix_close(ra_mix *mix);
bool ra_mix_get_id(const ra_mix *mix, uint32_t id, ra_view *result, ra_error *error);
bool ra_mix_get(const ra_mix *mix, const char *name, ra_view *result, ra_error *error);

typedef struct ra_mount ra_mount;
typedef struct { ra_mount *mounts; size_t count, capacity; } ra_vfs;
typedef struct {
    ra_view view;
    ra_file loose_file;
    char *source;
    int priority;
} ra_resource;

/* Larger priority wins. For equal priorities, the last mounted source wins.
 * MIX spec: UTF-8 archive path followed by zero or more |nested.mix components.
 * Hash mode is explicit: RA2 uses CRC32, older games may use CLASSIC.
 * No implicit discovery, recursive mounting, or original-engine order assumed. */
bool ra_vfs_mount_mix(ra_vfs *vfs, const char *spec, int priority,
                      ra_hash_kind kind, ra_error *error);
bool ra_vfs_mount_directory(ra_vfs *vfs, const char *directory, int priority,
                            ra_error *error);
bool ra_vfs_read(const ra_vfs *vfs, const char *name, ra_resource *resource,
                  ra_error *error);
void ra_resource_close(ra_resource *resource);
void ra_vfs_close(ra_vfs *vfs);

typedef struct { char *name; size_t line; } ra_ini_section;
typedef struct { char *section, *key, *value; size_t line; } ra_ini_entry;
typedef struct { char *text; size_t line; } ra_ini_diagnostic;
typedef enum { RA_INI_COMPAT, RA_INI_STRICT } ra_ini_mode;
typedef struct {
    char *source;
    ra_ini_section *sections;
    ra_ini_entry *entries;
    size_t section_count, entry_count, duplicate_count;
    const char *encoding;
    size_t *index; /* private lookup table; entries remain in source order */
    size_t index_capacity;
    ra_ini_diagnostic *ignored_lines;
    size_t ignored_count;
} ra_ini;

/* UTF-8 BOM and UTF-16 LE/BE BOM supported. Otherwise preserve bytes exactly
 * (encoding="bytes" if not UTF-8); never guess or replace legacy characters.
 * ASCII-insensitive lookup; repeated keys/sections retained in source order;
 * last assignment wins. ';' starts a comment, including inside quotes.
 * Default COMPAT mode reports non-assignment prose and trailing section-header
 * text as diagnostics. STRICT rejects them. Unclosed/empty headers and malformed
 * assignments are errors in both modes.
 * No includes, interpolation, inheritance or multiline values.
 * These are this reader's documented semantics, not full engine equivalence. */
bool ra_ini_parse(ra_ini *ini, ra_view bytes, const char *source, ra_error *error);
bool ra_ini_parse_ex(ra_ini *ini, ra_view bytes, const char *source,
                     ra_ini_mode mode, ra_error *error);
const ra_ini_entry *ra_ini_get(const ra_ini *ini, const char *section, const char *key);
bool ra_ini_integer(const ra_ini_entry *entry, int64_t *value, ra_error *error);
bool ra_ini_boolean(const ra_ini_entry *entry, bool *value, ra_error *error);
void ra_ini_close(ra_ini *ini);

#endif
