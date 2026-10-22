"""Promote only after the production matrix and independent default-rule scene pass."""
from pathlib import Path
import difflib,hashlib,json,re,shutil
R=Path(__file__).resolve().parent;P=R.parent.parent;S=R/'evidence/movement-state-v12'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,x):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def rows(tag,mode='original'):
    return [json.loads(l) for l in (S/'runs'/tag/mode/'state.jsonl').open(encoding='utf-8')]
assert not (S/'validation.json').exists()
accept=read(S/'strict-acceptance.json');budget=read(S/'budget-real-scenes.json')
assert accept['passed'] and accept['paired_scenes']==27 and accept['paired_frames']==14897
assert budget['passed'] and budget['default_rules_full_exhaustion_verified']
exe=R/'ra2/build-original-c/ra2.exe';digest=sha(exe)
assert digest==accept['exe_sha256']==budget['formal_executable_sha256']
receipt=read(R/'ra2/build-original-c/source-content-receipt.json')
assert receipt['executable_sha256']==digest and receipt['source_count']==114 and receipt['refreshed_count']==0
for name,value in receipt['inputs'].items():assert sha(Path(name))==value,name
default=read(S/'runs/c-score-default/comparison.json');c=default['comparison']
assert default['passed'] and default['exe_sha256']==digest and default['scenario_rules_sha256'] is None
assert c['frames_compared']==c['equal_frames']==c['consecutive_equal_frames']==901
assert c['first_difference'] is None and c['command_difference'] is None and c['rng_equal_all_frames']
assert c['negative_control']['passed'] and c['negative_control']['missing_frame_rejected']
for run in default['runs']:assert run['passed'] and run['save_before']==run['save_after']
select=lambda seq:[r for r in seq if r['kind'] in ('submit','execute','movement-audit') or r['kind'].startswith('fixture-')]
assert select(rows('c-score-default'))==select(rows('c-score-default','generated-c'))
old=read(S/'runs/a-walk/comparison.json');assert not old['passed'] and old['comparison']['first_difference']['frame']==28
for mode in ['original','generated-c']:
    f28=next(r for r in rows('c-score-default',mode) if r['kind']=='state' and r['frame']==28)
    assert next(o for o in f28['objects'] if o['id']==1032262)['position'][0]==17343
assert (R/'ra2/src/runtime/state_trace.c').read_bytes()==(S/'baseline/ra2/src/runtime/state_trace.c').read_bytes()
for rel in ['reports/latest-recovery.json','reports/latest-state-comparison.json','reports/latest-movement-candidate.json']:
    assert (P/rel).read_bytes()==(S/'baseline/project'/rel).read_bytes(),rel

# Verify preserved, immutable checkpoints against their own manifests, not live files.
counts={}
archives=[('v9',R/'evidence/movement-state-v9','source-manifest.json','final-source'),
    ('v10',R/'evidence/movement-state-v10','source-manifest.json','final-source'),
    ('v11',R/'evidence/movement-state-v11','source-manifest.json','final-source'),
    ('v12-baseline',S/'baseline','source-manifest.json',''),
    ('walk-verified',S/'parts/walk-verified','manifest.json',''),
    ('path-cache-verified',S/'parts/path-cache-verified','source-manifest.json','')]
for label,base,manifest_name,subdir in archives:
    entries=read(base/manifest_name)
    for e in entries:assert sha(base/subdir/e['path'])==e['sha256'],(label,e['path'])
    counts[label]=len(entries)
for name in ['allied-collision-verified','terrain-tail-verified']:
    base=R/'evidence/movement-state-v10/parts'/name;entries=read(base/'manifest.json')
    for e in entries:assert sha(base/e['path'])==e['sha256'],(name,e['path'])
    counts[name]=len(entries)
inputs=read(R/'evidence/original-inputs-before.json')
for e in inputs:assert sha(Path('H:/开发/运行版本/原版1.006')/e['name'])==e['sha256']
counts['H_originals']=len(inputs)
assert sha(R/'ra2/game/game.exe')=='fe67fdac5073530a79baec14c4e072b5e7e4c0c462cee9659870c5330e9e6e3e'
assert sha(R/'ra2/game/SAVE0029.SAV')=='8a2e04fb4412aa5e51b6ffeacc5cb9fe265682d880966d39c1826dc810768b3b'
assert sha(P/'build/ra2battle.exe')=='05d7221ffacdddb2a300aee2c51b61d1fa1d269a5336a08e0c68b023f51bdd27'
guards=sum(len(re.findall(r'ra2_recovery_unimplemented\((0x[0-9A-Fa-f]+)',p.read_text(encoding='utf-8'))) for p in (R/'ra2/src/recomp/gen_game').glob('*.c'))
assert guards==37
preservation=dict(passed=True,counts=counts,game_save_old_engine_preserved=True,unsupported_guards=guards)
write(S/'preservation.json',preservation)

walk=dict(passed=True,first_old_difference=old['comparison']['first_difference'],final_scene='c-score-default',final_frames=901,
    root_cause='71F410 adds a tiny negative X displacement under original x87 53-bit toward-zero arithmetic; host nearest double rounds the sum back to 17344 before integer conversion.',
    original_x=17343,old_c_x=17344,new_c_x=17343,original_arithmetic_control='0xE7F',
    implementation='ra2_walk_advance_axis in gameplay/walk_movement.c',numeric_cases=1572864,
    instructions=['71F3F2..71F3FA Y multiply/subtract/convert','71F40C..71F417 X multiply/add/convert'],
    numeric_scope='finite bounded coordinates; original arithmetic instruction sequence and mapped 77F110 integer conversion',
    diagnostics_removed=True,diagnostic_checkpoint='diagnostic-walk',full_infantry_process_readable=False)
write(S/'walk-investigation.json',walk)
path=dict(passed=True,scoring_entry='42786C..42787A',priority_entry='427E75..427E7E',
    generation_entries=['4277BD','4277F2'],cache_compare_entries=['4277C6..4277D4','4277FB..427809'],
    scoring_copies=6,generation_copies=10,cache_compare_copies=10,
    readable_files=['ra2/src/gameplay/ground_path_cost.h','ra2/src/gameplay/ground_path_cost.c','ra2/src/gameplay/ground_path_cache.h','ra2/src/gameplay/ground_path_cache.c'],
    old_accumulation_preserved=True,step_cases=786432,cache_cases=786432,priority_cases=786432,
    original_distance_approximation_preserved=True,whole_search_heap_and_cache_storage_readable=False,finite_nonnegative_scope=True)
write(S/'path-score-cache.json',path)

# Reconcile early 27-scene observations with the new, separately constructed real scene.
conditions=read(S/'budget-conditions.json')
conditions['original_27_natural_budget_entries']=conditions.pop('natural_budget_entries')
conditions['original_27_scenes_without_budget_entry']=conditions.pop('all_natural_scenes_no_budget_entry')
conditions.update(natural_exhaustion_verified=True,default_rules_full_exhaustion_verified=True,
    natural_budget_scope=budget['scope'],new_real_scene_evidence=str(S/'budget-real-scenes.json'),
    natural_budget_entries=budget['scenes']['h-default-budget']['modes']['original']['budget_events'],
    new_static_followup=budget['callback_scope'],necessary_conditions=budget['necessary_conditions'])
ordinary=conditions.get('ordinary_drive_failure_analysis',{})
ordinary.update(main_search_failure='Stop clears the Drive destination, but subsequent AI failure callbacks may restore a destination before failed Prepare returns.',
    conclusion='The same Drive alone does not exclude budget consumption. Default-rule AI TRUCKA scene verifies restored goals and natural exhaustion when goals remain beyond CloseEnough.')
ordinary['assumptions'].append('The earlier no-consumption inference also requires callbacks not to restore a destination; the new default-rule AI scene does not satisfy that extra premise.')
conditions['ordinary_drive_failure_analysis']=ordinary
conditions['unresolved']=['Exact 4C3895 callback site is not separately hooked.','Unassisted random-match occurrence frequency is not established.','Whole game equivalence and complete readable path search remain unfinished.']
write(S/'budget-conditions.json',conditions)
effect=read(S/'effects.json');effect['budget'].update(default_rules_full_exhaustion_verified=True,natural_exhaustion_verified=True,
    natural_scope=budget['scope'],real_scene_evidence=str(S/'budget-real-scenes.json'))
effect_budget=effect['budget']
effect_budget['legacy_controlled_and_one_cell_scenes']={key:effect_budget.pop(key) for key in ['entry_calls','countdown','natural_test_constraints','natural_test_failure_budget_values','natural_test_failed_rebuild_observed','limitation']}
effect_budget['normal_pathfinding_exhaustion_verified']=True
effect_budget['natural_budget_events']=budget['scenes']['h-default-budget']['modes']['original']['budget_events']
effect_budget['natural_stop_frame']=38
effect_budget['limitation']=budget['scope']
effect['infantry_frame28']=walk;effect['path_score_cache']=path;write(S/'effects.json',effect)
accept.update(paired_scenes=28,paired_frames=15798,production_default_skirmish_frames=901,production_default_skirmish='c-score-default',
    natural_budget_exhaustion_verified=True,natural_budget_scope=budget['scope'],independent_budget_frames=901,
    full_original_equivalence_verified=False)
write(S/'strict-acceptance.json',accept)

report=P/'docs/单位移动第十一批-步兵步进与路径评分缓存-20261022.txt'
handoff=P/'交接文档-单位移动第十一批正式验收-20261022.txt'
report_text=f'''单位移动第十一批：步兵步进、路径评分与缓存（2026-10-22）

一、已验收结果与边界

默认遭遇战步兵第 28 帧差异已解决。新正式基线代次 11，验证轮次 12。
程序：{exe}
SHA-256：{digest}
正式验收：{S/'validation.json'}
严格验收：{S/'strict-acceptance.json'}
原有 27 场景、14897 帧全部重新通过，另加入默认遭遇战 0..900 共 901 帧：合计 28 场景、15798 帧。
对象状态、RNG、外部命令和全部内部有序观测一致；比较器未修改，位移 +1 与缺帧反例仍被拒绝。
固定 SAVE0029.SAV、seed 12345、2190..3000 的窗口继续通过，包含旧第 2247 帧。
三格包围第 52 帧的修正保持通过，未重新引入额外查询。
墙、闸门、临时/隐形障碍、友方几何、零速度地形、转弯接续及二次补建失败均通过原有实景效果门槛。
42 组原版片段/数值检查通过：旧 40 组加步兵单轴与评分缓存两组。
新增步兵 1572864 例；评分、缓存、优先级各 786432 例，共新增 3932160 例。
菜单、无诊断运行及非法对象命令拒绝等辅助检查通过。
上述仍是明确范围内的等价验证，全游戏等价没有完成。

二、第 28 帧步兵差异

旧原版 X=17343，旧 C X=17344；单位 1032262，Walk locomotor，而非已整理的 Ground Drive。
71F410 的极小负方向分量乘速度后与整数起点相加。原版 x87 使用 53 位精度、向零舍入；
宿主默认就近舍入把结果重新舍回 17344，再截断也无法恢复原版结果。
新 walk_movement.c 以命名函数 ra2_walk_advance_axis(origin, direction_component, speed, subtract_step, arithmetic_control, conversion_control)
分别执行乘法、坐标加减、整数转换。沿用现有纯 C 旧数值层，不按帧号、对象编号或坐标打特判。
walk_movement_bridge.c 只读取旧栈/寄存器、处理 FPU 栈和返回约定；生成外壳在 X/Y 两个原位置调用。
默认遭遇战 901 帧及固定存档 811 帧先单独验证，保存 walk-verified 回退节点后才整理评分。
数值检查覆盖 24/53/64 位精度、四种舍入、两轴方向、极小正负分量；硬件原指令序列与映射原版整数转换对照通过。
数值接口限定有限、32 位坐标范围内的数据，未声明通用非有限数或溢出模拟。
诊断程序与失败日志保留在 diagnostic-walk、a-walk，正式 state_trace.c 已恢复为原基线内容。

三、可读路径评分与缓存

gameplay/ground_path_cost.c：
  ra2_ground_score_path_step：通行代价 × 搜索权重 + 方向偏置，再按原版精度/舍入保存 float。
  ra2_ground_accumulate_path_cost：父节点累计代价 + 本步代价；保留上轮已验收的第 52 帧修正。
  ra2_ground_path_priority：原版近似距离 + 累计代价，按原版方式保存队列优先级。
gameplay/ground_path_cache.c：
  ra2_ground_path_cache_is_current：条目 generation 是否属于本轮搜索。
  ra2_ground_path_cache_compare：比较 cached_cost 与 parent_cost + epsilon；严格小于时跳过该候选的通行查询。
原近似距离服务 4BA410 仍保留；不能随意换成 sqrt。epsilon、偏置、权重由旧外壳读取原值。
评分六处、generation 与缓存判断各十处生成展开已接入命名函数；保留查询顺序及旧标志适配。
接口参数和纯 C 逻辑可直接阅读修改；缓存内存布局、寻路堆 427929..427C96 及完整搜索循环仍在生成外壳，尚待继续整理。
默认精度近似替代会改变候选顺序；制作 MOD 时优先改上层权重/规则输入，修改数值策略须重新对照。
原版片段对照：步评分和缓存直接执行映射片段，优先级执行同一原指令序列；全部有限非负测试通过。
先通过三格包围 101 帧与默认遭遇战 901 帧并保存 path-cache-verified，再跑完整矩阵。

四、默认规则下失败预算自然耗尽：已补齐实景

独立实景工具：{S/'truck-actor-fixture-probe.exe'}
SHA-256：{budget['fixture_executable_sha256']}
此工具只替换测试摆放器对象，其他 113 个生产构建对象与正式程序一致；对象哈希、编译和链接参数见 truck-actor-fixture-receipt.json。
原版遭遇战菜单进入同一地图，seed 12345，未加载 SAV，未使用独立 RULES 覆盖；CloseEnough 保持 2.25，即 576 世界单位。
第 27 帧通过原版构造、摆放、任务排队与 SetDestination 服务创建一辆 AI TRUCKA，格子 87,122，初始命令去 67,124。
随后通过正常摆放服务创建 16 辆敌对 TRUCKA，半径 2，封闭边界；无跳过格。
原版车辆/地形规则未改；未直接写预算、队列、移动目标或碰撞结果，未强制调用寻路/预算入口。
初始创建与移动命令属于显式实景构造；后续搜索失败、AI 回退和预算消耗完全由正常游戏更新触发。
这证明默认规则可合法自然耗尽，不代表一场未干预随机对局已自然遇到同一布置。

e-truck-closed：241 帧严格通过；h-default-budget：延长到 901 帧仍全部严格一致。
第 27..37 帧预算入口值依次为 10、9、8、7、6、5、4、3、2、1、0。
失败 Prepare 返回时是同一个 Drive，且回调恢复了有效目标。各次目标距离均超过原版 CloseEnough，避免近距离停止提前结束。
第 38 帧预算保持 0、目标与当前路径段清空；38..240 帧确认停止。
预算证据：{S/'budget-real-scenes.json'}
同一 Drive 不足以推出“不会扣预算”：停止后的 AI 回调可能赋予新目标。
静态回调链 4C3895 -> 7053F0 -> 4C8030 -> MoveTo 4C8165 由原版反汇编与状态支持；4C3895 本身未额外挂钩，不能称已逐调用直接记录。

负结果保留：d-truck-far-02 的武装 AI 单位转入攻击，预算未扣；e-truck-actor 的摆放器误跳普通覆盖物格，围圈留空，车辆驶出。
修正测试摆放器的空格判断后，所有 16 处由原版服务判断摆放是否合法，不清除地形或已有对象。
原有 explicit budget-entry 与一格主动重寻路仍单独记账，没有拿它们充当本轮自然耗尽证明。

五、构建与保全

C17，无新 C++ 游戏实现。114 个 C 源、170 项内容跟踪输入。头文件变化触发完整新编译；最终无变化构建刷新 0 源，EXE 哈希不变。
新增源使链接参数超过命令行长度限制后，Ninja 响应文件中的中文路径被链接器按错误编码读取。
build-faithful.ps1 在生成的链接响应文件内容开头加 UTF-8 BOM，保留所有对象和路径；无硬编码短路径或缺省删除对象。
正式二进制为完整新编译后的 2d2ae4...；完整哈希见上。
旧代次 9、10 及本轮 baseline、walk-verified、path-cache-verified 源/程序逐个按清单复核，均保留。
H 盘 20 项原始输入、game.exe、SAVE0029.SAV、旧手写引擎及 37 处未支持保护保持原样。
未提交、未推送，没有建立 GitHub 仓库。

六、下一步

继续将完整寻路的节点/缓存读写和优先队列堆整理成命名结构，再整理 Advance 前半段插值及 Prepare 共享入口。
不要只改数值公式后宣布完整寻路可读；节点更新、同分排序和查询短路顺序也必须保留。
步兵目前只整理了两轴坐标推进，完整 Walk Process 仍需分块。
如继续预算调查，可直接在本轮默认规则实景上补 4C3895 精确回调记录，不需重做合法触发条件。
每部分从本轮正式基线独立保存回退；沿用严格状态/RNG/命令/有序内部事件对照，继续保留原始输入。
'''
report.parent.mkdir(parents=True,exist_ok=True);assert not report.exists() and not handoff.exists()
report.write_text(report_text,encoding='utf-8')
handoff.write_text(f'''单位移动第十一批正式验收交接（2026-10-22）

已解决：默认遭遇战步兵第 28 帧；已整理：两轴步进、路径评分/优先级、缓存代次与剪枝比较；已补齐：默认规则自然预算耗尽实景。
正式程序：{exe}
SHA-256：{digest}
正式代次 11 / 验证轮次 12：{S/'validation.json'}
28 场景、15798 帧严格通过；另独立默认规则预算实景 901 帧严格通过；42 组片段/数值检查通过。
预算第 27..37 帧从 10 到 0，第 38 帧目标清空。实景显式创建并下达初始移动命令，后续失败/耗尽自然发生，未覆写默认 RULES。
完整范围、证据和限制：{report}
可读入口：{R/'ra2/src/gameplay/walk_movement.c'}；ground_path_cost.c；ground_path_cache.c。
阅读说明：{R/'ra2/src/gameplay/阅读说明-单位移动.txt'}
本轮完整源码与 EXE：{S/'final-source'}；身份：source-manifest.json / final-check.json。
旧正式代次 10：{S/'baseline/ra2/build-original-c/ra2.exe'}，SHA-256 f40ca4c47e788636e149545112da046a9463f71498797699438a8835e33377b4。
中间回退：{S/'parts/walk-verified'}；{S/'parts/path-cache-verified'}。
下一步：完整寻路节点/缓存更新与优先队列堆；Advance 前半段插值和 Prepare 共享入口；Walk Process 余段。
继续从现有代码与清单接续，不重新生成全库；不提交、不推送。全游戏等价与完整移动可读仍未完成。
''',encoding='utf-8')

guide=R/'ra2/src/gameplay/阅读说明-单位移动.txt'
shutil.copy2(guide,S/'reading-guide-before.txt')
text=guide.read_text(encoding='utf-8')
text='''第十一批当前状态（2026-10-22，优先于下文历史阶段描述）

默认遭遇战步兵第 28 帧已修正；默认规则真实 AI TRUCKA 包围实景已自然耗尽预算。
28 场景 / 15798 帧生产程序严格一致，另预算工具 901 帧严格一致，42 组片段/数值检查通过。
下文早期“默认规则尚未耗尽”“第 28 帧待办”等均为当时历史状态，当前结果见第三十一节与本轮交接。

'''+text
text+='''
三十一、步兵两轴推进、路径评分缓存与默认规则预算实景

walk_movement.h/.c：ra2_walk_advance_axis；可修改方向分量、速度输入及加减方向，保持原版控制字下的运算顺序。
它先乘位移，再与整数起点相加/相减，再转换到整数。极小负位移不可在宿主 double 中提前舍掉。
runtime/walk_movement_bridge.c 只适配旧栈、返回值、标志与 FPU 栈；完整 Walk Process 尚未整理。

ground_path_cost.h/.c：边评分 traversal_cost * search_weight + direction_bias；累计代价 previous_cost + step_cost；优先级 approximate_distance + accumulated_cost。
ground_path_cache.h/.c：generation 相等才复用；cached_cost < parent_cost + epsilon 才提前剪枝。等号边界不可改成 <=。
每一步必须保留原版 x87 精度与 float 保存舍入；近似距离仍调用原版表算法，不直接替换为 sqrt。
纯 C 命名接口已接入全部对应展开；堆、节点结构及缓存写回/淘汰仍在生成外壳，尚非完整可读寻路。
做 MOD 优先调整服务或规则给出的权重/偏置、上层速度/目标输入，并按同样场景对照；数值层负责原版兼容。

默认规则预算：原地图/菜单、固定 seed12345，用正常构造/摆放/任务/目的地服务建立真实 AI TRUCKA 和 16 辆敌对 TRUCKA 圈。
初始移动由测试设置，后续不再调用寻路或预算入口、不直接写目标/队列/预算。CloseEnough 保持原版 576。
第 27..37 帧入口值 10..0，第 38 帧目标清空；241 帧与 901 帧完整对照均通过。
必要条件是 AI 失败回调在同一 Drive 恢复有效目标，且各次目标超出 CloseEnough；无武器角色避免攻击流程打断。
此结果证明默认规则下可合法自然耗尽，不等于未干预随机对局中的出现频率已验证。
精确 4C3895 调用点未单独记录，当前证据为原版静态链、失败返回后的状态及自然恢复入口序列。
'''
guide.write_text(text,encoding='utf-8')
main=P/'交接文档-原版逆向与C重编译-20261020.txt'
assert main.read_bytes()==(S/'baseline/project'/main.name).read_bytes()
main.write_text(main.read_text(encoding='utf-8')+f'\n\n2026-10-22 第十一批正式验收接续入口：{handoff}\n默认遭遇战步兵第 28 帧已修正；两轴步进、路径评分与缓存比较已整理；28 场景 / 15798 帧严格通过。\n默认规则真实 AI 车辆包围场景已验证预算自然耗尽，另 901 帧严格通过；完整游戏等价仍未完成。\n',encoding='utf-8')

paths={e['path'] for e in read(S/'baseline/source-manifest.json')}
paths.update(p.relative_to(R).as_posix() for p in R.glob('*v12*') if p.is_file())
paths.update(['ra2/src/gameplay/walk_movement.c','ra2/src/gameplay/walk_movement.h','ra2/src/runtime/walk_movement_bridge.c','ra2/src/runtime/walk_movement_bridge.h','ra2/src/gameplay/ground_path_cache.c','ra2/src/gameplay/ground_path_cache.h'])
paths.update(p.relative_to(R).as_posix() for p in S.iterdir() if p.is_file() and (p.suffix=='.c' or p.name in ['native_probe_host.h','truck-actor-fixture-build-arguments.json','truck-actor-fixture-probe.exe','truck-actor-fixture-receipt.json']))
paths.update(p.relative_to(R).as_posix() for p in (S/'fixtures').iterdir() if p.is_file())
manifest=[];patch=[]
for rel in sorted(paths):
    src=R/rel;data=src.read_bytes();dest=S/'final-source'/rel;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
    manifest.append(dict(path=rel,sha256=sha(src)))
    prior=S/'baseline'/rel
    if prior.exists() and prior.read_bytes()==data:continue
    if src.suffix.lower() in ['.c','.h','.py','.ps1','.txt','.ini'] or src.name=='CMakeLists.txt':
        try:patch.extend(difflib.unified_diff(prior.read_text(encoding='utf-8').splitlines(keepends=True) if prior.exists() else [],data.decode('utf-8').splitlines(keepends=True),fromfile='before/'+rel,tofile='after/'+rel))
        except UnicodeDecodeError:pass
write(S/'source-manifest.json',manifest);(S/'source-changes.patch').write_text(''.join(patch),encoding='utf-8')
validation=dict(passed=True,formal_baseline_generation=11,verification_round=12,exe_sha256=digest,state_schema=12,
    paired_scenes=28,paired_frames=15798,independent_default_budget_scenes=1,independent_default_budget_frames=901,
    probes=42,new_numeric_cases=3932160,source_content_verified=True,diagnostics_removed=True,strict_ordered_audit_passed=True,
    frame_comparison_passed=True,default_rules_full_budget_exhaustion_verified=True,budget_scope=budget['scope'],
    source_files=len(manifest),preservation=preservation,unsupported_guards=37,full_original_equivalence_verified=False,
    whole_ground_movement_readable=False,whole_infantry_process_readable=False,whole_search_heap_and_cache_storage_readable=False,
    report=str(report),handoff=str(handoff))
write(S/'validation.json',validation)
recovery=read(S/'baseline/project/reports/latest-recovery.json')
recovery.update(validation=str(S/'validation.json'),sha256=digest,executable=str(exe),formal_baseline_generation=11,verification_round=12,
    normal_budget_exhaustion_verified=True,default_rules_full_budget_exhaustion_verified=True,budget_exhaustion_evidence=str(S/'budget-real-scenes.json'),
    budget_scope=budget['scope'],infantry_frame28_fixed=True,path_score_cache_comparison_readable=True,
    whole_path_search_readable=False,report=str(report),handoff=str(handoff),next_difference=None,
    next_readable_region='Full path node/cache storage and heap; Advance front/interpolation, Prepare shared entries; remaining Walk Process',
    previous_recovery_validation=str(R/'evidence/movement-state-v11/validation.json'),
    previous_recovery_executable=str(S/'baseline/ra2/build-original-c/ra2.exe'),previous_recovery_sha256=sha(S/'baseline/ra2/build-original-c/ra2.exe'))
write(P/'reports/latest-recovery.json',recovery)
write(P/'reports/latest-state-comparison.json',dict(validation=str(S/'validation.json'),exe_sha256=digest,state_schema=12,
    paired_scenes=28,paired_frames=15798,independent_default_budget_frames=901,passed=True,strict_ordered_audit_passed=True,
    first_difference=None,full_original_equivalence_verified=False,normal_budget_exhaustion_verified=True,
    legal_rules_natural_budget_exhaustion_verified=True,default_rules_full_budget_exhaustion_verified=True,budget_scope=budget['scope'],
    infantry_frame28_fixed=True,additional_known_difference=None,report=str(report)))
write(P/'reports/latest-movement-candidate.json',dict(passed=True,status='promoted',formal_baseline_generation=11,verification_round=12,
    executable=str(exe),exe_sha256=digest,validation=str(S/'validation.json'),full_original_equivalence_verified=False,report=str(report)))
for e in manifest:assert sha(R/e['path'])==sha(S/'final-source'/e['path'])==e['sha256'],e['path']
assert sha(exe)==digest and read(P/'reports/latest-recovery.json')['sha256']==digest
write(S/'final-check.json',dict(passed=True,source_files=len(manifest),source_archive_matches_live=True,formal_pointers_match=True,
    old_baselines_preserved=True,exe_sha256=digest,report_sha256=sha(report),handoff_sha256=sha(handoff),
    reading_guide_sha256=sha(guide),main_previous_sha256=sha(S/'baseline/project'/main.name),main_current_sha256=sha(main)))
print(json.dumps(dict(passed=True,formal_baseline=11,exe_sha256=digest,source_files=len(manifest),handoff=str(handoff)),ensure_ascii=False))
