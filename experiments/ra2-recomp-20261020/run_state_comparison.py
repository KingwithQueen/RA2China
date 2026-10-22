"""在独立真实存档副本上运行原始机器码/C，按真实模拟帧比较可定位的状态。"""
import argparse
import copy
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def first_difference(a, b, path=''):
    if type(a) is not type(b):
        return {'path': path, 'original': a, 'generated_c': b}
    if isinstance(a, dict):
        if a.keys() != b.keys():
            return {'path': path + '.keys', 'original': list(a), 'generated_c': list(b)}
        for key in a:
            mismatch = first_difference(a[key], b[key], path + '.' + str(key))
            if mismatch:
                return mismatch
    elif isinstance(a, list):
        if len(a) != len(b):
            return {'path': path + '.length', 'original': len(a), 'generated_c': len(b)}
        for i, (left, right) in enumerate(zip(a, b)):
            label = '[id=%s]' % left['id'] if isinstance(left, dict) and 'id' in left else '[%d]' % i
            mismatch = first_difference(left, right, path + label)
            if mismatch:
                return mismatch
    elif a != b:
        # RNG 的完整字节串较长，仅输出第一个不同字节，原始记录仍保留全部状态。
        if path.endswith(('.rng', '.table')) and isinstance(a, str) and len(a) == len(b):
            index = next(i for i in range(0, min(len(a), len(b)), 2) if a[i:i+2] != b[i:i+2])
            return {'path': path, 'byte_offset': index // 2, 'original': a[index:index+2], 'generated_c': b[index:index+2]}
        return {'path': path, 'original': a, 'generated_c': b}
    return None


def validate_records(records, first, last):
    if not records or records[0].get('kind') != 'header' or records[-1].get('kind') != 'complete':
        raise ValueError('状态记录缺少开始或完成标记')
    states = [r for r in records if r['kind'] == 'state']
    if not first:
        first = records[0]['first']
    if [r['frame'] for r in states] != list(range(first, last + 1)):
        raise ValueError('状态记录出现缺帧、重复或越界')
    return records, states


def load_trace(path, first, last):
    records = [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines()]
    return validate_records(records, first, last)


def compare_traces(left_path, right_path, first, last):
    left, ls = load_trace(left_path, first, last)
    right, rs = load_trace(right_path, first, last)
    difference = None
    matched = equal = 0
    differing_frames = []
    for original, generated in zip(ls, rs):
        delta = first_difference(original, generated, 'state')
        if delta:
            if difference is None:
                difference = {'frame': original['frame'], **delta}
            differing_frames.append(original['frame'])
        else:
            equal += 1
            if difference is None:
                matched += 1
    commands_left = [r for r in left if r['kind'] in ('submit', 'execute', 'movement-audit')]
    commands_right = [r for r in right if r['kind'] in ('submit', 'execute', 'movement-audit')]
    command_difference = first_difference(commands_left, commands_right, 'commands')
    # 用实际记录做故障注入，验证比较器能定位到具体帧、对象与字段。
    mutated = copy.deepcopy(ls[0])
    if not mutated['objects']:
        raise ValueError('受控场景没有可比较对象')
    mutated['objects'][0]['position'][0] += 1
    negative = first_difference(ls[0], mutated, 'state')
    if not negative or '.position[0]' not in negative['path']:
        raise ValueError('差异定位自检失败')
    incomplete = [r for r in left if not (r['kind'] == 'state' and r['frame'] == ls[0]['frame'])]
    try:
        validate_records(incomplete, first, last)
    except ValueError:
        missing_rejected = True
    else:
        raise ValueError('比较器没有拒绝缺帧记录')
    controlled = []
    for uid in sorted({r['id'] for r in commands_left if r['kind'] == 'submit'}):
        original_samples = [(r['frame'],o) for r in ls for o in r['objects'] if o['id']==uid]
        generated_samples = [(r['frame'],o) for r in rs for o in r['objects'] if o['id']==uid]
        if not original_samples or not generated_samples:
            raise ValueError('受控单位没有出现在状态轨迹中')
        sample_frames = [frame for frame,_ in original_samples]
        lo = [o for _,o in original_samples]
        ro = [o for _,o in generated_samples]
        stop_frames = [r['frame'] for r in commands_left if r['kind'] == 'execute' and r['id'] == uid and r['mission'] == 13]
        last_stop = max(stop_frames) if stop_frames else None
        queued_after_stop = last_stop is not None and any(13 in o['mission'] for frame, o in original_samples if frame > last_stop)
        settled_after_stop = (last_stop is not None and len(lo) >= 10 and sample_frames[-10] > last_stop and sample_frames[-1] == last
                              and len({tuple(o['position']) for o in lo[-10:]}) == 1
                              and lo[-1]['mission'] in ([5, -1, -1], [13, -1, -1]))
        controlled.append({'id': uid, 'all_fields_equal': original_samples == generated_samples,
                           'first_observed_frame':sample_frames[0], 'last_observed_frame':sample_frames[-1],
                           'movement_observed': len({tuple(o['position']) for o in lo}) > 1,
                           'stop_queued': any(13 in o['mission'] for o in lo),
                           'stop_entered': any(o['mission'][0] == 13 for o in lo),
                           'stop_executed': bool(stop_frames), 'stop_queued_after_execution': queued_after_stop,
                           'stop_completed': queued_after_stop and settled_after_stop,
                           'final_position': lo[-1]['position'], 'final_mission': lo[-1]['mission'],
                           'last_ten_positions_stationary': len({tuple(o['position']) for o in lo[-10:]}) == 1})
    return {'passed': difference is None and command_difference is None, 'first': ls[0]['frame'], 'last': last,
            'frames_compared': len(ls), 'equal_frames': equal, 'consecutive_equal_frames': matched, 'first_difference': difference,
            'differing_frames': differing_frames, 'rng_equal_all_frames': all(a['rng'] == b['rng'] for a, b in zip(ls, rs)),
            'controlled_objects': controlled,
            'commands': commands_left, 'command_difference': command_difference, 'object_count_first': len(ls[0]['objects']),
            'negative_control': {'passed': True, 'injected': 'position x +1', 'located': negative, 'missing_frame_rejected': missing_rejected}}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--tag', required=True)
    ap.add_argument('--movement-audit', action='store_true')
    ap.add_argument('--range', default='2250:2350')
    ap.add_argument('--order', action='append', default=[])
    ap.add_argument('--seconds', type=int, default=150)
    ap.add_argument('--detail-id', type=int)
    ap.add_argument('--cell-catalog', action='store_true')
    ap.add_argument('--require-completed-stop', action='store_true')
    ap.add_argument('--compare-only', nargs=2)
    ap.add_argument('--evidence-stage', default='state-step-v1')
    args = ap.parse_args()
    first, last = map(int, args.range.split(':'))
    if args.compare_only:
        result = compare_traces(*(Path(p) for p in args.compare_only), first, last)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result['passed'] else 1
    stage = ROOT / 'evidence' / args.evidence_stage
    if stage.resolve().parent != (ROOT / 'evidence').resolve():
        raise ValueError('阶段名称必须是单层目录名')
    out = stage / 'runs' / args.tag
    if not out.resolve().is_relative_to((stage / 'runs').resolve()):
        raise ValueError('场景路径越界')
    out.mkdir(parents=True, exist_ok=False)
    exe = ROOT / 'ra2/build-original-c/ra2.exe'
    fingerprint = sha(exe)
    if sha(ROOT / 'ra2/game/game.exe') != 'fe67fdac5073530a79baec14c4e072b5e7e4c0c462cee9659870c5330e9e6e3e':
        raise ValueError('输入 EXE 指纹不属于已核实的本机 1.006')
    os.environ['RA2_TARGET'] = 'game'
    spec = importlib.util.spec_from_file_location('playtest', ROOT / 'ra2/tools/playtest.py')
    test = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(test)
    script = test.SP().press(test.SINGLE, 'LoadSavedGame', 0xB7).select(0xB7, 1317, 0).press(0xB7, 'Load').waitlog(test.INGAME)

    def run(original):
        mode = 'original' if original else 'generated-c'
        folder = out / mode
        folder.mkdir()
        game = Path(test.farm(str(folder / 'game')))
        save = game / 'SAVE0029.SAV'
        if save.stat().st_nlink != 1:
            raise ValueError('存档不是独立真实副本')
        save_before = sha(save)
        if save_before != sha(ROOT / 'ra2/game/SAVE0029.SAV'):
            raise ValueError('存档初态不一致')
        cmd = [str(exe), '--headless', '--run', '--mute', '--debuglog', '--watchdog', str(args.seconds),
               '--exe', str(game / 'game.exe'), '--game', str(game), '--mod', 'none', '--seed', '12345',
               '--state-log', str(folder / 'state.jsonl'), '--state-range', args.range] + script.args
        for order in args.order:
            cmd += ['--frame-order', order]
        if args.detail_id:
            cmd += ['--state-detail-id', str(args.detail_id)]
        if args.movement_audit:
            cmd += ['--state-movement-audit']
        if args.cell_catalog:
            cmd += ['--state-cell-catalog', str(folder / 'cells.json')]
        if original:
            cmd += ['--original']
        (folder / 'command.json').write_text(json.dumps(cmd, ensure_ascii=False, indent=2), encoding='utf-8')
        with (folder / 'run.log').open('w', encoding='utf-8') as log:
            code = subprocess.run(cmd, cwd=ROOT / 'ra2', stdout=log, stderr=subprocess.STDOUT, timeout=args.seconds + 30).returncode
        text = (folder / 'run.log').read_text(encoding='utf-8', errors='replace')
        bad = [line for line in text.splitlines() if line.startswith(('===', 'ICALL', 'ITAIL', '[not-lifted]', '[state-error]', '[recovery-unimplemented]', '[messagebox]'))]
        passed = code == 0 and '[state-complete]' in text and 'Seed is 00003039' in text and not bad
        return {'mode': mode, 'exit_code': code, 'passed': passed, 'failures': bad,
                'save_before_sha256': save_before, 'save_after_sha256': sha(save), 'save_is_private_copy': True,
                'state_sha256': sha(folder / 'state.jsonl') if (folder / 'state.jsonl').exists() else None}

    with ThreadPoolExecutor(max_workers=2) as pool:
        jobs = [pool.submit(run, original) for original in (True, False)]
        runs = [job.result() for job in jobs]
    report = {'exe': str(exe), 'exe_sha256': fingerprint, 'input_exe_sha256': sha(ROOT / 'ra2/game/game.exe'),
              'seed': 12345, 'runs': runs, 'shared_host': True, 'whole_game_equivalence_verified': False}
    if all(r['passed'] for r in runs):
        report['comparison'] = compare_traces(out / 'original/state.jsonl', out / 'generated-c/state.jsonl', first, last)
        if args.cell_catalog:
            report['cell_catalog_equal'] = sha(out / 'original/cells.json') == sha(out / 'generated-c/cells.json')
            report['comparison']['passed'] = report['comparison']['passed'] and report['cell_catalog_equal']
        if args.require_completed_stop:
            controlled = report['comparison']['controlled_objects']
            # 原版移动中停止会先排入 13，再在路段结束时直接转入 Guard(5)；帧边界未必能采到 current==13。
            effects_passed = bool(controlled) and all(o['all_fields_equal'] and o['movement_observed'] and o['stop_executed']
                and o['stop_completed'] for o in controlled)
            report['comparison']['completed_stop_verified'] = effects_passed
            report['comparison']['passed'] = report['comparison']['passed'] and effects_passed
    report['passed'] = all(r['passed'] for r in runs) and report.get('comparison', {}).get('passed', False) and sha(exe) == fingerprint
    (out / 'comparison.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2), flush=True)
    return 0 if report['passed'] else 1


if __name__ == '__main__':
    sys.exit(main())
