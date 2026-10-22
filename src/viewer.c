#define _CRT_SECURE_NO_WARNINGS
#define UNICODE
#define _UNICODE
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <windowsx.h>
#include <commdlg.h>
#include <dwmapi.h>
#include <wchar.h>
#include <wctype.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>
#include "internal.h"
#include "asset_profile.h"
#include "asset_catalog.h"
#include "entry.h"

enum { ID_PROFILE = 100, ID_RESOURCE, ID_LOAD, ID_PALETTE, ID_PREV, ID_NEXT, ID_FRAME, ID_GOTO, ID_PLAY, ID_ZOOM, ID_SEARCH, ID_LIST, ID_DETAIL, ID_EXPORT };
typedef struct { ra_vfs vfs; ra_csf csf; ra_resource text; bool loaded; } viewer_profile;
typedef struct {
    HWND window, profile, resource, palette, previous, next, frame_edit, jump, play, zoom, search, list, detail, load, export_button;
    HFONT font, heading;
    viewer_profile profiles[2];
    const char *original, *mod;
    int current, zoom_value;
    ra_resource image;
    ra_shp shp;
    ra_palette colors;
    uint8_t *pixels;
    size_t frame;
    bool palette_only, playing, busy;
    wchar_t status[1024];
    RECT canvas;
} viewer;

static viewer app;

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

static void status_error(const ra_error *error)
{
    wchar_t *message = wide_text(error->message);
    swprintf(app.status, 1024, L"读取失败：%ls", message ? message : L"内存不足");
    free(message);
    InvalidateRect(app.window, NULL, FALSE);
}

static bool contains(const wchar_t *text, const wchar_t *query)
{
    if (!*query) return true;
    for (; *text; ++text) {
        size_t i = 0;
        while (query[i] && text[i] && towlower(query[i]) == towlower(text[i])) ++i;
        if (!query[i]) return true;
    }
    return false;
}

static void show_text(void)
{
    LRESULT selected = SendMessageW(app.list, LB_GETCURSEL, 0, 0);
    const ra_csf *csf = &app.profiles[app.current].csf;
    const ra_csf_label *label;
    wchar_t *display, *name;
    size_t i, capacity = 256, used;
    LRESULT index;
    if (selected == LB_ERR) {
        SetWindowTextW(app.detail, L"没有匹配的文本。");
        return;
    }
    index = SendMessageW(app.list, LB_GETITEMDATA, (WPARAM)selected, 0);
    if (index < 0 || (size_t)index >= csf->label_count) return;
    label = &csf->labels[index];
    capacity += strlen(label->name);
    for (i = 0; i < label->value_count; ++i) capacity += csf->values[label->first_value + i].length + 128;
    display = calloc(capacity, sizeof(*display));
    name = wide_text(label->name);
    if (!display || !name) {
        free(display);
        free(name);
        return;
    }
    used = (size_t)swprintf(display, capacity, L"%ls\r\n\r\n", name);
    free(name);
    for (i = 0; i < label->value_count; ++i) {
        const ra_csf_value *value = &csf->values[label->first_value + i];
        wchar_t *text = wide_bytes(value->text, value->length);
        if (!text) continue;
        used += (size_t)swprintf(display + used, capacity - used, L"%ls\r\n", text);
        free(text);
        if (value->has_extra) used += (size_t)swprintf(display + used, capacity - used, L"附加数据：%zu 字节\r\n", value->extra.size);
    }
    SetWindowTextW(app.detail, display);
    free(display);
}

static void filter_text(void)
{
    wchar_t query[256];
    const ra_csf *csf = &app.profiles[app.current].csf;
    size_t i;
    GetWindowTextW(app.search, query, 256);
    SendMessageW(app.list, WM_SETREDRAW, FALSE, 0);
    SendMessageW(app.list, LB_RESETCONTENT, 0, 0);
    for (i = 0; i < csf->label_count; ++i) {
        const ra_csf_label *label = &csf->labels[i];
        wchar_t *name = wide_text(label->name), *text = NULL;
        bool match;
        size_t j;
        if (!name) continue;
        match = contains(name, query);
        for (j = 0; !match && j < label->value_count; ++j) {
            const ra_csf_value *value = &csf->values[label->first_value + j];
            wchar_t *candidate = wide_bytes(value->text, value->length);
            if (candidate) match = contains(candidate, query);
            free(candidate);
        }
        if (match) {
            wchar_t row[512];
            LRESULT at;
            if (label->value_count) {
                const ra_csf_value *value = &csf->values[label->first_value];
                text = wide_bytes(value->text, value->length);
            }
            swprintf(row, 512, L"%.110ls    %.160ls", name, text ? text : L"");
            for (j = 0; row[j]; ++j) if (row[j] == L'\r' || row[j] == L'\n' || row[j] == L'\t') row[j] = L' ';
            at = SendMessageW(app.list, LB_ADDSTRING, 0, (LPARAM)row);
            if (at >= 0) SendMessageW(app.list, LB_SETITEMDATA, (WPARAM)at, (LPARAM)i);
            free(text);
        }
        free(name);
    }
    SendMessageW(app.list, LB_SETCURSEL, 0, 0);
    SendMessageW(app.list, WM_SETREDRAW, TRUE, 0);
    InvalidateRect(app.list, NULL, TRUE);
    show_text();
}

static void image_status(void)
{
    wchar_t *source = wide_text(app.image.source ? app.image.source : "");
    wchar_t number[32];
    swprintf(number, 32, L"%zu", app.frame + 1);
    SetWindowTextW(app.frame_edit, number);
    if (app.palette_only) swprintf(app.status, 1024, L"PAL · 256 色 · 六位 RGB\n来源：%ls", source ? source : L"");
    else swprintf(app.status, 1024, L"SHP · %u × %u · 第 %zu / %u 帧 · CSF：%zu 个标签\n来源：%ls", app.shp.width, app.shp.height,
        app.frame + 1, app.shp.count, app.profiles[app.current].csf.label_count, source ? source : L"");
    free(source);
    InvalidateRect(app.window, NULL, FALSE);
}

static bool load_image(void)
{
    char *name = control_utf8(app.resource), *palette = control_utf8(app.palette);
    ra_resource resource = {0};
    ra_shp shp = {0};
    ra_palette colors;
    ra_error error = {0};
    uint8_t *pixels = NULL;
    bool pal, ok = false;
    if (!name || !palette) goto done;
    pal = strlen(name) >= 4 && ra_equal(name + strlen(name) - 4, ".pal");
    if (!ra_vfs_read(&app.profiles[app.current].vfs, name, &resource, &error)) goto failed;
    if (pal) {
        if (!ra_palette_parse(&colors, resource.view, &error)) goto failed;
    } else {
        if (!ra_asset_palette(&app.profiles[app.current].vfs, palette, &colors, &error)) goto failed;
        if (!ra_shp_open(&shp, resource.view, &error)) goto failed;
        pixels = malloc(shp.width && shp.height ? (size_t)shp.width * shp.height : 1);
        if (!pixels) {
            ra_fail(&error, RA_MEMORY, 0, "viewer pixel allocation failed");
            goto failed;
        }
        if (!ra_shp_decode(&shp, 0, pixels, (size_t)shp.width * shp.height, &error)) goto failed;
    }
    /* 新资源完全成功后才替换当前画面，读取错误不会破坏已有预览。 */
    ra_shp_close(&app.shp);
    ra_resource_close(&app.image);
    free(app.pixels);
    app.shp = shp;
    memset(&shp, 0, sizeof(shp));
    app.image = resource;
    memset(&resource, 0, sizeof(resource));
    app.colors = colors;
    app.pixels = pixels;
    pixels = NULL;
    app.palette_only = pal;
    app.frame = 0;
    app.playing = false;
    SetWindowTextW(app.play, L"播放");
    image_status();
    ok = true;
    goto done;
failed:
    status_error(&error);
done:
    free(name);
    free(palette);
    free(pixels);
    ra_shp_close(&shp);
    ra_resource_close(&resource);
    return ok;
}

static bool load_profile(int number)
{
    viewer_profile *profile = &app.profiles[number];
    ra_error error = {0};
    size_t i;
    if (!profile->loaded) {
        SetCursor(LoadCursorW(NULL, IDC_WAIT));
        if (!ra_asset_mount(&profile->vfs, app.original, number ? app.mod : NULL, &error) ||
            !ra_vfs_read(&profile->vfs, "ra2.csf", &profile->text, &error) || !ra_csf_parse(&profile->csf, profile->text.view, &error)) {
            ra_csf_close(&profile->csf);
            ra_resource_close(&profile->text);
            ra_vfs_close(&profile->vfs);
            SetCursor(LoadCursorW(NULL, IDC_ARROW));
            status_error(&error);
            SendMessageW(app.profile, CB_SETCURSEL, (WPARAM)app.current, 0);
            return false;
        }
        profile->loaded = true;
        SetCursor(LoadCursorW(NULL, IDC_ARROW));
    }
    app.busy = true;
    app.current = number;
    SendMessageW(app.profile, CB_SETCURSEL, (WPARAM)number, 0);
    SendMessageW(app.resource, CB_RESETCONTENT, 0, 0);
    SendMessageW(app.palette, CB_RESETCONTENT, 0, 0);
    for (i = 0; i < sizeof(asset_names) / sizeof(*asset_names); ++i) {
        ra_resource available = {0};
        if (ra_vfs_read(&profile->vfs, asset_names[i], &available, &error)) {
            wchar_t *name = wide_text(asset_names[i]);
            if (name) {
                SendMessageW(app.resource, CB_ADDSTRING, 0, (LPARAM)name);
                if (strstr(asset_names[i], ".pal")) SendMessageW(app.palette, CB_ADDSTRING, 0, (LPARAM)name);
            }
            free(name);
        }
        ra_resource_close(&available);
    }
    SetWindowTextW(app.resource, number ? L"pla.shp" : L"gi.shp");
    SetWindowTextW(app.palette, L"unittem.pal");
    SetWindowTextW(app.search, number ? L"Name:CNPLA" : L"Name:E1");
    app.busy = false;
    filter_text();
    return load_image();
}

static void set_frame(size_t frame)
{
    ra_error error = {0};
    if (!app.shp.count || app.palette_only) return;
    frame %= app.shp.count;
    if (!ra_shp_decode(&app.shp, frame, app.pixels, (size_t)app.shp.width * app.shp.height, &error)) {
        status_error(&error);
        return;
    }
    app.frame = frame;
    image_status();
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

static void draw_canvas(HDC dc)
{
    int w = app.canvas.right - app.canvas.left, h = app.canvas.bottom - app.canvas.top;
    int x, y;
    fill(dc, app.canvas, RGB(231, 235, 240));
    if (app.palette_only) {
        int size = min(w / 16, h / 16), left = app.canvas.left + (w - size * 16) / 2, top = app.canvas.top + (h - size * 16) / 2;
        for (y = 0; y < 16; ++y) {
            for (x = 0; x < 16; ++x) {
                ra_rgb c = app.colors.colors[y * 16 + x];
                RECT cell = {left + x * size, top + y * size, left + (x + 1) * size - 1, top + (y + 1) * size - 1};
                fill(dc, cell, RGB(c.r, c.g, c.b));
            }
        }
    } else if (app.pixels && app.shp.count && app.shp.width && app.shp.height) {
        BITMAPINFO info = {0};
        size_t count = (size_t)app.shp.width * app.shp.height, i;
        uint32_t *rgb = malloc(count * sizeof(*rgb));
        int scale = app.zoom_value ? app.zoom_value : min(w / app.shp.width, h / app.shp.height);
        int width, height, left, top;
        if (!rgb) return;
        if (scale < 1) scale = 1;
        width = app.shp.width * scale;
        height = app.shp.height * scale;
        /* 大画布按窗口比例缩小，小图保持整数倍率和清晰像素。 */
        if (!app.zoom_value && (width > w || height > h)) {
            double ratio = min((double)w / app.shp.width, (double)h / app.shp.height);
            width = max(1, (int)(app.shp.width * ratio));
            height = max(1, (int)(app.shp.height * ratio));
        }
        left = app.canvas.left + (w - width) / 2;
        top = app.canvas.top + (h - height) / 2;
        for (i = 0; i < count; ++i) {
            unsigned index = app.pixels[i];
            const ra_shp_frame *frame = &app.shp.frames[app.frame];
            size_t px = i % app.shp.width, py = i / app.shp.width;
            ra_rgb c = app.colors.colors[index];
            unsigned background = ((i % app.shp.width / 8 + i / app.shp.width / 8) & 1) ? 220u : 244u;
            bool transparent = !frame->offset || px < frame->x || py < frame->y || px >= (size_t)frame->x + frame->width || py >= (size_t)frame->y + frame->height;
            if (!index && (transparent || (frame->flags & 1u))) c.r = c.g = c.b = (uint8_t)background;
            rgb[i] = ((uint32_t)c.r << 16) | ((uint32_t)c.g << 8) | c.b;
        }
        info.bmiHeader.biSize = sizeof(BITMAPINFOHEADER);
        info.bmiHeader.biWidth = app.shp.width;
        info.bmiHeader.biHeight = -(LONG)app.shp.height;
        info.bmiHeader.biPlanes = 1;
        info.bmiHeader.biBitCount = 32;
        info.bmiHeader.biCompression = BI_RGB;
        SaveDC(dc);
        IntersectClipRect(dc, app.canvas.left, app.canvas.top, app.canvas.right, app.canvas.bottom);
        SetStretchBltMode(dc, COLORONCOLOR);
        StretchDIBits(dc, left, top, width, height, 0, 0, app.shp.width, app.shp.height, rgb, &info, DIB_RGB_COLORS, SRCCOPY);
        RestoreDC(dc, -1);
        free(rgb);
    } else {
        draw_label(dc, app.canvas.left + 20, app.canvas.top + 20, w - 40, 40, L"空白图像", RGB(91, 107, 127));
    }
}

static void paint(HDC dc)
{
    RECT client;
    int right;
    GetClientRect(app.window, &client);
    right = max(570, (client.right * 55) / 100);
    fill(dc, client, RGB(247, 249, 252));
    SetBkMode(dc, TRANSPARENT);
    SelectObject(dc, app.heading);
    draw_label(dc, 20, 15, 800, 40, L"红色警戒2 · 资源查看器", RGB(23, 40, 63));
    SelectObject(dc, app.font);
    draw_label(dc, 20, 57, 800, 24, L"PAL / SHP / CSF    ·    原版与中国 MOD 资源只读预览", RGB(91, 107, 127));
    draw_label(dc, 20, 94, 65, 24, L"资源集", RGB(42, 60, 82));
    draw_label(dc, 20, 135, 55, 24, L"文件", RGB(42, 60, 82));
    draw_label(dc, right + 20, 94, 360, 24, L"中文文本 · 按标签或内容搜索", RGB(42, 60, 82));
    draw_label(dc, 20, client.bottom - 105, 65, 24, L"调色板", RGB(42, 60, 82));
    draw_canvas(dc);
    draw_label(dc, 20, client.bottom - 61, client.right - 40, 58, app.status, RGB(60, 77, 98));
}

static HWND control(const wchar_t *type, const wchar_t *text, DWORD style, int id)
{
    HWND handle = CreateWindowExW(0, type, text, WS_CHILD | WS_VISIBLE | WS_TABSTOP | style, 0, 0, 10, 10, app.window,
        (HMENU)(INT_PTR)id, GetModuleHandleW(NULL), NULL);
    SendMessageW(handle, WM_SETFONT, (WPARAM)app.font, TRUE);
    return handle;
}

static void layout(void)
{
    RECT client;
    int right, left_width, text_width;
    GetClientRect(app.window, &client);
    right = max(570, (client.right * 55) / 100);
    left_width = right - 40;
    text_width = client.right - right - 40;
    app.canvas = (RECT){20, 214, right - 20, client.bottom - 120};
    MoveWindow(app.profile, 85, 89, left_width - 65, 200, TRUE);
    MoveWindow(app.resource, 75, 129, left_width - 150, 400, TRUE);
    MoveWindow(app.load, right - 90, 128, 70, 31, TRUE);
    MoveWindow(app.previous, 20, 174, 65, 30, TRUE);
    MoveWindow(app.next, 92, 174, 65, 30, TRUE);
    MoveWindow(app.frame_edit, 167, 174, 65, 30, TRUE);
    MoveWindow(app.jump, 240, 174, 65, 30, TRUE);
    MoveWindow(app.play, 314, 174, 70, 30, TRUE);
    MoveWindow(app.zoom, right - 140, 174, 120, 180, TRUE);
    MoveWindow(app.palette, 85, client.bottom - 111, left_width - 150, 350, TRUE);
    MoveWindow(app.export_button, right - 90, client.bottom - 111, 70, 31, TRUE);
    MoveWindow(app.search, right + 20, 128, text_width, 31, TRUE);
    MoveWindow(app.list, right + 20, 174, text_width, client.bottom - 429, TRUE);
    MoveWindow(app.detail, right + 20, client.bottom - 240, text_width, 120, TRUE);
    InvalidateRect(app.window, NULL, TRUE);
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
    wchar_t path[32768] = L"资源预览.bmp";
    OPENFILENAMEW dialog = {0};
    dialog.lStructSize = sizeof(dialog);
    dialog.hwndOwner = app.window;
    dialog.lpstrFilter = L"位图预览 (*.bmp)\0*.bmp\0\0";
    dialog.lpstrFile = path;
    dialog.nMaxFile = 32768;
    dialog.lpstrDefExt = L"bmp";
    dialog.Flags = OFN_OVERWRITEPROMPT | OFN_PATHMUSTEXIST | OFN_NOCHANGEDIR;
    if (GetSaveFileNameW(&dialog) && !save_snapshot(path)) MessageBoxW(app.window, L"无法保存预览图。", L"资源查看器", MB_ICONERROR);
}

static LRESULT CALLBACK window_proc(HWND window, UINT message, WPARAM wparam, LPARAM lparam)
{
    if (message == WM_CREATE) {
        size_t i;
        static const wchar_t *zooms[] = {L"适合窗口", L"1 ×", L"2 ×", L"4 ×", L"8 ×"};
        app.window = window;
        app.font = CreateFontW(-16, 0, 0, 0, FW_NORMAL, FALSE, FALSE, FALSE, DEFAULT_CHARSET, 0, 0, CLEARTYPE_QUALITY, 0, L"Microsoft YaHei UI");
        app.heading = CreateFontW(-26, 0, 0, 0, FW_SEMIBOLD, FALSE, FALSE, FALSE, DEFAULT_CHARSET, 0, 0, CLEARTYPE_QUALITY, 0, L"Microsoft YaHei UI");
        app.profile = control(L"COMBOBOX", L"", CBS_DROPDOWNLIST, ID_PROFILE);
        SendMessageW(app.profile, CB_ADDSTRING, 0, (LPARAM)L"原版 1.006");
        SendMessageW(app.profile, CB_ADDSTRING, 0, (LPARAM)L"中国 MOD（叠加原版资源）");
        app.resource = control(L"COMBOBOX", L"", CBS_DROPDOWN | CBS_AUTOHSCROLL | WS_VSCROLL, ID_RESOURCE);
        app.load = control(L"BUTTON", L"读取", BS_PUSHBUTTON, ID_LOAD);
        app.palette = control(L"COMBOBOX", L"", CBS_DROPDOWN | CBS_AUTOHSCROLL | WS_VSCROLL, ID_PALETTE);
        app.previous = control(L"BUTTON", L"上一帧", BS_PUSHBUTTON, ID_PREV);
        app.next = control(L"BUTTON", L"下一帧", BS_PUSHBUTTON, ID_NEXT);
        app.frame_edit = control(L"EDIT", L"1", WS_BORDER | ES_NUMBER | ES_AUTOHSCROLL, ID_FRAME);
        SendMessageW(app.frame_edit, EM_SETLIMITTEXT, 6, 0);
        app.jump = control(L"BUTTON", L"跳转", BS_PUSHBUTTON, ID_GOTO);
        app.play = control(L"BUTTON", L"播放", BS_PUSHBUTTON, ID_PLAY);
        app.zoom = control(L"COMBOBOX", L"", CBS_DROPDOWNLIST, ID_ZOOM);
        for (i = 0; i < 5; ++i) SendMessageW(app.zoom, CB_ADDSTRING, 0, (LPARAM)zooms[i]);
        SendMessageW(app.zoom, CB_SETCURSEL, 0, 0);
        app.search = control(L"EDIT", L"", WS_BORDER | ES_AUTOHSCROLL, ID_SEARCH);
        SendMessageW(app.search, EM_SETLIMITTEXT, 255, 0);
        app.list = control(L"LISTBOX", L"", WS_BORDER | WS_VSCROLL | WS_HSCROLL | LBS_NOTIFY | LBS_NOINTEGRALHEIGHT, ID_LIST);
        SendMessageW(app.list, LB_SETHORIZONTALEXTENT, 1600, 0);
        app.detail = control(L"EDIT", L"", WS_BORDER | WS_VSCROLL | ES_MULTILINE | ES_READONLY | ES_AUTOVSCROLL, ID_DETAIL);
        app.export_button = control(L"BUTTON", L"保存图", BS_PUSHBUTTON, ID_EXPORT);
        SetTimer(window, 1, 100, NULL);
        return 0;
    }
    if (message == WM_SIZE) {
        layout();
        return 0;
    }
    if (message == WM_GETMINMAXINFO) {
        MINMAXINFO *limits = (MINMAXINFO *)lparam;
        limits->ptMinTrackSize = (POINT){1050, 680};
        return 0;
    }
    if (message == WM_COMMAND && !app.busy) {
        int id = LOWORD(wparam), event = HIWORD(wparam);
        if (id == ID_PROFILE && event == CBN_SELCHANGE) load_profile((int)SendMessageW(app.profile, CB_GETCURSEL, 0, 0));
        else if (id == ID_LOAD) load_image();
        else if ((id == ID_RESOURCE || id == ID_PALETTE) && event == CBN_SELENDOK) PostMessageW(window, WM_COMMAND, ID_LOAD, 0);
        else if (id == ID_PREV) set_frame(app.frame ? app.frame - 1 : app.shp.count ? app.shp.count - 1u : 0u);
        else if (id == ID_NEXT) set_frame(app.frame + 1);
        else if (id == ID_GOTO) {
            wchar_t text[16];
            unsigned long value;
            GetWindowTextW(app.frame_edit, text, 16);
            value = wcstoul(text, NULL, 10);
            if (value && value <= app.shp.count) set_frame(value - 1);
            else set_frame(app.frame);
        } else if (id == ID_PLAY && app.shp.count) {
            app.playing = !app.playing;
            SetWindowTextW(app.play, app.playing ? L"暂停" : L"播放");
        } else if (id == ID_ZOOM && event == CBN_SELCHANGE) {
            static const int zooms[] = {0, 1, 2, 4, 8};
            LRESULT selected = SendMessageW(app.zoom, CB_GETCURSEL, 0, 0);
            if (selected >= 0 && selected < 5) app.zoom_value = zooms[selected];
            InvalidateRect(window, &app.canvas, FALSE);
        } else if (id == ID_SEARCH && event == EN_CHANGE) filter_text();
        else if (id == ID_LIST && event == LBN_SELCHANGE) show_text();
        else if (id == ID_EXPORT) export_snapshot();
        return 0;
    }
    if (message == WM_TIMER && app.playing) set_frame(app.frame + 1);
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
    wchar_t *folder = wide_text(directory), path[32768], details[2048];
    uint8_t before[20], after[20];
    unsigned checks = 0, failures = 0;
    int profile;
#define VERIFY(expr) do { ++checks; if (!(expr)) { ++failures; fprintf(stderr, "VIEWER FAIL: %s\n", #expr); } } while (0)
    if (!folder) return 1;
    for (profile = 0; profile < 2; ++profile) {
        ra_view pixels;
        SendMessageW(app.profile, CB_SETCURSEL, (WPARAM)profile, 0);
        SendMessageW(app.window, WM_COMMAND, MAKEWPARAM(ID_PROFILE, CBN_SELCHANGE), (LPARAM)app.profile);
        VERIFY(app.current == profile && app.profiles[profile].loaded && app.shp.count > 2);
        VERIFY(app.shp.count == (profile ? 696 : 744));
        VERIFY(app.profiles[profile].csf.label_count == (profile ? 4513u : 4479u));
        VERIFY(SendMessageW(app.list, LB_GETCOUNT, 0, 0) > 0);
        GetWindowTextW(app.detail, details, 2048);
        VERIFY(wcsstr(details, profile ? L"解放" : L"大兵") != NULL);
        pixels = (ra_view){app.pixels, (size_t)app.shp.width * app.shp.height};
        if (!pixels.data) continue;
        ra_sha1(pixels, before);
        SendMessageW(app.next, BM_CLICK, 0, 0);
        ra_sha1(pixels, after);
        VERIFY(app.frame == 1 && memcmp(before, after, 20));
        SendMessageW(app.previous, BM_CLICK, 0, 0);
        VERIFY(app.frame == 0);
        SetWindowTextW(app.frame_edit, L"3");
        SendMessageW(app.jump, BM_CLICK, 0, 0);
        VERIFY(app.frame == 2);
        SendMessageW(app.play, BM_CLICK, 0, 0);
        SendMessageW(app.window, WM_TIMER, 1, 0);
        VERIFY(app.playing && app.frame == 3);
        SendMessageW(app.play, BM_CLICK, 0, 0);
        VERIFY(!app.playing);
        {
            MSG pending;
            while (PeekMessageW(&pending, NULL, 0, 0, PM_REMOVE)) {
                TranslateMessage(&pending);
                DispatchMessageW(&pending);
            }
        }
        swprintf(path, 32768, L"%ls/%ls.bmp", folder, profile ? L"china-viewer" : L"original-viewer");
        VERIFY(save_snapshot(path));
    }
    SetWindowTextW(app.resource, L"cameo.pal");
    SendMessageW(app.window, WM_COMMAND, ID_LOAD, 0);
    VERIFY(app.palette_only && !app.shp.count);
    swprintf(path, 32768, L"%ls/palette-viewer.bmp", folder);
    VERIFY(save_snapshot(path));
    SetWindowTextW(app.resource, L"missing-image.shp");
    SendMessageW(app.window, WM_COMMAND, ID_LOAD, 0);
    VERIFY(app.palette_only && wcsstr(app.status, L"读取失败"));
    SetWindowTextW(app.search, L"不存在的标签_ra2_test");
    VERIFY(SendMessageW(app.list, LB_GETCOUNT, 0, 0) == 0);
    printf("{\"checks\":%u,\"failures\":%u,\"profiles\":2,\"snapshots\":3}\n", checks, failures);
    free(folder);
    return failures ? 1 : 0;
#undef VERIFY
}

static int app_main(int argc, char **argv)
{
    WNDCLASSW type = {0};
    MSG message;
    HWND window;
    const char *test_directory = NULL;
    int i, result = 0;
    app.original = "H:/开发/运行版本/原版1.006";
    app.mod = "H:/开发/运行版本/中国开局验证";
    app.busy = true;
    for (i = 1; i < argc; ++i) {
        if (i + 1 < argc && !strcmp(argv[i], "--original")) app.original = argv[++i];
        else if (i + 1 < argc && !strcmp(argv[i], "--mod")) app.mod = argv[++i];
        else if (i + 1 < argc && !strcmp(argv[i], "--self-test")) test_directory = argv[++i];
        else {
            fputs("Usage: ra2viewer [--original directory] [--mod directory] [--self-test output-directory]\n", stderr);
            return 2;
        }
    }
    SetProcessDPIAware();
    type.lpfnWndProc = window_proc;
    type.hInstance = GetModuleHandleW(NULL);
    type.lpszClassName = L"RA2PureCResourceViewer";
    type.hCursor = LoadCursorW(NULL, IDC_ARROW);
    if (!RegisterClassW(&type)) return 1;
    window = CreateWindowExW(0, type.lpszClassName, L"红色警戒2 · 资源查看器", WS_OVERLAPPEDWINDOW | WS_CLIPCHILDREN,
        CW_USEDEFAULT, CW_USEDEFAULT, 1220, 820, NULL, NULL, type.hInstance, NULL);
    if (!window) return 1;
    layout();
    app.busy = false;
    if (test_directory) {
        /* 截图验收需要原生子控件完成真实绘制，短暂显示但不抢占输入焦点。 */
        ShowWindow(window, SW_SHOWNOACTIVATE);
        UpdateWindow(window);
        result = self_test(test_directory);
    }
    else {
        ShowWindow(window, SW_SHOW);
        UpdateWindow(window);
        load_profile(1);
        while (GetMessageW(&message, NULL, 0, 0) > 0) {
            if (!IsDialogMessageW(window, &message)) {
                TranslateMessage(&message);
                DispatchMessageW(&message);
            }
        }
    }
    if (IsWindow(window)) DestroyWindow(window);
    ra_shp_close(&app.shp);
    ra_resource_close(&app.image);
    free(app.pixels);
    for (i = 0; i < 2; ++i) {
        ra_csf_close(&app.profiles[i].csf);
        ra_resource_close(&app.profiles[i].text);
        ra_vfs_close(&app.profiles[i].vfs);
    }
    DeleteObject(app.font);
    DeleteObject(app.heading);
    return result;
}
