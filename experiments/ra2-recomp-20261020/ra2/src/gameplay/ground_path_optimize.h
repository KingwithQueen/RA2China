#ifndef RA2_GROUND_PATH_OPTIMIZE_H
#define RA2_GROUND_PATH_OPTIMIZE_H
#include "ground_path_rebuild.h"
typedef struct Ra2PathOptimizationServices {
    void *context;
    const Ra2PathPoint *offsets;
    Ra2PathPoint (*connection_exit)(void *context,const Ra2PathPoint *point);
    int32_t (*shorten_turn)(void *context,int32_t *directions,int32_t *levels,int32_t first_count,int32_t second_count,Ra2PathPoint *anchor);
    void (*find_anchor)(void *context,int32_t *directions,int32_t end,int32_t start,int32_t *anchor_index,Ra2PathPoint *anchor);
    void (*rewrite_segment)(void *context,int32_t *directions,int32_t count,Ra2PathPoint *anchor,Ra2PathPoint *delta,int32_t level,int final_segment);
} Ra2PathOptimizationServices;
/* 两段斜向路径识别和折返段后处理。碰撞感知的局部改写由服务提供。 */
void ra2_path_smooth(Ra2RebuiltPath *path,const Ra2PathOptimizationServices *services);
void ra2_path_postprocess(Ra2RebuiltPath *path,const Ra2PathOptimizationServices *services);
#endif
