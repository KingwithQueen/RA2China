/* Executable adapter only: keep the library independent of command-line APIs. */
#ifdef _WIN32
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdlib.h>
static int app_main(int argc, char **argv);
int wmain(int argc, wchar_t **wide)
{
    int i, result = 1;
    char **argv = calloc((size_t)argc+1, sizeof(*argv));
    if (!argv) return 1;
    for (i = 0; i < argc; ++i) {
        int n = WideCharToMultiByte(CP_UTF8, WC_ERR_INVALID_CHARS, wide[i], -1, NULL, 0, NULL, NULL);
        if (!n || !(argv[i] = malloc((size_t)n))) goto done;
        if (!WideCharToMultiByte(CP_UTF8, WC_ERR_INVALID_CHARS, wide[i], -1, argv[i], n, NULL, NULL)) goto done;
    }
    result = app_main(argc, argv);
done:
    for (i = 0; i < argc; ++i) free(argv[i]);
    free(argv); return result;
}
#else
static int app_main(int argc, char **argv);
int main(int argc, char **argv) { return app_main(argc, argv); }
#endif
