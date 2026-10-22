#ifndef RA2_RULES_INTERNAL_H
#define RA2_RULES_INTERNAL_H

#include "internal.h"
#include "ra2/rules.h"

typedef struct { const char *section; uint32_t kind; } ra_registry_spec;
typedef struct { const char *field; const char *id; } ra_group_spec;
typedef struct {
    ra_rule_value_kind value_kind;
    ra_rule_domain target_domain;
    uint32_t target_kinds;
    bool reference;
    bool list;
    bool allow_null;
    bool prerequisite;
    bool structural;
    bool recognized;
    bool art_fallback;
} ra_field_spec;

extern const ra_registry_spec ra_rule_registries[];
extern const size_t ra_rule_registry_count;
extern const ra_group_spec ra_rule_groups[];
extern const size_t ra_rule_group_count;
const ra_registry_spec *ra_rule_registry(const char *section);
ra_field_spec ra_rule_schema(const ra_rule_object *object, const ra_ini_entry *entry);
bool ra_rule_null(const char *value);

#endif
