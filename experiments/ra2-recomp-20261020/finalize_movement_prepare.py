"""第三批收口：先核对同指纹测试、原始输入和回退，再发布报告与正式入口。"""
import ast
import difflib
import json
import re
import shutil
from pathlib import Path

from finalize_movement_state import sha, read, write
from run_state_comparison import compare_traces, first_difference

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parent.parent
STAGE = ROOT / 'evidence/movement-prepare-v3'
PREVIOUS = ROOT / 'evidence/movement-state-v2'


def trace(tag, mode):
    return STAGE / 'runs' / tag / mode / 'state.jsonl'


def main():
    assert not (STAGE / 'validation.json').exists() and not (STAGE / 'final-source').exists()
    exe = ROOT / 'ra2/build-original-c/ra2.exe'
    fingerprint = sha(exe)
    tags = ['final-idle', 'final-standard-01', 'final-standard-02', 'final-congestion-01',
        'final-congestion-02', 'final-water-target']
    runs = {tag: read(STAGE / 'runs' / tag / 'comparison.json') for tag in tags}
    bindings = {}
    for tag, result in runs.items():
        assert result['passed'] and result['exe_sha256'] == fingerprint, tag
        compared = result['comparison']
        assert compared['frames_compared'] == compared['equal_frames'] == 811 and compared['rng_equal_all_frames']
        if tag.startswith(('final-standard', 'final-congestion')):
            assert compared['completed_stop_verified']
        for mode in ['original', 'generated-c']:
            folder = STAGE / 'runs' / tag / mode
            with trace(tag, mode).open(encoding='utf-8') as stream:
                assert json.loads(next(stream))['schema'] == 6
            lines = [line for line in (folder / 'run.log').read_bytes().splitlines() if line.startswith(b'[com-local]')]
            suffix = ('\\runs\\' + tag + '\\' + mode + '\\game\\Blowfish.dll hr=00000000').encode('ascii').lower()
            assert len(lines) >= 2 and all(suffix in line.lower() for line in lines)
            bindings[tag + '/' + mode] = {'successful_private_factory_calls': len(lines),
                'requested_server': str(folder / 'game/Blowfish.dll'), 'server_sha256': sha(folder / 'game/Blowfish.dll')}

    repeatability = {}
    for scene in ['standard', 'congestion']:
        for mode in ['original', 'generated-c']:
            left, right = trace('final-' + scene + '-01', mode), trace('final-' + scene + '-02', mode)
            assert sha(left) == sha(right)
            compared = compare_traces(left, right, 0, 3000)
            assert compared['passed'] and compared['frames_compared'] == 811
            repeatability[scene + '/' + mode] = {'byte_identical': True, 'frames': 811, 'sha256': sha(left)}

    parts = {tag: read(STAGE / 'runs' / tag / 'comparison.json') for tag in
        ['prepare-entry', 'retry-local-com', 'failure-recovery', 'overlay-barrier', 'final-congestion-01']}
    assert all(part['passed'] and part['comparison']['frames_compared'] == 811 for part in parts.values())
    catalog = read(STAGE / 'runs/cell-catalog/comparison.json')
    assert catalog['passed'] and catalog['cell_catalog_equal'] and catalog['exe_sha256'] == fingerprint
    selection = read(STAGE / 'blocked-route-selection.json')
    assert selection['target_cell'] == [54, 107] and selection['all_25_neighbor_cells_land_2_without_bridge']
    water = runs['final-water-target']['comparison']['controlled_objects'][0]
    assert water['id'] == 1032240 and not water['movement_observed'] and water['stop_completed']
    assert water['final_position'] == [17280, 29312, 416]
    prefix = {}
    for mode in ['original', 'generated-c']:
        rows = {}
        for tag in ['final-standard-01', 'final-water-target']:
            rows[tag] = [json.loads(line) for line in trace(tag, mode).read_text(encoding='utf-8').splitlines()]
            rows[tag] = [row for row in rows[tag] if row['kind'] == 'state' and row['frame'] <= 2192]
        assert first_difference(rows['final-standard-01'], rows['final-water-target']) is None
        prefix[mode] = {'same_initial_states_through_frame': 2192, 'standard_move_observed': True, 'water_move_observed': False}

    effects = read(STAGE / 'final-effects.json')
    assert effects['passed'] and all(item['retry_timer_changes_observed'] for item in effects['results'])
    # 不把没有真实发生的预算耗尽写成实景覆盖。
    budget_observed = any(item['failure_budget_changes_observed'] for item in effects['results'])
    probes = {name: read(STAGE / name) for name in ['prepare-probe-delay-boundary-final.json',
        'recovery_probe-final.json', 'barrier_probe-final.json']}
    assert all(item['passed'] for item in probes.values())
    assert probes['prepare-probe-delay-boundary-final.json']['entry_cases'] == 65536
    assert probes['prepare-probe-delay-boundary-final.json']['retry_cases'] == 65536
    assert probes['recovery_probe-final.json']['failure_budget_cases'] == 65536
    assert probes['recovery_probe-final.json']['shared_finish_cases'] == 65536
    assert probes['barrier_probe-final.json']['overlay_cases'] == 65536 and probes['barrier_probe-final.json']['gate_cases'] == 65536
    regressions = {name: read(STAGE / name) for name in ['path_fragment_probe-regression.json',
        'drive_process_probe-regression.json', 'collision_probe-regression.json', 'arrival_probe-regression.json',
        'movement-probe-regression.json', 'original-movement-probe-regression.json']}
    assert all(item['passed'] for item in regressions.values())
    auxiliary = read(STAGE / 'auxiliary-final/validation.json')
    assert auxiliary['passed'] and auxiliary['exe_sha256'] == fingerprint

    baseline = read(STAGE / 'baseline/manifest.json')
    assert all(sha(STAGE / 'baseline' / item['path']) == item['sha256'] for item in baseline)
    assert sha(STAGE / 'baseline/ra2/build-original-c/ra2.exe') == 'b1471d51b290b91040b529e084b35240f4e2b96c2bb8360675181dd97cecf46e'
    previous_sources = read(PREVIOUS / 'source-manifest.json')
    assert all(sha(PREVIOUS / 'final-source' / item['path']) == item['sha256'] for item in previous_sources)
    unchanged_paths = [item for item in baseline if item['path'].startswith(('ra2/src/compat/',
        'ra2/src/gameplay/unit_movement.', 'ra2/src/gameplay/ground_drive.', 'ra2/src/gameplay/ground_path.',
        'ra2/src/gameplay/ground_collision.', 'ra2/src/gameplay/ground_arrival.', 'ra2/src/runtime/movement_bridge.',
        'ra2/src/runtime/ground_drive_bridge.', 'ra2/src/runtime/ground_path_bridge.',
        'ra2/src/runtime/ground_collision_bridge.', 'ra2/src/runtime/ground_arrival_bridge.'))]
    assert all(sha(ROOT / item['path']) == item['sha256'] for item in unchanged_paths)

    snapshots = {}
    for name in ['prepare-entry-verified', 'retry-path-verified', 'failure-recovery-verified',
        'overlay-barrier-verified', 'gate-barrier-verified']:
        folder = STAGE / 'parts' / name
        manifest = read(folder / 'manifest.json')
        assert all(sha(folder / item['path']) == item['sha256'] for item in manifest)
        snapshots[name] = {'path': str(folder), 'files': len(manifest), 'exe_sha256': sha(folder / 'ra2/build-original-c/ra2.exe')}
    project_baseline = []
    for path in sorted((STAGE / 'baseline/project').rglob('*')):
        if path.is_file():
            relative = path.relative_to(STAGE / 'baseline/project')
            assert sha(PROJECT / relative) == sha(path), str(relative)
            project_baseline.append({'path': relative.as_posix(), 'sha256': sha(path)})
    write(STAGE / 'baseline/project-manifest.json', project_baseline)

    original_directory = Path(r'H:\开发\运行版本\原版1.006')
    inputs = []
    for item in read(ROOT / 'evidence/original-inputs-before.json'):
        actual = sha(original_directory / item['name'])
        inputs.append({**item, 'actual_sha256': actual, 'unchanged': actual == item['sha256']})
    assert len(inputs) == 20 and all(item['unchanged'] for item in inputs)
    old_engine_hash = sha(PROJECT / 'build/ra2battle.exe')
    assert old_engine_hash == '05d7221ffacdddb2a300aee2c51b61d1fa1d269a5336a08e0c68b023f51bdd27'
    guards = []
    for path in (ROOT / 'ra2/src/recomp/gen_game').glob('*.c'):
        guards.extend(re.findall(r'ra2_recovery_unimplemented\((0x[0-9A-Fa-f]+)', path.read_text(encoding='utf-8')))
    assert len(guards) == 37
    preservation = {'passed': True, 'inputs': inputs, 'all_20_original_inputs_unchanged': True,
        'old_engine_unchanged': True, 'old_engine_sha256': old_engine_hash, 'unsupported_guards': len(guards),
        'previous_source_snapshot_unchanged': True, 'component_snapshots': snapshots}
    write(STAGE / 'preservation.json', preservation)

    failures = {tag: read(STAGE / 'runs' / tag / 'comparison.json') for tag in ['retry-path', 'retry-path-rerun', 'startup-diagnostics']}
    assert all(not result['passed'] for result in failures.values())
    assert all(result['runs'][0]['state_sha256'] is None for result in failures.values())
    diagnostic = read(STAGE / 'startup-debug/exceptions.json')
    exception = next(event for event in diagnostic['events'] if event.get('type') == '.?AV_com_error@@')
    hresult = int.from_bytes(bytes.fromhex(exception['object_bytes'])[4:8], 'little')
    assert hresult == 0x80004003
    registered = {}
    try:
        import winreg
        key_path = r'CLSID\{1440AD10-6AA8-11D1-B6F9-00A024DDAFD1}\InprocServer32'
        with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, key_path, 0, winreg.KEY_READ | winreg.KEY_WOW64_32KEY) as key:
            server = Path(winreg.QueryValueEx(key, '')[0])
        registered = {'key': key_path, 'server': str(server), 'sha256': sha(server) if server.exists() else None}
    except OSError as error:
        registered = {'read_error': str(error)}
    old_c = trace('retry-path', 'generated-c')
    fixed_c = trace('retry-local-com', 'generated-c')
    assert sha(old_c) == sha(fixed_c)
    com_evidence = {'private_bindings': bindings, 'registered_server_read_only': registered,
        'private_input_dll_sha256': sha(ROOT / 'ra2/game/Blowfish.dll'), 'observed_com_error_hresult': hex(hresult),
        'failed_attempts_retained': list(failures), 'c_states_before_after_binding_byte_identical': True,
        'c_trace_sha256': sha(old_c), 'registry_written': False, 'dll_modified': False,
        'ole_run_diagnostic_shim_removed': 'static void shim_OleRun' not in (ROOT / 'ra2/src/runtime/host.c').read_text(encoding='utf-8')}
    write(STAGE / 'com-binding-evidence.json', com_evidence)

    sources = {item['path'] for item in baseline}
    sources.update(['prepare_movement_v3.py', 'build-prepare-probes.ps1', 'snapshot_prepare_part.py',
        'integrate_ground_prepare.py', 'integrate_ground_barrier.py', 'debug_original_startup.py',
        'run_prepare_auxiliary.py', 'audit_prepare_scenarios.py', 'select_blocked_route.py', 'finalize_movement_prepare.py'])
    for directory in ['ra2/src/gameplay', 'ra2/src/runtime']:
        for name in ['ground_prepare', 'ground_recovery', 'ground_barrier', 'ground_prepare_bridge',
            'ground_recovery_bridge', 'ground_barrier_bridge']:
            sources.update(path.relative_to(ROOT).as_posix() for path in (ROOT / directory).glob(name + '.*') if path.suffix in ['.c', '.h'])
    sources.update(path.relative_to(ROOT).as_posix() for path in STAGE.glob('*.c'))
    sources.add('evidence/movement-prepare-v3/native_probe_host.h')
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
        if source.suffix in ['.c', '.h', '.py', '.ps1', '.txt'] or source.name == 'CMakeLists.txt':
            old = STAGE / 'baseline' / relative
            patch.extend(difflib.unified_diff(old.read_text(encoding='utf-8').splitlines(True) if old.exists() else [],
                source.read_text(encoding='utf-8').splitlines(True), fromfile='before/' + relative, tofile='after/' + relative))
    write(STAGE / 'source-manifest.json', manifest)
    (STAGE / 'source-changes.patch').write_text(''.join(patch), encoding='utf-8', newline='\n')
    modules = {'prepare_entry': '0x4A2690..0x4A285E', 'retry_path': '0x4A285E..0x4A2A83',
        'failure_recovery': '0x4A2DFD..0x4A2F7A; shared 0x4A2EAC',
        'overlay_barrier': '0x703331..0x703439', 'gate_barrier': '0x703536..0x7035AC'}
    report = {'passed': True, 'executable': str(exe), 'exe_sha256': fingerprint, 'seed': 12345,
        'input_exe_sha256': sha(ROOT / 'ra2/game/game.exe'), 'save_sha256': sha(ROOT / 'ra2/game/SAVE0029.SAV'),
        'state_schema': 6, 'frame_range_inclusive': [2190, 3000], 'frames_per_run': 811,
        'modules': modules, 'parts': parts, 'final_runs': runs, 'repeatability': repeatability,
        'native_probes': probes, 'new_native_case_count': 393216, 'unchanged_module_regressions': regressions,
        'unchanged_module_source_hashes_verified': True, 'auxiliary': auxiliary, 'scenario_effects': effects,
        'water_target_selection': selection, 'water_vs_standard_initial_prefix': prefix,
        'failure_budget_changes_seen_in_real_scene': budget_observed, 'cell_catalog': catalog,
        'com_binding_evidence': com_evidence, 'preservation': preservation,
        'source_manifest': str(STAGE / 'source-manifest.json'), 'source_snapshot': str(snapshot),
        'limitations': ['原始机器码和 C 使用同一宿主；不是独立原版进程全流程对照',
            '原版片段探针使用受控世界服务，真实场景未触发失败预算耗尽；耗尽分支由机器码探针覆盖',
            '墙/闸门有机器码输入对照及整合回归，尚未补齐专用墙/门实景场景',
            'PrepareSegment 的障碍观察、新段选择、转向和递归重试，以及 AdvanceSegment 和 CanEnterCell 其余逻辑仍需整理',
            '路径搜索服务本身仍为生成 C；全局目标、生产队列、完整资源、战役、联网同步及渲染未全面验收'],
        'whole_prepare_function_readable': False, 'whole_ground_movement_readable': False,
        'whole_game_equivalence_verified': False, 'default_gameplay_changed': False, 'new_mod_rules_added': False,
        'committed': False, 'pushed': False}
    write(STAGE / 'validation.json', report)

    document = PROJECT / 'docs/路径准备重寻路与障碍状态整理-20261021.txt'
    document.write_text(f'''单位移动第三批：路径准备、重寻路、失败收尾与墙/门碰撞（2026-10-21）

程序：{exe}
SHA-256：{fingerprint}
正式验证：{STAGE / 'validation.json'}
阅读说明：{ROOT / 'ra2/src/gameplay/阅读说明-单位移动.txt'}

一、本批已接入的可读 C17

ground_prepare.c：准备入口的目标/等待/队伍状态检查、已有方向队列的距离裁剪、重寻路计时器、重建调用、目标复核与近距离停止。
ground_recovery.c：失败预算扣减与耗尽后的停止、提示音、关联对象通知、路径状态清理；共享入口不会重复扣预算和发提示。
ground_barrier.c：箱子限制、墙体碾压/攻击/同盟等级、闸门通行与敌我障碍处理。保留等级 0..7 与是否立即结束扫描的区别。
原版地址和栈约定单独放在 runtime/ground_*_bridge.c，gameplay 核心以状态结构体和命名服务表达。尚未确认的谓词/字段保留偏移名称，不把猜测写成 INI 规则。
新增生产模块按 /W4 /WX /std:c17 /utf-8 编译，保持纯 C；测试执行器的内联汇编仅用于调用真实原版机器码。
默认玩法、路径搜索服务和 MOD 配置加载保持既有行为；本批没有新增玩法规则。

二、逐部分验证

路径准备入口、重寻路、失败收尾、墙体/覆盖物、闸门分开接入，每部分均与原版真实存档对照 2190..3000 共 811 帧，结果一致。
路径准备入口与重寻路各 65,536 组机器码输入；失败预算与共享收尾各 65,536 组；覆盖物/墙与闸门各 65,536 组，共 393,216 组通过。
探针核对状态写入、服务调用顺序及有效参数、继续入口、返回值、栈和被调用方保存寄存器/标志。等待换算还核对三种有效 x87 精度、四种舍入方式和 0.01 等边界系数。
原版世界服务在这些探针中由受控替身提供；不能把输入探针称为全部实景覆盖。
初版探针包含 x87 保留精度编号，已改为有效编号；墙体探针曾在返回后覆盖被测栈槽，已改为覆盖前采样。原始失败日志均保留，没有放宽相等判据。

三、最终同指纹回归

SAVE0029.SAV、seed 12345；实际模拟帧 2190..3000，每次 811 帧。
待机：两路全部覆盖字段一致。
移动/改向/停止：2192 移动、2230 改向、2270 停止；独立重复两次，两路一致且各自的重复状态文件字节相同。
四车拥堵/建筑占格：2192 四车驶向同一格、2350 两车驶向建筑格、2500 四车停止；独立重复两次，两路一致且各自重复字节相同。
水面受阻目标：只读导出本存档格数据，选取 [54,107]；该点及周围 25 格均为 land==2 且无桥。2192 对坦克 1032240 发移动命令、2800 发停止；两路 811 帧一致，坦克保持原位，停止确实执行并完成。
水面场景与普通移动场景发令前状态一致，普通移动能观察到移动；这支持水面目标受阻的行为区别，不把“命令已经提交”误算为单位已移动。
地图格数据两路完全一致；此目录只作选点诊断，不改地图、存档或地形。
最终六次双路长场景均无缺帧、重复帧或覆盖字段差异，第 2247 帧继续一致。另有两帧地图目录采集，不算新增长场景。
状态格式 6 新增重寻路计时器、失败预算和准备标志；真实记录确实有重试计时器变化，但本批实景未触发预算递减/耗尽。耗尽分支由机器码探针覆盖，后续仍需专用实景。
已有速度/x87、路径游标、顶层调度、占格和路段到达探针全部回归通过，相关生产源码与上轮指纹不变。
关闭状态诊断后，两路菜单退出正常；错误对象命令仍以退出码 7 明确失败。

四、原版启动问题与宿主依赖定位

重寻路整合时，两次原版对照在生成状态记录之前退出；另一次临时 COM 诊断的 C 路径超时。均保留为失败，不算算法对照通过。
外部只读异常观察发现 _com_error，错误对象 HRESULT 0x80004003；此前 COM 异常信息还出现接口未注册/接口不可用。系统类注册指向 Steam 安装目录。
当时核对注册目录与私有目录的 Blowfish.dll 摘要相同，因此不能据此声称 DLL 字节或版本不一致，也没有证据认定注册项在本轮被修改。
宿主现在优先用私有游戏目录中 Blowfish.dll 的本地类工厂创建其提供的对象，其他类保留系统 COM 路径；不改注册表、不改 DLL、不修改原版检查与异常处理。
修正后，两路均正常启动并完成全部最终场景；日志逐次确认请求了各自私有 DLL 且创建成功。修正前后 C 路径同场景的状态文件也字节相同，支持其为依赖定位修正。
临时 OleRun 诊断适配已移除，最终仍用原有 OleRun 路径。详细证据：com-binding-evidence.json、startup-debug/exceptions.json 和各失败运行目录。

五、保护与回退

{STAGE / 'baseline'} 保存上一轮 b1471d51... 程序及 60 项聚焦源码/工具、旧正式入口与说明。
{STAGE / 'parts'} 保存 prepare-entry-verified、retry-path-verified、failure-recovery-verified、overlay-barrier-verified、gate-barrier-verified 五个已验证节点。
{STAGE / 'final-source'} 保存本轮最终程序、相关源码和构建/验证脚本；source-manifest.json 与 source-changes.patch 对应当前文件。
这是现有实验的聚焦回退资料，保留其余生成文件和依赖。回退前先保全当前工作，再按相应清单恢复并重新验证；不要重写历史报告。
旧入口节点未包含本轮宿主定位修正，回退后不能直接沿用新版本的启动结论；需要当前稳定节点时，优先使用 retry-path-verified 及之后的快照。
上一轮 final-source 全部指纹不变，H 盘明确列出的 20 个原始输入与旧手写引擎均不变，37 处未支持指令失败保护保留。
本轮没有提交、推送或操作 GitHub，没有写入 H 盘项目或原始资源。

六、尚未完成与下一顺序

PrepareSegment 尚未完整可读：障碍观察/让路 0x4A2A83..0x4A2DFD 与 0x4A2F7A..0x4A32CA、新段选择和转向/递归重试 0x4A32CA 以后仍有生成 C。
路径搜索本身、AdvanceSegment 其余内部状态、CanEnterCell 的其余地形/特殊建筑/单位交通交互也仍待整理；墙、闸门和预算耗尽还需补专用实景。
下一批先接续上述障碍观察与新段选择，再继续 AdvanceSegment/CanEnterCell；每部分保留旧默认行为与回退，继续机器码输入探针加真实存档逐帧对照。
这些结果不等于整个移动系统或整个游戏已全部可读/等价，也未覆盖独立原版全流程、完整资源与生产队列、完整战役、联网、全部渲染和性能。
''', encoding='utf-8', newline='\n')
    pointer = {'experiment': str(ROOT), 'validation': str(STAGE / 'validation.json'), 'executable': str(exe),
        'sha256': fingerprint, 'bounded_state_comparison_passed': True, 'frame_range_inclusive': [2190, 3000],
        'controlled_frame_range_inclusive': [2190, 3000], 'state_schema': 6, 'full_original_equivalence_verified': False,
        'whole_prepare_function_readable': False, 'whole_ground_movement_readable': False,
        'complete_outer_process_readable': True, 'complete_segment_completion_readable': True,
        'longer_scene_passed': True, 'next_difference': None, 'preservation_passed': True, 'report': str(document),
        'previous_recovery_validation': str(PREVIOUS / 'validation.json'),
        'previous_recovery_executable': str(STAGE / 'baseline/ra2/build-original-c/ra2.exe'),
        'previous_recovery_sha256': 'b1471d51b290b91040b529e084b35240f4e2b96c2bb8360675181dd97cecf46e'}
    for name in ['latest-recovery.json', 'latest-state-comparison.json']:
        write(PROJECT / 'reports' / name, pointer)
    (PROJECT / 'docs/逆向恢复与C重编译.txt').write_text(f'''原版 1.006 C 静态重编译：单位移动第三批（2026-10-21）

当前 EXE：{exe}
SHA-256：{fingerprint}
正式入口：{PROJECT / 'reports/latest-recovery.json'}
详细报告：{document}
阅读入口：{ROOT / 'ra2/src/gameplay/ground_prepare.c'}
阅读说明：{ROOT / 'ra2/src/gameplay/阅读说明-单位移动.txt'}

新增路径准备入口、重寻路等待/重建决策、失败预算与共享收尾、墙/覆盖物和闸门的可读 C17；五部分各有 811 帧原版对照，新增机器码输入探针 393,216 组通过。
最终待机、移动改向停止、四车拥堵建筑占格、水面受阻目标共六次双路长场景，2190..3000 各 811 帧一致；前两类受控移动各重复两次且状态文件字节相同。
实景观察到重试计时器变化，尚未触发失败预算耗尽；墙/闸门专用实景也待补充。完整 PrepareSegment、AdvanceSegment 和 CanEnterCell 仍需继续整理。
宿主优先绑定私有原版 Blowfish.dll，解决本轮遇到的 COM 启动接口问题；两路规则相同，不改注册表和原始组件。
旧基线、逐部分回退、20 项原始输入、旧手写引擎和 37 处失败保护均保留；未提交或推送。下一步整理障碍观察、新段选择和其余内部状态。
原始机器码与 C 共用宿主，完整游戏等价、独立原版、全战役、联网与全部渲染尚未验收。
''', encoding='utf-8', newline='\n')
    assert sha(exe) == fingerprint and all(sha(ROOT / item['path']) == item['sha256'] for item in manifest)
    print(json.dumps({'passed': True, 'exe_sha256': fingerprint, 'source_files': len(manifest),
        'new_native_cases': 393216, 'final_runs': len(runs), 'report': str(document)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
