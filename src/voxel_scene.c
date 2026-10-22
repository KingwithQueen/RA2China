#include "internal.h"
#include "voxel_scene.h"
#include <stdlib.h>
#include <string.h>

bool voxel_context_open(voxel_context *context, const char *original, const char *mod, ra_error *error)
{
    voxel_context result = {0};
    if (!context) return ra_fail(error, RA_ARGUMENT, 0, "voxel context output is required");
    if (!ra_asset_mount(&result.vfs, original, mod, error) || !ra_vfs_read(&result.vfs, "rules.ini", &result.rule_bytes, error) ||
        !ra_ini_parse(&result.rules, result.rule_bytes.view, result.rule_bytes.source, error) || !ra_vfs_read(&result.vfs, "art.ini", &result.art_bytes, error) ||
        !ra_ini_parse(&result.art, result.art_bytes.view, result.art_bytes.source, error) || !ra_vfs_read(&result.vfs, "ra2.csf", &result.text_bytes, error) ||
        !ra_csf_parse(&result.text, result.text_bytes.view, error) || !ra_vfs_read(&result.vfs, "voxels.vpl", &result.vpl_bytes, error) ||
        !ra_vpl_parse(&result.vpl, result.vpl_bytes.view, error) || !ra_asset_palette(&result.vfs, "unittem.pal", &result.palette, error)) {
        voxel_context_close(&result);
        return false;
    }
    *context = result;
    return true;
}

void voxel_context_close(voxel_context *context)
{
    if (!context) return;
    ra_csf_close(&context->text);
    ra_ini_close(&context->rules);
    ra_ini_close(&context->art);
    ra_resource_close(&context->rule_bytes);
    ra_resource_close(&context->art_bytes);
    ra_resource_close(&context->text_bytes);
    ra_resource_close(&context->vpl_bytes);
    ra_vfs_close(&context->vfs);
    memset(context, 0, sizeof(*context));
}

bool voxel_model_load(voxel_model *model, const ra_vfs *vfs, const char *base, ra_error *error)
{
    voxel_model result = {0};
    ra_resource resource = {0};
    char name[256];
    bool ok = false;
    if (!model || !base || strlen(base) > 240) return ra_fail(error, RA_ARGUMENT, 0, "invalid voxel model name");
    snprintf(name, sizeof(name), "%s.vxl", base);
    if (!ra_vfs_read(vfs, name, &resource, error) || !ra_vxl_parse(&result.vxl, resource.view, error)) goto done;
    result.source = resource.source;
    resource.source = NULL;
    ra_resource_close(&resource);
    snprintf(name, sizeof(name), "%s.hva", base);
    if (!ra_vfs_read(vfs, name, &resource, error) || !ra_hva_parse(&result.hva, resource.view, error)) goto done;
    result.animation_source = resource.source;
    resource.source = NULL;
    result.mapping = calloc(result.vxl.section_count, sizeof(*result.mapping));
    if (!result.mapping) {
        ra_fail(error, RA_MEMORY, 0, "voxel HVA mapping allocation failed");
        goto done;
    }
    if (!ra_hva_bind(&result.vxl, &result.hva, result.mapping, result.vxl.section_count, error)) {
        /* 原版部分单节模型的 HVA 名称不同；仅在无歧义的一对一场景按序连接并报告。 */
        if (result.vxl.section_count != 1 || result.hva.section_count != 1) goto done;
        result.mapping[0] = 0;
        result.index_binding = true;
    }
    *model = result;
    memset(&result, 0, sizeof(result));
    ok = true;
done:
    voxel_model_close(&result);
    ra_resource_close(&resource);
    return ok;
}

void voxel_model_close(voxel_model *model)
{
    if (!model) return;
    ra_vxl_close(&model->vxl);
    ra_hva_close(&model->hva);
    free(model->mapping);
    free(model->source);
    free(model->animation_source);
    memset(model, 0, sizeof(*model));
}

bool voxel_scene_load(voxel_scene *scene, const voxel_context *context, const char *id, bool assemble, ra_error *error)
{
    static const char *suffixes[] = {"tur", "barl"};
    voxel_scene result = {0};
    const ra_ini_entry *image, *ui_name;
    const ra_csf_label *label;
    size_t length, i;
    if (!scene || !context || !id || !(length = strlen(id)) || length >= sizeof(result.id)) return ra_fail(error, RA_ARGUMENT, 0, "invalid voxel scene identifier");
    memcpy(result.id, id, length + 1);
    image = ra_ini_get(&context->rules, id, "Image");
    if (image && strlen(image->value) >= sizeof(result.image)) return ra_fail(error, RA_RANGE, 0, "voxel image identifier is too long");
    snprintf(result.image, sizeof(result.image), "%s", image ? image->value : id);
    length = strlen(result.image);
    if (length > 4 && ra_equal(result.image + length - 4, ".vxl")) result.image[length - 4] = 0;
    ui_name = ra_ini_get(&context->rules, id, "UIName");
    label = ui_name ? ra_csf_get(&context->text, ui_name->value) : NULL;
    result.title = label && label->value_count ? context->text.values[label->first_value].text : NULL;
    if (!voxel_model_load(&result.models[0], &context->vfs, result.image, error)) goto fail;
    result.count = 1;
    if (assemble) {
        for (i = 0; i < 2; ++i) {
            char base[256], file[272];
            ra_resource present = {0};
            snprintf(base, sizeof(base), "%s%s", result.image, suffixes[i]);
            snprintf(file, sizeof(file), "%s.vxl", base);
            if (!ra_vfs_read(&context->vfs, file, &present, error)) {
                if (error && error->code == RA_NOT_FOUND) continue;
                goto fail;
            }
            ra_resource_close(&present);
            if (!voxel_model_load(&result.models[result.count], &context->vfs, base, error)) goto fail;
            ++result.count;
        }
    }
    result.frames = 1;
    for (i = 0; i < result.count; ++i) if (result.models[i].hva.frame_count > result.frames) result.frames = result.models[i].hva.frame_count;
    *scene = result;
    /* 发布对象后再连接内部指针，避免指向栈上临时场景。 */
    for (i = 0; i < scene->count; ++i) {
        scene->parts[i].vxl = &scene->models[i].vxl;
        scene->parts[i].hva = &scene->models[i].hva;
        scene->parts[i].mapping = scene->models[i].mapping;
    }
    return true;
fail:
    voxel_scene_close(&result);
    return false;
}

void voxel_scene_close(voxel_scene *scene)
{
    size_t i;
    if (!scene) return;
    for (i = 0; i < 3; ++i) voxel_model_close(&scene->models[i]);
    memset(scene, 0, sizeof(*scene));
}
