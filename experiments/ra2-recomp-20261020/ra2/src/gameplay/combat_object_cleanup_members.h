#pragma once
#include <stdint.h>

typedef struct Ra2ObjectMembersCleanupServices {
    void *context;
    void (*begin)(void *);
    void (*member_step)(void *, uint32_t);
    int32_t (*restore_and_has_optional)(void *);
    void (*cleanup_optional)(void *);
    void (*clear_optional)(void *);
    void (*cleanup_abstract)(void *);
} Ra2ObjectMembersCleanupServices;

/* 两引用成员先释放再终结，恢复保存寄存器后处理可选成员及基类。 */
void ra2_cleanup_object_members(const Ra2ObjectMembersCleanupServices *services);
