#include "internal.h"
#include <string.h>
#include "blowfish_constants.h"

static uint32_t rol(uint32_t x, unsigned n) { return x << n | x >> (32-n); }
static void sha1_block(uint32_t state[5], const uint8_t block[64])
{
    uint32_t w[80], a = state[0], b = state[1], c = state[2], d = state[3], e = state[4];
    unsigned i;
    for (i = 0; i < 16; ++i) w[i] = (uint32_t)block[4*i] << 24 |
        (uint32_t)block[4*i+1] << 16 | (uint32_t)block[4*i+2] << 8 | block[4*i+3];
    for (; i < 80; ++i) w[i] = rol(w[i-3] ^ w[i-8] ^ w[i-14] ^ w[i-16], 1);
    for (i = 0; i < 80; ++i) {
        uint32_t f, k, t;
        if (i < 20) { f = (b & c) | (~b & d); k = 0x5a827999; }
        else if (i < 40) { f = b ^ c ^ d; k = 0x6ed9eba1; }
        else if (i < 60) { f = (b & c) | (b & d) | (c & d); k = 0x8f1bbcdc; }
        else { f = b ^ c ^ d; k = 0xca62c1d6; }
        t = rol(a, 5) + f + e + k + w[i]; e = d; d = c; c = rol(b, 30); b = a; a = t;
    }
    state[0] += a; state[1] += b; state[2] += c; state[3] += d; state[4] += e;
}

void ra_sha1(ra_view input, uint8_t digest[20])
{
    uint32_t state[5] = {0x67452301,0xefcdab89,0x98badcfe,0x10325476,0xc3d2e1f0};
    uint8_t tail[128] = {0};
    size_t blocks = input.size / 64, rem = input.size % 64, i;
    uint64_t bits = (uint64_t)input.size * 8;
    for (i = 0; i < blocks; ++i) sha1_block(state, input.data + 64*i);
    if (rem) memcpy(tail, input.data + blocks*64, rem);
    tail[rem] = 0x80;
    blocks = rem < 56 ? 1 : 2;
    for (i = 0; i < 8; ++i) tail[blocks*64-1-i] = (uint8_t)(bits >> (8*i));
    sha1_block(state, tail);
    if (blocks == 2) sha1_block(state, tail+64);
    for (i = 0; i < 20; ++i) digest[i] = (uint8_t)(state[i/4] >> (24-8*(i%4)));
}

static uint32_t bf_f(const ra_blowfish *c, uint32_t x)
{ return ((c->s[x >> 24] + c->s[256 + ((x >> 16) & 255)]) ^
          c->s[512 + ((x >> 8) & 255)]) + c->s[768 + (x & 255)]; }
static void bf_encrypt(const ra_blowfish *c, uint32_t *l, uint32_t *r)
{
    uint32_t a = *l, b = *r, t;
    unsigned i;
    for (i = 0; i < 16; ++i) { a ^= c->p[i]; b ^= bf_f(c, a); t = a; a = b; b = t; }
    *l = b ^ c->p[17]; *r = a ^ c->p[16];
}
void ra_blowfish_init(ra_blowfish *c, const uint8_t *key, size_t length)
{
    size_t i, j = 0;
    uint32_t l = 0, r = 0;
    memcpy(c->p, ra_bf_initial, sizeof(c->p));
    memcpy(c->s, ra_bf_initial + 18, sizeof(c->s));
    for (i = 0; i < 18; ++i) {
        uint32_t k = 0;
        unsigned n;
        for (n = 0; n < 4; ++n) { k = k << 8 | key[j]; j = (j+1) % length; }
        c->p[i] ^= k;
    }
    for (i = 0; i < 18; i += 2) { bf_encrypt(c, &l, &r); c->p[i] = l; c->p[i+1] = r; }
    for (i = 0; i < 1024; i += 2) { bf_encrypt(c, &l, &r); c->s[i] = l; c->s[i+1] = r; }
}
void ra_blowfish_decrypt(const ra_blowfish *c, uint8_t block[8])
{
    uint32_t a = 0, b = 0, t;
    int i;
    for (i = 0; i < 4; ++i) { a = a << 8 | block[i]; b = b << 8 | block[i+4]; }
    for (i = 17; i > 1; --i) { a ^= c->p[i]; b ^= bf_f(c, a); t = a; a = b; b = t; }
    a ^= c->p[1]; b ^= c->p[0];
    for (i = 0; i < 4; ++i) { block[i] = (uint8_t)(b >> (24-8*i)); block[i+4] = (uint8_t)(a >> (24-8*i)); }
}

/* Fixed 320-bit arithmetic for the public Westwood MIX key transform only.
 * Not a general-purpose cryptography API. Values use little-endian bytes.
 * An extra byte holds carry during modular addition. */
typedef struct { uint8_t b[41]; } big;
static const big modulus = {{
    0x15,0x7f,0x43,0xaa,0x3d,0x4f,0xfb,0xd1,0xe6,0xc1,0xb0,0xf8,0x6a,0x0e,0xdd,0xab,
    0x4a,0xb0,0x82,0x66,0xfa,0x54,0xaa,0xe8,0xa2,0x3f,0x71,0x51,0xd6,0x60,0x51,0x56,
    0xe4,0xfc,0x39,0x6d,0x08,0xda,0xbc,0x51,0x00 }};
static int big_compare(const big *a, const big *b)
{
    int i;
    for (i = 40; i >= 0; --i) if (a->b[i] != b->b[i]) return a->b[i] > b->b[i] ? 1 : -1;
    return 0;
}
static void big_sub(big *a, const big *b)
{
    unsigned i, borrow = 0;
    for (i = 0; i < 41; ++i) {
        unsigned sub = (unsigned)b->b[i] + borrow, v = a->b[i];
        a->b[i] = (uint8_t)(v-sub); borrow = v < sub;
    }
}
static big big_add_mod(const big *a, const big *b)
{
    big out = {{0}};
    unsigned i, carry = 0;
    for (i = 0; i < 41; ++i) {
        unsigned v = (unsigned)a->b[i] + b->b[i] + carry;
        out.b[i] = (uint8_t)v; carry = v >> 8;
    }
    if (big_compare(&out, &modulus) >= 0) big_sub(&out, &modulus);
    return out;
}
static big big_mul_mod(big a, const big *b)
{
    big out = {{0}};
    unsigned i;
    for (i = 0; i < 320; ++i) {
        if ((b->b[i/8] >> (i%8)) & 1) out = big_add_mod(&out, &a);
        a = big_add_mod(&a, &a);
    }
    return out;
}
void ra_mix_key(const uint8_t block[80], uint8_t key[56])
{
    unsigned part;
    for (part = 0; part < 2; ++part) {
        big a = {{0}}, base, result;
        unsigned i;
        memcpy(a.b, block + part*40, 40);
        while (big_compare(&a, &modulus) >= 0) big_sub(&a, &modulus);
        base = a; result = a;
        for (i = 0; i < 16; ++i) result = big_mul_mod(result, &result);
        result = big_mul_mod(result, &base); /* exponent 65537 */
        memcpy(key + part*39, result.b, part ? 17 : 39);
    }
}
