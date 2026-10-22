#include "rules_internal.h"
#include <string.h>

/* 旧编码的高位字节使用可恢复的转义，避免生成无效 JSON。 */
static void json_string(FILE *output, const char *text)
{
    ra_view view = {(const uint8_t *)text, strlen(text)};
    bool utf8 = ra_utf8_valid(view);
    fputc('"', output);
    while (*text) {
        unsigned c = (uint8_t)*text++;
        if (c == '"' || c == '\\') {
            fputc('\\', output);
            fputc((int)c, output);
        } else if (c < 32 || (!utf8 && c >= 128)) fprintf(output, "\\u%04x", c);
        else fputc((int)c, output);
    }
    fputc('"', output);
}

static void kind_names(FILE *output, uint32_t kinds)
{
    unsigned i;
    bool comma = false;
    fputc('[', output);
    for (i = 0; i < 22; ++i) {
        if (!(kinds & (1u << i))) continue;
        if (comma) fputc(',', output);
        json_string(output, ra_rule_kind_name(1u << i));
        comma = true;
    }
    fputc(']', output);
}

static void source_location(FILE *output, const ra_ini *document, const char *section, const char *key, size_t line)
{
    fputs("\"source\":", output);
    json_string(output, document->source);
    fputs(",\"section\":", output);
    json_string(output, section);
    fputs(",\"key\":", output);
    json_string(output, key);
    fprintf(output, ",\"line\":%zu", line);
}

static void reference_json(FILE *output, const ra_rules *rules, const ra_rule_reference *reference)
{
    const ra_rule_object *owner = rules->objects + reference->owner;
    fputc('{', output);
    if (reference->field != RA_RULE_NO_INDEX) {
        const ra_rule_field *field = rules->fields + reference->field;
        source_location(output, field->document, field->entry->section, field->entry->key, field->entry->line);
    } else source_location(output, owner->document, owner->id, "Image", owner->line);
    fprintf(output, ",\"owner\":%zu,\"implicit\":%s,\"target_id\":", reference->owner, reference->implicit ? "true" : "false");
    json_string(output, reference->target_id);
    fputs(",\"target_domain\":", output);
    json_string(output, ra_rule_domain_name(reference->target_domain));
    fputs(",\"expected_kinds\":", output);
    kind_names(output, reference->expected_kinds);
    fputs(",\"status\":", output);
    json_string(output, ra_rule_ref_status_name(reference->status));
    if (reference->target == RA_RULE_NO_INDEX) fputs(",\"target_object\":null", output);
    else fprintf(output, ",\"target_object\":%zu", reference->target);
    fputc('}', output);
}

static void fields_json(FILE *output, const ra_rules *rules)
{
    static const char *types[] = {"text", "integer", "number", "boolean", "reference"};
    size_t i;
    fputs(",\"fields\":[", output);
    for (i = 0; i < rules->field_count; ++i) {
        const ra_rule_field *field = rules->fields + i;
        if (i) fputc(',', output);
        fprintf(output, "{\"index\":%zu,\"object\":%zu,", i, field->object);
        source_location(output, field->document, field->entry->section, field->entry->key, field->entry->line);
        fputs(",\"value\":", output);
        json_string(output, field->entry->value);
        fputs(",\"value_type\":", output);
        json_string(output, types[field->value_kind]);
        fputs(",\"data_support\":", output);
        json_string(output, ra_rule_support_name(field->support));
        fputs(",\"valid\":", output);
        if (field->support == RA_FIELD_TYPED) fputs(field->valid ? "true" : "false", output);
        else fputs("null", output);
        fputs(",\"runtime_status\":", output);
        json_string(output, field->structural ? "structural_only" : "not_implemented");
        if (field->support == RA_FIELD_TYPED && field->valid) {
            if (field->value_kind == RA_VALUE_INTEGER) fprintf(output, ",\"decoded\":%lld", (long long)field->value.integer);
            else if (field->value_kind == RA_VALUE_NUMBER) fprintf(output, ",\"decoded\":%.17g", field->value.number);
            else if (field->value_kind == RA_VALUE_BOOLEAN) fprintf(output, ",\"decoded\":%s", field->value.boolean ? "true" : "false");
        }
        fputc('}', output);
    }
    fputc(']', output);
}

bool ra_rules_write_json(const ra_rules *rules, FILE *output, ra_error *error)
{
    size_t i;
    size_t support[3] = {0};
    bool comma = false;
    if (!rules || !output || !rules->logic) return ra_fail(error, RA_ARGUMENT, 0, "invalid rule report arguments");
    for (i = 0; i < rules->field_count; ++i) ++support[rules->fields[i].support];
    fputs("{\"schema_version\":1,\"rules_source\":", output);
    json_string(output, rules->logic->source);
    fputs(",\"art_source\":", output);
    if (rules->art) json_string(output, rules->art->source);
    else fputs("null", output);
    fprintf(output, ",\"summary\":{\"objects\":%zu,\"fields\":%zu,\"references\":%zu,", rules->object_count, rules->field_count, rules->reference_count);
    fprintf(output, "\"resolved\":%zu,\"missing_targets\":%zu,\"declarations_without_definition\":%zu,", rules->resolved_count, rules->missing_count, rules->declared_only_count);
    fprintf(output, "\"wrong_types\":%zu,\"invalid_values\":%zu,\"unchecked_assets\":%zu,", rules->wrong_type_count, rules->invalid_value_count, rules->unchecked_asset_count);
    fprintf(output, "\"unloaded_domains\":%zu,\"null_references\":%zu,\"unimplemented_field_groups\":%zu,", rules->unloaded_count, rules->null_count, rules->gap_count);
    fprintf(output, "\"raw_fields\":%zu,\"typed_fields\":%zu,\"reference_fields\":%zu,\"runtime_fields_implemented\":0},", support[0], support[1], support[2]);
    fputs("\"has_reference_or_value_errors\":", output);
    fputs(ra_rules_has_errors(rules) ? "true" : "false", output);
    fputs(",\"scope\":\"Static checks for explicitly modeled references and scalar fields; resource bytes and gameplay behavior are not verified.\"", output);
    fputs(",\"objects\":[", output);
    for (i = 0; i < rules->object_count; ++i) {
        const ra_rule_object *object = rules->objects + i;
        if (i) fputc(',', output);
        fprintf(output, "{\"index\":%zu,\"id\":", i);
        json_string(output, object->id);
        fputs(",\"domain\":", output);
        json_string(output, ra_rule_domain_name(object->domain));
        fputs(",\"kinds\":", output);
        kind_names(output, object->kinds);
        fprintf(output, ",\"defined\":%s,\"registered\":%s,\"line\":%zu,\"field_count\":%zu,\"source\":",
                object->defined ? "true" : "false", object->registered ? "true" : "false", object->line, object->field_count);
        json_string(output, object->document->source);
        fputc('}', output);
    }
    fputs("],\"references\":[", output);
    for (i = 0; i < rules->reference_count; ++i) {
        if (i) fputc(',', output);
        reference_json(output, rules, rules->references + i);
    }
    fputs("],\"missing_references\":[", output);
    for (i = 0; i < rules->reference_count; ++i) {
        const ra_rule_reference *reference = rules->references + i;
        if (reference->status != RA_REF_MISSING && reference->status != RA_REF_DECLARED_ONLY && reference->status != RA_REF_WRONG_TYPE) continue;
        if (comma) fputc(',', output);
        reference_json(output, rules, reference);
        comma = true;
    }
    fputs("],\"invalid_fields\":[", output);
    comma = false;
    for (i = 0; i < rules->field_count; ++i) {
        const ra_rule_field *field = rules->fields + i;
        if (field->valid) continue;
        if (comma) fputc(',', output);
        fprintf(output, "{\"field\":%zu,", i);
        source_location(output, field->document, field->entry->section, field->entry->key, field->entry->line);
        fputs(",\"value\":", output);
        json_string(output, field->entry->value);
        fputc('}', output);
        comma = true;
    }
    fputs("],\"unimplemented_fields\":[", output);
    for (i = 0; i < rules->gap_count; ++i) {
        const ra_rule_gap *gap = rules->gaps + i;
        const ra_rule_field *field = rules->fields + gap->first_field;
        if (i) fputc(',', output);
        fputs("{\"domain\":", output);
        json_string(output, ra_rule_domain_name(rules->objects[field->object].domain));
        fputs(",\"key\":", output);
        json_string(output, field->entry->key);
        fprintf(output, ",\"occurrences\":%zu,\"raw_only\":%zu,\"typed\":%zu,\"reference_checked\":%zu,",
                gap->occurrences, gap->raw_count, gap->typed_count, gap->reference_count);
        fprintf(output, "\"first_field\":%zu,\"runtime_status\":\"not_implemented\"}", gap->first_field);
    }
    fputc(']', output);
    fields_json(output, rules);
    fputs("}\n", output);
    if (fflush(output) == EOF || ferror(output)) return ra_fail(error, RA_IO, 0, "rule report output failed");
    return true;
}
