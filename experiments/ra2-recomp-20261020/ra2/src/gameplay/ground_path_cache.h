#ifndef RA2_GROUND_PATH_CACHE_H
#define RA2_GROUND_PATH_CACHE_H
#include <stdint.h>
/* 每轮搜索以 generation 标记有效条目，避免清空整张地图的代价数组。 */
int ra2_ground_path_cache_is_current(uint32_t entry_generation,uint32_t search_generation);
/* 比较缓存代价与 parent_cost + epsilon：-1 小于，0 相等，1 大于。
 * 小于时已有更便宜的路径，可跳过本候选格的内部通行查询。有限非负寻路数据。 */
int ra2_ground_path_cache_compare(float cached_cost,float parent_cost,double epsilon,uint16_t control);
#endif
