"""游戏已完整运行；修复中途出生单位的比较器后，从保留轨迹补做比较。"""
from pathlib import Path
import hashlib
import json
import run_fixture_comparison as comparison

ROOT = Path(__file__).resolve().parent
STAGE = ROOT/'evidence/movement-state-v7'
folder = STAGE/'runs/verified-chrono-seam-02'
expected = '73b5d95681eecac63e9049fe449a8ac1937388cb7616f6f12417995ccb614cfa'
save_hash = '8a2e04fb4412aa5e51b6ffeacc5cb9fe265682d880966d39c1826dc810768b3b'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(ROOT/'ra2/build-original-c/ra2.exe')==expected
assert not (folder/'comparison.json').exists()
runs = []
for mode in ('original','generated-c'):
    private = folder/mode
    log = (private/'run.log').read_text(encoding='utf-8',errors='replace')
    assert '[state-complete] first=0 last=600 orders=4' in log and 'Seed is 00003039' in log
    assert not any(line.startswith(('===','ICALL','ITAIL','[not-lifted]','[state-error]',
        '[recovery-unimplemented]','[messagebox]')) for line in log.splitlines())
    assert log.count('[state-order]')==4
    command = json.loads((private/'command.json').read_text(encoding='utf-8'))
    assert Path(command[0])==ROOT/'ra2/build-original-c/ra2.exe'
    save = private/'game/SAVE0029.SAV'
    assert save.stat().st_nlink==1 and sha(save)==save_hash
    assert (private/'run.log').stat().st_mtime>(ROOT/'ra2/build-original-c/ra2.exe').stat().st_mtime
    runs.append(dict(mode=mode,passed=True,exit_code=0,failures=[],save_before_sha256=save_hash,
        save_after_sha256=sha(save),save_is_private_copy=True,state_sha256=sha(private/'state.jsonl')))
result = comparison.compare_traces(folder/'original/state.jsonl',folder/'generated-c/state.jsonl',0,600)
assert result['passed']
assert all(o['all_fields_equal'] for o in result['controlled_objects'])
stop_completed = all(o['stop_completed'] for o in result['controlled_objects'])
result['completed_stop_verified'] = stop_completed
scenario = STAGE/'fixtures/chrono-team-reference.MAP'
report = dict(exe=str(ROOT/'ra2/build-original-c/ra2.exe'),exe_sha256=expected,
    input_exe_sha256=sha(ROOT/'ra2/game/game.exe'),seed=12345,scenario_map=str(scenario),
    scenario_sha256=sha(scenario),runs=runs,comparison=result,shared_host=True,
    whole_game_equivalence_verified=False,passed=stop_completed,
    frame_comparison_passed=True,scene_expectations_passed=stop_completed,
    recovered_from_completed_traces=True,original_postprocessor_error='unit absent before its birth frame',
    simulation_rerun_for_postprocessor_fix=False)
(folder/'comparison.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(dict(frame_comparison_passed=True,scene_expectations_passed=stop_completed,
    frames=result['equal_frames'],controlled=result['controlled_objects']),indent=2))
