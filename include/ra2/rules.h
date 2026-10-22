#ifndef RA2_RULES_H
#define RA2_RULES_H

#include "ra2.h"
#include <stdio.h>

/* 名称在所属命名空间中忽略 ASCII 大小写，国家 GDI 与阵营 GDI 不共用对象。 */
typedef enum { RA_DOMAIN_RULES, RA_DOMAIN_ART, RA_DOMAIN_SIDE, RA_DOMAIN_GROUP, RA_DOMAIN_ASSET } ra_rule_domain;
typedef enum {
    RA_KIND_SECTION = 1u << 0,
    RA_KIND_REGISTRY = 1u << 1,
    RA_KIND_COUNTRY = 1u << 2,
    RA_KIND_SIDE = 1u << 3,
    RA_KIND_INFANTRY = 1u << 4,
    RA_KIND_VEHICLE = 1u << 5,
    RA_KIND_AIRCRAFT = 1u << 6,
    RA_KIND_BUILDING = 1u << 7,
    RA_KIND_WEAPON = 1u << 8,
    RA_KIND_PROJECTILE = 1u << 9,
    RA_KIND_WARHEAD = 1u << 10,
    RA_KIND_ANIMATION = 1u << 11,
    RA_KIND_PARTICLE = 1u << 12,
    RA_KIND_PARTICLE_SYSTEM = 1u << 13,
    RA_KIND_SUPERWEAPON = 1u << 14,
    RA_KIND_TERRAIN = 1u << 15,
    RA_KIND_OVERLAY = 1u << 16,
    RA_KIND_SMUDGE = 1u << 17,
    RA_KIND_VOXEL_ANIMATION = 1u << 18,
    RA_KIND_TIBERIUM = 1u << 19,
    RA_KIND_ART = 1u << 20,
    RA_KIND_GROUP = 1u << 21
} ra_rule_kind;

#define RA_KIND_UNIT (RA_KIND_INFANTRY | RA_KIND_VEHICLE | RA_KIND_AIRCRAFT | RA_KIND_BUILDING)
#define RA_RULE_NO_INDEX SIZE_MAX

typedef enum { RA_VALUE_TEXT, RA_VALUE_INTEGER, RA_VALUE_NUMBER, RA_VALUE_BOOLEAN, RA_VALUE_REFERENCE } ra_rule_value_kind;
typedef enum { RA_FIELD_RAW, RA_FIELD_TYPED, RA_FIELD_REFERENCES } ra_rule_support;
typedef enum {
    RA_REF_RESOLVED, RA_REF_MISSING, RA_REF_DECLARED_ONLY, RA_REF_WRONG_TYPE,
    RA_REF_NULL, RA_REF_ASSET_UNCHECKED, RA_REF_NOT_LOADED
} ra_rule_ref_status;

typedef struct {
    char *id;
    ra_rule_domain domain;
    uint32_t kinds;
    bool defined;
    bool registered;
    const ra_ini *document;
    size_t line;
    size_t *fields;
    size_t field_count;
    size_t field_capacity;
} ra_rule_object;

typedef struct {
    size_t object;
    const ra_ini *document;
    const ra_ini_entry *entry;
    ra_rule_value_kind value_kind;
    ra_rule_support support;
    /* 仅对已建立标量类型的字段表示转换结果；原文保留不等于验证通过。 */
    bool valid;
    bool structural;
    union { int64_t integer; double number; bool boolean; } value;
} ra_rule_field;

typedef struct {
    size_t owner;
    size_t field;
    char *target_id;
    ra_rule_domain target_domain;
    uint32_t expected_kinds;
    size_t target;
    ra_rule_ref_status status;
    bool implicit;
} ra_rule_reference;

typedef struct {
    size_t first_field;
    size_t occurrences;
    size_t raw_count;
    size_t typed_count;
    size_t reference_count;
} ra_rule_gap;

typedef struct {
    const ra_ini *logic;
    const ra_ini *art;
    ra_rule_object *objects;
    ra_rule_field *fields;
    ra_rule_reference *references;
    ra_rule_gap *gaps;
    size_t object_count, field_count, reference_count, gap_count;
    size_t object_capacity, field_capacity, reference_capacity, gap_capacity;
    size_t *object_index;
    size_t object_index_capacity;
    size_t missing_count, declared_only_count, wrong_type_count, invalid_value_count;
    size_t resolved_count, unchecked_asset_count, unloaded_count, null_count;
} ra_rules;

/* 模型借用 INI 文档中的字段字符串；先关闭模型，再关闭传入的 INI 文档。
 * 构建成功表示分析完成，不表示缺失引用为零，更不表示字段已经参与游戏运行。
 * art 可以为空，此时美术引用明确标为未加载，不冒充目标缺失。 */
bool ra_rules_build(ra_rules *rules, const ra_ini *logic, const ra_ini *art, ra_error *error);
void ra_rules_close(ra_rules *rules);
size_t ra_rules_find(const ra_rules *rules, ra_rule_domain domain, const char *id);
const ra_rule_field *ra_rules_field(const ra_rules *rules, size_t object, const char *key);
bool ra_rules_has_errors(const ra_rules *rules);
bool ra_rules_write_json(const ra_rules *rules, FILE *output, ra_error *error);
const char *ra_rule_domain_name(ra_rule_domain domain);
const char *ra_rule_kind_name(uint32_t kind);
const char *ra_rule_support_name(ra_rule_support support);
const char *ra_rule_ref_status_name(ra_rule_ref_status status);

#endif
