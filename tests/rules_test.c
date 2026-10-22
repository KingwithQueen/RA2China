#define _CRT_SECURE_NO_WARNINGS
#include "rules_internal.h"
#include <stdlib.h>
#include <string.h>
#include "entry.h"

static unsigned checks;
static unsigned failures;
#define CHECK(expression)                                                                                                                                      \
    do                                                                                                                                                         \
    {                                                                                                                                                          \
        ++checks;                                                                                                                                              \
        if (!(expression))                                                                                                                                     \
        {                                                                                                                                                      \
            ++failures;                                                                                                                                        \
            fprintf(stderr, "FAIL %s:%d: %s\n", __FILE__, __LINE__, #expression);                                                                              \
            return;                                                                                                                                            \
        }                                                                                                                                                      \
    } while (0)

/* 合成资料覆盖类型总表、隐式武器、阵营同名、通用前置和重复覆盖。 */
static const char *fixture = "[Countries]\n0=GDI\n1=Neutral\n[Sides]\nGDI=GDI,Neutral\n[GDI]\nSide=GDI\n[Neutral]\nSide=GDI\n"
                             "[VehicleTypes]\n0=TANK\n[InfantryTypes]\n0=MAN\n[AircraftTypes]\n0=JET\n[BuildingTypes]\n0=FACT\n"
                             "[Warheads]\n0=AP\n[Animations]\n0=Muzzle\n[ParticleSystems]\n0=SmokeSys\n[Particles]\n0=Smoke\n"
                             "[SuperWeaponTypes]\n0=Nuke\n[General]\nPrerequisiteFactory=FACT\n"
                             "[TANK]\nStrength=100\nCost=200\nSpeed=5.5\nPrimary=OldInvalid\nPrimary=Gun\nSecondary=none\n"
                             "Weapon1=Gun\nWeaponCount=1\nOwner=GDI\nPrerequisite=FACTORY,FACT\nSpawns=JET\nDeploysInto=FACT\n"
                             "Image=TankArt\nCustomExtension=keep-original\nTurret=yes\n[MAN]\nPrimary=Gun\n[JET]\nStrength=50\n"
                             "[FACT]\nUndeploysInto=TANK\n[Gun]\nProjectile=Ball\nWarhead=AP\nDamage=10\nROF=15\nRange=5.75\nAnim=Muzzle\n"
                             "[SpareGun]\nProjectile=Ball\nWarhead=AP\n[Ball]\nInviso=no\nImage=none\n[AP]\nName=Armor piercing\n"
                             "[SmokeSys]\nHoldsWhat=Smoke\n[Smoke]\nName=Smoke\n[Nuke]\nWeaponType=Gun\n";
static const char *art_fixture = "[TankArt]\nVoxel=yes\nCameo=TANKICON\n[MAN]\nSequence=ManSequence\n[ManSequence]\nReady=0,1,1\n"
                                 "[FACT]\nFoundation=2x2\n[JET]\nVoxel=yes\n[Muzzle]\nRate=1\nHeight=1.5\nDamage=.03\n";

static bool parse_model(const char *text, const char *art_text, ra_ini *logic, ra_ini *art, ra_rules *rules, ra_error *error)
{
    ra_view input = {(const uint8_t *)text, strlen(text)};
    if (!ra_ini_parse(logic, input, "合成规则.ini", error)) return false;
    if (art_text)
    {
        input.data = (const uint8_t *)art_text;
        input.size = strlen(art_text);
        if (!ra_ini_parse(art, input, "合成美术.ini", error)) return false;
    }
    return ra_rules_build(rules, logic, art_text ? art : NULL, error);
}

static void close_model(ra_ini *logic, ra_ini *art, ra_rules *rules)
{
    ra_rules_close(rules);
    ra_ini_close(art);
    ra_ini_close(logic);
}

static char *with_suffix(const char *suffix)
{
    size_t length = strlen(fixture) + strlen(suffix) + 1;
    char *text = malloc(length);
    if (text) snprintf(text, length, "%s%s", fixture, suffix);
    return text;
}

static size_t status_count(const ra_rules *rules, const char *target, ra_rule_ref_status status)
{
    size_t result = 0;
    size_t i;
    for (i = 0; i < rules->reference_count; ++i)
    {
        const ra_rule_reference *reference = rules->references + i;
        if (reference->status == status && ra_equal(reference->target_id, target)) ++result;
    }
    return result;
}

static void object_tests(void)
{
    ra_ini logic = {0};
    ra_ini art = {0};
    ra_rules rules = {0};
    ra_error error = {0};
    const ra_rule_field *field;
    size_t tank;
    size_t country;
    size_t side;
    size_t weapon;
    CHECK(parse_model(fixture, art_fixture, &logic, &art, &rules, &error));
    CHECK(!ra_rules_has_errors(&rules));
    CHECK(rules.declared_only_count == 0);
    CHECK(rules.field_count == logic.entry_count + art.entry_count - logic.duplicate_count - art.duplicate_count);
    country = ra_rules_find(&rules, RA_DOMAIN_RULES, "GDI");
    side = ra_rules_find(&rules, RA_DOMAIN_SIDE, "gdi");
    CHECK(country != RA_RULE_NO_INDEX && side != RA_RULE_NO_INDEX && country != side);
    CHECK(rules.objects[country].kinds & RA_KIND_COUNTRY);
    CHECK(rules.objects[side].kinds & RA_KIND_SIDE);
    tank = ra_rules_find(&rules, RA_DOMAIN_RULES, "tank");
    CHECK(tank != RA_RULE_NO_INDEX && (rules.objects[tank].kinds & RA_KIND_VEHICLE));
    field = ra_rules_field(&rules, tank, "sTrEnGtH");
    CHECK(field && field->support == RA_FIELD_TYPED && field->valid && field->value.integer == 100);
    field = ra_rules_field(&rules, tank, "Speed");
    CHECK(field && field->value_kind == RA_VALUE_NUMBER && field->value.number == 5.5);
    field = ra_rules_field(&rules, tank, "CustomExtension");
    CHECK(field && field->support == RA_FIELD_RAW && !strcmp(field->entry->value, "keep-original"));
    CHECK(ra_rules_field(&rules, tank, "WeaponCount")->support == RA_FIELD_RAW);
    CHECK(status_count(&rules, "OldInvalid", RA_REF_MISSING) == 0);
    CHECK(status_count(&rules, "FACTORY", RA_REF_RESOLVED) == 1);
    CHECK(status_count(&rules, "none", RA_REF_NULL) == 2);
    CHECK(status_count(&rules, "TANKICON", RA_REF_ASSET_UNCHECKED) == 1);
    weapon = ra_rules_find(&rules, RA_DOMAIN_RULES, "SpareGun");
    CHECK(weapon != RA_RULE_NO_INDEX && (rules.objects[weapon].kinds & RA_KIND_WEAPON));
    CHECK(!rules.objects[weapon].registered);
    CHECK(ra_rules_find(&rules, RA_DOMAIN_RULES, "missing") == RA_RULE_NO_INDEX);
    CHECK(ra_rules_field(&rules, RA_RULE_NO_INDEX, "Cost") == NULL);
    CHECK(rules.gap_count > 0);
    weapon = ra_rules_find(&rules, RA_DOMAIN_ART, "Muzzle");
    CHECK(ra_rules_field(&rules, weapon, "Damage")->value.number == 0.03);
    CHECK(ra_rules_field(&rules, weapon, "Height")->value.number == 1.5);
    close_model(&logic, &art, &rules);
    CHECK(rules.objects == NULL && rules.references == NULL && rules.object_count == 0);
    CHECK(parse_model("[Countries]\n0=Special\n[Special]\nSide=GDI\n[Sides]\nGDI=Special\n[Warheads]\n0=FX\n[Animations]\n0=FX\n[FX]\nVerses=100%\n[Launcher]"
                      "\nProjectile=Ball\nWarhead=Special\n[Ball]\nInviso=yes\n",
                      art_fixture, &logic, &art, &rules, &error));
    country = ra_rules_find(&rules, RA_DOMAIN_RULES, "Special");
    CHECK((rules.objects[country].kinds & (RA_KIND_COUNTRY | RA_KIND_WARHEAD)) == (RA_KIND_COUNTRY | RA_KIND_WARHEAD));
    CHECK(status_count(&rules, "Special", RA_REF_WRONG_TYPE) == 0);
    close_model(&logic, &art, &rules);
}

static void reference_tests(void)
{
    const char *changes[] = {"[TANK]\nPrimary=MissingGun\n",    "[TANK]\nPrimary=FACT\n",        "[VehicleTypes]\n1=UndefinedVehicle\n",
                             "[TANK]\nImage=UnverifiedAsset\n", "[TANK]\nOwner=GDI,NoCountry\n", "[TANK]\nPrerequisite=MissingGroup\n"};
    const ra_rule_ref_status statuses[] = {RA_REF_MISSING, RA_REF_WRONG_TYPE, RA_REF_DECLARED_ONLY, RA_REF_ASSET_UNCHECKED, RA_REF_MISSING, RA_REF_MISSING};
    const char *targets[] = {"MissingGun", "FACT", "UndefinedVehicle", "UnverifiedAsset", "NoCountry", "MissingGroup"};
    size_t i;
    for (i = 0; i < sizeof(changes) / sizeof(*changes); ++i)
    {
        ra_ini logic = {0};
        ra_ini art = {0};
        ra_rules rules = {0};
        ra_error error = {0};
        char *text = with_suffix(changes[i]);
        CHECK(text != NULL);
        CHECK(parse_model(text, art_fixture, &logic, &art, &rules, &error));
        CHECK(status_count(&rules, targets[i], statuses[i]) == 1);
        if (i == 0 || i == 1 || i == 4 || i == 5) CHECK(ra_rules_has_errors(&rules));
        else CHECK(!ra_rules_has_errors(&rules));
        close_model(&logic, &art, &rules);
        free(text);
    }
    {
        ra_ini logic = {0};
        ra_ini art = {0};
        ra_rules rules = {0};
        ra_error error = {0};
        CHECK(parse_model(fixture, NULL, &logic, &art, &rules, &error));
        CHECK(rules.unloaded_count > 0 && rules.missing_count == 0 && !ra_rules_has_errors(&rules));
        close_model(&logic, &art, &rules);
        CHECK(parse_model(fixture, "[MAN]\nSequence=MissingSequence\n", &logic, &art, &rules, &error));
        CHECK(status_count(&rules, "MissingSequence", RA_REF_MISSING) == 1);
        CHECK(status_count(&rules, "TankArt", RA_REF_ASSET_UNCHECKED) == 1);
        close_model(&logic, &art, &rules);
    }
}

static void value_tests(void)
{
    ra_ini logic = {0};
    ra_ini art = {0};
    ra_rules rules = {0};
    ra_error error = {0};
    size_t tank;
    char *text = with_suffix("[TANK]\nStrength=99999999999999999999999\nSpeed=nan\nTurret=perhaps\n");
    CHECK(text != NULL);
    CHECK(parse_model(text, art_fixture, &logic, &art, &rules, &error));
    CHECK(rules.invalid_value_count == 3 && ra_rules_has_errors(&rules));
    tank = ra_rules_find(&rules, RA_DOMAIN_RULES, "TANK");
    CHECK(!ra_rules_field(&rules, tank, "Strength")->valid);
    close_model(&logic, &art, &rules);
    free(text);
    text = with_suffix("[Gun]\nRange=70%\n");
    CHECK(text != NULL);
    CHECK(parse_model(text, art_fixture, &logic, &art, &rules, &error));
    tank = ra_rules_find(&rules, RA_DOMAIN_RULES, "Gun");
    CHECK(ra_rules_field(&rules, tank, "Range")->value.number == 0.7);
    CHECK(rules.invalid_value_count == 0);
    close_model(&logic, &art, &rules);
    free(text);
    CHECK(!ra_rules_build(&rules, NULL, NULL, &error) && error.code == RA_ARGUMENT);
    CHECK(parse_model("", NULL, &logic, &art, &rules, &error));
    CHECK(rules.object_count == 0 && rules.field_count == 0 && !ra_rules_has_errors(&rules));
    close_model(&logic, &art, &rules);
}

static void scale_tests(void)
{
    const size_t units = 512;
    const size_t capacity = 300000;
    size_t used = 0;
    size_t i;
    char *text = malloc(capacity);
    ra_ini logic = {0};
    ra_ini art = {0};
    ra_rules rules = {0};
    ra_error error = {0};
    CHECK(text != NULL);
    used += (size_t)snprintf(text + used, capacity - used, "[Warheads]\n0=AP\n[AP]\nName=AP\n[VehicleTypes]\n");
    for (i = 0; i < units; ++i) used += (size_t)snprintf(text + used, capacity - used, "%zu=V%zu\n", i, i);
    for (i = 0; i < units; ++i)
    {
        used += (size_t)snprintf(text + used, capacity - used,
                                 "[V%zu]\nPrimary=W%zu\nStrength=%zu\n[W%zu]\nProjectile=P%zu\nWarhead=AP\n[P%zu]\nInviso=yes\nImage=none\n", i, i, i, i, i, i);
    }
    CHECK(used < capacity);
    CHECK(parse_model(text, NULL, &logic, &art, &rules, &error));
    CHECK(rules.missing_count == 0 && rules.wrong_type_count == 0 && rules.invalid_value_count == 0);
    CHECK(rules.unloaded_count == units && rules.null_count == units);
    for (i = 0; i < units; ++i)
    {
        char name[32];
        size_t object;
        const ra_rule_field *field;
        snprintf(name, sizeof(name), "v%zu", i);
        object = ra_rules_find(&rules, RA_DOMAIN_RULES, name);
        CHECK(object != RA_RULE_NO_INDEX);
        field = ra_rules_field(&rules, object, "Strength");
        CHECK(field && field->value.integer == (int64_t)i);
    }
    close_model(&logic, &art, &rules);
    free(text);
}

static void corpus_tests(const char *logic_path, const char *art_path, bool china)
{
    ra_file logic_file = {0};
    ra_file art_file = {0};
    ra_ini logic = {0};
    ra_ini art = {0};
    ra_rules rules = {0};
    ra_error error = {0};
    size_t unit;
    CHECK(ra_file_open(&logic_file, logic_path, &error));
    CHECK(ra_file_open(&art_file, art_path, &error));
    CHECK(ra_ini_parse(&logic, logic_file.view, logic_path, &error));
    CHECK(ra_ini_parse(&art, art_file.view, art_path, &error));
    CHECK(ra_rules_build(&rules, &logic, &art, &error));
    CHECK(rules.field_count == logic.entry_count + art.entry_count - logic.duplicate_count - art.duplicate_count);
    CHECK(status_count(&rules, "Cannon", RA_REF_RESOLVED) > 0);
    CHECK(status_count(&rules, "AP", RA_REF_RESOLVED) > 0);
    CHECK(ra_rules_find(&rules, RA_DOMAIN_RULES, "GDI") != ra_rules_find(&rules, RA_DOMAIN_SIDE, "GDI"));
    unit = ra_rules_find(&rules, RA_DOMAIN_RULES, "CNLTNK");
    if (china)
    {
        const ra_rule_field *field;
        CHECK(unit != RA_RULE_NO_INDEX);
        field = ra_rules_field(&rules, unit, "Strength");
        CHECK(field && field->valid && field->value.integer == 400);
        CHECK(status_count(&rules, "CNAP120", RA_REF_RESOLVED) > 0);
        CHECK(status_count(&rules, "ChinaProbe", RA_REF_RESOLVED) > 0);
    }
    else CHECK(unit == RA_RULE_NO_INDEX);
    printf("CORPUS %s: %zu objects, %zu fields, %zu references\n", china ? "china" : "original", rules.object_count, rules.field_count, rules.reference_count);
    close_model(&logic, &art, &rules);
    ra_file_close(&art_file);
    ra_file_close(&logic_file);
}

static int app_main(int argc, char **argv)
{
    object_tests();
    reference_tests();
    value_tests();
    scale_tests();
    if (argc == 5)
    {
        corpus_tests(argv[1], argv[2], false);
        corpus_tests(argv[3], argv[4], true);
    }
    else if (argc != 1)
    {
        fputs("Usage: ra2rulestests [original-rules original-art china-rules china-art]\n", stderr);
        return 2;
    }
    printf("{\"checks\":%u,\"failures\":%u,\"corpus\":%s}\n", checks, failures, argc == 5 ? "true" : "false");
    return failures ? 1 : 0;
}
