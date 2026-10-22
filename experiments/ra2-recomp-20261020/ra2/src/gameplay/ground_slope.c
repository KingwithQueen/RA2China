#include <string.h>
#include "ground_slope.h"
#include "x87_arithmetic.h"

void ra2_ground_initialize_slopes(Ra2SlopeCache *c, int32_t height, uint16_t control)
{
    if (!(c->initialized & 1))
    {
        c->level_height = (double)height;
        c->initialized |= 1;
    }
    Ra2LegacyReal h = ra2_real_from_f64(c->level_height);
    if (!(c->initialized & 2))
    {
        c->world_scale = ra2_real_store_f64(ra2_real_multiply(h, ra2_real_from_f64(1.0 / 256.0), control), control);
        c->initialized |= 2;
    }
    if (!(c->initialized & 4))
    {
        /* 第一种坡面的方向/偏移来自静态表，原版初始化只写它的上限和额外高度。 */
        c->planes[0].ceiling = c->level_height;
        c->planes[0].extra_height = 0;
        static const int8_t gradients[15][2] = {
            {0,1},{-1,0},{0,-1},{1,1},{-1,1},{-1,-1},{1,-1},
            {1,1},{-1,1},{-1,-1},{1,-1},{1,1},{-1,1},{-1,-1},{1,-1}
        };
        static const int8_t offsets[15] = {0,1,1,-1,0,1,0,0,1,2,1,0,1,2,1};
        double two = ra2_real_store_f64(ra2_real_add(h, h, control), control);
        double half = ra2_real_store_f64(ra2_real_multiply(h, ra2_real_from_f64(0.5), control), control);
        double negative_half = ra2_real_store_f64(ra2_real_multiply(h, ra2_real_from_f64(-0.5), control), control);
        for (unsigned i = 1; i < 16; ++i)
        {
            int offset = offsets[i - 1];
            c->planes[i] = (Ra2SlopePlane){ gradients[i - 1][0], gradients[i - 1][1],
                offset == -1 ? -c->level_height : offset == 0 ? 0 : offset == 1 ? c->level_height : two,
                i < 12 ? c->level_height : two, 0 };
        }
        for (unsigned i = 16; i < 20; ++i)
            c->planes[i] = (Ra2SlopePlane){0, 0, i & 1 ? c->level_height : 0, half, i & 1 ? negative_half : half};
        c->initialized |= 4;
    }
}

static unsigned top_bit(uint64_t value)
{ unsigned n = 0; while (value >>= 1) ++n; return n; }

/* 比较扩展精度的确切值；先落成double再比较会改变靠近坡顶的分支。 */
static int compare(Ra2LegacyReal a, Ra2LegacyReal b)
{
    if (!a.significand && !b.significand) return 0;
    if (!a.significand) return b.negative ? 1 : -1;
    if (!b.significand) return a.negative ? -1 : 1;
    if (a.negative != b.negative) return a.negative ? -1 : 1;
    unsigned at = top_bit(a.significand), bt = top_bit(b.significand);
    int32_t ae = a.exponent + (int32_t)at, be = b.exponent + (int32_t)bt;
    int result;
    if (ae != be) result = ae < be ? -1 : 1;
    else
    {
        uint64_t av = a.significand << (63 - at), bv = b.significand << (63 - bt);
        result = av == bv ? 0 : av < bv ? -1 : 1;
    }
    return a.negative ? -result : result;
}

int32_t ra2_ground_slope_height(const Ra2SlopeCache *c, int32_t height, int8_t level, uint8_t slope,
    Ra2WorldPoint position, uint16_t initial_control, uint16_t conversion_control)
{
    uint32_t product = (uint32_t)(int32_t)level * (uint32_t)height;
    int32_t signed_product; memcpy(&signed_product, &product, sizeof(product));
    Ra2LegacyReal base = ra2_real_add(ra2_real_from_i32(signed_product), ra2_real_from_f64(0.5), initial_control);
    int32_t rounded_base = ra2_real_truncate_i32(base);
    if (!slope) return rounded_base;
    const Ra2SlopePlane *p = &c->planes[slope - 1];
    Ra2LegacyReal y = ra2_real_multiply(ra2_real_from_i32((int32_t)((uint32_t)position.y & 255)),
        ra2_real_from_f64(p->y_gradient), conversion_control);
    y = ra2_real_multiply(y, ra2_real_from_f64(c->world_scale), conversion_control);
    Ra2LegacyReal x = ra2_real_multiply(ra2_real_from_i32((int32_t)((uint32_t)position.x & 255)),
        ra2_real_from_f64(p->x_gradient), conversion_control);
    x = ra2_real_multiply(x, ra2_real_from_f64(c->world_scale), conversion_control);
    Ra2LegacyReal value = ra2_real_add(y, x, conversion_control);
    value = ra2_real_add(value, ra2_real_from_f64(p->offset), conversion_control);
    value = ra2_real_add(value, ra2_real_from_f64(p->extra_height), conversion_control);
    Ra2LegacyReal zero = ra2_real_from_i32(0), ceiling = ra2_real_from_f64(p->ceiling);
    if (compare(value, zero) < 0) value = zero;
    if (compare(value, ceiling) > 0) value = ceiling;
    return ra2_real_truncate_i32(ra2_real_add(ra2_real_from_i32(rounded_base), value, conversion_control));
}
