#ifndef RA2_COMBAT_MANAGER_CONSTRUCTOR_GLOBAL_LOAD_BRIDGE_H
#define RA2_COMBAT_MANAGER_CONSTRUCTOR_GLOBAL_LOAD_BRIDGE_H
#include <stdint.h>

/* 每次调用读取固定全局地址的当前值。 */
uint32_t ra2_manager_constructor_global_load_bridge(void);
#endif
