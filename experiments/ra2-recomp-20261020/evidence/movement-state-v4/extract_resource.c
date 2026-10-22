#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdio.h>
#include <wchar.h>
#include "ra2/ra2.h"
int wmain(int argc, wchar_t **argv)
{
    char archive[4096], name[256];
    ra_vfs vfs = { 0 };
    ra_resource resource = { 0 };
    ra_error error = { 0 };
    if (argc != 4) return 2;
    WideCharToMultiByte(CP_UTF8, 0, argv[1], -1, archive, sizeof(archive), NULL, NULL);
    WideCharToMultiByte(CP_UTF8, 0, argv[2], -1, name, sizeof(name), NULL, NULL);
    if (!ra_vfs_mount_mix(&vfs, archive, 1, RA_HASH_CRC32, &error) || !ra_vfs_read(&vfs, name, &resource, &error))
    {
        fprintf(stderr, "%s\n", error.message); return 1;
    }
    FILE *output = _wfopen(argv[3], L"wbx");
    if (!output) return 2;
    size_t written = fwrite(resource.view.data, 1, resource.view.size, output);
    int result = written == resource.view.size && fclose(output) == 0 ? 0 : 1;
    ra_resource_close(&resource); ra_vfs_close(&vfs);
    return result;
}
