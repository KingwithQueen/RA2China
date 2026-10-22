"""核对第二批移动整理的最终指纹、逐部分证据和回退资料，再更新正式入口。只运行一次。"""
import ast
import difflib
import hashlib
import json
import re
import shutil
from pathlib import Path

from run_state_comparison import compare_traces

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parent.parent
STAGE = ROOT / 'evidence/movement-state-v2'
PREVIOUS = ROOT / 'evidence/movement-readable-v1'


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def write(path, data):
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def trace_path(tag, mode):
    return STAGE / 'runs' / tag / mode / 'state.jsonl'


def main():
    assert not (STAGE / 'validation.json').exists()
    assert not (STAGE / 'final-source').exists()
    executable = ROOT / 'ra2/build-original-c/ra2.exe'
    fingerprint = sha(executable)
    tags = ['final-idle', 'final-standard-01', 'final-standard-02', 'final-congestion-01', 'final-congestion-02']
    final_runs = {tag: read(STAGE / 'runs' / tag / 'comparison.json') for tag in tags}
    for tag, run in final_runs.items():
        assert run['passed'] and run['exe_sha256'] == fingerprint, tag
        compared = run['comparison']
        assert compared['frames_compared'] == 811 and compared['equal_frames'] == 811
        assert compared['rng_equal_all_frames'] and compared['first_difference'] is None
        for mode in ['original', 'generated-c']:
            with trace_path(tag, mode).open(encoding='utf-8') as stream:
                assert json.loads(next(stream))['schema'] == 5
        if tag != 'final-idle':
            assert compared['completed_stop_verified']

    repeatability = {}
    for scene in ['standard', 'congestion']:
        for mode in ['original', 'generated-c']:
            left = trace_path('final-' + scene + '-01', mode)
            right = trace_path('final-' + scene + '-02', mode)
            assert sha(left) == sha(right)
            compared = compare_traces(left, right, 0, 3000)
            assert compared['passed'] and compared['frames_compared'] == 811
            repeatability[scene + '/' + mode] = {'passed': True, 'byte_identical': True, 'trace_sha256': sha(left), 'frames': 811}

    parts = {tag: read(STAGE / 'runs' / tag / 'comparison.json') for tag in
        ['expanded-baseline', 'path-advance', 'drive-process-fixed', 'collision-standard', 'collision-congestion']}
    assert all(run['passed'] and run['comparison']['frames_compared'] == 811 for run in parts.values())
    probes = {name: read(STAGE / name) for name in ['path_fragment_probe-final.json', 'drive_process_probe-final.json',
        'collision_probe-final.json', 'arrival_probe-final.json', 'movement-probe-final.json', 'original-movement-probe-final.json']}
    assert all(probe['passed'] for probe in probes.values())
    assert probes['path_fragment_probe-final.json']['original_fragment_cases'] == 6048
    assert probes['drive_process_probe-final.json']['native_process_fixtures'] == 32768
    assert probes['collision_probe-final.json']['native_occupation_cases'] == 131072
    assert probes['collision_probe-final.json']['native_bridge_layer_cases'] == 8192
    assert probes['arrival_probe-final.json']['native_arrival_cases'] == 65536
    auxiliary = read(STAGE / 'auxiliary-final/validation.json')
    assert auxiliary['passed'] and auxiliary['exe_sha256'] == fingerprint
    effects = read(STAGE / 'scenario-effects.json')
    assert effects['passed'] and len(effects['results']) == 2

    # 不重建旧探针：只有确认它们引用的生产源码与原验收快照完全相同，才复用旧探针程序。
    previous_sources = {item['path']: item['sha256'] for item in read(PREVIOUS / 'source-manifest.json')}
    numeric_sources = ['ra2/src/gameplay/unit_movement.c', 'ra2/src/gameplay/unit_movement.h',
        'ra2/src/compat/x87_arithmetic.c', 'ra2/src/compat/x87_arithmetic.h', 'ra2/src/runtime/movement_bridge.c',
        'ra2/src/runtime/movement_bridge.h', 'evidence/movement-readable-v1/movement_probe.c',
        'evidence/movement-readable-v1/original_movement_probe.c']
    assert all(sha(ROOT / path) == previous_sources[path] for path in numeric_sources)

    # 验证接手时保存的 32 个文件；gen_game/0046 是本轮新增受影响分片，单独补入基线清单。
    baseline_manifest = read(STAGE / 'baseline/manifest.json')
    assert all(sha(STAGE / 'baseline' / item['path']) == item['sha256'] for item in baseline_manifest)
    baseline_exe = STAGE / 'baseline/ra2/build-original-c/ra2.exe'
    assert sha(baseline_exe) == '3c905c50b33124ed62f99aec7baed14da8a7186e2cd91526ae9ffc0ec29e31fc'
    additional_baseline = []
    for path in [STAGE / 'baseline/ra2/src/recomp/gen_game/recomp_0046.c', *sorted((STAGE / 'baseline/project').rglob('*'))]:
        if path.is_file():
            additional_baseline.append({'path': path.relative_to(STAGE / 'baseline').as_posix(), 'sha256': sha(path)})
    write(STAGE / 'baseline/additional-manifest.json', additional_baseline)
    snapshots = {}
    for name in ['path-advance-verified', 'drive-process-verified', 'collision-verified', 'arrival-verified']:
        folder = STAGE / 'parts' / name
        manifest = read(folder / 'manifest.json')
        assert all(sha(folder / item['path']) == item['sha256'] for item in manifest)
        snapshots[name] = {'path': str(folder), 'files': len(manifest),
            'exe_sha256': sha(folder / 'ra2/build-original-c/ra2.exe')}

    inputs = []
    original_directory = Path(r'H:\开发\运行版本\原版1.006')
    for item in read(ROOT / 'evidence/original-inputs-before.json'):
        actual = sha(original_directory / item['name'])
        inputs.append({**item, 'actual_sha256': actual, 'unchanged': actual == item['sha256']})
    assert len(inputs) == 20 and all(item['unchanged'] for item in inputs)
    old_engine = PROJECT / 'build/ra2battle.exe'
    old_engine_hash = sha(old_engine)
    assert old_engine_hash == '05d7221ffacdddb2a300aee2c51b61d1fa1d269a5336a08e0c68b023f51bdd27'
    guards = []
    for path in (ROOT / 'ra2/src/recomp/gen_game').glob('*.c'):
        guards.extend(re.findall(r'ra2_recovery_unimplemented\((0x[0-9A-Fa-f]+)', path.read_text(encoding='utf-8')))
    assert len(guards) == 37
    preservation = {'passed': True, 'all_20_original_inputs_unchanged': True, 'input_directory': str(original_directory),
        'inputs': inputs, 'old_engine': str(old_engine), 'old_engine_sha256': old_engine_hash, 'old_engine_unchanged': True,
        'baseline_exe_sha256': sha(baseline_exe), 'previous_validation_sha256': sha(PREVIOUS / 'validation.json'),
        'unsupported_instruction_guard_count': len(guards), 'component_snapshots': snapshots}
    write(STAGE / 'preservation.json', preservation)

    sources = {item['path'] for item in baseline_manifest}
    sources.update(['ra2/src/recomp/gen_game/recomp_0046.c', 'build-state-probes.ps1', 'preserve_movement_part.py',
        'integrate-ground-arrival.py', 'run_movement_state_auxiliary.py', 'audit_movement_scenarios.py', 'finalize_movement_state.py'])
    for directory in ['ra2/src/gameplay', 'ra2/src/runtime']:
        sources.update(path.relative_to(ROOT).as_posix() for path in (ROOT / directory).glob('ground_*') if path.suffix in ['.c', '.h'])
    sources.update(path.relative_to(ROOT).as_posix() for path in STAGE.glob('*.c'))
    sources.add('evidence/movement-state-v2/native_probe_host.h')
    snapshot = STAGE / 'final-source'
    snapshot.mkdir()
    manifest, patch = [], []
    for relative in sorted(sources):
        source = ROOT / relative
        if source.suffix == '.py':
            ast.parse(source.read_text(encoding='utf-8'), filename=relative)
        target = snapshot / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        manifest.append({'path': relative, 'sha256': sha(source), 'bytes': source.stat().st_size})
        old = STAGE / 'baseline' / relative
        if source.suffix in ['.c', '.h', '.py', '.ps1', '.txt'] or source.name == 'CMakeLists.txt':
            patch.extend(difflib.unified_diff(old.read_text(encoding='utf-8').splitlines(True) if old.exists() else [],
                source.read_text(encoding='utf-8').splitlines(True), fromfile='before/' + relative, tofile='after/' + relative))
    write(STAGE / 'source-manifest.json', manifest)
    (STAGE / 'source-changes.patch').write_text(''.join(patch), encoding='utf-8', newline='\n')

    report = {'passed': True, 'executable': str(executable), 'exe_sha256': fingerprint,
        'input_exe_sha256': sha(ROOT / 'ra2/game/game.exe'), 'save_sha256': sha(ROOT / 'ra2/game/SAVE0029.SAV'),
        'seed': 12345, 'state_schema': 5, 'frame_range_inclusive': [2190, 3000], 'frames_per_run': 811,
        'parts': parts, 'final_runs': final_runs, 'repeatability': repeatability, 'scenario_effects': effects,
        'native_probes': probes, 'auxiliary': auxiliary, 'preservation': preservation,
        'source_manifest': str(STAGE / 'source-manifest.json'), 'source_snapshot': str(snapshot),
        'readable_parts': {
            'path_cursor': {'original': '0x4A166A..0x4A16A6; 0x4A1F94', 'source': 'ground_path.c'},
            'complete_outer_process': {'original': '0x4A05F0..0x4A0BBB', 'source': 'ground_drive.c'},
            'collision_layer_and_occupation_tail': {'original': '0x70307B/703082; 0x703A9E; 0x703AA9..0x703BC8', 'source': 'ground_collision.c'},
            'segment_completion_state_machine': {'original': '0x4A2034..0x4A22F9', 'source': 'ground_arrival.c'}},
        'fixed_during_work': 'Process 清空已经为空的段终点时必须保留 driving；32,768 组原版结构测试发现并修复，失败日志保留。',
        'coverage': ['稳定对象 ID、类型、阵营索引、生命、位置、任务和朝向', '两组随机状态的完整有效字段',
            '已核实的部分全局和 House +0x24C 原始字段', 'Drive 目标、段终点、游标、进度、速度原始位、有效路径方向队列',
            '地表属性、有效计时器字段、导航与桥层相关标志'],
        'limitations': ['原始机器码和 C 共用宿主，不是独立原版进程的全流程对照',
            '调度、到达和占格的原版机器码探针使用世界服务替身，真实场景覆盖单个存档和所列命令',
            '桥层有机器码输入探针，尚未做真实桥梁多单位场景；门、墙、碾压战斗等尚未全部实景验收',
            'PrepareSegment、AdvanceSegment 的其余内部逻辑、CanEnterCell 的前序地形/对象交互仍为生成 C',
            '尚未覆盖完整目标、生产队列、完整资源、原版 CRC、完整战役、网络同步和全部渲染'],
        'whole_ground_movement_readable': False, 'whole_game_equivalence_verified': False,
        'new_mod_rules_added': False, 'committed': False, 'pushed': False}
    write(STAGE / 'validation.json', report)

    document = PROJECT / 'docs/单位移动路径碰撞与状态机整理-20261021.txt'
    text = f'''单位移动第二批：路径推进、占格碰撞、顶层调度及路段收尾（2026-10-21）

当前程序：{executable}
SHA-256：{fingerprint}
正式验证：{STAGE / 'validation.json'}
阅读说明：{ROOT / 'ra2/src/gameplay/阅读说明-单位移动.txt'}

一、本批实际接入的可读 C

ground_drive.c：原版 Process 完整顶层调度。包括活动路段推进、转向后刷新、目标到达、任务等待/停止及新路段准备。内部世界服务仍调用已有重编译实现。
ground_path.c：进度扣除、合法起点/终止采样区分及采样索引推进；与首批坐标变换、插值及数值兼容连用。
ground_collision.c：桥层选择、自身车辆占格排除和最终占格结果。保留车辆/步兵、同盟、Crusher、火车、武器查询的原版顺序与 0..7 返回编号。
ground_arrival.c：路段耗尽后的同格/跨格落位、段清理、目标格/高度到达判定、清目标与队列、Move 结束和单位失效返回。
原版地址、字段偏移、寄存器和栈约定全部集中在 runtime/ground_*_bridge.c；gameplay 文件不访问原版地址。
全部新生产模块为 C17，按 /W4 /WX /std:c17 /utf-8 编译。探针为 x86 C 测试，测试专用执行器用内联汇编调用原版机器码。
没有修改默认玩法或增加 MOD 配置加载器，也没有完成整个单位移动系统的可读化。

二、每部分独立对照

扩展记录后的旧算法基线：2190..3000，811 帧一致。
路径采样接入：811 帧一致；原版片段 6,048 组输入一致。
Process 调度接入并修正空段特例：811 帧一致；原版完整函数加受控世界服务 32,768 组一致。
碰撞接入：普通移动与四车拥堵两个场景各 811 帧一致；原版占格尾部 131,072 组、桥层选择 8,192 组一致。
路段收尾接入：最终普通移动与拥堵场景各 811 帧一致；原版收尾机器码加受控世界服务 65,536 组一致。
探针还比较状态写入、查询顺序、必要参数、被调用方保存寄存器、栈与返回标志。它们不能替代真实世界服务验收。
Process 的空段重复清理特例由探针发现：段本来为空时原版保留 driving；本批已修复，失败与修复日志都保留。

三、最终程序回归，均使用上述同一指纹

SAVE0029.SAV，seed 12345，帧入口 LogicClass 0x53D890；原始机器码与 C 使用相同宿主。
待机场景：2190..3000，811 帧，无缺帧/重复帧，覆盖字段全部一致。
移动/改向/停止：2192 帧移动，2230 帧改向，2270 帧 Stop；811 帧一致，独立重复两次，两路各自的状态文件字节相同。
四车拥堵/建筑占格：2192 帧四车驶向同一格，2350 帧两车驶向现有建筑格，2500 帧四车 Stop；811 帧一致，独立重复两次且字节相同。
四辆车确实移动并停止，路径队列与活动路段均有变化；没有完全相同的车辆中心，两辆车没有进入建筑中心。停止效果按实际执行、排队与后续稳定状态验收。
最终合计五次双路场景，每次 811 帧；重复采样不算新增地图或不同场景。第 2247 帧继续一致。
记录除位置/任务/朝向/生命/RNG 等旧字段，还比较目标、段终点、路径游标、进度、速度原始位、有效方向队列、地表过渡计时器和导航标志。
原版结构的未初始化填充、堆指针和终止符后的失效队列尾槽不参与相等判断。
诊断关闭的两路菜单退出正常；无效对象命令明确失败，退出码 7。
首批速度、插值、变换和 x87 数值回归全部通过，相关源码与首批验收指纹完全相同。

四、保护与回退

{STAGE / 'baseline'}：接手时 3c905c50... 程序与受影响源码、旧正式入口和说明。manifest.json 为原有 32 项，additional-manifest.json 补充本轮新增受影响分片及项目文件。
{STAGE / 'parts'}：各部分已验证程序和源码。path-advance-verified、drive-process-verified、collision-verified、arrival-verified。
{STAGE / 'final-source'}：当前程序及相关源码、构建/验证脚本和探针副本。
{STAGE / 'source-manifest.json'}：完整聚焦清单；source-changes.patch 记录相对接手版本的修改。
这些是现有实验的聚焦回退文件，需要保留实验依赖和其余生成文件。回退先保全当前代码，再按相应 manifest 恢复列出的文件并重编译核对指纹；不要覆盖历史证据。
H 盘原始目录明确列出的 20 个输入 SHA-256 全部不变，旧手写引擎 ra2battle.exe 不变；37 处未支持指令失败保护保留。
没有提交、推送或操作 GitHub。

五、剩余工作与下一步

“完整顶层调度”和“完整路段收尾”已经可读；PrepareSegment(0x4A2670) 的路径准备/重寻路、AdvanceSegment(0x4A1000) 的其余内部状态、CanEnterCell(0x703040) 的前序地形/墙/门/对象链表/让路判断仍需继续整理。
下一批优先 PrepareSegment 的路径准备和重寻路分支，保持本批默认行为和回退资料；仍按每部分原版机器码探针加真实存档逐帧对照推进。
真实桥梁、碾压/战斗、全部单位地图、独立原版全流程、完整战役、联网同步和性能仍未验收。House +0x24C 等字段尚未完全命名，不能声称覆盖全部资源与队列。
本批不新增 MOD 规则，先提供有原版验证依据的修改入口；制作 MOD 时保留原版默认分支，并为有意改变的行为建立单独预期。
'''
    document.write_text(text, encoding='utf-8', newline='\n')
    pointer = {'experiment': str(ROOT), 'validation': str(STAGE / 'validation.json'), 'executable': str(executable),
        'sha256': fingerprint, 'bounded_state_comparison_passed': True, 'frame_range_inclusive': [2190, 3000],
        'controlled_frame_range_inclusive': [2190, 3000], 'state_schema': 5, 'full_original_equivalence_verified': False,
        'whole_ground_movement_readable': False, 'complete_outer_process_readable': True,
        'complete_segment_completion_readable': True, 'longer_scene_passed': True, 'next_difference': None,
        'preservation_passed': True, 'report': str(document), 'previous_recovery_validation': str(PREVIOUS / 'validation.json'),
        'previous_recovery_executable': str(baseline_exe), 'previous_recovery_sha256': sha(baseline_exe)}
    for name in ['latest-recovery.json', 'latest-state-comparison.json']:
        write(PROJECT / 'reports' / name, pointer)
    (PROJECT / 'docs/逆向恢复与C重编译.txt').write_text(f'''原版 1.006 C 静态重编译：单位移动第二批（2026-10-21）

当前 EXE：{executable}
SHA-256：{fingerprint}
正式入口：{PROJECT / 'reports/latest-recovery.json'}
详细报告：{document}
可读核心：{ROOT / 'ra2/src/gameplay/ground_drive.c'}
代码阅读说明：{ROOT / 'ra2/src/gameplay/阅读说明-单位移动.txt'}

已新增路径采样消耗、完整顶层 Process 调度、桥层/最终占格判定、完整路段落位与到达收尾的可读 C17，保留首批 2247 帧修复及数值核心。
最终同存档、seed 12345 的待机、移动改向停止、四车拥堵建筑占格场景，2190..3000 各 811 帧全部一致；后两类独立重复两次，状态文件各自字节相同。
新增机器码输入探针合计 243,616 组通过，另保留全部首批数值回归。真实场景和使用世界服务替身的探针应区分。
尚未完成 PrepareSegment、AdvanceSegment 剩余内部状态和 CanEnterCell 前序全部交互；不代表整个移动系统或整个游戏已可读、已等价。
原始机器码和 C 共用宿主；完整玩法、桥梁实景、独立原版、联网及完整战役仍未验收。
旧基线、逐部分回退、原始输入和 37 处失败保护保留；未提交或推送。下一步继续路径准备/重寻路，每部分做原版对照。
''', encoding='utf-8', newline='\n')
    assert sha(executable) == fingerprint
    assert all(sha(ROOT / item['path']) == item['sha256'] for item in manifest)
    print(json.dumps({'passed': True, 'exe_sha256': fingerprint, 'source_files': len(manifest),
        'report': str(document), 'final_runs': len(final_runs)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
