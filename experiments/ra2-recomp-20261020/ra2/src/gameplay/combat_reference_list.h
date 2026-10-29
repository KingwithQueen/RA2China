#pragma once
#include <stdint.h>

typedef struct Ra2ReferenceListServices {
    void *context;
    int32_t (*begin_positive)(void *);
    void (*begin_items)(void *);
    void (*release_current)(void *);
    int32_t (*clear_and_advance)(void *);
    void (*end_items)(void *);
    void (*clear_field)(void *, uint32_t offset);
    void (*write_state)(void *, uint32_t state);
    void (*mark_dead)(void *);
    void (*restore_counter)(void *);
} Ra2ReferenceListServices;

/* 只遍历正计数；回调后的清槽、计数重读及状态写回保持原顺序。 */
void ra2_cleanup_reference_list(const Ra2ReferenceListServices *services);
