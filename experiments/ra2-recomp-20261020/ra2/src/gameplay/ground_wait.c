#include <stdint.h>
#include <string.h>
#include "ground_wait.h"
#include "ground_failure_transition.h"
#include "ground_prepare_exit.h"


static int32_t level_difference(int32_t left, int32_t right)
{
    uint32_t bits = (uint32_t)left - (uint32_t)right;
    if (bits & UINT32_C(0x80000000))
    {
        bits = 0u - bits;
    }
    int32_t result;
    memcpy(&result, &bits, sizeof(result));
    return result;
}

/* 通行后才解析可碾覆盖和层高；每次查询仍使用当时的context。 */
static void resolve_clear_terrain(int32_t overlay,int32_t reference_level,
    Ra2ClearanceResult *result,const Ra2ClearanceServices *services)
{
    if (overlay != -1 && services->query(services->context, RA2_CLEARANCE_OVERLAY_CRUSHABLE))
    {
        result->crush_overlay = 1;
    }
    int32_t level = services->query(services->context, RA2_CLEARANCE_CELL_LEVEL);
    if (level_difference(reference_level, level) >= 2)
    {
        result->target_level = reference_level;
        result->land = 1;
    }
    else
    {
        /* 原版重新查询两次；引擎服务的调用顺序是行为的一部分。 */
        result->target_level = services->query(services->context, RA2_CLEARANCE_CELL_LEVEL);
        result->land = services->query(services->context, RA2_CLEARANCE_CELL_LAND);
    }
}

Ra2ClearancePhase ra2_ground_check_clearance(Ra2GroundPrepareState *state, Ra2WorldPoint invalid_position,
    int32_t passage, int32_t reference_level, int clear_only, Ra2ClearanceResult *result,
    const Ra2ClearanceServices *services)
{
    if (!clear_only)
    {
        int32_t overlay = services->query(services->context, RA2_CLEARANCE_OVERLAY_INDEX);
        if (passage == RA2_CELL_CLEAR)
        {
            resolve_clear_terrain(overlay,reference_level,result,services);
            return RA2_CLEARANCE_TERRAIN_SPEED;
        }
        if (passage != RA2_CELL_GATE)
        {
            return RA2_CLEARANCE_SPECIAL_OBSTACLE;
        }
        services->request_gate(services->context);
    }
    ra2_ground_invalidate_segment(&state->segment_end, &state->driving, invalid_position);
    return passage == RA2_CELL_MOVING_OBSTACLE ? RA2_CLEARANCE_WAIT_FOR_TRAFFIC : RA2_CLEARANCE_OTHER_OBSTACLE;
}

/* 首次阻塞只启动一次；start_wait可改写计时或waiting，调用后不覆盖。 */
static void start_traffic_wait_once(Ra2TrafficWaitState *state,const Ra2TrafficWaitServices *services)
{
    state->waiting = 1;
    state->obstruction.start_frame = services->current_frame(services->context);
    state->obstruction.remaining_frames = services->wait_duration(services->context);
    services->start_wait(services->context, state->obstruction.start_frame, state->obstruction.remaining_frames);
}

static Ra2TrafficWaitPhase rebuild_after_traffic_wait(int mode,const Ra2TrafficWaitServices *services)
{
    int rebuilt = services->rebuild_path(services->context, mode);
    /* 重建服务可替换对象或推进帧；统一出口在服务返回后重新查询。 */
    Ra2PrepareExitServices exit_services = { services->context, services->owner_exists,
        services->write_aborted, services->destination_accepted, services->stop_navigation,
        services->current_frame, services->retry_delay, services->restart_retry };
    return ra2_ground_prepare_after_rebuild(rebuilt, 0, &exit_services)
        ? RA2_TRAFFIC_RETURN_TRUE : RA2_TRAFFIC_RETURN_FALSE;
}

/* 先通过短重试门禁，再按同一帧判断长等待；此选择本身不重置已有等待起点。 */
static int traffic_rebuild_mode(const Ra2TrafficWaitState *state,int32_t frame)
{
    if(!ra2_ground_retry_timer_ready(state->retry,frame))return 0;
    return state->waiting && ra2_ground_retry_timer_ready(state->obstruction,frame) ? 2:1;
}

Ra2TrafficWaitPhase ra2_ground_wait_for_traffic(Ra2TrafficWaitState *state,
    const Ra2TrafficWaitServices *services)
{
    if(!state->waiting)start_traffic_wait_once(state,services);
    int32_t frame=services->current_frame(services->context);
    int mode=traffic_rebuild_mode(state,frame);
    if(!mode)return RA2_TRAFFIC_REPORT_OBSTACLE;
    return rebuild_after_traffic_wait(mode,services);
}
