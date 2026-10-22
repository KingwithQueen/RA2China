#define _CRT_SECURE_NO_WARNINGS
#include "internal.h"
#include "ra2/battle.h"
#include "battle_number.h"
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

static bool number(const ra_ini *ini, const char *section, const char *key, uint32_t scale, uint32_t fallback, uint32_t *value, ra_error *error)
{
    const ra_ini_entry *e = ra_ini_get(ini, section, key);
    uint64_t whole = 0, fraction = 0, divisor = 1, result;
    const char *p;
    bool digit = false;
    if (!e)
    {
        *value = fallback;
        return true;
    }
    p = e->value;
    while (*p == ' ' || *p == '\t') ++p;
    while (isdigit((unsigned char)*p))
    {
        digit = true;
        whole = whole * 10 + (unsigned)(*p++ - '0');
        if (whole > 10000000) goto invalid;
    }
    if (*p == '.')
    {
        ++p;
        while (isdigit((unsigned char)*p))
        {
            digit = true;
            if (divisor >= 100000000) goto invalid;
            fraction = fraction * 10 + (unsigned)(*p++ - '0');
            divisor *= 10;
        }
    }
    result = whole * divisor + fraction;
    /* 先检查缩放乘法，拒绝可绕回合法射程的超大十进制数。 */
    if (result > UINT64_MAX / scale) goto invalid;
    result = result * scale / divisor;
    if (*p == '%')
    {
        result /= 100;
        ++p;
    }
    while (*p == ' ' || *p == '\t') ++p;
    if (!digit || *p || result > UINT32_MAX) goto invalid;
    *value = (uint32_t)result;
    return true;
invalid:
    return ra_fail(error, RA_SYNTAX, e->line, "unsupported number [%s] %s=%s", section, key, e->value);
}

static bool boolean(const ra_ini *ini, const char *section, const char *key)
{
    const ra_ini_entry *e = ra_ini_get(ini, section, key);
    return e && (ra_equal(e->value, "yes") || ra_equal(e->value, "true") || !strcmp(e->value, "1"));
}

static bool signed_number(const ra_ini *ini, const char *section, const char *key, int32_t fallback, int32_t *result, ra_error *error)
{
    const ra_ini_entry *entry = ra_ini_get(ini, section, key);
    if (!entry)
    {
        *result = fallback;
        return true;
    }
    const char *value = entry->value;
    bool negative = *value == '-';
    uint64_t whole = 0, fraction = 0, divisor = 1;
    bool digit = false;
    if (negative) ++value;
    while (isdigit((unsigned char)*value))
    {
        digit = true;
        whole = whole * 10 + (unsigned)(*value++ - '0');
        if (whole > 10000) break;
    }
    if (*value == '.')
    {
        ++value;
        while (isdigit((unsigned char)*value) && divisor < 10000)
        {
            digit = true;
            fraction = fraction * 10 + (unsigned)(*value++ - '0');
            divisor *= 10;
        }
    }
    while (*value == ' ' || *value == '\t') ++value;
    if (!digit || *value || whole > 10000) return ra_fail(error, RA_RANGE, entry->line, "threat coefficient is outside the supported range");
    uint32_t magnitude = (uint32_t)(whole * 10000 + fraction * 10000 / divisor);
    *result = negative ? -(int32_t)magnitude : (int32_t)magnitude;
    return true;
}

bool ra_battle_type_rules(ra_battle *b, uint32_t index, const ra_ini *rules, ra_error *error)
{
    static const char *armors[11] = {"none", "flak", "plate", "light", "medium", "heavy", "wood", "steel", "concrete", "special_1", "special_2"};
    ra_battle_type type;
    const ra_ini_entry *e, *primary, *projectile, *warhead;
    uint32_t speed, burst;
    bool spawner = false;
    if (!b || index >= b->type_count || b->count || !rules) return ra_fail(error, RA_ARGUMENT, 0, "invalid combat type registration");
    type = b->types[index];
    static const char *coefficient_names[5] = {"DumbMyEffectivenessCoefficient", "DumbTargetEffectivenessCoefficient", "DumbTargetSpecialThreatCoefficient",
                                               "DumbTargetStrengthCoefficient", "DumbTargetDistanceCoefficient"};
    for (unsigned i = 0; i < 5; ++i)
        if (!signed_number(rules, "General", coefficient_names[i], i == 4 ? -10000 : 2000000, &type.threat_coefficients[i], error)) return false;
    if (!signed_number(rules, type.id, "SpecialThreatValue", 0, &type.special_threat, error)) return false;
    primary = ra_ini_get(rules, type.id, "Primary");
    if (primary && strlen(primary->value) >= 32) return ra_fail(error, RA_NOT_FOUND, 0, "primary weapon is missing or too long");
    if (!number(rules, type.id, "Speed", 1, 0, &speed, error) || !number(rules, type.id, "ROT", 1, 5, &type.rot, error) ||
        !number(rules, type.id, "Strength", 1, 0, &type.strength, error) || !number(rules, "General", "TrackedUphill", 10000, 10000, &type.uphill, error) ||
        !number(rules, "General", "TrackedDownhill", 10000, 12000, &type.downhill, error) ||
        !number(rules, type.id, "SlowdownDistance", 1, 500, &type.slowdown, error) ||
        !number(rules, type.id, "Sight", RA_BATTLE_CELL, 8 * RA_BATTLE_CELL, &type.sight, error) ||
        !number(rules, type.id, "GuardRange", RA_BATTLE_CELL, 0, &type.guard_range, error) ||
        !number(rules, type.id, "DeaccelerationFactor", 10000, 20, &type.deceleration, error) ||
        !number(rules, type.id, "AccelerationFactor", 10000, 300, &type.acceleration, error))
        return false;
    type.step = ra_battle_native_speed(speed) * 256;
    e = ra_ini_get(rules, type.id, "Armor");
    type.armor = 11;
    for (unsigned i = 0; i < 11; ++i)
        if (e && ra_equal(e->value, armors[i])) type.armor = i;
    if ((!type.step && !type.structure) || !type.strength || type.strength > 1000000 || type.rot > 127 || type.armor == 11 || type.uphill > 100000 ||
        type.downhill > 100000 || type.deceleration > 10000 || type.acceleration > 10000 || type.sight > 32 * RA_BATTLE_CELL ||
        type.guard_range > 32 * RA_BATTLE_CELL)
        return ra_fail(error, RA_RANGE, 0, "unsupported vehicle motion or armor fields");
    const ra_ini_entry *zone = ra_ini_get(rules, type.id, "MovementZone");
    type.amphibious = zone && !strncmp(zone->value, "Amphibious", 10);
    type.naval = boolean(rules, type.id, "Naval");
    type.flying = zone && ra_equal(zone->value, "Fly");
    e = ra_ini_get(rules, type.id, "CanPassiveAquire");
    type.passive_acquire = !e || boolean(rules, type.id, "CanPassiveAquire");
    if (!number(rules, type.id, "Passengers", 1, 0, &type.passengers, error) || !number(rules, type.id, "Size", 1, 1, &type.size, error) ||
        !number(rules, type.id, "SizeLimit", 1, 1, &type.size_limit, error) || !number(rules, type.id, "JumpjetHeight", 1, 600, &type.flight_height, error) ||
        !number(rules, type.id, "Ammo", 1, 0, &type.ammo, error))
        return false;
    if (type.passengers > 32 || type.size > 100 || type.size_limit > 100 || type.flight_height > 4096 || type.ammo > 100) return false;
    type.engineer = boolean(rules, type.id, "Engineer");
    type.powered = boolean(rules, type.id, "Powered");
    type.c4 = boolean(rules, type.id, "C4");
    type.insignificant = boolean(rules, type.id, "Insignificant");
    if (!number(rules, "General", "C4Delay", 60 * RA_BATTLE_HZ, 27, &type.c4_ticks, error) || type.c4_ticks > 9000) return false;
    if (!primary || type.engineer || ra_equal(primary->value, "none"))
    {
        memset(&type.weapon, 0, sizeof(type.weapon));
        b->types[index] = type;
        return true;
    }
    projectile = ra_ini_get(rules, primary->value, "Projectile");
    warhead = ra_ini_get(rules, primary->value, "Warhead");
    spawner = boolean(rules, primary->value, "Spawner");
    if (spawner)
    {
        const ra_ini_entry *spawn = ra_ini_get(rules, type.id, "Spawns");
        if (!spawn || (!ra_equal(spawn->value, "V3ROCKET") && !ra_equal(spawn->value, "DMISL")))
            return ra_fail(error, RA_RANGE, 0, "unsupported spawn aircraft");
        type.weapon.missile = ra_equal(spawn->value, "V3ROCKET") ? 1 : 2;
    }
    if (!projectile || !warhead || strlen(projectile->value) >= 32 || strlen(warhead->value) >= 32)
        return ra_fail(error, RA_NOT_FOUND, 0, "weapon projectile or warhead is missing");
    strcpy(type.weapon.id, primary->value);
    strcpy(type.weapon.projectile, projectile->value);
    const char *warhead_id = spawner ? (type.weapon.missile == 1 ? "V3WH" : "DMISLWH") : warhead->value;
    strcpy(type.weapon.warhead, warhead_id);
    if (!number(rules, primary->value, "Damage", 1, 0, &type.weapon.damage, error) || !number(rules, primary->value, "ROF", 1, 0, &type.weapon.rof, error) ||
        !number(rules, primary->value, "Range", RA_BATTLE_CELL, 0, &type.weapon.range, error) ||
        !number(rules, primary->value, "Speed", 1, 0, &type.weapon.speed, error) ||
        !number(rules, projectile->value, "ROT", 1, 0, &type.weapon.projectile_rot, error) ||
        !number(rules, "General", "Gravity", 256, 1536, &type.weapon.gravity, error) ||
        !number(rules, warhead_id, "CellSpread", RA_BATTLE_CELL, 0, &type.weapon.spread, error) ||
        !number(rules, warhead_id, "PercentAtMax", 10000, 10000, &type.weapon.percent_at_max, error) ||
        !number(rules, "CombatDamage", "MaxDamage", 1, 10000, &type.weapon.max_damage, error) || !number(rules, primary->value, "Burst", 1, 1, &burst, error))
        return false;
    if (!type.weapon.damage || type.weapon.damage > 100000 || !type.weapon.rof || type.weapon.rof > 10000 || !type.weapon.speed || type.weapon.speed > 1024 ||
        type.weapon.range > 32 * RA_BATTLE_CELL || !type.weapon.range || type.weapon.gravity > 25600 || type.weapon.spread > 8 * RA_BATTLE_CELL ||
        type.weapon.percent_at_max > 10000 || burst > 8 || !burst || type.weapon.projectile_rot > 127)
        return ra_fail(error, RA_RANGE, 0, "weapon is outside the current cannon support range");
    type.weapon.burst = burst;
    if (!number(rules, primary->value, "MinimumRange", RA_BATTLE_CELL, 0, &type.weapon.minimum, error) || type.weapon.minimum >= type.weapon.range)
        return false;
    if (spawner)
    {
        const char *prefix = type.weapon.missile == 1 ? "V3Rocket" : "DMisl";
        char key[64];
        uint32_t tilt, pause;
        snprintf(key, sizeof(key), "%sDamage", prefix);
        if (!number(rules, "General", key, 1, 200, &type.weapon.damage, error)) return false;
        snprintf(key, sizeof(key), "%sAltitude", prefix);
        if (!number(rules, "General", key, 1, 768, &type.weapon.altitude, error)) return false;
        snprintf(key, sizeof(key), "%sTiltFrames", prefix);
        if (!number(rules, "General", key, 1, 60, &tilt, error)) return false;
        snprintf(key, sizeof(key), "%sPauseFrames", prefix);
        if (!number(rules, "General", key, 1, 0, &pause, error)) return false;
        type.weapon.launch_delay = tilt + pause;
        const ra_ini_entry *spawn = ra_ini_get(rules, type.id, "Spawns");
        uint32_t rocket_speed;
        if (!number(rules, spawn->value, "Speed", 1, 15, &rocket_speed, error) || !rocket_speed || rocket_speed > 100) return false;
        type.weapon.speed = ra_battle_native_speed(rocket_speed);
        if (!number(rules, spawn->value, "Strength", 1, 50, &type.weapon.missile_health, error) ||
            !number(rules, type.id, "SpawnRegenRate", 1, 400, &type.weapon.regeneration, error))
            return false;
        if (tilt > 900 || pause > 900 || type.weapon.altitude > 4096 || type.weapon.regeneration > 10000) return false;
    }
    type.instant_weapon = !spawner && boolean(rules, projectile->value, "Inviso");
    type.weapon.arcing = boolean(rules, projectile->value, "Arcing");
    type.weapon.percent_bits = battle_real_float_bits(battle_real_ratio(type.weapon.percent_at_max, 10000));
    type.weapon.cliffs = boolean(rules, projectile->value, "SubjectToCliffs");
    type.weapon.walls = boolean(rules, projectile->value, "SubjectToWalls");
    type.weapon.elevation = boolean(rules, projectile->value, "SubjectToElevation");
    type.weapon.high = boolean(rules, primary->value, "Lobber");
    type.weapon.floater = boolean(rules, projectile->value, "Floater");
    type.weapon.wall = boolean(rules, warhead_id, "Wall");
    e = ra_ini_get(rules, "CombatDamage", "IonCannonWarhead");
    type.weapon.bridge_forced = e && ra_equal(warhead_id, e->value);
    type.weapon.proximity = boolean(rules, projectile->value, "Proximity");
    type.weapon.ranged = boolean(rules, projectile->value, "Ranged");
    if (!number(rules, projectile->value, "Arm", 1, 0, &type.weapon.arm, error) || type.weapon.arm > 10000)
        return ra_fail(error, RA_RANGE, 0, "unsupported projectile Arm");
    type.weapon.aa = boolean(rules, projectile->value, "AA");
    e = ra_ini_get(rules, projectile->value, "AG");
    type.weapon.no_ground = e && !boolean(rules, projectile->value, "AG");
    e = ra_ini_get(rules, warhead_id, "Verses");
    if (!e || strlen(e->value) >= 256) return ra_fail(error, RA_NOT_FOUND, 0, "Verses requires eleven armor values");
    {
        char values[256], *p, *end;
        strcpy(values, e->value);
        p = values;
        for (unsigned i = 0; i < 11; ++i)
        {
            unsigned long value;
            value = strtoul(p, &end, 10);
            if (end == p || value > 100000 || *end != '%') return ra_fail(error, RA_SYNTAX, e->line, "unsupported Verses value");
            type.weapon.verses[i] = (uint32_t)value * 100;
            p = end + 1;
            while (*p == ' ') ++p;
            if (i < 10)
            {
                if (*p++ != ',') return ra_fail(error, RA_SYNTAX, e->line, "Verses needs eleven values");
            }
            else if (*p) return ra_fail(error, RA_SYNTAX, e->line, "extra Verses values");
        }
    }
    b->types[index] = type;
    return true;
}

bool ra_battle_type_art(ra_battle *b, uint32_t index, const ra_ini *rules, const ra_ini *art, ra_error *error)
{
    if (!b || !rules || !art || index >= b->type_count || b->count) return ra_fail(error, RA_ARGUMENT, 0, "invalid muzzle registration");
    const ra_ini_entry *image = ra_ini_get(rules, b->types[index].id, "Image");
    const char *section = image ? image->value : b->types[index].id;
    const ra_ini_entry *entry = ra_ini_get(art, section, "PrimaryFireFLH"), *offset = ra_ini_get(art, section, "TurretOffset");
    int32_t turret_offset = 0;
    if (offset)
    {
        char *end;
        long value = strtol(offset->value, &end, 10);
        while (*end == ' ' || *end == '\t') ++end;
        if (end == offset->value || *end || value < -4096 || value > 4096) return ra_fail(error, RA_RANGE, offset->line, "invalid TurretOffset");
        turret_offset = (int32_t)value;
    }
    if (!entry && !b->types[index].weapon.damage) return true;
    if (!entry) return ra_fail(error, RA_NOT_FOUND, 0, "PrimaryFireFLH is missing");
    const char *p = entry->value;
    int32_t values[3];
    for (unsigned i = 0; i < 3; ++i)
    {
        char *end;
        long value = strtol(p, &end, 10);
        if (p == end || value < -4096 || value > 4096) return ra_fail(error, RA_SYNTAX, entry->line, "invalid PrimaryFireFLH");
        values[i] = (int32_t)value;
        while (*end == ' ' || *end == '\t') ++end;
        if (i < 2 ? *end != ',' : *end != 0) return ra_fail(error, RA_SYNTAX, entry->line, "PrimaryFireFLH requires three integers");
        p = end + (i < 2);
    }
    memcpy(b->types[index].flh, values, sizeof(values));
    b->types[index].turret_offset = turret_offset;
    return true;
}
