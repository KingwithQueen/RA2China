#pragma once
#include <stdint.h>

typedef enum Ra2BuildingPairQuery {
    RA2_BCP_FIND, RA2_BCP_VALID_INDEX, RA2_BCP_MORE
} Ra2BuildingPairQuery;

typedef enum Ra2BuildingPairOperation {
    RA2_BCP_READ_KEY, RA2_BCP_BEGIN_SHIFT, RA2_BCP_SHIFT_NEXT, RA2_BCP_TRIM_LAST
} Ra2BuildingPairOperation;

typedef struct Ra2BuildingPairServices {
    void *context;
    int32_t (*query)(void *, Ra2BuildingPairQuery);
    void (*perform)(void *, Ra2BuildingPairOperation);
} Ra2BuildingPairServices;

/* 共用键读取/查找继续委托；只清理当前命中的一项，保持其余成对项顺序。 */
void ra2_cleanup_building_pair(const Ra2BuildingPairServices *services);
