"""对已完成的多单位逐帧记录做行为覆盖检查，不把发令记录当执行效果。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STAGE = ROOT / 'evidence/movement-state-v2'
IDS = [1032240, 1032241, 1032242, 1032243]


def audit(tag):
    report = json.loads((STAGE / 'runs' / tag / 'comparison.json').read_text(encoding='utf-8'))
    assert report['passed']
    records = [json.loads(line) for line in (STAGE / 'runs' / tag / 'original/state.jsonl').read_text(encoding='utf-8').splitlines()]
    states = [r for r in records if r['kind'] == 'state']
    result = {'tag': tag, 'frames': len(states), 'all_four_moved_and_stopped': False, 'objects': []}
    for uid in IDS:
        objects = [next(o for o in r['objects'] if o['id'] == uid) for r in states]
        directions = [o['ground_drive']['path_directions'] for o in objects]
        controlled = next(o for o in report['comparison']['controlled_objects'] if o['id'] == uid)
        assert controlled['movement_observed'] and controlled['stop_completed'] and controlled['all_fields_equal']
        result['objects'].append({'id': uid, 'unique_positions': len({tuple(o['position']) for o in objects}),
            'path_queue_nonempty_frames': sum(bool(q) for q in directions),
            'active_path_frames': sum(o['ground_drive']['path_selector'] != -1 for o in objects),
            'final_position': objects[-1]['position'], 'final_mission': objects[-1]['mission']})
    result['all_four_moved_and_stopped'] = True
    result['identical_vehicle_centers_frames'] = sum(len({tuple(next(o for o in r['objects'] if o['id'] == uid)['position'])
        for uid in IDS}) != len(IDS) for r in states)
    building = next(o for o in states[0]['objects'] if o['id'] == 1032328)
    assert building['position'] == [18048, 30080, 416]
    result['building_position'] = building['position']
    result['building_command_executed'] = all(any(r['kind'] == 'execute' and r['id'] == uid and r['frame'] == 2350 for r in records)
        for uid in [1032240, 1032242])
    result['building_target_vehicles_remained_outside_center'] = all(
        next(o for o in r['objects'] if o['id'] == uid)['position'] != building['position']
        for r in states if r['frame'] >= 2350 for uid in [1032240, 1032242])
    assert result['building_command_executed'] and result['building_target_vehicles_remained_outside_center']
    assert result['identical_vehicle_centers_frames'] == 0
    result['passed'] = True
    return result


if __name__ == '__main__':
    results = [audit(tag) for tag in ['final-congestion-01', 'final-congestion-02']]
    path = STAGE / 'scenario-effects.json'
    assert not path.exists()
    path.write_text(json.dumps({'passed': True, 'results': results}, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'passed': True, 'scenarios': len(results)}))
