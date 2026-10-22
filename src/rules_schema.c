#include "rules_internal.h"
#include <string.h>

const ra_registry_spec ra_rule_registries[] = {
    {"Countries", RA_KIND_COUNTRY}, {"InfantryTypes", RA_KIND_INFANTRY},
    {"VehicleTypes", RA_KIND_VEHICLE}, {"AircraftTypes", RA_KIND_AIRCRAFT},
    {"BuildingTypes", RA_KIND_BUILDING}, {"Warheads", RA_KIND_WARHEAD},
    {"Animations", RA_KIND_ANIMATION}, {"ParticleSystems", RA_KIND_PARTICLE_SYSTEM},
    {"Particles", RA_KIND_PARTICLE}, {"SuperWeaponTypes", RA_KIND_SUPERWEAPON},
    {"TerrainTypes", RA_KIND_TERRAIN}, {"OverlayTypes", RA_KIND_OVERLAY},
    {"SmudgeTypes", RA_KIND_SMUDGE}, {"VoxelAnims", RA_KIND_VOXEL_ANIMATION},
    {"Tiberiums", RA_KIND_TIBERIUM}
};
const size_t ra_rule_registry_count = sizeof(ra_rule_registries) / sizeof(*ra_rule_registries);
const ra_group_spec ra_rule_groups[] = {
    {"PrerequisitePower", "POWER"}, {"PrerequisiteFactory", "FACTORY"},
    {"PrerequisiteBarracks", "BARRACKS"}, {"PrerequisiteRadar", "RADAR"},
    {"PrerequisiteTech", "TECH"}, {"PrerequisiteProc", "PROC"}
};
const size_t ra_rule_group_count = sizeof(ra_rule_groups) / sizeof(*ra_rule_groups);

const ra_registry_spec *ra_rule_registry(const char *section)
{
    size_t i;
    for (i = 0; i < ra_rule_registry_count; ++i) {
        if (ra_equal(section, ra_rule_registries[i].section)) return ra_rule_registries + i;
    }
    return NULL;
}

bool ra_rule_null(const char *value)
{
    return !*value || ra_equal(value, "none") || ra_equal(value, "<none>") || ra_equal(value, "(none)") || ra_equal(value, "null") || ra_equal(value, "<null>");
}

static bool in_names(const char *key, const char *names)
{
    const char *start = names;
    while (*start) {
        const char *end = strchr(start, '|');
        size_t length = end ? (size_t)(end - start) : strlen(start);
        size_t i;
        bool same = strlen(key) == length;
        for (i = 0; same && i < length; ++i) {
            unsigned a = (uint8_t)key[i];
            unsigned b = (uint8_t)start[i];
            if (a >= 'A' && a <= 'Z') a += 32;
            if (b >= 'A' && b <= 'Z') b += 32;
            same = a == b;
        }
        if (same) return true;
        if (!end) break;
        start = end + 1;
    }
    return false;
}

static bool weapon_slot(const char *key)
{
    const char *prefixes[] = {"Weapon", "EliteWeapon"};
    size_t i;
    for (i = 0; i < sizeof(prefixes) / sizeof(*prefixes); ++i) {
        size_t n = strlen(prefixes[i]);
        size_t j;
        char prefix[16];
        if (strlen(key) <= n) continue;
        memcpy(prefix, key, n);
        prefix[n] = 0;
        if (!ra_equal(prefix, prefixes[i])) continue;
        for (j = n; key[j] >= '0' && key[j] <= '9'; ++j) { }
        if (!key[j]) return true;
    }
    return false;
}

static ra_field_spec reference(ra_rule_domain domain, uint32_t kinds, bool list, bool nullable)
{
    ra_field_spec spec = {0};
    spec.value_kind = RA_VALUE_REFERENCE;
    spec.target_domain = domain;
    spec.target_kinds = kinds;
    spec.reference = true;
    spec.recognized = true;
    spec.list = list;
    spec.allow_null = nullable;
    spec.art_fallback = domain == RA_DOMAIN_ART && kinds == RA_KIND_ANIMATION;
    return spec;
}

static ra_field_spec typed(ra_rule_value_kind kind)
{
    ra_field_spec spec = {0};
    spec.value_kind = kind;
    spec.recognized = true;
    return spec;
}

ra_field_spec ra_rule_schema(const ra_rule_object *object, const ra_ini_entry *entry)
{
    ra_field_spec spec = {0};
    const char *key = entry->key;
    uint32_t kinds = object->kinds;
    size_t i;
    const ra_registry_spec *registry = ra_rule_registry(object->id);
    if (object->domain == RA_DOMAIN_RULES && registry) {
        spec = reference(registry->kind == RA_KIND_ANIMATION ? RA_DOMAIN_ART : RA_DOMAIN_RULES, registry->kind, false, false);
        spec.structural = true;
        return spec;
    }
    if (object->domain == RA_DOMAIN_RULES && ra_equal(object->id, "Sides")) {
        spec = reference(RA_DOMAIN_RULES, RA_KIND_COUNTRY, true, false);
        spec.structural = true;
        return spec;
    }
    if (object->domain == RA_DOMAIN_RULES && ra_equal(object->id, "General")) {
        for (i = 0; i < ra_rule_group_count; ++i) {
            if (ra_equal(key, ra_rule_groups[i].field)) {
                spec = reference(RA_DOMAIN_RULES, RA_KIND_BUILDING, true, true);
                spec.structural = true;
                return spec;
            }
        }
        if (in_names(key, "NukeWarhead|C4Warhead|IvanWarhead|V3Warhead|DMislWarhead|V3EliteWarhead|DMislEliteWarhead"))
            return reference(RA_DOMAIN_RULES, RA_KIND_WARHEAD, false, false);
        if (in_names(key, "PrismType|BuildConst|BuildRefinery|BuildBarracks|BuildTech|BuildWeapons|BuildRadar|BuildPower|BuildNavalYard"))
            return reference(RA_DOMAIN_RULES, RA_KIND_BUILDING, true, true);
        if (in_names(key, "Crew|AlliedCrew|SovietCrew|Technician|Engineer|Disguise")) return reference(RA_DOMAIN_RULES, RA_KIND_INFANTRY, false, true);
    }
    if (object->domain == RA_DOMAIN_ART) {
        if (ra_equal(key, "Damage")) return typed(RA_VALUE_NUMBER);
        if (ra_equal(key, "Sequence")) return reference(RA_DOMAIN_ART, RA_KIND_ART, false, true);
        if (in_names(key, "ActiveAnim|ActiveAnimDamaged|ActiveAnimTwo|ActiveAnimTwoDamaged|ActiveAnimThree|ActiveAnimThreeDamaged|"
                          "ActiveAnimFour|ActiveAnimFourDamaged|IdleAnim|IdleAnimDamaged|ProductionAnim|ProductionAnimDamaged|"
                          "SpecialAnim|SpecialAnimDamaged|DeployingAnim|DeployingAnimDamaged|UnderDoorAnim|UnderDoorAnimDamaged|"
                          "RoofDeployingAnim|RoofDeployingAnimDamaged|UnderRoofDoorAnim|UnderRoofDoorAnimDamaged|TrailerAnim|Next"))
            return reference(RA_DOMAIN_ART, RA_KIND_ANIMATION, false, true);
        if (in_names(key, "Image|Cameo|AltCameo|Buildup|BibShape|Palette")) return reference(RA_DOMAIN_ASSET, 0, false, true);
        if (ra_equal(key, "Warhead")) return reference(RA_DOMAIN_RULES, RA_KIND_WARHEAD, false, true);
    }
    if (kinds & RA_KIND_COUNTRY) {
        if (ra_equal(key, "Side")) return reference(RA_DOMAIN_SIDE, RA_KIND_SIDE, false, false);
        if (ra_equal(key, "ParentCountry")) return reference(RA_DOMAIN_RULES, RA_KIND_COUNTRY, false, true);
    }
    if (kinds & RA_KIND_UNIT) {
        if (in_names(key, "Primary|Secondary|ElitePrimary|EliteSecondary|DeathWeapon|EliteDeathWeapon|OccupyWeapon|EliteOccupyWeapon") || weapon_slot(key))
            return reference(RA_DOMAIN_RULES, RA_KIND_WEAPON, false, true);
        if (in_names(key, "Owner|RequiredHouses|ForbiddenHouses")) return reference(RA_DOMAIN_RULES, RA_KIND_COUNTRY, true, true);
        if (in_names(key, "Prerequisite|PrerequisiteOverride")) {
            spec = reference(RA_DOMAIN_RULES, RA_KIND_BUILDING, true, true);
            spec.prerequisite = true;
            return spec;
        }
        if (in_names(key, "DeploysInto|PowersUpBuilding")) return reference(RA_DOMAIN_RULES, RA_KIND_BUILDING, false, true);
        if (ra_equal(key, "UndeploysInto")) return reference(RA_DOMAIN_RULES, RA_KIND_VEHICLE, false, true);
        if (ra_equal(key, "FreeUnit")) return reference(RA_DOMAIN_RULES, RA_KIND_VEHICLE, false, true);
        if (ra_equal(key, "Spawns")) return reference(RA_DOMAIN_RULES, RA_KIND_AIRCRAFT, false, true);
        if (ra_equal(key, "Dock")) return reference(RA_DOMAIN_RULES, RA_KIND_BUILDING, true, true);
        if (in_names(key, "SuperWeapon|SuperWeapon2")) return reference(RA_DOMAIN_RULES, RA_KIND_SUPERWEAPON, false, true);
    }
    if (kinds & (RA_KIND_UNIT | RA_KIND_PROJECTILE | RA_KIND_TERRAIN | RA_KIND_OVERLAY | RA_KIND_SMUDGE)) {
        if (ra_equal(key, "Image")) {
            spec = reference(RA_DOMAIN_ART, RA_KIND_ART, false, true);
            spec.art_fallback = true;
            return spec;
        }
    }
    if (kinds & RA_KIND_WEAPON) {
        if (ra_equal(key, "Projectile")) return reference(RA_DOMAIN_RULES, RA_KIND_PROJECTILE, false, false);
        if (ra_equal(key, "Warhead")) return reference(RA_DOMAIN_RULES, RA_KIND_WARHEAD, false, false);
        if (ra_equal(key, "Anim")) return reference(RA_DOMAIN_ART, RA_KIND_ANIMATION, true, true);
        if (ra_equal(key, "AttachedParticleSystem")) return reference(RA_DOMAIN_RULES, RA_KIND_PARTICLE_SYSTEM, false, true);
    }
    if (kinds & RA_KIND_PROJECTILE) {
        if (in_names(key, "AirburstWeapon|ShrapnelWeapon")) return reference(RA_DOMAIN_RULES, RA_KIND_WEAPON, false, true);
    }
    if ((kinds & RA_KIND_WARHEAD) && ra_equal(key, "AnimList")) return reference(RA_DOMAIN_ART, RA_KIND_ANIMATION, true, true);
    if ((kinds & RA_KIND_SUPERWEAPON) && ra_equal(key, "WeaponType")) return reference(RA_DOMAIN_RULES, RA_KIND_WEAPON, false, true);
    if ((kinds & RA_KIND_PARTICLE_SYSTEM) && ra_equal(key, "HoldsWhat")) return reference(RA_DOMAIN_RULES, RA_KIND_PARTICLE, false, false);
    if ((kinds & RA_KIND_PARTICLE) && ra_equal(key, "NextParticle")) return reference(RA_DOMAIN_RULES, RA_KIND_PARTICLE, false, true);
    if (kinds & (RA_KIND_UNIT | RA_KIND_WEAPON | RA_KIND_PARTICLE | RA_KIND_VOXEL_ANIMATION)) {
        if (in_names(key, "DamageParticleSystems|DestroyParticleSystems")) return reference(RA_DOMAIN_RULES, RA_KIND_PARTICLE_SYSTEM, true, true);
        if (in_names(key, "Explosion|DebrisAnim|DebrisAnims|TrailerAnim")) return reference(RA_DOMAIN_ART, RA_KIND_ANIMATION, true, true);
    }
    if (in_names(key, "Name|UIName")) return typed(RA_VALUE_TEXT);
    if (kinds & (RA_KIND_UNIT | RA_KIND_WEAPON | RA_KIND_WARHEAD | RA_KIND_PROJECTILE | RA_KIND_SUPERWEAPON | RA_KIND_ART)) {
        if (in_names(key, "Strength|Cost|TechLevel|Points|Power|Ammo|Damage|ROF|Burst|Adjacent|Passengers|MaxDebris|MinDebris|InfDeath|Start|End|Rate"))
            return typed(RA_VALUE_INTEGER);
        if (in_names(key, "Speed|Sight|Range|MinimumRange|Size|Weight|Height|ROT|AccelerationFactor|DeaccelerationFactor|"
                          "RechargeTime|ProneDamage|CellSpread|PercentAtMax"))
            return typed(RA_VALUE_NUMBER);
        if (in_names(key, "Turret|Naval|Organic|IsTilter|Accelerates|Crusher|Trainable|SelfHealing|CanBeOccupied|"
                          "IsSelectableCombatant|OpportunityFire|MobileFire|IsPowered|ShowTimer|Powered|Capturable|Crewed|Voxel|"
                          "Remapable|Multiplay|AA|AG|Inviso|Arcing|Bright|Remappable"))
            return typed(RA_VALUE_BOOLEAN);
        if (in_names(key, "Armor|Category|MovementZone|Locomotor|Factory|BuildCat|Action|Type")) return typed(RA_VALUE_TEXT);
    }
    return spec;
}
