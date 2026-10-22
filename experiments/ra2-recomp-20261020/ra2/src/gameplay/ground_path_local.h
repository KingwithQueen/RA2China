#ifndef RA2_GROUND_PATH_LOCAL_H
#define RA2_GROUND_PATH_LOCAL_H
#include "ground_path_distance.h"

typedef struct Ra2LocalPathCell {int32_t ground_level; uint32_t flags;} Ra2LocalPathCell;
typedef struct Ra2LocalPathServices {
    void *context;
    const Ra2PathPoint *offsets;
    const uint16_t *numeric_control;
    double (*owner_factor)(void *context);
    uint32_t (*owner_house)(void *context);
    uintptr_t (*cell_at)(void *context,const Ra2PathPoint *point);
    Ra2LocalPathCell (*cell_properties)(void *context,uintptr_t cell);
    Ra2PathPoint (*connection_exit)(void *context,const Ra2PathPoint *point);
    int32_t (*passage)(void *context,uintptr_t cell,int32_t direction,int32_t level);
    int32_t (*threat)(void *context,const Ra2PathPoint *point,uint32_t house);
} Ra2LocalPathServices;

/* 从段尾反向定位折返锚点，跳过-2；方向8在这里仍按低3位方向处理。
 * directions、levels容量和方向合法性沿用原版路径输出的前提。 */
void ra2_path_find_anchor(const int32_t *directions,int32_t end,int32_t start,
    int32_t *anchor_index,Ra2PathPoint *anchor,const Ra2PathPoint offsets[8]);
/* 保持两段总槽数，尝试中间方向；返回已经推进的前缀长度并写回锚点。 */
int32_t ra2_path_shorten_turn(int32_t *directions,const int32_t *levels,int32_t first_count,
    int32_t second_count,Ra2PathPoint *anchor,const Ra2LocalPathServices *services);
/* 依次尝试“斜向后直向”和交换后的顺序；成功才改写方向，剩余槽标-2。
 * 不改写anchor/delta；final_segment允许少量高威胁格通过。 */
int ra2_path_rewrite_segment(int32_t *directions,int32_t count,const Ra2PathPoint *anchor,
    const Ra2PathPoint *delta,int32_t level,int final_segment,const Ra2LocalPathServices *services);
#endif
