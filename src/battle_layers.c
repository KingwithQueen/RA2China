#include "internal.h"
#include "battle_internal.h"

uint32_t ra_battle_cell_y(const ra_battle *b, uint32_t node)
{
    return node / b->width % b->height;
}

bool ra_battle_bridge_add(ra_battle *b, uint32_t cell, uint32_t axis, bool intact, ra_error *error)
{
    if (!b || !b->tiles || b->terrain_sealed || b->tick || b->count || cell >= b->width * b->height || axis < 1 || axis > 2 || b->tiles[cell].height > 123)
        return ra_fail(error, RA_ARGUMENT, 0, "invalid initial bridge surface");
    uint32_t deck = cell + b->width * b->height;
    b->bridges[cell] = (uint8_t)(axis | (intact ? 4u : 0u));
    b->tiles[deck] = (ra_battle_tile){100, (uint8_t)(b->tiles[cell].height + 4), 0, (uint8_t)!intact, 1};
    return true;
}

uint32_t battle_bridge_test(const ra_battle_tile *from, const ra_battle_tile *to, uint32_t ff, uint32_t tf, int32_t *level, bool *transition, bool initial)
{
    /* 原版 4c8730 的高度与桥标志分支；不把桥上标志应用到桥下占格。 */
    if (initial)
    {
        if (*level == -1 && (tf & 0x100)) *level = to->height + 4;
        return 0;
    }
    if (*level == -1 && (ff & 0x100))
    {
        *level = from->height + 4;
        if (!(tf & 0x200)) return 7;
    }
    int delta = ((ff & 0x100) ? from->height : *level) - to->height;
    if (!delta)
    {
        if ((tf & 0x300) == 0x300 && (ff & 0x100)) return 0;
        return *level == -1 || *level == to->height ? 0 : 7;
    }
    if (delta == 1) return to->ramp ? 0 : 7;
    if (delta == -1) return from->ramp ? 0 : 7;
    if (delta != 4 && delta != -4) return 7;
    if (from->height == to->height - 4 && (*level != to->height || !(ff & 0x100))) return 7;
    if (to->height == from->height - 4)
    {
        if ((tf & 0x300) != 0x300) return 7;
        *transition = true;
    }
    return 0;
}

bool battle_bridge_edge(const ra_battle *b, uint32_t from, uint32_t to)
{
    uint32_t n = b->width * b->height, a = from % n, c = to % n;
    if (from < n && to < n) return ra_battle_slope_edge(&b->tiles[a], &b->tiles[c]);
    int32_t level = b->tiles[from].height;
    bool transition = false;
    uint32_t ff = b->bridges[a] ? 0x100u | ((b->bridges[a] & 4) ? 0x200u : 0u) : 0;
    uint32_t tf = b->bridges[c] ? 0x100u | ((b->bridges[c] & 4) ? 0x200u : 0u) : 0;
    if (battle_bridge_test(&b->tiles[a], &b->tiles[c], ff, tf, &level, &transition, false)) return false;
    if ((from < n) != (to < n))
    {
        uint32_t bridge = from >= n ? a : c, axis = b->bridges[bridge] & 3;
        int dx = (int)(a % b->width) - (int)(c % b->width), dy = (int)(a / b->width) - (int)(c / b->width);
        /* 桥口只沿桥长接岸；不允许从侧面横跨栏杆或从桥下垂直跳上桥面。 */
        if (axis == 1 ? dy || !dx : dx || !dy) return false;
    }
    return b->tiles[from].height == b->tiles[to].height;
}

uint32_t battle_track_node(const ra_battle *b, uint32_t physical, uint32_t previous, uint32_t end, uint32_t unit)
{
    uint32_t n = b->width * b->height, same = physical + (previous / n) * n;
    if (same == previous || ra_battle_edge(b, previous, same, unit)) return same;
    uint32_t other = physical + (1 - previous / n) * n;
    if ((physical == end % n || b->bridges[physical]) && ra_battle_edge(b, previous, other, unit)) return other;
    return same;
}

uint32_t ra_battle_unit_layer(const ra_battle *b, const ra_battle_unit *u)
{
    uint32_t n = b->width * b->height;
    if (u->track_active)
    {
        int64_t x = (int64_t)u->x + RA_BATTLE_CELL / 2, y = (int64_t)u->y + RA_BATTLE_CELL / 2;
        if (x >= 0 && y >= 0 && x < (int64_t)b->width * RA_BATTLE_CELL && y < (int64_t)b->height * RA_BATTLE_CELL)
        {
            uint32_t cell = (uint32_t)(y / RA_BATTLE_CELL) * b->width + (uint32_t)(x / RA_BATTLE_CELL);
            for (uint32_t i = 0; i < u->reserved_count; ++i)
                if (u->reserved[i] % n == cell) return u->reserved[i] / n;
        }
    }
    return u->cell / n;
}

int32_t ra_battle_unit_height(const ra_battle *b, const ra_battle_unit *u)
{
    uint32_t n = b->width * b->height;
    if (ra_battle_unit_layer(b, u)) return b->tiles[u->cell >= n ? u->cell : u->next].height * 104;
    return ra_battle_ground_height(b, u->x, u->y) + u->altitude;
}

uint32_t ra_battle_unit_ramp(const ra_battle *b, const ra_battle_unit *u)
{
    if (b->types[u->type].flying || b->types[u->type].naval || ra_battle_unit_layer(b, u)) return 0;
    int64_t x = (int64_t)u->x + RA_BATTLE_CELL / 2, y = (int64_t)u->y + RA_BATTLE_CELL / 2;
    if (x < 0 || y < 0 || x >= (int64_t)b->width * RA_BATTLE_CELL || y >= (int64_t)b->height * RA_BATTLE_CELL) return 0;
    return b->tiles[(uint32_t)(y / RA_BATTLE_CELL) * b->width + (uint32_t)(x / RA_BATTLE_CELL)].ramp;
}

bool ra_battle_targetable(const ra_battle *b, const ra_battle_unit *u, const ra_battle_unit *v, bool automatic, bool force)
{
    if (!b || !u || !v || u == v || !u->health || !v->health || u->type >= b->type_count || v->type >= b->type_count || !u->team || u->team > RA_BATTLE_TEAMS)
        return false;
    const ra_battle_weapon *w = &b->types[u->type].weapon;
    uint32_t mask = 1u << (u->team - 1), invalid = RA_UNIT_LIMBO | RA_UNIT_SINKING | RA_UNIT_UNTARGETABLE | RA_UNIT_SUBMERGED;
    if ((u->traits & invalid) || (v->traits & invalid) || (v->hidden_from & mask)) return false;
    if ((v->traits & RA_UNIT_CLOAKED) && !(v->detected_by & mask) && v->team != u->team) return false;
    if (!force && ra_battle_allied(b, u->team, v->team)) return false;
    if ((v->traits & RA_UNIT_AIRBORNE) ? !w->aa : w->no_ground) return false;
    uint32_t armor = b->types[v->type].armor;
    if (armor >= 11 || !w->damage || !w->verses[armor] || (v->traits & RA_UNIT_IMMUNE)) return false;
    /* 0%、1%、2% 的原版含义依次限制强制攻击、报复和主动索敌。 */
    if (automatic && (!b->types[u->type].passive_acquire || w->verses[armor] <= 200)) return false;
    uint32_t n = b->width * b->height;
    if ((b->bridges[u->cell % n] & 4) && (b->bridges[v->cell % n] & 4) && (ra_battle_unit_layer(b, u) != ra_battle_unit_layer(b, v))) return false;
    return true;
}

uint32_t battle_surface_collision(int32_t previous_z, int32_t z, int32_t ground, int32_t deck, bool bridge)
{
    /* 原版 460497：下穿桥面与上撞桥底采用严格不同的等号边界。 */
    if (bridge && previous_z < deck && z >= deck) return RA_COLLISION_BRIDGE_UP;
    if (bridge && previous_z >= deck && z < deck) return RA_COLLISION_BRIDGE_DOWN;
    return z < ground ? RA_COLLISION_GROUND : RA_COLLISION_NONE;
}

uint32_t battle_fuse(int32_t dx, int32_t dy, int32_t dz, uint32_t *previous)
{
    battle_real x = battle_real_int(dx), y = battle_real_int(dy), z = battle_real_int(dz);
    battle_real sum = battle_real_add(battle_real_add(battle_real_mul(x, x), battle_real_mul(y, y)), battle_real_mul(z, z));
    uint32_t distance = (uint32_t)battle_real_integer(battle_legacy_sqrt(sum)) / 2;
    /* 原版 4ceee0：32 以内起爆，256 以内已越过最近点则给出经过状态。 */
    if (distance < 32) return 1;
    if (distance < 256 && distance > *previous) return 2;
    *previous = distance;
    return 0;
}
