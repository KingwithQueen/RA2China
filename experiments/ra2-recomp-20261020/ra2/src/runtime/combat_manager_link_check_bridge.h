#ifndef RA2_COMBAT_MANAGER_LINK_CHECK_BRIDGE_H
#define RA2_COMBAT_MANAGER_LINK_CHECK_BRIDGE_H
#include <stdint.h>

/* 401D9F：只回传局部CMP元组，保留公开标志及全部通用寄存器。 */
typedef struct Ra2ManagerLinkCheckFlags {
    uint32_t kind, left, right, carry;
} Ra2ManagerLinkCheckFlags;

int ra2_manager_link_check_bridge(uint32_t source, Ra2ManagerLinkCheckFlags *flags);
#endif
