#include "voxel_internal.h"
#include "voxel_normals.h"
#include <float.h>
#include <stdlib.h>

#define VOXEL_PI 3.14159265358979323846f
typedef struct
{
    float x, y, z;
} projected;

bool ra_voxel_normal(uint8_t type, uint8_t index, float output[3])
{
    if (!output || (type != 2 && type != 4) || index >= (type == 2 ? 36 : 244)) return false;
    memcpy(output, type == 2 ? ts_normals[index] : ra2_normals[index], sizeof(float) * 3);
    return true;
}

bool ra_voxel_transform(const ra_vxl_section *section, const float *matrix, const float point[3], float output[3], ra_error *error)
{
    float local[3], step[3], scale;
    size_t i, j;
    if (!section || !matrix || !point || !output) return ra_fail(error, RA_ARGUMENT, 0, "voxel transform requires section, matrix and points");
    scale = section->scale > 0 ? section->scale : 1.0f;
    for (i = 0; i < 3; ++i)
    {
        if (!section->size[i]) return ra_fail(error, RA_FORMAT, 0, "voxel transform has a zero dimension");
        step[i] = (section->bounds[i + 3] - section->bounds[i]) / section->size[i];
        local[i] = section->bounds[i] + point[i] * step[i];
    }
    for (i = 0; i < 3; ++i)
    {
        float value = matrix[i * 4 + 3] * scale * step[i];
        for (j = 0; j < 3; ++j) value += matrix[i * 4 + j] * local[j];
        output[i] = value * scale;
        if (!isfinite(output[i])) return ra_fail(error, RA_RANGE, 0, "voxel transform produced nonfinite coordinates");
    }
    return true;
}

bool ra_voxel_image_create(ra_voxel_image *image, size_t width, size_t height, ra_error *error)
{
    ra_voxel_image result = {0};
    size_t count;
    if (!image || !width || !height || width > 4096 || height > 4096 || width > SIZE_MAX / height)
        return ra_fail(error, RA_RANGE, 0, "invalid voxel image dimensions");
    count = width * height;
    result.pixels = malloc(count * sizeof(*result.pixels));
    result.depth = malloc(count * sizeof(*result.depth));
    if (!result.pixels || !result.depth)
    {
        ra_voxel_image_close(&result);
        return ra_fail(error, RA_MEMORY, 0, "voxel image allocation failed");
    }
    result.width = width;
    result.height = height;
    *image = result;
    return true;
}

void ra_voxel_image_close(ra_voxel_image *image)
{
    if (!image) return;
    free(image->pixels);
    free(image->depth);
    memset(image, 0, sizeof(*image));
}

static const float *section_matrix(const ra_voxel_part *part, size_t section, size_t frame)
{
    if (!part->hva) return part->vxl->sections[section].transform;
    return part->hva->matrices + ((frame % part->hva->frame_count) * part->hva->section_count + part->mapping[section]) * 12;
}

static projected project_point(const ra_voxel_part *part, const ra_voxel_camera *camera, const float xyz[3], const float chassis[12])
{
    float part_angle = part->yaw * VOXEL_PI / 180.0f, angle = camera->yaw * VOXEL_PI / 180.0f, pitch = camera->pitch * VOXEL_PI / 180.0f;
    float px = cosf(part_angle) * xyz[0] - sinf(part_angle) * xyz[1] + part->offset[0];
    float py = sinf(part_angle) * xyz[0] + cosf(part_angle) * xyz[1] + part->offset[1], pz = xyz[2] + part->offset[2];
    if (chassis)
    {
        float value[3] = {px, py, pz};
        px = chassis[0] * value[0] + chassis[1] * value[1] + chassis[2] * value[2] + chassis[3];
        py = chassis[4] * value[0] + chassis[5] * value[1] + chassis[6] * value[2] + chassis[7];
        pz = chassis[8] * value[0] + chassis[9] * value[1] + chassis[10] * value[2] + chassis[11];
    }
    /* VXL 与地图的 Y 轴相反；底盘和炮塔先在模型坐标中合成，再统一转换。 */
    if (camera->world_axes) py = -py;
    float x = cosf(angle) * px - sinf(angle) * py, y = sinf(angle) * px + cosf(angle) * py;
    projected result = {x, sinf(pitch) * y - cosf(pitch) * pz, cosf(pitch) * y + sinf(pitch) * pz};
    return result;
}

static float edge(projected a, projected b, float x, float y)
{
    return (x - a.x) * (b.y - a.y) - (y - a.y) * (b.x - a.x);
}

static void triangle(ra_voxel_image *image, projected a, projected b, projected c, uint32_t color)
{
    float area = edge(a, b, c.x, c.y), min_x, max_x, min_y, max_y;
    int left, right, top, bottom, x, y;
    if (fabsf(area) < 0.00001f) return;
    min_x = fminf(a.x, fminf(b.x, c.x));
    max_x = fmaxf(a.x, fmaxf(b.x, c.x));
    min_y = fminf(a.y, fminf(b.y, c.y));
    max_y = fmaxf(a.y, fmaxf(b.y, c.y));
    if (max_x < 0 || max_y < 0 || min_x >= image->width || min_y >= image->height) return;
    left = (int)fmaxf(0, floorf(min_x));
    right = (int)fminf((float)image->width - 1, ceilf(max_x));
    top = (int)fmaxf(0, floorf(min_y));
    bottom = (int)fminf((float)image->height - 1, ceilf(max_y));
    for (y = top; y <= bottom; ++y)
    {
        for (x = left; x <= right; ++x)
        {
            float u = edge(b, c, x + 0.5f, y + 0.5f) / area, v = edge(c, a, x + 0.5f, y + 0.5f) / area, w = 1 - u - v;
            size_t at;
            float depth;
            if (u < -0.00001f || v < -0.00001f || w < -0.00001f) continue;
            at = (size_t)y * image->width + (size_t)x;
            depth = u * a.z + v * b.z + w * c.z;
            if (depth > image->depth[at])
            {
                if (image->depth[at] == -FLT_MAX) ++image->drawn_pixels;
                image->depth[at] = depth;
                image->pixels[at] = color;
                if (x < image->min_x) image->min_x = x;
                if (y < image->min_y) image->min_y = y;
                if (x > image->max_x) image->max_x = x;
                if (y > image->max_y) image->max_y = y;
            }
        }
    }
}

static uint32_t voxel_color(const ra_vxl_section *section, const float *matrix, const ra_voxel_part *part, ra_voxel voxel, const ra_palette *palette,
                            const ra_vpl *vpl, const ra_voxel_camera *camera, const float chassis[12])
{
    float normal[3], rotated[3], angle = part->yaw * VOXEL_PI / 180.0f, light = camera->light_yaw * VOXEL_PI / 180.0f;
    float length, dot, brightness;
    unsigned color = voxel.color;
    unsigned remap_start = vpl ? vpl->remap_start : part->vxl->remap_start, remap_end = vpl ? vpl->remap_end : part->vxl->remap_end;
    ra_rgb rgb;
    size_t i;
    if (!ra_voxel_normal(section->normal_type, voxel.normal, normal))
    {
        normal[0] = 0;
        normal[1] = 0;
        normal[2] = 1;
    }
    for (i = 0; i < 3; ++i) rotated[i] = matrix[i * 4] * normal[0] + matrix[i * 4 + 1] * normal[1] + matrix[i * 4 + 2] * normal[2];
    normal[0] = cosf(angle) * rotated[0] - sinf(angle) * rotated[1];
    normal[1] = sinf(angle) * rotated[0] + cosf(angle) * rotated[1];
    normal[2] = rotated[2];
    if (chassis)
    {
        memcpy(rotated, normal, sizeof(rotated));
        for (i = 0; i < 3; ++i) normal[i] = chassis[i * 4] * rotated[0] + chassis[i * 4 + 1] * rotated[1] + chassis[i * 4 + 2] * rotated[2];
    }
    if (camera->world_axes) normal[1] = -normal[1];
    length = sqrtf(normal[0] * normal[0] + normal[1] * normal[1] + normal[2] * normal[2]);
    dot = length > 0.00001f ? (normal[0] * cosf(light) * 0.6f + normal[1] * sinf(light) * 0.6f + normal[2] * 0.8f) / length : 0;
    brightness = 0.65f + 0.35f * fmaxf(0, dot);
    if (camera->use_vpl && vpl && vpl->tables.data)
    {
        size_t shade = (size_t)((1 - brightness) * (vpl->section_count - 1) + 0.5f);
        color = vpl->tables.data[shade * 256 + color];
    }
    rgb = palette->colors[color];
    if (camera->remap && voxel.color >= remap_start && voxel.color <= remap_end && remap_end > remap_start)
    {
        float ramp = (float)(remap_end - voxel.color) / (float)(remap_end - remap_start) * 0.65f + 0.35f;
        rgb.r = (uint8_t)(camera->house_color.r * ramp * brightness);
        rgb.g = (uint8_t)(camera->house_color.g * ramp * brightness);
        rgb.b = (uint8_t)(camera->house_color.b * ramp * brightness);
    }
    return ((uint32_t)rgb.r << 16) | ((uint32_t)rgb.g << 8) | rgb.b;
}

bool ra_voxel_render_chassis(const ra_voxel_part *parts, size_t count, size_t frame, const ra_palette *palette, const ra_vpl *vpl,
                             const ra_voxel_camera *camera, const float chassis[12], ra_voxel_image *image, ra_error *error)
{
    static const unsigned faces[6][4] = {{0, 2, 6, 4}, {1, 5, 7, 3}, {0, 4, 5, 1}, {2, 3, 7, 6}, {0, 1, 3, 2}, {4, 6, 7, 5}};
    static const int neighbors[6][3] = {{-1, 0, 0}, {1, 0, 0}, {0, -1, 0}, {0, 1, 0}, {0, 0, -1}, {0, 0, 1}};
    float bounds[4] = {FLT_MAX, FLT_MAX, -FLT_MAX, -FLT_MAX}, scale, center_x, center_y;
    size_t p, s, i;
    if (!parts || !count || count > 16 || !palette || !camera || !image || !image->pixels || !image->depth)
        return ra_fail(error, RA_ARGUMENT, 0, "invalid voxel render arguments");
    if (!voxel_number(camera->yaw) || !voxel_number(camera->pitch) || !voxel_number(camera->zoom) || camera->zoom <= 0 || camera->zoom > 20 ||
        camera->pitch < -89 || camera->pitch > 89 || !voxel_number(camera->light_yaw) || !voxel_number(camera->pixels_per_unit) ||
        camera->pixels_per_unit < 0 || camera->pixels_per_unit > 1024 || !voxel_number(camera->origin_x) || !voxel_number(camera->origin_y))
        return ra_fail(error, RA_RANGE, 0, "invalid voxel camera");
    if (chassis)
        for (i = 0; i < 12; ++i)
            if (!voxel_number(chassis[i])) return ra_fail(error, RA_RANGE, 0, "invalid chassis matrix");
    for (p = 0; p < count; ++p)
    {
        const ra_voxel_part *part = &parts[p];
        if (!part->vxl || !part->vxl->sections || (part->hva && (!part->mapping || !part->hva->frame_count)))
            return ra_fail(error, RA_ARGUMENT, 0, "voxel part is not initialized");
        if (!voxel_number(part->yaw)) return ra_fail(error, RA_RANGE, 0, "invalid part rotation");
        for (i = 0; i < 3; ++i)
            if (!voxel_number(part->offset[i])) return ra_fail(error, RA_RANGE, 0, "invalid part offset");
        for (s = 0; s < part->vxl->section_count; ++s)
        {
            const ra_vxl_section *section = &part->vxl->sections[s];
            size_t f, frames = part->hva ? part->hva->frame_count : 1;
            if (part->hva && part->mapping[s] >= part->hva->section_count) return ra_fail(error, RA_RANGE, 0, "invalid HVA section mapping");
            for (f = 0; f < frames; ++f)
            {
                const float *matrix = section_matrix(part, s, f);
                for (i = 0; i < 8; ++i)
                {
                    float point[3] = {(i & 1) ? (float)section->size[0] : 0.0f, (i & 2) ? (float)section->size[1] : 0.0f,
                                      (i & 4) ? (float)section->size[2] : 0.0f},
                          world[3];
                    projected q;
                    if (!ra_voxel_transform(section, matrix, point, world, error)) return false;
                    q = project_point(part, camera, world, chassis);
                    bounds[0] = fminf(bounds[0], q.x);
                    bounds[1] = fminf(bounds[1], q.y);
                    bounds[2] = fmaxf(bounds[2], q.x);
                    bounds[3] = fmaxf(bounds[3], q.y);
                }
            }
        }
    }
    if (camera->pixels_per_unit > 0)
    {
        /* 战场不随朝向、炮塔和坡面重新适配包围盒，地面原点始终落在同一像素。 */
        scale = camera->pixels_per_unit * camera->zoom;
        center_x = center_y = 0;
        image->origin_x = camera->origin_x;
        image->origin_y = camera->origin_y;
    }
    else
    {
        scale = fminf((float)image->width / fmaxf(0.001f, bounds[2] - bounds[0]), (float)image->height / fmaxf(0.001f, bounds[3] - bounds[1])) * 0.78f *
                camera->zoom;
        center_x = (bounds[0] + bounds[2]) * 0.5f;
        center_y = (bounds[1] + bounds[3]) * 0.5f;
        image->origin_x = (float)image->width * 0.5f;
        image->origin_y = (float)image->height * 0.5f;
    }
    image->drawn_pixels = 0;
    image->min_x = (int)image->width;
    image->min_y = (int)image->height;
    image->max_x = image->max_y = -1;
    for (i = 0; i < image->width * image->height; ++i)
    {
        image->pixels[i] = ((i % image->width / 32 + i / image->width / 32) & 1) ? 0x253243u : 0x29384au;
        image->depth[i] = -FLT_MAX;
    }
    for (p = 0; p < count; ++p)
    {
        const ra_voxel_part *part = &parts[p];
        for (s = 0; s < part->vxl->section_count; ++s)
        {
            const ra_vxl_section *section = &part->vxl->sections[s];
            const float *matrix = section_matrix(part, s, frame);
            size_t volume = (size_t)section->size[0] * section->size[1] * section->size[2];
            uint8_t *occupied;
            if (camera->section >= 0 && (size_t)camera->section != s) continue;
            occupied = calloc(volume, 1);
            if (!occupied) return ra_fail(error, RA_MEMORY, 0, "voxel visibility allocation failed");
            for (i = 0; i < section->voxel_count; ++i)
            {
                ra_voxel v = section->voxels[i];
                if (v.color) occupied[v.x + (size_t)section->size[0] * (v.y + (size_t)section->size[1] * v.z)] = 1;
            }
            for (i = 0; i < section->voxel_count; ++i)
            {
                ra_voxel v = section->voxels[i];
                projected vertices[8];
                uint32_t color;
                unsigned corner, face;
                if (!v.color) continue;
                color = voxel_color(section, matrix, part, v, palette, vpl, camera, chassis);
                for (corner = 0; corner < 8; ++corner)
                {
                    float point[3] = {(float)v.x + ((corner & 1) != 0), (float)v.y + ((corner & 2) != 0), (float)v.z + ((corner & 4) != 0)}, world[3];
                    if (!ra_voxel_transform(section, matrix, point, world, error))
                    {
                        free(occupied);
                        return false;
                    }
                    vertices[corner] = project_point(part, camera, world, chassis);
                    vertices[corner].x = (vertices[corner].x - center_x) * scale + image->origin_x;
                    vertices[corner].y = (vertices[corner].y - center_y) * scale + image->origin_y;
                }
                for (face = 0; face < 6; ++face)
                {
                    int x = v.x + neighbors[face][0], y = v.y + neighbors[face][1], z = v.z + neighbors[face][2];
                    const unsigned *q = faces[face];
                    if (x >= 0 && y >= 0 && z >= 0 && x < section->size[0] && y < section->size[1] && z < section->size[2] &&
                        occupied[(size_t)x + section->size[0] * ((size_t)y + section->size[1] * (size_t)z)])
                        continue;
                    triangle(image, vertices[q[0]], vertices[q[1]], vertices[q[2]], color);
                    triangle(image, vertices[q[0]], vertices[q[2]], vertices[q[3]], color);
                }
            }
            free(occupied);
        }
    }
    return true;
}

bool ra_voxel_render(const ra_voxel_part *parts, size_t count, size_t frame, const ra_palette *palette, const ra_vpl *vpl, const ra_voxel_camera *camera,
                     ra_voxel_image *image, ra_error *error)
{
    return ra_voxel_render_chassis(parts, count, frame, palette, vpl, camera, NULL, image, error);
}
