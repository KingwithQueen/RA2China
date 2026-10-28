#pragma once
#include <stdint.h>

typedef struct Ra2TechnoMemberRegistryServices {
    void *context;
    int32_t (*has_member)(void *);
    void (*cleanup_member)(void *);
    void (*clear_member)(void *);
    int32_t (*find)(void *);
    void (*remove)(void *, int32_t);
} Ra2TechnoMemberRegistryServices;

/* 成员清理回调返回后清原槽，再用当时的第三登记表查询并有条件移除。 */
void ra2_cleanup_techno_member_registry(const Ra2TechnoMemberRegistryServices *services);
