"""使用相同资源副本和输入，分别运行原版机器码与生成 C 的程序。"""
import argparse
import hashlib
import importlib.util
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('cases', nargs='*', default=['menu-idle', 'menu-exit', 'skirmish-start', 'skirmish-build', 'campaign-allied', 'campaign-soviet'])
    parser.add_argument('--resume', action='store_true')
    parser.add_argument('--continue-on-failure', action='store_true')
    parser.add_argument('--report', default='runtime-comparison.json')
    args = parser.parse_args()
    report_file = ROOT / 'evidence' / args.report
    if not report_file.resolve().is_relative_to((ROOT / 'evidence').resolve()):
        raise ValueError('报告路径必须位于实验 evidence 目录。')
    executable = ROOT / 'ra2/build-original-c/ra2.exe'
    if not executable.is_file():
        raise FileNotFoundError(executable)
    os.environ['RA2_TARGET'] = 'game'
    os.environ['RA2_EXE'] = str(executable)
    os.environ['RA2_RECORD_LOSSLESS'] = '1'
    os.environ['PATH'] = r'E:\Program Files\ffmpeg-6.0-full_build\bin;' + os.environ['PATH']
    spec = importlib.util.spec_from_file_location('upstream_playtest', ROOT / 'ra2/tools/playtest.py')
    test = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(test)
    test.CASES['menu-exit-final'] = test.CASES['menu-exit']
    # 同一存档固定地图、对象和随机状态，补充按墙钟发令的随机遭遇战测试。
    test.case('save-load-paused', test.SP().press(test.SINGLE, 'LoadSavedGame', 0xB7).select(0xB7, 1317, 0).press(0xB7, 'Load')
              .waitlog(test.INGAME).key('0x1B', after=2), 120, ingame=True)
    test.case('save-load-isolated-paused', test.SP().press(test.SINGLE, 'LoadSavedGame', 0xB7).select(0xB7, 1317, 0).press(0xB7, 'Load')
              .waitlog(test.INGAME).key('0x1B', after=0), 70, ingame=True, paused=True)
    test.case('save-load-frozen-world', test.SP().press(test.SINGLE, 'LoadSavedGame', 0xB7).select(0xB7, 1317, 0).press(0xB7, 'Load')
              .waitlog(test.INGAME), 65, ingame=True, freeze_frame=2250)
    test.case('save-load-fixed-seed-world', test.SP().press(test.SINGLE, 'LoadSavedGame', 0xB7).select(0xB7, 1317, 0).press(0xB7, 'Load')
              .waitlog(test.INGAME), 65, ingame=True, freeze_frame=2250)
    records = []
    if args.resume:
        previous = json.loads(report_file.read_text(encoding='utf-8'))
        if previous['exe_sha256'] != hashlib.sha256(executable.read_bytes()).hexdigest():
            raise ValueError('程序指纹已变化，不能把旧测试合并为本次验收。')
        records = previous['results']
    for name in args.cases:
        case_args, seconds, expect = test.CASES[name]
        # 上游会清理重试场景目录；先核对解析后的目标仍位于本实验目录内。
        for suffix in ('', '.original'):
            target = Path(test.OUT) / (name + suffix) / 'game'
            if not target.resolve().is_relative_to(ROOT.resolve()):
                raise ValueError('拒绝处理实验目录外的场景: ' + str(target))
        started = time.time()
        print('开始原版与 C 对照: %s，单次上限 %d 秒' % (name, seconds), flush=True)
        with ThreadPoolExecutor(max_workers=2) as pool:
            jobs = [(original, pool.submit(test.run, name, case_args, seconds, expect, 10, original)) for original in (True, False)]
            for original, job in jobs:
                _, code, failures, seen = job.result()
                record = {'case': name, 'mode': 'original' if original else 'generated-c', 'exit_code': code, 'passed': not failures,
                          'failures': failures, 'observed': seen, 'seconds_limit': seconds, 'elapsed_pair_seconds': round(time.time() - started, 2)}
                records.append(record)
                print(json.dumps(record, ensure_ascii=False), flush=True)
        report = {'exe_sha256': hashlib.sha256(executable.read_bytes()).hexdigest(), 'results': records,
                  'all_cases_passed': all(item['passed'] for item in records), 'pixel_identity_verified': False,
                  'whole_game_equivalence_verified': False, 'original_inputs_directory_used_at_runtime': False}
        report_file.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
        if not args.continue_on_failure and any(not item['passed'] for item in records[-2:]):
            return 1
    return 0 if all(item['passed'] for item in records) else 1


if __name__ == '__main__':
    sys.exit(main())
