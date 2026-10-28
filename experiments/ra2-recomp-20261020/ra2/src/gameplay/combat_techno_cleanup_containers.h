#pragma once
#include <stdint.h>

typedef struct Ra2TechnoContainersServices {
    void *context;
    void (*begin)(void *, uint32_t);
    int32_t (*has_data)(void *);
    int32_t (*owns_data)(void *);
    void (*free_data)(void *);
    void (*end)(void *, uint32_t);
    void (*finish_member118)(void *);
} Ra2TechnoContainersServices;

/* 逆序成员逐项处理，借用指针保留；118的原接口不重置成员。 */
void ra2_cleanup_techno_containers(const Ra2TechnoContainersServices *services);
