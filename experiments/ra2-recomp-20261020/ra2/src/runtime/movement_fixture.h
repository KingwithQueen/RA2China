#pragma once
#include <stdint.h>
#include <stdio.h>
int ra2_movement_fixture_arg(int argc, char **argv, int index);
int ra2_movement_fixture_requested(void);
void ra2_movement_fixture_tick(uint32_t frame, FILE *output, int original_mode);
