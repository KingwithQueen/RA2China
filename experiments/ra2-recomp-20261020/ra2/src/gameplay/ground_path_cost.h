#ifndef RA2_GROUND_PATH_COST_H
#define RA2_GROUND_PATH_COST_H

#include <stdint.h>

/* 累计一条寻路边的代价。有限非负路径代价；control 是原版 x87 精度及舍入控制字。
 * 单精度保存会影响后续缓存剪枝，不能用默认舍入的 float 加法替代。 */
float ra2_ground_accumulate_path_cost(float previous_cost, float step_cost, uint16_t control);
/* 一条边的评分 = 通行代价 * 搜索权重 + 方向偏置；最后单独保存 float。 */
float ra2_ground_score_path_step(double traversal_cost,float search_weight,float direction_bias,uint16_t control);
/* 队列优先级 = 原版近似距离 + 已累计路径代价。距离服务仍由适配外壳提供。 */
float ra2_ground_path_priority(double approximate_distance,float accumulated_cost,uint16_t control);

#endif
