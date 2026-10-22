#pragma once
#include <stdint.h>
/* 隧道逐步行进：每个乘、加/减分别服从原 x87 控制字，最后向零截断。
   不能用宿主 double 的默认最近舍入；极小的正分量也可能使整数坐标减少 1。 */
int32_t ra2_ground_connection_axis(double origin, double distance, double component,
    int subtract, uint16_t control);
