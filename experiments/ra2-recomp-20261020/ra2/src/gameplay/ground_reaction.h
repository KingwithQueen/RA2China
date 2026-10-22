#pragma once
#include "ground_prepare.h"
#include "ground_collision.h"

typedef enum Ra2ReactionEntry
{
    RA2_REACTION_DISPATCH,
    RA2_REACTION_REPORT,
    RA2_REACTION_ATTACK,
    RA2_REACTION_FINISH
} Ra2ReactionEntry;

typedef struct Ra2ReactionServices
{
    void *context;
    int (*sound_pending)(void *context);
    void (*play_sound)(void *context);
    int (*retry_recursively)(void *context, int32_t path_head, uint32_t flags);
    uint32_t (*find_object)(void *context, uint32_t flags);
    int (*object_allied)(void *context, uint32_t object);
    void (*attack_object)(void *context, uint32_t flags);
    int (*has_overlay)(void *context, int32_t missing_index);
    int (*overlay_is_wall)(void *context);
    void (*attack_wall)(void *context, uint32_t flags);
    int (*has_target_488)(void *context);
    void (*cancel_target)(void *context);
    int (*stop_navigation)(void *context, int target_variant);
    void (*clear_pending_and_selector)(void *context);
} Ra2ReactionServices;

/* 0x4A3A8E..0x4A3C92：阻挡提示、攻击可破坏障碍、一次递归重试及最终停止。
   dispatch_code 是入口 EAX，passage 是当前栈帧保存的通行结果，两者不能随意合并。
   path_head/flags 来自共享入口寄存器；常规调用为 -1/0，仍保留其原始位值。 */
int ra2_ground_react_to_obstacle(Ra2GroundPrepareState *state, Ra2WorldPoint invalid_position,
    Ra2ReactionEntry entry, int32_t dispatch_code, int32_t passage, int allow_recursive,
    int32_t path_head, uint32_t flags, const Ra2ReactionServices *services);
