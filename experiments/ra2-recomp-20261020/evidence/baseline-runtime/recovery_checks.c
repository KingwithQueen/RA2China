#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdint.h>
#include <stdio.h>

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
