#pragma once
#include <stdint.h>
/* 样本坐标到格子坐标：有符号除256向零，再保留低16位。 */
uint32_t ra2_ground_sample_cell(int32_t x,int32_t y);
uint32_t ra2_ground_sample_adjusted(int32_t value);
typedef struct Ra2TemplatePassageServices {
    void *context;
    uintptr_t (*next_cell)(void *);
    void (*mark)(void *,unsigned);
    int32_t (*classify)(void *,uintptr_t);
} Ra2TemplatePassageServices;
/* 离格标记、通行查询、恢复标记的次序不能交换；每次服务重读当前单位。 */
int32_t ra2_ground_prepare_template_passage(const Ra2TemplatePassageServices *services);
