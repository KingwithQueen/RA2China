#include "battle_internal.h"
#include <string.h>
static void put(uint8_t **p, uint32_t value)
{
    for (uint32_t i = 0; i < 4; ++i) *(*p)++ = (uint8_t)(value >> (i * 8));
}
void battle_economy_hash(const ra_battle *b, bool initial, uint8_t **p)
{
    const ra_battle_economy *e = b->economy;
    put(p, e ? 1 : 0);
    if (!e) return;
    const ra_econ_state *s = initial ? &e->initial : &e->state;
    put(p, e->build_rate);
    put(p, e->low_min);
    put(p, e->low_max);
    put(p, e->low_penalty);
    put(p, e->ore_value);
    put(p, e->gem_value);
    put(p, e->harvest_ticks);
    put(p, e->unload_ticks);
    memcpy(*p, e->generic, sizeof(e->generic));
    *p += sizeof(e->generic);
    memcpy(*p, initial ? e->initial_ore : e->ore, (size_t)b->width * b->height);
    *p += (size_t)b->width * b->height;
    for (uint32_t i = 0; i < b->type_count; ++i)
    {
        const ra_econ_type *t = &e->types[i];
        put(p, t->cost);
        put(p, t->ticks);
        put(p, t->adjacent);
        put(p, t->factory);
        put(p, t->storage);
        put(p, t->free_type);
        put(p, (uint32_t)t->tech);
        put(p, t->enabled);
        put(p, t->harvester);
        put(p, t->refinery);
        put(p, t->chrono);
        put(p, t->airport_bound);
        memcpy(*p, t->prerequisite, sizeof(t->prerequisite));
        *p += sizeof(t->prerequisite);
        memcpy(*p, t->owners, sizeof(t->owners));
        *p += sizeof(t->owners);
        memcpy(*p, t->forbidden, sizeof(t->forbidden));
        *p += sizeof(t->forbidden);
        memcpy(*p, t->docks, sizeof(t->docks));
        *p += sizeof(t->docks);
    }
    for (uint32_t i = 0; i < RA_BATTLE_TEAMS; ++i)
    {
        const ra_econ_house *h = &s->houses[i];
        memcpy(*p, h->country, sizeof(h->country));
        *p += sizeof(h->country);
        put(p, (uint32_t)h->credits);
        put(p, (uint32_t)(h->credits >> 32));
        put(p, h->tech);
        put(p, (uint32_t)h->spent);
        put(p, (uint32_t)(h->spent >> 32));
        put(p, (uint32_t)h->earned);
        put(p, (uint32_t)(h->earned >> 32));
        put(p, h->produced);
        put(p, h->built);
        for (uint32_t j = 0; j < RA_ECON_CATEGORIES; ++j)
        {
            const ra_econ_queue *q = &h->queues[j];
            put(p, q->count);
            put(p, q->progress);
            put(p, q->paid);
            put(p, q->paused);
            put(p, q->producer);
            for (uint32_t k = 0; k < q->count; ++k) put(p, q->types[k]);
        }
    }
    for (uint32_t i = 0; i < b->count; ++i)
    {
        const ra_econ_miner *m = &s->miners[i];
        put(p, m->active);
        put(p, m->ore);
        put(p, m->gems);
        put(p, m->destination);
        put(p, m->refinery);
        put(p, m->delay);
        put(p, s->free_pending[i]);
        put(p, s->dock_owner[i]);
    }
}
