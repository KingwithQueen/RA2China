"""Promote generation 13 only after all round 14 strict gates pass."""
from pathlib import Path
import difflib,hashlib,json,re,shutil
R=Path(__file__).resolve().parent;P=R.parent.parent;S=R/'evidence/movement-state-v14'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,value):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def rows(tag,mode='original'):
    return [json.loads(l) for l in (S/'runs'/tag/mode/'state.jsonl').open(encoding='utf-8')]
assert not (S/'validation.json').exists()
accept=read(S/'strict-acceptance.json');budget=read(S/'budget-real-scenes.json')
assert accept['passed'] and accept['paired_scenes']==27 and accept['paired_frames']==14897
assert budget['passed'] and budget['default_rules_full_exhaustion_verified']
exe=R/'ra2/build-original-c/ra2.exe';digest=sha(exe)
assert digest==accept['exe_sha256']==budget['formal_executable_sha256']
receipt=read(R/'ra2/build-original-c/source-content-receipt.json')
assert receipt['source_count']==122 and receipt['refreshed_count']==0 and receipt['executable_sha256']==digest
for name,value in receipt['inputs'].items():assert sha(Path(name))==value,name
default=read(S/'runs/b-search-default/comparison.json');c=default['comparison']
assert default['passed'] and default['exe_sha256']==digest and default['scenario_rules_sha256'] is None
assert c['frames_compared']==c['equal_frames']==c['consecutive_equal_frames']==901
assert c['first_difference'] is None and c['command_difference'] is None and c['rng_equal_all_frames']
assert c['negative_control']['passed'] and c['negative_control']['missing_frame_rejected']
assert all(r['passed'] and r['save_before']==r['save_after'] for r in default['runs'])
select=lambda seq:[r for r in seq if r['kind'] in ('submit','execute','movement-audit') or r['kind'].startswith('fixture-')]
assert select(rows('b-search-default'))==select(rows('b-search-default','generated-c'))
for mode in ['original','generated-c']:
    f28=next(r for r in rows('b-search-default',mode) if r['kind']=='state' and r['frame']==28)
    assert next(o for o in f28['objects'] if o['id']==1032262)['position'][0]==17343
for rel in ['reports/latest-recovery.json','reports/latest-state-comparison.json','reports/latest-movement-candidate.json']:
    assert (P/rel).read_bytes()==(S/'baseline/project'/rel).read_bytes(),rel
assert read(S/'parts/search-verified/validation.json')['exe_sha256']==digest
assert read(S/'refactor-structure.json')['passed']
distance=read(S/'path-distance-probe-verified-01.json');search=read(S/'path-search-probe-verified-01.json')
assert distance['passed'] and search['passed'] and search['cases']==8192
assert search['mapped_complete_original_loop'] and search['services_stubbed'] and all(search['stop_cases'])
assert distance['distance_cases']==131072 and distance['connection_cases']==131072
new_cases=distance['distance_cases']+distance['connection_cases']+search['cases'];assert new_cases==270336
counts={}
archives=[(f'v{v}',R/f'evidence/movement-state-v{v}','source-manifest.json','final-source') for v in [9,10,11,12,13]]
archives+=[('v14-baseline',S/'baseline','source-manifest.json','')]
archives+=[(name,S/'parts'/name,'manifest.json','') for name in ['distance-verified','search-verified']]
for label,base,name,subdir in archives:
    entries=read(base/name)
    for e in entries:assert sha(base/subdir/e['path'])==e['sha256'],(label,e['path'])
    counts[label]=len(entries)
for e in read(R/'evidence/original-inputs-before.json'):
    assert sha(Path('H:/开发/运行版本/原版1.006')/e['name'])==e['sha256'],e['name']
counts['H_originals']=20
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
ordinary.update(main_search_failure='Stop clears the destination; later AI failure callbacks can restore it before failed Prepare returns.',
    conclusion='The default-rule AI TRUCKA fixture exhausts its normal budget naturally with a restored goal in the same Drive.')
ordinary['assumptions'].append('No-consumption inference additionally requires that callbacks do not restore a destination; the default AI scene violates this premise.')
conditions['unresolved']=['Exact 4C3895 callback site is not separately hooked.','Untouched random-match frequency is not measured.',
    'Search setup, itinerary construction, path reconstruction and full-game equivalence remain unfinished.']
write(S/'budget-conditions.json',conditions)
effect=read(S/'effects.json');eb=effect['budget']
eb['legacy_controlled_and_one_cell_scenes']={k:eb.pop(k) for k in ['entry_calls','countdown','natural_test_constraints','natural_test_failure_budget_values','natural_test_failed_rebuild_observed','limitation']}
eb.update(normal_pathfinding_exhaustion_verified=True,natural_exhaustion_verified=True,default_rules_full_exhaustion_verified=True,
    natural_scope=budget['scope'],real_scene_evidence=str(S/'budget-real-scenes.json'),natural_budget_events=conditions['natural_budget_entries'],natural_stop_frame=38)
effect['node_distance']=dict(readable=True,native_probe=distance,integration=read(S/'distance-integration.json'),
    squared_distance_wrap_is_int32=True,original_approximate_distance_service_retained=True,special_connection_metric='Chebyshev')
effect['neighbor_search']=dict(readable=True,native_probe=search,integration=read(S/'search-integration.json'),
    eight_adjacent_and_one_special_neighbor=True,region_exemptions_preserved=True,ordered_callbacks_preserved=True,
    setup_itinerary_and_path_reconstruction_still_generated=True)
write(S/'effects.json',effect)
accept.update(paired_scenes=28,paired_frames=15798,production_default_skirmish='b-search-default',production_default_skirmish_frames=901,
    natural_budget_exhaustion_verified=True,natural_budget_scope=budget['scope'],independent_budget_frames=901,
    neighbor_search_readable=True,node_coordinate_distance_readable=True,whole_search_readable=False,full_original_equivalence_verified=False)
write(S/'strict-acceptance.json',accept)

report=P/'docs/单位移动第十三批-完整邻格搜索与节点距离-20261022.txt'
handoff=P/'交接文档-单位移动第十三批正式验收-20261022.txt'
assert not report.exists() and not handoff.exists()
report.write_text(f'''单位移动第十三批：完整邻格搜索与节点距离（2026-10-22）

一、正式验收
正式代次 13 / 验证轮次 14。
程序：{exe}
SHA-256：{digest}
验收：{S/'validation.json'}
28 场景 / 15798 帧严格一致，另独立默认规则预算自然耗尽场景 901 帧。
对象、RNG、外部命令与内部有序事件均参加比较，比较器未改；位移 +1 和缺帧反例继续被拒绝。
固定 SAVE0029.SAV、seed12345、2190..3000 窗口保持通过，覆盖第2247帧；默认步兵第28帧、三格包围第52帧旧修正保持通过。
墙、闸门、临时/隐形障碍、移动友方几何、转弯接续、二次补建失败及既有状态机效果门槛通过。
46 组原版片段/数值检查全部通过；本轮新增距离与完整邻格循环两组，合计 {new_cases} 例。
菜单、关闭诊断、非法对象命令拒绝等辅助检查通过。全游戏等价仍未完成。

二、节点坐标与距离
可读 C：gameplay/ground_path_distance.h/.c；适配：runtime/ground_path_distance_bridge.h/.c。
Ra2PathPoint 使用 signed16 坐标。ra2_path_squared_distance 在32位无符号域计算差值平方之和，再保留原版 signed32 位模式。
即使坐标极端时平方和回绕，仍将对应有符号结果送给旧距离服务。没有改用 sqrt。
原版 4BA410 近似距离、查表及节点评分尾部仍保留；本轮拆出了坐标算术，没有宣称整个启发式服务都已重写。
ra2_path_connection_distance 使用 max(abs(dx),abs(dy))，是第九项特殊连接的 Chebyshev 距离，不加八方向地形权重。
节点距离入口 1 处、特殊连接距离片段最初 6 处接入；其中完整循环里的 2 处随后被命名循环整体接管，旧内部入口仍保留适配。
映射原版片段：平方距离 {distance['distance_cases']} 例，特殊连接距离 {distance['connection_cases']} 例，覆盖完整 int16 坐标取值范围的固定随机样本。

三、完整邻格搜索
可读 C：gameplay/ground_path_search.h/.c；适配：runtime/ground_path_search_bridge.h/.c。
Ra2PathSearch 显式列出当前节点、暂存候选、目标、展开数、两层缓存、堆、区域路线游标、表面高度和代价参数。
ra2_path_search_neighbors 接管 42764A..427CB5 的完整循环，两份生成展开均接入；其余 3 处旧内部入口复用 ra2_path_region_allows。
每次展开先检查预算和目标，再按原顺序处理八个相邻格与一个特殊连接；随后取下一节点、继承高度、增加展开数。
四种退出结果为达到展开上限、到达目标、遇到不可通行目标和候选耗尽。
区域规则保留已标记区域、上层、格子连接标记与未开启限制时的豁免；地面且无豁免才拒绝未连通区域。
格子先检查代次及旧代价，再调用对象通行查询和地形代价。通行/代价回调可能发布缓存，建节点之前必须重新读取标记。
高度、搜索权重、移动模式、路线游标及代次使用共享视图，避免回调后继续使用旧副本。
路线项仍按 uint16 零扩展，候选区域按 int16 符号扩展，二者比较不能擅自统一符号。
节点创建、堆候选、缓存发布及路线游标更新的顺序保持原版；沿用上一轮 pending 最新候选规则和同分顺序。
原版引擎服务通过命名回调调用，固定地址和旧栈布局集中在 runtime 适配层，业务 C 中没有原版绝对地址访问。

完整原版循环独立检查 {search['cases']} 例，比较 {search['ordered_service_events']} 次有序服务事件、{search['created_nodes']} 个新节点及全部链/堆/缓存输出。
覆盖地面/桥面、空邻居、特殊连接、区域限制及豁免、正负区域编号与路线符号、缓存命中/失效、回调更新权重或缓存、满堆和四种退出条件。
12 种 x87 精度/舍入设置；退出样本数依次 {search['stop_cases']}。
该检查映射原版完整循环，但将区域、通行、地形代价与节点创建四个引擎服务替换为同一组确定性测试服务；它是分支/调用顺序验证，不等于真实对局。
初版工具给原版回调预留的宿主栈过小，造成假差异。扩大到32KiB并加入底部保护后通过；原游戏代码未因此修改，初始差异日志保留。

四、逐块回退与默认预算实景
距离接入后：a-distance-default 901帧、a-distance-ur3 101帧、a-distance-budget 901帧通过，保存 parts/distance-verified。
搜索接入后：b-search-default 901帧、b-search-ur3 101帧、h-default-budget 901帧通过，保存 parts/search-verified。
随后原有27场景14897帧完整回归，与默认遭遇战组成正式28场景15798帧。
预算场景使用原版菜单和地图、默认 RULES、seed12345、CloseEnough=576；仅通过正常服务创建并初次命令一辆真实 AI TRUCKA，摆放16辆敌对 TRUCKA。
没有直接写预算、路径队列和目标，没有强制调用寻路或预算恢复入口。后续由正常游戏更新自行失败与恢复。
第27..37帧预算入口值10..0，第38帧目标与路径段清空；38..240帧保持停止。
失败 Prepare 返回时同一 Drive 的目标仍有效，回退目标始终在默认 CloseEnough 之外。
这是显式构造的真实对象场景；没有证明未干预随机对局中的出现频率。精确4C3895回调点仍是静态链与状态证据，没有单独挂钩逐调用。
摆放工具：{S/'truck-actor-fixture-probe.exe'}
工具 SHA-256：{budget['fixture_executable_sha256']}
仅摆放器对象不同，其余121个生产构建对象一致，详见 truck-actor-fixture-receipt.json。

五、重启恢复、资源副本与保全
客户端崩溃及系统强制重启后，从磁盘检查点接续，未将未通过候选升级为正式版本。中断目录保存在 interrupted-before-reboot-1151。
长期保留的测试副本令资源文件达到NTFS每文件1024硬链接上限；失败发生在启动游戏前，记录保存在 investigations/resource-link-limit。
playtest.py 现为耗尽链接的只读资源建立新的后备副本，逐字节SHA-256核对后原子发布，再供测试副本建立硬链接。
SAV与INI继续使用独立副本；比较器、生产游戏逻辑及规则未改。该基础设施变化原文件保存在 playtest-before-link-pool.py。
122个生产C源、{len(receipt['inputs'])}项构建输入内容核对通过；最终无变化构建刷新0源，EXE哈希不变。
纯C17，新业务与适配层 /W4 /WX；state_trace.c 与前正式基线相同，37处未支持保护保持。
前正式基线、两个本轮回退点、旧失败候选、原始输入及旧手写引擎均保留。未提交、未推送、未建立远程仓库。

六、接续范围
完整邻格展开循环已可读；搜索入口准备、区域路线构造、最终路径重建、近似距离服务、Advance插值与Prepare共享入口仍需继续整理。
优先接着处理搜索入口/路线准备与最终路径重建，再接Advance和Prepare；每块继续走原版片段和默认遭遇战/预算圈逐帧门槛。
完整寻路、完整单位移动和全游戏等价均未完成。MOD修改可从命名搜索状态、区域规则、服务回调及评分入口着手，另建候选并与正式基线分开验收。
''',encoding='utf-8')
handoff.write_text(f'''单位移动第十三批正式验收交接（2026-10-22）

完整九邻格展开/取出循环、区域豁免规则及节点坐标距离算术已整理为命名 C。
正式代次13 / 验证轮次14：{S/'validation.json'}
程序：{exe}
SHA-256：{digest}
28场景/15798帧，另默认规则预算自然耗尽场景901帧严格一致；46组原版片段/数值检查通过。
新增270336例：距离262144例，完整循环8192例（四个引擎服务使用确定性替身，真实场景另外对照）。
第2247帧、默认步兵第28帧及三格包围第52帧旧修正保持通过。
默认预算第27..37帧按10..0自然消耗，第38帧清空目标；构造真实车辆圈、默认规则，未直接写预算/路径/目标。
业务入口：{R/'ra2/src/gameplay/ground_path_search.h'}；ground_path_search.c；ground_path_distance.h/.c。
旧布局适配：runtime/ground_path_search_bridge.h/.c；ground_path_distance_bridge.h/.c。
详细说明：{report}
完整源码/程序：{S/'final-source'}；清单source-manifest.json，差异source-changes.patch，末检final-check.json。
前正式基线：{S/'baseline/ra2/build-original-c/ra2.exe'}，SHA-256 e1d8e97c5706794f8de58d37ad726a1855ccf075947c403c9aeb7204b35dbff5。
本轮回退：{S/'parts/distance-verified'}；{S/'parts/search-verified'}。
重启中断记录和资源硬链接上限失败记录均保留；playtest.py后备副本方案已通过重跑。
下一步：搜索入口准备、区域路线构造与最终路径重建，然后Advance插值、Prepare共享入口；继续逐块原版对照。
近似距离服务仍保留原版；完整寻路、完整单位移动、全游戏等价尚未完成。暂不提交或推送。
''',encoding='utf-8')
guide=R/'ra2/src/gameplay/阅读说明-单位移动.txt';shutil.copy2(guide,S/'reading-guide-before.txt')
guide.write_text(f'''第十三批当前状态（2026-10-22，优先于下文历史阶段描述）

完整九邻格展开、区域豁免与节点坐标距离已整理；28场景/15798帧，另默认预算901帧严格一致，46组检查通过。
入口 ground_path_search.h/.c 和 ground_path_distance.h/.c；完整搜索准备、路线构造、路径重建及原版近似距离服务仍未全部整理。
本轮说明：{report}

'''+guide.read_text(encoding='utf-8')+'''
三十三、邻格搜索与坐标距离的修改入口

ground_path_search.h/.c：Ra2PathSearch、Ra2PathSearchServices、ra2_path_search_neighbors 和 ra2_path_region_allows。
搜索状态把当前节点、目标、缓存、堆、预算、表面高度和区域路线分开命名，业务函数按原顺序处理八邻格及第九特殊连接。
region/passage/traversal_cost/create_node 是服务边界。回调后必须重新读取共享字段和缓存发布标记，不能合并查询或缓存旧值。
区域豁免包括当前代次、上层、格子连接标记和未开启区域限制；路线项 uint16 与区域编号 int16 的符号差异必须保留。
评分、pending暂存、堆同分顺序和先写代次后写代价的发布顺序沿用前批。
ground_path_distance.h/.c：signed16坐标差和平方和保持32位位模式；特殊连接用Chebyshev距离。
4BA410近似距离仍由原版服务提供，不能直接换成sqrt。runtime适配层负责地址、寄存器和局部帧，MOD业务规则优先放在gameplay层。
新的MOD策略另建候选并验收；完整搜索入口/路线准备、路径重建、Advance插值及Prepare共享入口仍待继续。
''',encoding='utf-8')
main=P/'交接文档-原版逆向与C重编译-20261020.txt';assert main.read_bytes()==(S/'baseline/project'/main.name).read_bytes()
main.write_text(main.read_text(encoding='utf-8')+f'\n\n2026-10-22 第十三批正式验收接续入口：{handoff}\n完整九邻格展开/区域豁免和节点距离算术已整理；28场景15798帧，另默认预算901帧严格通过，46组检查通过。\n下一步搜索入口/路线准备、最终路径重建，然后Advance及Prepare。全游戏等价未完成；不提交、不推送。\n',encoding='utf-8')

paths={e['path'] for e in read(S/'baseline/source-manifest.json')}
paths.update(p.relative_to(R).as_posix() for p in (R/'ra2/src').rglob('*') if p.is_file() and p.suffix in ('.c','.h','.txt'))
paths.update(p.relative_to(R).as_posix() for p in R.glob('*v14*') if p.is_file())
paths.add('ra2/tools/playtest.py')
paths.update(p.relative_to(R).as_posix() for p in S.iterdir() if p.is_file() and (p.suffix in ('.c','.h','.asm') or p.name in ['truck-actor-fixture-build-arguments.json','truck-actor-fixture-probe.exe','truck-actor-fixture-receipt.json','playtest-before-link-pool.py']))
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
validation=dict(passed=True,formal_baseline_generation=13,verification_round=14,exe_sha256=digest,state_schema=12,
    paired_scenes=28,paired_frames=15798,independent_default_budget_scenes=1,independent_default_budget_frames=901,
    probes=46,new_fragment_cases=new_cases,source_content_verified=True,diagnostics_removed=True,strict_ordered_audit_passed=True,
    frame_comparison_passed=True,default_rules_full_budget_exhaustion_verified=True,budget_scope=budget['scope'],
    source_files=len(manifest),production_c_sources=122,content_inputs=len(receipt['inputs']),preservation=preservation,unsupported_guards=37,
    node_coordinate_distance_readable=True,complete_neighbor_loop_readable=True,region_exemptions_readable=True,
    original_approximate_distance_service_retained=True,whole_path_search_readable=False,whole_ground_movement_readable=False,
    full_original_equivalence_verified=False,report=str(report),handoff=str(handoff))
write(S/'validation.json',validation)
recovery=read(S/'baseline/project/reports/latest-recovery.json')
recovery.update(validation=str(S/'validation.json'),sha256=digest,executable=str(exe),formal_baseline_generation=13,verification_round=14,
    node_coordinate_distance_readable=True,complete_neighbor_loop_readable=True,region_exemptions_readable=True,
    whole_path_search_readable=False,report=str(report),handoff=str(handoff),budget_exhaustion_evidence=str(S/'budget-real-scenes.json'),
    next_readable_region='Search setup, region itinerary construction and final path reconstruction; Advance interpolation and Prepare shared entries',
    previous_recovery_validation=str(R/'evidence/movement-state-v13/validation.json'),previous_recovery_executable=str(S/'baseline/ra2/build-original-c/ra2.exe'),
    previous_recovery_sha256=sha(S/'baseline/ra2/build-original-c/ra2.exe'))
write(P/'reports/latest-recovery.json',recovery)
write(P/'reports/latest-state-comparison.json',dict(validation=str(S/'validation.json'),exe_sha256=digest,state_schema=12,paired_scenes=28,paired_frames=15798,
    independent_default_budget_frames=901,passed=True,strict_ordered_audit_passed=True,first_difference=None,full_original_equivalence_verified=False,
    normal_budget_exhaustion_verified=True,default_rules_full_budget_exhaustion_verified=True,budget_scope=budget['scope'],report=str(report)))
write(P/'reports/latest-movement-candidate.json',dict(passed=True,status='promoted',formal_baseline_generation=13,verification_round=14,
    executable=str(exe),exe_sha256=digest,validation=str(S/'validation.json'),full_original_equivalence_verified=False,report=str(report)))
for e in manifest:assert sha(R/e['path'])==sha(S/'final-source'/e['path'])==e['sha256'],e['path']
assert sha(exe)==digest and read(P/'reports/latest-recovery.json')['sha256']==digest
write(S/'final-check.json',dict(passed=True,source_files=len(manifest),source_archive_matches_live=True,formal_pointers_match=True,old_baselines_preserved=True,
    exe_sha256=digest,report_sha256=sha(report),handoff_sha256=sha(handoff),reading_guide_sha256=sha(guide),
    main_previous_sha256=sha(S/'baseline/project'/main.name),main_current_sha256=sha(main)))
print(json.dumps(dict(passed=True,formal_baseline=13,exe_sha256=digest,source_files=len(manifest),handoff=str(handoff)),ensure_ascii=False))
