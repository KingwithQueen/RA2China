#define _CRT_SECURE_NO_WARNINGS
#include "rules_internal.h"
#include <errno.h>
#include <math.h>
#include <stdlib.h>
#include <string.h>

/* 对象索引与字段汇总共用稳定的 ASCII 名称散列，不依赖系统区域设置。 */
static uint64_t name_hash(ra_rule_domain domain, const char *id)
{
    uint64_t hash = UINT64_C(14695981039346656037) ^ (unsigned)domain;
    while (*id) {
        unsigned c = (uint8_t)*id++;
        if (c >= 'A' && c <= 'Z') c += 32;
        hash = (hash ^ c) * UINT64_C(1099511628211);
    }
    return hash;
}

static void *reserve_array(void *array, size_t count, size_t *capacity, size_t item_size, ra_error *error)
{
    size_t next;
    void *result;
    if (count < *capacity) return array;
    next = *capacity ? *capacity * 2 : 16;
    if (next < *capacity || next > SIZE_MAX / item_size) {
        ra_fail(error, RA_MEMORY, 0, "rule array capacity overflow");
        return NULL;
    }
    result = realloc(array, next * item_size);
    if (!result) {
        ra_fail(error, RA_MEMORY, 0, "rule array allocation failed");
        return NULL;
    }
    *capacity = next;
    return result;
}

size_t ra_rules_find(const ra_rules *rules, ra_rule_domain domain, const char *id)
{
    size_t slot;
    if (!rules || !id || !rules->object_index_capacity) return RA_RULE_NO_INDEX;
    slot = (size_t)name_hash(domain, id) & (rules->object_index_capacity - 1);
    while (rules->object_index[slot]) {
        size_t index = rules->object_index[slot] - 1;
        const ra_rule_object *object = rules->objects + index;
        if (object->domain == domain && ra_equal(object->id, id)) return index;
        slot = (slot + 1) & (rules->object_index_capacity - 1);
    }
    return RA_RULE_NO_INDEX;
}

static bool ensure_object(ra_rules *rules, ra_rule_domain domain, const char *id, uint32_t kinds,
                          bool defined, bool registered, const ra_ini *document, size_t line, ra_error *error)
{
    size_t index = ra_rules_find(rules, domain, id);
    ra_rule_object *object;
    if (index != RA_RULE_NO_INDEX) {
        object = rules->objects + index;
        object->kinds |= kinds;
        object->registered |= registered;
        if (defined && !object->defined) {
            object->document = document;
            object->line = line;
        }
        object->defined |= defined;
        return true;
    }
    object = reserve_array(rules->objects, rules->object_count, &rules->object_capacity, sizeof(*object), error);
    if (!object) return false;
    rules->objects = object;
    object = rules->objects + rules->object_count;
    memset(object, 0, sizeof(*object));
    object->id = ra_copy(id, strlen(id));
    if (!object->id) return ra_fail(error, RA_MEMORY, line, "rule object name allocation failed");
    object->domain = domain;
    object->kinds = kinds;
    object->defined = defined;
    object->registered = registered;
    object->document = document;
    object->line = line;
    index = (size_t)name_hash(domain, id) & (rules->object_index_capacity - 1);
    while (rules->object_index[index]) index = (index + 1) & (rules->object_index_capacity - 1);
    rules->object_index[index] = ++rules->object_count;
    return true;
}

static bool collect_sections(ra_rules *rules, const ra_ini *document, ra_rule_domain domain, ra_error *error)
{
    size_t i;
    if (!document) return true;
    for (i = 0; i < document->section_count; ++i) {
        const ra_ini_section *section = document->sections + i;
        uint32_t kinds = RA_KIND_SECTION;
        if (domain == RA_DOMAIN_ART) kinds |= RA_KIND_ART;
        if (domain == RA_DOMAIN_RULES && (ra_rule_registry(section->name) || ra_equal(section->name, "Sides"))) kinds |= RA_KIND_REGISTRY;
        if (!ensure_object(rules, domain, section->name, kinds, true, false, document, section->line, error)) return false;
    }
    return true;
}

static bool effective(const ra_ini *document, const ra_ini_entry *entry)
{
    return ra_ini_get(document, entry->section, entry->key) == entry;
}

static bool collect_declarations(ra_rules *rules, ra_error *error)
{
    size_t i;
    for (i = 0; i < rules->logic->entry_count; ++i) {
        const ra_ini_entry *entry = rules->logic->entries + i;
        const ra_registry_spec *registry;
        size_t j;
        if (!effective(rules->logic, entry)) continue;
        registry = ra_rule_registry(entry->section);
        if (registry && !ra_rule_null(entry->value)) {
            if (!ensure_object(rules, RA_DOMAIN_RULES, entry->value, registry->kind, false, true, rules->logic, entry->line, error)) return false;
            if (registry->kind == RA_KIND_ANIMATION && rules->art) {
                size_t art = ra_rules_find(rules, RA_DOMAIN_ART, entry->value);
                if (art != RA_RULE_NO_INDEX) rules->objects[art].kinds |= RA_KIND_ANIMATION;
            }
        }
        if (ra_equal(entry->section, "Sides")) {
            if (!ensure_object(rules, RA_DOMAIN_SIDE, entry->key, RA_KIND_SIDE, true, true, rules->logic, entry->line, error)) return false;
        }
        if (!ra_equal(entry->section, "General")) continue;
        for (j = 0; j < ra_rule_group_count; ++j) {
            if (!ra_equal(entry->key, ra_rule_groups[j].field)) continue;
            if (!ensure_object(rules, RA_DOMAIN_GROUP, ra_rule_groups[j].id, RA_KIND_GROUP, true, true, rules->logic, entry->line, error)) return false;
        }
    }
    return true;
}

/* 武器和弹道没有独立总表；先识别明显定义，再沿有类型的引用传播。 */
static void discover_types(ra_rules *rules)
{
    size_t i;
    bool changed;
    for (i = 0; i < rules->object_count; ++i) {
        ra_rule_object *object = rules->objects + i;
        if (object->domain != RA_DOMAIN_RULES || !object->defined) continue;
        if (ra_ini_get(rules->logic, object->id, "Verses")) object->kinds |= RA_KIND_WARHEAD;
        if (object->kinds != RA_KIND_SECTION) continue;
        if (ra_ini_get(rules->logic, object->id, "Projectile") && ra_ini_get(rules->logic, object->id, "Warhead")) object->kinds |= RA_KIND_WEAPON;
        else if (ra_ini_get(rules->logic, object->id, "Inviso") || ra_ini_get(rules->logic, object->id, "Arcing")) object->kinds |= RA_KIND_PROJECTILE;
    }
    do {
        changed = false;
        for (i = 0; i < rules->logic->entry_count; ++i) {
            const ra_ini_entry *entry = rules->logic->entries + i;
            size_t owner = ra_rules_find(rules, RA_DOMAIN_RULES, entry->section);
            size_t target;
            ra_field_spec spec;
            uint32_t meaningful;
            if (!effective(rules->logic, entry) || owner == RA_RULE_NO_INDEX) continue;
            spec = ra_rule_schema(rules->objects + owner, entry);
            if (!spec.reference || spec.list || spec.target_domain != RA_DOMAIN_RULES || ra_rule_null(entry->value)) continue;
            if (!(spec.target_kinds & (RA_KIND_WEAPON | RA_KIND_PROJECTILE | RA_KIND_WARHEAD))) continue;
            target = ra_rules_find(rules, RA_DOMAIN_RULES, entry->value);
            if (target == RA_RULE_NO_INDEX || !rules->objects[target].defined) continue;
            meaningful = rules->objects[target].kinds & ~(uint32_t)(RA_KIND_SECTION | RA_KIND_REGISTRY);
            /* 原版弹头可与国家或动画共用节名，不能仅凭总表将其判成错类型。 */
            if (!(meaningful & spec.target_kinds) && (!meaningful ||
                (spec.target_kinds == RA_KIND_WARHEAD && (meaningful & (RA_KIND_COUNTRY | RA_KIND_ANIMATION))))) {
                rules->objects[target].kinds |= spec.target_kinds;
                changed = true;
            }
        }
    } while (changed);
}

static bool parse_number(const char *text, double *result)
{
    char *end;
    double number;
    errno = 0;
    number = strtod(text, &end);
    if (errno == ERANGE || end == text || !isfinite(number)) return false;
    if (*end == '%' && !end[1]) {
        number /= 100;
        ++end;
    }
    if (*end) return false;
    *result = number;
    return true;
}

static bool collect_fields(ra_rules *rules, const ra_ini *document, ra_rule_domain domain, ra_error *error)
{
    size_t i;
    if (!document) return true;
    for (i = 0; i < document->entry_count; ++i) {
        const ra_ini_entry *entry = document->entries + i;
        size_t owner;
        ra_rule_field *fields;
        ra_rule_field *field;
        ra_rule_object *object;
        ra_field_spec spec;
        size_t *indices;
        if (!effective(document, entry)) continue;
        owner = ra_rules_find(rules, domain, entry->section);
        if (owner == RA_RULE_NO_INDEX) return ra_fail(error, RA_FORMAT, entry->line, "rule section was not indexed");
        fields = reserve_array(rules->fields, rules->field_count, &rules->field_capacity, sizeof(*fields), error);
        if (!fields) return false;
        rules->fields = fields;
        field = rules->fields + rules->field_count;
        memset(field, 0, sizeof(*field));
        field->object = owner;
        field->document = document;
        field->entry = entry;
        field->valid = true;
        object = rules->objects + owner;
        spec = ra_rule_schema(object, entry);
        field->structural = spec.structural;
        field->value_kind = spec.value_kind;
        field->support = spec.reference ? RA_FIELD_REFERENCES : spec.recognized ? RA_FIELD_TYPED : RA_FIELD_RAW;
        if (spec.recognized && !spec.reference) {
            ra_error local = {0};
            if (spec.value_kind == RA_VALUE_INTEGER) field->valid = ra_ini_integer(entry, &field->value.integer, &local);
            else if (spec.value_kind == RA_VALUE_NUMBER) field->valid = parse_number(entry->value, &field->value.number);
            else if (spec.value_kind == RA_VALUE_BOOLEAN) field->valid = ra_ini_boolean(entry, &field->value.boolean, &local);
        }
        if (!field->valid) ++rules->invalid_value_count;
        indices = reserve_array(object->fields, object->field_count, &object->field_capacity, sizeof(*indices), error);
        if (!indices) return false;
        object->fields = indices;
        object->fields[object->field_count++] = rules->field_count++;
    }
    return true;
}

const ra_rule_field *ra_rules_field(const ra_rules *rules, size_t object, const char *key)
{
    size_t i;
    const ra_rule_object *owner;
    if (!rules || !key || object >= rules->object_count) return NULL;
    owner = rules->objects + object;
    for (i = 0; i < owner->field_count; ++i) {
        const ra_rule_field *field = rules->fields + owner->fields[i];
        if (ra_equal(field->entry->key, key)) return field;
    }
    return NULL;
}

static void count_reference(ra_rules *rules, ra_rule_ref_status status)
{
    if (status == RA_REF_RESOLVED) ++rules->resolved_count;
    else if (status == RA_REF_MISSING) ++rules->missing_count;
    else if (status == RA_REF_DECLARED_ONLY) ++rules->declared_only_count;
    else if (status == RA_REF_WRONG_TYPE) ++rules->wrong_type_count;
    else if (status == RA_REF_ASSET_UNCHECKED) ++rules->unchecked_asset_count;
    else if (status == RA_REF_NOT_LOADED) ++rules->unloaded_count;
    else if (status == RA_REF_NULL) ++rules->null_count;
}

static bool add_reference(ra_rules *rules, size_t owner, size_t field, const char *id,
                          ra_field_spec spec, bool implicit, ra_error *error)
{
    ra_rule_reference result = {0};
    ra_rule_reference *references;
    result.owner = owner;
    result.field = field;
    result.target = RA_RULE_NO_INDEX;
    result.target_domain = spec.target_domain;
    result.expected_kinds = spec.target_kinds;
    result.implicit = implicit;
    if (spec.allow_null && ra_rule_null(id)) result.status = RA_REF_NULL;
    else if (spec.target_domain == RA_DOMAIN_ASSET) result.status = RA_REF_ASSET_UNCHECKED;
    else if (spec.target_domain == RA_DOMAIN_ART && !rules->art) result.status = RA_REF_NOT_LOADED;
    else {
        if (spec.prerequisite) {
            result.target = ra_rules_find(rules, RA_DOMAIN_GROUP, id);
            if (result.target != RA_RULE_NO_INDEX) {
                result.target_domain = RA_DOMAIN_GROUP;
                result.expected_kinds = RA_KIND_GROUP;
            }
        }
        if (result.target == RA_RULE_NO_INDEX) result.target = ra_rules_find(rules, spec.target_domain, id);
        if (result.target != RA_RULE_NO_INDEX) {
            ra_rule_object *object = rules->objects + result.target;
            if (spec.target_domain == RA_DOMAIN_ART && spec.target_kinds == RA_KIND_ANIMATION) object->kinds |= RA_KIND_ANIMATION;
            if (!(object->kinds & result.expected_kinds)) result.status = RA_REF_WRONG_TYPE;
            else result.status = object->defined ? RA_REF_RESOLVED : RA_REF_DECLARED_ONLY;
        } else if (spec.target_domain == RA_DOMAIN_ART && spec.art_fallback) result.status = RA_REF_ASSET_UNCHECKED;
        else result.status = RA_REF_MISSING;
    }
    result.target_id = ra_copy(id, strlen(id));
    if (!result.target_id) return ra_fail(error, RA_MEMORY, 0, "reference target allocation failed");
    references = reserve_array(rules->references, rules->reference_count, &rules->reference_capacity, sizeof(*references), error);
    if (!references) {
        free(result.target_id);
        return false;
    }
    rules->references = references;
    rules->references[rules->reference_count++] = result;
    count_reference(rules, result.status);
    return true;
}

static bool field_references(ra_rules *rules, size_t field_index, ra_field_spec spec, ra_error *error)
{
    const ra_rule_field *field = rules->fields + field_index;
    size_t owner = field->object;
    char *text = ra_copy(field->entry->value, strlen(field->entry->value));
    char *cursor;
    if (!text) return ra_fail(error, RA_MEMORY, 0, "reference list allocation failed");
    if (field->document == rules->logic && ra_equal(field->entry->section, "Sides")) owner = ra_rules_find(rules, RA_DOMAIN_SIDE, field->entry->key);
    if (field->document == rules->logic && ra_equal(field->entry->section, "General")) {
        size_t i;
        for (i = 0; i < ra_rule_group_count; ++i) {
            if (ra_equal(field->entry->key, ra_rule_groups[i].field)) owner = ra_rules_find(rules, RA_DOMAIN_GROUP, ra_rule_groups[i].id);
        }
    }
    cursor = text;
    do {
        char *next = spec.list ? strchr(cursor, ',') : NULL;
        char *end;
        if (next) *next++ = 0;
        while (*cursor == ' ' || *cursor == '\t') ++cursor;
        end = cursor + strlen(cursor);
        while (end > cursor && (end[-1] == ' ' || end[-1] == '\t')) *--end = 0;
        if (!add_reference(rules, owner, field_index, cursor, spec, false, error)) {
            free(text);
            return false;
        }
        cursor = next;
    } while (cursor);
    free(text);
    return true;
}

static bool collect_references(ra_rules *rules, ra_error *error)
{
    size_t i;
    for (i = 0; i < rules->field_count; ++i) {
        const ra_rule_field *field = rules->fields + i;
        ra_field_spec spec = ra_rule_schema(rules->objects + field->object, field->entry);
        if (spec.reference && !field_references(rules, i, spec, error)) return false;
    }
    /* 未写 Image 的单位默认映射同名美术；这里仅检查节，不宣称文件存在。 */
    for (i = 0; i < rules->object_count; ++i) {
        const ra_rule_object *object = rules->objects + i;
        ra_field_spec spec = {0};
        uint32_t physical = RA_KIND_UNIT | RA_KIND_PROJECTILE | RA_KIND_TERRAIN | RA_KIND_OVERLAY | RA_KIND_SMUDGE;
        if (object->domain != RA_DOMAIN_RULES || !object->defined || !(object->kinds & physical)) continue;
        if (ra_rules_field(rules, i, "Image")) continue;
        spec.reference = true;
        spec.target_domain = RA_DOMAIN_ART;
        spec.target_kinds = RA_KIND_ART;
        spec.art_fallback = true;
        if (!add_reference(rules, i, RA_RULE_NO_INDEX, object->id, spec, true, error)) return false;
    }
    return true;
}

static bool collect_gaps(ra_rules *rules, ra_error *error)
{
    size_t capacity = 16;
    size_t *index;
    size_t i;
    if (rules->field_count > SIZE_MAX / 2) return ra_fail(error, RA_MEMORY, 0, "field summary capacity overflow");
    while (capacity < rules->field_count * 2) {
        if (capacity > SIZE_MAX / 2) return ra_fail(error, RA_MEMORY, 0, "field summary capacity overflow");
        capacity *= 2;
    }
    index = calloc(capacity, sizeof(*index));
    if (!index) return ra_fail(error, RA_MEMORY, 0, "field summary allocation failed");
    for (i = 0; i < rules->field_count; ++i) {
        const ra_rule_field *field = rules->fields + i;
        ra_rule_domain domain = rules->objects[field->object].domain;
        size_t slot = (size_t)name_hash(domain, field->entry->key) & (capacity - 1);
        ra_rule_gap *gap;
        if (field->structural) continue;
        while (index[slot]) {
            const ra_rule_gap *previous = rules->gaps + index[slot] - 1;
            const ra_rule_field *first = rules->fields + previous->first_field;
            if (rules->objects[first->object].domain == domain && ra_equal(first->entry->key, field->entry->key)) break;
            slot = (slot + 1) & (capacity - 1);
        }
        if (!index[slot]) {
            gap = reserve_array(rules->gaps, rules->gap_count, &rules->gap_capacity, sizeof(*gap), error);
            if (!gap) {
                free(index);
                return false;
            }
            rules->gaps = gap;
            gap = rules->gaps + rules->gap_count;
            memset(gap, 0, sizeof(*gap));
            gap->first_field = i;
            index[slot] = ++rules->gap_count;
        }
        gap = rules->gaps + index[slot] - 1;
        ++gap->occurrences;
        if (field->support == RA_FIELD_RAW) ++gap->raw_count;
        else if (field->support == RA_FIELD_TYPED) ++gap->typed_count;
        else ++gap->reference_count;
    }
    free(index);
    return true;
}

bool ra_rules_build(ra_rules *rules, const ra_ini *logic, const ra_ini *art, ra_error *error)
{
    ra_rules result = {0};
    size_t estimated;
    size_t capacity = 16;
    if (!rules || !logic) return ra_fail(error, RA_ARGUMENT, 0, "rules and logic document are required");
    if (logic->section_count > SIZE_MAX - 16 || logic->entry_count > SIZE_MAX - logic->section_count - 16)
        return ra_fail(error, RA_MEMORY, 0, "rule model capacity overflow");
    estimated = logic->entry_count + logic->section_count + 16;
    if (art) {
        if (art->section_count > SIZE_MAX - estimated) return ra_fail(error, RA_MEMORY, 0, "art model capacity overflow");
        estimated += art->section_count;
    }
    if (estimated > SIZE_MAX / 2) return ra_fail(error, RA_MEMORY, 0, "rule model capacity overflow");
    while (capacity < estimated * 2) {
        if (capacity > SIZE_MAX / 2) return ra_fail(error, RA_MEMORY, 0, "rule model capacity overflow");
        capacity *= 2;
    }
    result.object_index = calloc(capacity, sizeof(*result.object_index));
    if (!result.object_index) return ra_fail(error, RA_MEMORY, 0, "rule model index allocation failed");
    result.object_index_capacity = capacity;
    result.logic = logic;
    result.art = art;
    if (!collect_sections(&result, logic, RA_DOMAIN_RULES, error) || !collect_sections(&result, art, RA_DOMAIN_ART, error)) goto failed;
    if (!collect_declarations(&result, error)) goto failed;
    discover_types(&result);
    if (!collect_fields(&result, logic, RA_DOMAIN_RULES, error) || !collect_fields(&result, art, RA_DOMAIN_ART, error)) goto failed;
    if (!collect_references(&result, error) || !collect_gaps(&result, error)) goto failed;
    *rules = result;
    return true;
failed:
    ra_rules_close(&result);
    return false;
}

bool ra_rules_has_errors(const ra_rules *rules)
{
    return rules && (rules->missing_count || rules->wrong_type_count || rules->invalid_value_count);
}

void ra_rules_close(ra_rules *rules)
{
    size_t i;
    if (!rules) return;
    for (i = 0; i < rules->object_count; ++i) {
        free(rules->objects[i].id);
        free(rules->objects[i].fields);
    }
    for (i = 0; i < rules->reference_count; ++i) free(rules->references[i].target_id);
    free(rules->objects);
    free(rules->fields);
    free(rules->references);
    free(rules->gaps);
    free(rules->object_index);
    memset(rules, 0, sizeof(*rules));
}

const char *ra_rule_domain_name(ra_rule_domain domain)
{
    static const char *names[] = {"rules", "art", "side", "prerequisite_group", "asset"};
    return (unsigned)domain < sizeof(names) / sizeof(*names) ? names[domain] : "unknown";
}

const char *ra_rule_kind_name(uint32_t kind)
{
    static const char *names[] = {"section", "registry", "country", "side", "infantry", "vehicle", "aircraft", "building", "weapon", "projectile", "warhead",
        "animation", "particle", "particle_system", "superweapon", "terrain", "overlay", "smudge", "voxel_animation", "tiberium", "art", "prerequisite_group"};
    unsigned i;
    for (i = 0; i < sizeof(names) / sizeof(*names); ++i) {
        if (kind == (1u << i)) return names[i];
    }
    return "unknown";
}

const char *ra_rule_support_name(ra_rule_support support)
{
    static const char *names[] = {"raw_only", "typed", "reference_checked"};
    return (unsigned)support < sizeof(names) / sizeof(*names) ? names[support] : "unknown";
}

const char *ra_rule_ref_status_name(ra_rule_ref_status status)
{
    static const char *names[] = {"resolved", "missing", "declared_without_definition", "wrong_type", "null", "asset_not_checked", "domain_not_loaded"};
    return (unsigned)status < sizeof(names) / sizeof(*names) ? names[status] : "unknown";
}
