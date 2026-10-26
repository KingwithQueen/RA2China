#pragma once
#include <stdint.h>
typedef enum Ra2LifecycleQuery {
    RA2_LIFE_DEATH_FRAMES, RA2_LIFE_DEATH_FRAME_UNSET,
    RA2_LIFE_SINKABLE, RA2_LIFE_START_SINK, RA2_LIFE_DEATH_DEFERRED,
    RA2_LIFE_HAS_ATTACHED, RA2_LIFE_HAS_TEAM, RA2_LIFE_HAS_TIMER,
    RA2_LIFE_QUEUE_ROOM, RA2_LIFE_QUEUE_CAN_GROW, RA2_LIFE_QUEUE_GROW,
    RA2_LIFE_QUEUE_NONEMPTY, RA2_LIFE_QUEUE_MORE, RA2_LIFE_READY_TO_DELETE,
    RA2_LIFE_FIND_CURRENT, RA2_LIFE_VALID_INDEX, RA2_LIFE_SHIFT_MORE,
    RA2_LIFE_IS_OBJECT, RA2_LIFE_KEEP_ACTIVE_TYPE
} Ra2LifecycleQuery;
typedef enum Ra2LifecycleOperation {
    RA2_LIFE_CREDIT_KILL, RA2_LIFE_BEGIN_DEATH_FRAME, RA2_LIFE_REVIVE_DELAYED,
    RA2_LIFE_CLEAR_OCCUPATION, RA2_LIFE_STOP_MOTION, RA2_LIFE_CLEAR_MISSION,
    RA2_LIFE_DEATH_MISSION, RA2_LIFE_COMMIT_MISSION, RA2_LIFE_NOTIFY_DEATH,
    RA2_LIFE_UNINIT, RA2_LIFE_CANCEL_ATTACHED, RA2_LIFE_LEAVE_TEAM,
    RA2_LIFE_OBJECT_UNINIT, RA2_LIFE_CANCEL_TIMER, RA2_LIFE_DETACH_REFERENCES,
    RA2_LIFE_LIMBO, RA2_LIFE_MARK_INACTIVE, RA2_LIFE_APPEND_DELETE,
    RA2_LIFE_SELECT_CURRENT, RA2_LIFE_DECREMENT_COUNT, RA2_LIFE_SHIFT_ITEM,
    RA2_LIFE_MARK_CURRENT_ACTIVE, RA2_LIFE_DELETE_CURRENT
} Ra2LifecycleOperation;
typedef struct Ra2LifecycleServices {
    void *context;
    int32_t (*query)(void *context,Ra2LifecycleQuery query,uint32_t index);
    void (*perform)(void *context,Ra2LifecycleOperation operation,uint32_t index);
} Ra2LifecycleServices;
typedef enum Ra2DerivedDeathRoute {
    RA2_DEATH_RETURN, RA2_DEATH_EFFECTS, RA2_DEATH_LIVE_EFFECTS, RA2_DEATH_DELAYED_EFFECTS
} Ra2DerivedDeathRoute;
Ra2DerivedDeathRoute ra2_unit_damage_handoff(const Ra2LifecycleServices *services,int32_t state);
Ra2DerivedDeathRoute ra2_infantry_damage_handoff(const Ra2LifecycleServices *services,int32_t state);
void ra2_finish_derived_death(const Ra2LifecycleServices *services,int unit);
void ra2_uninit_foot(const Ra2LifecycleServices *services);
void ra2_uninit_object(const Ra2LifecycleServices *services);
/* 延迟删除队列在回调之后重新读数量和数组；移除同一对象的所有队列项后才析构。
   不在入队时析构，也不把当前对象缓存为可在析构后读取的指针。 */
void ra2_drain_object_deletions(const Ra2LifecycleServices *services);
