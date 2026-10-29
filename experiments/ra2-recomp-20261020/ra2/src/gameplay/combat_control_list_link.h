#ifndef RA2_COMBAT_CONTROL_LIST_LINK_H
#define RA2_COMBAT_CONTROL_LIST_LINK_H

#include <stdint.h>

typedef struct Ra2ControlListLinkCursor {
    uint32_t value, current, node;
} Ra2ControlListLinkCursor;

typedef struct Ra2ControlListLinkServices {
    void *context;
    uint32_t (*read)(void *context, uint32_t address);
    void (*write)(void *context, uint32_t address, uint32_t value);
} Ra2ControlListLinkServices;

void ra2_insert_control_link_before(Ra2ControlListLinkCursor *cursor, const Ra2ControlListLinkServices *services);
void ra2_insert_control_link_after(Ra2ControlListLinkCursor *cursor, const Ra2ControlListLinkServices *services);
void ra2_detach_control_link(Ra2ControlListLinkCursor *cursor, const Ra2ControlListLinkServices *services);

#endif
