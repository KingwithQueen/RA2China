#ifndef RA2_COMBAT_CONTROL_FREE_LIST_H
#define RA2_COMBAT_CONTROL_FREE_LIST_H

#include "combat_control_list_link.h"

uint32_t ra2_take_control_free_node(Ra2ControlListLinkCursor *cursor, const Ra2ControlListLinkServices *services);
void ra2_return_control_free_node(Ra2ControlListLinkCursor *cursor, const Ra2ControlListLinkServices *services);

#endif
