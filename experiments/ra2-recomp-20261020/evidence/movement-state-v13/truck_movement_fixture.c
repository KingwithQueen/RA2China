#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "native32.h"
#include "movement_fixture.h"
#include "ground_recovery_bridge.h"
#include "state_trace.h"

#define U32(address) (*(uint32_t *)(uintptr_t)(address))
#define U8(address) (*(uint8_t *)(uintptr_t)(address))

static uint32_t fixture_frame, fixture_id;
static uint32_t fixture_radius=1;
static int requested, applied;
static uint32_t recovery_host_stack;
static unsigned char recovery_stack[65536];

/* 实景局部入口试验：使用真实单位、原版停止/通知服务和原版栈布局。
 * 它不表示普通移动任务已经自然走到此入口；运行报告必须分别说明。 */
#pragma warning(push)
#pragma warning(disable: 4100) /* 裸函数按实际栈偏移读取参数，编译器不识别该引用。 */
static __declspec(naked) uint32_t invoke_original_recovery(uint32_t object, uint32_t frame)
{
    __asm
    {
        pushad
        mov recovery_host_stack, esp
        mov ebp, dword ptr [esp + 36]
        mov ecx, dword ptr [esp + 40]
        lea eax, returned
        mov dword ptr [ecx + 5Ch], eax
        mov esp, ecx
        mov eax, 4A2DFDh
        jmp eax
    returned:
        mov esp, recovery_host_stack
        mov dword ptr [esp + 28], eax
        popad
        ret
    }
}
#pragma warning(pop)

static void fixture_fail(const char *reason)
{
    fprintf(stderr, "[state-error] wall-ring fixture: %s\n", reason);
    fflush(stderr);
    ExitProcess(7);
}

int ra2_movement_fixture_arg(int argc, char **argv, int index)
{
    int unit_ring = !strcmp(argv[index], "--state-unit-ring");
    int budget_entry = !strcmp(argv[index], "--state-budget-entry");
    if (strcmp(argv[index], "--state-wall-ring") && !unit_ring && !budget_entry) return 0;
    char tail;
    int fields=0,valid=0;
    if (index+1<argc)
    {
        fields=sscanf(argv[index+1],"%u:%u:%u%c",&fixture_frame,&fixture_id,&fixture_radius,&tail);
        if (fields==3) valid=1;
        else if (fields==2) valid=sscanf(argv[index+1],"%u:%u%c",&fixture_frame,&fixture_id,&tail)==2;
    }
    if (requested || !valid || fixture_radius<1 || fixture_radius>3
        || (budget_entry && fixture_radius!=1))
    {
        fixture_fail("expected one FRAME:UID[:RADIUS], radius 1..3");
    }
    requested = budget_entry ? 3 : unit_ring ? 2 : 1;
    return 2;
}

int ra2_movement_fixture_requested(void)
{
    return requested;
}

/* 按原版 43C438..43C46D 的 new(0x9C) + OverlayClass 构造流程建墙。
 * 此辅助器只在显式试验参数开启时运行，不直接写路径队列、失败计数或碰撞结果。 */
#pragma optimize("y", off)
static uint32_t invoke_original(uint32_t target, uint32_t object, const uint32_t *arguments, unsigned count)
{
    uint32_t result;
    __asm
    {
        push ebx
        push esi
        push edi
        mov ebx, esp
        mov esi, arguments
        mov edi, count
    push_arguments:
        test edi, edi
        jz invoke
        dec edi
        push dword ptr [esi + edi * 4]
        jmp push_arguments
    invoke:
        mov ecx, object
        call target
        mov result, eax
        mov esp, ebx
        pop edi
        pop esi
        pop ebx
    }
    return result;
}
#pragma optimize("y", on)

static uint32_t fixture_call(int original_mode, uint32_t target, uint32_t object, const uint32_t *arguments, unsigned count)
{
    uint32_t saved[] = { g_eax,g_ecx,g_edx,g_esp,g_ebx,g_esi,g_edi,g_ebp,g_cur_func,
        g_flag_k,g_flag_a,g_flag_b,g_flag_cf,g_fs_base,g_gs_base,g_mxcsr };
    double floating[8];
    uint64_t mm[8];
    xmm_t xmm[8];
    memcpy(floating, g_st, sizeof(floating));
    memcpy(mm, g_mm, sizeof(mm));
    memcpy(xmm, g_xmm, sizeof(xmm));
    int top = g_fp_top;
    uint16_t control = g_fpu_cw;
    uint32_t result;
    if (target == 0x4A2DFD)
    {
        uint32_t frame = (uint32_t)(uintptr_t)(recovery_stack + 32768);
        memset(recovery_stack, 0, sizeof(recovery_stack));
        U32(frame + 0x14) = object + 4;
        if (original_mode)
        {
            result = invoke_original_recovery(object, frame);
        }
        else
        {
            g_esp = frame;
            g_ebp = object;
            ra2_state_movement_audit(3, object, 0, 0);
            ra2_ground_recover_path_bridge(0);
            result = g_eax;
        }
    }
    else if (original_mode)
    {
        result = invoke_original(target, object, arguments, count);
    }
    else
    {
        g_ecx = object;
        g_esp -= 0x100;
        native32_call_guest(target, (int)count, arguments);
        result = g_eax;
    }
    g_eax = saved[0]; g_ecx = saved[1]; g_edx = saved[2]; g_esp = saved[3];
    g_ebx = saved[4]; g_esi = saved[5]; g_edi = saved[6]; g_ebp = saved[7]; g_cur_func = saved[8];
    g_flag_k = saved[9]; g_flag_a = saved[10]; g_flag_b = saved[11]; g_flag_cf = saved[12];
    g_fs_base = saved[13]; g_gs_base = saved[14]; g_mxcsr = saved[15];
    memcpy(g_st, floating, sizeof(floating)); memcpy(g_mm, mm, sizeof(mm)); memcpy(g_xmm, xmm, sizeof(xmm));
    g_fp_top = top; g_fpu_cw = control;
    return result;
}

void ra2_movement_fixture_tick(uint32_t frame, FILE *output, int original_mode)
{
    if (!requested || frame < fixture_frame || (requested != 3 && applied) || (requested == 3 && applied == 11)) return;
    if (frame != fixture_frame + (requested == 3 ? (uint32_t)applied : 0)) fixture_fail("frame skipped");
    uint32_t actor = 0, count = U32(0xA40C30), data = U32(0xA40C24);
    if (count > 16384) fixture_fail("invalid object vector");
    for (uint32_t i = 0; i < count; ++i)
    {
        uint32_t object = U32(data + i * 4);
        if (U32(object + 0x10) == fixture_id) actor = object;
    }
    if (!actor || U32(actor) != 0x7ADDF8) fixture_fail("missing UnitClass actor");
    uint32_t locomotion = U32(actor + 0x564);
    if (!locomotion || U32(locomotion) != 0x7A04CC) fixture_fail("actor is not a ground driver");
    uint32_t drive = locomotion - 4;
    if (requested == 3)
    {
        int32_t before = (int32_t)U32(actor + 0x53C);
        int32_t expected = applied < 10 ? 10 - applied : 0;
        if (before != expected) fixture_fail("unexpected natural initial failure budget");
        uint32_t result = fixture_call(original_mode, 0x4A2DFD, drive, NULL, 0) & 255u;
        int32_t after = (int32_t)U32(actor + 0x53C);
        if (after != (before > 0 ? before - 1 : 0)) fixture_fail("recovery entry budget transition failed");
        fprintf(output, "{\"kind\":\"fixture-budget-entry\",\"frame\":%u,\"id\":%u,\"before\":%d,\"after\":%d,\"result\":%u}\n",
            frame, fixture_id, before, after, result);
        ++applied;
        return;
    }
    if (!U32(drive + 0x34) && !U32(drive + 0x38) && !U32(drive + 0x3C)) fixture_fail("move was not accepted before wall placement");
    uint32_t destination_argument = drive + 0x34;
    uint32_t accepted_before = fixture_call(original_mode, U32(U32(actor) + 0x2AC), actor, &destination_argument, 1) & 255u;
    uint32_t type = U32(U32(0xA35DEC) + 26 * 4);
    if (strcmp((const char *)(uintptr_t)(type + 0x24), "NAWALL") || !U8(type + 0x278)) fixture_fail("unexpected overlay type");
    int32_t x = (int32_t)U32(actor + 0x88) / 256, y = (int32_t)U32(actor + 0x8C) / 256;
    uint32_t house = U32(actor + 0x1B4), wall_owner = U32(house + 0x30);
    uint32_t cells[24], coordinates[24], placed = 0;
    /* 先核实全部位置，避免遇到已有对象/覆盖物后留下半个试验条件。 */
    int radius=(int)fixture_radius;
    for (int dy = -radius; dy <= radius; ++dy)
    {
        for (int dx = -radius; dx <= radius; ++dx)
        {
            if (abs(dx)!=radius && abs(dy)!=radius) continue;
            int32_t cx = x + dx, cy = y + dy;
            if (cx < 0 || cx >= 512 || cy < 0 || cy >= 512) fixture_fail("cell outside vector");
            uint32_t cell = U32(U32(0x832618) + (cy * 512 + cx) * 4);
            if (!cell) fixture_fail("missing ring cell");
            if (U32(cell + 0xE4) || U32(cell + 0xE8))
            {
                fprintf(output, "{\"kind\":\"fixture-occupied\",\"frame\":%u,\"id\":%u,\"cell\":[%d,%d]}\n", frame, fixture_id, cx, cy);
                continue;
            }
            cells[placed] = cell;
            coordinates[placed++] = (uint16_t)cx | (uint32_t)(uint16_t)cy << 16;
        }
    }
    for (uint32_t i = 0; i < placed; ++i)
    {
        if (requested == 2)
        {
            /* 临时单位障碍不重分地形通行区，适合检验重寻路失败的有限预算。 */
            if (U32(0xA322A8) < 2) fixture_fail("missing blocker house");
            uint32_t enemy_house = U32(U32(0xA3229C) + 4);
            if (enemy_house == house) enemy_house = U32(U32(0xA3229C));
            if (enemy_house == house) fixture_fail("blocker house equals actor house");
            uint32_t unit_type = 0, size = 0x7D0;
            uint32_t type_count = U32(0xA35D58), type_data = U32(0xA35D4C);
            if (type_count > 4096) fixture_fail("invalid UnitType vector");
            for (uint32_t ti = 0; ti < type_count; ++ti)
            {
                uint32_t candidate = U32(type_data + ti * 4);
                if (candidate && U32(candidate) == 0x7AE328
                    && !strcmp((const char *)(uintptr_t)(candidate + 0x24), "TRUCKA")) unit_type = candidate;
            }
            if (!unit_type) fixture_fail("default TRUCKA type not found");
            uint32_t blocker = fixture_call(original_mode, 0x782017, 0, &size, 1);
            if (!blocker) fixture_fail("unit allocation failed");
            uint32_t constructor_arguments[2] = { unit_type, enemy_house };
            fixture_call(original_mode, 0x6FA400, blocker, constructor_arguments, 2);
            int32_t point[3] = { (int16_t)(coordinates[i] & 0xFFFF) * 256 + 128,
                (int16_t)(coordinates[i] >> 16) * 256 + 128, (int32_t)U32(actor + 0x90) };
            uint32_t placement_arguments[2] = { (uint32_t)(uintptr_t)point, 0 };
            uint32_t success = fixture_call(original_mode, U32(U32(blocker) + 0xD4), blocker, placement_arguments, 2);
            if (!(success & 255u) || !U8(blocker + 0x74) || U32(blocker + 0x88) != (uint32_t)point[0]
                || U32(blocker + 0x8C) != (uint32_t)point[1]) fixture_fail("engine did not place blocker unit");
            fprintf(output, "{\"kind\":\"fixture-unit\",\"frame\":%u,\"id\":%u,\"blocker_id\":%u,\"cell\":[%u,%u]}\n",
                frame, fixture_id, U32(blocker + 0x10), coordinates[i] & 0xFFFF, coordinates[i] >> 16);
            continue;
        }
        uint32_t size = 0x9C;
        uint32_t overlay = fixture_call(original_mode, 0x782017, 0, &size, 1);
        if (!overlay) fixture_fail("engine allocation failed");
        uint32_t arguments[3] = { type, (uint32_t)(uintptr_t)&coordinates[i], wall_owner };
        fixture_call(original_mode, 0x5DA7D0, overlay, arguments, 3);
        if (U32(cells[i] + 0x44) != 26)
        {
            fprintf(stderr, "[state-fixture-detail] cell=%u,%u overlay=%d owner=%d expected-owner=%u flags=%u,%u active=%u\n",
                coordinates[i] & 0xFFFF, coordinates[i] >> 16, (int32_t)U32(cells[i] + 0x44),
                (int32_t)U32(cells[i] + 0x50), wall_owner, U8(overlay + 0x74), U8(overlay + 0x76), U8(0xA40958));
            fixture_fail("engine did not place the wall");
        }
        /* 原版运行中建墙采用其当前墙体归属全局量，可能得到无主墙；如实记录，不代改归属。 */
        fprintf(output, "{\"kind\":\"fixture-wall\",\"frame\":%u,\"id\":%u,\"cell\":[%u,%u],\"overlay\":26,\"owner\":%d}\n",
            frame, fixture_id, coordinates[i] & 0xFFFF, coordinates[i] >> 16, (int32_t)U32(cells[i] + 0x50));
    }
    applied = 1;
    uint32_t accepted_after = fixture_call(original_mode, U32(U32(actor) + 0x2AC), actor, &destination_argument, 1) & 255u;
    uint32_t rebuilt = UINT32_MAX;
    if (requested == 2 && fixture_radius == 1)
    {
        /* 保留早期一格压力试验的显式重建步骤。新增两/三格包围不调用这里，
           让正常移动更新自行发现障碍；不得提前清掉正在观察的残余路径。 */
        int32_t destination_x = (int32_t)U32(drive + 0x34) / 256;
        int32_t destination_y = (int32_t)U32(drive + 0x38) / 256;
        uint32_t rebuild_arguments[3] = { (uint16_t)destination_x | (uint32_t)(uint16_t)destination_y << 16, 0, 0 };
        rebuilt = fixture_call(original_mode, 0x4C3000, actor, rebuild_arguments, 3) & 255u;
    }
    fprintf(output, "{\"kind\":\"fixture-constraints\",\"frame\":%u,\"id\":%u,\"accepted_before\":%u,\"accepted_after\":%u,"
        "\"close_enough\":%d,\"explicit_rebuild_result\":%u,\"path_head\":%d}\n", frame, fixture_id, accepted_before, accepted_after,
        (int32_t)U32(U32(0x839848) + 0x1380), rebuilt, (int32_t)U32(actor + 0x4D0));
    fprintf(stderr, "[state-fixture] frame=%u actor=%u kind=%s count=%u engine-created\n",
        frame, fixture_id, requested == 2 ? "units" : "walls", placed);
}
