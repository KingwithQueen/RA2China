#include <string.h>
#include "recomp_types.h"
#include "ground_path_distance.h"
#include "ground_path_distance_bridge.h"
static Ra2PathPoint point_at(uint32_t address)
{Ra2PathPoint point;memcpy(&point,(const void *)(uintptr_t)address,4);return point;}
void ra2_path_node_distance_bridge(void)
{
    uint32_t stack=g_esp,point=MEM32(MEM32(stack+0x18))+0x24,target=MEM32(stack+0x1C);
    Ra2PathPoint from=point_at(point),to=point_at(target);
    int32_t squared=ra2_path_squared_distance(from,to);
    int32_t dx=(int32_t)from.x-to.x,dy=(int32_t)from.y-to.y;
    uint32_t ax=(uint32_t)(dx<0?-dx:dx),ay=(uint32_t)(dy<0?-dy:dy);
    double argument=(double)squared;
    g_esp=stack-8;memcpy((void *)(uintptr_t)g_esp,&argument,8);
    MEM32(stack+0x18)=(uint32_t)squared;
    g_ebx=target;g_edi=point;g_ecx=ax;g_eax=ax*ax;g_edx=(uint32_t)squared;
    g_flag_k=FK_ADD;g_flag_a=ay*ay;g_flag_b=ax*ax;g_flag_cf=(uint32_t)squared<ay*ay;
}
void ra2_path_connection_distance_bridge(void)
{
    uint32_t point=MEM32(MEM32(g_esp+0x20))+0x24,target=MEM32(g_esp+0x30);
    float distance=ra2_path_connection_distance(point_at(point),point_at(target));
    memcpy((void *)(uintptr_t)(g_esp+0x34),&distance,4);
    g_edi=MEM32(g_esp+0x24);
}
