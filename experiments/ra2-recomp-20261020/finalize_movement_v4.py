"""核对第四批同指纹实景、探针和回退后发布；自然预算覆盖保持诚实的 false。"""
import difflib
import json
import re
import shutil
from pathlib import Path
from finalize_movement_state import sha, read, write

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parent.parent
STAGE = ROOT / 'evidence/movement-state-v4'
PREVIOUS = ROOT / 'evidence/movement-prepare-v3'

def main():
    assert not (STAGE / 'validation.json').exists() and not (STAGE / 'final-source').exists()
    fingerprint = sha(ROOT / 'ra2/build-original-c/ra2.exe')
    assert fingerprint == 'a91b434a273fe2e621b6fdfa500e6eecd0f4c33f1c7cc41e2f48e7e3a1f7ce0d'
    tags = {'final-idle': 811, 'final-standard-01': 811, 'final-standard-02': 811,
        'final-congestion-01': 811, 'final-congestion-02': 811, 'final-wall': 1001,
        'final-gate': 701, 'final-truck': 301, 'final-budget-entry': 101, 'final-budget-natural': 301}
    results = {}
    for tag, count in tags.items():
        report = read(STAGE / 'runs' / tag / 'comparison.json')
        assert report['passed'] and report['exe_sha256'] == fingerprint, tag
        comparison = report['comparison']
        assert comparison['frames_compared'] == comparison['equal_frames'] == count
        assert comparison['rng_equal_all_frames'] and comparison['first_difference'] is None
        if tag.startswith(('final-standard', 'final-congestion')):
            assert comparison['completed_stop_verified']
        for mode in ['original', 'generated-c']:
            folder = STAGE / 'runs' / tag / mode
            with (folder / 'state.jsonl').open(encoding='utf-8') as stream:
                assert json.loads(next(stream))['schema'] == 7
            assert '[com-local]' in (folder / 'run.log').read_text(encoding='utf-8', errors='replace')
        results[tag] = {'passed': True, 'paired_frames': count, 'comparison': str(STAGE / 'runs' / tag / 'comparison.json')}
    assert read(STAGE / 'matrix.json')['passed']
    repeatability = {}
    for scene in ['standard', 'congestion']:
        for mode in ['original', 'generated-c']:
            paths = [STAGE / 'runs' / f'final-{scene}-{number}' / mode / 'state.jsonl' for number in ['01', '02']]
            assert sha(paths[0]) == sha(paths[1]), (scene, mode)
            repeatability[scene + '/' + mode] = {'byte_identical': True, 'sha256': sha(paths[0])}
    effects = read(STAGE / 'effects.json')
    assert effects['passed'] and effects['budget']['real_world_recovery_entry_verified']
    assert effects['budget']['normal_pathfinding_exhaustion_verified'] is False
    probes = {}
    for name in ['movement-probe-final.json', 'original_movement_probe-final.json', 'path_fragment_probe-final.json',
        'drive_process_probe-final.json', 'collision_probe-final.json', 'arrival_probe-final.json', 'prepare_probe-final.json',
        'recovery_probe-final.json', 'barrier_probe-final.json', 'obstacle_probe-final.json', 'segment_probe-final.json', 'speed-ramp-probe-01.json']:
        probes[name] = read(STAGE / name)
        assert probes[name]['passed'], name
    auxiliary = read(STAGE / 'auxiliary-final/validation.json')
    assert auxiliary['passed'] and auxiliary['exe_sha256'] == fingerprint
    baseline = read(STAGE / 'baseline/manifest.json')
    assert all(sha(STAGE / 'baseline' / item['path']) == item['sha256'] for item in baseline)
    previous_manifest = read(PREVIOUS / 'source-manifest.json')
    assert all(sha(PREVIOUS / 'final-source' / item['path']) == item['sha256'] for item in previous_manifest)
    assert sha(STAGE / 'baseline/ra2/build-original-c/ra2.exe') == '3a3024ced1d2315662d7534b096054ba1bcbd4e92f64bb44021b31ca12eb0581'
    snapshots = {}
    for name in ['obstacle-observation-verified', 'segment-preparation-verified', 'speed-ramp-and-recovery-verified']:
        folder = STAGE / 'parts' / name
        manifest = read(folder / 'manifest.json')
        assert all(sha(folder / item['path']) == item['sha256'] for item in manifest), name
        snapshots[name] = {'path': str(folder), 'files': len(manifest), 'exe_sha256': sha(folder / 'ra2/build-original-c/ra2.exe')}
    originals = Path(r'H:\开发\运行版本\原版1.006')
    inputs = []
    for item in read(ROOT / 'evidence/original-inputs-before.json'):
        actual = sha(originals / item['name'])
        assert actual == item['sha256'], item['name']
        inputs.append({**item, 'verified_sha256': actual})
    assert len(inputs) == 20
    old_engine = sha(PROJECT / 'build/ra2battle.exe')
    assert old_engine == '05d7221ffacdddb2a300aee2c51b61d1fa1d269a5336a08e0c68b023f51bdd27'
    guards = []
    for path in (ROOT / 'ra2/src/recomp/gen_game').glob('*.c'):
        guards.extend(re.findall(r'ra2_recovery_unimplemented\((0x[0-9A-Fa-f]+)', path.read_text(encoding='utf-8')))
    assert len(guards) == 37
    preservation = {'passed': True, 'all_20_original_inputs_unchanged': True, 'inputs': inputs,
        'old_engine_unchanged': True, 'old_engine_sha256': old_engine, 'unsupported_guards': len(guards),
        'v3_sources_and_baseline_unchanged': True, 'component_snapshots': snapshots}
    write(STAGE / 'preservation.json', preservation)

    new_report = PROJECT / 'docs/路径准备内部状态与墙闸实景验证-20261021.txt'
    guide = ROOT / 'ra2/src/gameplay/阅读说明-单位移动.txt'
    append = '''
十、第四批：障碍观察、新路段准备与速度爬升

ground_obstacle.c / ra2_ground_observe_obstacle：0x4A2A83..0x4A2DFD 和 0x4A2F7A..0x4A32CA。
明确区分重建失败后的观察与重建成功后的复核；保留再次查询朝向/队列、请求开闸、友军识别、近距离停止、桥层让路通知。
成功复核后才把失败预算恢复为 10；失败观察继续到原有预算收尾。

ground_segment.c / ra2_ground_prepare_segment：0x4A32CA..0x4A3550。
按队列方向构造下一格，查询当前高度层，记录桥面切换，等待闸门许可和转向，然后临时撤销自身占用、检查下一格、恢复自身占用。
IsTrain、Crusher 与 overlay index == 0 的原版特例保持顺序。世界调用仍在 runtime/ground_prepare_bridge.c，核心不直接访问原版对象偏移。

unit_movement.c 新增加速/减速运算；compat/x87_arithmetic.c 增加有限数 double 存储舍入。
修正专用卡车地图第 27 帧 Unit+0x468 的一个最低位差异：原版 47e17a14ae47d13f，原 C 为 48e17a14ae47d13f。
不能用宿主默认 double 加法代替原版 PC/RC；新数值函数覆盖三种精度、四种舍入方式。

十一、第四批实景与覆盖边界

详细报告：docs/路径准备内部状态与墙闸实景验证-20261021.txt。
证据目录：experiments/ra2-recomp-20261020/evidence/movement-state-v4。
墙体、原版 GAGATE_A 的关闭/开闸/通行/再次关闭均有专用真实地图逐帧验证。
状态格式 7 新增桥面切换标志、阻挡长等待计时器和闸门动画/通行状态。
真实游戏对象上的恢复入口连续 11 次对照覆盖预算 10→0 及零预算收尾；这是显式入口试验，不能宣称普通寻路已经自然触发预算耗尽。
普通墙体/车辆阻挡（含 CloseEnough=0 压力图）中，原版寻路失败先经 4C4B60→49FEF0 清空行进目标，预算保持 10；这项自然触发覆盖仍待补齐。
movement_fixture.c 的建墙、建车和恢复入口只在显式参数及诊断同时开启时启用；默认不执行，不直接写失败计数、队列或伪造查询结果。

接续位置：PrepareSegment 的 0x4A3550..0x4A4725（剩余阻挡分类、等待/递归重试及路段模板选择），随后推进 AdvanceSegment 与 CanEnterCell 其余状态。
既有 v1/v2/v3、第四批 baseline/parts/final-source 和失败记录全部保留。未提交或推送。
'''
    assert '十、第四批' not in guide.read_text(encoding='utf-8')
    guide_body = guide.read_text(encoding='utf-8').replace('第三批，路径准备与重寻路', '第四批，障碍观察与路段准备')
    guide_body = guide_body.replace('当前详细报告：docs/路径准备重寻路', '第三批详细报告：docs/路径准备重寻路')
    guide_body = guide_body.replace('当前证据目录：experiments/ra2-recomp-20261020/evidence/movement-prepare-v3',
        '第三批证据目录：experiments/ra2-recomp-20261020/evidence/movement-prepare-v3')
    guide_body = guide_body.replace('再读 ground_drive.h 和 ground_drive.c',
        '接着读 ground_obstacle.h/.c 和 ground_segment.h/.c，了解下一格障碍、开闸/让路、桥面和转向等待。\n再读 ground_drive.h 和 ground_drive.c')
    guide.write_text(guide_body.rstrip() + '\n' + append, encoding='utf-8', newline='\n')
    report_text = f'''原版 1.006 单位移动第四批：路径准备内部状态与墙闸实景（2026-10-21）

一、结论
整理了障碍观察的成功/失败双入口、新路段坐标与高度/桥面/闸门/转向状态，并修复卡车第 27 帧速度最低位差异。
所有列明的最终比较均在同一 EXE 上完成：{ROOT / 'ra2/build-original-c/ra2.exe'}
SHA-256：{fingerprint}
最终 10 次双路逐帧场景共 6,460 对状态一致；移动与四车拥堵各重复两次，两种模式内部各自字节相同。
新增原版片段输入对照 196,608 组（障碍观察 131,072、新段准备 65,536），新增加减速 x87 数值对照 240,000 组，旧模块探针全部回归通过。

二、代码阅读和修改入口
{ROOT / 'ra2/src/gameplay/ground_obstacle.c'}
{ROOT / 'ra2/src/gameplay/ground_segment.c'}
{ROOT / 'ra2/src/gameplay/unit_movement.c'}
前两者用具名状态与世界服务表达原版分支，保持调用顺序和目标/计时器副作用。未知虚函数仍保留已核实的偏移名称。
原版对象读写与续接栈放在 runtime/ground_prepare_bridge.c，未把尚未恢复的整个搜索器改写成猜测算法。

三、专用实景
墙体：原版建图流程放置 8 格 NAWALL，原版碰撞分支实际命中，坦克攻击阻挡墙后到达目标；1001 帧一致。
闸门：原版 GAGATE_A 与墙体走廊，记录开闸任务 24、动画 0/1 允许通行、坦克穿过及闸门再次关闭；701 帧一致。
卡车：第 30 帧由原版 new/OverlayClass 构造流程建墙；第 27 帧原差异消失，301 帧一致。
预算入口：对真实游戏对象显式进入原版 4A2DFD / 对应 C 恢复入口，不替换世界服务；10→9→…→0，再验证 0→0 的停止和清理，101 帧一致。

四、预算自然触发尚未覆盖
不能把上一项写成普通寻路自然触发。已尝试默认墙围、车辆围堵、先接受路线再调用原版构造器建墙/建敌方车辆、显式原版重寻路、CloseEnough=0 压力图。
最终压力图确认目标前后可达性查询都为真，真实路径重建返回 0、队列头为 -1，但原版同时经 4C371A→4C4B60→49FEF0 清空行进目标，因此未进入预算扣减。
实际预算仍为 10，完整轨迹与未通过/未触发记录均保留；这只说明本轮场景的行为，尚未证明该分支在所有原版状态下都不可达。
汇编依据：{STAGE / 'native-failed-path-calls-stop.asm'}
预算常态入口条件应继续追踪，不通过写计数、禁用停止或伪造寻路返回值制造“通过”。

五、逐帧范围和限制
固定存档 SAVE0029.SAV、seed=12345，原版/C 共用相同宿主，2190..3000 每次 811 帧；专用地图由原版引擎从第 0 帧建立。
状态格式 7 比较对象位置、生命、任务、朝向、有效路径队列、路段/采样/速度、两种重试计时器、预算、准备标志、桥面切换、闸门通行和完整 RNG 等已定位字段。
没有宣称整个 PrepareSegment、AdvanceSegment、CanEnterCell 或全游戏源码均已整理完毕；渲染、联网、所有生产/战斗资源状态和全部战役仍未验收。
下一处整理起点为 0x4A3550..0x4A4725 的内部阻挡、等待与递归重试，然后继续路径推进及碰撞余下分支。

六、回退与保留
{STAGE / 'baseline'} 保留 v3 程序、86 项源文件/工具及原报告入口。
{STAGE / 'parts'} 保存障碍观察、新段准备、速度修正/恢复验收节点。
{STAGE / 'final-source'} 保存本批聚焦源码、工具、测试图与程序；source-manifest.json 记录指纹，source-changes.patch 记录差异。
20 项 H: 原始输入、旧手写引擎、v3 发布源和 37 处未支持指令失败保护核验未变。没有提交、推送或访问远程仓库。
汇总：{STAGE / 'validation.json'}
效果断言：{STAGE / 'effects.json'}
保留核验：{STAGE / 'preservation.json'}
'''
    new_report.write_text(report_text, encoding='utf-8', newline='\n')
    brief = f'''原版 1.006 C 静态重编译：单位移动第四批（2026-10-21）

当前 EXE：{ROOT / 'ra2/build-original-c/ra2.exe'}
SHA-256：{fingerprint}
正式入口：{PROJECT / 'reports/latest-recovery.json'}
详细报告：{new_report}
阅读说明：{guide}

新增 ground_obstacle.c 和 ground_segment.c：障碍观察、请求开闸/让路、近距离停止、新段坐标/高度/桥面、转向和占用恢复。
修复新卡车场景第 27 帧速度最低位差异。10 次最终双路回放共 6460 对状态一致；原版片段 196608 组及新速度数值 240000 组通过，旧探针回归通过。
墙体与闸门专用实景已通过。真实对象上恢复入口的预算 10→0 与耗尽收尾已通过；普通寻路自然触发预算耗尽仍未覆盖，详见报告，不把显式入口试验冒充自然流程。
状态格式 7 新增桥面切换、长等待计时器、闸门动画/通行。接续 0x4A3550..0x4A4725 内部状态，随后完善 AdvanceSegment 和 CanEnterCell。
全部旧基线、回退、原始输入和旧引擎保留；未提交、推送。全游戏等价和全部模块可读尚未证明。
'''
    (PROJECT / 'docs/逆向恢复与C重编译.txt').write_text(brief, encoding='utf-8', newline='\n')
    (PROJECT / '交接文档-单位移动第四批-20261021.txt').write_text(report_text, encoding='utf-8', newline='\n')

    # 保存全部现有聚焦依赖与本轮工具，保留目录结构供回退。
    paths = {item['path'] for item in baseline}
    paths.update(path.relative_to(ROOT).as_posix() for pattern in ['*.py', '*.ps1'] for path in ROOT.glob(pattern))
    for folder in ['ra2/src/gameplay', 'ra2/src/runtime', 'ra2/src/compat']:
        paths.update(path.relative_to(ROOT).as_posix() for path in (ROOT / folder).iterdir()
            if path.suffix in ['.c', '.h', '.txt'])
    for pattern in ['*.c', '*.h', 'fixtures/*.MAP']:
        paths.update(path.relative_to(ROOT).as_posix() for path in STAGE.glob(pattern))
    manifest = []
    patch = []
    for relative in sorted(paths):
        source = ROOT / relative
        assert source.resolve().is_relative_to(ROOT.resolve())
        target = STAGE / 'final-source' / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        manifest.append({'path': relative, 'bytes': source.stat().st_size, 'sha256': sha(target)})
        if source.suffix in ['.c', '.h', '.py', '.ps1', '.txt'] or source.name == 'CMakeLists.txt':
            old = STAGE / 'baseline' / relative
            before = old.read_text(encoding='utf-8').splitlines(True) if old.exists() else []
            after = source.read_text(encoding='utf-8').splitlines(True)
            if before != after:
                patch.extend(difflib.unified_diff(before, after, fromfile='before/' + relative, tofile='after/' + relative))
    write(STAGE / 'source-manifest.json', manifest)
    (STAGE / 'source-changes.patch').write_text(''.join(patch), encoding='utf-8', newline='\n')
    validation = {'passed': True, 'exe_sha256': fingerprint, 'state_schema': 7, 'runs': results,
        'total_paired_frames': sum(tags.values()), 'repeatability': repeatability, 'effects': effects,
        'probes': probes, 'new_native_fragment_cases': 196608, 'new_x87_numeric_cases': 240000,
        'preservation_passed': True, 'auxiliary_passed': True, 'source_files': len(manifest), 'shared_host': True,
        'full_original_equivalence_verified': False, 'whole_prepare_function_readable': False,
        'whole_ground_movement_readable': False, 'normal_budget_exhaustion_verified': False,
        'controlled_real_world_budget_entry_verified': True, 'committed': False, 'pushed': False, 'report': str(new_report)}
    write(STAGE / 'validation.json', validation)
    pointer = {'experiment': str(ROOT), 'validation': str(STAGE / 'validation.json'),
        'executable': str(ROOT / 'ra2/build-original-c/ra2.exe'), 'sha256': fingerprint,
        'bounded_state_comparison_passed': True, 'state_schema': 7, 'frame_range_inclusive': [2190, 3000],
        'full_original_equivalence_verified': False, 'whole_prepare_function_readable': False,
        'whole_ground_movement_readable': False, 'complete_outer_process_readable': True,
        'complete_segment_completion_readable': True, 'wall_scene_verified': True, 'gate_scene_verified': True,
        'normal_budget_exhaustion_verified': False, 'controlled_real_world_budget_entry_verified': True,
        'next_difference': None, 'preservation_passed': True, 'report': str(new_report),
        'next_readable_region': '0x4A3550..0x4A4725',
        'previous_recovery_validation': str(PREVIOUS / 'validation.json'),
        'previous_recovery_executable': str(STAGE / 'baseline/ra2/build-original-c/ra2.exe'),
        'previous_recovery_sha256': '3a3024ced1d2315662d7534b096054ba1bcbd4e92f64bb44021b31ca12eb0581'}
    write(PROJECT / 'reports/latest-recovery.json', pointer)
    write(PROJECT / 'reports/latest-state-comparison.json', {**pointer, 'paired_frames': sum(tags.values()), 'runs': results})
    print(json.dumps({'passed': True, 'exe_sha256': fingerprint, 'paired_frames': sum(tags.values()),
        'source_files': len(manifest), 'normal_budget_exhaustion_verified': False, 'report': str(new_report)}, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
