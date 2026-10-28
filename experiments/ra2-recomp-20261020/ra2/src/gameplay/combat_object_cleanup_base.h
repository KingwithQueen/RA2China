#pragma once
#include <stdint.h>

typedef struct Ra2ObjectBaseCleanupServices {
    void *context;
    uint32_t (*association_owner)(void *);
    void (*clear_owner_link)(void *, uint32_t);
    void (*clear_member_link)(void *);
    void (*write_abstract_table)(void *, uint32_t, uint32_t);
} Ra2ObjectBaseCleanupServices;

void ra2_detach_object_association(const Ra2ObjectBaseCleanupServices *services);
void ra2_reset_abstract_tables(const Ra2ObjectBaseCleanupServices *services);
