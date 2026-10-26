#pragma once
#include <stdint.h>

/* 抽样常量来自原镜像；乘积保持来宾精度，不先存为double再比较。 */
int ra2_crew_roll_succeeds(int32_t draw,double unit,double chance,uint16_t control);
typedef enum Ra2CrewQuery {
    RA2_CQ_CREWED,RA2_CQ_HOUSE_KIND,RA2_CQ_ALLIED,RA2_CQ_SOVIET,RA2_CQ_TECHNICIAN,
    RA2_CQ_COUNTRY_VALID,RA2_CQ_TECHNICIAN_GATE,RA2_CQ_RANDOM_100,RA2_CQ_CURRENT_TECHNICIAN
} Ra2CrewQuery;
typedef enum Ra2CrewOperation {RA2_CO_SAVE_SELECTION_REGISTER,RA2_CO_PUBLISH_SELECTION} Ra2CrewOperation;
typedef struct Ra2CrewServices {
    void *context;
    uint32_t (*query)(void *,Ra2CrewQuery);
    void (*perform)(void *,Ra2CrewOperation,uint32_t);
} Ra2CrewServices;
typedef struct Ra2CrewSelection {uint32_t type;unsigned eligible;} Ra2CrewSelection;
Ra2CrewSelection ra2_select_crew_type(const Ra2CrewServices *services);
