#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>
#include "recomp_types.h"
#include "ground_path.h"
#include "ground_path_bridge.h"
#include "native_probe_host.h"

uint32_t g_eax, g_ecx, g_edx, g_esp, g_ebx, g_esi, g_edi, g_ebp;
static uint32_t entry, saved_stack, test_stack, test_drive, native_resume;
static uint32_t native_eax, native_ecx, native_edx, native_ebx, native_esi, native_edi, native_ebp, native_flags;
static unsigned char stack_data[4096], drive_data[128];
static Ra2PathSample samples[96];

static __declspec(naked) void execute_fragment(void)
{
    __asm
    {
        push ebp
        push ebx
        push esi
        push edi
        mov saved_stack, esp
        mov ebp, test_drive
        mov edi, 3456789Ah
        mov esp, test_stack
        add esp, 4
        call dword ptr [entry]
        pushfd
        pop native_flags
        mov native_eax, eax
        mov native_ecx, ecx
        mov native_edx, edx
        mov native_ebx, ebx
        mov native_esi, esi
        mov native_edi, edi
        mov native_ebp, ebp
        mov esp, saved_stack
        pop edi
        pop esi
        pop ebx
        pop ebp
        ret
    }
}

static void append_exit(unsigned char *code, unsigned offset, uint32_t destination)
{
    code[offset] = 0xC7;
    code[offset + 1] = 0x05;
    uint32_t address = (uint32_t)(uintptr_t)&native_resume;
    memcpy(code + offset + 2, &address, 4);
    memcpy(code + offset + 6, &destination, 4);
    code[offset + 10] = 0xC3;
}

int main(int argc, char **argv)
{
    if (argc != 2) return 2;
    hold_image();
    map_original_image(argv[1]);
    unsigned char *code = VirtualAlloc(NULL, 4096, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);
    if (!code) return 2;
    memcpy(code, (void *)0x4A166A, 60);
    append_exit(code, 60, 0x4A16A6);
    append_exit(code, 71, 0x4A1FDC);
    int32_t relative = 11;
    memcpy(code + (0x4A16A0 - 0x4A166A) + 2, &relative, 4);
    FlushInstructionCache(GetCurrentProcess(), code, 82);
    entry = (uint32_t)(uintptr_t)code;
    test_stack = (uint32_t)(uintptr_t)(stack_data + 2048);
    test_drive = (uint32_t)(uintptr_t)drive_data;
    uint32_t table = (uint32_t)(uintptr_t)&samples[32];
    const int32_t progress_values[] = { INT32_MIN, INT32_MIN + 7, -8, -1, 0, 1, 6, 7, 8, 14, 15, 21, 22, INT32_MAX };
    unsigned checked = 0;
    for (int32_t index = -16; index <= 31; ++index)
    {
        for (unsigned p = 0; p < sizeof(progress_values) / sizeof(*progress_values); ++p)
        {
            for (unsigned combination = 0; combination < 9; ++combination)
            {
                Ra2PathSample *sample = &samples[index + 32];
                sample->x = (int32_t)(combination % 3) * 11 - 11;
                sample->y = (int32_t)(combination / 3) * 11 - 11;
                sample->direction = 224;
                MEM32(test_drive + 0x5C) = (uint32_t)index;
                MEM32(test_stack + 0x38) = table;
                MEM32(test_stack + 0x3C) = (uint32_t)progress_values[p];
                execute_fragment();
                uint32_t expected_progress = MEM32(test_stack + 0x3C);
                uint32_t expected_x = MEM32(test_stack + 0x8C), expected_y = MEM32(test_stack + 0x90);
                MEM32(test_stack + 0x3C) = (uint32_t)progress_values[p];
                g_esp = test_stack; g_ebp = test_drive; g_edi = 0x3456789A;
                uint32_t destination = ra2_ground_consume_sample_bridge();
                uint32_t flags = recomp_eflags(g_flag_k, g_flag_a, g_flag_b, g_flag_cf, 1);
                if (destination != native_resume || MEM32(test_stack + 0x3C) != expected_progress
                    || MEM32(test_stack + 0x8C) != expected_x || MEM32(test_stack + 0x90) != expected_y
                    || g_eax != native_eax || g_ecx != native_ecx || g_edx != native_edx || g_ebx != native_ebx
                    || g_esi != native_esi || g_edi != native_edi || g_ebp != native_ebp || (flags & 0x8D5) != (native_flags & 0x8D5))
                {
                    printf("fragment mismatch index=%d progress=%d sample=%d,%d flags=%x/%x\n", index, progress_values[p],
                        sample->x, sample->y, flags, native_flags);
                    return 1;
                }
                ++checked;
            }
        }
    }
    printf("{\"passed\":true,\"original_fragment_cases\":%u,\"registers_and_flags_verified\":true}\n", checked);
    return 0;
}
