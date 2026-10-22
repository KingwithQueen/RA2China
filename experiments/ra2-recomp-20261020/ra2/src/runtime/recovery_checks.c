#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdint.h>
#include <stdio.h>

static uint32_t recovery_freeze_frame;
static DWORD recovery_engine_thread;
static uint32_t recovery_seed;

void ra2_recovery_set_seed(uint32_t seed)
{
    recovery_seed = seed;
}

/* 原版初始化函数读取这个预留槽；只在显式指定种子时设置进程内副本，不改写 EXE。 */
void ra2_recovery_apply_seed(uint32_t base)
{
    if (!recovery_seed) return;
    if (base != 0x00400000u) TerminateProcess(GetCurrentProcess(), 6);
    *(uint32_t *)(uintptr_t)0x00A40D40u = recovery_seed;
    fprintf(stderr, "[recovery-seed] value=%u address=0x00A40D40\n", recovery_seed);
}

void ra2_recovery_set_freeze(uint32_t frame)
{
    recovery_freeze_frame = frame;
}

void ra2_recovery_engine_thread(void)
{
    recovery_engine_thread = GetCurrentThreadId();
}

/* 在指定模拟帧的时钟查询处停止主线程，保留真实战场画面供录屏，不打开覆盖画面的暂停菜单。 */
void ra2_recovery_frame_guard(uint32_t frame)
{
    if (!recovery_freeze_frame || frame < recovery_freeze_frame || GetCurrentThreadId() != recovery_engine_thread) return;
    fprintf(stderr, "[recovery-freeze] game-frame=%u target=%u\n", frame, recovery_freeze_frame);
    fflush(stderr);
    for (;;) Sleep(1000);
}

/* 本地光盘版仍检查启动器互斥对象；仅补齐启动环境，不改写游戏的检查函数。 */
void ra2_recovery_launcher_start(int namespaced)
{
    static HANDLE launcher_mutex;
    static HANDLE launcher_event;
    char name[128];
    const char *id = "48BC11BD-C4D7-466b-8A31-C6ABBAD47B3E";
    if (namespaced) snprintf(name, sizeof(name), "%s.%lu", id, GetCurrentProcessId());
    else snprintf(name, sizeof(name), "%s", id);
    launcher_mutex = CreateMutexA(NULL, FALSE, name);
    id = "D6E7FC97-64F9-4d28-B52C-754EDF721C6F";
    if (namespaced) snprintf(name, sizeof(name), "%s.%lu", id, GetCurrentProcessId());
    else snprintf(name, sizeof(name), "%s", id);
    launcher_event = CreateEventA(NULL, TRUE, FALSE, name);
    fprintf(stderr, "[recovery-launcher] namespaced=%d mutex=%d event=%d\n", namespaced, launcher_mutex != NULL, launcher_event != NULL);
}

/* 未实现指令不能静默跳过；记录原版地址后停止本次实验，避免产生假通过结果。 */
void ra2_recovery_unimplemented(uint32_t address, const char *instruction)
{
    fprintf(stderr, "[recovery-unimplemented] address=0x%08X instruction=%s\n", address, instruction);
    fflush(stderr);
    TerminateProcess(GetCurrentProcess(), 5);
}
