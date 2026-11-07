#ifndef RA2_COMBAT_MANAGER_POST_CLEANUP_READS_BRIDGE_H
#define RA2_COMBAT_MANAGER_POST_CLEANUP_READS_BRIDGE_H
#include <stdint.h>

/* Independent entry after prior call: use current local stack and ECX slot. */
void ra2_manager_post_cleanup_reads_bridge(uint32_t stack, uint32_t *value);
#endif
