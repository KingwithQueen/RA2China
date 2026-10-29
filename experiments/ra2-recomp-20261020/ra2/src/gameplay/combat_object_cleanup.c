#include "combat_control_list_end.h"
#include "combat_control_list_link.h"
#include "combat_control_list_read.h"
#include "combat_control_walk.h"
#include "combat_control_switch.h"
#include "combat_control_transition.h"
#include "combat_control_set.h"
#include "combat_control_tail.h"
#include "combat_control_dispatch.h"
#include "combat_reference_count.h"
#include "combat_reference_exit.h"
#include "combat_reference_list.h"
#include "combat_reference_controller.h"
#include "combat_reference_prefix.h"
#include "combat_object_cleanup_base.h"
#include "combat_object_cleanup_members.h"
#include "combat_object_cleanup_tables.h"
#include "combat_object_cleanup.h"

void ra2_cleanup_object_registry(const Ra2ObjectCleanupServices *s)
{
    s->begin(s->context);
    if (s->find(s->context) == -1) return;
    if (!s->can_remove(s->context)) return;
    if (!s->shrink_has_following(s->context)) return;
    while (s->shift_next(s->context)) {}
}

void ra2_cleanup_object_tables(const Ra2ObjectTablesCleanupServices *s)
{
    for (uint32_t table = 0; table < 4; ++table) {
        s->select_table(s->context, table);
        ra2_cleanup_object_registry(&s->registry);
    }
}

void ra2_cleanup_object_members(const Ra2ObjectMembersCleanupServices *s)
{
    s->begin(s->context);
    for (uint32_t step = 0; step < 4; ++step) s->member_step(s->context, step);
    if (s->restore_and_has_optional(s->context)) {
        s->cleanup_optional(s->context);
        s->clear_optional(s->context);
    }
    s->cleanup_abstract(s->context);
}

void ra2_detach_object_association(const Ra2ObjectBaseCleanupServices *s)
{
    uint32_t owner = s->association_owner(s->context);
    if (owner) {
        /* 必须先清关联对象，再清成员；两处可能重叠，不重新读取owner。 */
        s->clear_owner_link(s->context, owner);
        s->clear_member_link(s->context);
    }
}

void ra2_reset_abstract_tables(const Ra2ObjectBaseCleanupServices *s)
{
    static const uint32_t tables[] = {0x79ADD8, 0x79ADBC, 0x79ADB4, 0x79ADAC};
    for (uint32_t i = 0; i < 4; ++i) s->write_abstract_table(s->context, i * 4, tables[i]);
}

uint32_t ra2_check_reference_prefix(const Ra2ReferencePrefixServices *s)
{
    s->begin(s->context);
    if (!s->active(s->context)) return RA2_REFERENCE_EARLY;
    if (!s->manager_matches(s->context)) return RA2_REFERENCE_EARLY;
    if (!s->has_reference(s->context)) return RA2_REFERENCE_EARLY;
    if (!s->first_stamp_matches(s->context)) return RA2_REFERENCE_INVALID;
    if (!s->second_stamp_matches(s->context)) return RA2_REFERENCE_INVALID;
    if (s->is_dead(s->context)) return RA2_REFERENCE_INVALID;
    return RA2_REFERENCE_CONTINUE;
}

void ra2_cleanup_reference_controller(const Ra2ReferenceControllerServices *s)
{
    if (!s->has_controller(s->context)) return;
    if (!s->owns_reference(s->context)) return;
    if (s->needs_cancel(s->context)) s->cancel(s->context);
    s->release_current(s->context);
    static const uint32_t offsets[] = {0xC0, 0xBC, 0xB4, 0xB8, 0x90, 0x98, 0x9C};
    for (uint32_t i = 0; i < 7; ++i) s->clear_current_field(s->context, offsets[i]);
    s->clear_reference_link(s->context);
}

void ra2_cleanup_reference_list(const Ra2ReferenceListServices *s)
{
    if (s->begin_positive(s->context)) {
        s->begin_items(s->context);
        do { s->release_current(s->context); } while (s->clear_and_advance(s->context));
        s->end_items(s->context);
    }
    s->clear_field(s->context, 0xA8);
    s->write_state(s->context, 4);
    s->clear_field(s->context, 0x138);
    s->clear_field(s->context, 0x278);
    s->mark_dead(s->context);
    s->restore_counter(s->context);
}

void ra2_finish_reference_cleanup(const Ra2ReferenceExitServices *s,
    uint32_t clear_reference, uint32_t clear_manager)
{
    if (clear_reference) s->clear_field(s->context, 0);
    s->clear_field(s->context, 8);
    if (clear_manager) s->clear_field(s->context, 0xC);
    s->restore_and_return(s->context);
}

void ra2_decrement_reference_count(const Ra2ReferenceCountServices *s)
{
    uint32_t result = s->read_count(s->context) - 1u;
    s->set_result(s->context, result);
    s->write_count(s->context, result);
    if ((int32_t)result < 0) s->write_count(s->context, 0);
}

void ra2_dispatch_control_cleanup(const Ra2ControlDispatchServices *s)
{
    s->begin(s->context);
    s->call_first(s->context);
    if (s->needs_optional(s->context)) s->call_optional(s->context);
    s->call_last(s->context);
    if (s->has_callback(s->context)) s->call_callback(s->context);
    s->finish(s->context);
}

uint32_t ra2_clear_control_state_and_tail(const Ra2ControlTailServices *s)
{
    s->begin(s->context);
    s->call_first(s->context);
    s->clear_state(s->context);
    return s->restore_and_tail(s->context);
}

uint32_t ra2_set_control_state_and_tail(const Ra2ControlSetServices *s)
{
    s->begin(s->context);
    s->call_first(s->context);
    s->set_state(s->context);
    return s->restore_and_tail(s->context);
}

uint32_t ra2_transition_control_state(const Ra2ControlTransitionServices *s)
{
    s->begin(s->context);
    s->call_first(s->context);
    if (s->needs_change(s->context)) {
        s->clear_active(s->context);
        s->call_change(s->context);
        s->finish_change(s->context);
    }
    return s->restore_and_tail(s->context);
}

uint32_t ra2_switch_control_state(const Ra2ControlSwitchServices *s)
{
    s->begin(s->context);
    s->call_first(s->context);
    if (s->needs_change(s->context)) {
        s->call_change(s->context);
        s->clear_changed(s->context);
        s->activate_state(s->context);
    }
    return s->restore_and_tail(s->context);
}


void ra2_walk_control_states(const Ra2ControlWalkServices *s)
{
    s->begin(s->context);
    s->first(s->context);
    if (s->has_current(s->context)) {
        do {
            if (s->is_active(s->context) && s->type_matches(s->context)) s->change(s->context);
            /* 回调可能改动当前寄存器，原流程在取下一项前再检查一次。 */
            if (!s->has_current(s->context)) break;
            s->next(s->context);
        } while (s->backedge_and_continue(s->context));
    }
    s->finish(s->context);
}


void ra2_read_control_list_link(const Ra2ControlListReadServices *s)
{
    if (!s->has_source(s->context)) {
        s->clear_result(s->context);
    } else {
        s->read_link(s->context);
        /* 空链不读节点；普通节点返回时保留哨兵比较的标志。 */
        if (s->has_link(s->context) && s->is_sentinel(s->context)) s->clear_result(s->context);
    }
    s->finish(s->context);
}


void ra2_insert_control_link_before(Ra2ControlListLinkCursor *r, const Ra2ControlListLinkServices *s)
{
    r->value = s->read(s->context, r->current + 4);
    s->write(s->context, r->node, r->current);
    s->write(s->context, r->node + 4, r->value);
    s->write(s->context, r->current + 4, r->node);
    /* 节点可能重叠，必须在前三次写入后再读取插入节点的前链。 */
    r->current = s->read(s->context, r->node + 4);
    s->write(s->context, r->current, r->node);
}

void ra2_insert_control_link_after(Ra2ControlListLinkCursor *r, const Ra2ControlListLinkServices *s)
{
    s->write(s->context, r->node + 4, r->current);
    r->value = s->read(s->context, r->current);
    s->write(s->context, r->node, r->value);
    s->write(s->context, r->current, r->node);
    r->current = s->read(s->context, r->node);
    s->write(s->context, r->current + 4, r->node);
}

void ra2_detach_control_link(Ra2ControlListLinkCursor *r, const Ra2ControlListLinkServices *s)
{
    r->value = s->read(s->context, r->current + 4);
    r->node = s->read(s->context, r->current);
    s->write(s->context, r->value, r->node);
    /* 修改前节点后，当前节点的两条链也可能因别名改变，不能沿用旧值。 */
    r->value = s->read(s->context, r->current);
    r->node = s->read(s->context, r->current + 4);
    s->write(s->context, r->value + 4, r->node);
    s->write(s->context, r->current, r->current);
    s->write(s->context, r->current + 4, r->current);
}


void ra2_read_control_front(Ra2ControlListEndCursor *r, const Ra2ControlListEndServices *s)
{
    /* 此入口没有空源保护，先读链，再区分空链和哨兵。 */
    r->value = s->read(s->context, r->current);
    r->left = r->right = r->value; r->compared = 0;
    if (r->value) {
        r->right = s->read(s->context, r->value + 8); r->compared = 1;
        if (r->value == r->right) {
            r->value = r->left = r->right = 0; r->compared = 0;
        }
    }
}

void ra2_read_control_back(Ra2ControlListEndCursor *r, const Ra2ControlListEndServices *s)
{
    r->current = s->read(s->context, r->current + 4);
    uint32_t difference = r->current - s->read(s->context, r->current + 8);
    uint32_t negated = 0u - difference;
    /* NEG的借位经SBB形成全位掩码，使用无符号取负覆盖80000000。 */
    r->left = negated ? UINT32_MAX : 0; r->right = r->current; r->compared = 0;
    r->value = r->left & r->current;
}
