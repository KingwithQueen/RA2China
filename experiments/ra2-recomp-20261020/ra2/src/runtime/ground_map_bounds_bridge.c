#include <stdint.h>
#include <string.h>
#include "recomp_types.h"
#include "ground_cell_services.h"
#include "ground_services_bridge.h"

/* 仅适配1.006的布局、AL返回、易失寄存器和ret 8；菱形规则在gameplay。 */
void ra2_cell_map_area_bridge(void)
{
    uint32_t stack=g_esp,map=g_ecx,input=MEM32(stack+4);
    Ra2ServiceCell point;memcpy(&point,(void *)(uintptr_t)ADDR(input),sizeof(point));
    Ra2MapArea area={(int32_t)MEM32(map+0xF0),(int32_t)MEM32(map+0xF8),
        (int32_t)MEM32(map+0xFC),(int32_t)MEM32(map+0x100),(int32_t)MEM32(map+0x104)};
    int32_t level=0;unsigned slope=0;
    if(MEM8(stack+8))
    {
        Ra2CellGrid grid={(const uint32_t *)(uintptr_t)ADDR(MEM32(0x832618)),262144,
            0xA6F9F8,(Ra2ServiceCell *)(uintptr_t)ADDR(0xA6FA1C)};
        uint32_t cell=(uint32_t)ra2_cell_at_point(&grid,point);
        level=(int8_t)MEM8(cell+0x11B);slope=MEM8(cell+0x11C);
    }
    Ra2MapAreaEdge edge=ra2_cell_area_boundary(&area,point,level,slope);
    g_eax=(uint32_t)area.width;g_edx=(uint32_t)(int32_t)point.y;
    if(edge==RA2_MAP_AREA_RIGHT)
        g_ecx=2u*((uint32_t)area.local_x+(uint32_t)area.local_width)-(uint32_t)area.width;
    else if(edge==RA2_MAP_AREA_LEFT || edge==RA2_MAP_AREA_INSIDE)
    {
        g_ecx=2u*(uint32_t)area.local_x;
        g_edx=(uint32_t)(int32_t)point.y-(uint32_t)(int32_t)point.x;
        g_eax=(uint32_t)area.width-g_ecx;
    }
    if(edge==RA2_MAP_AREA_INSIDE)
    {
        g_flag_k=FK_CMP;g_flag_a=g_edx;g_flag_b=g_eax;g_flag_cf=g_edx<g_eax;
        g_eax=(g_eax&0xFFFFFF00u)|1u;
    }
    else
    {
        g_eax&=0xFFFFFF00u;
        g_flag_k=FK_TEST;g_flag_a=0;g_flag_b=0;g_flag_cf=0;
    }
    g_esp=stack+12;
}
