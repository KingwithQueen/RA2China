#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include "unit_movement.h"

static uint32_t random_state = 0x26701283u;
static uint32_t next_random(void)
{
    random_state ^= random_state << 13;
    random_state ^= random_state >> 17;
    random_state ^= random_state << 5;
    return random_state;
}

static double operand(void)
{
    static const uint64_t boundaries[] = { 0,1,UINT64_C(0x0010000000000000),UINT64_C(0x3F9EB851EB851EB8),
        UINT64_C(0x3FCEB851EB851EB8),UINT64_C(0x3FD147AE147AE147),UINT64_C(0x3FEFFFFFFFFFFFFF),UINT64_C(0x3FF0000000000000) };
    uint32_t random = next_random();
    uint64_t bits = random & 1 ? boundaries[(random >> 1) & 7]
        : (UINT64_C(0x3FD0000000000000) | ((uint64_t)next_random() << 20) | (next_random() & 0xFFFFFu));
    bits |= (uint64_t)(random >> 31) << 63;
    double result;
    memcpy(&result, &bits, sizeof(result));
    return result;
}

int main(void)
{
    for (unsigned number = 0; number < 120000; ++number)
    {
        double current = operand(), rate = operand(), expected_add, expected_sub;
        int32_t elapsed = (int32_t)(next_random() % 101);
        const unsigned precisions[] = { 0,2,3 };
        uint16_t control = (uint16_t)(0x7F | precisions[number % 3] << 8 | (number / 3 % 4) << 10), saved;
        __asm
        {
            fnstcw saved
            fldcw control
            fld rate
            fadd current
            fstp expected_add
            fild elapsed
            fmul rate
            fsubr current
            fstp expected_sub
            fldcw saved
        }
        double actual_add = ra2_ground_add_acceleration(current, rate, control);
        double actual_sub = ra2_ground_apply_deceleration(current, elapsed, rate, control);
        if (memcmp(&actual_add, &expected_add, 8) || memcmp(&actual_sub, &expected_sub, 8))
        {
            printf("speed ramp mismatch case=%u control=%x elapsed=%d\n", number, control, elapsed);
            return 1;
        }
    }
    puts("{\"passed\":true,\"acceleration_cases\":120000,\"deceleration_cases\":120000,\"bit_exact\":true}");
    return 0;
}
