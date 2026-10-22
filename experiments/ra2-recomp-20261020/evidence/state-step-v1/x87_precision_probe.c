#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include "x87_precision.h"

/* 以实际 x86 CPU 执行与 0x4A23F0/0x4A2404/0x4A241F 相同的三条指令。 */
static uint32_t reference(int32_t integer, uint64_t coefficient, uint16_t control)
{
    uint16_t saved;
    uint32_t result;
    __asm
    {
        fnstcw saved
        fldcw control
        fild integer
        fmul qword ptr coefficient
        fstp dword ptr result
        fldcw saved
    }
    return result;
}

int main(void)
{
    static const unsigned precision[] = { 0, 2, 3 };
    static const int32_t edges[] = { INT32_MIN, INT32_MIN + 1, -16777217, -16777216, -1, 0, 1, 16777216, 16777217, INT32_MAX };
    static const uint64_t coefficients[] =
    {
        UINT64_C(0x3FC2492492492492), UINT64_C(0xBFC2492492492492), UINT64_C(0x3FF0000000000000),
        UINT64_C(0x3FD5555555555555), UINT64_C(0x0010000000000000), UINT64_C(0x0000000000000001),
        UINT64_C(0x47EFFFFFFFFFFFFF), UINT64_C(0x3690000000000000), UINT64_C(0x8000000000000000),
        UINT64_C(0x7FF0000000000000), UINT64_C(0x7FF8000000000011)
    };
    unsigned checked = 0, failed = 0;
    for (unsigned p = 0; p < 3; ++p)
    for (unsigned rc = 0; rc < 4; ++rc)
    {
        uint16_t control = (uint16_t)(0x7F | (precision[p] << 8) | (rc << 10));
        for (unsigned k = 0; k < sizeof(coefficients) / sizeof(coefficients[0]); ++k)
        for (int i = -1000; i < 1010; ++i)
        {
            int32_t value = i < 1000 ? i : edges[i - 1000];
            uint32_t actual = ra2_x87_imul_store_f32(value, coefficients[k], control);
            uint32_t expected = reference(value, coefficients[k], control);
            ++checked;
            if (actual != expected)
            {
                if (failed++ < 8) printf("FAIL value=%d coefficient=%016llX cw=%04X original=%08X c=%08X\n",
                    value, (unsigned long long)coefficients[k], control, expected, actual);
            }
        }
    }
    printf("checked=%u failed=%u\n", checked, failed);
    uint64_t scale = UINT64_C(0x3FC2492492492492);
    printf("movement progress=7 original=%08X c=%08X nearest=%08X\n", reference(7, scale, 0xE7F),
        ra2_x87_imul_store_f32(7, scale, 0xE7F), reference(7, scale, 0x27F));
    return failed ? 1 : 0;
}
