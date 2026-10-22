"""Clarify business names after preserving the handoff checkpoint; behavior remains original."""
from pathlib import Path
import json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v23'
assert json.loads((S/'parts/handoff-verified/validation.json').read_text(encoding='utf-8'))['passed']
p=R/'ra2/src/gameplay/ground_tube_state.h';t=p.read_text(encoding='utf-8')
t=t.replace('stop_object','request_object_clearance').replace('stop_self','request_self_clearance').replace('has_pending_navigation','goal_is_exit_cell').replace('避免停止回调改变链表','避免让路回调改变链表')
p.write_text(t,encoding='utf-8',newline='\n')
p=R/'ra2/src/runtime/ground_tube_state_bridge.c';t=p.read_text(encoding='utf-8')
t=t.replace('stop_object','request_object_clearance').replace('stop_self','request_self_clearance').replace('static int pending(', 'static int goal_is_exit_cell(').replace('enter,pending,','enter,goal_is_exit_cell,').replace('return MEM32(c->unit+0x494)!=c->cell;','return MEM32(c->unit+0x494)==c->cell;')
p.write_text(t,encoding='utf-8',newline='\n')
(R/'ra2/src/gameplay/ground_tube_state.c').write_text('''#include "ground_tube_state.h"

uint32_t ra2_ground_tube_exit(const Ra2TubeExitServices *services)
{
    void *context = services->context;
    uintptr_t object = services->exit_occupants(context);

    if (object) {
        /* 先复制出口对象链。让路请求可能修改原链表，不能边遍历边请求。 */
        services->begin_snapshot(context);
        do {
            services->append_snapshot(context, object);
            object = services->next_occupant(context, object);
        } while (object);

        /* 每次重读快照数量；类别不为1时必须再查一次，保留回调副作用。 */
        for (int32_t index = 0; index < services->snapshot_count(context); ++index) {
            object = services->snapshot_object(context, index);
            if (services->object_kind(context, object) == 1 ||
                services->object_kind(context, object) == 15) {
                if (!services->object_moving(context, object))
                    services->request_object_clearance(context, object);
            }
        }
        services->set_speed(context, 1);
        return services->end_snapshot(context);
    }

    /* 出口已空：落位、登记入格，再恢复任务与速度。目标判断是格指针相等。 */
    services->place_at_exit(context);
    services->enter_cell(context);
    if (services->goal_is_exit_cell(context))
        services->request_self_clearance(context);
    services->restore_mission(context);
    services->set_speed(context, 0);
    return services->face_next_connection(context);
}

Ra2TubeWaypointResult ra2_ground_tube_waypoint(int32_t distance, int32_t speed,
    const Ra2TubeWaypointServices *services)
{
    if (distance > speed)
        return RA2_TUBE_KEEP_STEP;

    /* 对齐到路点的回调可能改变结束标志，必须在回调后读取。 */
    services->advance_and_snap(services->context);
    return services->finished_after_snap(services->context)
        ? RA2_TUBE_EXIT : RA2_TUBE_NEXT_STEP;
}
''',encoding='utf-8',newline='\n')
(R/'ra2/src/gameplay/ground_handoff.c').write_text('''#include "ground_handoff.h"

unsigned ra2_ground_prepare_upper_layer(uint32_t cell_flags, int8_t cell_level,
    int32_t z, int32_t height_per_level)
{
    if (!(cell_flags & 0x100u))
        return 0;

    /* 原入口要求高度单位非零且除法可表示；有符号除法向零截断。 */
    int32_t divided = z / height_per_level;
    uint32_t difference = (uint32_t)divided - (uint32_t)(int32_t)cell_level;
    uint32_t absolute = difference & 0x80000000u ? 0u - difference : difference;
    return (int32_t)absolute > 2;
}
''',encoding='utf-8',newline='\n')
(R/'ra2/src/gameplay/ground_surface_class.c').write_text('''#include "ground_surface_class.h"

int ra2_ground_is_tube_entrance(int16_t connection, int32_t count, int32_t land)
{
    return connection >= 0 && connection < count && land == 10;
}

int ra2_ground_is_tile_family(int32_t tile, int32_t first)
{
    /* 上界采用原32位回绕，再进行有符号比较。 */
    return tile >= first && tile < (int32_t)((uint32_t)first + 14u);
}

int32_t ra2_ground_surface_support_height(const Ra2SurfaceSupportServices *services)
{
    void *context = services->context;
    int32_t height = services->base_height(context);

    /* 先计算坡面高度，再读取开关及对象链；计算回调可能改变二者。 */
    if (services->scan_objects(context)) {
        for (uintptr_t object = services->first_object(context); object;
             object = services->next_object(context, object)) {
            if (services->object_kind(context, object) == 6)
                return (int32_t)((uint32_t)height +
                    (uint32_t)services->support_height(context, object));
        }
    }
    if (services->fallback_support(context))
        height = (int32_t)((uint32_t)height + 85u);
    return height;
}
''',encoding='utf-8',newline='\n')
print('Clarified clearance requests, exit-cell equality, and business control flow')
