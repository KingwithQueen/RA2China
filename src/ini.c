#define _CRT_SECURE_NO_WARNINGS
#include "internal.h"
#include <errno.h>
#include <stdlib.h>
#include <string.h>

static bool whitespace(char c) { return c == ' ' || c == '\t' || c == '\v' || c == '\f'; }
static char *trim(char *s)
{
    size_t length;
    while (whitespace(*s)) ++s;
    length = strlen(s);
    while (length && whitespace(s[length-1])) s[--length] = 0;
    return s;
}

static char *decode(ra_view bytes, const char **encoding, ra_error *error)
{
    char *out;
    size_t skip = 0;
    if (bytes.size >= 2 && ((bytes.data[0] == 0xff && bytes.data[1] == 0xfe) ||
                           (bytes.data[0] == 0xfe && bytes.data[1] == 0xff))) {
        bool little = bytes.data[0] == 0xff;
        size_t i, used = 0;
        if (bytes.size % 2 || bytes.size > (SIZE_MAX-1)/2) {
            ra_fail(error, RA_FORMAT, 0, "invalid UTF-16 input length"); return NULL;
        }
        out = malloc(bytes.size*2+1);
        if (!out) { ra_fail(error, RA_MEMORY, 0, "INI text allocation failed"); return NULL; }
        *encoding = little ? "utf-16le" : "utf-16be";
        for (i = 2; i < bytes.size; i += 2) {
            uint32_t c = little ? ra_le16(bytes.data+i) : (uint16_t)(bytes.data[i] << 8 | bytes.data[i+1]);
            if (c >= 0xd800 && c <= 0xdbff) {
                uint32_t low;
                if (bytes.size-i < 4) goto bad_utf16;
                i += 2;
                low = little ? ra_le16(bytes.data+i) : (uint16_t)(bytes.data[i] << 8 | bytes.data[i+1]);
                if (low < 0xdc00 || low > 0xdfff) goto bad_utf16;
                c = 0x10000+((c-0xd800) << 10)+(low-0xdc00);
            } else if (c >= 0xdc00 && c <= 0xdfff) goto bad_utf16;
            if (!c) goto bad_utf16;
            if (c < 0x80) out[used++] = (char)c;
            else if (c < 0x800) { out[used++] = (char)(0xc0 | c >> 6); out[used++] = (char)(0x80 | (c & 63)); }
            else if (c < 0x10000) {
                out[used++] = (char)(0xe0 | c >> 12); out[used++] = (char)(0x80 | ((c >> 6) & 63)); out[used++] = (char)(0x80 | (c & 63));
            } else {
                out[used++] = (char)(0xf0 | c >> 18); out[used++] = (char)(0x80 | ((c >> 12) & 63));
                out[used++] = (char)(0x80 | ((c >> 6) & 63)); out[used++] = (char)(0x80 | (c & 63));
            }
        }
        out[used] = 0; return out;
bad_utf16:
        free(out); ra_fail(error, RA_FORMAT, 0, "invalid UTF-16 scalar or embedded NUL"); return NULL;
    }
    if (bytes.size >= 3 && memcmp(bytes.data, "\xef\xbb\xbf", 3) == 0) skip = 3;
    {
        ra_view text = {bytes.data ? bytes.data+skip : NULL, bytes.size-skip};
        bool valid = ra_utf8_valid(text);
        if (skip && !valid) { ra_fail(error, RA_FORMAT, 0, "invalid UTF-8 after BOM"); return NULL; }
        if (text.size && memchr(text.data, 0, text.size)) { ra_fail(error, RA_FORMAT, 0, "embedded NUL in INI"); return NULL; }
        *encoding = valid ? "utf-8" : "bytes";
        out = ra_copy(text.data ? (const char *)text.data : "", text.size);
        if (!out) ra_fail(error, RA_MEMORY, 0, "INI text allocation failed");
        return out;
    }
}

static bool grow(void **array, size_t count, size_t *capacity, size_t size, ra_error *error)
{
    size_t cap;
    void *p;
    if (count < *capacity) return true;
    cap = *capacity ? *capacity*2 : 16;
    if (cap < *capacity || cap > SIZE_MAX/size) return ra_fail(error, RA_MEMORY, 0, "INI capacity overflow");
    p = realloc(*array, cap*size);
    if (!p) return ra_fail(error, RA_MEMORY, 0, "INI array allocation failed");
    *array = p; *capacity = cap;
    return true;
}

static bool ignored_text(ra_ini *ini, const char *text, size_t line, size_t *capacity, ra_error *error)
{
    ra_ini_diagnostic *diagnostic;
    if (!grow((void **)&ini->ignored_lines, ini->ignored_count, capacity, sizeof(*ini->ignored_lines), error)) return false;
    diagnostic = ini->ignored_lines+ini->ignored_count++;
    diagnostic->line = line; diagnostic->text = ra_copy(text, strlen(text));
    if (!diagnostic->text) return ra_fail(error, RA_MEMORY, line, "INI diagnostic allocation failed");
    return true;
}

static uint64_t key_hash(const char *section, const char *key)
{
    uint64_t h = UINT64_C(14695981039346656037);
    unsigned part;
    for (part = 0; part < 2; ++part) {
        const uint8_t *s = (const uint8_t *)(part ? key : section);
        while (*s) {
            unsigned c = *s++;
            if (c >= 'A' && c <= 'Z') c += 32;
            h = (h ^ c) * UINT64_C(1099511628211);
        }
        h = (h ^ 0) * UINT64_C(1099511628211);
    }
    return h;
}

static bool build_index(ra_ini *ini, ra_error *error)
{
    size_t cap = 16, i;
    if (ini->entry_count > SIZE_MAX/2) return ra_fail(error, RA_MEMORY, 0, "INI index overflow");
    while (cap < ini->entry_count*2) {
        if (cap > SIZE_MAX/2) return ra_fail(error, RA_MEMORY, 0, "INI index overflow");
        cap *= 2;
    }
    ini->index = calloc(cap, sizeof(*ini->index)); ini->index_capacity = cap;
    if (!ini->index) return ra_fail(error, RA_MEMORY, 0, "INI index allocation failed");
    for (i = 0; i < ini->entry_count; ++i) {
        const ra_ini_entry *e = ini->entries+i;
        size_t slot = (size_t)key_hash(e->section, e->key) & (cap-1);
        while (ini->index[slot]) {
            const ra_ini_entry *previous = ini->entries+ini->index[slot]-1;
            if (ra_equal(e->section, previous->section) && ra_equal(e->key, previous->key)) {
                ++ini->duplicate_count; break;
            }
            slot = (slot+1) & (cap-1);
        }
        ini->index[slot] = i+1;
    }
    return true;
}

bool ra_ini_parse_ex(ra_ini *ini, ra_view bytes, const char *source, ra_ini_mode mode, ra_error *error)
{
    ra_ini out = {0};
    char *text, *cursor, *current = NULL;
    size_t line = 0, section_cap = 0, entry_cap = 0, ignored_cap = 0;
    bool ok = false;
    if (!ini || !source || (!bytes.data && bytes.size) || (mode != RA_INI_COMPAT && mode != RA_INI_STRICT))
        return ra_fail(error, RA_ARGUMENT, 0, "invalid INI arguments");
    text = decode(bytes, &out.encoding, error);
    if (!text) return false;
    out.source = ra_copy(source, strlen(source));
    if (!out.source) { free(text); return ra_fail(error, RA_MEMORY, 0, "INI source allocation failed"); }
    cursor = text;
    while (*cursor) {
        char *s = cursor, *comment, *equal, *end;
        ++line;
        while (*cursor && *cursor != '\r' && *cursor != '\n') ++cursor;
        if (*cursor) {
            char first = *cursor; *cursor++ = 0;
            if (first == '\r' && *cursor == '\n') ++cursor;
        }
        comment = strchr(s, ';'); if (comment) *comment = 0;
        s = trim(s); if (!*s) continue;
        if (*s == '[') {
            ra_ini_section *section;
            end = strchr(s+1, ']');
            if (!end || (mode == RA_INI_STRICT && *trim(end+1))) { ra_fail(error, RA_SYNTAX, line, "invalid section header"); goto done; }
            if (*trim(end+1) && !ignored_text(&out, trim(end+1), line, &ignored_cap, error)) goto done;
            *end = 0; s = trim(s+1);
            if (!*s) { ra_fail(error, RA_SYNTAX, line, "empty section name"); goto done; }
            if (!grow((void **)&out.sections, out.section_count, &section_cap, sizeof(*out.sections), error)) goto done;
            section = out.sections+out.section_count++; section->line = line; section->name = ra_copy(s, strlen(s));
            if (!section->name) { ra_fail(error, RA_MEMORY, line, "section allocation failed"); goto done; }
            current = section->name;
            continue;
        }
        equal = strchr(s, '=');
        if (!equal && mode == RA_INI_COMPAT) {
            if (!ignored_text(&out, s, line, &ignored_cap, error)) goto done;
            continue;
        }
        if (!current || !equal) { ra_fail(error, RA_SYNTAX, line, "expected key=value inside a section"); goto done; }
        *equal = 0; s = trim(s); equal = trim(equal+1);
        if (!*s) { ra_fail(error, RA_SYNTAX, line, "empty key"); goto done; }
        if (!grow((void **)&out.entries, out.entry_count, &entry_cap, sizeof(*out.entries), error)) goto done;
        {
            ra_ini_entry *entry = out.entries+out.entry_count++;
            entry->section = ra_copy(current, strlen(current)); entry->key = ra_copy(s, strlen(s));
            entry->value = ra_copy(equal, strlen(equal)); entry->line = line;
            if (!entry->section || !entry->key || !entry->value) { ra_fail(error, RA_MEMORY, line, "entry allocation failed"); goto done; }
        }
    }
    if (!build_index(&out, error)) goto done;
    *ini = out; ok = true;
done:
    free(text);
    if (!ok) ra_ini_close(&out);
    return ok;
}

bool ra_ini_parse(ra_ini *ini, ra_view bytes, const char *source, ra_error *error)
{ return ra_ini_parse_ex(ini, bytes, source, RA_INI_COMPAT, error); }

const ra_ini_entry *ra_ini_get(const ra_ini *ini, const char *section, const char *key)
{
    size_t slot;
    if (!ini || !section || !key || !ini->index_capacity) return NULL;
    slot = (size_t)key_hash(section, key) & (ini->index_capacity-1);
    while (ini->index[slot]) {
        const ra_ini_entry *entry = ini->entries+ini->index[slot]-1;
        if (ra_equal(section, entry->section) && ra_equal(key, entry->key)) return entry;
        slot = (slot+1) & (ini->index_capacity-1);
    }
    return NULL;
}

bool ra_ini_integer(const ra_ini_entry *entry, int64_t *value, ra_error *error)
{
    char *end;
    long long parsed;
    if (!entry || !value) return ra_fail(error, RA_ARGUMENT, 0, "invalid integer arguments");
    errno = 0; parsed = strtoll(entry->value, &end, 10);
    if (errno == ERANGE || end == entry->value || *end)
        return ra_fail(error, RA_RANGE, entry->line, "invalid decimal integer: %s", entry->value);
    *value = (int64_t)parsed; return true;
}
bool ra_ini_boolean(const ra_ini_entry *entry, bool *value, ra_error *error)
{
    if (!entry || !value) return ra_fail(error, RA_ARGUMENT, 0, "invalid boolean arguments");
    if (ra_equal(entry->value, "yes") || ra_equal(entry->value, "true") || ra_equal(entry->value, "on") || ra_equal(entry->value, "1")) { *value = true; return true; }
    if (ra_equal(entry->value, "no") || ra_equal(entry->value, "false") || ra_equal(entry->value, "off") || ra_equal(entry->value, "0")) { *value = false; return true; }
    return ra_fail(error, RA_RANGE, entry->line, "invalid boolean: %s", entry->value);
}
void ra_ini_close(ra_ini *ini)
{
    size_t i;
    if (!ini) return;
    for (i = 0; i < ini->section_count; ++i) free(ini->sections[i].name);
    for (i = 0; i < ini->entry_count; ++i) {
        free(ini->entries[i].section); free(ini->entries[i].key); free(ini->entries[i].value);
    }
    for (i = 0; i < ini->ignored_count; ++i) free(ini->ignored_lines[i].text);
    free(ini->sections); free(ini->entries); free(ini->source); free(ini->index); free(ini->ignored_lines);
    memset(ini, 0, sizeof(*ini));
}
