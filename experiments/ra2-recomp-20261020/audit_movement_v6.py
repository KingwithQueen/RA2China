"""逐帧相等之外，断言真实障碍、模板和预算调查实际发生的效果。"""
from pathlib import Path
import collections
import json

ROOT = Path(__file__).resolve().parent
STAGE = ROOT / 'evidence/movement-state-v6'


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def write(path, value):
    assert not path.exists(), path
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')


def rows(tag):
    return [json.loads(line) for line in (STAGE/'runs'/tag/'original/state.jsonl').open(encoding='utf-8')]


def states(records):
    return [r for r in records if r['kind']=='state']


def audits(records, stage):
    return [r for r in records if r['kind']=='movement-audit' and r['stage']==stage]


# 延续原版墙/闸/精确速度及受控预算断言；复用时只改变本批目录与运行标签。
source = (ROOT/'audit_movement_v4.py').read_text(encoding='utf-8')
source = source.replace("'evidence/movement-state-v4'", "'evidence/movement-state-v6'")
source = source.replace("'final-", "'schema8-")
source = source[:source.index('with (STAGE /')]
scope = {'__file__':str(ROOT/'audit_movement_v4.py'), '__name__':'audit_base'}
exec(compile(source, str(ROOT/'audit_movement_v4.py'), 'exec'), scope)
effect = scope['effect']

congestion = rows('schema8-congestion-01')
waits = audits(congestion, 8)
assert waits and {r['value'] for r in waits}=={0,1}
temporary = audits(congestion, 11)
assert temporary and all(r['value']==6 for r in temporary)
assert any(r['value']==2 for r in audits(congestion, 9))
effect['traffic_wait'] = dict(entries=len(waits), start_and_continue_observed=True)
effect['temporary_obstacle'] = dict(tag='schema8-congestion-01', entries=temporary,
    primary_special_branch_really_entered=True)

terrain = {}
for tag, value in [('schema8-restricted-clear',0), ('schema8-restricted-rock',3)]:
    events = audits(rows(tag),7)
    assert events and all(r['value']==value for r in events)
    terrain[tag] = dict(queries=len(events), movement_restricted_to=value)
effect['terrain'] = terrain

cloaked_rows = rows('schema8-cloaked-corridor')
cloaked_states = states(cloaked_rows)
reveal = audits(cloaked_rows,12)
assert len(reveal)==1 and reveal[0]['frame']==197 and reveal[0]['value']==1
enemy = [(s['frame'],next(o for o in s['objects'] if o['id']==1022580)) for s in cloaked_states]
before = next(o for f,o in enemy if f==197)
assert before['cloak_state']==2
after = [(f,o['cloak_state']) for f,o in enemy if 197<f<=220]
assert any(value==3 for _,value in after) and any(value==0 for _,value in after)
effect['cloaked_obstacle'] = dict(tag='schema8-cloaked-corridor', reveal=reveal,
    before_cloak_state=before['cloak_state'], after_cloak_states=after,
    original_ini_cloak_ability_fixture=True, stock_truck_has_cloak=False,
    real_world_cloak_and_reveal_verified=True)

template = {}
for tag in ('schema8-standard-01','schema8-congestion-01','schema8-cloaked-corridor'):
    records = rows(tag)
    selection,commit = audits(records,13),audits(records,14)
    assert selection and commit
    template[tag] = dict(selection_entries=len(selection), segment_commit_entries=len(commit),
        selectors=sorted({r['value'] for r in selection}))
effect['template_state'] = template

zero = rows('final-zero-delay')
zero_waits = audits(zero,8)
assert zero_waits and all(r['auxiliary']==0 for r in zero_waits)
assert read(STAGE/'runs/final-zero-delay/comparison.json')['passed']
effect['zero_delay'] = dict(tag='final-zero-delay', wait_entries=len(zero_waits),
    zero_duration_really_observed=True, independent_complete_rules_ini=True)

matrix = read(STAGE/'schema8-matrix.json')
assert matrix['passed']
budget = read(ROOT/'evidence/movement-state-v5/budget-conditions.json')
budget['real_scene_evidence'] = []
budget['unresolved'] = [
    '仍未找到合法玩法中同时重建失败、保留调用者目标且通过后续可达性复核的自然耗尽场景。',
    '移动器包装确实存在；已观察的包装期没有命中旧 Drive 准备函数。仍需排查间接服务、替换瞬间或区划变化。',
    '不能从当前有限场景推导整个游戏的失败预算分支不可达。']
for tag in ('schema8-budget-natural','schema8-restricted-clear','schema8-restricted-rock','schema8-cloaked-corridor'):
    records = rows(tag)
    failures = [r for r in audits(records,6) if r['value']==0]
    assert failures
    assert all(r['active_is_caller'] and r['active_ground_drive'] and not r['caller_goal_valid']
               and not r['active_goal_valid'] for r in failures)
    values = sorted({o['ground_drive']['path_failure_counter'] for s in states(records)
                     for o in s['objects'] if o['id']==1022579})
    assert values==[10] and not audits(records,3)
    budget['real_scene_evidence'].append(dict(tag=tag, failed_rebuilds=failures,
        failure_budget_values=values, natural_budget_entries=0))

all_natural_tags = [r['tag'] for r in matrix['results'] if r['tag']!='schema8-budget-entry']
all_natural_tags += ['final-zero-delay','final-chrono-team-02','final-chrono-team-03']
for tag in all_natural_tags:
    assert read(STAGE/'runs'/tag/'comparison.json')['passed'], tag
    assert not audits(rows(tag),3), tag
    assert not audits(rows(tag),15), tag

# 固定存档中的矿车通过原版流程进入 Teleport 并恢复 Drive；不依赖受控入口。
wrapper = {}
for tag in ('schema8-standard-01','schema8-congestion-01'):
    records = rows(tag)
    samples = [(s['frame'],next(o for o in s['objects'] if o['id']==1032341)) for s in states(records)]
    counts = collections.Counter(hex(o['locomotor_vtable']) for _,o in samples)
    assert counts['0x7ad1a8']>0 and counts['0x7a04cc']>0
    transitions = []
    previous = None
    for frame,obj in samples:
        current = obj['locomotor_vtable']
        if current!=previous:
            transitions.append(dict(frame=frame,vtable=hex(current)))
            previous=current
    wrapper[tag] = dict(unit=1032341,frames_by_vtable=dict(counts),transitions=transitions,
        prepare_with_different_active_locomotor_entries=len(audits(records,15)))
budget['locomotor_investigation'] = dict(
    original_1006_locally_verified=True,
    ground_drive_interface_vtable='0x7A04CC',teleport_interface_vtable='0x7AD1A8',
    teleport_piggyback_vtable='0x7AD184',teleport_guid_address='0x7A1FD0',
    begin_piggyback='0x6E1960',end_piggyback='0x6E19B0',wrapped_interface_member='base+0x48',
    process='0x6E0E10..0x6E16EF', real_save=wrapper,
    static_findings=[
        'Teleport Process 主体未见直接调用 Drive Process/Prepare，未见间接 +0x40 调用，也未见读取包装成员 interface+0x44。',
        '这只缩小包装期仍执行旧 Drive 的假设；没有排除全部回调及辅助函数。',
        '原版 StopMoving 清当前 Teleport 的目标，理论上与旧 Drive 目标不同；必须先证明旧 Drive 此时真的执行，不能仅凭有包装就断言触发。'],
    evidence=['locomotor-layout.json','teleport-process.asm','teleport-stop.asm','teleport-begin-end.asm'],
    public_header_leads_only=[
        'https://raw.githubusercontent.com/Ares-Developers/YRpp/master/TeleportLocomotionClass.h',
        'https://raw.githubusercontent.com/Ares-Developers/YRpp/master/GeneralDefinitions.h'],
    yuri_addresses_or_layout_transplanted=False)
budget['fixture_attempts'] = dict(
    malformed_lowercase_team='final-chrono-team: both modes fail to load; null TaskForce at 0x6C01A6; retained',
    canonical_key_without_tag='final-chrono-team-02: both modes pass 601 frames; no reinforcement spawned',
    canonical_key_with_tag='final-chrono-team-03: inspect effects.chrono_trigger for actual branch coverage')

chrono_rows = rows('final-chrono-team-03')
first_ids = {o['id'] for o in states(chrono_rows)[0]['objects']}
created = sorted({o['id'] for s in states(chrono_rows) for o in s['objects'] if o['id'] not in first_ids
                  and 'locomotor_vtable' in o})
vts = collections.Counter(hex(o['locomotor_vtable']) for s in states(chrono_rows) for o in s['objects']
                          if o['id'] in created)
effect['chrono_trigger'] = dict(tag='final-chrono-team-03', new_unit_ids=created,
    new_unit_frames_by_vtable=dict(vts), reinforcement_spawn_observed=bool(created),
    prepare_with_different_active_locomotor_entries=len(audits(chrono_rows,15)),
    natural_budget_entries=len(audits(chrono_rows,3)))
budget['locomotor_investigation']['chrono_trigger'] = effect['chrono_trigger']
budget['natural_exhaustion_verified'] = False
budget['controlled_entry_is_natural'] = False
budget['all_natural_scenes_no_budget_entry'] = all_natural_tags
effect['budget_conditions'] = str(STAGE/'budget-conditions.json')
effect['passed'] = True
write(STAGE/'budget-conditions.json',budget)
write(STAGE/'effects.json',effect)
print(json.dumps(dict(passed=True, temporary_entries=len(temporary),cloak_frame=197,
    template=template,chrono=effect['chrono_trigger'],natural_exhaustion_verified=False),ensure_ascii=False,indent=2))
