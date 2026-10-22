"""最终 EXE 的诊断关闭菜单退出，以及错误对象编号的失败保护。"""
import hashlib
import importlib.util
import json
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'evidence/state-step-v1/auxiliary-final'
OUT.mkdir(exist_ok=False)
os.environ['RA2_TARGET'] = 'game'
spec = importlib.util.spec_from_file_location('playtest', ROOT / 'ra2/tools/playtest.py')
test = importlib.util.module_from_spec(spec)
spec.loader.exec_module(test)
exe = ROOT / 'ra2/build-original-c/ra2.exe'
fingerprint = hashlib.sha256(exe.read_bytes()).hexdigest()


def run(name, original, invalid):
    folder = OUT / name
    folder.mkdir()
    game = Path(test.farm(str(folder / 'game')))
    script = (test.SP().press(test.SINGLE, 'LoadSavedGame', 0xB7).select(0xB7, 1317, 0).press(0xB7, 'Load')
              if invalid else test.EXIT(test.S()))
    cmd = [str(exe), '--headless', '--run', '--mute', '--debuglog', '--watchdog', '90',
           '--exe', str(game / 'game.exe'), '--game', str(game), '--mod', 'none'] + script.args
    if original:
        cmd += ['--original']
    if invalid:
        cmd += ['--seed', '12345', '--state-log', str(folder / 'state.jsonl'), '--state-range', '0:2246',
                '--frame-order', '2190:4294967295:2:70:114']
    (folder / 'command.json').write_text(json.dumps(cmd, ensure_ascii=False, indent=2), encoding='utf-8')
    with (folder / 'run.log').open('w', encoding='utf-8') as log:
        result = subprocess.run(cmd, cwd=ROOT / 'ra2', stdout=log, stderr=subprocess.STDOUT, timeout=120)
    text = (folder / 'run.log').read_text(encoding='utf-8', errors='replace')
    if invalid:
        passed = result.returncode == 7 and '[state-error] order object does not exist' in text and '[state-complete]' not in text
    else:
        passed = result.returncode == 0 and '[dialog] open 0x120' in text and '[state-' not in text
    return {'case': name, 'exit_code': result.returncode, 'passed': passed, 'diagnostics_disabled': not invalid}


with ThreadPoolExecutor(max_workers=2) as pool:
    runs = list(pool.map(lambda x: run(*x), [('menu-original', True, False), ('menu-c', False, False), ('invalid-id-c', False, True)]))
report = {'exe_sha256': fingerprint, 'results': runs, 'passed': all(r['passed'] for r in runs)}
(OUT / 'validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(report, ensure_ascii=False, indent=2))
raise SystemExit(0 if report['passed'] else 1)
