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

