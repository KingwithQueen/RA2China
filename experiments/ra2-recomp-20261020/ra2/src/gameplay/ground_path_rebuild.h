#ifndef RA2_GROUND_PATH_REBUILD_H
#define RA2_GROUND_PATH_REBUILD_H
#include "ground_path_distance.h"
#include "ground_path_nodes.h"
typedef struct Ra2RebuiltPath {
    Ra2PathPoint start;
    int32_t score, length;
    int32_t *directions;
    uint32_t reserved;
    int32_t *surface_levels;
    Ra2PathPoint scratch;
} Ra2RebuiltPath;
typedef Ra2PathPoint (*Ra2PathPointReader)(void *context, void *cell_reference);
/* path_length计入根节点。末槽写-1，上层高度来自每一步的父链。
 * 非相邻格用方向8，交由后续特殊连接处理。合法父链及缓冲容量由调用者保证。 */
void ra2_path_rebuild(const Ra2SearchNode *end, int32_t *directions, int32_t *surface_levels,
    const int32_t direction_table[9], Ra2PathPointReader read_point, void *context, Ra2RebuiltPath *out);
#endif
