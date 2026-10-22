"""Generation 12 promotion after heap/node and complete bounded regression gates."""
from pathlib import Path
import difflib,hashlib,json,re,shutil
R=Path(__file__).resolve().parent;P=R.parent.parent;S=R/'evidence/movement-state-v13'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,x):
    p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def rows(tag,mode='original'):
    return [json.loads(l) for l in (S/'runs'/tag/mode/'state.jsonl').open(encoding='utf-8')]
assert not (S/'validation.json').exists()
accept=read(S/'strict-acceptance.json');budget=read(S/'budget-real-scenes.json')
assert accept['passed'] and accept['paired_scenes']==27 and accept['paired_frames']==14897
assert budget['passed'] and budget['default_rules_full_exhaustion_verified']
exe=R/'ra2/build-original-c/ra2.exe';digest=sha(exe)
assert digest==accept['exe_sha256']==budget['formal_executable_sha256']
receipt=read(R/'ra2/build-original-c/source-content-receipt.json')
assert receipt['executable_sha256']==digest and receipt['source_count']==118 and receipt['refreshed_count']==0
for name,value in receipt['inputs'].items():assert sha(Path(name))==value,name
default=read(S/'runs/c-nodes-default/comparison.json');c=default['comparison']
assert default['passed'] and default['exe_sha256']==digest and default['scenario_rules_sha256'] is None
assert c['frames_compared']==c['equal_frames']==c['consecutive_equal_frames']==901
assert c['first_difference'] is None and c['command_difference'] is None and c['rng_equal_all_frames']
assert c['negative_control']['passed'] and c['negative_control']['missing_frame_rejected']
for run in default['runs']:assert run['passed'] and run['save_before']==run['save_after']
select=lambda seq:[r for r in seq if r['kind'] in ('submit','execute','movement-audit') or r['kind'].startswith('fixture-')]
assert select(rows('c-nodes-default'))==select(rows('c-nodes-default','generated-c'))
for mode in ['original','generated-c']:
    f28=next(r for r in rows('c-nodes-default',mode) if r['kind']=='state' and r['frame']==28)
    assert next(o for o in f28['objects'] if o['id']==1032262)['position'][0]==17343
assert (R/'ra2/src/runtime/state_trace.c').read_bytes()==(S/'baseline/ra2/src/runtime/state_trace.c').read_bytes()
for rel in ['reports/latest-recovery.json','reports/latest-state-comparison.json','reports/latest-movement-candidate.json']:
    assert (P/rel).read_bytes()==(S/'baseline/project'/rel).read_bytes(),rel
assert read(S/'parts/nodes-cache-verified/validation.json')['exe_sha256']==digest
assert read(S/'refactor-structure.json')['passed']
heap_probe=read(S/'path-heap-probe-verified-01.json');nodes_probe=read(S/'path-nodes-probe-verified-01.json')
assert heap_probe['passed'] and nodes_probe['passed']
new_cases=sum(heap_probe[k] for k in ['offer_cases','take_cases','tail_cases'])+sum(nodes_probe[k] for k in ['node_cases','publish_cases','reset_cases'])
assert new_cases==429268

counts={}
archives=[(f'v{v}',R/f'evidence/movement-state-v{v}','source-manifest.json','final-source') for v in [9,10,11,12]]
archives += [('v13-baseline',S/'baseline','source-manifest.json','')]
archives += [(name,S/'parts'/name,'manifest.json','') for name in ['heap-verified','nodes-cache-verified']]
archives += [(name,R/'evidence/movement-state-v12/parts'/name,manifest,'') for name,manifest in [('walk-verified','manifest.json'),('path-cache-verified','source-manifest.json')]]
for label,base,manifest_name,subdir in archives:
    entries=read(base/manifest_name)
    for e in entries:assert sha(base/subdir/e['path'])==e['sha256'],(label,e['path'])
    counts[label]=len(entries)
incomplete=S/'investigations/heap-before-inc-rule'
for e in read(incomplete/'manifest.json'):assert sha(incomplete/e['path'])==e['sha256']
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

conditions=read(S/'budget-conditions.json')
conditions['original_27_natural_budget_entries']=conditions.pop('natural_budget_entries')
conditions['original_27_scenes_without_budget_entry']=conditions.pop('all_natural_scenes_no_budget_entry')
conditions.update(natural_exhaustion_verified=True,default_rules_full_exhaustion_verified=True,natural_budget_scope=budget['scope'],
    new_real_scene_evidence=str(S/'budget-real-scenes.json'),natural_budget_entries=budget['scenes']['h-default-budget']['modes']['original']['budget_events'],
    new_static_followup=budget['callback_scope'],necessary_conditions=budget['necessary_conditions'])
ordinary=conditions['ordinary_drive_failure_analysis']
ordinary.update(main_search_failure='Stop clears the Drive destination; later AI failure callbacks can restore it before failed Prepare returns.',
    conclusion='The default-rule AI TRUCKA fixture continues to exhaust its normal budget naturally with a restored goal in the same Drive.')
ordinary['assumptions'].append('Earlier no-consumption inference also requires callbacks not to restore a destination; the default-rule AI scene does not satisfy that extra premise.')
conditions['unresolved']=['Exact 4C3895 callback site is not separately hooked.','Untouched random-match frequency is not measured.','Complete search loop and full-game equivalence remain unfinished.']
write(S/'budget-conditions.json',conditions)
effect=read(S/'effects.json');eb=effect['budget']
eb['legacy_controlled_and_one_cell_scenes']={k:eb.pop(k) for k in ['entry_calls','countdown','natural_test_constraints','natural_test_failure_budget_values','natural_test_failed_rebuild_observed','limitation']}
eb.update(normal_pathfinding_exhaustion_verified=True,natural_exhaustion_verified=True,default_rules_full_exhaustion_verified=True,
    natural_scope=budget['scope'],real_scene_evidence=str(S/'budget-real-scenes.json'),natural_budget_events=conditions['natural_budget_entries'],natural_stop_frame=38)
effect['path_heap']=dict(readable=True,integration=read(S/'heap-integration.json'),native_probe=heap_probe,
    deferred_candidate_rule='INC at 427939 supplies the branch zero flag. For normal counts, enqueue the old pending candidate and defer the new candidate, regardless of their relative scores.',
    tie_rule='heap root wins against equal pending candidate; sift uses strict comparison and prefers left among equal children')
effect['node_cache']=dict(readable=True,integration=read(S/'node-cache-integration.json'),native_probe=nodes_probe,
    generation_wrap_scope='mapped original reset fragment; not 2^32 real searches',node_heuristic_tail_still_generated=True)
write(S/'effects.json',effect)
accept.update(paired_scenes=28,paired_frames=15798,production_default_skirmish='c-nodes-default',production_default_skirmish_frames=901,
    natural_budget_exhaustion_verified=True,natural_budget_scope=budget['scope'],independent_budget_frames=901,
    whole_search_readable=False,full_original_equivalence_verified=False)
write(S/'strict-acceptance.json',accept)

report=P/'docs/单位移动第十二批-寻路堆与节点缓存-20261022.txt'
handoff=P/'交接文档-单位移动第十二批正式验收-20261022.txt'
assert not report.exists() and not handoff.exists()
report.write_text(f'''单位移动第十二批：寻路堆、节点与缓存读写（2026-10-22）

一、正式验收

正式代次 12 / 验证轮次 13。
程序：{exe}
SHA-256：{digest}
验收：{S/'validation.json'}
28 场景、15798 帧严格一致；其中原有矩阵 27 场景 14897 帧，默认遭遇战 0..900 共 901 帧。
独立默认规则预算自然耗尽场景另 901 帧严格一致。
对象状态、RNG、外部命令及全部内部有序事件一起比较；比较器保持原样，位移 +1 和缺帧反例均继续被拒绝。
44 组原版片段/数值检查通过：原有 42 组加堆、节点缓存两组，新检查合计 {new_cases} 例。
固定 SAVE0029.SAV、seed12345、2190..3000 窗口通过，包含第 2247 帧；默认步兵第 28 帧与三格包围第 52 帧修正保持通过。
墙、门、隐形/临时障碍、移动友方几何、转弯接续、二次补建失败等既有实景效果门槛再次通过。
菜单、无诊断运行、非法对象命令拒绝等辅助检查通过。全游戏等价仍未完成。

二、可读 C：堆

gameplay/ground_path_heap.h/.c：Ra2SearchNode、Ra2PathHeap、ra2_path_heap_offer、ra2_path_heap_take。
候选暂存、堆上浮、堆下沉、出队、清空均为命名 C 函数。runtime/ground_path_heap_bridge.c 只适配旧寄存器、栈和内部接续入口。
生成展开中 7 处完整入队、11 处完整取出，以及 3 个内部接续入口已接入。
一基下标：0 号槽闲置，capacity-1 为可用节点数。入堆记录地址上/下界，出堆和清空均保留历史界限。
独立 pending 槽表示尚未入堆的候选，不保证它的分数最小。

原版实测细节：427934 fnstsw、427936 test 之后，427939 INC 改写零标志；42793C 实际依据计数递增结果分支。
正常计数下，旧 pending 入堆，新候选留在 pending；满堆时旧候选入堆失败，仍暂存新候选。
不能根据前面的浮点比较，把它改写成“仅在新候选更好时替换”。早期整理误读了这个顺序，原版片段检查第 1 组就抓住差异。
未通过的数值记录和候选程序保存在 investigations/heap-before-inc-rule；没有升级那个版本。
堆根与 pending 同分时取堆根；下沉只在严格更小时交换，左右同分保留左侧优先。
映射原版片段：入队 {heap_probe['offer_cases']} 例、取出 {heap_probe['take_cases']} 例、内部接续 {heap_probe['tail_cases']} 例。
覆盖空堆、满堆、同分、不同分数及节点地址界限；有限评分范围。

三、可读 C：节点和缓存

gameplay/ground_path_nodes.h/.c：Ra2PathLink、Ra2PathNodeStorage、Ra2PathNodeInput、Ra2PathNodeCache、Ra2PathRegionCache。
ra2_path_node_create 按原顺序追加节点与路径链，保留父链、路径长度和累计代价；根节点从上下文继承表面高度。
后继节点按原版的桥面连接关系决定地面高度或地面 +4，累计代价仍使用此前已验收的纯 C 旧数值层。
节点构造尾部的坐标距离计算及原版近似距离服务仍由旧外壳提供；不是整段搜索循环都已可读。

ra2_path_cache_read_stamp/read_cost/write_cost/publish：显式区分地面和上层缓存。
generation 相同才使用该轮次数据；发布顺序为先写代次，再写累计代价。旧代价不逐轮清零，避免无谓清图。
主搜索对应的代次比较 10 段、已访问检查 14 段、代价读取 10 处、完整发布 9 处及代价发布接续 1 处已接入命名接口。
ra2_path_search_reset 复用节点池、链池和两个堆；代次自然递增。仅当它回绕为 0 时，清两层格子标记及九组区域标记，再从 1 开始。
reset 保留旧代价值、堆容量与历史地址界限，保持原版行为。
原版片段检查：节点分配/表面继承 {nodes_probe['node_cases']} 例；缓存发布 {nodes_probe['publish_cases']} 例；重置与代次边界 {nodes_probe['reset_cases']} 例。
代次回绕是映射原版片段的边界验证，没有声称实景中已执行 2^32 次搜索。
当前接口按原版合法存储容量和有限代价使用；没有增加池扩容、缓存新策略或 MOD 规则变化。

四、逐块实景及预算持续验证

堆完成后：b-heap-default 901 帧、b-heap-ur3 351 帧、b-heap-budget 901 帧均严格通过，保存 heap-verified。
节点缓存接入后：c-nodes-default 901 帧、c-nodes-ur3 101 帧、h-default-budget 901 帧严格通过，保存 nodes-cache-verified。
随后扩展完整既有 27 场景矩阵，与上述默认遭遇战共同组成正式 28 场景。
默认规则预算场景维持上一轮构造：原版菜单/地图，seed12345，默认 RULES，CloseEnough=576。
仅通过正常服务创建真实 AI TRUCKA、下达一次初始移动命令、摆放 16 辆敌对 TRUCKA；后续由正常游戏更新自行失败和恢复。
未直接写预算、路径队列或目标，未强制调用寻路或预算入口。
第 27..37 帧预算入口值继续按 10..0 出现，第 38 帧目标与当前路径段清空；38..240 帧确认保持停止。
同一 Drive 的失败 Prepare 返回时目标仍有效，AI 回退目标保持在默认 CloseEnough 之外。
此证据来自显式构造的真实游戏对象场景，不等于未干预随机对局的出现频率已经验证。
工具：{S/'truck-actor-fixture-probe.exe'}
工具 SHA-256：{budget['fixture_executable_sha256']}
只有测试摆放器对象与正式程序不同，其余 117 个生产构建对象一致；见 truck-actor-fixture-receipt.json。
预算明细：{S/'budget-real-scenes.json'}
精确 4C3895 回调点仍未单独挂钩；静态链与失败后目标状态证据沿用并复核，不夸称逐调用直接记录。

五、保全与接续

118 个 C 源、{len(receipt['inputs'])} 项构建输入完成内容核对；本轮头文件变化触发完整新编译，最终无变化构建刷新 0 源，EXE 哈希不变。
纯 C17，新的业务逻辑均通过 /W4 /WX；正式 state_trace.c 与前正式基线一致，没有新增诊断写入。
旧正式基线、两个本轮回退节点、失败候选、原始输入和旧手写引擎均保留；37 处未支持保护保持。
源码身份：source-manifest.json、source-changes.patch、final-check.json；构建身份：source-content-receipt.json。
未提交、未推送，未建立远程仓库。

下一步优先整理完整搜索邻居循环、区域连通判断与剩余节点坐标/距离尾部，再整理 Advance 插值及 Prepare 共享入口。
制作 MOD 可从命名输入、评分函数和缓存/堆接口入手；改策略后仍须走独立候选与原版对照，不直接覆盖已验收基线。
完整寻路和完整单位移动仍未全部变成命名 C；继续从本轮正式源接续，不重新生成全库。
''',encoding='utf-8')
handoff.write_text(f'''单位移动第十二批正式验收交接（2026-10-22）

寻路堆、节点/路径链分配、两层缓存读写/发布和搜索重置已整理为命名 C。
正式代次 12 / 验证轮次 13：{S/'validation.json'}
程序：{exe}
SHA-256：{digest}
28 场景 / 15798 帧，另默认规则预算场景 901 帧严格一致；44 组片段/数值检查通过。
默认步兵第 28 帧、第 2247 帧与三格包围第 52 帧旧修正保持通过。
默认预算第 27..37 帧自然经过 10..0，第 38 帧目标清空；实景为正常服务构造的真实车辆圈，默认规则未变。
详细边界、地址和操作顺序：{report}
可读入口：{R/'ra2/src/gameplay/ground_path_heap.h'}；ground_path_heap.c；ground_path_nodes.h/.c。
适配入口：runtime/ground_path_heap_bridge.c；runtime/ground_path_nodes_bridge.c。
原版 pending 槽按最新候选暂存：427939 INC 覆盖前面的比较标志，不能改成只保留最低分。
源码/程序归档：{S/'final-source'}；清单 source-manifest.json；末检 final-check.json。
前正式代次 11：{S/'baseline/ra2/build-original-c/ra2.exe'}，SHA-256 2d2ae4f94d96fb6a8226db4f594a6188c310af67390e20d7269251e933898fd0。
本轮回退：{S/'parts/heap-verified'}；{S/'parts/nodes-cache-verified'}。
下一步：完整搜索邻居循环、区域连通、节点坐标/距离尾部；Advance 插值和 Prepare 共享入口。
全游戏等价未完成；继续保留所有输入、基线和失败证据，暂不提交或推送。
''',encoding='utf-8')
guide=R/'ra2/src/gameplay/阅读说明-单位移动.txt';shutil.copy2(guide,S/'reading-guide-before.txt')
text=guide.read_text(encoding='utf-8')
text='''第十二批当前状态（2026-10-22，优先于下文历史阶段描述）

寻路堆、节点/路径链分配、两层缓存读写与搜索重置已整理。28 场景/15798 帧，另默认预算 901 帧严格一致；44 组检查通过。
完整邻居循环、区域判断和节点距离尾部仍在旧外壳，完整寻路及全游戏等价没有完成。当前入口见第三十二节。

'''+text+'''
三十二、寻路堆与节点缓存的修改入口

ground_path_heap.h/.c：Ra2SearchNode(priority/accumulated_cost/path_length)、Ra2PathHeap；offer/take/clear 是队列入口。
pending 表示暂存候选，不保证最优。原版 427939 的 INC 覆盖评分比较后的零标志，正常计数下总是将旧 pending 入堆并暂存新候选。
满堆时旧候选入堆失败但仍替换 pending；堆根与 pending 同分时先取堆根；下沉用严格比较，左右同分优先左侧。
不要把这段改写成标准“保留最优 pending”，也不要重置出堆后的历史地址界限。新的策略应另建 MOD 候选并验证。

ground_path_nodes.h/.c：Ra2PathLink、Ra2PathNodeStorage、Ra2PathNodeInput；node_create 管理父链、表面高度、累计代价和长度。
cache_read_stamp/read_cost、cache_write_cost/publish 显式区分地面/上层；先检查代次才用代价，publish 先写代次后写代价。
search_reset 归零两个池计数、清两个堆，再递增 generation；仅回绕到零时清两层格子及九组区域标记，然后 generation=1。
代价数组保留旧值，合法性由代次决定。回绕已用映射原版片段验证，不等于实景已跑过 2^32 次搜索。
runtime/ground_path_*_bridge.c 负责旧布局和调用约定；业务文件没有原版固定地址。堆/节点接口目前按合法原版容量与有限评分使用。
完整节点坐标距离尾部、邻居循环、区域连通仍待继续整理；旧近似距离服务没有替换成 sqrt。
每次修改后保留独立候选，继续跑默认遭遇战、预算圈、既有状态矩阵和原版片段检查。
'''
guide.write_text(text,encoding='utf-8')
main=P/'交接文档-原版逆向与C重编译-20261020.txt';assert main.read_bytes()==(S/'baseline/project'/main.name).read_bytes()
main.write_text(main.read_text(encoding='utf-8')+f'\n\n2026-10-22 第十二批正式验收接续入口：{handoff}\n寻路堆、节点/路径链及缓存读写/重置已整理；28 场景15798帧，另默认预算901帧严格通过，44组检查通过。\n下一步为完整搜索邻居循环、区域连通及节点距离尾部；仍不提交、不推送。\n',encoding='utf-8')

paths={e['path'] for e in read(S/'baseline/source-manifest.json')}
paths.update(p.relative_to(R).as_posix() for p in (R/'ra2/src').rglob('*') if p.is_file() and p.suffix in ('.c','.h','.txt'))
paths.update(p.relative_to(R).as_posix() for p in R.glob('*v13*') if p.is_file())
paths.update(p.relative_to(R).as_posix() for p in S.iterdir() if p.is_file() and (p.suffix in ('.c','.h') or p.name in ['truck-actor-fixture-build-arguments.json','truck-actor-fixture-probe.exe','truck-actor-fixture-receipt.json']))
paths.update(p.relative_to(R).as_posix() for p in (S/'fixtures').iterdir() if p.is_file())
paths.update(p.relative_to(R).as_posix() for p in (S/'pending').iterdir() if p.is_file())
manifest=[];patch=[]
for rel in sorted(paths):
    src=R/rel;data=src.read_bytes();dest=S/'final-source'/rel;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data);manifest.append(dict(path=rel,sha256=sha(src)))
    prior=S/'baseline'/rel
    if prior.exists() and prior.read_bytes()==data:continue
    if src.suffix.lower() in ['.c','.h','.py','.ps1','.txt','.ini'] or src.name=='CMakeLists.txt':
        try:patch.extend(difflib.unified_diff(prior.read_text(encoding='utf-8').splitlines(keepends=True) if prior.exists() else [],data.decode('utf-8').splitlines(keepends=True),fromfile='before/'+rel,tofile='after/'+rel))
        except UnicodeDecodeError:pass
write(S/'source-manifest.json',manifest);(S/'source-changes.patch').write_text(''.join(patch),encoding='utf-8')
validation=dict(passed=True,formal_baseline_generation=12,verification_round=13,exe_sha256=digest,state_schema=12,
    paired_scenes=28,paired_frames=15798,independent_default_budget_scenes=1,independent_default_budget_frames=901,
    probes=44,new_fragment_cases=new_cases,source_content_verified=True,diagnostics_removed=True,strict_ordered_audit_passed=True,
    frame_comparison_passed=True,default_rules_full_budget_exhaustion_verified=True,budget_scope=budget['scope'],
    source_files=len(manifest),preservation=preservation,unsupported_guards=37,path_heap_readable=True,node_cache_read_write_readable=True,
    generation_wrap_fragment_verified=True,generation_wrap_naturally_observed=False,node_heuristic_tail_still_generated=True,
    refactor_checks_passed=True,
    whole_path_search_readable=False,whole_ground_movement_readable=False,full_original_equivalence_verified=False,
    report=str(report),handoff=str(handoff))
write(S/'validation.json',validation)
recovery=read(S/'baseline/project/reports/latest-recovery.json')
recovery.update(validation=str(S/'validation.json'),sha256=digest,executable=str(exe),formal_baseline_generation=12,verification_round=13,
    path_heap_readable=True,node_cache_read_write_readable=True,search_generation_wrap_fragment_verified=True,
    whole_path_search_readable=False,report=str(report),handoff=str(handoff),budget_exhaustion_evidence=str(S/'budget-real-scenes.json'),
    next_readable_region='Complete neighbor loop, region connectivity and node coordinate/distance tail; Advance interpolation and Prepare shared entries',
    previous_recovery_validation=str(R/'evidence/movement-state-v12/validation.json'),previous_recovery_executable=str(S/'baseline/ra2/build-original-c/ra2.exe'),
    previous_recovery_sha256=sha(S/'baseline/ra2/build-original-c/ra2.exe'))
write(P/'reports/latest-recovery.json',recovery)
write(P/'reports/latest-state-comparison.json',dict(validation=str(S/'validation.json'),exe_sha256=digest,state_schema=12,paired_scenes=28,paired_frames=15798,
    independent_default_budget_frames=901,passed=True,strict_ordered_audit_passed=True,first_difference=None,full_original_equivalence_verified=False,
    normal_budget_exhaustion_verified=True,default_rules_full_budget_exhaustion_verified=True,budget_scope=budget['scope'],report=str(report)))
write(P/'reports/latest-movement-candidate.json',dict(passed=True,status='promoted',formal_baseline_generation=12,verification_round=13,
    executable=str(exe),exe_sha256=digest,validation=str(S/'validation.json'),full_original_equivalence_verified=False,report=str(report)))
for e in manifest:assert sha(R/e['path'])==sha(S/'final-source'/e['path'])==e['sha256'],e['path']
assert sha(exe)==digest and read(P/'reports/latest-recovery.json')['sha256']==digest
write(S/'final-check.json',dict(passed=True,source_files=len(manifest),source_archive_matches_live=True,formal_pointers_match=True,old_baselines_preserved=True,
    exe_sha256=digest,report_sha256=sha(report),handoff_sha256=sha(handoff),reading_guide_sha256=sha(guide),
    main_previous_sha256=sha(S/'baseline/project'/main.name),main_current_sha256=sha(main)))
print(json.dumps(dict(passed=True,formal_baseline=12,exe_sha256=digest,source_files=len(manifest),handoff=str(handoff)),ensure_ascii=False))
