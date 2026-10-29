#ifndef RA2_COMBAT_CONTROL_LIST_READ_H
#define RA2_COMBAT_CONTROL_LIST_READ_H

#include <stdint.h>

typedef struct Ra2ControlListReadServices {
    void *context;
    int32_t (*has_source)(void *context);
    void (*read_link)(void *context);
    int32_t (*has_link)(void *context);
    int32_t (*is_sentinel)(void *context);
    void (*clear_result)(void *context);
    void (*finish)(void *context);
} Ra2ControlListReadServices;

void ra2_read_control_list_link(const Ra2ControlListReadServices *services);

#endif
