#ifndef RA2_COMBAT_CONTROL_LIST_END_H
#define RA2_COMBAT_CONTROL_LIST_END_H

#include <stdint.h>

typedef struct Ra2ControlListEndCursor {
    uint32_t value, current, left, right, compared;
} Ra2ControlListEndCursor;

typedef struct Ra2ControlListEndServices {
    void *context;
    uint32_t (*read)(void *context, uint32_t address);
} Ra2ControlListEndServices;

void ra2_read_control_front(Ra2ControlListEndCursor *cursor, const Ra2ControlListEndServices *services);
void ra2_read_control_back(Ra2ControlListEndCursor *cursor, const Ra2ControlListEndServices *services);

#endif
