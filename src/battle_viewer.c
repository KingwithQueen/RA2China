#define _CRT_SECURE_NO_WARNINGS
#define UNICODE
#define _UNICODE
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <windowsx.h>
#include <commdlg.h>
#include <dwmapi.h>
#include "internal.h"
#include "battle_scene.h"
#include <stdlib.h>
#include <string.h>
#include <limits.h>

enum
{
    ID_MAP = 100,
    ID_PAUSE,
    ID_STEP,
    ID_RESET,
    ID_SAVE,
    ID_LOAD,
    ID_NAV,
    ID_HOME,
    ID_OPTIONS,
    ID_RESUME = 200,
    ID_ZOOM,
    ID_MENU_SAVE,
    ID_MENU_LOAD,
    ID_MENU_QUIT
};
static struct
{
    HWND window, combo, pause, menu_controls[5];
    ra_ini keyboard;
    HFONT font;
    battle_scene scene;
    uint32_t *pixels, *picked;
    float *heights;
    int width, height, pan_x, pan_y, drag_x, drag_y, old_x, old_y;
    double zoom;
    bool selected[RA_BATTLE_UNITS], paused, dragging, panning, navigation, loading, replay;
    bool groups[10][RA_BATTLE_UNITS], marks[4], type_mask[RA_BATTLE_TYPES], held[256], pointer_inside, right_moved, options, resume_after_menu, follow;
    int mark_x[4], mark_y[4], pointer_x, pointer_y, right_x, right_y, event_x[8], event_y[8];
    uint32_t modifiers, last_team, event_count, event_cursor;
    bool planning;
    uint32_t planning_key, plan_count[RA_BATTLE_UNITS], plan_loop[RA_BATTLE_UNITS], plan_cells[RA_BATTLE_UNITS][RA_BATTLE_WAYPOINTS];
    ULONGLONG last_team_time, last_type_time, last_event_time;
    uint64_t camera_phase;
    uint32_t replay_end;
    uint8_t expected[20];
    uint64_t phase;
    LARGE_INTEGER last, frequency;
    wchar_t status[512];
    const char *original;
    uint32_t place_type_plus_one, campaign_camera_serial;
    bool test_probe, reported_selection[RA_BATTLE_UNITS];
} app;

static bool snapshot(const char *path);
static void menu_set(bool value);
static void view_tick(uint64_t microseconds);
static void view_limit(void);
static void plan_clear(void);
static void plan_commit(void);
static bool friendly_selected(void);
static void center_at(int x, int y);
static bool ground_cell(int x, int y, uint32_t *result);
static void wide(const char *text, wchar_t *output, int count)
{
    if (!MultiByteToWideChar(CP_UTF8, MB_ERR_INVALID_CHARS, text, -1, output, count)) output[0] = 0;
}
static void message(const wchar_t *text)
{
    wcsncpy_s(app.status, 512, text, _TRUNCATE);
    InvalidateRect(app.window, NULL, FALSE);
}
static void error_message(const ra_error *e)
{
    wchar_t text[400], result[512];
    wide(e->message, text, 400);
    swprintf(result, 512, L"操作失败：%s", text);
    message(result);
}
static void home(void)
{
    int x, y;
    if (!app.scene.battle.count)
    {
        app.pan_x = app.width / 2 - (int)(app.scene.ground.width * app.zoom / 2);
        app.pan_y = app.height / 2 - (int)(app.scene.ground.height * app.zoom / 2);
        view_limit();
        return;
    }
    uint32_t focus = 0;
    for (uint32_t i = 0; i < app.scene.battle.count; ++i)
        if (app.scene.battle.units[i].health && !(app.scene.battle.units[i].traits & RA_UNIT_LIMBO) && app.scene.battle.units[i].team == 1 &&
            !app.scene.battle.types[app.scene.battle.units[i].type].structure)
        {
            focus = i;
            break;
        }
    battle_unit_pixel(&app.scene, &app.scene.battle.units[focus], &x, &y);
    app.pan_x = (app.width - (app.scene.battle.economy ? 260 : 0)) / 2 - (int)(x * app.zoom);
    app.pan_y = app.height / 2 - (int)(y * app.zoom);
    view_limit();
    InvalidateRect(app.window, NULL, FALSE);
}
static void clock_reset(void)
{
    app.phase = 0;
    QueryPerformanceCounter(&app.last);
}
static void paused(bool value)
{
    app.paused = value;
    SetWindowTextW(app.pause, value ? L"继续" : L"暂停");
    clock_reset();
}
static void map_load(size_t source)
{
    ra_error e = {0};
    app.loading = true;
    paused(true);
    app.replay = false;
    memset(app.reported_selection, 0, sizeof(app.reported_selection));
    plan_clear();
    memset(app.selected, 0, sizeof(app.selected));
    if (battle_scene_map(&app.scene, source, true, &e))
    {
        wchar_t text[512];
        app.selected[0] = true;
        app.zoom = 1.0;
        memset(app.groups, 0, sizeof(app.groups));
        memset(app.marks, 0, sizeof(app.marks));
        app.event_count = app.event_cursor = 0;
        app.follow = false;
        home();
        swprintf(text, 512, L"原版资源已加载；蓝方由玩家控制，红方受击还击。缺失地形 %zu，高桥格 %zu（分层通行）。左键地面移动，左键红方攻击，右键取消。",
                 app.scene.missing, app.scene.bridges);
        if (app.scene.scenario)
            swprintf(text, 512, L"原始场景：建筑 %zu、坦克 %zu；尚未启用战役脚本和其他单位行为。左键选择，选中坦克后左键敌方建筑攻击。",
                     app.scene.structure_count, app.scene.imported_units);
        message(text);
    }
    else error_message(&e);
    app.place_type_plus_one = 0;
    app.loading = false;
    clock_reset();
}
static void step(void)
{
    ra_battle *b = &app.scene.battle;
    if (!b->tiles) return;
    if (app.replay && b->tick == app.replay_end) return;
    ra_battle_step(b);
    if (b->campaign)
    {
        const ra_campaign_state *state = &b->campaign->state;
        if (state->camera_serial != app.campaign_camera_serial)
        {
            app.campaign_camera_serial = state->camera_serial;
            if (state->camera_waypoint < 1024 && b->campaign->waypoints[state->camera_waypoint] != UINT32_MAX)
            {
                uint32_t cell = b->campaign->waypoints[state->camera_waypoint];
                center_at(((int)(cell % b->width) - (int)(cell / b->width)) * 30 + app.scene.ground.origin_x + 30,
                          ((int)(cell % b->width) + (int)(cell / b->width) - b->tiles[cell].height) * 15 + app.scene.ground.origin_y + 15);
            }
        }
        if (state->outcome) paused(true);
    }
    ra_error refresh_error = {0};
    if (!battle_scene_refresh(&app.scene, &refresh_error))
    {
        paused(true);
        message(L"桥梁图像更新失败，请检查资源。 ");
    }
    for (uint32_t i = 0; i < RA_BATTLE_SHOTS; ++i)
    {
        const ra_battle_shot *shot = &b->shots[i];
        if (shot->active != 2 || shot->impact_tick != b->tick) continue;
        memmove(app.event_x + 1, app.event_x, 7 * sizeof(*app.event_x));
        memmove(app.event_y + 1, app.event_y, 7 * sizeof(*app.event_y));
        app.event_x[0] = (int)(((int64_t)shot->x - shot->y) * 30 / RA_BATTLE_CELL) + app.scene.ground.origin_x + 30;
        app.event_y[0] = (int)(((int64_t)shot->x + shot->y) * 15 / RA_BATTLE_CELL - (int64_t)shot->z * 15 / (104 * 256)) + app.scene.ground.origin_y + 15;
        if (app.event_count < 8) ++app.event_count;
        app.event_cursor = 0;
    }
    if (app.replay && b->tick == app.replay_end)
    {
        uint8_t digest[20];
        ra_battle_hash(b, digest);
        paused(true);
        message(memcmp(digest, app.expected, 20) ? L"回放结束：状态校验失败。" : L"回放结束：状态校验一致。");
    }
}
static void render(void)
{
    battle_scene *s = &app.scene;
    ra_battle *b = &s->battle;
    size_t count = (size_t)app.width * app.height;
    uint32_t order[RA_BATTLE_UNITS], i, j;
    int x, y;
    if (!app.pixels || !app.picked || !app.heights) return;
    memset(app.picked, 0, count * sizeof(*app.picked));
    for (y = 0; y < app.height; ++y)
        for (x = 0; x < app.width; ++x)
        {
            int wx = (int)((x - app.pan_x) / app.zoom), wy = (int)((y - app.pan_y) / app.zoom);
            uint32_t color = 0x101923;
            if (s->ground.pixels && wx >= 0 && wy >= 0 && wx < s->ground.width && wy < s->ground.height)
            {
                size_t at = (size_t)wy * s->ground.width + wx;
                color = s->ground.pixels[at];
                if (app.navigation && s->ground.picked[at] >= 0)
                {
                    const ra_map_cell *c = &s->map.cells[s->ground.picked[at]];
                    bool pass = ra_battle_passable(b, c->y * 512 + c->x);
                    color = ((color & 0xfefefe) >> 1) + (pass ? 0x004800 : 0x650000);
                }
            }
            app.pixels[(size_t)y * app.width + x] = color;
        }
    if (b->economy)
    {
        const ra_palette *palette = &s->ore_palette;
        for (size_t n = 0; n < s->map.cell_count; ++n)
        {
            const ra_map_cell *cell = &s->map.cells[n];
            uint8_t resource = b->economy->ore[cell->y * b->width + cell->x];
            if (!(resource & 63)) continue;
            uint32_t kind = (resource >> 6) - 1;
            const ra_shp *shape = &s->ore_shapes[kind];
            if (!s->ore_pixels[kind] || !shape->count) continue;
            uint32_t frame = (resource & 63) - 1;
            if (frame >= shape->count) frame = shape->count - 1;
            int cx = (int)((((int)cell->x - cell->y) * 30 + s->ground.origin_x + 30) * app.zoom) + app.pan_x;
            int cy = (int)((((int)cell->x + cell->y - cell->height) * 15 + s->ground.origin_y + 15) * app.zoom) + app.pan_y;
            int w = (int)(shape->width * app.zoom), h = (int)(shape->height * app.zoom);
            const uint8_t *pixels = s->ore_pixels[kind] + (size_t)frame * shape->width * shape->height;
            for (int row = 0; row < h; ++row)
                for (int col = 0; col < w; ++col)
                {
                    int px = cx - w / 2 + col, py = cy - h / 2 + row;
                    if (px < 0 || py < 0 || px >= app.width || py >= app.height) continue;
                    unsigned index = pixels[(size_t)(row * (int)shape->height / h) * shape->width + (size_t)(col * (int)shape->width / w)];
                    if (!index) continue;
                    ra_rgb color = palette->colors[index];
                    app.pixels[(size_t)py * app.width + px] = (uint32_t)color.r << 16 | (uint32_t)color.g << 8 | color.b;
                }
        }
    }
    for (i = 0; i < b->count; ++i) order[i] = i;
    for (i = 1; i < b->count; ++i)
    {
        uint32_t value = order[i];
        j = i;
        while (j && (int64_t)b->units[order[j - 1]].x + b->units[order[j - 1]].y > (int64_t)b->units[value].x + b->units[value].y)
        {
            order[j] = order[j - 1];
            --j;
        }
        order[j] = value;
    }
    for (unsigned layer = 0; layer < 2; ++layer)
    {
        if (layer && s->deck.pixels)
            for (y = 0; y < app.height; ++y)
                for (x = 0; x < app.width; ++x)
                {
                    int wx = (int)((x - app.pan_x) / app.zoom), wy = (int)((y - app.pan_y) / app.zoom);
                    if (wx < 0 || wy < 0 || wx >= s->deck.width || wy >= s->deck.height) continue;
                    size_t at = (size_t)wy * s->deck.width + wx, target = (size_t)y * app.width + x;
                    uint32_t color = s->deck.pixels[at];
                    if (color >> 24)
                    {
                        /* 接岸后仍按每个模型像素的真实高度遮挡，不能把整辆地面单位盖在桥图下面。 */
                        if (app.picked[target] && app.heights[target] >= s->deck_heights[at] - 0.0001f) continue;
                        app.pixels[target] = color & 0xffffff;
                        app.picked[target] = 0;
                    }
                }
        for (j = 0; j < b->count; ++j)
        {
            const ra_battle_unit *u;
            const ra_voxel_image *sprite;
            int cx, cy, left, top, width, height;
            i = order[j];
            u = &b->units[i];
            ra_error error = {0};
            if (!u->health || (u->traits & RA_UNIT_LIMBO) || (ra_battle_unit_layer(b, u) != layer)) continue;
            bool structure = b->types[u->type].structure;
            sprite = structure ? battle_scene_structure_sprite(s, u, &error) : battle_scene_sprite(s, u, &error);
            if (!sprite)
            {
                if (structure)
                {
                    battle_unit_pixel(s, u, &cx, &cy);
                    cx = (int)(cx * app.zoom) + app.pan_x;
                    cy = (int)(cy * app.zoom) + app.pan_y;
                    for (int d = -8; d <= 8; ++d)
                        for (int side = -1; side <= 1; side += 2)
                        {
                            int px = cx + d, py = cy + side * d;
                            if (px >= 0 && py >= 0 && px < app.width && py < app.height)
                            {
                                app.pixels[(size_t)py * app.width + px] = 0xff00ff;
                                app.picked[(size_t)py * app.width + px] = u->id;
                                app.heights[(size_t)py * app.width + px] = (float)ra_battle_unit_height(b, u) / 104;
                            }
                        }
                }
                continue;
            }
            int32_t unit_height = ra_battle_unit_height(b, u);
            battle_unit_pixel(s, u, &cx, &cy);
            cx = (int)(cx * app.zoom) + app.pan_x;
            cy = (int)(cy * app.zoom) + app.pan_y;
            width = (int)(sprite->width * app.zoom);
            height = (int)(sprite->height * app.zoom);
            left = cx - (int)(sprite->origin_x * app.zoom);
            top = cy - (int)(sprite->origin_y * app.zoom);
            if (app.selected[i])
                for (y = -10; y <= 10; ++y)
                    for (x = -29; x <= 29; ++x)
                    {
                        int v = x * x * 100 + y * y * 841, px = cx + (int)(x * app.zoom), py = cy + (int)(y * app.zoom);
                        if (v > 65000 && v < 84000 && px >= 0 && py >= 0 && px < app.width && py < app.height)
                            app.pixels[(size_t)py * app.width + px] = 0x62ff87;
                    }
            for (y = 0; y < height; ++y)
                for (x = 0; x < width; ++x)
                {
                    int px = left + x, py = top + y;
                    uint32_t color;
                    if (px < 0 || py < 0 || px >= app.width || py >= app.height) continue;
                    size_t source = (size_t)(y * (int)sprite->height / height) * sprite->width + (size_t)(x * (int)sprite->width / width);
                    color = sprite->pixels[source];
                    if (color >> 24)
                    {
                        if (u->flash_until > b->tick && (b->tick / 4) % 2) color = 0xffffffffu;
                        app.pixels[(size_t)py * app.width + px] = color & 0xffffff;
                        app.picked[(size_t)py * app.width + px] = u->id;
                        app.heights[(size_t)py * app.width + px] =
                            (structure || b->types[u->type].infantry)
                                ? (float)unit_height / 104 + (sprite->origin_y - (float)(source / sprite->width)) / 17.320508f
                                : battle_sprite_height(sprite, source, unit_height);
                    }
                }
            int bar_width = (int)(36 * app.zoom), bar_top = top + (int)(sprite->min_y * app.zoom) - 7;
            for (y = 0; y < 4; ++y)
                for (x = 0; x < bar_width; ++x)
                {
                    int px = cx - bar_width / 2 + x, py = bar_top + y;
                    if (px < 0 || py < 0 || px >= app.width || py >= app.height) continue;
                    bool filled = (uint64_t)(uint32_t)x * s->battle.types[u->type].strength < (uint64_t)u->health * (uint32_t)bar_width;
                    app.pixels[(size_t)py * app.width + px] = filled ? (u->team == 1 ? 0x60ed91 : 0xf06b58) : 0x17212a;
                }
            if (b->economy && b->economy->types[u->type].harvester)
            {
                const ra_econ_miner *miner = &b->economy->state.miners[i];
                uint32_t cargo = miner->ore + miner->gems, capacity = b->economy->types[u->type].storage;
                for (int col = 0; col < bar_width; ++col)
                {
                    int px = cx - bar_width / 2 + col, py = bar_top + 5;
                    if (px >= 0 && py >= 0 && px < app.width && py < app.height)
                        app.pixels[(size_t)py * app.width + px] =
                            (uint64_t)(uint32_t)col * capacity < (uint64_t)cargo * (uint32_t)bar_width ? 0xeec857 : 0x17212a;
                }
            }
        }
    }
    for (i = 0; i < RA_BATTLE_SHOTS; ++i)
    {
        const ra_battle_shot *shot = &b->shots[i];
        if (shot->active != 1 && shot->active != 2) continue;
        int wx = (int)(((int64_t)shot->x - shot->y) * 30 / RA_BATTLE_CELL) + s->ground.origin_x + 30;
        int wy = (int)(((int64_t)shot->x + shot->y) * 15 / RA_BATTLE_CELL - (int64_t)shot->z * 15 / (104 * 256)) + s->ground.origin_y + 15;
        int cx = (int)(wx * app.zoom) + app.pan_x, cy = (int)(wy * app.zoom) + app.pan_y;
        if (shot->active == 1 && b->types[shot->type].weapon.missile)
        {
            ra_error error = {0};
            const ra_voxel_image *sprite = battle_scene_missile_sprite(s, shot, &error);
            if (sprite)
            {
                int width = (int)(sprite->width * app.zoom), height = (int)(sprite->height * app.zoom);
                for (int py = 0; py < height; ++py)
                    for (int px = 0; px < width; ++px)
                    {
                        int dx = cx + px - (int)(sprite->origin_x * app.zoom), dy = cy + py - (int)(sprite->origin_y * app.zoom);
                        if (dx < 0 || dy < 0 || dx >= app.width || dy >= app.height) continue;
                        uint32_t color = sprite->pixels[(size_t)(py * sprite->height / height) * sprite->width + px * sprite->width / width];
                        if (color >> 24) app.pixels[(size_t)dy * app.width + dx] = color & 0xffffff;
                    }
                continue;
            }
        }
        if (shot->active == 1)
        {
            for (y = -2; y <= 2; ++y)
                for (x = -3; x <= 3; ++x)
                    if (cx + x >= 0 && cy + y >= 0 && cx + x < app.width && cy + y < app.height) app.pixels[(size_t)(cy + y) * app.width + cx + x] = 0xffe8a2;
        }
        else if (s->impact_pixels)
        {
            size_t frame = (size_t)(b->tick - shot->impact_tick) * s->impact.count / 13;
            if (frame >= s->impact.count) frame = s->impact.count - 1;
            int width = (int)(s->impact.width * app.zoom), height = (int)(s->impact.height * app.zoom);
            const uint8_t *pixels = s->impact_pixels + frame * s->impact.width * s->impact.height;
            for (y = 0; y < height; ++y)
                for (x = 0; x < width; ++x)
                {
                    int px = cx - width / 2 + x, py = cy - height / 2 + y;
                    if (px < 0 || py < 0 || px >= app.width || py >= app.height) continue;
                    unsigned index = pixels[(size_t)(y * (int)s->impact.height / height) * s->impact.width + (size_t)(x * (int)s->impact.width / width)];
                    if (!index) continue;
                    ra_rgb color = s->impact_palette.colors[index];
                    app.pixels[(size_t)py * app.width + px] = ((uint32_t)color.r << 16) | ((uint32_t)color.g << 8) | color.b;
                }
        }
    }
}
static void cell_point(uint32_t cell, int *x, int *y)
{
    const battle_scene *s = &app.scene;
    *x = (int)((((int)(cell % 512) - (int)ra_battle_cell_y(&app.scene.battle, cell)) * 30 + s->ground.origin_x + 30) * app.zoom) + app.pan_x;
    *y =
        (int)((((int)(cell % 512) + (int)ra_battle_cell_y(&app.scene.battle, cell) - s->battle.tiles[cell].height) * 15 + s->ground.origin_y + 15) * app.zoom) +
        app.pan_y + 58;
}
static void draw_waypoints(HDC dc)
{
    int saved = SaveDC(dc);
    IntersectClipRect(dc, 0, 58, app.width, app.height + 58);
    SetBkMode(dc, TRANSPARENT);
    SelectObject(dc, app.font);
    for (uint32_t i = 0; i < app.scene.battle.count; ++i)
    {
        const ra_battle_unit *u = &app.scene.battle.units[i];
        uint32_t count = app.plan_count[i], cursor = 0, loop = app.plan_loop[i];
        const uint32_t *cells = app.plan_cells[i];
        if (!u->health || (u->traits & RA_UNIT_LIMBO)) continue;
        if (!count && app.selected[i] && u->waypoint_count)
        {
            count = u->waypoint_count;
            cursor = u->waypoint_cursor;
            cells = u->waypoints;
            loop = u->waypoint_loop;
        }
        if (!count) continue;
        COLORREF color = app.plan_count[i] ? RGB(90, 240, 255) : RGB(245, 216, 100);
        HPEN pen = CreatePen(PS_SOLID, 2, color);
        HGDIOBJ old = SelectObject(dc, pen), brush = SelectObject(dc, GetStockObject(HOLLOW_BRUSH));
        int x, y;
        battle_unit_pixel(&app.scene, u, &x, &y);
        MoveToEx(dc, (int)(x * app.zoom) + app.pan_x, (int)(y * app.zoom) + app.pan_y + 58, NULL);
        SetTextColor(dc, color);
        for (uint32_t j = cursor; j < count; ++j)
        {
            wchar_t number[16];
            cell_point(cells[j], &x, &y);
            LineTo(dc, x, y);
            Ellipse(dc, x - 6, y - 6, x + 7, y + 7);
            swprintf(number, 16, L"%u", j + 1);
            TextOutW(dc, x + 8, y - 12, number, (int)wcslen(number));
        }
        if (loop)
        {
            cell_point(cells[loop - 1], &x, &y);
            LineTo(dc, x, y);
        }
        SelectObject(dc, brush);
        SelectObject(dc, old);
        DeleteObject(pen);
    }
    RestoreDC(dc, saved);
}
static uint32_t economy_row(uint32_t row)
{
    const ra_battle *b = &app.scene.battle;
    if (!b->economy) return UINT32_MAX;
    for (uint32_t i = 0; i < b->type_count; ++i)
    {
        const ra_econ_type *t = &b->economy->types[i];
        if (!t->enabled) continue;
        if (b->types[i].structure && b->types[i].id[0] != (app.scene.economy_allied ? 'G' : 'N')) continue;
        if (!b->types[i].structure && !ra_economy_owner_allowed(b, 1, i)) continue;
        if (!row--) return i;
    }
    return UINT32_MAX;
}
static bool economy_click(int x, int y, bool right)
{
    ra_battle *b = &app.scene.battle;
    if (!b->economy || x < app.width - 260 || y < 58 || y >= app.height + 58) return false;
    if (app.replay || app.options || y < 58 + 118) return true;
    uint32_t type = economy_row((uint32_t)(y - 58 - 118) / 48);
    if (type == UINT32_MAX) return true;
    uint32_t category = ra_economy_category(b, type);
    ra_econ_queue *q = &b->economy->state.houses[0].queues[category];
    ra_error error = {0};
    if (right)
    {
        if (q->count && q->types[0] == type && !ra_economy_command(b, b->tick + 1, 1, q->paused ? RA_ECON_CANCEL : RA_ECON_PAUSE, category, &error))
            error_message(&error);
    }
    else if (q->count && q->types[0] == type && q->paused)
    {
        if (!ra_economy_command(b, b->tick + 1, 1, RA_ECON_PAUSE, category, &error)) error_message(&error);
    }
    else if (!category && q->count && q->types[0] == type && q->progress == b->economy->types[type].ticks * 1000)
    {
        app.place_type_plus_one = type + 1;
        message(L"建筑就绪：左键可用地面放置，右键取消放置。矿区、坡面、桥梁和占地不能放置。 ");
    }
    else if (!ra_economy_available(b, 1, type)) message(L"科技条件尚未满足：检查建造厂、前置建筑和科技等级。 ");
    else if (!ra_economy_command(b, b->tick + 1, 1, RA_ECON_QUEUE, type, &error)) error_message(&error);
    InvalidateRect(app.window, NULL, FALSE);
    return true;
}
static void economy_panel(HDC dc)
{
    ra_battle *b = &app.scene.battle;
    if (!b->economy) return;
    RECT panel = {app.width - 260, 58, app.width, app.height + 58};
    HBRUSH brush = CreateSolidBrush(RGB(23, 32, 39));
    FillRect(dc, &panel, brush);
    DeleteObject(brush);
    SelectObject(dc, app.font);
    SetBkMode(dc, TRANSPARENT);
    SetTextColor(dc, RGB(235, 235, 225));
    wchar_t line[256], title[96];
    const ra_econ_house *house = &b->economy->state.houses[0];
    uint32_t output, drain;
    ra_battle_power(b, 1, &output, &drain);
    swprintf(line, 256, L"资金 %llu    科技 %u", (unsigned long long)house->credits, house->tech);
    TextOutW(dc, panel.left + 12, 72, line, (int)wcslen(line));
    swprintf(line, 256, L"电力 %u / %u%s", output, drain, output < drain ? L"  低电力" : L"");
    TextOutW(dc, panel.left + 12, 98, line, (int)wcslen(line));
    TextOutW(dc, panel.left + 12, 125, L"左键生产 / 放置", 9);
    TextOutW(dc, panel.left + 12, 148, L"右键暂停，再次右键取消", 12);
    uint32_t rows = 0;
    for (; rows < 16; ++rows)
    {
        uint32_t type = economy_row(rows);
        if (type == UINT32_MAX) break;
        const ra_econ_type *definition = &b->economy->types[type];
        const ra_econ_queue *q = &house->queues[ra_economy_category(b, type)];
        const ra_ini_entry *entry = ra_ini_get(&app.scene.voxels.rules, b->types[type].id, "UIName");
        const ra_csf_label *label = entry ? ra_csf_get(&app.scene.voxels.text, entry->value) : NULL;
        wide(label && label->value_count ? app.scene.voxels.text.values[label->first_value].text : b->types[type].id, title, 96);
        bool active = q->count && q->types[0] == type;
        uint32_t percent = active ? (uint32_t)((uint64_t)q->progress * 100 / (definition->ticks * 1000)) : 0;
        SetTextColor(dc, ra_economy_available(b, 1, type) ? RGB(220, 235, 245) : RGB(130, 135, 140));
        swprintf(line, 256, L"%s  $%u", title, definition->cost);
        TextOutW(dc, panel.left + 12, 58 + 122 + (int)rows * 48, line, (int)wcslen(line));
        if (active) swprintf(line, 256, L"%u%%  队列 %u  %s", percent, q->count, q->paused ? L"暂停" : percent == 100 ? L"就绪" : L"建造中");
        if (!active) wcscpy_s(line, 256, ra_economy_available(b, 1, type) ? L"可生产" : L"前提未满足");
        TextOutW(dc, panel.left + 12, 58 + 144 + (int)rows * 48, line, (int)wcslen(line));
    }
    SetTextColor(dc, RGB(230, 230, 220));
    TextOutW(dc, panel.left + 12, 58 + 135 + (int)rows * 48, L"矿车：选中后左键矿区 / 矿厂", 16);
    if (app.place_type_plus_one && app.pointer_inside && app.pointer_x < app.width - 260)
    {
        uint32_t cell, type = app.place_type_plus_one - 1;
        if (ground_cell(app.pointer_x, app.pointer_y, &cell))
        {
            bool valid = ra_economy_placeable(b, 1, type, cell);
            HPEN pen = CreatePen(PS_SOLID, 2, valid ? RGB(80, 255, 100) : RGB(255, 80, 70));
            HGDIOBJ old = SelectObject(dc, pen);
            for (uint32_t row = 0; row < b->types[type].foundation_height; ++row)
                for (uint32_t col = 0; col < b->types[type].foundation_width; ++col)
                {
                    int x, y;
                    cell_point(cell + row * b->width + col, &x, &y);
                    MoveToEx(dc, x, y - (int)(15 * app.zoom), NULL);
                    LineTo(dc, x + (int)(30 * app.zoom), y);
                    LineTo(dc, x, y + (int)(15 * app.zoom));
                    LineTo(dc, x - (int)(30 * app.zoom), y);
                    LineTo(dc, x, y - (int)(15 * app.zoom));
                }
            SelectObject(dc, old);
            DeleteObject(pen);
        }
    }
}
static void paint(HDC dc)
{
    BITMAPINFO info = {0};
    RECT canvas = {0, 58, app.width, app.height + 58}, footer;
    uint8_t digest[20];
    char hex[41];
    wchar_t text[512];
    unsigned selected = 0;
    RECT toolbar = {0, 0, app.width, 58};
    FillRect(dc, &toolbar, (HBRUSH)(COLOR_BTNFACE + 1));
    render();
    info.bmiHeader.biSize = sizeof(BITMAPINFOHEADER);
    info.bmiHeader.biWidth = app.width;
    info.bmiHeader.biHeight = -app.height;
    info.bmiHeader.biPlanes = 1;
    info.bmiHeader.biBitCount = 32;
    info.bmiHeader.biCompression = BI_RGB;
    if (app.pixels) StretchDIBits(dc, 0, 58, app.width, app.height, 0, 0, app.width, app.height, app.pixels, &info, DIB_RGB_COLORS, SRCCOPY);
    else FillRect(dc, &canvas, (HBRUSH)GetStockObject(BLACK_BRUSH));
    draw_waypoints(dc);
    economy_panel(dc);
    GetClientRect(app.window, &footer);
    footer.top = app.height + 58;
    FillRect(dc, &footer, (HBRUSH)GetStockObject(BLACK_BRUSH));
    SelectObject(dc, app.font);
    SetTextColor(dc, RGB(225, 234, 242));
    SetBkMode(dc, TRANSPARENT);
    for (unsigned i = 0; i < app.scene.battle.count; ++i)
        if (app.selected[i]) ++selected;
    if (app.scene.battle.tiles)
    {
        ra_battle_hash(&app.scene.battle, digest);
        ra_hex(digest, 20, hex);
        swprintf(text, 512, L"原版 1.006 战场  |  %s  |  固定 %u 步/秒  |  步 %u  |  已选 %u  |  命令 %u  |  发射 %u  |  摧毁 %u",
                 app.paused ? L"暂停" : L"运行", RA_BATTLE_HZ, app.scene.battle.tick, selected, app.scene.battle.command_count, app.scene.battle.fired,
                 app.scene.battle.kills);
        TextOutW(dc, 12, footer.top + 8, text, (int)wcslen(text));
        wide(hex, text, 512);
        TextOutW(dc, 12, footer.top + 31, L"状态 SHA-1：", 10);
        TextOutW(dc, 130, footer.top + 31, text, (int)wcslen(text));
        if (app.scene.structure_count)
        {
            uint32_t output, drain;
            size_t structures = 0;
            for (uint32_t i = 0; i < app.scene.battle.count; ++i)
                if (app.scene.battle.units[i].health && !(app.scene.battle.units[i].traits & RA_UNIT_LIMBO) &&
                    app.scene.battle.types[app.scene.battle.units[i].type].structure)
                    ++structures;
            ra_battle_power(&app.scene.battle, 1, &output, &drain);
            swprintf(text, 512, L"建筑 %zu  |  电力 %u / %u", structures, output, drain);
            TextOutW(dc, 560, footer.top + 31, text, (int)wcslen(text));
        }
    }
    if (app.scene.battle.campaign)
    {
        const ra_campaign_state *state = &app.scene.battle.campaign->state;
        const ra_csf_label *label = ra_csf_get(&app.scene.voxels.text, state->message);
        const char *message_text = label && label->value_count ? app.scene.voxels.text.values[label->first_value].text : state->message;
        wide(message_text, text, 512);
        if (state->outcome) swprintf(text, 512, state->outcome == 1 ? L"任务完成（任务逻辑仍在开发验证）" : L"任务失败");
        else if (!*text) swprintf(text, 512, L"原版任务运行中；部分海空演出、事件和动作尚未实现，详见本阶段报告。");
        TextOutW(dc, 12, footer.top + 54, text, (int)wcslen(text));
    }
    else TextOutW(dc, 12, footer.top + 54, app.status, (int)wcslen(app.status));
    {
        const wchar_t *hint = L"Ctrl 开火 · Ctrl+Shift 移动攻击 · G 警戒 · X 散开 · 按住 Z 路径 / 巡逻 · S 停止 · 右键取消 / 拖图 · Esc 选项";
        TextOutW(dc, 12, footer.top + 77, hint, (int)wcslen(hint));
    }
    if (app.options)
    {
        RECT panel = {app.width / 2 - 240, app.height / 2 - 120, app.width / 2 + 240, app.height / 2 + 180};
        FillRect(dc, &panel, (HBRUSH)GetStockObject(BLACK_BRUSH));
        TextOutW(dc, panel.left + 24, panel.top + 16, L"选项", 2);
        TextOutW(dc, panel.left + 24, panel.top + 94, L"预览比例", 4);
    }
    if (app.dragging)
    {
        HPEN pen = CreatePen(PS_DOT, 1, RGB(110, 255, 160));
        HGDIOBJ old = SelectObject(dc, pen), brush = SelectObject(dc, GetStockObject(HOLLOW_BRUSH));
        Rectangle(dc, app.drag_x, app.drag_y + 58, app.old_x, app.old_y + 58);
        SelectObject(dc, brush);
        SelectObject(dc, old);
        DeleteObject(pen);
    }
}
static void layout(void)
{
    RECT r;
    size_t count;
    GetClientRect(app.window, &r);
    app.width = r.right > 1 ? r.right : 1;
    app.height = r.bottom > 160 ? r.bottom - 160 : 1;
    count = (size_t)app.width * app.height;
    free(app.pixels);
    free(app.picked);
    free(app.heights);
    app.pixels = calloc(count, sizeof(uint32_t));
    app.picked = calloc(count, sizeof(uint32_t));
    app.heights = calloc(count, sizeof(float));
}
static bool replay_save(const char *path)
{
    uint8_t *bytes = NULL;
    size_t size = 0;
    ra_error e = {0};
    bool ok = ra_battle_replay_write(&app.scene.battle, &bytes, &size, &e) && battle_file_write(path, bytes, size, &e);
    free(bytes);
    if (ok) message(L"回放已保存，包含原始命令和最终状态校验。");
    else error_message(&e);
    return ok;
}
static bool replay_load(const char *path)
{
    ra_file file = {0};
    ra_error e = {0};
    bool ok;
    paused(true);
    ok = ra_file_open(&file, path, &e) && ra_battle_replay_read(&app.scene.battle, file.view, &app.replay_end, app.expected, &e);
    ra_file_close(&file);
    if (ok)
    {
        plan_clear();
        app.replay = true;
        app.event_count = app.event_cursor = 0;
        if (app.replay_end)
        {
            paused(false);
            message(L"正在重放命令；结束后自动比较状态摘要。");
        }
        else
        {
            uint8_t digest[20];
            ra_battle_hash(&app.scene.battle, digest);
            message(memcmp(digest, app.expected, 20) ? L"回放结束：状态校验失败。" : L"回放结束：状态校验一致。");
        }
    }
    else error_message(&e);
    return ok;
}
static void file_dialog(bool save)
{
    OPENFILENAMEW dialog = {0};
    wchar_t path[32768] = L"战场回放.rpl";
    char utf8[65536];
    dialog.lStructSize = sizeof(dialog);
    dialog.hwndOwner = app.window;
    dialog.lpstrFile = path;
    dialog.nMaxFile = 32768;
    dialog.lpstrFilter = L"战场命令回放 (*.rpl)\0*.rpl\0\0";
    dialog.lpstrDefExt = L"rpl";
    dialog.Flags = OFN_EXPLORER | OFN_NOCHANGEDIR | (save ? OFN_OVERWRITEPROMPT : OFN_FILEMUSTEXIST);
    paused(true);
    if (!(save ? GetSaveFileNameW(&dialog) : GetOpenFileNameW(&dialog))) return;
    if (!WideCharToMultiByte(CP_UTF8, WC_ERR_INVALID_CHARS, path, -1, utf8, sizeof(utf8), NULL, NULL))
    {
        message(L"路径过长或无效。");
        return;
    }
    if (save) replay_save(utf8);
    else replay_load(utf8);
}
static void plan_clear(void)
{
    app.planning = false;
    memset(app.plan_count, 0, sizeof(app.plan_count));
    memset(app.plan_loop, 0, sizeof(app.plan_loop));
}
static void selected_order(ra_battle_order kind, uint32_t target)
{
    ra_battle *b = &app.scene.battle;
    ra_error e = {0};
    unsigned count = 0;
    if (app.replay)
    {
        message(L"回放期间不接受新命令；重新开始可恢复操作。");
        return;
    }
    for (uint32_t i = 0; i < b->count; ++i)
    {
        if (!app.selected[i] || !b->units[i].health || (b->units[i].traits & RA_UNIT_LIMBO) || b->units[i].team != 1 || b->types[b->units[i].type].structure)
            continue;
        if (ra_battle_order_add(b, b->tick + 1, i + 1, kind, target, &e))
        {
            app.plan_count[i] = app.plan_loop[i] = 0;
            ++count;
        }
    }
    message(!count                     ? L"请先选择仍存活的蓝方单位。"
            : kind == RA_ORDER_DEPLOY  ? L"展开命令已提交；附近占地需平坦且无阻挡。"
            : kind == RA_ORDER_ATTACK  ? L"攻击命令已排入下一模拟步；进入射程并完成炮塔转向后开火。"
            : kind == RA_ORDER_STOP    ? L"停止命令已排入下一模拟步；完成当前路段后停靠，原任务与路径点清除。"
            : kind == RA_ORDER_GUARD   ? L"警戒命令已排入下一模拟步；接近来敌并交战，随后返回警戒位置。"
            : kind == RA_ORDER_SCATTER ? L"散开命令已排入下一模拟步；各单位选择附近可通行空格。"
                                       : L"强制开火命令已排入下一模拟步；允许攻击地面及友军，注意波及。 ");
}
static bool ground_cell(int x, int y, uint32_t *result)
{
    battle_scene *s = &app.scene;
    int wx = (int)((x - app.pan_x) / app.zoom), wy = (int)((y - app.pan_y) / app.zoom), index;
    if (!s->ground.pixels || wx < 0 || wy < 0 || wx >= s->ground.width || wy >= s->ground.height) return false;
    if (s->deck.picked && s->deck.picked[(size_t)wy * s->deck.width + wx] >= 0)
    {
        *result = (uint32_t)s->deck.picked[(size_t)wy * s->deck.width + wx];
        return true;
    }
    index = s->ground.picked[(size_t)wy * s->ground.width + wx];
    if (index < 0) return false;
    *result = s->map.cells[index].y * 512 + s->map.cells[index].x;
    return true;
}
static void plan_commit(void)
{
    ra_battle *b = &app.scene.battle;
    ra_error e = {0};
    uint32_t before = b->command_count, count = 0;
    bool ok = !app.replay;
    for (uint32_t i = 0; ok && i < b->count; ++i)
    {
        if (!app.plan_count[i] || !b->units[i].health) continue;
        ok = ra_battle_waypoints_add(b, b->tick + 1, i + 1, app.plan_cells[i], app.plan_count[i], app.plan_loop[i] ? app.plan_loop[i] - 1 : UINT32_MAX, &e);
        ++count;
    }
    /* 当前线程尚未推进模拟；容量不足时回退整个规划提交，避免只启动一部分编队。 */
    if (!ok) b->command_count = before;
    plan_clear();
    if (!ok) error_message(&e);
    else message(count ? L"路径规划已统一提交；单位从下一模拟步依次执行，闭合路线持续巡逻。" : L"已退出路径规划。");
}
static void move_to(int x, int y, ra_battle_order kind)
{
    ra_battle *b = &app.scene.battle;
    uint32_t cell, used[RA_BATTLE_UNITS], targets[RA_BATTLE_UNITS], count = 0;
    ra_error e = {0};
    if (app.replay)
    {
        message(L"回放期间不接受移动命令；重新开始可恢复操作。");
        return;
    }
    if (!ground_cell(x, y, &cell)) return;
    bool selected_amphibious = false;
    for (uint32_t i = 0; i < b->count; ++i)
        if (app.selected[i] && b->types[b->units[i].type].amphibious) selected_amphibious = true;
    if (!ra_battle_passable(b, cell) && !(selected_amphibious && cell < b->width * b->height && !b->tiles[cell].blocked && b->tiles[cell].land == 2))
    {
        message(L"目标不可通行：水面、悬崖、障碍、损坏或未确认桥段、地图边界。");
        return;
    }
    for (uint32_t i = 0; i < b->count; ++i) targets[i] = UINT32_MAX;
    for (uint32_t i = 0; i < b->count; ++i)
    {
        if (!app.selected[i] || !b->units[i].health || (b->units[i].traits & RA_UNIT_LIMBO) || b->units[i].team != 1) continue;
        if (app.planning && kind == RA_ORDER_MOVE)
        {
            /* 点击已有节点闭合路线；节点索引随单位分别保存。 */
            for (uint32_t j = 0; j < app.plan_count[i]; ++j)
                if (app.plan_cells[i][j] == cell)
                {
                    for (uint32_t k = 0; k < b->count; ++k)
                        if (app.selected[k] && app.plan_count[k] > j) app.plan_loop[k] = j + 1;
                    message(L"路线已闭合；松开 Z 后开始巡逻。 ");
                    return;
                }
            if (app.plan_count[i] == RA_BATTLE_WAYPOINTS)
            {
                message(L"每单位最多 32 个路径点；先松开 Z 执行，或按 S 清除所选单位的规划。 ");
                return;
            }
        }
        for (int r = 0; r < 9 && targets[i] == UINT32_MAX; ++r)
            for (int dy = -r; dy <= r && targets[i] == UINT32_MAX; ++dy)
                for (int dx = -r; dx <= r; ++dx)
                {
                    int tx = (int)(cell % 512) + dx, ty = (int)ra_battle_cell_y(&app.scene.battle, cell) + dy;
                    bool duplicate = false;
                    if (abs(dx) != r && abs(dy) != r) continue;
                    if (tx < 0 || ty < 0 || tx >= 512 || ty >= 512) continue;
                    uint32_t candidate = (uint32_t)ty * 512 + (uint32_t)tx + cell / (512 * 512) * (512 * 512);
                    for (uint32_t j = 0; j < count; ++j)
                        if (used[j] == candidate) duplicate = true;
                    if (!duplicate &&
                        (ra_battle_passable(b, candidate) || (b->types[b->units[i].type].amphibious && candidate < b->width * b->height &&
                                                              !b->tiles[candidate].blocked && b->tiles[candidate].land == 2)) &&
                        (!b->occupied[candidate] || b->occupied[candidate] == i + 1))
                    {
                        targets[i] = candidate;
                        used[count++] = candidate;
                        break;
                    }
                }
    }
    count = 0;
    for (uint32_t i = 0; i < b->count; ++i)
    {
        if (targets[i] == UINT32_MAX) continue;
        if (app.planning && kind == RA_ORDER_MOVE)
        {
            app.plan_cells[i][app.plan_count[i]++] = targets[i];
            app.plan_loop[i] = 0;
            ++count;
        }
        else if (ra_battle_order_add(b, b->tick + 1, i + 1, kind, targets[i], &e))
        {
            app.plan_count[i] = app.plan_loop[i] = 0;
            ++count;
        }
    }
    message(!count                                  ? L"没有可移动的选中单位或目标周围没有空格。"
            : app.planning && kind == RA_ORDER_MOVE ? L"路径点已添加；继续左键添加，右键可换选另一编队，松开 Z 统一执行。"
            : kind == RA_ORDER_ATTACK_MOVE          ? L"移动攻击已排入下一模拟步；遇敌交战，结束后继续前往目的地。"
                                                    : L"移动命令已排入下一模拟步；自动绕开静态障碍和其他单位。");
}

/* 所有键位从原版包内 keyboard.ini 解析，界面状态不参与游戏模拟或回放。 */
static bool hotkey(const char *command, uint32_t code)
{
    int64_t value = -1;
    return ra_ini_integer(ra_ini_get(&app.keyboard, "Hotkey", command), &value, NULL) && value == code;
}
static bool friendly_selected(void)
{
    for (uint32_t i = 0; i < app.scene.battle.count; ++i)
        if (app.selected[i] && app.scene.battle.units[i].health && !(app.scene.battle.units[i].traits & RA_UNIT_LIMBO) && app.scene.battle.units[i].team == 1 &&
            !app.scene.battle.types[app.scene.battle.units[i].type].structure)
            return true;
    return false;
}
static void view_limit(void)
{
    if (!app.scene.ground.pixels) return;
    int width = (int)(app.scene.ground.width * app.zoom), height = (int)(app.scene.ground.height * app.zoom);
    int viewport = app.width - (app.scene.battle.economy ? 260 : 0);
    if (width <= viewport) app.pan_x = (viewport - width) / 2;
    else app.pan_x = max(viewport - width, min(0, app.pan_x));
    if (height <= app.height) app.pan_y = (app.height - height) / 2;
    else app.pan_y = max(app.height - height, min(0, app.pan_y));
}
static void center_at(int x, int y)
{
    app.pan_x = (app.width - (app.scene.battle.economy ? 260 : 0)) / 2 - (int)(x * app.zoom);
    app.pan_y = app.height / 2 - (int)(y * app.zoom);
    view_limit();
    InvalidateRect(app.window, NULL, FALSE);
}
static void center_selection(void)
{
    int64_t sx = 0, sy = 0;
    uint32_t count = 0;
    for (uint32_t i = 0; i < app.scene.battle.count; ++i)
        if (app.selected[i] && app.scene.battle.units[i].health)
        {
            int x, y;
            battle_unit_pixel(&app.scene, &app.scene.battle.units[i], &x, &y);
            sx += x;
            sy += y;
            ++count;
        }
    if (count) center_at((int)(sx / count), (int)(sy / count));
}
static bool visible_unit(uint32_t i)
{
    int x, y;
    battle_unit_pixel(&app.scene, &app.scene.battle.units[i], &x, &y);
    x = (int)(x * app.zoom) + app.pan_x;
    y = (int)(y * app.zoom) + app.pan_y;
    return x >= 0 && y >= 0 && x < app.width && y < app.height;
}
static void base_home(void)
{
    ra_battle *b = &app.scene.battle;
    int min_x = INT_MAX, min_y = INT_MAX, max_x = INT_MIN, max_y = INT_MIN;
    for (uint32_t i = 0; i < b->count; ++i)
    {
        ra_error error = {0};
        const ra_battle_unit *unit = &b->units[i];
        const ra_voxel_image *image =
            b->types[unit->type].structure ? battle_scene_structure_sprite(&app.scene, unit, &error) : battle_scene_sprite(&app.scene, unit, &error);
        if (!image) continue;
        int x, y;
        battle_unit_pixel(&app.scene, unit, &x, &y);
        int left = x - (int)image->origin_x, top = y - (int)image->origin_y;
        if (left + image->min_x < min_x) min_x = left + image->min_x;
        if (top + image->min_y - 12 < min_y) min_y = top + image->min_y - 12;
        if (left + image->max_x > max_x) max_x = left + image->max_x;
        if (top + image->max_y > max_y) max_y = top + image->max_y;
    }
    if (min_x == INT_MAX) return;
    int viewport = app.width - (b->economy ? 260 : 0);
    double zoom_x = (double)(viewport - 96) / (max_x - min_x + 1), zoom_y = (double)(app.height - 96) / (max_y - min_y + 1);
    app.zoom = zoom_x < zoom_y ? zoom_x : zoom_y;
    if (app.zoom > 1.25) app.zoom = 1.25;
    if (app.zoom < 0.25) app.zoom = 0.25;
    app.pan_x = viewport / 2 - (int)((min_x + max_x) * app.zoom / 2);
    app.pan_y = app.height / 2 - (int)((min_y + max_y) * app.zoom / 2);
    view_limit();
}
static void type_select(bool all)
{
    bool types[RA_BATTLE_TYPES] = {false};
    for (uint32_t i = 0; i < app.scene.battle.count; ++i)
        if (app.selected[i] && app.scene.battle.units[i].health && !(app.scene.battle.units[i].traits & RA_UNIT_LIMBO) && app.scene.battle.units[i].team == 1)
            types[app.scene.battle.units[i].type] = true;
    bool any = false;
    for (unsigned i = 0; i < RA_BATTLE_TYPES; ++i)
        if (types[i]) any = true;
    if (all && !any) memcpy(types, app.type_mask, sizeof(types));
    else memcpy(app.type_mask, types, sizeof(types));
    for (uint32_t i = 0; i < app.scene.battle.count; ++i)
    {
        const ra_battle_unit *u = &app.scene.battle.units[i];
        app.selected[i] = u->health && !(u->traits & RA_UNIT_LIMBO) && u->team == 1 && types[u->type] && (all || visible_unit(i));
    }
    app.follow = false;
}
static void select_next(void)
{
    uint32_t count = app.scene.battle.count, start = count ? count - 1 : 0;
    for (uint32_t i = 0; i < count; ++i)
        if (app.selected[i])
        {
            start = i;
            break;
        }
    for (uint32_t step = 1; step <= count; ++step)
    {
        uint32_t at = (start + step) % count;
        if (!app.scene.battle.units[at].health || app.scene.battle.units[at].team != 1 || app.scene.battle.types[app.scene.battle.units[at].type].structure)
            continue;
        memset(app.selected, 0, sizeof(app.selected));
        app.selected[at] = true;
        app.follow = false;
        break;
    }
}
static void menu_layout(void)
{
    int left = app.width / 2 - 216, top = app.height / 2 - 76;
    for (unsigned i = 0; i < 5; ++i)
        if (app.menu_controls[i]) MoveWindow(app.menu_controls[i], left + (i == 1 ? 110 : 0), top + (int)i * 46, i == 1 ? 220 : 432, i == 1 ? 200 : 32, TRUE);
}
static void menu_set(bool value)
{
    if (value == app.options) return;
    if (value)
    {
        plan_clear();
        app.resume_after_menu = !app.paused;
        paused(true);
        app.dragging = app.panning = false;
        if (GetCapture() == app.window) ReleaseCapture();
    }
    app.options = value;
    for (unsigned id = ID_MAP; id < ID_OPTIONS; ++id) EnableWindow(GetDlgItem(app.window, (int)id), !value);
    memset(app.held, 0, sizeof(app.held));
    app.modifiers = 0;
    app.pointer_inside = false;
    for (unsigned i = 0; i < 5; ++i) ShowWindow(app.menu_controls[i], value ? SW_SHOW : SW_HIDE);
    if (!value && app.resume_after_menu) paused(false);
    menu_layout();
    SetFocus(app.window);
    InvalidateRect(app.window, NULL, FALSE);
}
static void view_tick(uint64_t microseconds)
{
    int dx = 0, dy = 0;
    if (app.options || app.loading) return;
    if (app.pointer_inside && !app.dragging && !app.panning)
    {
        if (app.pointer_x < 10) --dx;
        if (app.pointer_x >= app.width - 10) ++dx;
        if (app.pointer_y < 10) --dy;
        if (app.pointer_y >= app.height - 10) ++dy;
    }
    if (dx || dy)
    {
        if (microseconds > 100000) microseconds = 100000;
        app.camera_phase += microseconds * 600;
        int pixels = (int)(app.camera_phase / 1000000);
        app.camera_phase %= 1000000;
        app.pan_x -= max(-1, min(1, dx)) * pixels;
        app.pan_y -= max(-1, min(1, dy)) * pixels;
        app.follow = false;
        view_limit();
        if (pixels) InvalidateRect(app.window, NULL, FALSE);
    }
    else if (app.follow) center_selection();
}
static void key_command(uint32_t key, bool repeat)
{
    uint32_t code = key | app.modifiers;
    char command[48];
    ULONGLONG now = GetTickCount64();
    if (hotkey("Options", code))
    {
        if (!repeat) menu_set(!app.options);
        return;
    }
    if (app.options || repeat || (app.scene.battle.campaign && (app.scene.battle.campaign->state.input_locked || app.scene.battle.campaign->state.outcome)))
        return;
    if (hotkey("StopObject", code)) selected_order(RA_ORDER_STOP, 0);
    else if (hotkey("GuardObject", code)) selected_order(RA_ORDER_GUARD, 0);
    else if (hotkey("DeployObject", code)) selected_order(RA_ORDER_DEPLOY, 0);
    else if (hotkey("ScatterObject", code)) selected_order(RA_ORDER_SCATTER, 0);
    else if (hotkey("PlanningMode", code))
    {
        if (!app.replay)
        {
            app.planning = true;
            app.planning_key = key & 255;
            message(L"按住 Z 规划路径；左键添加节点，点击已有节点闭合巡逻，松键统一执行。 ");
        }
    }
    else if (hotkey("TypeSelect", code))
    {
        type_select(now - app.last_type_time < 500);
        app.last_type_time = now;
    }
    else if (hotkey("CombatantSelect", code))
    {
        for (uint32_t i = 0; i < app.scene.battle.count; ++i)
            app.selected[i] = app.scene.battle.units[i].health && !(app.scene.battle.units[i].traits & RA_UNIT_LIMBO) && app.scene.battle.units[i].team == 1 &&
                              !app.scene.battle.types[app.scene.battle.units[i].type].structure;
        app.follow = false;
    }
    else if (hotkey("NextObject", code)) select_next();
    else if (hotkey("CenterView", code)) center_selection();
    else if (hotkey("Follow", code))
    {
        app.follow = !app.follow && friendly_selected();
        if (app.follow) center_selection();
    }
    else if (hotkey("CenterOnRadarEvent", code))
    {
        if (app.event_count)
        {
            if (now - app.last_event_time > 1000) app.event_cursor = 0;
            center_at(app.event_x[app.event_cursor], app.event_y[app.event_cursor]);
            app.event_cursor = (app.event_cursor + 1) % app.event_count;
            app.last_event_time = now;
            app.follow = false;
        }
        else message(L"当前没有战场警报事件。");
    }
    else if (hotkey("ScreenCapture", code))
    {
        wchar_t module[32768], file[32768], *slash;
        char path[65536];
        if (!GetModuleFileNameW(NULL, module, 32768) || !(slash = wcsrchr(module, L'\\'))) return;
        *slash = 0;
        swprintf(file, 32768, L"%s\\screenshots", module);
        CreateDirectoryW(file, NULL);
        swprintf(file, 32768, L"%s\\screenshots\\battle-%llu.bmp", module, now);
        if (WideCharToMultiByte(CP_UTF8, 0, file, -1, path, sizeof(path), NULL, NULL) && snapshot(path))
            message(L"截图已保存到程序目录的 screenshots 文件夹。");
    }
    else if (hotkey("CenterBase", code)) message(L"尚未实现建设厂；H 保留原版基地定位用途。");
    else
    {
        for (unsigned group = 1; group <= 10; ++group)
        {
            snprintf(command, sizeof(command), "TeamCreate_%u", group);
            if (hotkey(command, code))
            {
                for (uint32_t i = 0; i < app.scene.battle.count; ++i)
                    app.groups[group - 1][i] = app.selected[i] && app.scene.battle.units[i].health && !(app.scene.battle.units[i].traits & RA_UNIT_LIMBO) &&
                                               app.scene.battle.units[i].team == 1;
                message(L"编队已建立；数字选择，Shift+数字加选，Alt+数字居中。");
                return;
            }
            snprintf(command, sizeof(command), "TeamSelect_%u", group);
            bool choose = hotkey(command, code);
            snprintf(command, sizeof(command), "TeamAddSelect_%u", group);
            bool add = hotkey(command, code);
            snprintf(command, sizeof(command), "TeamCenter_%u", group);
            bool center = hotkey(command, code);
            if (choose || add || center)
            {
                for (uint32_t i = 0; i < app.scene.battle.count; ++i)
                {
                    bool member = app.groups[group - 1][i] && app.scene.battle.units[i].health && !(app.scene.battle.units[i].traits & RA_UNIT_LIMBO) &&
                                  app.scene.battle.units[i].team == 1;
                    app.selected[i] = member || (add && app.selected[i] && app.scene.battle.units[i].team == 1 && app.scene.battle.units[i].health);
                }
                if (center || (choose && app.last_team == group && now - app.last_team_time < 500)) center_selection();
                app.last_team = group;
                app.last_team_time = now;
                app.follow = false;
                return;
            }
        }
        for (unsigned mark = 1; mark <= 4; ++mark)
        {
            snprintf(command, sizeof(command), "SetView%u", mark);
            if (hotkey(command, code))
            {
                app.marks[mark - 1] = true;
                app.mark_x[mark - 1] = app.pan_x;
                app.mark_y[mark - 1] = app.pan_y;
                return;
            }
            snprintf(command, sizeof(command), "View%u", mark);
            if (hotkey(command, code))
            {
                if (app.marks[mark - 1])
                {
                    app.pan_x = app.mark_x[mark - 1];
                    app.pan_y = app.mark_y[mark - 1];
                    app.follow = false;
                    view_limit();
                }
                return;
            }
        }
        /* 未完成的玩法保留原键语义，不借用为原型工具或其他战斗命令。 */
        for (size_t i = 0; i < app.keyboard.entry_count; ++i)
        {
            int64_t value = 0;
            const ra_ini_entry *entry = &app.keyboard.entries[i];
            if (ra_ini_integer(entry, &value, NULL) && value == code)
            {
                wchar_t name[96], text[160];
                wide(entry->key, name, 96);
                swprintf(text, 160, L"原版命令 %s 对应的玩法尚未实现，键位已保留。", name);
                message(text);
                break;
            }
        }
    }
}
static void left_release(int x, int y, WPARAM flags)
{
    ra_battle *b = &app.scene.battle;
    if (b->campaign && (b->campaign->state.input_locked || b->campaign->state.outcome)) return;
    if (app.place_type_plus_one && b->economy && !app.replay)
    {
        uint32_t cell, type = app.place_type_plus_one - 1;
        ra_error error = {0};
        if (ground_cell(x, y, &cell) && ra_economy_placeable(b, 1, type, cell))
        {
            if (ra_economy_command(b, b->tick + 1, 1, RA_ECON_PLACE, cell * RA_BATTLE_TYPES + type, &error)) app.place_type_plus_one = 0;
            else error_message(&error);
        }
        else message(L"此处不能放置，选择平坦、空闲且靠近己方建筑的地面。 ");
        return;
    }
    app.last_type_time = 0;
    bool box = abs(x - app.drag_x) + abs(y - app.drag_y) > 8;
    bool shift = (flags & MK_SHIFT) != 0;
    uint32_t count = app.scene.battle.count;
    if (box)
    {
        if (!shift) memset(app.selected, 0, sizeof(app.selected));
        for (uint32_t i = 0; i < count; ++i)
        {
            int px, py;
            const ra_battle_unit *u = &app.scene.battle.units[i];
            if (!u->health || (u->traits & RA_UNIT_LIMBO) || u->team != 1 || app.scene.battle.types[u->type].structure) continue;
            battle_unit_pixel(&app.scene, u, &px, &py);
            px = (int)(px * app.zoom) + app.pan_x;
            py = (int)(py * app.zoom) + app.pan_y;
            if (px >= min(x, app.drag_x) && px <= max(x, app.drag_x) && py >= min(y, app.drag_y) && py <= max(y, app.drag_y)) app.selected[i] = true;
        }
    }
    else if (x >= 0 && y >= 0 && x < app.width && y < app.height)
    {
        render();
        uint32_t id = app.picked[(size_t)y * app.width + x];
        if (id && !app.modifiers && !shift && !app.replay && b->types[b->units[id - 1].type].passengers && b->units[id - 1].team == 1)
        {
            uint32_t commands = 0;
            ra_error error = {0};
            for (uint32_t i = 0; i < b->count; ++i)
                if (app.selected[i] && i + 1 != id && b->units[i].health && b->units[i].team == 1 &&
                    ra_battle_order_add(b, b->tick + 1, i + 1, RA_ORDER_LOAD, id, &error))
                    ++commands;
            if (commands)
            {
                message(L"登载命令已提交；选择运输工具后按 D 卸载。 ");
                return;
            }
        }
        if (id && !app.modifiers && !shift && !app.replay && (b->types[b->units[id - 1].type].structure || b->types[b->units[id - 1].type].naval))
        {
            uint32_t commands = 0;
            ra_error error = {0};
            for (uint32_t i = 0; i < b->count; ++i)
            {
                const ra_battle_unit *u = &b->units[i];
                const ra_battle_type *t = &b->types[u->type];
                if (app.selected[i] && u->health && !(u->traits & RA_UNIT_LIMBO) && u->team == 1 &&
                    (t->engineer || (t->c4 && !ra_battle_allied(b, 1, b->units[id - 1].team))) &&
                    ra_battle_order_add(b, b->tick + 1, i + 1, RA_ORDER_ENTER, id, &error))
                    ++commands;
            }
            if (commands)
            {
                message(L"接近目标后执行维修、占领或爆破。 ");
                return;
            }
        }
        if (b->economy && !app.modifiers && !shift && !app.replay)
        {
            uint32_t cell = 0;
            bool refinery = id && b->units[id - 1].team == 1 && b->economy->types[b->units[id - 1].type].refinery;
            bool ore = !id && ground_cell(x, y, &cell) && cell < b->width * b->height && (b->economy->ore[cell] & 63);
            if (refinery || ore)
            {
                uint32_t commands = 0;
                ra_error error = {0};
                for (uint32_t i = 0; i < b->count; ++i)
                    if (app.selected[i] && b->units[i].team == 1 && b->units[i].health && b->economy->types[b->units[i].type].harvester &&
                        ra_economy_command(b, b->tick + 1, i + 1, refinery ? RA_ECON_RETURN : RA_ECON_HARVEST, refinery ? id : cell, &error))
                        ++commands;
                if (commands)
                {
                    message(refinery ? L"矿车返回指定矿厂。 " : L"矿车开始采矿，装满后自动返回并继续采集。 ");
                    return;
                }
            }
        }
        if (app.modifiers & 0x400)
        {
            message(L"强制移动、碾压与护卫目标仍待对应单位和行为实现，Alt 修饰点击保持原用途。 ");
            return;
        }
        if ((flags & MK_CONTROL) && shift)
        {
            move_to(x, y, RA_ORDER_ATTACK_MOVE);
            return;
        }
        if (flags & MK_CONTROL)
        {
            uint32_t cell;
            if (id) selected_order(RA_ORDER_FORCE_UNIT, id);
            else if (ground_cell(x, y, &cell)) selected_order(RA_ORDER_FORCE_GROUND, cell);
            return;
        }
        if (id && id <= count && app.scene.battle.units[id - 1].team == 1)
        {
            bool old = app.selected[id - 1];
            if (!shift) memset(app.selected, 0, sizeof(app.selected));
            app.selected[id - 1] = !shift || !old;
        }
        else if (id && friendly_selected() && !ra_battle_allied(&app.scene.battle, 1, app.scene.battle.units[id - 1].team)) selected_order(RA_ORDER_ATTACK, id);
        else if (!id && friendly_selected()) move_to(x, y, RA_ORDER_MOVE);
        else
        {
            if (!shift) memset(app.selected, 0, sizeof(app.selected));
            if (id && id <= count) app.selected[id - 1] = true;
        }
    }
    app.follow = false;
}

static void selection_events(void)
{
    ra_battle *b = &app.scene.battle;
    if (!b->campaign || app.replay || b->campaign->state.input_locked || b->campaign->state.outcome) return;
    for (uint32_t i = 0; i < b->count; ++i)
    {
        if (app.selected[i] && !app.reported_selection[i] && b->units[i].health && b->units[i].team == 1)
        {
            ra_error error = {0};
            ra_battle_order_add(b, b->tick + 1, i + 1, RA_EVENT_SELECT, 0, &error);
        }
        app.reported_selection[i] = app.selected[i];
    }
}
static LRESULT CALLBACK window_proc(HWND window, UINT msg, WPARAM w, LPARAM l)
{
    switch (msg)
    {
    case WM_CREATE:
    {
        static const wchar_t *labels[] = {L"暂停", L"单步", L"重新开始", L"保存回放", L"读取回放", L"通行层", L"回到单位", L"选项 [Esc]"};
        app.window = window;
        app.font = CreateFontW(-16, 0, 0, 0, FW_NORMAL, 0, 0, 0, DEFAULT_CHARSET, 0, 0, CLEARTYPE_QUALITY, 0, L"Microsoft YaHei UI");
        app.combo = CreateWindowW(L"COMBOBOX", L"", WS_CHILD | WS_VISIBLE | CBS_DROPDOWNLIST | WS_VSCROLL, 12, 14, 220, 400, window, (HMENU)(INT_PTR)ID_MAP,
                                  NULL, NULL);
        SendMessageW(app.combo, WM_SETFONT, (WPARAM)app.font, TRUE);
        for (int i = 0; i < 8; ++i)
        {
            HWND button = CreateWindowW(L"BUTTON", labels[i], WS_CHILD | WS_VISIBLE | BS_PUSHBUTTON, 242 + i * 137, 11, 129, 32, window,
                                        (HMENU)(INT_PTR)(ID_PAUSE + i), NULL, NULL);
            SendMessageW(button, WM_SETFONT, (WPARAM)app.font, TRUE);
            if (!i) app.pause = button;
        }
        static const wchar_t *menu_labels[5] = {L"返回战场", L"", L"保存命令回放", L"读取命令回放", L"退出查看器"};
        for (int i = 0; i < 5; ++i)
        {
            app.menu_controls[i] = CreateWindowW(i == 1 ? L"COMBOBOX" : L"BUTTON", menu_labels[i], WS_CHILD | (i == 1 ? CBS_DROPDOWNLIST : BS_PUSHBUTTON), 0, 0,
                                                 10, 10, window, (HMENU)(INT_PTR)(ID_RESUME + i), NULL, NULL);
            SendMessageW(app.menu_controls[i], WM_SETFONT, (WPARAM)app.font, TRUE);
        }
        for (int i = 0; i < 4; ++i)
            SendMessageW(app.menu_controls[1], CB_ADDSTRING, 0, (LPARAM)(const wchar_t *[]){L"75%", L"100%（原始像素）", L"150%", L"200%"}[i]);
        SendMessageW(app.menu_controls[1], CB_SETCURSEL, 1, 0);
        SetTimer(window, 1, 16, NULL);
        return 0;
    }
    case WM_SIZE:
        layout();
        menu_layout();
        return 0;
    case WM_ERASEBKGND:
        return 1;
    case WM_PRINTCLIENT:
        /* 原生截图直接绘制当前客户区，避免桌面合成器返回前一帧的交互提示。 */
        paint((HDC)w);
        return 0;
    case WM_PAINT:
    {
        PAINTSTRUCT ps;
        HDC dc = BeginPaint(window, &ps);
        paint(dc);
        EndPaint(window, &ps);
        return 0;
    }
    case WM_TIMER:
    {
        LARGE_INTEGER now;
        QueryPerformanceCounter(&now);
        uint64_t us = (uint64_t)(now.QuadPart - app.last.QuadPart) * 1000000 / (uint64_t)app.frequency.QuadPart;
        if (GetActiveWindow() == app.window) view_tick(us);
        else if (app.follow && !app.options) center_selection();
        if (!app.loading && !app.paused && app.scene.battle.tiles)
        {
            uint32_t ticks = ra_battle_clock(&app.phase, us);
            if (ticks)
            {
                while (ticks--) step();
                InvalidateRect(window, NULL, FALSE);
            }
        }
        app.last = now;
        return 0;
    }
    case WM_COMMAND:
        if (LOWORD(w) == ID_ZOOM && HIWORD(w) == CBN_SELCHANGE)
        {
            static const double scales[4] = {.75, 1, 1.5, 2};
            LRESULT selected = SendMessageW(app.menu_controls[1], CB_GETCURSEL, 0, 0);
            if (selected >= 0 && selected < 4)
            {
                int cx = (int)((app.width / 2 - app.pan_x) / app.zoom), cy = (int)((app.height / 2 - app.pan_y) / app.zoom);
                app.zoom = scales[selected];
                center_at(cx, cy);
            }
            SetFocus(window);
            return 0;
        }
        if (app.options && LOWORD(w) < ID_OPTIONS) return 0;
        if (LOWORD(w) == ID_MAP && HIWORD(w) == CBN_SELCHANGE)
        {
            map_load((size_t)SendMessageW(app.combo, CB_GETCURSEL, 0, 0));
            return 0;
        }
        if (HIWORD(w) != BN_CLICKED) break;
        switch (LOWORD(w))
        {
        case ID_PAUSE:
            paused(!app.paused);
            break;
        case ID_STEP:
            paused(true);
            step();
            break;
        case ID_RESET:
            plan_clear();
            ra_battle_reset(&app.scene.battle);
            app.scene.battle.command_count = 0;
            app.replay = false;
            memset(app.reported_selection, 0, sizeof(app.reported_selection));
            app.event_count = app.event_cursor = 0;
            app.follow = false;
            paused(true);
            message(L"战场已重置；命令记录已清空。");
            break;
        case ID_SAVE:
            file_dialog(true);
            break;
        case ID_LOAD:
            file_dialog(false);
            break;
        case ID_NAV:
            app.navigation = !app.navigation;
            break;
        case ID_HOME:
            home();
            break;
        case ID_OPTIONS:
            menu_set(!app.options);
            break;
        case ID_RESUME:
            menu_set(false);
            break;
        case ID_MENU_SAVE:
            file_dialog(true);
            break;
        case ID_MENU_LOAD:
            menu_set(false);
            file_dialog(false);
            break;
        case ID_MENU_QUIT:
            DestroyWindow(window);
            return 0;
        }
        SetFocus(window);
        InvalidateRect(window, NULL, FALSE);
        return 0;
    case WM_KEYDOWN:
    case WM_SYSKEYDOWN:
        if (w < 256) app.held[w] = true;
        if (w == VK_SHIFT) app.modifiers |= 0x100;
        if (w == VK_CONTROL) app.modifiers |= 0x200;
        if (w == VK_MENU) app.modifiers |= 0x400;
        if (msg == WM_SYSKEYDOWN && w == VK_F4 && (app.modifiers & 0x400)) break;
        key_command((uint32_t)w | ((l & ((LPARAM)1 << 24)) ? 0x800 : 0), (l & ((LPARAM)1 << 30)) != 0);
        selection_events();
        InvalidateRect(window, NULL, FALSE);
        return 0;
    case WM_KEYUP:
    case WM_SYSKEYUP:
        if (app.planning && w == app.planning_key) plan_commit();
        if (w < 256) app.held[w] = false;
        if (w == VK_SHIFT) app.modifiers &= ~0x100u;
        if (w == VK_CONTROL) app.modifiers &= ~0x200u;
        if (w == VK_MENU) app.modifiers &= ~0x400u;
        return 0;
    case WM_KILLFOCUS:
    case WM_CANCELMODE:
        plan_clear();
        memset(app.held, 0, sizeof(app.held));
        app.modifiers = 0;
        app.pointer_inside = app.dragging = app.panning = false;
        app.camera_phase = 0;
        if (GetCapture() == window) ReleaseCapture();
        return 0;
    case WM_LBUTTONDOWN:
        if (app.options) return 0;
        SetFocus(window);
        if (economy_click(GET_X_LPARAM(l), GET_Y_LPARAM(l), false)) return 0;
        if (GET_Y_LPARAM(l) >= 58 && GET_Y_LPARAM(l) < app.height + 58)
        {
            app.dragging = true;
            app.drag_x = app.old_x = GET_X_LPARAM(l);
            app.drag_y = app.old_y = GET_Y_LPARAM(l) - 58;
            SetCapture(window);
        }
        return 0;
    case WM_LBUTTONUP:
        if (app.dragging && !app.options)
        {
            left_release(GET_X_LPARAM(l), GET_Y_LPARAM(l) - 58, w);
            selection_events();
            app.dragging = false;
            ReleaseCapture();
            InvalidateRect(window, NULL, FALSE);
        }
        return 0;
    case WM_LBUTTONDBLCLK:
        if (!app.options)
        {
            render();
            int x = GET_X_LPARAM(l), y = GET_Y_LPARAM(l) - 58;
            if (x >= 0 && y >= 0 && x < app.width && y < app.height)
            {
                uint32_t id = app.picked[(size_t)y * app.width + x];
                if (id && app.scene.battle.units[id - 1].team == 1)
                {
                    memset(app.selected, 0, sizeof(app.selected));
                    app.selected[id - 1] = true;
                    type_select(false);
                }
            }
        }
        InvalidateRect(window, NULL, FALSE);
        return 0;
    case WM_RBUTTONDOWN:
        if (app.options || GET_Y_LPARAM(l) < 58 || GET_Y_LPARAM(l) >= app.height + 58) return 0;
        SetFocus(window);
        if (economy_click(GET_X_LPARAM(l), GET_Y_LPARAM(l), true)) return 0;
        app.dragging = false;
        app.panning = true;
        app.right_moved = false;
        app.right_x = app.old_x = GET_X_LPARAM(l);
        app.right_y = app.old_y = GET_Y_LPARAM(l);
        SetCapture(window);
        return 0;
    case WM_RBUTTONUP:
        if (app.options) return 0;
        if (app.scene.battle.economy && GET_X_LPARAM(l) >= app.width - 260) return 0;
        if (app.place_type_plus_one)
        {
            app.place_type_plus_one = 0;
            app.panning = false;
            ReleaseCapture();
            InvalidateRect(window, NULL, FALSE);
            return 0;
        }
        if (!app.right_moved)
        {
            memset(app.selected, 0, sizeof(app.selected));
            app.follow = false;
            app.last_type_time = 0;
            message(app.planning ? L"已取消选择，已规划路线保留；可选择另一编队，松开 Z 统一执行。" : L"已取消选择；已下达的单位命令继续执行，S 才是停止。 ");
        }
        app.panning = app.right_moved = false;
        if (GetCapture() == window) ReleaseCapture();
        InvalidateRect(window, NULL, FALSE);
        return 0;
    case WM_CAPTURECHANGED:
        app.panning = app.dragging = false;
        return 0;
    case WM_MOUSELEAVE:
        app.pointer_inside = false;
        app.camera_phase = 0;
        return 0;
    case WM_MOUSEMOVE:
    {
        int x = GET_X_LPARAM(l), y = GET_Y_LPARAM(l);
        if (!app.pointer_inside)
        {
            TRACKMOUSEEVENT tracking = {sizeof(tracking), TME_LEAVE, window, 0};
            TrackMouseEvent(&tracking);
        }
        app.pointer_x = x;
        app.pointer_y = y - 58;
        app.pointer_inside = x >= 0 && x < app.width && y >= 58 && y < app.height + 58;
        if (app.options) return 0;
        if (app.panning)
        {
            if (abs(x - app.right_x) + abs(y - app.right_y) > 4) app.right_moved = true;
            if (app.right_moved)
            {
                app.pan_x -= x - app.old_x;
                app.pan_y -= y - app.old_y;
                app.follow = false;
                view_limit();
            }
            app.old_x = x;
            app.old_y = y;
        }
        else if (app.dragging)
        {
            app.old_x = x;
            app.old_y = y - 58;
        }
        if (app.panning || app.dragging) InvalidateRect(window, NULL, FALSE);
        return 0;
    }
    case WM_MOUSEWHEEL:
        /* 原版没有战场滚轮缩放；预览倍率改由选项中的显式控件设置。 */
        return 0;
    case WM_SETCURSOR:
        if (LOWORD(l) == HTCLIENT && !app.options)
        {
            POINT point;
            GetCursorPos(&point);
            ScreenToClient(window, &point);
            point.y -= 58;
            if (point.x >= 0 && point.y >= 0 && point.x < app.width && point.y < app.height)
            {
                LPCWSTR cursor = app.panning ? IDC_SIZEALL : IDC_ARROW;
                uint32_t id = app.picked ? app.picked[(size_t)point.y * app.width + point.x] : 0;
                if (friendly_selected() && id && !ra_battle_allied(&app.scene.battle, 1, app.scene.battle.units[id - 1].team)) cursor = IDC_CROSS;
                SetCursor(LoadCursorW(NULL, cursor));
                return TRUE;
            }
        }
        break;
    case WM_DESTROY:
        KillTimer(window, 1);
        PostQuitMessage(0);
        return 0;
    }
    return DefWindowProcW(window, msg, w, l);
}

static void pump(void)
{
    MSG msg;
    unsigned count = 0;
    ULONGLONG deadline = GetTickCount64() + 20;
    /* 检查构建可能绘制很慢，必须给消息泵设置工作预算，避免刷新队列长期占满。 */
    while (count++ < 32 && GetTickCount64() < deadline && PeekMessageW(&msg, NULL, 0, 0, PM_REMOVE))
    {
        TranslateMessage(&msg);
        DispatchMessageW(&msg);
    }
}
static bool snapshot(const char *path)
{
    HDC dc, memory;
    HBITMAP bitmap;
    HGDIOBJ old;
    BITMAPINFO info = {0};
    RECT r;
    void *pixels;
    map_image image = {0};
    ra_error e = {0};
    bool ok;
    pump();
    RedrawWindow(app.window, NULL, NULL, RDW_INVALIDATE | RDW_UPDATENOW | RDW_ALLCHILDREN);
    DwmFlush();
    GetClientRect(app.window, &r);
    dc = GetDC(app.window);
    memory = CreateCompatibleDC(dc);
    info.bmiHeader.biSize = sizeof(BITMAPINFOHEADER);
    info.bmiHeader.biWidth = r.right;
    info.bmiHeader.biHeight = -r.bottom;
    info.bmiHeader.biPlanes = 1;
    info.bmiHeader.biBitCount = 32;
    bitmap = CreateDIBSection(dc, &info, DIB_RGB_COLORS, &pixels, NULL, 0);
    old = SelectObject(memory, bitmap);
    ok = PrintWindow(app.window, memory, PW_CLIENTONLY) != 0;
    GdiFlush();
    image.pixels = pixels;
    image.width = r.right;
    image.height = r.bottom;
    if (ok) ok = map_image_bmp(&image, path, &e);
    SelectObject(memory, old);
    DeleteObject(bitmap);
    DeleteDC(memory);
    ReleaseDC(app.window, dc);
    return ok;
}
static bool snapshot_has_color(const char *path, uint32_t color)
{
    ra_file file = {0};
    ra_error e = {0};
    uint32_t count = 0;
    if (!ra_file_open(&file, path, &e)) return false;
    if (file.view.size >= 54 && ra_le32(file.view.data + 10) == 54 && ra_le16(file.view.data + 28) == 32)
        for (size_t i = 54; i + 4 <= file.view.size; i += 4)
            if ((ra_le32(file.view.data + i) & 0xffffff) == color) ++count;
    ra_file_close(&file);
    return count >= 64;
}
static void test_click(int x, int y, WPARAM flags, bool right)
{
    SendMessageW(app.window, right ? WM_RBUTTONDOWN : WM_LBUTTONDOWN, flags | (right ? MK_RBUTTON : MK_LBUTTON), MAKELPARAM(x, y + 58));
    SendMessageW(app.window, right ? WM_RBUTTONUP : WM_LBUTTONUP, flags, MAKELPARAM(x, y + 58));
}
static void test_key(uint32_t key, uint32_t modifiers)
{
    if (modifiers & 0x100) SendMessageW(app.window, WM_KEYDOWN, VK_SHIFT, 0);
    if (modifiers & 0x200) SendMessageW(app.window, WM_KEYDOWN, VK_CONTROL, 0);
    if (modifiers & 0x400) SendMessageW(app.window, WM_SYSKEYDOWN, VK_MENU, 0);
    SendMessageW(app.window, modifiers & 0x400 ? WM_SYSKEYDOWN : WM_KEYDOWN, key, 0);
    SendMessageW(app.window, modifiers & 0x400 ? WM_SYSKEYUP : WM_KEYUP, key, 0);
    if (modifiers & 0x400) SendMessageW(app.window, WM_SYSKEYUP, VK_MENU, 0);
    if (modifiers & 0x200) SendMessageW(app.window, WM_KEYUP, VK_CONTROL, 0);
    if (modifiers & 0x100) SendMessageW(app.window, WM_KEYUP, VK_SHIFT, 0);
}
static bool test_unit_point(uint32_t id, int *x, int *y)
{
    render();
    for (size_t at = 0; at < (size_t)app.width * app.height; ++at)
        if (app.picked[at] == id)
        {
            *x = (int)(at % app.width);
            *y = (int)(at / app.width);
            return true;
        }
    return false;
}
typedef struct
{
    size_t expected, visible, bridge_overlap;
} unit_visibility;
static unit_visibility test_unit_visibility(const ra_battle_unit *u)
{
    unit_visibility result = {0};
    ra_error error = {0};
    const ra_voxel_image *sprite = battle_scene_sprite(&app.scene, u, &error);
    if (!sprite) return result;
    render();
    int cx, cy;
    battle_unit_pixel(&app.scene, u, &cx, &cy);
    int width = (int)(sprite->width * app.zoom), height = (int)(sprite->height * app.zoom);
    int left = (int)(cx * app.zoom) + app.pan_x - (int)(sprite->origin_x * app.zoom);
    int top = (int)(cy * app.zoom) + app.pan_y - (int)(sprite->origin_y * app.zoom);
    /* 逐像素检查整辆车，而不是只找到一个可点击像素就认为模型完整。 */
    for (int y = 0; y < height; ++y)
        for (int x = 0; x < width; ++x)
        {
            size_t source = (size_t)(y * (int)sprite->height / height) * sprite->width + (size_t)(x * (int)sprite->width / width);
            if (!(sprite->pixels[source] >> 24)) continue;
            ++result.expected;
            int px = left + x, py = top + y;
            if (px < 0 || py < 0 || px >= app.width || py >= app.height) continue;
            if (app.picked[(size_t)py * app.width + px] == u->id && app.pixels[(size_t)py * app.width + px] == (sprite->pixels[source] & 0xffffff))
                ++result.visible;
            int wx = (int)((px - app.pan_x) / app.zoom), wy = (int)((py - app.pan_y) / app.zoom);
            if (wx >= 0 && wy >= 0 && wx < app.scene.deck.width && wy < app.scene.deck.height &&
                (app.scene.deck.pixels[(size_t)wy * app.scene.deck.width + wx] >> 24))
                ++result.bridge_overlap;
        }
    return result;
}
static int self_test(const char *directory)
{
    unsigned checks = 0, failures = 0;
    char path[32768];
    uint8_t digest[20], expected[20];
    uint32_t goal = 0, start, end;
    ra_error e = {0};
    ra_battle *b = &app.scene.battle;
    int x = 0, y = 0, x2 = 0, y2 = 0;
#define VERIFY(c)                                                                                                                                              \
    do                                                                                                                                                         \
    {                                                                                                                                                          \
        ++checks;                                                                                                                                              \
        if (!(c))                                                                                                                                              \
        {                                                                                                                                                      \
            ++failures;                                                                                                                                        \
            fprintf(stderr, "line %d: %s\n", __LINE__, #c);                                                                                                    \
        }                                                                                                                                                      \
    } while (0)
    VERIFY(b->count == 4 && app.scene.ground.missing == 0);
    VERIFY(app.keyboard.entry_count == 89 && hotkey("NextObject", 'N') && hotkey("ScreenCapture", 'C' | 0x200));
    paused(true);
    VERIFY(test_unit_point(1, &x, &y));
    test_click(x, y, 0, false);
    VERIFY(app.selected[0] && !app.selected[1] && !app.selected[2] && !app.selected[3]);
    test_click(x, y, MK_SHIFT, false);
    VERIFY(!app.selected[0] && b->command_count == 0);
    test_click(x, y, MK_SHIFT, false);
    VERIFY(test_unit_point(2, &x2, &y2));
    test_click(x2, y2, MK_SHIFT, false);
    VERIFY(app.selected[0] && app.selected[1]);
    test_click(x, y, 0, true);
    VERIFY(!app.selected[0] && !app.selected[1] && b->command_count == 0);
    VERIFY(test_unit_point(1, &x, &y));
    test_click(x, y, 0, false);
    start = b->units[0].cell;
    VERIFY(battle_scene_goal(&app.scene, 1, 5, &goal));
    x = (int)((((int)(goal % 512) - (int)ra_battle_cell_y(b, goal)) * 30 + app.scene.ground.origin_x + 30) * app.zoom) + app.pan_x;
    y = (int)((((int)(goal % 512) + (int)ra_battle_cell_y(b, goal) - b->tiles[goal].height) * 15 + app.scene.ground.origin_y + 15) * app.zoom) + app.pan_y;
    snprintf(path, sizeof(path), "%s/battle-before.bmp", directory);
    VERIFY(snapshot(path));
    test_click(x, y, 0, true);
    VERIFY(b->command_count == 0 && !app.selected[0]);
    VERIFY(test_unit_point(1, &x2, &y2));
    test_click(x2, y2, 0, false);
    test_click(x, y, MK_CONTROL, false);
    VERIFY(b->command_count == 1 && b->commands[0].kind == RA_ORDER_FORCE_GROUND && app.selected[0]);
    test_click(x, y, MK_CONTROL | MK_SHIFT, false);
    VERIFY(b->command_count == 2 && b->commands[1].kind == RA_ORDER_ATTACK_MOVE);
    SendMessageW(app.window, WM_COMMAND, ID_RESET, 0);
    app.selected[0] = true;
    test_click(x, y, 0, false);
    VERIFY(b->command_count == 1 && b->commands[0].kind == RA_ORDER_MOVE);
    test_click(x2, y2, 0, true);
    VERIFY(b->command_count == 1 && !app.selected[0]);
    for (unsigned i = 0; i < 900; ++i) SendMessageW(app.window, WM_COMMAND, ID_STEP, 0);
    VERIFY(b->units[0].cell == goal && goal != start);
    ra_battle_hash(b, expected);
    end = b->tick;
    snprintf(path, sizeof(path), "%s/battle-after.bmp", directory);
    VERIFY(snapshot(path));
    snprintf(path, sizeof(path), "%s/native.rpl", directory);
    VERIFY(replay_save(path));
    VERIFY(replay_load(path));
    paused(true);
    while (b->tick < end) step();
    ra_battle_hash(b, digest);
    VERIFY(!memcmp(digest, expected, 20) && wcsstr(app.status, L"校验一致"));
    VERIFY(!ra_battle_command_add(b, 0, 1, goal, &e));
    SendMessageW(app.window, WM_COMMAND, ID_RESET, 0);
    VERIFY(!app.replay && b->tick == 0 && b->command_count == 0);
    snprintf(path, sizeof(path), "%s/empty.rpl", directory);
    VERIFY(replay_save(path));
    VERIFY(replay_load(path));
    VERIFY(app.paused && app.replay_end == 0 && wcsstr(app.status, L"校验一致"));
    SendMessageW(app.window, WM_COMMAND, ID_RESET, 0);
    home();
    {
        uint32_t enemy = 3;
        bool flight = false, explosion = false;
        VERIFY(test_unit_point(enemy, &x, &y));
        test_click(x, y, 0, true);
        test_click(x, y, 0, false);
        VERIFY(app.selected[enemy - 1] && !friendly_selected() && b->command_count == 0);
        VERIFY(test_unit_point(2, &x2, &y2));
        test_click(x2, y2, 0, false);
        test_click(x, y, 0, false);
        VERIFY(b->command_count == 1 && b->commands[0].kind == RA_ORDER_ATTACK && b->commands[0].target == enemy && app.selected[1]);
        for (unsigned i = 0; i < 900 && !b->kills; ++i)
        {
            step();
            if (!flight && b->fired)
            {
                snprintf(path, sizeof(path), "%s/combat-flight.bmp", directory);
                VERIFY(snapshot(path));
                flight = true;
            }
            if (!explosion && b->impacts)
            {
                snprintf(path, sizeof(path), "%s/combat-impact.bmp", directory);
                VERIFY(snapshot(path));
                explosion = true;
            }
        }
        VERIFY(flight && explosion && b->fired >= 4 && b->impacts >= 4 && b->kills == 1);
        VERIFY(!b->units[enemy - 1].health && !b->occupied[b->units[enemy - 1].cell]);
        snprintf(path, sizeof(path), "%s/combat-destroyed.bmp", directory);
        VERIFY(snapshot(path));
        VERIFY(app.event_count > 0);
        int pan = app.pan_x;
        app.pan_x -= 150;
        test_key(VK_SPACE, 0);
        VERIFY(app.paused && app.pan_x != pan - 150);
        ra_battle_hash(b, expected);
        end = b->tick;
        snprintf(path, sizeof(path), "%s/combat.rpl", directory);
        VERIFY(replay_save(path));
        VERIFY(replay_load(path));
        paused(true);
        while (b->tick < end) step();
        ra_battle_hash(b, digest);
        VERIFY(!memcmp(digest, expected, 20) && wcsstr(app.status, L"校验一致"));
        SendMessageW(app.window, WM_COMMAND, ID_RESET, 0);
    }
    /* 以下操作由真实窗口消息触发，并观察固定步后的实际单位行为。 */
    home();
    memset(app.selected, 0, sizeof(app.selected));
    app.selected[0] = true;
    VERIFY(test_unit_point(2, &x, &y));
    test_click(x, y, MK_CONTROL, false);
    VERIFY(b->command_count == 1 && b->commands[0].kind == RA_ORDER_FORCE_UNIT && b->commands[0].target == 2 && app.selected[0]);
    for (unsigned i = 0; i < 160; ++i) step();
    VERIFY(b->fired > 0 && b->units[1].health < b->initial[1].health);
    SendMessageW(app.window, WM_COMMAND, ID_RESET, 0);
    app.selected[0] = true;
    VERIFY(battle_scene_goal(&app.scene, 1, 5, &goal));
    cell_point(goal, &x, &y);
    test_click(x, y - 58, MK_CONTROL, false);
    for (unsigned i = 0; i < 900 && !b->fired; ++i) step();
    if (!b->fired)
        fprintf(stderr, "force ground: order=%u cell=%u next=%u goal=%u fire_cell=%u path=%u/%u rejected=%u health=%u\n", b->units[0].order, b->units[0].cell,
                b->units[0].next, b->units[0].goal, b->units[0].fire_cell, b->units[0].path_cursor, b->units[0].path_count, b->rejected, b->units[0].health);
    VERIFY(b->units[0].order == RA_ORDER_FORCE_GROUND && b->fired > 0 && b->units[0].target == 0);
    snprintf(path, sizeof(path), "%s/force-ground.bmp", directory);
    VERIFY(snapshot(path));
    SendMessageW(app.window, WM_COMMAND, ID_RESET, 0);
    home();
    app.selected[0] = true;
    test_key('G', 0);
    step();
    VERIFY(b->command_count == 1 && b->units[0].order == RA_ORDER_GUARD && b->units[0].anchor == b->initial[0].cell);
    SendMessageW(app.window, WM_COMMAND, ID_RESET, 0);
    app.selected[0] = true;
    test_key('X', 0);
    for (unsigned i = 0; i < 120; ++i) step();
    VERIFY(b->command_count == 1 && b->units[0].order == RA_ORDER_SCATTER && b->units[0].cell != b->initial[0].cell);
    SendMessageW(app.window, WM_COMMAND, ID_RESET, 0);
    home();
    app.selected[0] = true;
    uint32_t route[2];
    VERIFY(battle_scene_goal(&app.scene, 1, 5, &route[0]) && battle_scene_goal(&app.scene, 1, 3, &route[1]) && route[0] != route[1]);
    SendMessageW(app.window, WM_KEYDOWN, 'Z', 0);
    for (unsigned i = 0; i < 2; ++i)
    {
        cell_point(route[i], &x, &y);
        test_click(x, y - 58, 0, false);
    }
    VERIFY(app.planning && app.plan_count[0] == 2 && b->command_count == 0);
    for (unsigned i = 0; i < 10; ++i) step();
    VERIFY(b->units[0].cell == b->initial[0].cell);
    snprintf(path, sizeof(path), "%s/waypoints-planning.bmp", directory);
    VERIFY(snapshot(path) && snapshot_has_color(path, 0x5af0ff));
    test_click(100, 100, 0, true);
    VERIFY(!app.selected[0] && app.plan_count[0] == 2);
    VERIFY(test_unit_point(2, &x, &y));
    test_click(x, y, 0, false);
    VERIFY(battle_scene_goal(&app.scene, 2, 7, &goal));
    cell_point(goal, &x, &y);
    test_click(x, y - 58, 0, false);
    VERIFY(app.plan_count[0] == 2 && app.plan_count[1] == 1);
    SendMessageW(app.window, WM_KEYUP, 'Z', 0);
    VERIFY(!app.planning && b->command_count == 3 && b->commands[0].tick == b->commands[2].tick);
    for (unsigned i = 0; i < 1200; ++i) step();
    if (b->units[0].cell != route[1] || b->units[1].cell != goal)
        fprintf(stderr, "waypoints: u1 cell=%u goal=%u intent=%u wanted=%u cursor=%u count=%u; u2 cell=%u goal=%u wanted=%u\n", b->units[0].cell,
                b->units[0].goal, b->units[0].destination, route[1], b->units[0].waypoint_cursor, b->units[0].waypoint_count, b->units[1].cell,
                b->units[1].goal, goal);
    VERIFY(b->units[0].cell == route[1] && b->units[1].cell == goal && !b->units[0].waypoint_count);
    ra_battle_hash(b, expected);
    end = b->tick;
    snprintf(path, sizeof(path), "%s/waypoints.rpl", directory);
    VERIFY(replay_save(path) && replay_load(path));
    paused(true);
    while (b->tick < end) step();
    ra_battle_hash(b, digest);
    VERIFY(!memcmp(digest, expected, 20));
    SendMessageW(app.window, WM_COMMAND, ID_RESET, 0);
    home();
    memset(app.selected, 0, sizeof(app.selected));
    app.selected[0] = true;
    SendMessageW(app.window, WM_KEYDOWN, 'Z', 0);
    for (unsigned i = 0; i < 2; ++i)
    {
        cell_point(route[i], &x, &y);
        test_click(x, y - 58, 0, false);
    }
    cell_point(route[0], &x, &y);
    test_click(x, y - 58, 0, false);
    VERIFY(app.plan_loop[0] == 1);
    SendMessageW(app.window, WM_KEYUP, 'Z', 0);
    step();
    VERIFY(b->units[0].waypoint_count == 2 && b->units[0].waypoint_loop == 1);
    snprintf(path, sizeof(path), "%s/patrol.bmp", directory);
    VERIFY(snapshot(path) && snapshot_has_color(path, 0xf5d864));
    test_key('S', 0);
    step();
    VERIFY(!b->units[0].waypoint_count && !b->units[0].waypoint_loop);
    SendMessageW(app.window, WM_COMMAND, ID_RESET, 0);
    SendMessageW(app.window, WM_KEYDOWN, 'Z', 0);
    cell_point(route[0], &x, &y);
    test_click(x, y - 58, 0, false);
    SendMessageW(app.window, WM_KILLFOCUS, 0, 0);
    SendMessageW(app.window, WM_KEYUP, 'Z', 0);
    VERIFY(!app.planning && b->command_count == 0 && !app.plan_count[0]);
    home();
    memset(app.selected, 0, sizeof(app.selected));
    app.selected[0] = true;
    test_key('A', 0);
    VERIFY(b->command_count == 0 && wcsstr(app.status, L"ToggleAlliance"));
    test_key(VK_SPACE, 0);
    VERIFY(app.paused && b->tick == 0);
    test_key(VK_F5, 0);
    test_key(VK_F9, 0);
    test_key(VK_F10, 0);
    VERIFY(b->tick == 0 && b->command_count == 0 && !app.replay);
    test_key('S', 0);
    VERIFY(b->command_count == 1 && b->commands[0].kind == RA_ORDER_STOP);
    SendMessageW(app.window, WM_COMMAND, ID_RESET, 0);
    app.selected[0] = true;
    test_key('1', 0x200);
    VERIFY(app.groups[0][0] && !app.groups[0][1]);
    memset(app.selected, 0, sizeof(app.selected));
    app.selected[1] = true;
    test_key('1', 0x100);
    VERIFY(app.selected[0] && app.selected[1]);
    test_key('0', 0x200);
    VERIFY(app.groups[9][0] && app.groups[9][1]);
    memset(app.selected, 0, sizeof(app.selected));
    test_key('0', 0);
    VERIFY(app.selected[0] && app.selected[1]);
    test_key('1', 0);
    VERIFY(app.selected[0] && !app.selected[1]);
    int pan = app.pan_x;
    test_key('1', 0x400);
    VERIFY(app.pan_x != pan && app.selected[0]);
    app.pan_x -= 100;
    pan = app.pan_x;
    test_key('1', 0);
    VERIFY(app.pan_x != pan);
    /* 在地图内部验证拖动位移，边界处视角会按原版习惯停止滚动。 */
    app.pan_x = (app.width - (int)(app.scene.ground.width * app.zoom)) / 2;
    app.pan_y = (app.height - (int)(app.scene.ground.height * app.zoom)) / 2;
    test_key(VK_F1, 0x200);
    int bookmarked_x = app.pan_x, bookmarked_y = app.pan_y;
    SendMessageW(app.window, WM_RBUTTONDOWN, MK_RBUTTON, MAKELPARAM(500, 400));
    SendMessageW(app.window, WM_MOUSEMOVE, MK_RBUTTON, MAKELPARAM(520, 410));
    SendMessageW(app.window, WM_RBUTTONUP, 0, MAKELPARAM(520, 410));
    VERIFY(app.pan_x == bookmarked_x - 20 && app.pan_y == bookmarked_y - 10 && app.selected[0]);
    test_key(VK_F1, 0);
    VERIFY(app.pan_x == bookmarked_x && app.pan_y == bookmarked_y);
    memset(app.selected, 0, sizeof(app.selected));
    app.selected[0] = true;
    test_key('N', 0);
    VERIFY(app.selected[1] && !app.selected[0]);
    test_key('P', 0);
    VERIFY(app.selected[0] && app.selected[1] && !app.selected[2]);
    home();
    memset(app.selected, 0, sizeof(app.selected));
    app.selected[0] = true;
    app.last_type_time = 0;
    test_key('T', 0);
    VERIFY(app.selected[0] && !app.selected[1]);
    app.pan_x = app.pan_y = 0;
    app.last_type_time = 0;
    test_key('T', 0);
    test_key('T', 0);
    VERIFY(app.selected[0] && !app.selected[1]);
    home();
    VERIFY(test_unit_point(1, &x, &y));
    SendMessageW(app.window, WM_LBUTTONDBLCLK, MK_LBUTTON, MAKELPARAM(x, y + 58));
    VERIFY(app.selected[0] && !app.selected[1] && b->command_count == 0);
    test_key('F', 0);
    VERIFY(app.follow);
    app.pan_x -= 100;
    pan = app.pan_x;
    view_tick(16000);
    VERIFY(app.pan_x != pan);
    test_key('F', 0);
    VERIFY(!app.follow);
    ra_battle_hash(b, expected);
    pan = app.pan_x;
    app.pointer_inside = true;
    app.pointer_x = app.width - 1;
    app.pointer_y = app.height / 2;
    view_tick(100000);
    VERIFY(app.pan_x == pan - 60);
    SendMessageW(app.window, WM_MOUSELEAVE, 0, 0);
    pan = app.pan_x;
    view_tick(100000);
    VERIFY(app.pan_x == pan);
    SendMessageW(app.window, WM_KEYDOWN, VK_LEFT, (LPARAM)1 << 24);
    view_tick(100000);
    SendMessageW(app.window, WM_KEYUP, VK_LEFT, (LPARAM)1 << 24);
    VERIFY(app.pan_x == pan);
    SendMessageW(app.window, WM_KEYDOWN, VK_CONTROL, 0);
    SendMessageW(app.window, WM_KILLFOCUS, 0, 0);
    VERIFY(!app.modifiers && !app.pointer_inside && !app.held[VK_CONTROL]);
    double zoom = app.zoom;
    SendMessageW(app.window, WM_MOUSEWHEEL, MAKEWPARAM(0, WHEEL_DELTA), 0);
    VERIFY(app.zoom == zoom);
    SendMessageW(app.window, WM_MBUTTONDOWN, MK_MBUTTON, MAKELPARAM(500, 400));
    SendMessageW(app.window, WM_MOUSEMOVE, MK_MBUTTON, MAKELPARAM(520, 410));
    SendMessageW(app.window, WM_MBUTTONUP, 0, MAKELPARAM(520, 410));
    VERIFY(app.pan_x == pan);
    SendMessageW(app.window, WM_MOUSELEAVE, 0, 0);
    ra_battle_hash(b, digest);
    VERIFY(!memcmp(digest, expected, 20));
    paused(false);
    test_key(VK_ESCAPE, 0);
    VERIFY(app.options && app.paused && !IsWindowEnabled(app.combo));
    uint32_t commands = b->command_count;
    test_click(100, 100, 0, false);
    test_key('S', 0);
    VERIFY(b->command_count == commands);
    SendMessageW(app.menu_controls[1], CB_SETCURSEL, 2, 0);
    SendMessageW(app.window, WM_COMMAND, MAKEWPARAM(ID_ZOOM, CBN_SELCHANGE), 0);
    VERIFY(app.zoom == 1.5);
    snprintf(path, sizeof(path), "%s/input-options.bmp", directory);
    VERIFY(snapshot(path));
    test_key(VK_ESCAPE, 0);
    VERIFY(!app.options && !app.paused && IsWindowEnabled(app.combo));
    paused(true);
    test_key('C', 0x200);
    VERIFY(wcsstr(app.status, L"截图已保存"));
    {
        ULONGLONG started = GetTickCount64();
        paused(false);
        for (unsigned i = 0; i < 25; ++i)
        {
            Sleep(10);
            pump();
        }
        paused(true);
        VERIFY(b->tick > 0 && b->tick <= (GetTickCount64() - started) * RA_BATTLE_HZ / 1000 + 2);
    }
    test_click(0, 0, 0, true);
    SendMessageW(app.window, WM_LBUTTONDOWN, MK_LBUTTON, MAKELPARAM(0, 58));
    SendMessageW(app.window, WM_LBUTTONUP, 0, MAKELPARAM(app.width - 1, app.height + 57));
    for (unsigned i = 0; i < 4; ++i) VERIFY(app.selected[i] == (i < 2));
    SendMessageW(app.window, WM_COMMAND, ID_NAV, 0);
    VERIFY(app.navigation);
    snprintf(path, sizeof(path), "%s/battle-navigation.bmp", directory);
    VERIFY(snapshot(path));
    printf("{\"checks\":%u,\"failures\":%u,\"snapshots\":10,\"missions\":true,\"simulation_version\":%u,\"mouse_selection\":true,\"mouse_move\":true,\"mouse_"
           "attack\":true,\"combat_replay\":true,\"left_"
           "commands\":true,\"right_cancel\":true,\"groups\":true,\"hotkeys_from_original\":%zu,\"timer_ticks\":%u}\n",
           checks, failures, RA_BATTLE_VERSION, app.keyboard.entry_count, b->tick);
    return failures ? 1 : 0;
#undef VERIFY
}
static int layers_self_test(const char *directory)
{
    unsigned checks = 0, failures = 0;
    ra_error e = {0};
    ra_battle *b = &app.scene.battle;
    uint32_t goal = 0, deck = 0;
    char path[32768];
    uint8_t trace[1800][20];
#define VERIFY_LAYER(value)                                                                                                                                    \
    do                                                                                                                                                         \
    {                                                                                                                                                          \
        ++checks;                                                                                                                                              \
        if (!(value))                                                                                                                                          \
        {                                                                                                                                                      \
            ++failures;                                                                                                                                        \
            fprintf(stderr, "layer line %d: %s\n", __LINE__, #value);                                                                                          \
        }                                                                                                                                                      \
    } while (0)
    VERIFY_LAYER(battle_scene_bridge_fixture(&app.scene, &goal, &e));
    if (failures) return 1;
    VERIFY_LAYER(ra_battle_route(b, 1, goal));
    uint32_t start = b->units[0].cell, middle = b->units[0].path[b->units[0].path_count / 2];
    for (uint32_t i = 0; i < b->units[0].path_count; ++i)
        if (b->units[0].path[i] >= 512 * 512)
        {
            deck = b->units[0].path[i];
            break;
        }
    VERIFY_LAYER(deck >= 512 * 512 && app.scene.deck.drawn > 0);
    ra_battle_reset(b);
    app.zoom = 1.5;
    home();
    int x = 0, y = 0;
    VERIFY_LAYER(test_unit_point(1, &x, &y));
    test_click(x, y, 0, false);
    VERIFY_LAYER(app.selected[0]);
    snprintf(path, sizeof(path), "%s/bridge-before.bmp", directory);
    VERIFY_LAYER(snapshot(path));
    unit_visibility before = test_unit_visibility(&b->units[0]);
    VERIFY_LAYER(before.expected && before.visible == before.expected);
    cell_point(deck, &x, &y);
    uint32_t picked = 0;
    VERIFY_LAYER(ground_cell(x, y - 58, &picked) && picked == deck);
    cell_point(goal, &x, &y);
    /* 长桥的对岸可能在画面外，先移动镜头再发送真实鼠标命令。 */
    if (x < 8 || y < 66 || x >= app.width - 8 || y >= app.height + 50)
    {
        app.pan_x += app.width / 2 - x;
        app.pan_y += app.height / 2 - (y - 58);
        view_limit();
        cell_point(goal, &x, &y);
    }
    test_click(x, y - 58, 0, false);
    VERIFY_LAYER(b->command_count == 1 && b->commands[0].target == goal);
    bool crossed = false;
    for (unsigned tick = 0; tick < 900; ++tick)
    {
        step();
        ra_battle_hash(b, trace[b->tick - 1]);
        if (!crossed && b->units[0].cell >= 512 * 512)
        {
            crossed = true;
            home();
            snprintf(path, sizeof(path), "%s/bridge-on-deck.bmp", directory);
            VERIFY_LAYER(snapshot(path));
            VERIFY_LAYER(ra_battle_unit_height(b, &b->units[0]) == b->tiles[b->units[0].cell].height * 104);
        }
    }
    VERIFY_LAYER(crossed && b->units[0].cell == goal && !b->units[0].reserved_count);
    home();
    snprintf(path, sizeof(path), "%s/bridge-after.bmp", directory);
    VERIFY_LAYER(snapshot(path));
    unit_visibility after = test_unit_visibility(&b->units[0]);
    VERIFY_LAYER(after.expected && after.bridge_overlap && after.visible == after.expected);
    /* 两岸、两种坦克、八个朝向和三档缩放都必须完整显示；显示夹具结束后恢复模拟状态。 */
    uint8_t pose_before[20], pose_after[20];
    ra_battle_hash(b, pose_before);
    ra_battle_unit saved = b->units[0];
    double old_zoom = app.zoom;
    unsigned poses = 0;
    size_t overlap_pixels = 0;
    for (unsigned bank = 0; bank < 2; ++bank)
        for (unsigned type = 0; type < 2; ++type)
            for (unsigned direction = 0; direction < 8; ++direction)
                for (unsigned scale = 0; scale < 3; ++scale)
                {
                    ra_battle_unit *u = &b->units[0];
                    u->cell = u->next = bank ? goal : start;
                    u->x = (int32_t)(u->cell % 512 * RA_BATTLE_CELL);
                    u->y = (int32_t)(u->cell / 512 * RA_BATTLE_CELL);
                    u->type = type;
                    u->body = u->turret = (ra_battle_turn){direction * 8192, direction * 8192, 0, 0};
                    app.zoom = 1.0 + scale * 0.5;
                    home();
                    unit_visibility pose = test_unit_visibility(u);
                    VERIFY_LAYER(pose.expected && pose.visible == pose.expected);
                    overlap_pixels += pose.bridge_overlap;
                    ++poses;
                }
    VERIFY_LAYER(poses == 96 && overlap_pixels > 0 && middle >= 512 * 512);
    b->units[0] = saved;
    b->units[0].cell = b->units[0].next = middle;
    b->units[0].x = (int32_t)(middle % 512 * RA_BATTLE_CELL);
    b->units[0].y = (int32_t)(ra_battle_cell_y(b, middle) * RA_BATTLE_CELL);
    app.zoom = old_zoom;
    home();
    unit_visibility on_deck = test_unit_visibility(&b->units[0]);
    VERIFY_LAYER(on_deck.expected && on_deck.visible == on_deck.expected);
    /* 只改变显示探针的层号，确认真正位于桥下的像素仍被遮挡，不改地图通行数据。 */
    b->units[0].cell = b->units[0].next = middle % (512 * 512);
    home();
    unit_visibility under = test_unit_visibility(&b->units[0]);
    VERIFY_LAYER(under.expected && under.bridge_overlap && under.visible < under.expected);
    snprintf(path, sizeof(path), "%s/bridge-under.bmp", directory);
    VERIFY_LAYER(snapshot(path));
    b->units[0] = saved;
    home();
    ra_battle_hash(b, pose_after);
    VERIFY_LAYER(!memcmp(pose_before, pose_after, sizeof(pose_before)));
    VERIFY_LAYER(ra_battle_command_add(b, b->tick + 1, 1, start, &e));
    for (unsigned tick = 0; tick < 900; ++tick)
    {
        step();
        ra_battle_hash(b, trace[b->tick - 1]);
    }
    VERIFY_LAYER(b->units[0].cell == start && !b->units[0].reserved_count && !b->units[0].track_active);
    home();
    unit_visibility returned = test_unit_visibility(&b->units[0]);
    VERIFY_LAYER(returned.expected && returned.visible == returned.expected);
    snprintf(path, sizeof(path), "%s/bridge-return.bmp", directory);
    VERIFY_LAYER(snapshot(path));
    char visibility[1024];
    int size = snprintf(visibility, sizeof(visibility),
                        "{\"before\":{\"visible\":%zu,\"expected\":%zu,\"overlap\":%zu},\"after\":{\"visible\":%zu,\"expected\":%zu,\"overlap\":%zu},"
                        "\"returned\":{\"visible\":%zu,\"expected\":%zu},\"under_bridge\":{\"visible\":%zu,\"expected\":%zu,\"overlap\":%zu},"
                        "\"shore_poses\":%u,\"pose_overlap_pixels\":%zu,\"simulation_unchanged\":true}\n",
                        before.visible, before.expected, before.bridge_overlap, after.visible, after.expected, after.bridge_overlap, returned.visible,
                        returned.expected, under.visible, under.expected, under.bridge_overlap, poses, overlap_pixels);
    snprintf(path, sizeof(path), "%s/pixel-visibility.json", directory);
    VERIFY_LAYER(size > 0 && (size_t)size < sizeof(visibility) && battle_file_write(path, visibility, (size_t)size, &e));
    snprintf(path, sizeof(path), "%s/bridge-native.rpl", directory);
    VERIFY_LAYER(replay_save(path) && replay_load(path));
    uint8_t digest[20];
    while (b->tick < app.replay_end)
    {
        step();
        ra_battle_hash(b, digest);
        VERIFY_LAYER(b->tick <= 1800 && !memcmp(digest, trace[b->tick - 1], sizeof(digest)));
    }
    ra_battle_hash(b, digest);
    VERIFY_LAYER(!memcmp(digest, app.expected, 20));
    app.replay = false;
    memset(app.reported_selection, 0, sizeof(app.reported_selection));
    /* 使用真实坡格显示底盘倾斜；平坦桥图没有坡面时改用 MP13DU。 */
    bool slope_shown = false;
    for (unsigned attempt = 0; attempt < 2 && !slope_shown; ++attempt)
    {
        if (attempt)
            for (size_t i = 0; i < app.scene.maps.source_count; ++i)
            {
                if (!ra_equal(app.scene.maps.sources[i].name, "MP13DU.map")) continue;
                SendMessageW(app.combo, CB_SETCURSEL, i, 0);
                map_load(i);
                break;
            }
        for (uint32_t cell = 0; cell < 512 * 512; ++cell)
        {
            if (!ra_battle_passable(b, cell) || !b->tiles[cell].ramp) continue;
            ra_battle_unit candidate = {0};
            candidate.cell = cell;
            candidate.x = (int32_t)(cell % 512 * RA_BATTLE_CELL);
            candidate.y = (int32_t)(cell / 512 * RA_BATTLE_CELL);
            int px, py;
            battle_unit_pixel(&app.scene, &candidate, &px, &py);
            if (px < 96 || py < 96 || px >= app.scene.ground.width - 96 || py >= app.scene.ground.height - 96) continue;
            b->tick = b->count = b->command_count = b->command_cursor = 0;
            memset(b->occupied, 0, (size_t)2 * 512 * 512 * sizeof(*b->occupied));
            memset(b->units, 0, RA_BATTLE_UNITS * sizeof(*b->units));
            VERIFY_LAYER(ra_battle_spawn_team(b, 0, 1, cell % 512, cell / 512, &e));
            b->units[0].body = (ra_battle_turn){16384, 16384, 0, 0};
            b->units[0].turret = b->units[0].body;
            VERIFY_LAYER(ra_battle_unit_ramp(b, &b->units[0]) == b->tiles[cell].ramp);
            const ra_voxel_image *image = battle_scene_sprite(&app.scene, &b->units[0], &e);
            VERIFY_LAYER(image && image->drawn_pixels > 0);
            home();
            VERIFY_LAYER(test_unit_point(1, &x, &y));
            snprintf(path, sizeof(path), "%s/slope-chassis.bmp", directory);
            VERIFY_LAYER(snapshot(path));
            slope_shown = true;
            break;
        }
    }
    VERIFY_LAYER(slope_shown);
    printf(
        "{\"checks\":%u,\"failures\":%u,\"simulation_version\":%u,\"snapshots\":6,\"replay_steps\":1800,\"bridge_crossed\":%s,\"original_bridge_art\":true}\n",
        checks, failures, RA_BATTLE_VERSION, crossed ? "true" : "false");
    return failures ? 1 : 0;
#undef VERIFY_LAYER
}
static int bridges_self_test(const char *directory)
{
    ra_error e = {0};
    ra_battle *b = &app.scene.battle;
    uint32_t cell = 0, goal = 0, checks = 0, failures = 0;
    char path[32768];
#define VERIFY_BRIDGE(value)                                                                                                                                   \
    do                                                                                                                                                         \
    {                                                                                                                                                          \
        ++checks;                                                                                                                                              \
        if (!(value))                                                                                                                                          \
        {                                                                                                                                                      \
            ++failures;                                                                                                                                        \
            fprintf(stderr, "bridge line %d: %s\n", __LINE__, #value);                                                                                         \
        }                                                                                                                                                      \
    } while (0)
    VERIFY_BRIDGE(battle_scene_bridge_lifecycle_fixture(&app.scene, &cell, &goal, &e));
    if (failures) return 1;
    app.zoom = 1.5;
    home();
    int x, y;
    VERIFY_BRIDGE(test_unit_point(1, &x, &y));
    VERIFY_BRIDGE(test_unit_point(2, &x, &y));
    uint32_t part = b->bridge_at[cell] - 1;
    VERIFY_BRIDGE(ra_battle_command_add(b, 1, 1, goal, &e));
    VERIFY_BRIDGE(ra_battle_bridge_event_add(b, 5, RA_EVENT_BRIDGE_HIT, cell, &e));
    VERIFY_BRIDGE(ra_battle_bridge_event_add(b, 12, RA_EVENT_BRIDGE_HIT, cell, &e));
    VERIFY_BRIDGE(ra_battle_bridge_event_add(b, 120, RA_EVENT_BRIDGE_REPAIR, cell, &e));
    VERIFY_BRIDGE(ra_battle_command_add(b, 121, 1, goal, &e));
    snprintf(path, sizeof(path), "%s/bridge-intact.bmp", directory);
    VERIFY_BRIDGE(snapshot(path));
    while (b->tick < 5) step();
    VERIFY_BRIDGE(b->bridge_parts[part].frame == (b->bridge_parts[part].axis == 1 ? 6u : 15u) && b->units[1].health);
    snprintf(path, sizeof(path), "%s/bridge-damaged.bmp", directory);
    VERIFY_BRIDGE(snapshot(path));
    while (b->tick < 12) step();
    VERIFY_BRIDGE(b->bridge_parts[part].frame == 255 && !b->units[1].health && b->bridge_falls == 1);
    VERIFY_BRIDGE(!ra_battle_passable(b, cell + 512 * 512) && !b->occupied[cell + 512 * 512]);
    cell_point(cell + 512 * 512, &x, &y);
    uint32_t picked = 0;
    VERIFY_BRIDGE(!ground_cell(x, y - 58, &picked) || picked != cell + 512 * 512);
    snprintf(path, sizeof(path), "%s/bridge-destroyed.bmp", directory);
    VERIFY_BRIDGE(snapshot(path));
    while (b->tick < 120) step();
    VERIFY_BRIDGE(ra_battle_passable(b, cell + 512 * 512) && !b->units[1].health && b->bridge_repaired > 0);
    cell_point(cell + 512 * 512, &x, &y);
    VERIFY_BRIDGE(ground_cell(x, y - 58, &picked) && picked == cell + 512 * 512);
    snprintf(path, sizeof(path), "%s/bridge-repaired.bmp", directory);
    VERIFY_BRIDGE(snapshot(path));
    while (b->tick < 900) step();
    VERIFY_BRIDGE(b->units[0].health && b->units[0].cell == goal && b->bridge_falls == 1);
    home();
    unit_visibility arrived = test_unit_visibility(&b->units[0]);
    VERIFY_BRIDGE(arrived.expected && arrived.visible == arrived.expected);
    snprintf(path, sizeof(path), "%s/bridge-arrived.bmp", directory);
    VERIFY_BRIDGE(snapshot(path));
    snprintf(path, sizeof(path), "%s/bridge-lifecycle.rpl", directory);
    VERIFY_BRIDGE(replay_save(path) && replay_load(path));
    while (b->tick < app.replay_end) step();
    uint8_t digest[20];
    ra_battle_hash(b, digest);
    VERIFY_BRIDGE(!memcmp(digest, app.expected, 20));
    printf("{\"checks\":%u,\"failures\":%u,\"simulation_version\":%u,\"snapshots\":5,\"bridge_falls\":%u,\"original_bridge_art\":true}\n", checks, failures,
           RA_BATTLE_VERSION, b->bridge_falls);
    return failures ? 1 : 0;
#undef VERIFY_BRIDGE
}
static int structures_self_test(const char *directory)
{
    ra_error error = {0};
    ra_battle *b = &app.scene.battle;
    uint32_t target = 0, checks = 0, failures = 0;
    char path[32768];
    uint8_t trace[900][20], digest[20];
#define VERIFY_STRUCTURE(value)                                                                                                                                \
    do                                                                                                                                                         \
    {                                                                                                                                                          \
        ++checks;                                                                                                                                              \
        if (!(value))                                                                                                                                          \
        {                                                                                                                                                      \
            ++failures;                                                                                                                                        \
            fprintf(stderr, "structure window line %d: %s\n", __LINE__, #value);                                                                               \
        }                                                                                                                                                      \
    } while (0)
    VERIFY_STRUCTURE(battle_scene_base_fixture(&app.scene, &target, &error));
    if (failures) return 1;
    app.zoom = 1.25;
    memset(app.selected, 0, sizeof(app.selected));
    app.selected[6] = app.selected[7] = true;
    base_home();
    test_key('P', 0);
    for (uint32_t i = 0; i < 6; ++i) VERIFY_STRUCTURE(!app.selected[i]);
    VERIFY_STRUCTURE(app.selected[6] && app.selected[7]);
    for (uint32_t i = 0; i < 6; ++i)
    {
        const ra_voxel_image *image = battle_scene_structure_sprite(&app.scene, &b->units[i], &error);
        VERIFY_STRUCTURE(image && image->drawn_pixels > 1000);
        int x, y;
        VERIFY_STRUCTURE(test_unit_point(i + 1, &x, &y));
    }
    uint32_t output_before, drain, output_after;
    ra_battle_power(b, 2, &output_before, &drain);
    VERIFY_STRUCTURE(output_before > 0);
    snprintf(path, sizeof(path), "%s/base-intact.bmp", directory);
    VERIFY_STRUCTURE(snapshot(path));
    int x = 0, y = 0;
    VERIFY_STRUCTURE(test_unit_point(target, &x, &y));
    test_click(x, y, 0, false);
    VERIFY_STRUCTURE(b->command_count == 2 && b->commands[0].target == target && b->commands[1].target == target);
    bool damaged = false, destroyed = false;
    for (unsigned tick = 0; tick < 900; ++tick)
    {
        step();
        ra_battle_hash(b, trace[tick]);
        ra_battle_unit *plant = &b->units[target - 1];
        if (!damaged && plant->health && plant->health * 2 <= b->types[plant->type].strength)
        {
            snprintf(path, sizeof(path), "%s/base-damaged.bmp", directory);
            VERIFY_STRUCTURE(snapshot(path));
            damaged = true;
        }
        if (!destroyed && !plant->health)
        {
            snprintf(path, sizeof(path), "%s/base-destroyed.bmp", directory);
            VERIFY_STRUCTURE(snapshot(path));
            destroyed = true;
        }
    }
    VERIFY_STRUCTURE(damaged && destroyed);
    const ra_battle_unit *plant = &b->units[target - 1];
    const ra_battle_type *definition = &b->types[plant->type];
    for (uint32_t row = 0; row < definition->foundation_height; ++row)
        for (uint32_t column = 0; column < definition->foundation_width; ++column) VERIFY_STRUCTURE(!b->occupied[plant->cell + row * b->width + column]);
    ra_battle_power(b, 2, &output_after, &drain);
    VERIFY_STRUCTURE(output_after < output_before);
    snprintf(path, sizeof(path), "%s/building-combat.rpl", directory);
    VERIFY_STRUCTURE(replay_save(path) && replay_load(path));
    while (b->tick < app.replay_end)
    {
        step();
        ra_battle_hash(b, digest);
        VERIFY_STRUCTURE(b->tick <= 900 && !memcmp(digest, trace[b->tick - 1], 20));
    }
    VERIFY_STRUCTURE(!memcmp(digest, app.expected, 20));
    printf("{\"checks\":%u,\"failures\":%u,\"paired_steps\":900,\"original_buildings\":6,\"destroyed\":%s,\"power_before\":%u,\"power_after\":%u,\"simulation_"
           "version\":%u}\n",
           checks, failures, destroyed ? "true" : "false", output_before, output_after, RA_BATTLE_VERSION);
    return failures ? 1 : 0;
#undef VERIFY_STRUCTURE
}
static int scenario_self_test(const char *directory)
{
    unsigned checks = 0, failures = 0;
    char path[32768];
    ra_battle *b = &app.scene.battle;
    uint8_t trace[30][20], digest[20];
#define VERIFY_SCENARIO(value)                                                                                                                                 \
    do                                                                                                                                                         \
    {                                                                                                                                                          \
        ++checks;                                                                                                                                              \
        if (!(value))                                                                                                                                          \
        {                                                                                                                                                      \
            ++failures;                                                                                                                                        \
            fprintf(stderr, "scenario window line %d: %s\n", __LINE__, #value);                                                                                \
        }                                                                                                                                                      \
    } while (0)
    VERIFY_SCENARIO(app.scene.scenario && app.scene.structure_count > 0 && app.scene.house_count > 0);
    bool found = false;
    memset(app.selected, 0, sizeof(app.selected));
    for (uint32_t i = 0; i < b->count && !found; ++i)
    {
        const ra_battle_unit *unit = &b->units[i];
        if (!unit->health || !b->types[unit->type].structure) continue;
        int x, y;
        battle_unit_pixel(&app.scene, unit, &x, &y);
        if (x < 128 || y < 128 || x >= app.scene.ground.width - 128 || y >= app.scene.ground.height - 128) continue;
        center_at(x, y);
        if (!test_unit_point(unit->id, &x, &y)) continue;
        test_click(x, y, 0, false);
        VERIFY_SCENARIO(app.selected[i]);
        found = true;
    }
    VERIFY_SCENARIO(found);
    snprintf(path, sizeof(path), "%s/scenario-native.bmp", directory);
    VERIFY_SCENARIO(snapshot(path));
    for (uint32_t tick = 0; tick < 30; ++tick)
    {
        step();
        ra_battle_hash(b, trace[tick]);
    }
    snprintf(path, sizeof(path), "%s/scenario-native.rpl", directory);
    VERIFY_SCENARIO(replay_save(path) && replay_load(path));
    while (b->tick < app.replay_end)
    {
        step();
        ra_battle_hash(b, digest);
        VERIFY_SCENARIO(b->tick <= 30 && !memcmp(digest, trace[b->tick - 1], 20));
    }
    VERIFY_SCENARIO(!memcmp(digest, app.expected, 20));
    printf("{\"checks\":%u,\"failures\":%u,\"structures\":%zu,\"houses\":%u,\"pending_objects\":%zu,\"paired_steps\":30,\"script_runtime\":false}\n", checks,
           failures, app.scene.structure_count, app.scene.house_count, app.scene.issue_count);
    return failures ? 1 : 0;
#undef VERIFY_SCENARIO
}

static int campaign_self_test(const char *directory)
{
    ra_battle *b = &app.scene.battle;
    ra_error error = {0};
    uint32_t checks = 0, failures = 0, frames = 0, paired = 0;
    char path[2048];
    uint8_t (*trace)[20] = calloc(960, 20), digest[20];
#define VERIFY_CAMPAIGN(x)                                                                                                                                     \
    do                                                                                                                                                         \
    {                                                                                                                                                          \
        ++checks;                                                                                                                                              \
        if (!(x))                                                                                                                                              \
        {                                                                                                                                                      \
            ++failures;                                                                                                                                        \
            fprintf(stderr, "campaign window %d: %s (%s)\n", __LINE__, #x, error.message);                                                                     \
            goto finish_campaign;                                                                                                                              \
        }                                                                                                                                                      \
    } while (0)
    VERIFY_CAMPAIGN(trace && b->campaign && b->economy);
    for (uint32_t i = 0; i < b->count; ++i)
    {
        const ra_battle_unit *u = &b->units[i];
        if (!b->types[u->type].infantry) continue;
        const ra_voxel_image *image = battle_scene_infantry_sprite(&app.scene, u, &error);
        VERIFY_CAMPAIGN(image && image->max_x > image->min_x);
        ++frames;
    }
    for (uint32_t i = 0; i < 900; ++i)
    {
        ra_battle_step(b);
        if (!app.test_probe) ra_battle_hash(b, trace[i]);
    }
    VERIFY_CAMPAIGN(b->campaign->state.fired > 0 && !b->campaign->state.input_locked && !b->campaign->state.outcome);
    uint32_t player = 0;
    for (uint32_t i = 0; i < b->count; ++i)
        if (b->units[i].health && b->units[i].team == 1 && b->types[b->units[i].type].infantry)
        {
            player = i + 1;
            break;
        }
    VERIFY_CAMPAIGN(player);
    memset(app.selected, 0, sizeof(app.selected));
    app.selected[player - 1] = true;
    home();
    int x, y;
    battle_unit_pixel(&app.scene, &b->units[player - 1], &x, &y);
    fprintf(stderr, "player %u %s cell=%u,%u pixel=%d,%d pan=%d,%d viewport=%d,%d goal=%u,%u order=%u script=%u path=%u/%u\n", player,
            b->types[b->units[player - 1].type].id, b->units[player - 1].cell % b->width, b->units[player - 1].cell / b->width, x, y, app.pan_x, app.pan_y,
            app.width, app.height, b->units[player - 1].goal % b->width, b->units[player - 1].goal / b->width, b->units[player - 1].order,
            b->units[player - 1].script_team, b->units[player - 1].path_cursor, b->units[player - 1].path_count);
    snprintf(path, sizeof(path), "%s/campaign-view.bmp", directory);
    VERIFY_CAMPAIGN(snapshot(path));
    VERIFY_CAMPAIGN(test_unit_point(player, &x, &y));
    test_click(x, y, 0, false);
    VERIFY_CAMPAIGN(app.selected[player - 1]);
    for (uint32_t i = 900; i < 960; ++i)
    {
        ra_battle_step(b);
        if (!app.test_probe) ra_battle_hash(b, trace[i]);
    }
    snprintf(path, sizeof(path), "%s/campaign-native.bmp", directory);
    VERIFY_CAMPAIGN(snapshot(path));
    snprintf(path, sizeof(path), "%s/campaign.json", directory);
    VERIFY_CAMPAIGN(battle_scene_campaign_report(&app.scene, path, &error));
    if (app.test_probe) goto finish_campaign;
    snprintf(path, sizeof(path), "%s/campaign.rpl", directory);
    VERIFY_CAMPAIGN(replay_save(path) && replay_load(path));
    while (b->tick < app.replay_end)
    {
        ra_battle_step(b);
        ra_battle_hash(b, digest);
        VERIFY_CAMPAIGN(!memcmp(digest, trace[b->tick - 1], 20));
        ++paired;
    }
    VERIFY_CAMPAIGN(!memcmp(digest, app.expected, 20));
finish_campaign:
    ra_battle_hash(b, digest);
    char state_hex[41];
    ra_hex(digest, 20, state_hex);
    printf("{\"checks\":%u,\"failures\":%u,\"infantry_images\":%u,\"paired_steps\":%u,\"state_sha1\":\"%s\",\"complete_original_mission\":false}\n", checks,
           failures, frames, paired, state_hex);
    free(trace);
    return failures ? 1 : 0;
#undef VERIFY_CAMPAIGN
}
static int mcv_self_test(const char *directory)
{
    ra_battle *b = &app.scene.battle;
    ra_error error = {0};
    uint32_t failures = 0;
    uint8_t before[20], after[20];
    char path[2048];
    memset(app.selected, 0, sizeof(app.selected));
    app.selected[0] = true;
    home();
    const ra_voxel_image *image = battle_scene_sprite(&app.scene, &b->units[0], &error);
    if (!image || image->max_x <= image->min_x) ++failures;
    snprintf(path, sizeof(path), "%s/mcv-before.bmp", directory);
    if (!snapshot(path)) ++failures;
    test_key('D', 0);
    ra_battle_step(b);
    if (!b->types[b->units[0].type].structure || b->count != 2) ++failures;
    image = battle_scene_structure_sprite(&app.scene, &b->units[0], &error);
    if (!image || !image->pixels) ++failures;
    snprintf(path, sizeof(path), "%s/mcv-after.bmp", directory);
    if (!snapshot(path)) ++failures;
    ra_battle_hash(b, before);
    snprintf(path, sizeof(path), "%s/mcv.rpl", directory);
    if (!replay_save(path) || !replay_load(path)) ++failures;
    ra_battle_step(b);
    ra_battle_hash(b, after);
    if (memcmp(before, after, 20)) ++failures;
    printf("{\"failures\":%u,\"paired_steps\":1,\"original_assets\":true}\n", failures);
    return failures ? 1 : 0;
}
static int economy_self_test(const char *directory)
{
    unsigned checks = 0, failures = 0, paired = 0;
    ra_battle *b = &app.scene.battle;
    uint8_t (*trace)[20] = calloc(16000, 20), digest[20];
    ra_error error = {0};
    char path[2048];
#define VERIFY_ECON(x)                                                                                                                                         \
    do                                                                                                                                                         \
    {                                                                                                                                                          \
        ++checks;                                                                                                                                              \
        if (!(x))                                                                                                                                              \
        {                                                                                                                                                      \
            ++failures;                                                                                                                                        \
            fprintf(stderr, "native economy line %d: %s (%s)\n", __LINE__, #x, error.message);                                                                 \
            goto finish;                                                                                                                                       \
        }                                                                                                                                                      \
    } while (0)
#define ADVANCE_ECON()                                                                                                                                         \
    do                                                                                                                                                         \
    {                                                                                                                                                          \
        VERIFY_ECON(b->tick < 16000);                                                                                                                          \
        ra_battle_step(b);                                                                                                                                     \
        if (!app.test_probe) ra_battle_hash(b, trace[b->tick - 1]);                                                                                            \
    } while (0)
    VERIFY_ECON(trace && b->economy && b->count == 2);
    static const char *allied[] = {"GAPOWR", "GAPILE", "GAREFN", "GAWEAP", "GAAIRC", "GATECH"};
    static const char *soviet[] = {"NAPOWR", "NAHAND", "NAREFN", "NAWEAP", "NARADR", "NATECH"};
    const char **ids = app.scene.economy_allied ? allied : soviet;
    VERIFY_ECON(!ra_economy_available(b, 1, ra_economy_type(b, ids[3])));
    for (uint32_t n = 0; n < 6; ++n)
    {
        uint32_t type = ra_economy_type(b, ids[n]), row;
        for (row = 0; row < 16 && economy_row(row) != type; ++row)
        {
        }
        fprintf(stderr, "building %s at tick %u\n", ids[n], b->tick);
        fflush(stderr);
        VERIFY_ECON(row < 16 && ra_economy_available(b, 1, type));
        test_click(app.width - 120, 118 + (int)row * 48 + 12, 0, false);
        ADVANCE_ECON();
        ra_econ_queue *q = &b->economy->state.houses[0].queues[0];
        VERIFY_ECON(q->count && q->types[0] == type);
        while (q->progress < b->economy->types[type].ticks * 1000)
        {
            ADVANCE_ECON();
        }
        test_click(app.width - 120, 118 + (int)row * 48 + 12, 0, false);
        VERIFY_ECON(app.place_type_plus_one == type + 1);
        uint32_t chosen = UINT32_MAX, best = UINT32_MAX;
        int bx = (int)(b->units[0].cell % b->width), by = (int)(b->units[0].cell / b->width);
        for (int dy = -24; dy <= 24; ++dy)
            for (int dx = -24; dx <= 24; ++dx)
            {
                int x = bx + dx, y = by + dy;
                if (x < 0 || y < 0 || x >= (int)b->width || y >= (int)b->height) continue;
                uint32_t cell = (uint32_t)y * b->width + (uint32_t)x, score = (uint32_t)(abs(dx) + abs(dy));
                if (score < best && ra_economy_placeable(b, 1, type, cell))
                {
                    chosen = cell;
                    best = score;
                }
            }
        VERIFY_ECON(chosen != UINT32_MAX);
        int x, y;
        cell_point(chosen, &x, &y);
        if (x < 0 || x >= app.width - 260 || y < 58 || y >= app.height + 58)
        {
            center_at((int)(((int)(chosen % b->width) - (int)(chosen / b->width)) * 30 + app.scene.ground.origin_x + 30),
                      (int)(((int)(chosen % b->width) + (int)(chosen / b->width) - b->tiles[chosen].height) * 15 + app.scene.ground.origin_y + 15));
            cell_point(chosen, &x, &y);
        }
        uint32_t before = b->count;
        test_click(x, y - 58, 0, false);
        ADVANCE_ECON();
        VERIFY_ECON(b->count > before && b->economy->state.houses[0].built == n + 1);
    }
    uint32_t type = ra_economy_type(b, app.scene.economy_allied ? "MTNK" : "HTNK"), row;
    for (row = 0; row < 16 && economy_row(row) != type; ++row)
    {
    }
    VERIFY_ECON(row < 16 && ra_economy_available(b, 1, type));
    test_click(app.width - 120, 118 + (int)row * 48 + 12, 0, false);
    ADVANCE_ECON();
    while (b->economy->state.houses[0].queues[1].count)
    {
        ADVANCE_ECON();
    }
    for (uint32_t n = 0; n < 900; ++n)
    {
        ADVANCE_ECON();
    }
    if (!b->economy->state.houses[0].earned)
    {
        uint32_t miner = 0, refinery = 0;
        for (uint32_t i = 0; i < b->count; ++i)
        {
            if (b->economy->types[b->units[i].type].harvester && b->economy->state.miners[i].ore + b->economy->state.miners[i].gems) miner = i + 1;
            if (b->economy->types[b->units[i].type].refinery) refinery = i + 1;
        }
        /* 原地图矿藏可能稀疏；提交真实的部分载货返厂命令，不改变容量或地图矿量。 */
        VERIFY_ECON(miner && refinery && ra_economy_command(b, b->tick + 1, miner, RA_ECON_RETURN, refinery, &error));
        while (!b->economy->state.houses[0].earned)
        {
            ADVANCE_ECON();
        }
    }
    for (uint32_t i = 0; i < b->count; ++i)
    {
        if (!b->economy->types[b->units[i].type].harvester) continue;
        const ra_battle_unit *u = &b->units[i];
        const ra_econ_miner *m = &b->economy->state.miners[i];
        fprintf(stderr, "miner %s id=%u cell=%u,%u next=%u,%u goal=%u,%u order=%u active=%u ore=%u gems=%u refinery=%u path=%u/%u track=%u retry=%u\n",
                b->types[u->type].id, u->id, u->cell % b->width, u->cell / b->width, u->next % b->width, u->next / b->width, u->goal % b->width,
                u->goal / b->width, u->order, m->active, m->ore, m->gems, m->refinery, u->path_cursor, u->path_count, u->track_active, u->retry);
    }
    VERIFY_ECON(b->economy->state.houses[0].earned > 0);
    VERIFY_ECON(b->economy->state.houses[0].produced >= 2);
    VERIFY_ECON(b->economy->state.houses[0].credits + b->economy->state.houses[0].spent == 10000 + b->economy->state.houses[0].earned);
    for (uint32_t i = 0; i < b->count; ++i)
    {
        const ra_voxel_image *image = b->types[b->units[i].type].structure ? battle_scene_structure_sprite(&app.scene, &b->units[i], &error)
                                                                           : battle_scene_sprite(&app.scene, &b->units[i], &error);
        VERIFY_ECON(image && image->pixels && image->max_x > image->min_x);
    }
    base_home();
    snprintf(path, sizeof(path), "%s/economy-rules.json", directory);
    VERIFY_ECON(battle_scene_economy_report(&app.scene, path, &error));
    snprintf(path, sizeof(path), "%s/economy-native.bmp", directory);
    VERIFY_ECON(snapshot(path));
    if (app.test_probe) goto finish;
    snprintf(path, sizeof(path), "%s/economy.rpl", directory);
    VERIFY_ECON(replay_save(path) && replay_load(path));
    while (b->tick < app.replay_end)
    {
        ra_battle_step(b);
        ra_battle_hash(b, digest);
        VERIFY_ECON(!memcmp(digest, trace[b->tick - 1], 20));
        ++paired;
    }
    VERIFY_ECON(!memcmp(digest, app.expected, 20));
finish:
    if (b->economy)
    {
        char state[41];
        ra_battle_hash(b, digest);
        ra_hex(digest, 20, state);
        printf("{\"checks\":%u,\"failures\":%u,\"paired_steps\":%u,\"side\":\"%s\",\"objects\":%u,\"built\":%u,\"produced\":%u,\"spent\":%llu,\"earned\":%llu,"
               "\"credits\":%llu,\"version\":%u,\"state_sha1\":\"%s\",\"complete_game\":false}\n",
               checks, failures, paired, app.scene.economy_allied ? "allied" : "soviet", b->count, b->economy->state.houses[0].built,
               b->economy->state.houses[0].produced, (unsigned long long)b->economy->state.houses[0].spent,
               (unsigned long long)b->economy->state.houses[0].earned, (unsigned long long)b->economy->state.houses[0].credits, RA_BATTLE_VERSION, state);
    }
    free(trace);
    return failures ? 1 : 0;
#undef ADVANCE_ECON
#undef VERIFY_ECON
}
static int app_main(int argc, char **argv)
{
    WNDCLASSW type = {0};
    MSG msg;
    ra_error e = {0};
    const char *test = NULL, *map = "MP05MW.map";
    int result = 0;
    bool test_layers = false, test_bridges = false, bridge_demo = false, base_demo = false, test_structures = false, test_scenario = false,
         test_economy = false, test_campaign = false, test_mcv = false;
    size_t selected = 0;
    app.original = "H:/开发/运行版本/原版1.006";
    app.zoom = 1.0;
    app.paused = app.loading = true;
    for (int i = 1; i < argc; ++i)
    {
        if (i + 1 < argc && !strcmp(argv[i], "--original")) app.original = argv[++i];
        else if (!strcmp(argv[i], "--campaign"))
        {
            app.scene.campaign_mode = app.scene.scenario = app.scene.economy_allied = true;
            map = "all01t.map";
        }
        else if (!strcmp(argv[i], "--mcv-demo"))
        {
            app.scene.mcv_mode = app.scene.economy_mode = true;
            map = "MP17T6.map";
        }
        else if (!strcmp(argv[i], "--scenario")) app.scene.scenario = true;
        else if (!strcmp(argv[i], "--base-demo")) base_demo = true;
        else if (!strcmp(argv[i], "--economy-demo")) app.scene.economy_mode = true;
        else if (!strcmp(argv[i], "--allied")) app.scene.economy_allied = true;
        else if (!strcmp(argv[i], "--probe")) app.test_probe = true;
        else if (i + 1 < argc && !strcmp(argv[i], "--self-test-campaign"))
        {
            test = argv[++i];
            test_campaign = app.scene.campaign_mode = app.scene.scenario = app.scene.economy_allied = true;
            map = "all01t.map";
        }
        else if (i + 1 < argc && !strcmp(argv[i], "--self-test-mcv"))
        {
            test = argv[++i];
            test_mcv = app.scene.economy_mode = app.scene.mcv_mode = true;
            map = "MP17T6.map";
        }
        else if (i + 1 < argc && !strcmp(argv[i], "--self-test-economy"))
        {
            test = argv[++i];
            test_economy = app.scene.economy_mode = true;
        }
        else if (!strcmp(argv[i], "--bridge-demo"))
        {
            bridge_demo = true;
            map = "MP06T2.map";
        }
        else if (i + 1 < argc && !strcmp(argv[i], "--self-test")) test = argv[++i];
        else if (i + 1 < argc && !strcmp(argv[i], "--self-test-bridges"))
        {
            test = argv[++i];
            test_bridges = true;
        }
        else if (i + 1 < argc && !strcmp(argv[i], "--self-test-layers"))
        {
            test = argv[++i];
            test_layers = true;
        }
        else if (i + 1 < argc && !strcmp(argv[i], "--self-test-structures"))
        {
            test = argv[++i];
            test_structures = true;
        }
        else if (i + 1 < argc && !strcmp(argv[i], "--self-test-scenario"))
        {
            test = argv[++i];
            test_scenario = app.scene.scenario = true;
        }
        else if (i + 1 < argc && !strcmp(argv[i], "--map")) map = argv[++i];
        else return 2;
    }
    if (test_economy)
    {
        fprintf(stderr, "economy startup\n");
        fflush(stderr);
    }
    SetProcessDPIAware();
    QueryPerformanceFrequency(&app.frequency);
    clock_reset();
    type.style = CS_DBLCLKS;
    type.lpfnWndProc = window_proc;
    type.hInstance = GetModuleHandleW(NULL);
    type.lpszClassName = L"RA2PureCBattle";
    type.hCursor = LoadCursorW(NULL, IDC_ARROW);
    if (!RegisterClassW(&type)) return 1;
    HWND window = CreateWindowW(type.lpszClassName, L"红色警戒2 · 原版 1.006 最小战场 · 纯 C", WS_OVERLAPPEDWINDOW | WS_CLIPCHILDREN, CW_USEDEFAULT,
                                CW_USEDEFAULT, 1360, 920, NULL, NULL, type.hInstance, NULL);
    if (!window) return 1;
    layout();
    if (!battle_scene_open(&app.scene, app.original, &e))
    {
        error_message(&e);
        result = 1;
        goto done;
    }
    {
        ra_resource keyboard = {0};
        bool ok = ra_vfs_read(&app.scene.voxels.vfs, "keyboard.ini", &keyboard, &e) && ra_ini_parse(&app.keyboard, keyboard.view, keyboard.source, &e);
        ra_resource_close(&keyboard);
        if (!ok)
        {
            error_message(&e);
            result = 1;
            goto done;
        }
    }
    for (size_t i = 0; i < app.scene.maps.source_count; ++i)
    {
        wchar_t label[128];
        wide(app.scene.maps.sources[i].name, label, 128);
        SendMessageW(app.combo, CB_ADDSTRING, 0, (LPARAM)label);
        if (ra_equal(app.scene.maps.sources[i].name, map)) selected = i;
    }
    SendMessageW(app.combo, CB_SETCURSEL, selected, 0);
    if (test_economy)
    {
        fprintf(stderr, "resources opened\n");
        fflush(stderr);
    }
    map_load(selected);
    if (test_economy)
    {
        fprintf(stderr, "map loaded %s\n", e.message);
        fflush(stderr);
    }
    if (app.scene.economy_mode)
    {
        if (!app.scene.battle.economy)
        {
            result = 1;
            goto done;
        }
        base_home();
        message(L"基地验证场：10000 资金和建造厂；侧栏依次建造电厂、兵营、矿厂、战车工厂。原版地图矿藏，矿厂赠送矿车。 ");
    }
    if (bridge_demo)
    {
        uint32_t cell = 0, goal = 0;
        ra_battle *b = &app.scene.battle;
        if (!battle_scene_bridge_lifecycle_fixture(&app.scene, &cell, &goal, &e) || !ra_battle_bridge_event_add(b, 90, RA_EVENT_BRIDGE_HIT, cell, &e) ||
            !ra_battle_bridge_event_add(b, 180, RA_EVENT_BRIDGE_HIT, cell, &e) || !ra_battle_bridge_event_add(b, 300, RA_EVENT_BRIDGE_REPAIR, cell, &e) ||
            !ra_battle_command_add(b, 301, 1, goal, &e))
        {
            error_message(&e);
            result = 1;
            goto done;
        }
        app.zoom = 1.5;
        home();
        message(L"桥梁演示：6 秒损坏，12 秒断裂，20 秒修复；可暂停或单步查看。 ");
    }
    if (base_demo)
    {
        uint32_t target;
        if (!battle_scene_base_fixture(&app.scene, &target, &e))
        {
            error_message(&e);
            result = 1;
            goto done;
        }
        memset(app.selected, 0, sizeof(app.selected));
        app.selected[6] = app.selected[7] = true;
        app.zoom = 1.25;
        base_home();
        message(L"建筑验证场：六座盟苏建筑，两个玩家坦克。左键选择，左键敌方建筑攻击；建筑损毁后占地恢复通行。 ");
    }
    ShowWindow(window, test ? SW_SHOWNOACTIVATE : SW_SHOW);
    UpdateWindow(window);
    if (test)
        result = test_campaign     ? campaign_self_test(test)
                 : test_mcv        ? mcv_self_test(test)
                 : test_economy    ? economy_self_test(test)
                 : test_scenario   ? scenario_self_test(test)
                 : test_structures ? structures_self_test(test)
                 : test_bridges    ? bridges_self_test(test)
                 : test_layers     ? layers_self_test(test)
                                   : self_test(test);
    else
    {
        paused(false);
        while (GetMessageW(&msg, NULL, 0, 0) > 0)
        {
            TranslateMessage(&msg);
            DispatchMessageW(&msg);
        }
    }
done:
    if (IsWindow(window)) DestroyWindow(window);
    ra_ini_close(&app.keyboard);
    battle_scene_close(&app.scene);
    free(app.pixels);
    free(app.picked);
    free(app.heights);
    DeleteObject(app.font);
    return result;
}
#include "entry.h"
