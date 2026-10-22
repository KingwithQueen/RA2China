#pragma once
#include <stdint.h>

int ra2_state_arg(int argc, char **argv, int i);
void ra2_state_validate(void);
void ra2_state_install_original(uint32_t base);
void ra2_state_tick(void);
void ra2_state_event(uint32_t event_address);
void ra2_state_math(uint32_t stack, uint32_t caller_frame, uint32_t output, uint32_t source);
void ra2_state_phase(uint32_t caller_stack, uint32_t caller_frame, const void *extended, const double *translated);
void ra2_state_speed(uint32_t caller_stack, uint32_t unit, const void *extended, const double *translated);
void ra2_state_movement_audit(uint32_t stage, uint32_t actor, uint32_t cell, uint32_t object);
