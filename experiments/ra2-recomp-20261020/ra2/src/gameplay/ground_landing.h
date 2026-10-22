#pragma once
#include "unit_movement.h"

typedef struct Ra2LandingServices
{
    void *context;
    int32_t (*selector)(void *context);
    void (*leave_cell)(void *context);
    void (*clear_segment)(void *context);
    int32_t (*connection_index)(void *context);
    int (*connection_exists)(void *context, int32_t index);
    void (*start_connection)(void *context, int32_t index);
    void (*set_approach_point)(void *context);
    int32_t (*current_ground_height)(void *context);
    int32_t (*target_ground_height)(void *context, int32_t *duration);
    void (*finish_connection)(void *context, int32_t height);
    void (*reject_connection)(void *context);
} Ra2LandingServices;
/* 方向8的特殊连接落位。已有模板继续普通采样，其余路径均在本帧返回false。 */
int ra2_ground_land_connection(const Ra2LandingServices *services);

/* Advance拒绝方向时按原寄存器值清路径；普通false出口不改变其他移动状态。 */
void ra2_ground_reject_direction(int32_t *path_head, int32_t rejected_value);
