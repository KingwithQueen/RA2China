#define _CRT_SECURE_NO_WARNINGS
#include "internal.h"
#include "battle_internal.h"
#include <errno.h>
#include <ctype.h>
#include <stdlib.h>
#include <string.h>

static const ra_ini_entry *field(const ra_ini *rules, const ra_ini *local, const char *id, const char *key)
{
    const ra_ini_entry *entry = local ? ra_ini_get(local, id, key) : NULL;
    return entry ? entry : ra_ini_get(rules, id, key);
}

static bool integer(const ra_ini_entry *entry, int32_t fallback, int32_t low, int32_t high, int32_t *value, ra_error *error)
{
    int64_t result = fallback;
    if (entry && !ra_ini_integer(entry, &result, error)) return false;
    if (result < low || result > high) return ra_fail(error, RA_RANGE, entry ? entry->line : 0, "structure field is outside the supported range");
    *value = (int32_t)result;
    return true;
}

static bool height_value(const ra_ini_entry *entry, int32_t *value, ra_error *error)
{
    if (!entry)
    {
        *value = 104;
        return true;
    }
    const char *p = entry->value;
    uint32_t whole = 0, fraction = 0, divisor = 1;
    bool digit = false;
    while (*p == ' ' || *p == '\t') ++p;
    while (isdigit((unsigned char)*p))
    {
        digit = true;
        whole = whole * 10 + (unsigned)(*p++ - '0');
        if (whole > 32) return ra_fail(error, RA_RANGE, entry->line, "structure Height exceeds 32 levels");
    }
    if (*p == '.')
    {
        ++p;
        while (isdigit((unsigned char)*p))
        {
            digit = true;
            if (divisor >= 1000000) return ra_fail(error, RA_RANGE, entry->line, "structure Height has too many decimal digits");
            fraction = fraction * 10 + (unsigned)(*p++ - '0');
            divisor *= 10;
        }
    }
    while (*p == ' ' || *p == '\t') ++p;
    if (!digit || *p || (whole == 32 && fraction)) return ra_fail(error, RA_FORMAT, entry->line, "invalid structure Height");
    *value = (int32_t)(whole * 104 + fraction * 104 / divisor);
    return true;
}

bool ra_battle_structure_rules(ra_battle *b, uint32_t index, const ra_ini *rules, const ra_ini *local, const ra_ini *art, ra_error *error)
{
    static const char *armors[] = {"none", "flak", "plate", "light", "medium", "heavy", "wood", "steel", "concrete", "special_1", "special_2"};
    if (!b || index >= b->type_count || b->tick || b->count || !rules || !art) return ra_fail(error, RA_ARGUMENT, 0, "invalid structure registration");
    ra_battle_type type = b->types[index];
    const ra_ini_entry *image = field(rules, local, type.id, "Image");
    const char *name = image ? image->value : type.id;
    const ra_ini_entry *foundation = ra_ini_get(art, name, "Foundation"), *armor = field(rules, local, type.id, "Armor");
    int width = 1, height = 1;
    char trailing;
    if (!foundation || sscanf(foundation->value, "%dx%d%c", &width, &height, &trailing) != 2 || width < 1 || height < 1 || width > 16 || height > 16)
        return ra_fail(error, RA_FORMAT, foundation ? foundation->line : 0, "unsupported structure foundation: %s", type.id);
    int32_t strength, levels;
    if (!integer(field(rules, local, type.id, "Strength"), 0, 1, 1000000, &strength, error) ||
        !integer(field(rules, local, type.id, "Power"), 0, -1000000, 1000000, &type.power, error) ||
        !height_value(ra_ini_get(art, name, "Height"), &levels, error))
        return false;
    type.armor = armor ? 11u : 0u;
    for (unsigned i = 0; i < 11; ++i)
        if (armor && ra_equal(armor->value, armors[i])) type.armor = i;
    if (type.armor == 11) return ra_fail(error, RA_FORMAT, armor ? armor->line : 0, "unsupported structure armor: %s", type.id);
    type.structure = true;
    const ra_ini_entry *gate = field(rules, local, type.id, "Gate");
    type.gate = gate && (ra_equal(gate->value, "yes") || ra_equal(gate->value, "true"));
    type.foundation_width = (uint32_t)width;
    type.foundation_height = (uint32_t)height;
    type.height = (uint32_t)levels;
    type.strength = (uint32_t)strength;
    type.step = 0;
    /* 建筑武器须逐类实现；不能把激光、驻军或防空建筑误当普通坦克炮。 */
    memset(&type.weapon, 0, sizeof(type.weapon));
    b->types[index] = type;
    return true;
}

static void occupancy(const ra_battle *b, uint32_t *occupied, const ra_battle_unit *u, bool release)
{
    const ra_battle_type *type = &b->types[u->type];
    uint32_t width = type->structure ? type->foundation_width : 1, height = type->structure ? type->foundation_height : 1;
    for (uint32_t y = 0; y < height; ++y)
        for (uint32_t x = 0; x < width; ++x)
        {
            uint32_t cell = u->cell + y * b->width + x;
            if (release)
            {
                if (occupied[cell] == u->id) occupied[cell] = 0;
            }
            else occupied[cell] = u->id;
        }
}

void battle_initial_occupancy(const ra_battle *b, uint32_t *occupied)
{
    for (uint32_t i = 0; i < b->count; ++i)
        if (b->units[i].health && !(b->units[i].traits & RA_UNIT_LIMBO) && !b->types[b->units[i].type].flying && !b->types[b->units[i].type].infantry)
            occupancy(b, occupied, &b->units[i], false);
}

void battle_structure_release(ra_battle *b, const ra_battle_unit *u)
{
    if (b->types[u->type].structure) occupancy(b, b->occupied, u, true);
}

bool ra_battle_spawn_structure(ra_battle *b, uint32_t type, uint32_t team, uint32_t x, uint32_t y, ra_error *error)
{
    return battle_spawn_building(b, type, team, x, y, false, error);
}
bool battle_spawn_building(ra_battle *b, uint32_t type, uint32_t team, uint32_t x, uint32_t y, bool runtime, ra_error *error)
{
    if (!b || !b->tiles || (!runtime && (b->tick || b->command_count)) || type >= b->type_count || !b->types[type].structure || !team ||
        team > RA_BATTLE_TEAMS || b->count == RA_BATTLE_UNITS)
        return ra_fail(error, RA_ARGUMENT, 0, "invalid initial structure");
    const ra_battle_type *definition = &b->types[type];
    if (!definition->foundation_width || !definition->foundation_height || definition->foundation_width > 16 || definition->foundation_height > 16)
        return ra_fail(error, RA_ARGUMENT, 0, "invalid structure foundation dimensions");
    if (x >= b->width || y >= b->height || definition->foundation_width > b->width - x || definition->foundation_height > b->height - y)
        return ra_fail(error, RA_RANGE, 0, "structure foundation exceeds map");
    for (uint32_t row = 0; row < definition->foundation_height; ++row)
        for (uint32_t column = 0; column < definition->foundation_width; ++column)
        {
            uint32_t cell = (y + row) * b->width + x + column;
            /* 原地图建筑可以位于水上或装饰地表，只要求该格存在且不与其他实体重叠。 */
            bool infantry = false;
            for (uint32_t i = 0; i < b->count; ++i)
                if (b->units[i].health && b->types[b->units[i].type].infantry && (b->units[i].cell == cell || b->units[i].next == cell)) infantry = true;
            if (b->tiles[cell].blocked || b->occupied[cell] || infantry) return ra_fail(error, RA_ARGUMENT, 0, "structure foundation is blocked or occupied");
        }
    ra_battle_unit *u = &b->units[b->count];
    memset(u, 0, sizeof(*u));
    u->id = b->count + 1;
    u->type = type;
    u->team = team;
    u->health = definition->strength;
    u->cell = u->next = u->goal = u->destination = u->anchor = y * b->width + x;
    u->x = (int32_t)(x * RA_BATTLE_CELL + (definition->foundation_width - 1) * RA_BATTLE_CELL / 2);
    u->y = (int32_t)(y * RA_BATTLE_CELL + (definition->foundation_height - 1) * RA_BATTLE_CELL / 2);
    u->order = definition->weapon.damage ? RA_ORDER_GUARD : RA_ORDER_STOP;
    occupancy(b, b->occupied, u, false);
    ++b->count;
    if (!runtime)
    {
        b->initial[b->count - 1] = *u;
        b->initial_count = b->count;
    }
    return true;
}

bool ra_battle_allied(const ra_battle *b, uint32_t first, uint32_t second)
{
    if (!b || !first || !second || first > RA_BATTLE_TEAMS || second > RA_BATTLE_TEAMS) return false;
    return first == second || (b->allies[first - 1] & (1u << (second - 1))) != 0;
}

void ra_battle_power(const ra_battle *b, uint32_t team, uint32_t *output, uint32_t *drain)
{
    uint64_t produced = 0, consumed = 0;
    if (b)
        for (uint32_t i = 0; i < b->count; ++i)
        {
            const ra_battle_unit *u = &b->units[i];
            const ra_battle_type *type = &b->types[u->type];
            if (!u->health || u->team != team || !type->structure) continue;
            if (type->power > 0) produced += (uint64_t)(uint32_t)type->power * u->health / type->strength;
            else consumed += (uint32_t)-type->power;
        }
    if (output) *output = produced > UINT32_MAX ? UINT32_MAX : (uint32_t)produced;
    if (drain) *drain = consumed > UINT32_MAX ? UINT32_MAX : (uint32_t)consumed;
}

static int64_t clamp(int64_t value, int64_t low, int64_t high)
{
    return value < low ? low : value > high ? high : value;
}

uint32_t battle_structure_distance(const ra_battle *b, const ra_battle_unit *u, int32_t x, int32_t y, int32_t z)
{
    const ra_battle_type *type = &b->types[u->type];
    int64_t left = (int64_t)(u->cell % b->width) * RA_BATTLE_CELL - RA_BATTLE_CELL / 2;
    int64_t top = (int64_t)(u->cell / b->width) * RA_BATTLE_CELL - RA_BATTLE_CELL / 2;
    int64_t dx = (x - clamp(x, left, left + (int64_t)type->foundation_width * RA_BATTLE_CELL - 1)) / 256;
    int64_t dy = (y - clamp(y, top, top + (int64_t)type->foundation_height * RA_BATTLE_CELL - 1)) / 256;
    int64_t ground = (int64_t)b->tiles[u->cell].height * 104 * 256;
    int64_t dz = (z - clamp(z, ground, ground + (int64_t)type->height * 256)) / 256;
    return battle_sqrt((uint64_t)(dx * dx + dy * dy + dz * dz));
}

void battle_target_point(const ra_battle *b, const ra_battle_unit *source, const ra_battle_unit *target, ra_battle_unit *aim)
{
    aim->id = target->id;
    aim->type = target->type;
    aim->altitude = target->altitude;
    aim->cell = target->cell;
    aim->x = target->x;
    aim->y = target->y;
    aim->track_active = aim->next = aim->reserved_count = 0;
    const ra_battle_type *type = &b->types[target->type];
    if (!type->structure) return;
    int64_t left = (int64_t)(target->cell % b->width) * RA_BATTLE_CELL, top = (int64_t)(target->cell / b->width) * RA_BATTLE_CELL;
    aim->x = (int32_t)clamp(source->x, left, left + (int64_t)(type->foundation_width - 1) * RA_BATTLE_CELL);
    aim->y = (int32_t)clamp(source->y, top, top + (int64_t)(type->foundation_height - 1) * RA_BATTLE_CELL);
    aim->cell = (uint32_t)((aim->y + RA_BATTLE_CELL / 2) / RA_BATTLE_CELL) * b->width + (uint32_t)((aim->x + RA_BATTLE_CELL / 2) / RA_BATTLE_CELL);
}
