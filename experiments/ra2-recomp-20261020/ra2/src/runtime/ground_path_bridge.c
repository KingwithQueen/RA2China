#include <stdint.h>
#include "recomp_types.h"
#include "ground_path.h"
#include "ground_path_bridge.h"

uint32_t ra2_ground_consume_sample_bridge(void)
{
    uint32_t table = MEM32(g_esp + 0x38);
    int32_t index = (int32_t)MEM32(g_ebp + 0x5C);
    uint32_t address = table + (uint32_t)index * 12;
    Ra2PathSample sample = { (int32_t)MEM32(address), (int32_t)MEM32(address + 4), (int32_t)MEM32(address + 8) };
    Ra2PathCursor cursor = { index, (int32_t)MEM32(g_esp + 0x3C) };
    Ra2PathSampleOutcome outcome = ra2_ground_consume_path_sample(&cursor, sample);
    MEM32(g_esp + 0x3C) = (uint32_t)cursor.remaining_progress;
    MEM32(g_esp + 0x8C) = (uint32_t)sample.x;
    MEM32(g_esp + 0x90) = (uint32_t)sample.y;
    g_eax = (uint32_t)index;
    g_esi = table;
    g_ebx = (uint32_t)cursor.remaining_progress;
    g_edx = (uint32_t)sample.x;
    g_ecx = (uint32_t)sample.y;
    /* 保留原版最后一次 test 的返回标志，供共享尾部和调用者继续使用。 */
    uint32_t tested = sample.x ? (uint32_t)sample.x : (sample.y ? (uint32_t)sample.y : (uint32_t)index);
    g_flag_k = FK_TEST;
    g_flag_a = tested;
    g_flag_b = tested;
    g_flag_cf = 0;
    return outcome == RA2_PATH_SAMPLE_REACHES_END ? 0x004A1FDCu : 0x004A16A6u;
}
