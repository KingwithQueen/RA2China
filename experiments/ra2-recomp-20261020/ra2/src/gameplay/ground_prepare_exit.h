#pragma once
#include <stdint.h>
typedef struct Ra2PrepareExitServices
{
    void *context;
    int (*owner_exists)(void *context);
    void (*write_aborted)(void *context);
    int (*destination_accepted)(void *context);
    void (*stop_navigation)(void *context);
    int32_t (*current_frame)(void *context);
    int32_t (*retry_delay)(void *context);
    void (*restart_timer)(void *context, int32_t frame, int32_t delay);
} Ra2PrepareExitServices;
/* 重建返回后的共享出口；成功或仍接受目的地时重启计时并返回true。 */
int ra2_ground_prepare_after_rebuild(int rebuilt, int timer_only, const Ra2PrepareExitServices *services);
typedef struct Ra2PreparePendingState { uint8_t sound_pending; int32_t selector; } Ra2PreparePendingState;
void ra2_ground_prepare_clear_pending(Ra2PreparePendingState *state);
