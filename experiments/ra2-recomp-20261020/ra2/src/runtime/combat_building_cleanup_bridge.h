#pragma once
void ra2_building_delete_bridge(void);
/* 从00439240入口接管prologue和前段，保持栈/寄存器交回0043931F。 */
void ra2_building_cleanup_prefix_bridge(void);
