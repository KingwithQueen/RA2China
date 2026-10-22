"""汇总本轮有界状态闭环，保全旧入口，并明确保留更长运行的失败记录。"""
import ast
import difflib
import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path

from run_state_comparison import compare_traces

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parent.parent
EVIDENCE = ROOT / 'evidence/state-step-v1'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def git(*args):
    return subprocess.check_output(['git', *args], encoding='utf-8', errors='replace').strip()


exe = ROOT / 'ra2/build-original-c/ra2.exe'
fingerprint = sha(exe)
tags = ['idle-final-01', 'move-stop-final-01', 'move-stop-final-02']
bounded = {tag: read(EVIDENCE / 'runs' / tag / 'comparison.json') for tag in tags}
auxiliary = read(EVIDENCE / 'auxiliary-final/validation.json')
longer = read(EVIDENCE / 'runs/longer-final/comparison.json')
preservation = read(EVIDENCE / 'preservation.json')
assert all(v['passed'] and v['exe_sha256'] == fingerprint for v in bounded.values())
assert auxiliary['passed'] and auxiliary['exe_sha256'] == fingerprint
assert longer['exe_sha256'] == fingerprint and not longer['passed']
assert preservation['all_20_original_inputs_unchanged'] and preservation['old_engine_unchanged']
assert 'checked=265320 failed=0' in (EVIDENCE / 'precision-probe.log').read_text()
assert 'error ' not in (EVIDENCE / 'owned-c-strict.log').read_text(encoding='utf-8-sig', errors='replace')
assert sha(EVIDENCE / 'baseline/ra2/build-original-c/ra2.exe') == 'c36887f886b399aea5a629b3ac5c2e4b1e3c1b6ffbe10c0e687498b43f1f54d5'

repeat = {}
for mode in ('original', 'generated-c'):
    left = EVIDENCE / 'runs/move-stop-final-01' / mode / 'state.jsonl'
    right = EVIDENCE / 'runs/move-stop-final-02' / mode / 'state.jsonl'
    result = compare_traces(left, right, 0, 2246)
    assert result['passed']
    repeat[mode] = {'passed': True, 'frames': result['frames_compared'], 'sha256_equal': sha(left) == sha(right),
                    'first_trace_sha256': sha(left), 'second_trace_sha256': sha(right)}

guard_addresses = []
for path in (ROOT / 'ra2/src/recomp/gen_game').glob('*.c'):
    guard_addresses.extend(re.findall(r'ra2_recovery_unimplemented\((0x[0-9A-Fa-f]+)', path.read_text(encoding='utf-8')))
assert len(guard_addresses) == 37

# 保全手写源、四个生成分片和可运行 EXE；普通 git diff 不包含这些忽略/未跟踪文件。
snapshot = EVIDENCE / 'final-source'
snapshot.mkdir(exist_ok=False)
sources = [ROOT / p for p in ['ra2/CMakeLists.txt', 'ra2/run_lift.py', 'ra2/src/runtime/host.c', 'ra2/src/runtime/oracle.c',
    'ra2/src/runtime/recovery_checks.c', 'ra2/src/runtime/state_trace.c', 'ra2/src/runtime/state_trace.h',
    'ra2/src/runtime/x87_precision.c', 'ra2/src/runtime/x87_precision.h', 'ra2/src/recomp/gen_game/recomp_0010.c',
    'ra2/src/recomp/gen_game/recomp_0011.c', 'ra2/src/recomp/gen_game/recomp_0021.c', 'ra2/src/recomp/gen_game/recomp_0048.c',
    'ra2/src/recomp/gen_game/recomp_target.h', 'ra2/build-original-c/ra2.exe', 'build-faithful.ps1', 'inspect_state.py',
    'instrument_state.py', 'fix_move_precision.py', 'run_state_comparison.py', 'run_state_auxiliary.py', 'export_state_layout.py',
    'finalize_state_step.py', 'evidence/state-step-v1/x87_precision_probe.c']]
manifest = []
patch = []
focused_index = []
for path in sources:
    relative = path.relative_to(ROOT)
    destination = snapshot / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, destination)
    manifest.append({'path': str(relative), 'sha256': sha(path), 'bytes': path.stat().st_size})
    baseline = EVIDENCE / 'baseline' / relative
    if baseline.exists() and path.suffix in ('.c', '.txt') or baseline.exists() and path.name == 'CMakeLists.txt':
        patch.extend(difflib.unified_diff(baseline.read_text(encoding='utf-8').splitlines(True), path.read_text(encoding='utf-8').splitlines(True),
            fromfile='before/' + relative.as_posix(), tofile='after/' + relative.as_posix()))
    if path.name.startswith('recomp_') and path.suffix == '.c':
        for line, text in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
            match = re.match(r'void (\w+)\(void\) \{', text)
            if match:
                focused_index.append({'name': match.group(1), 'file': str(relative), 'line': line})
    if path.suffix == '.py':
        ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
write(EVIDENCE / 'source-manifest.json', manifest)
write(EVIDENCE / 'changed-shards-function-index.json', focused_index)
(EVIDENCE / 'source-changes.patch').write_text(''.join(patch), encoding='utf-8', newline='\n')

old_entry = PROJECT / 'reports/latest-recovery.json'
old_brief = PROJECT / 'docs/逆向恢复与C重编译.txt'
shutil.copy2(old_entry, EVIDENCE / 'baseline/latest-recovery-before.json')
shutil.copy2(old_brief, EVIDENCE / 'baseline/brief-before.txt')

report = {'stage': '模拟帧状态对照的首个有界闭环及首个真实数值差异修复', 'date': '2026-10-21 Asia/Shanghai',
          'exe': str(exe), 'exe_sha256': fingerprint, 'input_exe_sha256': sha(ROOT / 'ra2/game/game.exe'),
          'bounded_scene_passed': True, 'frame_range_inclusive': [2190, 2246], 'frames_per_run': 57, 'objects_first_frame': 66,
          'bounded_reports': {k: str(EVIDENCE / 'runs' / k / 'comparison.json') for k in tags},
          'repeatability': repeat, 'auxiliary': auxiliary, 'native_cpu_precision_cases': 265320,
          'first_repaired_difference': {'before_frame': 2192, 'object_id': 1032341, 'field': 'position.x',
              'original': 32900, 'old_generated_c': 32899, 'cause': 'x87 PC/RC rounding in fild/fmul/fstp float32 sequence',
              'evidence': 'arithmetic-01: frame 2191 coefficient original=0x3F7FFFFF, C=0x3F800000',
              'implementation': 'C17 integer arithmetic; 12 lifted copies at original 0x004A241F'},
          'longer_scene_passed': False, 'next_difference': longer['comparison']['first_difference'],
          'next_difference_report': str(EVIDENCE / 'runs/longer-final/comparison.json'),
          'preservation': preservation, 'unsupported_guards_retained': len(guard_addresses),
          'full_original_equivalence_verified': False, 'shared_host': True,
          'fields_coverage': read(EVIDENCE / 'verified-layout.json'),
          'upstream': {'ra2_commit': git('-C', str(ROOT / 'ra2'), 'rev-parse', 'HEAD'),
                       'ra2_branch': git('-C', str(ROOT / 'ra2'), 'branch', '--show-current') or 'detached HEAD',
                       'ra2_status': git('-C', str(ROOT / 'ra2'), 'status', '--short'),
                       'pcrecomp_commit': git('-C', str(ROOT / 'pcrecomp'), 'rev-parse', 'HEAD'),
                       'pcrecomp_branch': git('-C', str(ROOT / 'pcrecomp'), 'branch', '--show-current') or 'detached HEAD',
                       'pcrecomp_status': git('-C', str(ROOT / 'pcrecomp'), 'status', '--short'),
                       'new_commits': False, 'pushed': False},
          'source_manifest': str(EVIDENCE / 'source-manifest.json'), 'source_snapshot': str(snapshot),
          'rollback_exe': str(EVIDENCE / 'baseline/ra2/build-original-c/ra2.exe')}
write(EVIDENCE / 'validation.json', report)
pointer = {'experiment': str(ROOT), 'validation': str(EVIDENCE / 'validation.json'), 'executable': str(exe),
           'sha256': fingerprint, 'bounded_state_comparison_passed': True, 'frame_range_inclusive': [2190, 2246],
           'full_original_equivalence_verified': False, 'longer_scene_passed': False,
           'next_difference': report['next_difference'], 'preservation_passed': True,
           'previous_recovery_validation': str(ROOT / 'evidence/validation.json'),
           'previous_recovery_executable': report['rollback_exe'],
           'previous_recovery_sha256': 'c36887f886b399aea5a629b3ac5c2e4b1e3c1b6ffbe10c0e687498b43f1f54d5'}
write(PROJECT / 'reports/latest-state-comparison.json', pointer)
write(old_entry, pointer)

document = f'''原版 1.006 模拟帧状态对照与移动精度修复（2026-10-21）

一、当前结果
已完成交接第十节第一优先项中的首个小场景闭环：相同 SAVE0029.SAV、seed 12345，在原始机器码与生成 C 两路中，从读档后的第 2190 帧到 2246 帧连续采样 57 次。每个初始场景有 66 个 Techno 对象。
无操作场景及移动/停止场景的当前覆盖字段逐帧一致。移动/停止场景独立运行两遍，两条路径各自重复结果一致。
第 2192 帧向对象 1032240 提交移动到 (68,114)，第 2218 帧提交 Stop；原版事件执行入口确认同帧消费。单位从 (17280,29312,416) 移至 (17536,29312,416)，进入原版 Stop 任务 13，最后连续十帧位置不变。
最初停止效果检查误要求最终任务必须为 Guard 5；原版实际保持 Stop 13。旧错误断言报告以 comparison-guard-only-expectation.json 保留，原始记录未改写；修正断言后另做了独立重跑。

二、首次差异及修复
修复前，第 2190/2191 帧记录一致；第 2192 帧矿车 1032341 的横坐标首次相差 1：原版 32900，C 32899。
进一步取得第 2191 帧的实际插值参数：原版 float 位模式 0x3F7FFFFF（略小于 1），C 为 0x3F800000（1）。
对应指令为 0x004A23F0 fild、0x004A2404 fmul、0x004A241F fstp float32。原版使用 x87 PC/RC，普通 C double 乘法和 float 转换使用宿主舍入，不能直接等同。
新增 x87_precision.c 以 C17 整数运算保留精确乘积，依次模拟乘法精度和单精度存储舍入。仅替换这个已核实指令序列的 12 份共享尾部转换副本，没有修改原版 EXE 或游戏规则。
独立 x86 CPU 探针对照 265,320 组样本全部一致，覆盖三种有效精度、四种舍入及符号/边界值。该结论仅针对这段指令序列，不表示所有 x87 运算均已修正。

三、明确保留的下一处差异
更长的最终程序诊断仍不通过：第 2247 帧，同一矿车横坐标原版 32045、C 32044。
内部记录显示，第 2246 帧移动进度值首次不同；后续应沿 0x004A1000 的速度/进度计算和 0x004C9B10 调查。不能把“第一处修复”写成整段长运行或整场游戏等价。
下一步先定位这处差异，再扩展攻击、选择、生产命令和目标、队列、完整资源字段；之后才处理交接第十节的残留恢复疑点。

四、当前采样语义与边界
边界为 0x0053D890 逻辑更新函数入口，真实计数位于 0x00A40D2C，0x00540684 写回递增值。快照发生在当前帧发令前；执行入口 0x004B65C0 单独记录实际消费帧。当前场景每帧恰好命中一次，缺帧或重复会失败。
以 AbstractClass +0x10 为稳定对象编号排序，阵营/所有者指针转换为 House 列表索引；不比较堆指针。
当前字段：对象编号/类型虚表、所有者、生命、三维位置、三个任务槽、三个方向结构的有效字段、场景编号计数、完整模拟 RNG 有效状态、House +0x24C 原始标量和待提交事件数量。
RNG 的 +1..+3、方向结构中的未初始化填充和 x87 控制字保留位均有原版构造器/指令依据，原始中间记录保留。不是遇到差异后任意忽略有效字段。
尚未覆盖全部目标引用、生产队列、完整资源收支和原版 CRC 覆盖范围。House +0x24C 暂保留偏移名，不将其误称为完整资源校验。
比较器已验证能定位人为增加 1 的对象坐标，并拒绝缺帧；错误对象编号的真实运行明确退出 7。37 处未支持指令失败保护仍保留。
原版/C 使用同一宿主，不能排除宿主共同影响；未做独立原版完整战役、全部单位、联网或多核性能验收。

五、程序、证据与复现
当前 EXE：{exe}
SHA-256：{fingerprint}
正常启动参数：--run --exe "{ROOT / 'ra2/game/game.exe'}" --game "{ROOT / 'ra2/game'}" --scale nearest
添加 --original 使用同宿主原始机器码。普通游玩不要加状态范围诊断；诊断会在最后一帧主动退出。
本轮正式入口：{PROJECT / 'reports/latest-state-comparison.json'}
汇总证据：{EVIDENCE / 'validation.json'}
对应原版指令/字段：{EVIDENCE / 'verified-layout.asm'}、verified-layout.json
源文件与程序快照：{snapshot}
新增手写文件和忽略的生成分片不在普通 git diff 内；应按 source-manifest.json 保全。
源码或生成目录变化后应使用新的唯一测试 tag，不得沿用旧 EXE 指纹报告，也不要覆盖旧场景。
复现示例（在实验目录运行）：
& 'E:\\Program Files\\Python\\python.exe' -B '.\\run_state_comparison.py' --tag 新的唯一名称 --range 0:2246 --order 2192:1032240:2:68:114 --order 2218:1032240:13:0:0 --require-completed-stop
--range 0:2246 表示自动记录读档后的第一个逻辑边界，并要求之后连续无缺帧；本存档首帧为 2190。
正常构建仍使用 build-faithful.ps1。原版固定地址映射需要正常本机执行环境；受限环境的映射失败不能解释为转换逻辑失败。
instrument_state.py 与 fix_move_precision.py 均拒绝重复覆盖。重新生成 C 前必须保全当前生成分片；重新生成会丢掉本轮探针及定点修复，不能直接覆盖。
旧 finalize_recovery.py 针对交接基线报告设计；本轮已用 finalize_state_step.py 汇总，不能用旧脚本覆盖当前正式入口。

六、保护与仓库状态
明确清单中的 20 个 H 盘原始输入逐个 SHA-256 不变；旧手写引擎 ra2battle.exe 不变。未声称整个 H 盘目录无并行更新。
原始存档在测试中均为真实独立副本，运行数据仅写入 D 盘实验。保留原报告、录屏、生成基线和旧手写工程。
交接基线 EXE：{report['rollback_exe']}
基线 SHA-256：c36887f886b399aea5a629b3ac5c2e4b1e3c1b6ffbe10c0e687498b43f1f54d5
项目根没有 Git 仓库。ra2 和 pcrecomp 的固定上游提交保持不变，已有适配及本轮改动保留在本地工作树；本轮未提交、未推送。
中国阵营、视频编码升级、多核优化均未纳入本轮。
'''
doc = PROJECT / 'docs/模拟帧状态对照与移动精度修复-20261021.txt'
doc.write_text(document, encoding='utf-8', newline='\n')
brief = f'''原版 1.006 汇编恢复与 C 静态重编译（2026-10-21 状态对照进度）

当前 EXE：{exe}
SHA-256：{fingerprint}
正式入口：{PROJECT / 'reports/latest-recovery.json'}
本轮报告：{doc}

已建立按真实模拟帧发令和关键对象/RNG 对照。相同存档、seed 12345，第 2190–2246 帧共 57 个模拟帧、66 个初始对象的当前覆盖字段逐帧一致；移动/停止场景独立重跑一致，停止后最后十帧静止。
已用 C17 修复一处 x87 移动插值舍入差异，真实 x86 CPU 的 265,320 组定点序列对照通过。关闭诊断的原版/C 菜单退出均为 0；错误对象编号按预期失败。
更长运行仍在第 2247 帧出现下一处矿车位置差异，尚未证明完整游戏等价。目标、生产队列和完整资源校验仍待扩展；保留 37 处未支持指令失败保护。

正常启动参数：--run --exe "{ROOT / 'ra2/game/game.exe'}" --game "{ROOT / 'ra2/game'}" --scale nearest
添加 --original 用于同宿主机器码对照。
仍是依赖原版静态数据、DLL 和必要 x86 ABI 桥的 C 静态重编译参考版，尚不是独立可移植的新引擎。
交接前的菜单、战役运行和固定画面证据对应旧 c368... 基线，完整旧说明保存在 {EVIDENCE / 'baseline/brief-before.txt'}，基线程序也保留；没有把那些结果移用到当前程序。
原始输入 20 项和旧手写引擎哈希保护通过；未提交或推送。下一步先定位 2247 帧差异，再扩展状态与命令覆盖。
'''
old_brief.write_text(brief, encoding='utf-8', newline='\n')
print(json.dumps({'exe_sha256': fingerprint, 'bounded_scene_passed': True, 'repeatability': repeat,
                  'next_difference': report['next_difference'], 'report': str(doc)}, ensure_ascii=False, indent=2))
