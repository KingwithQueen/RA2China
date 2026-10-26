#pragma once
#include <stdint.h>

typedef enum Ra2BuildingCrewQuery {
    RA2_BCQ_SPECIAL_DISABLED, RA2_BCQ_RANDOM_100, RA2_BCQ_FACTORY_KIND,
    RA2_BCQ_CURRENT_ENGINEER, RA2_BCQ_GENERIC_CREW
} Ra2BuildingCrewQuery;

typedef struct Ra2BuildingCrewServices {
    void *context;
    uint32_t (*query)(void *, Ra2BuildingCrewQuery);
} Ra2BuildingCrewServices;

/* 建筑自己的25%工程师分支；通用选员仍负责Crewed、阵营及技师规则。 */
uint32_t ra2_select_building_crew(const Ra2BuildingCrewServices *services);

typedef struct Ra2BuildingEvacuationServices {
    void *context;
    uint32_t (*select_type)(void *);
    uint32_t (*allocate)(void *, uint32_t size);
    uint32_t (*construct)(void *, uint32_t storage, uint32_t type);
} Ra2BuildingEvacuationServices;

/* 直接疏散接口的选型到构造段；位置、散开和销毁仍由原调用者处理。 */
uint32_t ra2_create_building_evacuee(const Ra2BuildingEvacuationServices *services);

typedef struct Ra2BuildingCrewRetryServices {
    void *context;
    uint32_t (*select_type)(void *);
    int (*is_engineer)(void *, uint32_t type);
    int (*engineer_already_selected)(void *);
    void (*mark_engineer_selected)(void *);
} Ra2BuildingCrewRetryServices;

/* 出售的直接选员段：本轮已有工程师时重抽，仍由原调用者创建与放置。 */
uint32_t ra2_select_building_sale_crew(const Ra2BuildingCrewRetryServices *services);
