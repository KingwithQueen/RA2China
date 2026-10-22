"""Promote generation 26 only after the concrete round 27 gates pass."""
from pathlib import Path
import difflib, hashlib, json, re, shutil

R = Path(__file__).resolve().parent
P = R.parent.parent
S = R / 'evidence/movement-state-v27'
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()

def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def existing(path, text):
    newline = '\r\n' if b'\r\n' in path.read_bytes() else '\n'
    path.write_bytes(text.replace('\r\n', '\n').replace('\n', newline).encode('utf-8'))

assert not (S / 'validation.json').exists()
accept = read(S / 'strict-acceptance.json')
budget = read(S / 'budget-real-scenes.json')
tubes = read(S / 'connection-real-scenes.json')
assert tubes['completed_scenes'] == 10 and tubes['original_equivalent_stall_scenes'] == 2 and not tubes['all_curved_height_routes_complete']
internal = read(S / 'internal-real-scenes.json')
callers = read(S / 'overlap-caller-identity.json')
assert callers['passed']
for item in callers['inputs']:
    assert sha(R / item['path']) == item['sha256'], item['path']
assert accept['passed'] and accept['paired_scenes'] == 27 and accept['paired_frames'] == 14897
assert len(accept['probes']) == 93 and read(S / 'native-gates.json')['passed']
assert budget['passed'] and budget['default_rules_full_exhaustion_verified']
assert tubes['passed'] and tubes['production_scenes'] == 12 and tubes['production_frames'] == 6712
assert tubes['curved_height_bidirectional_runtime_verified'] and tubes['curved_occupied_exit_runtime_verified']
assert internal['passed'] and internal['independent_frames'] == 4054
assert all(int(internal['stages'][str(i)]) > 0 for i in range(10, 20))
assert {18, 19}.issubset(internal['new_adapter_runtime_stages'])
exe = R / 'ra2/build-original-c/ra2.exe'
digest = sha(exe)
assert digest == accept['exe_sha256'] == budget['formal_executable_sha256'] == tubes['production_executable_sha256'] == internal['production_executable_sha256']
receipt = read(R / 'ra2/build-original-c/source-content-receipt.json')
assert receipt['source_count'] == 171 and len(receipt['inputs']) == 285 and receipt['refreshed_count'] == 0
assert receipt['executable_sha256'] == digest
for name, value in receipt['inputs'].items():
    assert sha(Path(name)) == value, name
default = read(S / 'runs/c-final-default/comparison.json')
c = default['comparison']
assert default['passed'] and default['exe_sha256'] == digest and default['scenario_rules_sha256'] is None
assert c['frames_compared'] == c['equal_frames'] == c['consecutive_equal_frames'] == 901
assert c['first_difference'] is None and c['command_difference'] is None and c['rng_equal_all_frames']
assert c['negative_control']['passed'] and c['negative_control']['missing_frame_rejected']
for mode in ['original', 'generated-c']:
    rows = [json.loads(line) for line in (S / 'runs/c-final-default' / mode / 'state.jsonl').open(encoding='utf-8')]
    frame = next(row for row in rows if row['kind'] == 'state' and row['frame'] == 28)
    assert next(obj for obj in frame['objects'] if obj['id'] == 1032262)['position'][0] == 17343
for name in ['latest-recovery.json', 'latest-state-comparison.json', 'latest-movement-candidate.json']:
    assert (P / 'reports' / name).read_bytes() == (S / 'baseline/project/reports' / name).read_bytes(), name

parts = {name: read(S / 'parts' / name / 'validation.json') for name in ['template-verified', 'passage-verified', 'returns-verified']}
for name, value in parts.items():
    assert value['passed'] and len(value['scenes']) == 6 and sum(s['frames'] for s in value['scenes']) == 3406
    archived = {e['path']: e['sha256'] for e in read(S / 'parts' / name / 'manifest.json')}
    assert all(Path(p).relative_to(R).as_posix() in archived for p in receipt['inputs'])
assert parts['returns-verified']['exe_sha256'] == digest
final_inputs = {e['path']: e['sha256'] for e in read(S / 'parts/returns-verified/manifest.json')}
assert all(final_inputs[Path(p).relative_to(R).as_posix()] == value for p, value in receipt['inputs'].items())
assert read(S / 'refactor-structure.json')['passed']
identities = {}
for name, cases in [('internal', 131072), ('connection-numeric', 1601904), ('tube-state', 131072),
                    ('progress', 491520), ('travel', 360448), ('joint', 262144), ('overlap', 262144)]:
    identity = read(S / ('native-' + name + '-identity.json'))
    assert identity['passed'] and identity['total_cases'] == cases
    for item in identity['inputs'] + [identity['probe_executable']]:
        assert sha(R / item['path']) == item['sha256'], item['path']
    identities[name] = identity

counts = {}
archives = [(f'v{v}', R / f'evidence/movement-state-v{v}', 'source-manifest.json', 'final-source') for v in range(9, 27)]
archives += [('v27-baseline', S / 'baseline', 'source-manifest.json', '')]
archives += [(name, S / 'parts' / name, 'manifest.json', '') for name in parts]
for label, base, manifest_name, sub in archives:
    entries = read(base / manifest_name)
    for item in entries:
        assert sha(base / sub / item['path']) == item['sha256'], (label, item['path'])
    counts[label] = len(entries)
for item in read(R / 'evidence/original-inputs-before.json'):
    assert sha(Path('H:/开发/运行版本/原版1.006') / item['name']) == item['sha256'], item['name']
counts['H_originals'] = 20
assert sha(R / 'ra2/game/game.exe') == 'fe67fdac5073530a79baec14c4e072b5e7e4c0c462cee9659870c5330e9e6e3e'
assert sha(R / 'ra2/game/SAVE0029.SAV') == '8a2e04fb4412aa5e51b6ffeacc5cb9fe265682d880966d39c1826dc810768b3b'
assert sha(P / 'build/ra2battle.exe') == '05d7221ffacdddb2a300aee2c51b61d1fa1d269a5336a08e0c68b023f51bdd27'
guards = sum(len(re.findall(r'ra2_recovery_unimplemented\((0x[0-9A-Fa-f]+)', p.read_text(encoding='utf-8'))) for p in (R / 'ra2/src/recomp/gen_game').glob('*.c'))
assert guards == 37
preservation = dict(passed=True, counts=counts, game_save_old_engine_preserved=True, unsupported_guards=guards, existing_connected_tail_targets_preserved=True)
write(S / 'preservation.json', preservation)

conditions = read(S / 'budget-conditions.json')
conditions['original_27_natural_budget_entries'] = conditions.pop('natural_budget_entries')
conditions['original_27_scenes_without_budget_entry'] = conditions.pop('all_natural_scenes_no_budget_entry')
conditions.update(necessary_conditions=budget['necessary_conditions'], new_static_followup=budget['callback_scope'], natural_exhaustion_verified=True,
                  default_rules_full_exhaustion_verified=True, natural_budget_scope=budget['scope'],
                  natural_budget_entries=budget['scenes']['v-default-budget']['modes']['original']['budget_events'],
                  new_real_scene_evidence=str(S / 'budget-real-scenes.json'), independent_internal_evidence=str(S / 'internal-real-scenes.json'),
                  unresolved=['4C3895 callback remains static inference, not independently hooked.', 'Untouched random-match frequency is not measured.',
                              'Nonprimary overlapping adapters have not been naturally observed; not all shared fragments are unified.'])
write(S / 'budget-conditions.json', conditions)
effects = read(S / 'effects.json')
effects['template_object_chain_shared_exits'] = identities['overlap']['results']
effects['connection_runtime'] = tubes['scenes']
effects['budget'].update(normal_pathfinding_exhaustion_verified=True, natural_exhaustion_verified=True, default_rules_full_exhaustion_verified=True, natural_scope=budget['scope'])
write(S / 'effects.json', effects)
flags = {k: v for k, v in read(R / 'evidence/movement-state-v26/validation.json').items() if k.endswith('_readable')}
flags.update(template_cell_transition_readable=True, template_type_gate_readable=True, object_chain_readable=True, passage_shared_exits_readable=True,
             whole_tube_movement_readable=False, whole_prepare_function_readable=False, whole_advance_function_readable=False,
             whole_object_passage_classifier_readable=False, whole_ground_movement_readable=False, full_original_equivalence_verified=False)
accept.update(paired_scenes=40, paired_frames=22510, production_default_skirmish='c-final-default', production_default_skirmish_frames=901,
              default_rules_full_budget_exhaustion_verified=True, natural_budget_scope=budget['scope'], independent_budget_frames=901,
              independent_connection_observer_scenes=12, independent_connection_observer_frames=6712,
              independent_internal_observer_scenes=4, independent_internal_observer_frames=4054, **flags)
write(S / 'strict-acceptance.json', accept)

report = P / 'docs/单位移动第二十六批-内部接续与对象分类链及共享出口-20261022.txt'
handoff = P / '交接文档-单位移动第二十六批正式验收-20261022.txt'
assert not report.exists() and not handoff.exists()
part_text = '\n'.join(name + ' : ' + value['exe_sha256'] for name, value in parts.items())
report.write_text(f'''单位移动第二十六批正式验收（2026-10-22）
正式代次26 / 验证轮次27
程序：{exe}
SHA-256：{digest}
证据：{S}

一、可读C整理
1. ground_template_transition：Advance 4A17FE六处重叠片段的目标/当前位置格子换算、同格比较和共享接续。保留负坐标修正、32位回绕、有符号右移及低16位比较；Advance既有主业务也复用该格子比较，避免两份不同算法。Prepare 4A3502两处类型放行判断保持原查询顺序；类型回调可能改变当前单位或共享分类，第二个条件重新读取，不能提前缓存。
2. ground_object_chain：对象通行分类链的地面/桥上链头选择、接触标记清零，以及继续遍历时恢复单元格和共享分类。703439一处，7038EF四处，所有旧回跳标签保留；具体对象类别仍由已整理分支和剩余生成片段执行，未宣称完整对象分类器已统一。
3. 五类共享出口：7031B1、703B5A、703B69、703BA8、703BBC共31个重叠返回片段复用ground_return_plan/ground_joint_bridge。正式主流程的通行分类收尾也改用同一返回助手；业务分类与ABI恢复分离。
三个新C编译单元为ground_template_transition、ground_object_chain、ground_overlap_bridge。纯C17/x86，业务模块无旧地址/直接guest内存操作；固定布局集中适配层。正式记录器schema12和两个公共比较器保持原样。

二、逐部分验收与回退
三部分各6场景3406帧：默认遭遇战901、三格包围101、默认规则真实AI预算901、双向隧道各501、出口占用501。
{part_text}
每份保存完整285项编译输入及程序。最终与returns回退逐项一致；171个C源、285项输入核对通过，最终空操作构建刷新0。

三、严格逐帧与原版片段检查
最终40个生产场景22510帧严格一致。另默认规则AI预算901帧、十二个隧道观察6712帧、四个内部观察4054帧独立对照。命令、随机数、有序查询、连续帧、坐标/缺帧负控及辅助菜单和非法命令门禁均通过。
93组原版片段检查通过；新增262144例，格子比较、类型放行、对象链、五类返回各65536例。保留极值坐标、类型回调改分类/换单位、链头空值/桥层和共享分类恢复等边界。主Advance和主通行收尾改用共享助手后重新运行其原版检查。
默认步兵第28帧X=17343、三格第52帧、转弯第197帧、二次补建失败第399帧和451..1111帧持续失败均保持。预算仍是默认规则下经正常服务构造的AI TRUCKA及16辆敌车，27..37帧10..0、第38帧停止；无直接目标/路径/预算写入。未经干预随机对局的发生频率和4C3895独立挂钩尚未验证。

四、弯曲隧道与内部接续独立实景
新增弯曲高差4/6和4/7双向四场景及弯曲出口占用，共五场景，每场景601帧。地图仅组合已核对的合法六段斜向Tubes路线及IsoMapPack5层高；没有原始运动状态注入。独立原版入口/高度/水平推进/出口观察点与C对应服务完整有序一致，观察程序与正式程序的完整状态和原有记录也一致。
完整穿越的高差场景为4→7上行和6→4下行，要求实际非直线轨迹、至少八个路点标记、非零高度范围、目标终点和目的地清空。另4→6上行和7→4下行在原版与C都出现异常：前者第一个斜向接续处高度保持436并摆动，后者高度持续下漂。两者601帧内不出隧道，仅验收原版行为一致，不能算成功穿越。另12段直角路线4→6上行也复现原版停滞，作为调查保留，不计入正式40场景。该现象与每步高度向零取整边界相符，完整因果边界尚未穷尽。占用场景在第217帧经正常构造与放置服务建立16辆真实敌车，出口格确实占用，要求连续等待后成功退出、恢复移动，且没有显式重建路径。具体出口帧、路点、等待及高度区间见connection-real-scenes.json。原双向、平直高差、平直出口占用及双向等高弯曲全部持续回归。
内部观察新增4A17FE、4A3502、703439和7038EF，与前六点一起在默认遭遇战、长距离、转弯隐形障碍、持续失败四场景直接命中；完整原版/C有序记录一致。十个测试对象替换只用于独立观察，不进入正式程序。
实际生成入口清点记录在internal-real-scenes.json及overlap-caller-identity.json：用真实调用返回地址、链接映射的包含函数和PE中E8调用指令三者核对，对象链适配在UnitClass__virtual_101（原入口00703040）自然执行；模板比较/类型判断的主业务边界已有实景，其他重叠副本仅有原版片段验证，尚未自然观察到非主入口。不得以人为跳转或修改运动内存冒充合法实景。所有少见重叠入口覆盖和全部副本统一仍未完成。

五、保存与后续
v9..v26旧正式归档、本批baseline及三份parts逐项核验；H盘20项输入、原游戏/SAV、旧手写C引擎保持原样。final-source/source-manifest及final-check绑定完整源码、程序和报告，保留全部轨迹与回退。
开发期间两个cl并行构建共享临时对象发生C1083/LNK1181，已归档失败尝试，并顺序重建、重新通过全部93组检查；这属于构建失败，没有作为游戏差异或通过证据。见native-build-development.json及investigations/native-build-attempt01。
首次入口清点使用的g_cur_func会被内部调用改写，不能独立证明调用来源；已保存原观察程序/源码及i-、w2-、o-轨迹，改用真实返回地址/链接映射/调用字节核对，并以新观察程序重新通过四个内部及十二个隧道场景。旧入口编号不作为最终归属依据，见investigations/observer-route-marker-attempt01。
完整Advance、Prepare、对象通行和隧道模块及全游戏等价仍未完成，37个未实现保护保留。下一步继续其余内部分类/模板，清点非主重叠入口的合法调用来源并在能自然触发时独立验证；补弯曲高差与出口占用的组合、不同曲率/桥层对象链等未覆盖场景。
本地提交，不推送；父提交513826391af2b54a458121e5593a8a4438e79183。
''', encoding='utf-8', newline='\n')
handoff.write_text(f'''单位移动第二十六批正式验收交接（2026-10-22）
正式代次26 / 验证轮次27：{S / 'validation.json'}
程序：{exe}
SHA-256：{digest}
本批：ground_template_transition的格子比较/类型放行，ground_object_chain的分类链初始化/继续，ground_overlap_bridge接续及31个共享出口。Advance主业务和主通行收尾复用相同助手。
三部分各6场景3406帧保存完整回退；最终40场景22510帧，另预算901、十二个隧道观察6712、四个内部观察4054帧；93组检查，本批262144例。
新增弯曲高差四场景及出口占用，各601帧；4→7上行、6→4下行完成穿越，4→6上行及7→4下行保留原版异常。十处内部边界原版/C完整记录一致。对象链适配从00703040主入口自然执行；其他重叠副本只有片段验证，非主入口自然调用尚未观察到。
报告：{report}
baseline、parts/template-verified、passage-verified、returns-verified保留；final-source及final-check绑定171个C源、285项输入和最终程序，空操作刷新0。
默认预算仍为正常服务构造的真实AI/敌车，27..37帧10..0、第38帧停止。未经干预随机频率及4C3895独立挂钩仍未测。完整模块/全游戏等价未完成，37个保护保留。
下一步其余内部分类/模板及非主重叠入口合法来源，补弯曲高差与出口占用组合、不同曲率和桥层对象链。保留全部旧基线/回退。本地提交，不推送。父提交5138263。
''', encoding='utf-8', newline='\n')
guide = R / 'ra2/src/gameplay/阅读说明-单位移动.txt'
shutil.copy2(guide, S / 'reading-guide-before.txt')
existing(guide, f'''第二十六批当前状态（2026-10-22，优先于历史描述）
ground_template_transition：目标/当前位置格子比较与类型放行；ground_object_chain：分类链选择与继续；ground_overlap_bridge：布局/接续，31个出口和主收尾复用共享返回。Advance主流程也复用格子比较。
三部分各6场景3406帧。最终40场景22510帧，另预算901、隧道观察6712、内部观察4054帧；93组检查，本批262144例。弯曲高差/出口占用对照通过，其中两例保留原版异常，十个内部边界直接命中。
对象链适配从主入口自然执行；非主重叠副本仍仅有片段验证，尚未完成全部副本统一与全模块/全游戏等价。
报告：{report}

''' + guide.read_text(encoding='utf-8'))
main = P / '交接文档-原版逆向与C重编译-20261020.txt'
assert main.read_bytes() == (S / 'baseline/project' / main.name).read_bytes()
existing(main, main.read_text(encoding='utf-8') + f'\n\n2026-10-22 第二十六批正式接续：{handoff}\n内部接续、对象分类链与共享出口完成本批验收；新增弯曲上/下行与出口占用，十个内部边界独立观察。40场景22510帧+预算901+隧道观察6712+内部观察4054帧，93组检查；三部分各6场景3406帧保存回退。非主重叠入口自然覆盖和全游戏等价未完成。本地提交，不推送。\n')
readme = P / 'README.md'
lines = readme.read_text(encoding='utf-8').splitlines(keepends=True)
lines[0] = '> 当前研究路线（2026-10-22）：原版1.006 C17/x86可读单位移动完成第二十六批正式验收。内部接续、对象分类链和共享出口通过，弯曲高差/出口占用及十处内部边界已独立观察（两例原版异常单列）；40场景22510帧，另预算901、隧道观察6712、内部观察4054帧及93组检查。入口为[第二十六批交接](交接文档-单位移动第二十六批正式验收-20261022.txt)及 `reports/latest-recovery.json`。非主重叠入口覆盖和全游戏等价未完成，旧基线及回退保留。\n'
existing(readme, ''.join(lines))

paths = {e['path'] for e in read(S / 'baseline/source-manifest.json')}
paths.update(Path(name).relative_to(R).as_posix() for name in receipt['inputs'])
paths.update(p.relative_to(R).as_posix() for p in (R / 'ra2/src').rglob('*') if p.is_file() and p.suffix in ('.c', '.h', '.txt'))
paths.update(p.relative_to(R).as_posix() for p in R.glob('*v27*') if p.is_file())
paths.update(p.relative_to(R).as_posix() for p in S.iterdir() if p.is_file() and (p.suffix in ('.c', '.h', '.asm') or p.name in ['truck-actor-fixture-build-arguments.json', 'truck-actor-fixture-probe.exe', 'truck-actor-fixture-receipt.json', 'connection-fixture-build-arguments.json', 'connection-fixture-probe.exe', 'connection-fixture.map']))
paths.update(p.relative_to(R).as_posix() for p in (S / 'fixtures').iterdir() if p.is_file())
manifest, patch = [], []
for rel in sorted(paths):
    source = R / rel
    data = source.read_bytes()
    dest = S / 'final-source' / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    manifest.append(dict(path=rel, sha256=sha(source)))
    prior = S / 'baseline' / rel
    if prior.exists() and prior.read_bytes() == data:
        continue
    if source.suffix.lower() in ['.c', '.h', '.py', '.ps1', '.txt', '.ini'] or source.name == 'CMakeLists.txt':
        try:
            patch.extend(difflib.unified_diff(prior.read_text(encoding='utf-8').splitlines(keepends=True) if prior.exists() else [], data.decode('utf-8').splitlines(keepends=True), fromfile='before/' + rel, tofile='after/' + rel))
        except UnicodeDecodeError:
            pass
write(S / 'source-manifest.json', manifest)
(S / 'source-changes.patch').write_text(''.join(patch), encoding='utf-8')
validation = dict(passed=True, formal_baseline_generation=26, verification_round=27, exe_sha256=digest, state_schema=12,
    part_checkpoints={name: dict(validation=str(S / 'parts' / name / 'validation.json'), exe_sha256=value['exe_sha256'], scenes=len(value['scenes']), frames=sum(s['frames'] for s in value['scenes'])) for name, value in parts.items()},
    final_build_inputs_match_returns_checkpoint=True, paired_scenes=40, paired_frames=22510,
    independent_default_budget_scenes=1, independent_default_budget_frames=901,
    independent_internal_observer_scenes=4, independent_internal_observer_frames=4054,
    independent_connection_observer_scenes=12, independent_connection_observer_frames=6712,
    probes=93, new_fragment_cases=262144, source_content_verified=True, diagnostics_removed=True,
    strict_ordered_audit_passed=True, frame_comparison_passed=True, default_rules_full_budget_exhaustion_verified=True,
    budget_scope=budget['scope'], source_files=len(manifest), production_c_sources=171, content_inputs=285,
    preservation=preservation, unsupported_guards=37, curved_bidirectional_runtime_verified=True,
    curved_height_bidirectional_runtime_verified=True, curved_occupied_exit_runtime_verified=True,
    original_equivalent_stall_scenes=2, completed_connection_scenes=10, all_curved_height_routes_complete=False,
    tube_approach_runtime_verified=True, tube_height_runtime_verified=True, tube_entry_runtime_verified=True,
    tube_horizontal_runtime_verified=True, occupied_exit_runtime_verified=True,
    previous_sample_real_scene_verified=True, internal_runtime_evidence=str(S / 'internal-real-scenes.json'),
    new_rare_branch_runtime_hits_independently_recorded=True, rare_branch_evidence_scope=tubes['scope'] + ' ' + internal['scope'],
    all_rare_branches_verified=False, nonprimary_overlapping_adapter_naturally_observed=internal['nonprimary_overlapping_adapter_naturally_observed'],
    alternate_saved_segment_pointer_real_scene_verified=False, connection_runtime_evidence=str(S / 'connection-real-scenes.json'),
    report=str(report), handoff=str(handoff), **flags)
write(S / 'validation.json', validation)
recovery = read(S / 'baseline/project/reports/latest-recovery.json')
recovery.update(validation=str(S / 'validation.json'), sha256=digest, executable=str(exe), formal_baseline_generation=26,
    verification_round=27, paired_scenes=40, paired_frames=22510, probes=93, new_fragment_cases=262144,
    production_c_sources=171, content_inputs=285, report=str(report), handoff=str(handoff), budget_exhaustion_evidence=str(S / 'budget-real-scenes.json'), **flags)
recovery.update(independent_internal_observer_scenes=4, independent_internal_observer_frames=4054,
    independent_connection_observer_scenes=12, independent_connection_observer_frames=6712,
    curved_height_bidirectional_runtime_verified=True, curved_occupied_exit_runtime_verified=True,
    original_equivalent_stall_scenes=2, completed_connection_scenes=10, all_curved_height_routes_complete=False, previous_sample_real_scene_verified=True,
    internal_runtime_evidence=str(S / 'internal-real-scenes.json'), connection_runtime_evidence=str(S / 'connection-real-scenes.json'),
    next_readable_region='Remaining internal type/template classifiers; establish legal nonprimary overlap callers; combined curved height/occupied exits and bridge-layer object chains',
    previous_recovery_validation=str(R / 'evidence/movement-state-v26/validation.json'), previous_recovery_executable=str(S / 'baseline/ra2/build-original-c/ra2.exe'),
    previous_recovery_sha256=sha(S / 'baseline/ra2/build-original-c/ra2.exe'), all_rare_branches_verified=False,
    nonprimary_overlapping_adapter_naturally_observed=internal['nonprimary_overlapping_adapter_naturally_observed'])
write(P / 'reports/latest-recovery.json', recovery)
write(P / 'reports/latest-state-comparison.json', dict(validation=str(S / 'validation.json'), exe_sha256=digest, state_schema=12,
    paired_scenes=40, paired_frames=22510, independent_default_budget_frames=901, independent_connection_observer_frames=6712,
    independent_internal_observer_frames=4054, passed=True, strict_ordered_audit_passed=True, first_difference=None,
    full_original_equivalence_verified=False, default_rules_full_budget_exhaustion_verified=True, budget_scope=budget['scope'], report=str(report)))
write(P / 'reports/latest-movement-candidate.json', dict(passed=True, status='promoted', formal_baseline_generation=26,
    verification_round=27, executable=str(exe), exe_sha256=digest, validation=str(S / 'validation.json'), full_original_equivalence_verified=False, report=str(report)))
for item in manifest:
    assert sha(R / item['path']) == sha(S / 'final-source' / item['path']) == item['sha256'], item['path']
write(S / 'final-check.json', dict(passed=True, source_files=len(manifest), source_archive_matches_live=True, formal_pointers_match=True,
    old_baselines_preserved=True, exe_sha256=digest, report_sha256=sha(report), handoff_sha256=sha(handoff), reading_guide_sha256=sha(guide)))
print(json.dumps(dict(passed=True, formal_baseline=26, exe_sha256=digest, source_files=len(manifest), handoff=str(handoff)), ensure_ascii=False))
