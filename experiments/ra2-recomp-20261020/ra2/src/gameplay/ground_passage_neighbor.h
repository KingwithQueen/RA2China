#pragma once
#include <stdint.h>
typedef struct Ra2NeighborPassageServices {
    void *context;
    uintptr_t (*neighbor)(void *,unsigned);
    uintptr_t (*obstacle)(void *,uintptr_t);
    int32_t (*orientation)(void *,uintptr_t);
} Ra2NeighborPassageServices;
/* 检查前进方向反侧相邻对象；只有方向差为3..5且方向有效才硬阻挡。 */
int ra2_ground_neighbor_blocks(int32_t direction,const Ra2NeighborPassageServices *services);
