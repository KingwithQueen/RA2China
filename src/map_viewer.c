#define _CRT_SECURE_NO_WARNINGS
#define UNICODE
#define _UNICODE
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <windowsx.h>
#include <commdlg.h>
#include <dwmapi.h>
#include <wchar.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "internal.h"
#include "map_scene.h"
#include "entry.h"

enum
{
    ID_PROFILE = 300,
    ID_MAP,
    ID_LOAD,
    ID_FILE,
    ID_OVERLAY,
    ID_OBJECTS,
    ID_LOCAL,
    ID_FIT,
    ID_ACTUAL,
    ID_SAVE,
    ID_TMP,
    ID_THEATER,
    ID_TMP_LOAD
};
typedef struct
{
    HWND window, profile, maps, load, file, overlay, objects, local, fit, actual, save, tmp, theater, tmp_load, detail;
    HFONT font;
    RECT canvas;
    map_context contexts[2];
    bool ready[2], busy, dragging, tmp_mode;
    int current;
    POINT drag;
    double zoom, pan_x, pan_y;
    const char *original, *mod;
    ra_map map;
    map_image image;
    char source[32768];
    wchar_t status[1024];
} map_app;
static map_app app;

static wchar_t *wide_text(const char *text)
{
    int n = MultiByteToWideChar(CP_UTF8, MB_ERR_INVALID_CHARS, text, -1, NULL, 0);
    wchar_t *result = n ? calloc((size_t)n, sizeof(*result)) : NULL;
    if (result) MultiByteToWideChar(CP_UTF8, MB_ERR_INVALID_CHARS, text, -1, result, n);
    return result;
}

static char *control_text(HWND control)
{
    wchar_t wide[32768];
    int n;
    char *text;
    GetWindowTextW(control, wide, 32768);
    n = WideCharToMultiByte(CP_UTF8, WC_ERR_INVALID_CHARS, wide, -1, NULL, 0, NULL, NULL);
    text = n ? malloc((size_t)n) : NULL;
    if (text) WideCharToMultiByte(CP_UTF8, WC_ERR_INVALID_CHARS, wide, -1, text, n, NULL, NULL);
    return text;
}

static HWND control(const wchar_t *type, const wchar_t *text, DWORD style, int id)
{
    HWND window =
        CreateWindowExW(0, type, text, WS_CHILD | WS_VISIBLE | WS_TABSTOP | style, 0, 0, 10, 10, app.window, (HMENU)(INT_PTR)id, GetModuleHandleW(NULL), NULL);
    SendMessageW(window, WM_SETFONT, (WPARAM)app.font, TRUE);
    return window;
}

static bool checked(HWND window)
{
    return SendMessageW(window, BM_GETCHECK, 0, 0) == BST_CHECKED;
}

static void error_status(const ra_error *error)
{
    wchar_t *text = wide_text(error->message);
    swprintf(app.status, 1024, L"读取失败：%ls", text ? text : L"错误信息不可显示");
    free(text);
    InvalidateRect(app.window, NULL, FALSE);
}

static void fit_image(void)
{
    if (!app.image.pixels) return;
    double x = (double)(app.canvas.right - app.canvas.left - 24) / app.image.width;
    double y = (double)(app.canvas.bottom - app.canvas.top - 24) / app.image.height;
    app.zoom = x < y ? x : y;
    app.pan_x = ((app.canvas.right - app.canvas.left) - app.image.width * app.zoom) / 2;
    app.pan_y = ((app.canvas.bottom - app.canvas.top) - app.image.height * app.zoom) / 2;
    InvalidateRect(app.window, NULL, FALSE);
}

static void details(void)
{
    wchar_t text[8192], *source = wide_text(app.source);
    if (app.tmp_mode) swprintf(text, 8192, L"TMP 地形原始像素\r\n\r\n%ls\r\n\r\n单击图像查看子块编号。\r\n\r\n滚轮缩放，拖动平移。", source ? source : L"");
    else
        swprintf(text, 8192,
                 L"%ls\r\n\r\n地图：%d × %d\r\n地形格：%zu\r\n覆盖物：%zu\r\n地图对象：%zu\r\n图外对象：%zu\r\n缺失地形：%zu\r\n\r\n红框：路径点（大框为 "
                 L"0–7）\r\n蓝色：建筑位置\r\n白色：单位位置\r\n绿色：树木等地物\r\n金色／紫色：覆盖物位置\r\n洋红色：缺失地形\r\n\r\n%"
                 L"ls\r\n\r\n单击查看格子；滚轮缩放，拖动平移。",
                 app.current ? L"中国 MOD" : L"原版 1.006", app.map.size[2], app.map.size[3], app.map.cell_count, app.map.overlay_count, app.map.object_count,
                 app.map.outside_objects, app.image.missing, source ? source : L"");
    SetWindowTextW(app.detail, text);
    free(source);
}

static void loaded_status(void)
{
    swprintf(app.status, 1024, L"%ls · %d × %d 像素 · 缺失地形 %zu · 滚轮缩放 / 拖动平移 / 单击查看", app.tmp_mode ? L"TMP 地形" : L"实际地形绘制",
             app.image.width, app.image.height, app.image.missing);
    details();
    InvalidateRect(app.window, NULL, FALSE);
}

static bool load_bytes(ra_view bytes, const char *source)
{
    ra_map candidate = {0};
    map_image image = {0};
    ra_error error = {0};
    if (!ra_map_open(&candidate, bytes, source, &error) ||
        !map_render(&app.contexts[app.current], &candidate, &image, checked(app.overlay), checked(app.objects), checked(app.local), &error))
    {
        ra_map_close(&candidate);
        map_image_close(&image);
        error_status(&error);
        return false;
    }
    ra_map_close(&app.map);
    map_image_close(&app.image);
    app.map = candidate;
    app.image = image;
    app.tmp_mode = false;
    snprintf(app.source, sizeof(app.source), "%s", source);
    fit_image();
    loaded_status();
    return true;
}

static void load_selected(void)
{
    LRESULT selected = SendMessageW(app.maps, CB_GETCURSEL, 0, 0);
    map_context *context = &app.contexts[app.current];
    if (selected >= 0 && (size_t)selected < context->source_count) load_bytes(context->sources[selected].bytes, context->sources[selected].source);
}

static void profile_load(int profile)
{
    map_context *context = &app.contexts[profile];
    ra_error error = {0};
    size_t i;
    int default_map = 0;
    if (app.busy) return;
    app.busy = true;
    SetCursor(LoadCursorW(NULL, IDC_WAIT));
    if (!app.ready[profile]) app.ready[profile] = map_context_open(context, app.original, profile ? app.mod : NULL, &error);
    if (!app.ready[profile])
    {
        error_status(&error);
        app.busy = false;
        return;
    }
    app.current = profile;
    SendMessageW(app.maps, CB_RESETCONTENT, 0, 0);
    for (i = 0; i < context->source_count; ++i)
    {
        char base[64];
        const ra_ini_entry *description;
        const ra_csf_label *label;
        wchar_t row[1024], *name = wide_text(context->sources[i].name), *title = NULL;
        snprintf(base, sizeof(base), "%s", context->sources[i].name);
        if (strchr(base, '.')) *strchr(base, '.') = 0;
        description = ra_ini_get(&context->missions, base, "Description");
        label = description ? ra_csf_get(&context->strings, description->value) : NULL;
        if (label && label->value_count) title = wide_text(context->strings.values[label->first_value].text);
        swprintf(row, 1024, L"%ls%ls%ls", name ? name : L"?", title ? L" · " : L"", title ? title : L"");
        SendMessageW(app.maps, CB_ADDSTRING, 0, (LPARAM)row);
        if (ra_equal(base, "MP02T2")) default_map = (int)i;
        free(title);
        free(name);
    }
    SendMessageW(app.maps, CB_SETCURSEL, (WPARAM)default_map, 0);
    app.busy = false;
    load_selected();
    SetCursor(LoadCursorW(NULL, IDC_ARROW));
}

static void load_tmp(void)
{
    char *name = control_text(app.tmp);
    ra_resource resource = {0};
    ra_tmp tmp = {0};
    map_image image = {0};
    ra_error error = {0};
    int theater = (int)SendMessageW(app.theater, CB_GETCURSEL, 0, 0);
    map_context *context = &app.contexts[app.current];
    bool ok = name && map_theater_open(context, theater, &error) && ra_vfs_read(&context->vfs, name, &resource, &error) &&
              ra_tmp_open(&tmp, resource.view, &error) && map_tmp_render(&tmp, &context->theaters[theater].palette, &image, &error);
    if (ok)
    {
        map_image_close(&app.image);
        app.image = image;
        app.tmp_mode = true;
        snprintf(app.source, sizeof(app.source), "%s", resource.source);
        fit_image();
        loaded_status();
    }
    else
    {
        map_image_close(&image);
        error_status(&error);
    }
    ra_tmp_close(&tmp);
    ra_resource_close(&resource);
    free(name);
}

static void rerender(void)
{
    ra_error error = {0};
    map_image image = {0};
    if (app.tmp_mode || !app.map.cell_count) return;
    if (map_render(&app.contexts[app.current], &app.map, &image, checked(app.overlay), checked(app.objects), checked(app.local), &error))
    {
        map_image_close(&app.image);
        app.image = image;
        fit_image();
        loaded_status();
    }
    else
    {
        map_image_close(&image);
        error_status(&error);
    }
}

static void layout(void)
{
    RECT client;
    GetClientRect(app.window, &client);
    MoveWindow(app.profile, 20, 54, 150, 180, TRUE);
    MoveWindow(app.maps, 180, 54, client.right - 455, 400, TRUE);
    MoveWindow(app.load, client.right - 265, 54, 105, 30, TRUE);
    MoveWindow(app.file, client.right - 150, 54, 130, 30, TRUE);
    MoveWindow(app.overlay, 20, 105, 250, 26, TRUE);
    MoveWindow(app.objects, 20, 135, 250, 26, TRUE);
    MoveWindow(app.local, 20, 165, 250, 26, TRUE);
    MoveWindow(app.fit, 20, 205, 115, 30, TRUE);
    MoveWindow(app.actual, 145, 205, 115, 30, TRUE);
    MoveWindow(app.save, 20, 247, 240, 30, TRUE);
    MoveWindow(app.theater, 20, 304, 100, 160, TRUE);
    MoveWindow(app.tmp, 130, 304, 130, 26, TRUE);
    MoveWindow(app.tmp_load, 20, 340, 240, 30, TRUE);
    MoveWindow(app.detail, 20, 392, 250, client.bottom - 445, TRUE);
    app.canvas = (RECT){290, 100, client.right - 20, client.bottom - 55};
    InvalidateRect(app.window, NULL, FALSE);
}

static void paint(HDC dc)
{
    RECT client, title;
    HBRUSH background = CreateSolidBrush(RGB(242, 245, 249)), dark = CreateSolidBrush(RGB(22, 29, 38));
    int saved;
    GetClientRect(app.window, &client);
    FillRect(dc, &client, background);
    FillRect(dc, &app.canvas, dark);
    DeleteObject(background);
    DeleteObject(dark);
    SelectObject(dc, app.font);
    SetBkMode(dc, TRANSPARENT);
    SetTextColor(dc, RGB(31, 47, 68));
    title = (RECT){20, 15, client.right - 20, 45};
    DrawTextW(dc, L"红色警戒2 · 地图与地形预览", -1, &title, DT_LEFT | DT_SINGLELINE);
    title = (RECT){20, client.bottom - 42, client.right - 20, client.bottom - 8};
    DrawTextW(dc, app.status, -1, &title, DT_LEFT | DT_WORDBREAK);
    if (!app.image.pixels) return;
    saved = SaveDC(dc);
    IntersectClipRect(dc, app.canvas.left, app.canvas.top, app.canvas.right, app.canvas.bottom);
    {
        BITMAPINFO info = {0};
        info.bmiHeader.biSize = sizeof(BITMAPINFOHEADER);
        info.bmiHeader.biWidth = app.image.width;
        info.bmiHeader.biHeight = -app.image.height;
        info.bmiHeader.biPlanes = 1;
        info.bmiHeader.biBitCount = 32;
        SetStretchBltMode(dc, COLORONCOLOR);
        StretchDIBits(dc, app.canvas.left + (int)app.pan_x, app.canvas.top + (int)app.pan_y, (int)(app.image.width * app.zoom),
                      (int)(app.image.height * app.zoom), 0, 0, app.image.width, app.image.height, app.image.pixels, &info, DIB_RGB_COLORS, SRCCOPY);
    }
    RestoreDC(dc, saved);
}

static void inspect_cell(int x, int y)
{
    int ix = (int)floor((x - app.canvas.left - app.pan_x) / app.zoom), iy = (int)floor((y - app.canvas.top - app.pan_y) / app.zoom);
    int32_t index;
    if (!app.image.pixels || ix < 0 || iy < 0 || ix >= app.image.width || iy >= app.image.height) return;
    index = app.image.picked[(size_t)iy * app.image.width + ix];
    if (index < 0) return;
    if (app.tmp_mode) swprintf(app.status, 1024, L"TMP 子块编号：%d · 图像位置 %d,%d", index, ix, iy);
    else
    {
        const ra_map_cell *cell = &app.map.cells[index];
        map_template *entry = NULL;
        ra_error error = {0};
        wchar_t *name = NULL;
        if (map_template_get(&app.contexts[app.current], map_theater_id(app.map.theater), cell->tile, &entry, &error)) name = wide_text(entry->name);
        swprintf(app.status, 1024, L"格子 %u,%u · 地形 %u / 子块 %u / 高度 %u · %ls · 覆盖物 %u，帧 %u", cell->x, cell->y, cell->tile, cell->subtile,
                 cell->height, name ? name : L"资源缺失", app.map.overlay ? app.map.overlay[(size_t)cell->y * 512 + cell->x] : 255,
                 app.map.overlay_data ? app.map.overlay_data[(size_t)cell->y * 512 + cell->x] : 0);
        free(name);
    }
    InvalidateRect(app.window, NULL, FALSE);
}

/* Windows 路径可能含无效代理项或超出 UTF-8 缓冲区，转换失败时禁止继续读写。 */
static bool file_path(const wchar_t *wide, char text[65536], ra_error *error)
{
    text[0] = 0;
    if (WideCharToMultiByte(CP_UTF8, WC_ERR_INVALID_CHARS, wide, -1, text, 65536, NULL, NULL)) return true;
    text[0] = 0;
    return ra_fail(error, RA_RANGE, 0, "file path is invalid Unicode or exceeds the UTF-8 path limit");
}

static void open_map_file(void)
{
    wchar_t path[32768] = L"";
    OPENFILENAMEW dialog = {0};
    dialog.lStructSize = sizeof(dialog);
    dialog.hwndOwner = app.window;
    dialog.lpstrFilter = L"红警2地图 (*.map;*.mpr)\0*.map;*.mpr\0所有文件\0*.*\0\0";
    dialog.lpstrFile = path;
    dialog.nMaxFile = 32768;
    dialog.Flags = OFN_FILEMUSTEXIST | OFN_PATHMUSTEXIST | OFN_NOCHANGEDIR;
    if (GetOpenFileNameW(&dialog))
    {
        char utf8[65536];
        ra_file file = {0};
        ra_error error = {0};
        if (file_path(path, utf8, &error) && ra_file_open(&file, utf8, &error)) load_bytes(file.view, utf8);
        else error_status(&error);
        ra_file_close(&file);
    }
}

static void export_image(void)
{
    wchar_t path[32768] = L"地图预览.bmp";
    OPENFILENAMEW dialog = {0};
    ra_error error = {0};
    char utf8[65536];
    if (!app.image.pixels) return;
    dialog.lStructSize = sizeof(dialog);
    dialog.hwndOwner = app.window;
    dialog.lpstrFilter = L"位图 (*.bmp)\0*.bmp\0\0";
    dialog.lpstrDefExt = L"bmp";
    dialog.lpstrFile = path;
    dialog.nMaxFile = 32768;
    dialog.Flags = OFN_OVERWRITEPROMPT | OFN_NOCHANGEDIR;
    if (!GetSaveFileNameW(&dialog)) return;
    if (!file_path(path, utf8, &error) || !map_image_bmp(&app.image, utf8, &error)) error_status(&error);
}

static LRESULT CALLBACK window_proc(HWND window, UINT message, WPARAM wparam, LPARAM lparam)
{
    if (message == WM_CREATE)
    {
        app.window = window;
        app.font = CreateFontW(-17, 0, 0, 0, FW_NORMAL, FALSE, FALSE, FALSE, DEFAULT_CHARSET, OUT_DEFAULT_PRECIS, CLIP_DEFAULT_PRECIS, CLEARTYPE_QUALITY,
                               DEFAULT_PITCH, L"Microsoft YaHei UI");
        app.profile = control(L"COMBOBOX", L"", CBS_DROPDOWNLIST, ID_PROFILE);
        SendMessageW(app.profile, CB_ADDSTRING, 0, (LPARAM)L"原版 1.006");
        SendMessageW(app.profile, CB_ADDSTRING, 0, (LPARAM)L"中国 MOD");
        SendMessageW(app.profile, CB_SETCURSEL, 1, 0);
        app.maps = control(L"COMBOBOX", L"", CBS_DROPDOWNLIST | WS_VSCROLL, ID_MAP);
        app.load = control(L"BUTTON", L"查看地图", BS_PUSHBUTTON, ID_LOAD);
        app.file = control(L"BUTTON", L"打开地图文件", BS_PUSHBUTTON, ID_FILE);
        app.overlay = control(L"BUTTON", L"显示覆盖物位置", BS_AUTOCHECKBOX, ID_OVERLAY);
        app.objects = control(L"BUTTON", L"显示起点与地图对象", BS_AUTOCHECKBOX, ID_OBJECTS);
        app.local = control(L"BUTTON", L"仅显示可玩区域", BS_AUTOCHECKBOX, ID_LOCAL);
        SendMessageW(app.overlay, BM_SETCHECK, BST_CHECKED, 0);
        SendMessageW(app.objects, BM_SETCHECK, BST_CHECKED, 0);
        SendMessageW(app.local, BM_SETCHECK, BST_CHECKED, 0);
        app.fit = control(L"BUTTON", L"适合窗口", BS_PUSHBUTTON, ID_FIT);
        app.actual = control(L"BUTTON", L"原始大小", BS_PUSHBUTTON, ID_ACTUAL);
        app.save = control(L"BUTTON", L"导出完整预览图", BS_PUSHBUTTON, ID_SAVE);
        app.theater = control(L"COMBOBOX", L"", CBS_DROPDOWNLIST, ID_THEATER);
        SendMessageW(app.theater, CB_ADDSTRING, 0, (LPARAM)L"温带");
        SendMessageW(app.theater, CB_ADDSTRING, 0, (LPARAM)L"雪地");
        SendMessageW(app.theater, CB_ADDSTRING, 0, (LPARAM)L"城市");
        SendMessageW(app.theater, CB_SETCURSEL, 0, 0);
        app.tmp = control(L"EDIT", L"cliff01.tem", WS_BORDER | ES_AUTOHSCROLL, ID_TMP);
        app.tmp_load = control(L"BUTTON", L"查看 TMP 地形", BS_PUSHBUTTON, ID_TMP_LOAD);
        app.detail = control(L"EDIT", L"正在加载地图资源……", ES_MULTILINE | ES_READONLY | WS_VSCROLL, 0);
        return 0;
    }
    if (message == WM_SIZE)
    {
        layout();
        return 0;
    }
    if (message == WM_GETMINMAXINFO)
    {
        ((MINMAXINFO *)lparam)->ptMinTrackSize = (POINT){1000, 760};
        return 0;
    }
    if (message == WM_COMMAND && !app.busy)
    {
        unsigned id = LOWORD(wparam), event = HIWORD(wparam);
        if (id == ID_PROFILE && event == CBN_SELCHANGE) profile_load((int)SendMessageW(app.profile, CB_GETCURSEL, 0, 0));
        else if (id == ID_MAP && event == CBN_SELCHANGE) load_selected();
        else if (event == BN_CLICKED)
        {
            if (id == ID_LOAD) load_selected();
            else if (id == ID_FILE) open_map_file();
            else if (id == ID_OVERLAY || id == ID_OBJECTS || id == ID_LOCAL) rerender();
            else if (id == ID_TMP_LOAD) load_tmp();
            else if (id == ID_FIT) fit_image();
            else if (id == ID_ACTUAL)
            {
                app.zoom = 1;
                app.pan_x = app.pan_y = 0;
                InvalidateRect(window, NULL, FALSE);
            }
            else if (id == ID_SAVE) export_image();
        }
        return 0;
    }
    if (message == WM_MOUSEWHEEL && app.image.pixels)
    {
        POINT p = {GET_X_LPARAM(lparam), GET_Y_LPARAM(lparam)};
        double previous = app.zoom;
        ScreenToClient(window, &p);
        if (!PtInRect(&app.canvas, p)) return 0;
        app.zoom *= GET_WHEEL_DELTA_WPARAM(wparam) > 0 ? 1.25 : 0.8;
        if (app.zoom < 0.02) app.zoom = 0.02;
        if (app.zoom > 8) app.zoom = 8;
        app.pan_x = p.x - app.canvas.left - (p.x - app.canvas.left - app.pan_x) * app.zoom / previous;
        app.pan_y = p.y - app.canvas.top - (p.y - app.canvas.top - app.pan_y) * app.zoom / previous;
        InvalidateRect(window, NULL, FALSE);
        return 0;
    }
    if (message == WM_LBUTTONDOWN)
    {
        app.drag = (POINT){GET_X_LPARAM(lparam), GET_Y_LPARAM(lparam)};
        if (PtInRect(&app.canvas, app.drag))
        {
            inspect_cell(app.drag.x, app.drag.y);
            app.dragging = true;
            SetCapture(window);
        }
        return 0;
    }
    if (message == WM_MOUSEMOVE && app.dragging)
    {
        POINT p = {GET_X_LPARAM(lparam), GET_Y_LPARAM(lparam)};
        app.pan_x += p.x - app.drag.x;
        app.pan_y += p.y - app.drag.y;
        app.drag = p;
        InvalidateRect(window, NULL, FALSE);
        return 0;
    }
    if (message == WM_LBUTTONUP || message == WM_CAPTURECHANGED)
    {
        app.dragging = false;
        if (GetCapture() == window) ReleaseCapture();
        return 0;
    }
    if (message == WM_ERASEBKGND) return 1;
    if (message == WM_PAINT)
    {
        PAINTSTRUCT p;
        HDC dc = BeginPaint(window, &p);
        paint(dc);
        EndPaint(window, &p);
        return 0;
    }
    if (message == WM_PRINTCLIENT)
    {
        paint((HDC)wparam);
        return 0;
    }
    if (message == WM_DESTROY)
    {
        PostQuitMessage(0);
        return 0;
    }
    return DefWindowProcW(window, message, wparam, lparam);
}

/* 自检通过真实窗口消息操作控件，截图包含系统实际绘制的中文界面。 */
static bool snapshot(const char *path)
{
    RECT client;
    BITMAPINFO info = {0};
    HDC screen, dc;
    HBITMAP bitmap, old;
    MSG pending;
    void *bits = NULL;
    map_image image = {0};
    ra_error error = {0};
    bool ok;
    while (PeekMessageW(&pending, NULL, 0, 0, PM_REMOVE))
    {
        TranslateMessage(&pending);
        DispatchMessageW(&pending);
    }
    GetClientRect(app.window, &client);
    info.bmiHeader.biSize = sizeof(BITMAPINFOHEADER);
    info.bmiHeader.biWidth = client.right;
    info.bmiHeader.biHeight = -client.bottom;
    info.bmiHeader.biPlanes = 1;
    info.bmiHeader.biBitCount = 32;
    screen = GetDC(app.window);
    dc = CreateCompatibleDC(screen);
    bitmap = CreateDIBSection(screen, &info, DIB_RGB_COLORS, &bits, NULL, 0);
    ReleaseDC(app.window, screen);
    if (!dc || !bitmap || !bits)
    {
        if (dc) DeleteDC(dc);
        if (bitmap) DeleteObject(bitmap);
        return false;
    }
    old = SelectObject(dc, bitmap);
    RedrawWindow(app.window, NULL, NULL, RDW_INVALIDATE | RDW_UPDATENOW | RDW_ALLCHILDREN);
    DwmFlush();
    ok = PrintWindow(app.window, dc, PW_CLIENTONLY | 2u) != 0;
    GdiFlush();
    image.pixels = bits;
    image.width = client.right;
    image.height = client.bottom;
    if (ok) ok = map_image_bmp(&image, path, &error);
    SelectObject(dc, old);
    DeleteObject(bitmap);
    DeleteDC(dc);
    return ok;
}

static int self_test(const char *directory)
{
    const char *names[] = {"MP02T2.map", "MP21S2.map", "MP29U2.map"};
    const wchar_t *tiles[] = {L"cliff01.tem", L"shore01.sno", L"clear01.urb"};
    size_t i, j;
    int profile, checks = 0, failures = 0;
    char path[32768];
    uint8_t before[20], after[20];
    ra_error error = {0};
#define VERIFY(expr)                                                                                                                                           \
    do                                                                                                                                                         \
    {                                                                                                                                                          \
        ++checks;                                                                                                                                              \
        if (!(expr))                                                                                                                                           \
        {                                                                                                                                                      \
            ++failures;                                                                                                                                        \
            fprintf(stderr, "MAP VIEWER FAIL: %s\n", #expr);                                                                                                   \
        }                                                                                                                                                      \
    } while (0)
    {
        char utf8[65536];
        wchar_t invalid[] = {0xd800, 0};
        wchar_t *long_path = calloc(24001, sizeof(*long_path));
        VERIFY(file_path(L"测试.map", utf8, &error) && !strcmp(utf8, "测试.map"));
        VERIFY(!file_path(invalid, utf8, &error) && !utf8[0]);
        if (long_path)
            for (i = 0; i < 24000; ++i) long_path[i] = L'地';
        VERIFY(long_path && !file_path(long_path, utf8, &error) && !utf8[0]);
        free(long_path);
    }
    for (profile = 0; profile < 2; ++profile)
    {
        SendMessageW(app.profile, CB_SETCURSEL, (WPARAM)profile, 0);
        SendMessageW(app.window, WM_COMMAND, MAKEWPARAM(ID_PROFILE, CBN_SELCHANGE), (LPARAM)app.profile);
        VERIFY(app.current == profile && app.ready[profile] && app.contexts[profile].source_count == 131);
        for (i = 0; i < 3; ++i)
        {
            for (j = 0; j < app.contexts[profile].source_count; ++j)
                if (ra_equal(app.contexts[profile].sources[j].name, names[i])) break;
            SendMessageW(app.maps, CB_SETCURSEL, (WPARAM)j, 0);
            SendMessageW(app.load, BM_CLICK, 0, 0);
            VERIFY(!app.tmp_mode && app.map.cell_count > 1000 && app.image.drawn > 100000 && !app.image.missing);
            VERIFY(map_theater_id(app.map.theater) == (int)i);
            VERIFY(strstr(app.source, profile ? app.mod : app.original) != NULL);
            snprintf(path, sizeof(path), "%s/%s-%zu.bmp", directory, profile ? "china" : "original", i);
            VERIFY(snapshot(path));
        }
    }
    ra_sha1((ra_view){(const uint8_t *)app.image.pixels, (size_t)app.image.width * app.image.height * 4}, before);
    SendMessageW(app.objects, BM_CLICK, 0, 0);
    ra_sha1((ra_view){(const uint8_t *)app.image.pixels, (size_t)app.image.width * app.image.height * 4}, after);
    VERIFY(memcmp(before, after, 20));
    SendMessageW(app.objects, BM_CLICK, 0, 0);
    SendMessageW(app.overlay, BM_CLICK, 0, 0);
    VERIFY(!checked(app.overlay));
    SendMessageW(app.overlay, BM_CLICK, 0, 0);
    SendMessageW(app.local, BM_CLICK, 0, 0);
    VERIFY(app.image.width == app.map.size[2] * 60);
    SendMessageW(app.local, BM_CLICK, 0, 0);
    SendMessageW(app.actual, BM_CLICK, 0, 0);
    VERIFY(app.zoom == 1);
    {
        POINT p = {app.canvas.left + 100, app.canvas.top + 100};
        double pan = app.pan_x;
        SendMessageW(app.window, WM_LBUTTONDOWN, MK_LBUTTON, MAKELPARAM(p.x, p.y));
        SendMessageW(app.window, WM_MOUSEMOVE, MK_LBUTTON, MAKELPARAM(p.x + 20, p.y + 10));
        SendMessageW(app.window, WM_LBUTTONUP, 0, MAKELPARAM(p.x + 20, p.y + 10));
        VERIFY(app.pan_x == pan + 20 && !app.dragging);
        ClientToScreen(app.window, &p);
        SendMessageW(app.window, WM_MOUSEWHEEL, MAKEWPARAM(0, WHEEL_DELTA), MAKELPARAM(p.x, p.y));
        VERIFY(app.zoom == 1.25);
    }
    SendMessageW(app.fit, BM_CLICK, 0, 0);
    VERIFY(app.zoom < 1);
    for (i = 0; i < 3; ++i)
    {
        SendMessageW(app.theater, CB_SETCURSEL, (WPARAM)i, 0);
        SetWindowTextW(app.tmp, tiles[i]);
        SendMessageW(app.tmp_load, BM_CLICK, 0, 0);
        VERIFY(app.tmp_mode && app.image.drawn > 100 && app.image.width < 1000);
        snprintf(path, sizeof(path), "%s/tmp-%zu.bmp", directory, i);
        VERIFY(snapshot(path));
    }
    SetWindowTextW(app.tmp, L"missing.tmp");
    SendMessageW(app.tmp_load, BM_CLICK, 0, 0);
    VERIFY(app.tmp_mode && wcsstr(app.status, L"读取失败"));
    snprintf(path, sizeof(path), "%s/export.bmp", directory);
    VERIFY(map_image_bmp(&app.image, path, &error));
    printf("{\"checks\":%d,\"failures\":%d,\"profiles\":2,\"snapshots\":9}\n", checks, failures);
    return failures ? 1 : 0;
#undef VERIFY
}

static int app_main(int argc, char **argv)
{
    WNDCLASSW type = {0};
    HWND window;
    MSG message;
    const char *test = NULL;
    int i, result = 0;
    app.original = "H:/开发/运行版本/原版1.006";
    app.mod = "H:/开发/运行版本/中国开局验证";
    app.zoom = 1;
    app.busy = true;
    for (i = 1; i < argc; ++i)
    {
        if (i + 1 < argc && !strcmp(argv[i], "--original")) app.original = argv[++i];
        else if (i + 1 < argc && !strcmp(argv[i], "--mod")) app.mod = argv[++i];
        else if (i + 1 < argc && !strcmp(argv[i], "--self-test")) test = argv[++i];
        else return 2;
    }
    SetProcessDPIAware();
    type.lpfnWndProc = window_proc;
    type.hInstance = GetModuleHandleW(NULL);
    type.lpszClassName = L"RA2PureCMapViewer";
    type.hCursor = LoadCursorW(NULL, IDC_ARROW);
    if (!RegisterClassW(&type)) return 1;
    window = CreateWindowExW(0, type.lpszClassName, L"红色警戒2 · 地图预览", WS_OVERLAPPEDWINDOW | WS_CLIPCHILDREN, CW_USEDEFAULT, CW_USEDEFAULT, 1360, 920,
                             NULL, NULL, type.hInstance, NULL);
    if (!window) return 1;
    layout();
    app.busy = false;
    ShowWindow(window, test ? SW_SHOWNOACTIVATE : SW_SHOW);
    UpdateWindow(window);
    if (test) result = self_test(test);
    else
    {
        profile_load(1);
        while (GetMessageW(&message, NULL, 0, 0) > 0)
        {
            if (!IsDialogMessageW(window, &message))
            {
                TranslateMessage(&message);
                DispatchMessageW(&message);
            }
        }
    }
    if (IsWindow(window)) DestroyWindow(window);
    ra_map_close(&app.map);
    map_image_close(&app.image);
    for (i = 0; i < 2; ++i) map_context_close(&app.contexts[i]);
    DeleteObject(app.font);
    return result;
}
