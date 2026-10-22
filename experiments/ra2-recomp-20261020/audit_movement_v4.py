"""对实际轨迹断言所需效果，防止只比较空跑便把未触发分支标为覆盖。"""
import collections
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
STAGE = ROOT / 'evidence/movement-state-v4'

def records(tag):
    return [json.loads(line) for line in (STAGE / 'runs' / tag / 'original/state.jsonl').read_text(encoding='utf-8').splitlines()]

def states(rows):
    return [row for row in rows if row['kind'] == 'state']

def actor(state):
    return next(obj for obj in state['objects'] if obj['id'] == 1022579)

gate_rows = records('final-gate')
gate_states = states(gate_rows)
gate_events = [row for row in gate_rows if row['kind'] == 'movement-audit' and row['stage'] == 2]
gate_objects = [obj for state in gate_states for obj in state['objects'] if 'gate' in obj]
assert gate_events and any(obj['gate']['passable'] for obj in gate_objects)
assert any(not obj['gate']['passable'] for obj in gate_objects)
assert any(obj['mission'][0] == 24 for obj in gate_objects)
assert actor(gate_states[0])['position'] == [17280, 29312, 416]
assert actor(gate_states[-1])['position'] == [17280, 27776, 416]
assert any(110 * 256 <= actor(state)['position'][1] <= 112 * 256 for state in gate_states)
assert gate_objects[-1]['gate']['passable'] is False

wall_rows = records('final-wall')
wall_states = states(wall_rows)
wall_events = [row for row in wall_rows if row['kind'] == 'movement-audit' and row['stage'] == 1]
assert wall_events and all(row['value'] == 26 for row in wall_events)
assert any(actor(state)['mission'][0] == 1 for state in wall_states)
assert actor(wall_states[-1])['position'] == [18048, 27776, 416]

budget_rows = records('final-budget-entry')
budget_events = [row for row in budget_rows if row['kind'] == 'fixture-budget-entry']
assert [(row['before'], row['after']) for row in budget_events] == [(i, i - 1) for i in range(10, 0, -1)] + [(0, 0)]
assert all(row['result'] == 0 for row in budget_events)
budget_states = states(budget_rows)
assert actor(budget_states[4])['ground_drive']['path_failure_counter'] == 10
assert actor(budget_states[15])['ground_drive']['path_failure_counter'] == 0
for state in budget_states[15:]:
    drive = actor(state)['ground_drive']
    assert drive['path_failure_counter'] == 0 and drive['path_selector'] == -1
    assert drive['segment_end'] == [0, 0, 0] and drive['flags_60_64'][1] == 0

natural_rows = records('final-budget-natural')
natural_states = states(natural_rows)
constraints = next(row for row in natural_rows if row['kind'] == 'fixture-constraints')
assert constraints['accepted_before'] == constraints['accepted_after'] == 1
assert constraints['close_enough'] == 0 and constraints['explicit_rebuild_result'] == 0 and constraints['path_head'] == -1
assert len([row for row in natural_rows if row['kind'] == 'fixture-unit']) == 8
assert all(actor(state)['ground_drive']['path_failure_counter'] == 10 for state in natural_states)
assert not any(row['kind'] == 'movement-audit' and row['stage'] == 3 for row in natural_rows)
assert any(actor(state)['ground_drive']['destination'] == [0, 0, 0] for state in natural_states[7:])

truck_rows = records('final-truck')
truck_states = states(truck_rows)
assert actor(truck_states[27])['ground_drive']['unit_speed_bits'] == '47e17a14ae47d13f'
assert len([row for row in truck_rows if row['kind'] == 'fixture-wall']) == 8
assert actor(truck_states[-1])['position'] == [18048, 27776, 416]

effect = {'passed': True, 'wall': {'real_wall_queries': len(wall_events), 'attack_observed': True, 'goal_reached': True},
    'gate': {'real_gate_queries': len(gate_events), 'opening_task_observed': True, 'passable_observed': True,
        'closed_again_observed': True, 'tank_crossed_and_reached_goal': True},
    'budget': {'real_world_recovery_entry_verified': True, 'entry_calls': len(budget_events), 'countdown': budget_events,
        'normal_pathfinding_exhaustion_verified': False, 'natural_test_constraints': constraints,
        'natural_test_failure_budget_values': [10], 'natural_test_failed_rebuild_observed': True,
        'limitation': '原版当前场景寻路失败时先清除行进目标；受控入口对照不能冒充自然寻路触发。'},
    'truck_speed': {'frame': 27, 'unit_speed_bits': '47e17a14ae47d13f', 'previous_first_difference_fixed': True,
        'goal_reached_after_runtime_wall_placement': True}}
with (STAGE / 'effects.json').open('x', encoding='utf-8') as output:
    json.dump(effect, output, ensure_ascii=False, indent=2)
print(json.dumps(effect, ensure_ascii=False, indent=2))
