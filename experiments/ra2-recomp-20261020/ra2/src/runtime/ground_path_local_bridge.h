#ifndef RA2_GROUND_PATH_LOCAL_BRIDGE_H
#define RA2_GROUND_PATH_LOCAL_BRIDGE_H
void ra2_path_turn_rewrite_bridge(void);
void ra2_path_anchor_bridge(void);
void ra2_path_segment_rewrite_bridge(void);
/* 使用原搜索局部帧，完成业务处理后恢复寄存器并按原ret 0x18退出。 */
void ra2_path_completion_bridge(unsigned preparation);
#endif
