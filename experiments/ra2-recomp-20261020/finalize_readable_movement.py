"""汇总本轮固定指纹、逐部分对照、最终回归和可读代码入口；保留此前所有证据。"""
import ast
import difflib
import hashlib
import json
import re
import shutil
from pathlib import Path

from run_state_comparison import compare_traces, first_difference

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parent.parent
EVIDENCE = ROOT / 'evidence/movement-readable-v1'


def sha(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def traces(tag, mode):
    path = EVIDENCE / 'runs' / tag / mode / 'state.jsonl'
    return [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines()]


exe = ROOT / 'ra2/build-original-c/ra2.exe'
fingerprint = sha(exe)
tags = ['idle-final-long', 'move-turn-stop-final-02', 'move-turn-stop-final-03', 'move-turn-control-no-stop']
final = {tag: read(EVIDENCE / 'runs' / tag / 'comparison.json') for tag in tags}
assert all(report['passed'] and report['exe_sha256'] == fingerprint for report in final.values())
assert final['idle-final-long']['comparison']['frames_compared'] == 811
assert all(report['comparison']['rng_equal_all_frames'] for report in final.values())
parts = {name: read(EVIDENCE / 'runs' / name / 'comparison.json') for name in
         ['speed-fixed', 'fraction', 'interpolation', 'transform', 'arrival']}
assert all(report['passed'] and report['comparison']['frames_compared'] == 161 for report in parts.values())
auxiliary = read(EVIDENCE / 'auxiliary-final/validation.json')
assert auxiliary['passed'] and auxiliary['exe_sha256'] == fingerprint
numeric = read(EVIDENCE / 'movement-probe-final.json')
original_functions = read(EVIDENCE / 'original-movement-probe-final.json')
assert numeric['passed'] and original_functions['passed']
assert numeric['scale'] == 115380 and original_functions['abi_cases'] == 27648
preservation = read(EVIDENCE / 'preservation.json')
for item in preservation['inputs']:
    item['actual_sha256'] = sha(Path(preservation['input_directory']) / item['name'])
    item['unchanged'] = item['actual_sha256'] == item['expected_sha256']
preservation['all_20_original_inputs_unchanged'] = len(preservation['inputs']) == 20 and all(item['unchanged'] for item in preservation['inputs'])
preservation['old_engine_sha256'] = sha(PROJECT / 'build/ra2battle.exe')
preservation['old_engine_unchanged'] = preservation['old_engine_sha256'] == '05d7221ffacdddb2a300aee2c51b61d1fa1d269a5336a08e0c68b023f51bdd27'
write(EVIDENCE / 'preservation.json', preservation)
assert preservation['all_20_original_inputs_unchanged'] and preservation['old_engine_unchanged']
assert sha(EVIDENCE / 'baseline/ra2/build-original-c/ra2.exe') == 'e959e53f70cd62154be02ab50a300115ba269fc7182f86f9091085c3c983fe3e'

repeatability = {}
for mode in ('original', 'generated-c'):
    left = EVIDENCE / 'runs/move-turn-stop-final-02' / mode / 'state.jsonl'
    right = EVIDENCE / 'runs/move-turn-stop-final-03' / mode / 'state.jsonl'
    compared = compare_traces(left, right, 0, 2600)
    assert compared['passed'] and sha(left) == sha(right)
    repeatability[mode] = {'passed': True, 'frames': 411, 'trace_sha256': sha(left), 'byte_identical': True}

stop_effect = {}
for mode in ('original', 'generated-c'):
    stop = [row for row in traces('move-turn-stop-final-02', mode) if row['kind'] == 'state']
    control = [row for row in traces('move-turn-control-no-stop', mode) if row['kind'] == 'state']
    assert all(first_difference(a, b) is None for a, b in zip(stop, control) if a['frame'] <= 2270)
    stop_objects = [next(o for o in row['objects'] if o['id'] == 1032240) for row in stop]
    control_objects = [next(o for o in row['objects'] if o['id'] == 1032240) for row in control]
    assert stop_objects[-1]['position'] != control_objects[-1]['position']
    assert stop_objects[-1]['position'] == [18048, 28800, 416]
    assert all(o['position'] == stop_objects[-1]['position'] for row, o in zip(stop, stop_objects) if row['frame'] >= 2301)
    stop_effect[mode] = {'matched_before_stop_frame': 2270, 'stop_command_frame': 2270, 'settled_frame': 2301,
                         'stop_position': stop_objects[-1]['position'], 'without_stop_final_position': control_objects[-1]['position'],
                         'counterfactual_changes_result': True}

guard_addresses = []
for source in (ROOT / 'ra2/src/recomp/gen_game').glob('*.c'):
    guard_addresses.extend(re.findall(r'ra2_recovery_unimplemented\((0x[0-9A-Fa-f]+)', source.read_text(encoding='utf-8')))
assert len(guard_addresses) == 37

source_files = ['ra2/CMakeLists.txt', 'ra2/run_lift.py', 'ra2/src/runtime/host.c', 'ra2/src/runtime/recovery_checks.c',
    'ra2/src/runtime/state_trace.c', 'ra2/src/runtime/state_trace.h', 'ra2/src/runtime/x87_precision.c', 'ra2/src/runtime/x87_precision.h',
    'ra2/src/runtime/movement_bridge.c', 'ra2/src/runtime/movement_bridge.h', 'ra2/src/gameplay/unit_movement.c',
    'ra2/src/gameplay/unit_movement.h', 'ra2/src/gameplay/阅读说明-单位移动.txt', 'ra2/src/compat/x87_arithmetic.c',
    'ra2/src/compat/x87_arithmetic.h', 'ra2/src/recomp/gen_game/recomp_0010.c', 'ra2/src/recomp/gen_game/recomp_0011.c',
    'ra2/src/recomp/gen_game/recomp_0012.c', 'ra2/src/recomp/gen_game/recomp_0021.c', 'ra2/src/recomp/gen_game/recomp_0048.c',
    'ra2/src/recomp/gen_game/recomp_target.h', 'ra2/build-original-c/ra2.exe', 'build-faithful.ps1', 'build-movement-probe.ps1',
    'run_state_comparison.py', 'run_state_auxiliary.py', 'run_movement_auxiliary.py', 'extract_readable_movement.py',
    'continue-readable-parts.ps1', 'finalize_readable_movement.py', 'evidence/movement-readable-v1/movement_probe.c',
    'evidence/movement-readable-v1/original_movement_probe.c']
snapshot = EVIDENCE / 'final-source'
assert not snapshot.exists() and not (EVIDENCE / 'validation.json').exists()
for relative in source_files:
    if relative.endswith('.py'):
        ast.parse((ROOT / relative).read_text(encoding='utf-8'), filename=relative)
snapshot.mkdir()
manifest = []
patch = []
for relative in source_files:
    source = ROOT / relative
    destination = snapshot / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    manifest.append({'path': relative, 'sha256': sha(source), 'bytes': source.stat().st_size})
    before = EVIDENCE / 'baseline' / relative
    if before.exists() and (source.suffix in ('.c', '.h', '.py', '.ps1') or source.name == 'CMakeLists.txt'):
        patch.extend(difflib.unified_diff(before.read_text(encoding='utf-8').splitlines(True), source.read_text(encoding='utf-8').splitlines(True),
            fromfile='before/' + relative, tofile='after/' + relative))
write(EVIDENCE / 'source-manifest.json', manifest)
(EVIDENCE / 'source-changes.patch').write_text(''.join(patch), encoding='utf-8', newline='\n')

for relative in ('reports/latest-recovery.json', 'reports/latest-state-comparison.json', 'docs/逆向恢复与C重编译.txt'):
    source = PROJECT / relative
    destination = EVIDENCE / 'baseline' / Path(relative).name
    assert not destination.exists()
    shutil.copy2(source, destination)

modules = {
    'speed': {'function': 'ra2_ground_scale_speed', 'original': '0x004C9B79..0x004C9B83', 'purpose': '基础速度乘当前系数后取整数进度'},
    'fraction': {'function': 'ra2_ground_progress_fraction', 'original': '0x004A23F0..0x004A241F', 'lifted_tail_copies': 12},
    'interpolation': {'function': 'ra2_ground_interpolate_position', 'original': '0x007220C0', 'typed_points': True},
    'transform': {'function': 'ra2_ground_transform_path_sample', 'original': '0x004A4740', 'preserves_output_z_in_bridge': True},
    'arrival': {'function': 'ra2_ground_arrival_progress_adjustment', 'original': '0x004A2015..0x004A202B', 'lifted_tail_copies': 6}}
old_stop = read(EVIDENCE / 'runs/move-turn-stop-final-01/comparison.json')
report = {'date': '2026-10-21 Asia/Shanghai', 'stage': '第2247帧修复和单位移动首批可读C', 'exe': str(exe), 'exe_sha256': fingerprint,
    'input_exe_sha256': sha(ROOT / 'ra2/game/game.exe'), 'seed': 12345,
    'repaired_difference': read(EVIDENCE / 'difference-2247.json'), 'readable_modules': modules,
    'module_source': str(ROOT / 'ra2/src/gameplay/unit_movement.c'), 'abi_bridge': str(ROOT / 'ra2/src/runtime/movement_bridge.c'),
    'numeric_compatibility': str(ROOT / 'ra2/src/compat/x87_arithmetic.c'), 'numeric_cpu_probe': numeric,
    'original_function_and_abi_probe': original_functions, 'parts': {name: {'report': str(EVIDENCE / 'runs' / name / 'comparison.json'),
        'exe_sha256': value['exe_sha256'], 'passed': value['passed'], 'frame_range_inclusive': [2190, 2350]} for name, value in parts.items()},
    'final_runs': {tag: str(EVIDENCE / 'runs' / tag / 'comparison.json') for tag in tags},
    'idle_frame_range_inclusive': [2190, 3000], 'idle_frames': 811, 'controlled_frame_range_inclusive': [2190, 2600],
    'controlled_frames': 411, 'initial_techno_objects': 66, 'repeatability': repeatability, 'stop_effect_counterfactual': stop_effect,
    'old_stop_observer_expectation': {'archived_report': str(EVIDENCE / 'runs/move-turn-stop-final-01/comparison.json'),
        'all_411_states_equal': old_stop['comparison']['equal_frames'] == 411,
        'why_report_failed': 'required current mission 13 at a boundary; native queued 13 then transitioned directly to Guard 5',
        'new_acceptance': 'Stop event executed, queued after execution, stable final position and idle mission; checked against no-Stop control'},
    'coverage': read(ROOT / 'evidence/state-step-v1/verified-layout.json'), 'unsupported_failure_guards_retained': 37,
    'auxiliary': auxiliary, 'preservation': preservation, 'shared_host': True, 'full_original_equivalence_verified': False,
    'complete_readable_movement_state_machine': False, 'new_mod_rules_added': False, 'next_observed_difference': None,
    'source_snapshot': str(snapshot), 'source_manifest': str(EVIDENCE / 'source-manifest.json'),
    'rollback_exe': str(EVIDENCE / 'baseline/ra2/build-original-c/ra2.exe'), 'new_commits': False, 'pushed': False}
write(EVIDENCE / 'validation.json', report)
pointer = {'experiment': str(ROOT), 'validation': str(EVIDENCE / 'validation.json'), 'executable': str(exe), 'sha256': fingerprint,
    'bounded_state_comparison_passed': True, 'frame_range_inclusive': [2190, 3000], 'controlled_frame_range_inclusive': [2190, 2600],
    'full_original_equivalence_verified': False, 'longer_scene_passed': True, 'next_difference': None,
    'preservation_passed': True, 'readable_movement_core_parts': 5,
    'previous_recovery_validation': str(ROOT / 'evidence/state-step-v1/validation.json'),
    'previous_recovery_executable': report['rollback_exe'],
    'previous_recovery_sha256': 'e959e53f70cd62154be02ab50a300115ba269fc7182f86f9091085c3c983fe3e'}
write(PROJECT / 'reports/latest-recovery.json', pointer)
write(PROJECT / 'reports/latest-state-comparison.json', pointer)

document = f'''单位移动首批可读 C 与第 2247 帧修复（2026-10-21）

一、当前结果
第 2247 帧矿车位置差异已消除。最终程序在同一 SAVE0029.SAV、seed 12345 下，原始机器码与 C 两路的当前覆盖字段从 2190 到 3000 连续 811 帧一致。
移动、改向、停止场景从 2190 到 2600 连续 411 帧一致，独立重复两次，两路各自的完整记录字节相同。另有相同移动/改向但不发送停止命令的对照，证明停止命令确实改变了最终位置。
这里比较的是已有覆盖字段：初始 66 个 Techno 对象及后续对象列表中的编号、种类、所属、生命、位置、任务、方向字段、模拟 RNG 及少量全局标量。目标、生产队列、完整资源收支和整个游戏状态仍未全部覆盖。全部场景使用同一宿主，不是独立启动的零改动原版进程。

二、程序和入口
EXE：{exe}
SHA-256：{fingerprint}
总证据：{EVIDENCE / 'validation.json'}
正式入口：{PROJECT / 'reports/latest-recovery.json'}
源码清单：{EVIDENCE / 'source-manifest.json'}
接入前回退程序：{report['rollback_exe']}
原输入 game.exe SHA-256：{report['input_exe_sha256']}
本批源码、程序和测试入口已留存；final-source 是本轮重点源码快照，仍需现有上游目录及原版静态数据才能重建，不是独立分发的完整新引擎源码包。

三、2247 帧根因与修复
在第 2246 帧的 0x004C9B83 整数转换前，基础速度为 10，系数二进制为 0x3FECCCCCCCCCCCCC（约 0.8999999999999999）。原版 PC=53、RC=向零舍入得到 8.999999999999998，再由 __ftol 截断为 8；旧 C 使用宿主 double 得到 9，截断仍为 9。
这使下一帧路径进度变成原版 4、旧 C 5，矿车 1032341 的 X 坐标成为原版 32045、旧 C 32044。
新函数 ra2_ground_scale_speed 用纯 C17 的整数精度兼容运算重现乘法舍入和整数转换，未对特定单位、帧或坐标打补丁。原始/旧 C 操作数保存在 difference-2247.json 与 runs/speed-probe。到达补偿并未在第 2246 帧执行，已排除其作为该差异根因。

四、已经整理并实际接入的五个部分
可读入口：{ROOT / 'ra2/src/gameplay/unit_movement.h'}
实现：{ROOT / 'ra2/src/gameplay/unit_movement.c'}
阅读说明：{ROOT / 'ra2/src/gameplay/阅读说明-单位移动.txt'}
1. 速度乘系数并取整数移动进度。
2. 路径进度转单精度插值比例，覆盖 12 个生成共享尾部副本。
3. 三维坐标插值，替换原版 0x007220C0 的生成函数体。
4. 路径采样的轴交换、镜像、平移与朝向变换，替换 0x004A4740 的生成函数体。
5. 剩余曼哈顿距离的到达进度补偿，覆盖 6 个生成共享尾部副本。
这些函数使用普通结构体和命名参数，游戏地址、寄存器、返回标志和栈维护集中在 runtime/movement_bridge.c。旧生成控制流仍保留必要入口标签及部分结果被替换的运算语句，重新运行通用提升器会覆盖接入点。
三维插值特别保留第一次整数转换之后的控制字变化。路径变换适配层只写 X/Y，保留输出 Z。数值兼容层位于 compat/x87_arithmetic.c；它覆盖本批所需有限数值运算，不能视为完整 x87 模拟器或全部游戏浮点修复。

五、验证与范围
每个部分接入后均单独构建，并以相同原版存档验证 2190..2350 共 161 帧，再进入下一部分；各阶段 EXE 哈希与报告位于 parts 和 runs。最终整理后的 EXE 重新执行了上述 811/411 帧回归，报告哈希与当前程序一致。
CPU 指令序列对照：速度 {numeric['scale']}，到达补偿 {numeric['arrival']}，进度比例 {numeric['fraction']}，插值坐标轴 {numeric['interpolated_axes']}，兼容加减乘及浮点存储 {numeric['arithmetic']}。覆盖 24/53/64 位精度及四种舍入，包含现场捕获的 2247 帧操作数。
直接调用本机原版机器码：三维插值 {original_functions['original_interpolations']} 组、路径变换 {original_functions['original_transforms']} 组；另有 {original_functions['abi_cases']} 项适配层输出、寄存器、返回标志、栈平衡、控制字和现有浮点栈保存检查。
新增生产代码与探针通过 /std:c17 /W4 /WX 构建。原版函数探针加载原版节数据但不运行其入口；计算函数直接在本机 CPU 上执行。生产游戏逻辑和精度兼容层是 C，Windows/x86 宿主与诊断桥仍有必要的内联汇编。
诊断关闭时，原版/C 菜单退出均为 0；错误对象编号仍以退出码 7 失败。37 处未支持指令失败保护仍保留。比较器仍有位置故障注入和缺帧拒绝自检。

六、停止行为的实测说明
2192 帧命令坦克 1032240 前往 (80,114)，2230 帧改向 (67,108)，2270 帧停止。两路在 2271 帧均显示移动任务 2、待执行停止任务 13，2301 帧完成当前路段后直接转为待命任务 5，停在 (18048,28800,416)，至 2600 帧不再移动。
原先验收脚本强制要求帧边界出现 current==13，因而把两路完全相同的正确行为误判为失败；该原报告保留在 move-turn-stop-final-01。最终改为核对事件实际执行、执行后进入任务队列、位置稳定及待命结果，并增加不发送停止的原版/C 对照。未伪造“观察到了 current==13”，也未改动原版停止逻辑。
不停止时的最终位置：{stop_effect['original']['without_stop_final_position']}。停止与不停止在第 2270 帧之前的完整采样状态相同，之后因显式停止命令产生不同结果。

七、制作 MOD 的入口与尚未完成的内容
优先阅读 gameplay 下的说明和命名函数，保留原版默认参数作为基线。新增玩法参数应通过显式结构传入，并给修改前的原版行为保留对照模式。当前没有加入 MOD 规则或配置加载器。
默认采样参数 7 与倒数、采样表、段结束判断及状态机相互关联，不能单改一个数就认定做完速度 MOD。兼容控制字和整数舍入通常应保留，不应作为玩法参数随意调整。
寻路搜索、碰撞/占格、完整加减速和路径状态机、堵塞/重寻路、特殊移动与网络/存读档结构仍未整体整理。当前可读的是首批五个核心环节，整个移动模块和整个游戏尚未成为可直接修改的完整可读 C 项目。
下一步沿 DriveLocomotion 继续恢复速度状态、路径段推进和堵塞/改向流程，建立字段结构及命名状态。先按普通平地、转弯、坡地、不同速度、拥堵等分别做原版对照，再替换对应状态机；随后扩展目标、生产队列和完整资源覆盖。

八、保全与现状
清单中的 20 项 H 盘原始输入 SHA-256 不变；旧手写引擎哈希不变。未声明整个 H 盘无其他并行更新。各测试使用隔离目录和独立真实存档副本，未提交或推送。
最新已测窗口没有发现下一处差异；这不表示窗口之外、其他地图或全部玩法已经等价。以前的画面、战役和旧程序证据保持原指纹归属，本轮没有追加像素级或完整战役验收。
'''
doc = PROJECT / 'docs/单位移动模块可读C整理与2247帧修复-20261021.txt'
doc.write_text(document, encoding='utf-8', newline='\n')
brief = f'''原版 1.006 C 静态重编译：单位移动首批可读核心（2026-10-21）

当前 EXE：{exe}
SHA-256：{fingerprint}
正式入口：{PROJECT / 'reports/latest-recovery.json'}
本轮详细报告：{doc}
可读实现：{ROOT / 'ra2/src/gameplay/unit_movement.c'}
代码阅读说明：{ROOT / 'ra2/src/gameplay/阅读说明-单位移动.txt'}

第 2247 帧差异已修复。相同原版存档、seed 12345，当前覆盖字段在无操作场景 2190..3000 共 811 帧一致，在移动/改向/停止场景 2190..2600 共 411 帧一致；后者独立重复两次，另有不停止的对照。每个部分接入后均与原版单独验证过 161 帧。
已实际接入五个可读 C 环节：速度换算、路径进度、坐标插值、路径变换、到达补偿。游戏逻辑与精度兼容为 C17，原版地址与 ABI 维护集中在桥接层。
尚未完成完整路径/寻路/碰撞/加减速状态机，也未覆盖全部目标、生产队列和完整资源；不是完整可读的游戏源码或独立可移植引擎，尚未证明全部玩法等价。
保留 37 处未支持指令失败保护、前一版可运行程序及原始输入。未提交或推送。下一步继续恢复 DriveLocomotion 的状态结构与路径推进，每部分做原版对照。
'''
(PROJECT / 'docs/逆向恢复与C重编译.txt').write_text(brief, encoding='utf-8', newline='\n')
assert sha(exe) == fingerprint
print(json.dumps({'exe_sha256': fingerprint, 'idle_frames': 811, 'controlled_frames': 411,
                  'readable_parts': 5, 'repeatability': repeatability, 'doc': str(doc)}, ensure_ascii=False, indent=2))
