#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "unit_movement.h"
#include "movement_bridge.h"
#include "recomp_types.h"

uint32_t g_eax, g_ecx, g_edx, g_esp, g_ebx, g_esi, g_edi, g_ebp;
double g_st[8];
int g_fp_top;
uint16_t g_fpu_cw;

void ra2_state_math(uint32_t stack, uint32_t frame, uint32_t output, uint32_t source)
{
    (void)stack; (void)frame; (void)output; (void)source;
}

static uint32_t input_target, input_ecx, input_edx, input_stack, host_stack;
static uint32_t actual_eax, actual_ecx, actual_edx, actual_ebx, actual_esi, actual_edi, actual_ebp, actual_esp, actual_flags;
static uint16_t actual_control;
static unsigned char private_stack[4096];

/* 使用同一个私有栈地址，直接核对原版与 ABI 适配层的寄存器、栈平衡和返回标志。 */
static __declspec(naked) void call_original_captured(void)
{
    __asm
    {
        push ebp
        push ebx
        push esi
        push edi
        mov host_stack, esp
        mov ecx, input_ecx
        mov edx, input_edx
        mov ebx, 12345678h
        mov esi, 23456789h
        mov edi, 3456789Ah
        mov ebp, 456789ABh
        mov esp, input_stack
        add esp, 4
        call dword ptr [input_target]
        mov actual_esp, esp
        pushfd
        pop actual_flags
        mov actual_eax, eax
        mov actual_ecx, ecx
        mov actual_edx, edx
        mov actual_ebx, ebx
        mov actual_esi, esi
        mov actual_edi, edi
        mov actual_ebp, ebp
        fnstcw actual_control
        mov esp, host_stack
        pop edi
        pop esi
        pop ebx
        pop ebp
        ret
    }
}

static void verify_bridge(uint32_t target, uint32_t first, uint32_t second, const uint32_t *arguments, unsigned argument_count, uint16_t control)
{
    uint32_t *stack = (uint32_t *)(private_stack + 2048);
    input_target = target; input_ecx = first; input_edx = second; input_stack = (uint32_t)(uintptr_t)stack;
    for (unsigned i = 0; i < argument_count; ++i) stack[i + 1] = arguments[i];
    uint32_t output_address = target == 0x7220C0 ? first : arguments[0];
    uint32_t *direction = target == 0x4A4740 ? (uint32_t *)(uintptr_t)arguments[2] : NULL;
    uint32_t direction_before = direction ? *direction : 0;
    Ra2WorldPoint before, expected;
    memcpy(&before, (void *)(uintptr_t)output_address, sizeof(before));
    uint16_t saved;
    __asm
    {
        fnstcw saved
        fldcw control
    }
    call_original_captured();
    __asm fldcw saved
    memcpy(&expected, (void *)(uintptr_t)output_address, sizeof(expected));
    uint32_t expected_direction = direction ? *direction : 0;
    memcpy((void *)(uintptr_t)output_address, &before, sizeof(before));
    if (direction) *direction = direction_before;
    /* 捕获返回标志时 pushfd 会复用已弹出的参数槽；在运行 C 适配层前恢复相同入口参数。 */
    for (unsigned i = 0; i < argument_count; ++i) stack[i + 1] = arguments[i];
    g_eax = 0;
    g_ecx = first; g_edx = second; g_esp = input_stack;
    g_ebx = 0x12345678; g_esi = 0x23456789; g_edi = 0x3456789A; g_ebp = 0x456789AB;
    g_fpu_cw = control;
    g_fp_top = 1;
    g_st[0] = 12345.625;
    if (target == 0x7220C0) ra2_movement_interpolate_bridge();
    else ra2_movement_transform_bridge();
    uint32_t flags = recomp_eflags(g_flag_k, g_flag_a, g_flag_b, g_flag_cf, 1);
    if (memcmp(&expected, (void *)(uintptr_t)output_address, sizeof(expected)) || (direction && *direction != expected_direction)
        || g_eax != actual_eax || g_ecx != actual_ecx || g_edx != actual_edx || g_esp != actual_esp
        || g_ebx != actual_ebx || g_esi != actual_esi || g_edi != actual_edi || g_ebp != actual_ebp
        || (flags & 0x8D5) != (actual_flags & 0x8D5) || (g_fpu_cw & 0x1F3F) != (actual_control & 0x1F3F)
        || g_fp_top != 1 || g_st[0] != 12345.625)
    {
        printf("bridge mismatch target=%08x cw=%x flags=%x/%x registers=%x,%x,%x/%x,%x,%x esp=%x/%x\n", target, control,
            flags, actual_flags, g_eax, g_ecx, g_edx, actual_eax, actual_ecx, actual_edx, g_esp, actual_esp);
        exit(1);
    }
}

/* 与正式宿主相同：在子进程加载 CRT 前预留原版地址，避免 Windows 堆与 ASLR 布局占用。 */
static void hold_image(void)
{
    char marker[8], executable[MAX_PATH];
    if (GetEnvironmentVariableA("RA2_MOVEMENT_PROBE_HELD", marker, sizeof(marker)))
    {
        SetEnvironmentVariableA("RA2_MOVEMENT_PROBE_HELD", NULL);
        return;
    }
    STARTUPINFOA startup = { 0 };
    PROCESS_INFORMATION process;
    startup.cb = sizeof(startup);
    startup.dwFlags = STARTF_USESTDHANDLES;
    startup.hStdInput = GetStdHandle(STD_INPUT_HANDLE);
    startup.hStdOutput = GetStdHandle(STD_OUTPUT_HANDLE);
    startup.hStdError = GetStdHandle(STD_ERROR_HANDLE);
    SetHandleInformation(startup.hStdOutput, HANDLE_FLAG_INHERIT, HANDLE_FLAG_INHERIT);
    SetHandleInformation(startup.hStdError, HANDLE_FLAG_INHERIT, HANDLE_FLAG_INHERIT);
    GetModuleFileNameA(NULL, executable, MAX_PATH);
    SetEnvironmentVariableA("RA2_MOVEMENT_PROBE_HELD", "1");
    BOOL made = CreateProcessA(executable, GetCommandLineA(), NULL, NULL, TRUE, CREATE_SUSPENDED | CREATE_NO_WINDOW,
        NULL, NULL, &startup, &process);
    SetEnvironmentVariableA("RA2_MOVEMENT_PROBE_HELD", NULL);
    if (!made) exit(2);
    if (!VirtualAllocEx(process.hProcess, (void *)0x400000, 0x800000, MEM_RESERVE, PAGE_NOACCESS))
    {
        fprintf(stderr, "child image reservation failed: %lu\n", GetLastError());
        TerminateProcess(process.hProcess, 2);
        exit(2);
    }
    ResumeThread(process.hThread);
    if (WaitForSingleObject(process.hProcess, 60000) != WAIT_OBJECT_0) TerminateProcess(process.hProcess, 2);
    DWORD code = 2;
    GetExitCodeProcess(process.hProcess, &code);
    CloseHandle(process.hThread);
    CloseHandle(process.hProcess);
    ExitProcess(code);
}

/* 仅加载原版节数据，不执行入口、不解析导入；本测试调用的两个纯计算函数不依赖导入。 */
static void map_original_image(const char *path)
{
    /* 必须先保留原版地址，再打开文件/分配大缓冲，避免 CRT 堆抢占低地址。 */
    unsigned char *image = VirtualAlloc((void *)0x400000, 0x800000, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);
    if (!image) image = VirtualAlloc((void *)0x400000, 0x800000, MEM_COMMIT, PAGE_EXECUTE_READWRITE);
    if (image != (void *)0x400000)
    {
        fprintf(stderr, "image allocation failed: %lu\n", GetLastError());
        uintptr_t cursor = 0x400000;
        while (cursor < 0xC00000)
        {
            MEMORY_BASIC_INFORMATION region;
            if (!VirtualQuery((void *)cursor, &region, sizeof(region))) break;
            fprintf(stderr, "region=%p allocation=%p size=%lu state=%lx type=%lx\n", region.BaseAddress, region.AllocationBase,
                (unsigned long)region.RegionSize, region.State, region.Type);
            cursor = (uintptr_t)region.BaseAddress + region.RegionSize;
        }
        exit(2);
    }
    FILE *file = NULL;
    if (fopen_s(&file, path, "rb") || !file) exit(2);
    fseek(file, 0, SEEK_END);
    long length = ftell(file);
    rewind(file);
    unsigned char *data = malloc((size_t)length);
    if (!data || fread(data, 1, (size_t)length, file) != (size_t)length) exit(2);
    fclose(file);
    IMAGE_DOS_HEADER *dos = (IMAGE_DOS_HEADER *)data;
    IMAGE_NT_HEADERS32 *pe = (IMAGE_NT_HEADERS32 *)(data + dos->e_lfanew);
    if (dos->e_magic != IMAGE_DOS_SIGNATURE || pe->Signature != IMAGE_NT_SIGNATURE
        || pe->OptionalHeader.ImageBase != 0x400000 || pe->FileHeader.TimeDateStamp != 0x3B1EBBED || pe->OptionalHeader.SizeOfImage > 0x800000) exit(2);
    memcpy(image, data, pe->OptionalHeader.SizeOfHeaders);
    IMAGE_SECTION_HEADER *section = IMAGE_FIRST_SECTION(pe);
    for (unsigned i = 0; i < pe->FileHeader.NumberOfSections; ++i)
        memcpy(image + section[i].VirtualAddress, data + section[i].PointerToRawData, section[i].SizeOfRawData);
    FlushInstructionCache(GetCurrentProcess(), image, pe->OptionalHeader.SizeOfImage);
    free(data);
}

typedef Ra2WorldPoint *(__fastcall *OriginalInterpolate)(Ra2WorldPoint *, const Ra2WorldPoint *, const Ra2WorldPoint *, float);
static OriginalInterpolate original_interpolate = (OriginalInterpolate)0x7220C0;

static void original_transform(void *drive, Ra2WorldPoint *output, const Ra2WorldPoint *sample, uint32_t *direction)
{
    uint32_t function_address = 0x4A4740;
    __asm
    {
        push direction
        push sample
        push output
        mov ecx, drive
        call function_address
    }
}

static uint32_t seed = 0x2247;
static uint32_t random_word(void)
{
    seed = seed * 1664525u + 1013904223u;
    return seed;
}

int main(int argc, char **argv)
{
    if (argc != 2) return 2;
    hold_image();
    map_original_image(argv[1]);
    const unsigned precisions[] = { 0, 2, 3 };
    uint16_t conversion = *(uint16_t *)0x7D8964;
    uint16_t saved;
    __asm fnstcw saved
    unsigned interpolation_count = 0, transform_count = 0, bridge_count = 0;
    for (unsigned p = 0; p < 3; ++p)
    {
        for (unsigned rounding = 0; rounding < 4; ++rounding)
        {
            uint16_t control = (uint16_t)(0x007F | (precisions[p] << 8) | (rounding << 10));
            for (unsigned i = 0; i < 10000; ++i)
            {
                Ra2WorldPoint start, finish, expected;
                start.x = (int32_t)(random_word() % 131073) - 65536;
                start.y = (int32_t)(random_word() % 131073) - 65536;
                start.z = (int32_t)(random_word() % 4097) - 2048;
                finish.x = (int32_t)(random_word() % 131073) - 65536;
                finish.y = (int32_t)(random_word() % 131073) - 65536;
                finish.z = (int32_t)(random_word() % 4097) - 2048;
                float fraction = (float)(i % 8) / 7.0f;
                __asm fldcw control
                Ra2WorldPoint *returned = original_interpolate(&expected, &start, &finish, fraction);
                uint16_t after;
                __asm
                {
                    fnstcw after
                    fldcw saved
                }
                Ra2WorldPoint actual = ra2_ground_interpolate_position(start, finish, fraction, control, conversion);
                if (memcmp(&actual, &expected, sizeof(actual)) || returned != &expected || (after & 0x1F3F) != (conversion & 0x1F3F))
                {
                    printf("original interpolation mismatch cw=%x case=%u after=%x conversion=%x expected=%d,%d,%d actual=%d,%d,%d\n",
                        control, i, after, conversion, expected.x, expected.y, expected.z, actual.x, actual.y, actual.z);
                    return 1;
                }
                ++interpolation_count;
                if (i < 256)
                {
                    uint32_t arguments[2] = { (uint32_t)(uintptr_t)&finish, 0 };
                    memcpy(&arguments[1], &fraction, 4);
                    verify_bridge(0x7220C0, (uint32_t)(uintptr_t)&expected, (uint32_t)(uintptr_t)&start, arguments, 2, control);
                    ++bridge_count;
                }
            }
        }
    }
    unsigned char drive[0x70] = { 0 };
    *(uint32_t *)(drive + 0x58) = 0;
    uint32_t *table_flags = (uint32_t *)0x7A0188;
    uint32_t saved_flags = *table_flags;
    for (unsigned flags = 0; flags < 8; ++flags)
    {
        *table_flags = flags;
        for (unsigned direction = 0; direction < 256; ++direction)
        {
            for (unsigned i = 0; i < 12; ++i)
            {
                Ra2WorldPoint sample, origin, expected = { 0, 0, 123456789 };
                uint32_t raw = random_word(); memcpy(&sample.x, &raw, 4);
                raw = random_word(); memcpy(&sample.y, &raw, 4);
                raw = random_word(); memcpy(&origin.x, &raw, 4);
                raw = random_word(); memcpy(&origin.y, &raw, 4);
                sample.z = 0;
                origin.z = 0;
                memcpy(drive + 0x40, &origin, sizeof(origin));
                uint32_t expected_direction = direction, actual_direction = direction;
                original_transform(drive, &expected, &sample, &expected_direction);
                Ra2WorldPoint actual = ra2_ground_transform_path_sample(sample, origin, flags, &actual_direction);
                if (actual.x != expected.x || actual.y != expected.y || actual_direction != expected_direction || expected.z != 123456789)
                {
                    printf("original transform mismatch flags=%u direction=%u case=%u\n", flags, direction, i);
                    return 1;
                }
                ++transform_count;
                uint32_t arguments[3] = { (uint32_t)(uintptr_t)&expected, (uint32_t)(uintptr_t)&sample,
                    (uint32_t)(uintptr_t)&expected_direction };
                verify_bridge(0x4A4740, (uint32_t)(uintptr_t)drive, 0, arguments, 3, 0x0E7F);
                ++bridge_count;
            }
        }
    }
    *table_flags = saved_flags;
    printf("{\"passed\":true,\"original_interpolations\":%u,\"original_transforms\":%u,\"abi_cases\":%u,\"conversion_control\":%u}\n",
        interpolation_count, transform_count, bridge_count, conversion);
    return 0;
}
