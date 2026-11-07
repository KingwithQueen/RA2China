#ifndef RA2_COMBAT_MANAGER_CLEANUP_FIELDS_BRIDGE_H
#define RA2_COMBAT_MANAGER_CLEANUP_FIELDS_BRIDGE_H
#include <stdint.h>

/* 输出指向互异的实际缓存寄存器；严格保留两次读取及中间EDX更新顺序。 */
void ra2_manager_cleanup_fields_bridge(uint32_t manager, uint32_t *value, uint32_t *data, uint32_t *head);
#endif
