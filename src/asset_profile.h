#ifndef RA2_ASSET_PROFILE_H
#define RA2_ASSET_PROFILE_H
#include "ra2/assets.h"

/* 根目录只读挂载；中国资源叠加在指定原版目录上，优先级明确递增。 */
bool ra_asset_mount(ra_vfs *vfs, const char *original, const char *mod, ra_error *error);
bool ra_asset_palette(const ra_vfs *vfs, const char *name, ra_palette *palette, ra_error *error);
#endif
