#ifndef RA2_GROUND_PATH_DISTANCE_H
#define RA2_GROUND_PATH_DISTANCE_H
#include <stdint.h>
typedef struct Ra2PathPoint { int16_t x,y; } Ra2PathPoint;
/* 原版在 32 位整数中平方并相加，再把结果作为有符号数传给距离近似表。
 * 正常地图坐标不会溢出；这里仍保留完整 int16 坐标范围的回绕行为。 */
int32_t ra2_path_squared_distance(Ra2PathPoint from,Ra2PathPoint to);
/* 第九个邻居表示特殊连接，使用棋盘距离，不乘方向权重。 */
float ra2_path_connection_distance(Ra2PathPoint from,Ra2PathPoint to);
#endif
