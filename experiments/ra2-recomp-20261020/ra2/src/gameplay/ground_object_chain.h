#pragma once
#include <stdint.h>

typedef struct Ra2ObjectChain
{
    uintptr_t object, cell;
    int32_t classification;
    unsigned pending_contact;
} Ra2ObjectChain;

/* 桥上与地面使用不同对象链；进入遍历时清除待处理接触标记。 */
void ra2_ground_object_chain_begin(Ra2ObjectChain *state, unsigned alternate_layer,
                                 uintptr_t ground_head, uintptr_t upper_head);

/* 对象回调之后，恢复原单元格以及共享参数中的最新分类再继续遍历。 */
void ra2_ground_object_chain_next(Ra2ObjectChain *state, uintptr_t next,
                                uintptr_t saved_cell, int32_t saved_classification);
