#define _CRT_SECURE_NO_WARNINGS
#define UNICODE
#define _UNICODE
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <windowsx.h>
#include <commdlg.h>
#include <dwmapi.h>
#include <wchar.h>
#include <limits.h>
#include <math.h>
#include <stdlib.h>
#include <string.h>
#include "internal.h"
#include "voxel_scene.h"
#include "voxel_catalog.h"
#include "entry.h"

enum { ID_PROFILE = 200, ID_MODEL, ID_LOAD, ID_PREV, ID_NEXT, ID_FRAME, ID_JUMP, ID_PLAY, ID_LEFT, ID_RIGHT, ID_UP, ID_DOWN,
    ID_TURRET_LEFT, ID_TURRET_RIGHT, ID_REMAP, ID_COLOR, ID_VPL, ID_ASSEMBLE, ID_SECTIONS, ID_PALETTE, ID_EXPORT, ID_RESET };
typedef struct {
    HWND window, profile, model, load, previous, next, frame_edit, jump, play, left, right, up, down, turret_left, turret_right;
    HWND remap, color, vpl, assemble, sections, palette, detail, export_button, reset;
    HFONT font, heading;
    voxel_context profiles[2];
    bool loaded[2], busy, playing, dirty, dragging;
    int current, selected_part, selected_section;
    POINT drag_start;
    const char *original, *mod;
    voxel_scene scene;
    ra_voxel_camera camera;
    ra_voxel_image image;
    ra_palette colors;
    size_t frame;
    RECT canvas;
    wchar_t status[1024];
} voxel_app;
static voxel_app app;

/* 平台显示辅助函数与上一阶段保持相同的 UTF-8 和只读窗口约定。 */
static wchar_t *wide_bytes(const char *text, size_t length)
{
    wchar_t *wide;
    int count;
    size_t i;
    if (length > INT_MAX) return NULL;
    count = MultiByteToWideChar(CP_UTF8, MB_ERR_INVALID_CHARS, text, (int)length, NULL, 0);
    if (!count && length) return NULL;
    wide = calloc((size_t)count + 1, sizeof(*wide));
    if (!wide) return NULL;
    if (count) MultiByteToWideChar(CP_UTF8, MB_ERR_INVALID_CHARS, text, (int)length, wide, count);
    /* 内嵌零以可见符号显示，避免窗口把后续文本截断。 */
    for (i = 0; i < (size_t)count; ++i) if (!wide[i]) wide[i] = 0x2400;
    return wide;
}

static wchar_t *wide_text(const char *text)
{
    return wide_bytes(text, strlen(text));
}

static char *control_utf8(HWND control)
{
    int length = GetWindowTextLengthW(control), bytes;
    wchar_t *wide = calloc((size_t)length + 1, sizeof(*wide));
    char *text = NULL;
    if (!wide) return NULL;
    GetWindowTextW(control, wide, length + 1);
    bytes = WideCharToMultiByte(CP_UTF8, WC_ERR_INVALID_CHARS, wide, -1, NULL, 0, NULL, NULL);
    if (bytes > 0) text = malloc((size_t)bytes);
    if (text) WideCharToMultiByte(CP_UTF8, WC_ERR_INVALID_CHARS, wide, -1, text, bytes, NULL, NULL);
    free(wide);
    return text;
}

static void fill(HDC dc, RECT rectangle, COLORREF color)
{
    HBRUSH brush = CreateSolidBrush(color);
    FillRect(dc, &rectangle, brush);
    DeleteObject(brush);
}

static void draw_label(HDC dc, int x, int y, int width, int height, const wchar_t *text, COLORREF color)
{
    RECT rectangle = {x, y, x + width, y + height};
    SetTextColor(dc, color);
    DrawTextW(dc, text, -1, &rectangle, DT_LEFT | DT_WORDBREAK | DT_NOPREFIX);
}

static HWND control(const wchar_t *type, const wchar_t *text, DWORD style, int id)
{
    HWND handle = CreateWindowExW(0, type, text, WS_CHILD | WS_VISIBLE | WS_TABSTOP | style, 0, 0, 10, 10, app.window,
        (HMENU)(INT_PTR)id, GetModuleHandleW(NULL), NULL);
    SendMessageW(handle, WM_SETFONT, (WPARAM)app.font, TRUE);
    return handle;
}

static void error_status(const ra_error *error)
{
    wchar_t *message = wide_text(error->message);
    swprintf(app.status, 1024, L"读取失败：%ls", message ? message : L"内存不足");
    free(message);
    InvalidateRect(app.window, NULL, FALSE);
}

static void update_status(void)
{
    wchar_t number[32];
    size_t i, count = 0;
    for (i = 0; i < app.scene.count; ++i) count += app.scene.models[i].vxl.voxel_count;
    swprintf(number, 32, L"%zu", app.frame + 1);
    SetWindowTextW(app.frame_edit, number);
    swprintf(app.status, 1024, L"%zu 个体素 · %zu 个模型部件 · HVA 第 %zu / %zu 帧 · 方向 %.0f° · 俯角 %.0f° · %.2f 倍\n%ls",
        count, app.scene.count, app.frame + 1, app.scene.frames, app.camera.yaw, app.camera.pitch, app.camera.zoom,
        app.scene.frames > 1 ? L"正在使用实际 HVA 多帧动画；视角与炮塔转向独立控制。" : L"该资源 HVA 只有一帧，显示静态姿态。鼠标拖动旋转，滚轮缩放。");
    app.dirty = true;
    InvalidateRect(app.window, NULL, FALSE);
}

static void update_detail(void)
{
    wchar_t display[8192], *title = wide_text(app.scene.title ? app.scene.title : app.scene.id), *image = wide_text(app.scene.image);
    size_t used, i;
    used = (size_t)swprintf(display, 8192, L"%.256ls\r\n\r\n规则对象：%.128hs\r\n图像映射：%.128ls\r\n\r\n", title ? title : L"", app.scene.id, image ? image : L"");
    free(title);
    free(image);
    for (i = 0; i < app.scene.count; ++i) {
        wchar_t *source = wide_text(app.scene.models[i].source), *animation = wide_text(app.scene.models[i].animation_source);
        size_t j, unmapped = 0;
        for (j = 0; j < app.scene.models[i].vxl.section_count; ++j) unmapped += app.scene.models[i].vxl.sections[j].unmapped_normals;
        used += (size_t)swprintf(display + used, 8192 - used, L"部件 %zu\r\n%.800ls\r\n%.800ls\r\n未定义法线：%zu 个（保留原值，以统一方向预览）\r\n\r\n",
            i + 1, source ? source : L"", animation ? animation : L"", unmapped);
        if (app.scene.models[i].index_binding) used += (size_t)swprintf(display + used, 8192 - used, L"名称不同：单节按顺序匹配。\r\n\r\n");
        free(source);
        free(animation);
    }
    used += (size_t)swprintf(display + used, 8192 - used, L"VPL：%u 个明暗查色表\r\n重映射范围：%u..%u\r\n\r\n",
        app.profiles[app.current].vpl.section_count, app.profiles[app.current].vpl.remap_start, app.profiles[app.current].vpl.remap_end);
    swprintf(display + used, 8192 - used, L"%ls", app.current ? L"中国模型按规则复用原版资源，来源路径如上。" : L"原版 1.006 资源只读预览。");
    SetWindowTextW(app.detail, display);
}

static bool render_current(void)
{
    ra_error error = {0};
    const ra_voxel_part *parts = app.scene.parts;
    ra_voxel_part selected;
    size_t count = app.scene.count;
    ra_voxel_camera camera = app.camera;
    if (!count) return false;
    if (app.selected_part >= 0) {
        selected = app.scene.parts[app.selected_part];
        parts = &selected;
        count = 1;
        camera.section = app.selected_section;
    }
    if (!ra_voxel_render(parts, count, app.frame, &app.colors, &app.profiles[app.current].vpl, &camera, &app.image, &error)) {
        error_status(&error);
        return false;
    }
    app.dirty = false;
    return true;
}

static bool load_model(void)
{
    char *id = control_utf8(app.model);
    voxel_scene scene = {0};
    ra_error error = {0};
    size_t i, j;
    bool assemble = SendMessageW(app.assemble, BM_GETCHECK, 0, 0) == BST_CHECKED;
    bool ok = id && voxel_scene_load(&scene, &app.profiles[app.current], id, assemble, &error);
    free(id);
    if (!ok) {
        error_status(&error);
        return false;
    }
    voxel_scene_close(&app.scene);
    app.scene = scene;
    for (i = 0; i < app.scene.count; ++i) {
        app.scene.parts[i].vxl = &app.scene.models[i].vxl;
        app.scene.parts[i].hva = &app.scene.models[i].hva;
        app.scene.parts[i].mapping = app.scene.models[i].mapping;
    }
    app.frame = 0;
    app.playing = false;
    app.selected_part = app.selected_section = -1;
    SetWindowTextW(app.play, L"播放 HVA");
    EnableWindow(app.play, app.scene.frames > 1);
    SendMessageW(app.sections, CB_RESETCONTENT, 0, 0);
    SendMessageW(app.sections, CB_ADDSTRING, 0, (LPARAM)L"全部部件");
    SendMessageW(app.sections, CB_SETITEMDATA, 0, (LPARAM)-1);
    for (i = 0; i < app.scene.count; ++i) {
        for (j = 0; j < app.scene.models[i].vxl.section_count; ++j) {
            const ra_vxl_section *section = &app.scene.models[i].vxl.sections[j];
            wchar_t row[256], *name = wide_text(section->name);
            LRESULT at;
            swprintf(row, 256, L"部件%zu / %ls · %u×%u×%u", i + 1, name ? name : L"", section->size[0], section->size[1], section->size[2]);
            at = SendMessageW(app.sections, CB_ADDSTRING, 0, (LPARAM)row);
            if (at >= 0) SendMessageW(app.sections, CB_SETITEMDATA, (WPARAM)at, (LPARAM)((i << 16) | j));
            free(name);
        }
    }
    SendMessageW(app.sections, CB_SETCURSEL, 0, 0);
    update_detail();
    update_status();
    return render_current();
}

static bool load_profile(int number)
{
    ra_error error = {0};
    size_t i;
    static const wchar_t *original_ids[] = {L"HTNK", L"MTNK", L"CARRIER", L"DEST", L"BEAG", L"SHAD", L"hmec.vxl"};
    static const wchar_t *china_ids[] = {L"CNLTNK", L"CNAPOC", L"CARRIER2", L"DEST2", L"J10", L"SEEK", L"hmec.vxl"};
    if (!app.loaded[number]) {
        SetCursor(LoadCursorW(NULL, IDC_WAIT));
        if (!voxel_context_open(&app.profiles[number], app.original, number ? app.mod : NULL, &error)) {
            SetCursor(LoadCursorW(NULL, IDC_ARROW));
            error_status(&error);
            SendMessageW(app.profile, CB_SETCURSEL, (WPARAM)app.current, 0);
            return false;
        }
        app.loaded[number] = true;
        SetCursor(LoadCursorW(NULL, IDC_ARROW));
    }
    app.busy = true;
    app.current = number;
    app.colors = app.profiles[number].palette;
    SendMessageW(app.profile, CB_SETCURSEL, (WPARAM)number, 0);
    SendMessageW(app.model, CB_RESETCONTENT, 0, 0);
    for (i = 0; i < 7; ++i) SendMessageW(app.model, CB_ADDSTRING, 0, (LPARAM)(number ? china_ids[i] : original_ids[i]));
    for (i = 0; i < sizeof(voxel_names) / sizeof(*voxel_names); ++i) {
        if (strstr(voxel_names[i], ".vxl")) {
            wchar_t *name = wide_text(voxel_names[i]);
            if (name) SendMessageW(app.model, CB_ADDSTRING, 0, (LPARAM)name);
            free(name);
        }
    }
    SetWindowTextW(app.model, number ? L"CNLTNK" : L"HTNK");
    SendMessageW(app.palette, CB_SETCURSEL, 0, 0);
    app.busy = false;
    return load_model();
}

static void layout(void)
{
    RECT client;
    int panel;
    GetClientRect(app.window, &client);
    panel = client.right - 340;
    app.canvas = (RECT){20, 190, panel - 20, client.bottom - 90};
    MoveWindow(app.profile, 85, 87, 300, 200, TRUE);
    MoveWindow(app.model, 400, 87, panel - 500, 460, TRUE);
    MoveWindow(app.load, panel - 90, 86, 70, 31, TRUE);
    MoveWindow(app.previous, 20, 134, 62, 31, TRUE);
    MoveWindow(app.next, 89, 134, 62, 31, TRUE);
    MoveWindow(app.frame_edit, 160, 134, 55, 31, TRUE);
    MoveWindow(app.jump, 223, 134, 55, 31, TRUE);
    MoveWindow(app.play, 288, 134, 90, 31, TRUE);
    MoveWindow(app.left, 390, 134, 60, 31, TRUE);
    MoveWindow(app.right, 456, 134, 60, 31, TRUE);
    MoveWindow(app.up, 522, 134, 60, 31, TRUE);
    MoveWindow(app.down, 588, 134, 60, 31, TRUE);
    MoveWindow(app.reset, 657, 134, 60, 31, TRUE);
    MoveWindow(app.sections, panel + 10, 87, 310, 300, TRUE);
    MoveWindow(app.assemble, panel + 10, 134, 300, 28, TRUE);
    MoveWindow(app.turret_left, panel + 10, 176, 145, 31, TRUE);
    MoveWindow(app.turret_right, panel + 170, 176, 145, 31, TRUE);
    MoveWindow(app.vpl, panel + 10, 222, 300, 28, TRUE);
    MoveWindow(app.remap, panel + 10, 262, 140, 28, TRUE);
    MoveWindow(app.color, panel + 170, 260, 145, 160, TRUE);
    MoveWindow(app.palette, panel + 10, 305, 305, 160, TRUE);
    MoveWindow(app.detail, panel + 10, 352, 305, client.bottom - 445, TRUE);
    MoveWindow(app.export_button, client.right - 130, client.bottom - 70, 110, 32, TRUE);
    InvalidateRect(app.window, NULL, TRUE);
}

static void paint(HDC dc)
{
    RECT client;
    BITMAPINFO info = {0};
    GetClientRect(app.window, &client);
    fill(dc, client, RGB(247,249,252));
    SetBkMode(dc, TRANSPARENT);
    SelectObject(dc, app.heading);
    draw_label(dc, 20, 15, 1000, 35, L"红色警戒2 · 体素预览", RGB(23,40,63));
    SelectObject(dc, app.font);
    draw_label(dc, 20, 55, 1000, 26, L"VXL / HVA / VPL    ·    坦克、舰船、飞机与真实部件动画", RGB(91,107,127));
    draw_label(dc, 20, 93, 65, 26, L"资源集", RGB(42,60,82));
    if (app.dirty) render_current();
    fill(dc, app.canvas, RGB(30,39,52));
    if (app.image.pixels && app.scene.count) {
        int width = min(app.canvas.right - app.canvas.left, MulDiv(app.canvas.bottom - app.canvas.top, (int)app.image.width, (int)app.image.height));
        int height = MulDiv(width, (int)app.image.height, (int)app.image.width);
        int left = app.canvas.left + (app.canvas.right - app.canvas.left - width) / 2;
        int top = app.canvas.top + (app.canvas.bottom - app.canvas.top - height) / 2;
        info.bmiHeader.biSize = sizeof(BITMAPINFOHEADER);
        info.bmiHeader.biWidth = (LONG)app.image.width;
        info.bmiHeader.biHeight = -(LONG)app.image.height;
        info.bmiHeader.biPlanes = 1;
        info.bmiHeader.biBitCount = 32;
        info.bmiHeader.biCompression = BI_RGB;
        SetStretchBltMode(dc, COLORONCOLOR);
        StretchDIBits(dc, left, top, width, height,
            0, 0, (int)app.image.width, (int)app.image.height, app.image.pixels, &info, DIB_RGB_COLORS, SRCCOPY);
    }
    draw_label(dc, 20, client.bottom - 65, client.right - 170, 60, app.status, RGB(60,77,98));
}

static bool save_snapshot(const wchar_t *path)
{
    RECT client;
    BITMAPINFO info = {0};
    BITMAPFILEHEADER header = {0};
    HDC screen, dc;
    HBITMAP bitmap, previous;
    void *bits = NULL;
    FILE *file;
    MSG pending;
    size_t size;
    bool ok;
    while (PeekMessageW(&pending, NULL, 0, 0, PM_REMOVE)) {
        TranslateMessage(&pending);
        DispatchMessageW(&pending);
    }
    GetClientRect(app.window, &client);
    size = (size_t)client.right * client.bottom * 4;
    screen = GetDC(app.window);
    dc = CreateCompatibleDC(screen);
    info.bmiHeader.biSize = sizeof(BITMAPINFOHEADER);
    info.bmiHeader.biWidth = client.right;
    info.bmiHeader.biHeight = -client.bottom;
    info.bmiHeader.biPlanes = 1;
    info.bmiHeader.biBitCount = 32;
    bitmap = CreateDIBSection(screen, &info, DIB_RGB_COLORS, &bits, NULL, 0);
    ReleaseDC(app.window, screen);
    if (!dc || !bitmap || !bits) {
        if (dc) DeleteDC(dc);
        if (bitmap) DeleteObject(bitmap);
        return false;
    }
    previous = SelectObject(dc, bitmap);
    RedrawWindow(app.window, NULL, NULL, RDW_INVALIDATE | RDW_UPDATENOW | RDW_ALLCHILDREN);
    DwmFlush();
    if (!PrintWindow(app.window, dc, PW_CLIENTONLY | 2u)) {
        SelectObject(dc, previous);
        DeleteObject(bitmap);
        DeleteDC(dc);
        return false;
    }
    GdiFlush();
    header.bfType = 0x4d42;
    header.bfOffBits = sizeof(header) + sizeof(BITMAPINFOHEADER);
    header.bfSize = header.bfOffBits + (DWORD)size;
    file = _wfopen(path, L"wb");
    ok = file && fwrite(&header, sizeof(header), 1, file) == 1 && fwrite(&info.bmiHeader, sizeof(BITMAPINFOHEADER), 1, file) == 1;
    if (ok) ok = fwrite(bits, 1, size, file) == size;
    if (file && fclose(file)) ok = false;
    SelectObject(dc, previous);
    DeleteObject(bitmap);
    DeleteDC(dc);
    return ok;
}

static void export_snapshot(void)
{
    wchar_t path[32768] = L"体素预览.bmp";
    OPENFILENAMEW dialog = {0};
    dialog.lStructSize = sizeof(dialog);
    dialog.hwndOwner = app.window;
    dialog.lpstrFilter = L"位图预览 (*.bmp)\0*.bmp\0\0";
    dialog.lpstrFile = path;
    dialog.nMaxFile = 32768;
    dialog.lpstrDefExt = L"bmp";
    dialog.Flags = OFN_OVERWRITEPROMPT | OFN_PATHMUSTEXIST | OFN_NOCHANGEDIR;
    if (GetSaveFileNameW(&dialog) && !save_snapshot(path)) MessageBoxW(app.window, L"无法保存预览图。", L"体素预览", MB_ICONERROR);
}

static void frame_step(int step)
{
    if (!app.scene.frames) return;
    app.frame = step < 0 ? (app.frame ? app.frame - 1 : app.scene.frames - 1) : (app.frame + 1) % app.scene.frames;
    update_status();
}

static LRESULT CALLBACK window_proc(HWND window, UINT message, WPARAM wparam, LPARAM lparam)
{
    if (message == WM_CREATE) {
        app.window = window;
        app.font = CreateFontW(-16, 0, 0, 0, FW_NORMAL, FALSE, FALSE, FALSE, DEFAULT_CHARSET, 0, 0, CLEARTYPE_QUALITY, 0, L"Microsoft YaHei UI");
        app.heading = CreateFontW(-26, 0, 0, 0, FW_SEMIBOLD, FALSE, FALSE, FALSE, DEFAULT_CHARSET, 0, 0, CLEARTYPE_QUALITY, 0, L"Microsoft YaHei UI");
        app.profile = control(L"COMBOBOX", L"", CBS_DROPDOWNLIST, ID_PROFILE);
        SendMessageW(app.profile, CB_ADDSTRING, 0, (LPARAM)L"原版 1.006");
        SendMessageW(app.profile, CB_ADDSTRING, 0, (LPARAM)L"中国 MOD（实际规则映射）");
        app.model = control(L"COMBOBOX", L"", CBS_DROPDOWN | CBS_AUTOHSCROLL | WS_VSCROLL, ID_MODEL);
        app.load = control(L"BUTTON", L"读取", BS_PUSHBUTTON, ID_LOAD);
        app.previous = control(L"BUTTON", L"上一帧", BS_PUSHBUTTON, ID_PREV);
        app.next = control(L"BUTTON", L"下一帧", BS_PUSHBUTTON, ID_NEXT);
        app.frame_edit = control(L"EDIT", L"1", WS_BORDER | ES_NUMBER, ID_FRAME);
        SendMessageW(app.frame_edit, EM_SETLIMITTEXT, 6, 0);
        app.jump = control(L"BUTTON", L"跳转", BS_PUSHBUTTON, ID_JUMP);
        app.play = control(L"BUTTON", L"播放 HVA", BS_PUSHBUTTON, ID_PLAY);
        app.left = control(L"BUTTON", L"左转", BS_PUSHBUTTON, ID_LEFT);
        app.right = control(L"BUTTON", L"右转", BS_PUSHBUTTON, ID_RIGHT);
        app.up = control(L"BUTTON", L"俯视", BS_PUSHBUTTON, ID_UP);
        app.down = control(L"BUTTON", L"平视", BS_PUSHBUTTON, ID_DOWN);
        app.reset = control(L"BUTTON", L"复位", BS_PUSHBUTTON, ID_RESET);
        app.assemble = control(L"BUTTON", L"合成车体、炮塔与炮管", BS_AUTOCHECKBOX, ID_ASSEMBLE);
        SendMessageW(app.assemble, BM_SETCHECK, BST_CHECKED, 0);
        app.turret_left = control(L"BUTTON", L"炮塔向左", BS_PUSHBUTTON, ID_TURRET_LEFT);
        app.turret_right = control(L"BUTTON", L"炮塔向右", BS_PUSHBUTTON, ID_TURRET_RIGHT);
        app.vpl = control(L"BUTTON", L"使用 VPL 明暗查色表", BS_AUTOCHECKBOX, ID_VPL);
        SendMessageW(app.vpl, BM_SETCHECK, BST_CHECKED, 0);
        app.remap = control(L"BUTTON", L"阵营换色", BS_AUTOCHECKBOX, ID_REMAP);
        SendMessageW(app.remap, BM_SETCHECK, BST_CHECKED, 0);
        app.color = control(L"COMBOBOX", L"", CBS_DROPDOWNLIST, ID_COLOR);
        SendMessageW(app.color, CB_ADDSTRING, 0, (LPARAM)L"红色");
        SendMessageW(app.color, CB_ADDSTRING, 0, (LPARAM)L"蓝色");
        SendMessageW(app.color, CB_ADDSTRING, 0, (LPARAM)L"绿色");
        SendMessageW(app.color, CB_ADDSTRING, 0, (LPARAM)L"黄色");
        SendMessageW(app.color, CB_SETCURSEL, 0, 0);
        app.palette = control(L"COMBOBOX", L"", CBS_DROPDOWNLIST, ID_PALETTE);
        SendMessageW(app.palette, CB_ADDSTRING, 0, (LPARAM)L"unittem.pal");
        SendMessageW(app.palette, CB_ADDSTRING, 0, (LPARAM)L"unitsno.pal");
        SendMessageW(app.palette, CB_ADDSTRING, 0, (LPARAM)L"uniturb.pal");
        app.sections = control(L"COMBOBOX", L"", CBS_DROPDOWNLIST, ID_SECTIONS);
        app.detail = control(L"EDIT", L"", WS_BORDER | WS_VSCROLL | ES_MULTILINE | ES_READONLY | ES_AUTOVSCROLL, 0);
        app.export_button = control(L"BUTTON", L"保存预览图", BS_PUSHBUTTON, ID_EXPORT);
        SetTimer(window, 1, 100, NULL);
        return 0;
    }
    if (message == WM_SIZE) {
        layout();
        return 0;
    }
    if (message == WM_GETMINMAXINFO) {
        ((MINMAXINFO *)lparam)->ptMinTrackSize = (POINT){1160,760};
        return 0;
    }
    if (message == WM_COMMAND && !app.busy) {
        int id = LOWORD(wparam), event = HIWORD(wparam);
        /* 文本刷新会同步发回编辑框通知；此处只响应操作，避免再次刷新造成递归。 */
        if (id == ID_FRAME || id == 0) return 0;
        if (id == ID_PROFILE && event == CBN_SELCHANGE) load_profile((int)SendMessageW(app.profile, CB_GETCURSEL, 0, 0));
        else if (id == ID_LOAD || id == ID_ASSEMBLE) load_model();
        else if (id == ID_MODEL && event == CBN_SELENDOK) PostMessageW(window, WM_COMMAND, ID_LOAD, 0);
        else if (id == ID_PREV) frame_step(-1);
        else if (id == ID_NEXT) frame_step(1);
        else if (id == ID_JUMP) {
            wchar_t number[32];
            unsigned long frame;
            GetWindowTextW(app.frame_edit, number, 32);
            frame = wcstoul(number, NULL, 10);
            if (frame && frame <= app.scene.frames) app.frame = frame - 1;
            update_status();
        } else if (id == ID_PLAY && app.scene.frames > 1) {
            app.playing = !app.playing;
            SetWindowTextW(app.play, app.playing ? L"暂停 HVA" : L"播放 HVA");
        } else if (id == ID_LEFT || id == ID_RIGHT) app.camera.yaw += id == ID_LEFT ? -15.0f : 15.0f;
        else if (id == ID_UP || id == ID_DOWN) app.camera.pitch = fminf(80, fmaxf(5, app.camera.pitch + (id == ID_UP ? 10.0f : -10.0f)));
        else if (id == ID_RESET) {
            app.camera.yaw = 45;
            app.camera.pitch = 30;
            app.camera.zoom = 1;
        } else if (id == ID_TURRET_LEFT || id == ID_TURRET_RIGHT) {
            size_t i;
            for (i = 1; i < app.scene.count; ++i) app.scene.parts[i].yaw += id == ID_TURRET_LEFT ? -15.0f : 15.0f;
        } else if (id == ID_REMAP || id == ID_VPL || (id == ID_COLOR && event == CBN_SELCHANGE)) {
            static const ra_rgb colors[] = {{235,65,55},{65,120,245},{75,210,95},{245,210,55}};
            LRESULT color = SendMessageW(app.color, CB_GETCURSEL, 0, 0);
            app.camera.remap = SendMessageW(app.remap, BM_GETCHECK, 0, 0) == BST_CHECKED;
            app.camera.use_vpl = SendMessageW(app.vpl, BM_GETCHECK, 0, 0) == BST_CHECKED;
            if (color >= 0 && color < 4) app.camera.house_color = colors[color];
        } else if (id == ID_PALETTE && event == CBN_SELCHANGE) {
            char *name = control_utf8(app.palette);
            ra_error error = {0};
            if (name && !ra_asset_palette(&app.profiles[app.current].vfs, name, &app.colors, &error)) error_status(&error);
            free(name);
        } else if (id == ID_SECTIONS && event == CBN_SELCHANGE) {
            LRESULT at = SendMessageW(app.sections, CB_GETCURSEL, 0, 0), data = SendMessageW(app.sections, CB_GETITEMDATA, (WPARAM)at, 0);
            app.selected_part = data < 0 ? -1 : (int)(data >> 16);
            app.selected_section = data < 0 ? -1 : (int)(data & 65535);
        } else if (id == ID_EXPORT) export_snapshot();
        if (id != ID_LOAD && id != ID_PROFILE && id != ID_MODEL && id != ID_ASSEMBLE) update_status();
        return 0;
    }
    if (message == WM_LBUTTONDOWN) {
        POINT point = {GET_X_LPARAM(lparam), GET_Y_LPARAM(lparam)};
        if (PtInRect(&app.canvas, point)) {
            app.dragging = true;
            app.drag_start = point;
            SetCapture(window);
        }
    }
    if (message == WM_MOUSEMOVE && app.dragging) {
        POINT point = {GET_X_LPARAM(lparam), GET_Y_LPARAM(lparam)};
        app.camera.yaw += (float)(point.x - app.drag_start.x) * 0.5f;
        app.camera.pitch = fminf(80, fmaxf(5, app.camera.pitch + (float)(point.y - app.drag_start.y) * 0.3f));
        app.drag_start = point;
        update_status();
    }
    if (message == WM_LBUTTONUP || message == WM_CAPTURECHANGED) {
        app.dragging = false;
        if (message == WM_LBUTTONUP && GetCapture() == window) ReleaseCapture();
    }
    if (message == WM_MOUSEWHEEL) {
        app.camera.zoom = fminf(3, fmaxf(0.25f, app.camera.zoom * (GET_WHEEL_DELTA_WPARAM(wparam) > 0 ? 1.1f : 0.9f)));
        update_status();
        return 0;
    }
    if (message == WM_TIMER && app.playing) frame_step(1);
    if (message == WM_ERASEBKGND) return 1;
    if (message == WM_PAINT) {
        PAINTSTRUCT state;
        HDC dc = BeginPaint(window, &state);
        paint(dc);
        EndPaint(window, &state);
        return 0;
    }
    if (message == WM_PRINTCLIENT) {
        paint((HDC)wparam);
        return 0;
    }
    if (message == WM_DESTROY) {
        KillTimer(window, 1);
        PostQuitMessage(0);
        return 0;
    }
    return DefWindowProcW(window, message, wparam, lparam);
}

static int self_test(const char *directory)
{
    static const wchar_t *original[] = {L"MTNK", L"CARRIER", L"BEAG", L"SHAD"};
    static const wchar_t *china[] = {L"CNAPOC", L"CARRIER2", L"J10", L"SEEK"};
    static const wchar_t *kinds[] = {L"tank", L"ship", L"aircraft", L"animation"};
    wchar_t *folder = wide_text(directory), path[32768], detail[8192];
    uint8_t before[20], after[20];
    unsigned checks = 0, failures = 0;
    int profile, item;
#define VERIFY(expr) do { ++checks; if (!(expr)) { ++failures; fprintf(stderr, "VOXEL VIEWER FAIL: %s\n", #expr); } } while (0)
    if (!folder) return 1;
    for (profile = 0; profile < 2; ++profile) {
        SendMessageW(app.profile, CB_SETCURSEL, (WPARAM)profile, 0);
        SendMessageW(app.window, WM_COMMAND, MAKEWPARAM(ID_PROFILE, CBN_SELCHANGE), (LPARAM)app.profile);
        VERIFY(app.current == profile && app.loaded[profile] && app.scene.count == 3);
        for (item = 0; item < 4; ++item) {
            SetWindowTextW(app.model, profile ? china[item] : original[item]);
            SendMessageW(app.load, BM_CLICK, 0, 0);
            VERIFY(app.scene.count > 0 && render_current() && app.image.drawn_pixels > 1000);
            GetWindowTextW(app.detail, detail, 8192);
            VERIFY(wcsstr(detail, L"ra2.mix|local.mix") != NULL);
            if (profile) VERIFY(app.scene.title && strlen(app.scene.title) > 0);
            if (item == 0) {
                VERIFY(app.scene.count == 3);
                SendMessageW(app.turret_right, BM_CLICK, 0, 0);
                VERIFY(app.scene.parts[1].yaw == 15 && app.scene.parts[2].yaw == 15);
                SendMessageW(app.turret_left, BM_CLICK, 0, 0);
            }
            if (item == 3) {
                VERIFY(app.scene.frames > 1);
                render_current();
                ra_sha1((ra_view){(uint8_t *)app.image.pixels, app.image.width * app.image.height * 4}, before);
                SendMessageW(app.next, BM_CLICK, 0, 0);
                render_current();
                ra_sha1((ra_view){(uint8_t *)app.image.pixels, app.image.width * app.image.height * 4}, after);
                VERIFY(app.frame == 1 && memcmp(before, after, 20));
                SendMessageW(app.previous, BM_CLICK, 0, 0);
                VERIFY(app.frame == 0);
                SendMessageW(app.play, BM_CLICK, 0, 0);
                VERIFY(app.playing);
                SendMessageW(app.window, WM_TIMER, 1, 0);
                VERIFY(app.frame == 1);
                SendMessageW(app.play, BM_CLICK, 0, 0);
                VERIFY(!app.playing);
                SetWindowTextW(app.frame_edit, L"1");
                SendMessageW(app.jump, BM_CLICK, 0, 0);
                VERIFY(app.frame == 0);
            }
            swprintf(path, 32768, L"%ls/%ls-%ls.bmp", folder, profile ? L"china" : L"original", kinds[item]);
            VERIFY(save_snapshot(path));
        }
    }
    render_current();
    ra_sha1((ra_view){(uint8_t *)app.image.pixels, app.image.width * app.image.height * 4}, before);
    SendMessageW(app.right, BM_CLICK, 0, 0);
    render_current();
    ra_sha1((ra_view){(uint8_t *)app.image.pixels, app.image.width * app.image.height * 4}, after);
    VERIFY(memcmp(before, after, 20));
    SendMessageW(app.vpl, BM_CLICK, 0, 0);
    render_current();
    ra_sha1((ra_view){(uint8_t *)app.image.pixels, app.image.width * app.image.height * 4}, before);
    VERIFY(!app.camera.use_vpl && memcmp(before, after, 20));
    SendMessageW(app.vpl, BM_CLICK, 0, 0);
    SendMessageW(app.color, CB_SETCURSEL, 1, 0);
    SendMessageW(app.window, WM_COMMAND, MAKEWPARAM(ID_COLOR, CBN_SELCHANGE), (LPARAM)app.color);
    VERIFY(app.camera.house_color.b == 245);
    SendMessageW(app.sections, CB_SETCURSEL, 1, 0);
    SendMessageW(app.window, WM_COMMAND, MAKEWPARAM(ID_SECTIONS, CBN_SELCHANGE), (LPARAM)app.sections);
    VERIFY(app.selected_part == 0 && app.selected_section == 0 && render_current());
    SetWindowTextW(app.model, L"HTK");
    SendMessageW(app.load, BM_CLICK, 0, 0);
    VERIFY(app.scene.count == 3 && app.scene.models[0].index_binding && render_current() && app.image.drawn_pixels > 1000);
    GetWindowTextW(app.detail, detail, 8192);
    VERIFY(wcsstr(detail, L"单节按顺序匹配") != NULL);
    SetWindowTextW(app.model, L"missing-voxel.vxl");
    SendMessageW(app.load, BM_CLICK, 0, 0);
    VERIFY(app.scene.count > 0 && wcsstr(app.status, L"读取失败"));
    printf("{\"checks\":%u,\"failures\":%u,\"profiles\":2,\"snapshots\":8}\n", checks, failures);
    free(folder);
    return failures ? 1 : 0;
#undef VERIFY
}

static int app_main(int argc, char **argv)
{
    WNDCLASSW type = {0};
    HWND window;
    MSG message;
    ra_error error = {0};
    const char *test = NULL;
    int i, result = 0;
    app.original = "H:/开发/运行版本/原版1.006";
    app.mod = "H:/开发/运行版本/中国开局验证";
    app.camera = (ra_voxel_camera){45,30,1,225,true,true,{235,65,55},-1};
    app.selected_part = app.selected_section = -1;
    app.busy = true;
    for (i = 1; i < argc; ++i) {
        if (i + 1 < argc && !strcmp(argv[i], "--original")) app.original = argv[++i];
        else if (i + 1 < argc && !strcmp(argv[i], "--mod")) app.mod = argv[++i];
        else if (i + 1 < argc && !strcmp(argv[i], "--self-test")) test = argv[++i];
        else return 2;
    }
    if (!ra_voxel_image_create(&app.image, 760, 560, &error)) return 1;
    SetProcessDPIAware();
    type.lpfnWndProc = window_proc;
    type.hInstance = GetModuleHandleW(NULL);
    type.lpszClassName = L"RA2PureCVoxelViewer";
    type.hCursor = LoadCursorW(NULL, IDC_ARROW);
    if (!RegisterClassW(&type)) return 1;
    window = CreateWindowExW(0, type.lpszClassName, L"红色警戒2 · 体素预览", WS_OVERLAPPEDWINDOW | WS_CLIPCHILDREN,
        CW_USEDEFAULT, CW_USEDEFAULT, 1300, 880, NULL, NULL, type.hInstance, NULL);
    if (!window) return 1;
    layout();
    app.busy = false;
    ShowWindow(window, test ? SW_SHOWNOACTIVATE : SW_SHOW);
    UpdateWindow(window);
    if (test) result = self_test(test);
    else {
        load_profile(1);
        while (GetMessageW(&message, NULL, 0, 0) > 0) {
            if (!IsDialogMessageW(window, &message)) {
                TranslateMessage(&message);
                DispatchMessageW(&message);
            }
        }
    }
    if (IsWindow(window)) DestroyWindow(window);
    voxel_scene_close(&app.scene);
    for (i = 0; i < 2; ++i) voxel_context_close(&app.profiles[i]);
    ra_voxel_image_close(&app.image);
    DeleteObject(app.font);
    DeleteObject(app.heading);
    return result;
}
