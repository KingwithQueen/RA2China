#ifndef RA2_INTERNAL_H
#define RA2_INTERNAL_H
#include "ra2/ra2.h"
#include <stdio.h>

bool ra_fail(ra_error *error, ra_status code, size_t line, const char *fmt, ...);
char *ra_copy(const char *text, size_t length);
bool ra_equal(const char *a, const char *b);
bool ra_utf8_valid(ra_view input);
uint16_t ra_le16(const uint8_t *p);
uint32_t ra_le32(const uint8_t *p);
bool ra_directory_exists(const char *path);
void ra_mix_key(const uint8_t block[80], uint8_t key[56]);
typedef struct { uint32_t p[18], s[1024]; } ra_blowfish;
void ra_blowfish_init(ra_blowfish *ctx, const uint8_t *key, size_t length);
void ra_blowfish_decrypt(const ra_blowfish *ctx, uint8_t block[8]);

#endif
