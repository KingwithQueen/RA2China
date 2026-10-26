#include <string.h>
#include "recomp_types.h"
#include "combat_warhead_values.h"
#include "combat_warhead_values_bridge.h"

void ra2_combat_warhead_percent_bridge(void)
{
    double unit;memcpy(&unit,(void *)(uintptr_t)ADDR(0x79C518),sizeof(unit));
    double value=ra2_combat_warhead_percent((int32_t)MEM32(g_esp+0x14),unit,g_fpu_cw);
    memcpy((void *)(uintptr_t)ADDR(g_ebx),&value,sizeof(value));
    /* 原后继继续调用strtok；准备原参数，净FPU栈深和控制字保持。 */
    g_esp-=8;MEM32(g_esp)=0;MEM32(g_esp+4)=0x7CE9C0;
}
