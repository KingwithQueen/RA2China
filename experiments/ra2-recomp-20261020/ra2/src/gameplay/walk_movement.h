#ifndef RA2_WALK_MOVEMENT_H
#define RA2_WALK_MOVEMENT_H
#include <stdint.h>
/* 一个轴的新坐标：origin +/- direction_component * speed。
 * 方向分量沿用原版数学服务；坐标及中间结果须为有限、32 位坐标范围内的值。 */
int32_t ra2_walk_advance_axis(int32_t origin,double direction_component,double speed,
    unsigned subtract_step,uint16_t arithmetic_control,uint16_t conversion_control);
#endif
