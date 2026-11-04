#ifndef RA2_COMBAT_MANAGER_FIRST_SCAN_BRIDGE_H
#define RA2_COMBAT_MANAGER_FIRST_SCAN_BRIDGE_H

#include <stdint.h>

typedef struct Ra2ManagerFirstScanFlags {
    uint32_t kind, left, right, carry;
} Ra2ManagerFirstScanFlags;

/* 局部标志单独回传，全局元组继续遵循原调用、返回和让出时机。 */
int ra2_manager_first_scan_bridge(Ra2ManagerFirstScanFlags *flags);

#endif
