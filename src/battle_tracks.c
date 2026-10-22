#include "internal.h"
#include "battle_internal.h"

typedef struct
{
    int32_t x, y;
    uint32_t direction;
} battle_track_point;
typedef struct
{
    uint32_t start, count;
    int32_t jump;
    uint32_t entry;
    int32_t middle;
} battle_track;
typedef struct
{
    uint32_t raw, direction, flags;
} battle_track_control;
#include "battle_tracks.inc"

bool ra_battle_slope_edge(const ra_battle_tile *from, const ra_battle_tile *to)
{
    if (!from || !to || from->ramp > 20 || to->ramp > 20) return false;
    int delta = (int)to->height - from->height;
    /* 原版 4c8730：跨一层必须由较低的格子提供坡面，坡面朝向通过其实际高度平面显示。 */
    return !delta || (delta == 1 && from->ramp) || (delta == -1 && to->ramp);
}

bool battle_track_sample(uint32_t control, uint32_t index, int32_t *x, int32_t *y, uint32_t *direction)
{
    if (control >= 64 || !track_controls[control].raw) return false;
    const battle_track_control *c = &track_controls[control];
    const battle_track *t = &tracks[c->raw];
    if (index >= t->count) return false;
    const battle_track_point *p = &track_points[t->start + index];
    int32_t px = p->x, py = p->y;
    uint32_t d = p->direction;
    if (c->flags & 1)
    {
        int32_t swap = px;
        px = py;
        py = swap;
        d = (192 - d) & 255;
    }
    if (c->flags & 2)
    {
        px = -px;
        d = (0 - d) & 255;
    }
    if (c->flags & 4)
    {
        py = -py;
        d = (128 - d) & 255;
    }
    *x = px;
    *y = py;
    *direction = d;
    return true;
}

int32_t battle_track_partial(int32_t delta, uint32_t remainder)
{
    /* 原版先乘二进制 1/7，再存入 float；直接整数除七会改变正负边界。 */
    battle_real fraction = battle_real_float(battle_real_float_bits(battle_real_mul(battle_real_int((int32_t)remainder), UINT64_C(0x3fc2492492492492))));
    return battle_real_integer(battle_real_mul(battle_real_int(delta), fraction));
}

void battle_reservations_clear(ra_battle *b, ra_battle_unit *u)
{
    for (uint32_t i = 0; i < u->reserved_count; ++i)
        if (b->occupied[u->reserved[i]] == u->id) b->occupied[u->reserved[i]] = 0;
    u->reserved_count = 0;
}

static uint32_t direction(const ra_battle *b, uint32_t from, uint32_t to)
{
    return battle_direction((int)(to % b->width) - (int)(from % b->width), (int)(ra_battle_cell_y(b, to)) - (int)(ra_battle_cell_y(b, from))) / 8192;
}

static void body_direction(ra_battle *b, ra_battle_unit *u, uint32_t value)
{
    u->body = (ra_battle_turn){value, value, b->tick, 0};
}

static bool reserve(ra_battle *b, ra_battle_unit *u, uint32_t control, uint32_t start, uint32_t end)
{
    uint32_t cells[RA_BATTLE_RESERVED], count = 1, previous = u->cell, d;
    int32_t x, y;
    cells[0] = u->cell;
    for (uint32_t i = start; battle_track_sample(control, i, &x, &y, &d); ++i)
    {
        int64_t px = (int64_t)(end % b->width) * RA_BATTLE_CELL + (int64_t)x * 256 + RA_BATTLE_CELL / 2;
        int64_t py = (int64_t)(ra_battle_cell_y(b, end)) * RA_BATTLE_CELL + (int64_t)y * 256 + RA_BATTLE_CELL / 2;
        if (px < 0 || py < 0 || px >= (int64_t)b->width * RA_BATTLE_CELL || py >= (int64_t)b->height * RA_BATTLE_CELL) return false;
        uint32_t physical = (uint32_t)(py / RA_BATTLE_CELL) * b->width + (uint32_t)(px / RA_BATTLE_CELL), j;
        uint32_t cell = battle_track_node(b, physical, previous, end, u->id);
        if (!ra_battle_passable(b, cell) || (b->occupied[cell] && b->occupied[cell] != u->id)) return false;
        /* 首个跳接采样可能已越过逻辑中心，只核对实际相邻的采样跨格。 */
        if (i > start && cell != previous && !ra_battle_edge(b, previous, cell, u->id)) return false;
        previous = cell;
        for (j = 0; j < count && cells[j] != cell; ++j)
        {
        }
        if (j == count)
        {
            if (count == RA_BATTLE_RESERVED) return false;
            cells[count++] = cell;
        }
    }
    battle_reservations_clear(b, u);
    for (uint32_t i = 0; i < count; ++i) b->occupied[u->reserved[u->reserved_count++] = cells[i]] = u->id;
    return true;
}

static bool start(ra_battle *b, ra_battle_unit *u)
{
    if (u->cell == u->goal) return false;
    if (u->retry)
    {
        --u->retry;
        return false;
    }
    if (u->path_cursor == u->path_count || !ra_battle_edge(b, u->cell, u->path[u->path_cursor], u->id))
    {
        if (!ra_battle_route(b, u->id, u->goal))
        {
            u->retry = RA_BATTLE_HZ;
            ++b->rejected;
            return false;
        }
    }
    if (u->path_cursor >= u->path_count) return false;
    uint32_t first = u->path[u->path_cursor], incoming = direction(b, u->cell, first), control = incoming * 9, end = first, consume = 1;
    ra_battle_turn_start(&u->body, incoming * 8192, b->types[u->type].rot, b->tick);
    if (b->tick - u->body.started < u->body.duration) return false;
    if (u->path_cursor + 1 < u->path_count)
    {
        uint32_t second = u->path[u->path_cursor + 1], candidate = incoming * 8 + direction(b, first, second);
        if ((track_controls[candidate].flags & 8) && ra_battle_edge(b, first, second, u->id) && reserve(b, u, candidate, 0, second))
        {
            control = candidate;
            end = second;
            consume = 2;
        }
    }
    if (consume == 1 && !reserve(b, u, control, 0, end))
    {
        u->retry = RA_BATTLE_HZ;
        return false;
    }
    u->track_control = control;
    u->track_index = 0;
    u->track_active = 1;
    u->track_via = first;
    u->next = end;
    u->path_cursor += consume;
    return true;
}

static void finish(ra_battle *b, ra_battle_unit *u)
{
    battle_reservations_clear(b, u);
    if (b->occupied[u->cell] == u->id) b->occupied[u->cell] = 0;
    u->cell = u->next;
    b->occupied[u->cell] = u->id;
    u->x = (int32_t)(u->cell % b->width * RA_BATTLE_CELL);
    u->y = (int32_t)(ra_battle_cell_y(b, u->cell) * RA_BATTLE_CELL);
    body_direction(b, u, track_controls[u->track_control].direction * 256);
    u->track_active = u->track_index = u->progress = 0;
}

static void join(ra_battle *b, ra_battle_unit *u, const battle_track *old)
{
    if (old->jump < 0 || u->track_index != (uint32_t)old->jump || u->path_cursor >= u->path_count) return;
    uint32_t next = u->path[u->path_cursor], incoming = track_controls[u->track_control].direction / 32;
    uint32_t control = incoming * 8 + direction(b, u->next, next), raw = track_controls[control].raw;
    if (!raw || !tracks[raw].entry || !ra_battle_edge(b, u->next, next, u->id)) return;
    if (!reserve(b, u, control, tracks[raw].entry, next)) return;
    u->track_via = u->next;
    u->next = next;
    u->track_control = control;
    u->track_index = tracks[raw].entry - 1;
    ++u->path_cursor;
    ++u->curve_joins;
}

void battle_move(ra_battle *b, ra_battle_unit *u)
{
    if (!u->health || b->types[u->type].structure) return;
    if (!u->track_active && !start(b, u)) goto facing;
    const ra_battle_type *type = &b->types[u->type];
    int64_t gx = (int64_t)(u->goal % b->width) * RA_BATTLE_CELL - u->x, gy = (int64_t)(ra_battle_cell_y(b, u->goal)) * RA_BATTLE_CELL - u->y;
    int slope = (int)b->tiles[u->next].height - b->tiles[u->cell].height;
    battle_real target = battle_motion_target(type, b->tiles[u->next].track, slope);
    u->motion_factor = battle_motion_factor(type, battle_sqrt((uint64_t)(gx * gx + gy * gy)) / 256, u->motion_factor, target);
    u->speed_factor = (uint32_t)battle_real_integer(battle_real_add(battle_real_mul(u->motion_factor, battle_real_int(10000)), battle_real_ratio(1, 2)));
    u->track_remainder += battle_motion_rate(type, u->motion_factor) / 256;
    /* 最多 1000% 地形修正和 255 基速，单步最多约 365 个采样；上界防御损坏状态。 */
    for (uint32_t steps = 0; steps < 1024 && u->track_active && u->track_remainder > 7; ++steps)
    {
        const battle_track *t = &tracks[track_controls[u->track_control].raw];
        int32_t x, y;
        uint32_t d;
        u->track_remainder -= 7;
        if (!battle_track_sample(u->track_control, u->track_index, &x, &y, &d) || (!x && !y && u->track_index))
        {
            finish(b, u);
            if (u->cell != u->goal) start(b, u);
            continue;
        }
        u->x = (int32_t)(u->next % b->width * RA_BATTLE_CELL) + x * 256;
        u->y = (int32_t)(ra_battle_cell_y(b, u->next) * RA_BATTLE_CELL) + y * 256;
        body_direction(b, u, d * 256);
        if (t->middle >= 0 && u->track_index == (uint32_t)t->middle) u->cell = u->track_via;
        join(b, u, t);
        ++u->track_index;
    }
    if (u->track_active)
    {
        int32_t x, y;
        uint32_t d;
        if (battle_track_sample(u->track_control, u->track_index, &x, &y, &d))
        {
            int32_t tx = (int32_t)(u->next % b->width * RA_BATTLE_CELL) + x * 256, ty = (int32_t)(ra_battle_cell_y(b, u->next) * RA_BATTLE_CELL) + y * 256;
            u->x += battle_track_partial((tx - u->x) / 256, u->track_remainder) * 256;
            u->y += battle_track_partial((ty - u->y) / 256, u->track_remainder) * 256;
        }
        u->progress = u->track_index * 7 + u->track_remainder;
    }
facing:
    u->facing = ((ra_battle_turn_value(&u->body, b->tick) + 4096) & 65535) / 8192;
    if (!u->target && u->order != RA_ORDER_FORCE_GROUND)
        ra_battle_turn_start(&u->turret, ra_battle_turn_value(&u->body, b->tick), b->types[u->type].rot, b->tick);
}
