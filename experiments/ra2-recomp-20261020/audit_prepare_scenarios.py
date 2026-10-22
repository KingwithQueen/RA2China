"""检查真实记录中的重寻路计时器、失败预算及命令效果。"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STAGE = ROOT / 'evidence/movement-prepare-v3'


def audit(tag):
    report = json.loads((STAGE / 'runs' / tag / 'comparison.json').read_text(encoding='utf-8'))
    assert report['passed']
    records = [json.loads(line) for line in (STAGE / 'runs' / tag / 'original/state.jsonl').read_text(encoding='utf-8').splitlines()]
    states = [r for r in records if r['kind'] == 'state']
    objects = {}
    for state in states:
        for item in state['objects']:
            if 'ground_drive' in item:
                objects.setdefault(item['id'], []).append((state['frame'], item))
    result = {'tag': tag, 'frames': len(states), 'units': []}
    for uid, samples in sorted(objects.items()):
        timer_states = [item['ground_drive']['path_retry_timer'] for _, item in samples]
        budgets = [item['ground_drive']['path_failure_counter'] for _, item in samples]
        result['units'].append({'id': uid, 'timer_states': sorted({tuple(t) for t in timer_states}),
            'timer_changed_frames': [samples[i][0] for i in range(1, len(samples)) if timer_states[i] != timer_states[i - 1]],
            'failure_budgets': sorted(set(budgets)),
            'failure_budget_changed_frames': [samples[i][0] for i in range(1, len(samples)) if budgets[i] != budgets[i - 1]]})
    result['retry_timer_changes_observed'] = any(unit['timer_changed_frames'] for unit in result['units'])
    result['failure_budget_changes_observed'] = any(unit['failure_budget_changed_frames'] for unit in result['units'])
    result['controlled_objects'] = report['comparison']['controlled_objects']
    result['passed'] = True
    return result


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('tags', nargs='+')
    ap.add_argument('--output')
    args = ap.parse_args()
    results = [audit(tag) for tag in args.tags]
    if args.output:
        path = STAGE / args.output
        assert path.resolve().parent == STAGE.resolve() and not path.exists()
        path.write_text(json.dumps({'passed': True, 'results': results}, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(results, ensure_ascii=False, indent=2))
