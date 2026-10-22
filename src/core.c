#define _CRT_SECURE_NO_WARNINGS
#include "internal.h"
#include <stdarg.h>
#include <errno.h>
#include <stdlib.h>
#include <string.h>
#ifdef _WIN32
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#else
#include <sys/stat.h>
#endif

bool ra_fail(ra_error *error, ra_status code, size_t line, const char *fmt, ...)
{
    if (error) {
        va_list args;
        error->code = code;
        error->line = line;
        va_start(args, fmt);
        vsnprintf(error->message, sizeof(error->message), fmt, args);
        va_end(args);
    }
    return false;
}

const char *ra_status_name(ra_status status)
{
    static const char *names[] = {"ok", "io", "format", "memory", "not_found",
                                 "argument", "syntax", "range"};
    return (unsigned)status < sizeof(names) / sizeof(*names) ? names[status] : "unknown";
}

char *ra_copy(const char *text, size_t length)
{
    char *copy;
    if (length == SIZE_MAX) return NULL;
    copy = malloc(length + 1);
    if (copy) { memcpy(copy, text, length); copy[length] = 0; }
    return copy;
}

static unsigned ascii_lower(unsigned c) { return c >= 'A' && c <= 'Z' ? c + 32 : c; }
bool ra_equal(const char *a, const char *b)
{
    while (*a && *b) {
        if (ascii_lower((uint8_t)*a++) != ascii_lower((uint8_t)*b++)) return false;
    }
    return *a == *b;
}

uint16_t ra_le16(const uint8_t *p) { return (uint16_t)(p[0] | (uint16_t)p[1] << 8); }
uint32_t ra_le32(const uint8_t *p)
{ return (uint32_t)p[0] | (uint32_t)p[1] << 8 | (uint32_t)p[2] << 16 | (uint32_t)p[3] << 24; }

bool ra_utf8_valid(ra_view input)
{
    size_t i = 0;
    while (i < input.size) {
        uint32_t c = input.data[i++], minimum;
        unsigned n;
        if (c < 128) continue;
        if (c >= 0xc2 && c <= 0xdf) { n = 1; minimum = 0x80; c &= 31; }
        else if (c >= 0xe0 && c <= 0xef) { n = 2; minimum = 0x800; c &= 15; }
        else if (c >= 0xf0 && c <= 0xf4) { n = 3; minimum = 0x10000; c &= 7; }
        else return false;
        if (n > input.size - i) return false;
        while (n--) {
            uint8_t b = input.data[i++];
            if ((b & 0xc0) != 0x80) return false;
            c = c << 6 | (b & 63);
        }
        if (c < minimum || c > 0x10ffff || (c >= 0xd800 && c <= 0xdfff)) return false;
    }
    return true;
}

#ifdef _WIN32
static wchar_t *wide_path(const char *path)
{
    int n = MultiByteToWideChar(CP_UTF8, MB_ERR_INVALID_CHARS, path, -1, NULL, 0);
    wchar_t *w;
    if (!n) return NULL;
    w = malloc((size_t)n * sizeof(*w));
    if (w && !MultiByteToWideChar(CP_UTF8, MB_ERR_INVALID_CHARS, path, -1, w, n)) {
        free(w); return NULL;
    }
    return w;
}
#endif

bool ra_file_open(ra_file *file, const char *path, ra_error *error)
{
    ra_file out = {0};
    if (!file || !path) return ra_fail(error, RA_ARGUMENT, 0, "file/path is null");
#ifdef _WIN32
    {
        LARGE_INTEGER size;
        HANDLE h, mapping;
        wchar_t *w = wide_path(path);
        DWORD code;
        if (!w) return ra_fail(error, RA_ARGUMENT, 0, "invalid UTF-8 path");
        h = CreateFileW(w, GENERIC_READ, FILE_SHARE_READ, NULL, OPEN_EXISTING,
                        FILE_ATTRIBUTE_NORMAL, NULL);
        code = GetLastError();
        free(w);
        if (h == INVALID_HANDLE_VALUE)
            return ra_fail(error, code == ERROR_FILE_NOT_FOUND || code == ERROR_PATH_NOT_FOUND
                           ? RA_NOT_FOUND : RA_IO, 0, "open failed (%lu): %s", (unsigned long)code, path);
        if (!GetFileSizeEx(h, &size) || size.QuadPart < 0 || (uint64_t)size.QuadPart > SIZE_MAX) {
            CloseHandle(h); return ra_fail(error, RA_IO, 0, "invalid file size: %s", path);
        }
        out.handle = h;
        out.view.size = (size_t)size.QuadPart;
        if (out.view.size) {
            mapping = CreateFileMappingW(h, NULL, PAGE_READONLY, 0, 0, NULL);
            if (!mapping) { CloseHandle(h); return ra_fail(error, RA_IO, 0, "mapping failed: %s", path); }
            out.mapping = mapping;
            out.view.data = MapViewOfFile(mapping, FILE_MAP_READ, 0, 0, 0);
            if (!out.view.data) { ra_file_close(&out); return ra_fail(error, RA_IO, 0, "map view failed: %s", path); }
        }
    }
#else
    {
        FILE *f = fopen(path, "rb");
        long size;
        if (!f) return ra_fail(error, errno == ENOENT || errno == ENOTDIR ? RA_NOT_FOUND : RA_IO, 0, "open failed: %s", path);
        if (fseek(f, 0, SEEK_END) || (size = ftell(f)) < 0 || fseek(f, 0, SEEK_SET)) {
            fclose(f); return ra_fail(error, RA_IO, 0, "seek failed: %s", path);
        }
        out.view.size = (size_t)size;
        if (size) {
            out.owned = malloc(out.view.size);
            if (!out.owned) { fclose(f); return ra_fail(error, RA_MEMORY, 0, "file allocation failed"); }
            if (fread(out.owned, 1, out.view.size, f) != out.view.size) {
                free(out.owned); fclose(f); return ra_fail(error, RA_IO, 0, "short read: %s", path);
            }
        }
        out.view.data = out.owned;
        fclose(f);
    }
#endif
    *file = out;
    return true;
}

void ra_file_close(ra_file *file)
{
    if (!file) return;
#ifdef _WIN32
    if (file->mapping && file->view.data) UnmapViewOfFile(file->view.data);
    if (file->mapping) CloseHandle(file->mapping);
    if (file->handle) CloseHandle(file->handle);
#endif
    free(file->owned);
    memset(file, 0, sizeof(*file));
}

bool ra_directory_exists(const char *path)
{
#ifdef _WIN32
    wchar_t *w = wide_path(path);
    DWORD attr;
    if (!w) return false;
    attr = GetFileAttributesW(w);
    free(w);
    return attr != INVALID_FILE_ATTRIBUTES && (attr & FILE_ATTRIBUTE_DIRECTORY) != 0;
#else
    struct stat s;
    return stat(path, &s) == 0 && S_ISDIR(s.st_mode);
#endif
}

void ra_hex(const uint8_t *bytes, size_t count, char *output)
{
    static const char digits[] = "0123456789abcdef";
    size_t i;
    for (i = 0; i < count; ++i) {
        output[2*i] = digits[bytes[i] >> 4]; output[2*i+1] = digits[bytes[i] & 15];
    }
    output[count*2] = 0;
}
