#include "ground_object_chain.h"

void ra2_ground_object_chain_begin(Ra2ObjectChain *state, unsigned alternate_layer,
                                 uintptr_t ground_head, uintptr_t upper_head)
{
    state->pending_contact = 0;
    state->object = alternate_layer ? upper_head : ground_head;
}

void ra2_ground_object_chain_next(Ra2ObjectChain *state, uintptr_t next,
                                uintptr_t saved_cell, int32_t saved_classification)
{
    state->object = next;
    state->cell = saved_cell;
    state->classification = saved_classification;
}
