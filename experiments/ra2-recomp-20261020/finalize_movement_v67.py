"""Formal 66 / verification 67; reverse and competing channel recovery."""
from run_batch_v67 import *
if '--freeze-lineage' in sys.argv:
 lineage=read(S/'checker-lineage.json')
 for e in lineage['entries']:
  e['final_derived_sha256']=sha(R/e['derived']);e['unchanged_after_initial_derivation']=e['final_derived_sha256']==e['derived_sha256']
 (S/'checker-lineage.json').write_text(json.dumps(lineage,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print('Current checker lineage frozen before cleanup.');raise SystemExit(0)
for name in ['native-gates.json','effects.json','traffic-effects.json','fairness-effects.json','mixed-recovery-effects.json','queue-recovery-effects.json','bridge-channel-effects.json','channel-comparison.json','traffic-event-linkage.json','channel-host-identity.json','current-explorations.json','preservation.json','cleanup.json','final-scene-matrix.json','rng-functional-impact.json','rng-first-split-window.json','boundary-inheritance.json','service-boundaries.json','infrastructure-status.json','baseline-native-identity.json','community-reference-review.json','community-current-use.json','heap-improvement-inheritance.json','prior-traffic-inheritance.json','prior-explorations.json','traffic-map-provenance.json','traffic-goal-terrain-validation.json','channel-observer-baseline-parity.json','progress-inventory.json','traffic-checker-review.json','traffic-boundary-contract.json']:assert read(S/name)['passed'],name
receipt=read(R/'ra2/build-original-c/source-content-receipt.json');digest=sha(R/'ra2/build-original-c/ra2.exe');matrix=read(S/'final-scene-matrix.json');native=read(S/'native-gates.json');clean=read(S/'cleanup.json');inventory=read(S/'progress-inventory.json')
parts=[read(S/'parts'/n/'validation.json') for n in ['reaction','recovery']];before=read(S/'traffic-baseline-scenes.json');assert parts[-1]['exe_sha256']==digest
pairs=sum(x['scene_count'] for x in parts)+len(matrix['results'])+len(before['results']);frames=sum(x['frames'] for x in parts)+sum(x['frames'] for x in matrix['results']+before['results']);strict=sum(x['scene_count'] for x in parts)+sum(x['strict_trace_equal'] for x in matrix['results']+before['results']);functional=pairs-strict
assert (pairs,frames,strict,functional)==(23,62273,19,4) and native['groups']==5 and native['cases']==393216
assert sorted(read(S/n)['unique_cases'] for n in native['receipts'])==[65536,65536,65536,65536,131072]
parent=read(S/'vcs-context.json')['parent_commit'];report=P/'docs/单位移动第六十六批-反向竞争通道与障碍恢复-20261025.txt';handoff=P/'交接文档-单位移动第六十六批正式验收-20261025.txt';progress_doc=P/'docs/当前进度与剩余内容-20261025-第六十六批.txt';policy=P/'docs/项目目标与验收边界-20261024.txt';addendum=P/'docs/寻路机制改进验收补充-20261025.txt'
measurements=[]
for item in read(S/'traffic-fixtures.json')['fixtures']:
 effect=read(S/'fairness-effects.json')['scenes'][item['observer_tag']]['original']['effects'];directions={key:{k:v for k,v in row.items() if k!='throughput_500_frame_windows'} for key,row in effect['by_direction'].items()}
 measurements.append(dict(tag=item['tag'],kind=item['kind'],frames=item['last']+1,requests=len(item['actor_ids']),blockers=len(item['blocker_ids']),actual_tube_actors=effect['actual_tube_actors'],non_tube_requests=effect['non_tube_requests'],exact_goal_count=effect['exact_goal_count'],near_goal_count=effect['near_goal_count'],stationary_request_count=effect['stationary_request_count'],last_exact_goal_arrival=effect['last_exact_goal_arrival'],by_direction=directions,opposing_inflight_frames=effect.get('opposing_inflight_frames')))
summary=json.dumps(measurements,ensure_ascii=False,indent=2)
report.write_text(f"""单位移动第六十六批（正式66 / 验证67），2026-10-25。
父提交：{parent}。
程序：{R/'ra2/build-original-c/ra2.exe'}
SHA-256：{digest}
验收边界：{policy}；机制补充：{addendum}。

本批实现
按整体功能、效果、规则和资源调用验收，不追求逐个BUG复刻；允许有证据支持的机制改进。只改ground_reaction.c与ground_recovery.c两处生产C，头文件、构建清单、runtime/生成入口与分发表、生产schema12记录器、通用比较器、规则和资源不改，181C/312输入/37保护保持。
reaction阶段：select_obstacle_response保留DISPATCH与保存passage的区别，友方障碍只把本次path_head/flags置-1/0；攻击递归直接返回其结果，false也不落入收尾。attack_obstacle_target保留第一次存在检查、第二次实时目标查询、敌我判断及攻击/墙体查询的原顺序；每次按当时services->context调用。finish_obstacle_response保留blocked的-1/0重试或本段失效/取消/停止，其余清pending/selector并返回1。
recovery阶段：finish_exhausted_budget串联预算耗尽后的本段失效、目标取消/停止、owner存活、声音与pending清理；正预算只减一次。finish_recovery_state先保留关联对象实时查询/通知，再清本段、selector和legacy61。finish_only继续跳过预算，返回约定与回调可改写状态保持。本批无新增全局FIFO、优先级、退避常数或路径算法。
原版reaction v42原字节四入口各65536，recovery v63预算/共享收尾各65536，共两份探针、五份收据、六段393216唯一例；改前和两段后通过，重复不累计。reaction检查所声明状态、回调、ABI与控制字；recovery按自身字段检查状态/回调/ABI，不虚称控制字或全ABI证明。

自然交通与恢复
两张新图只改父批地图Units/Infantry，地形、桥层、覆盖、双向Tubes原字节保持。创建地图前已用原版native catalog逐个检查起点、路点、终点的land/level；两次0:1校准只绑定实际actor ID，不计移动帧。
反向队列：12辆由东向西请求，3辆普通Sleep占道车。最高actor ID最先第5帧请求，后续100..2100帧每200帧来车；西侧占道车1600/1700/1800帧普通Move释放。逐车区分实际反向Tube与合法地面绕行，核对长等待、超越、出口发布和到达，不重发请求强迫恢复。
竞争通道：8辆北侧车辆按预定桥面/接近路点再向东请求，8辆东侧车辆向西请求；每向300帧间隔，两个流错开100帧。记录两向Tube内部进展的同帧重叠，实测帧数见汇总；每个实际向东Tube参与者有更早的同车桥层见证。普通移动命令之外无路径、预算或运动状态注入。
每张5401帧，正式程序/独立观测在改前与最终各执行一组；共8配对43208帧严格，全部当前每模式完整轨迹等于改前冻结数据。观测剔除fixture行后的全部生产记录逐模式一致。每车生命、最终格与请求目标距离、Guard、请求后实际运动、普通命令执行、实际路由、等待/分方向吞吐分别记录。反向队列有未精确到达/未启动请求，竞争流有近目标停稳，原版与改前C严格相同；这8配对只计原版行为边界，不计全车恢复成功。初始专用检查器的精确目标假设未成立后，保留初稿，改用明确边界分类，复用原始轨迹，不改游戏/规则/地图/全局比较器，见traffic-checker-review.json。
实测汇总：
{summary}
完整逐车及500帧吞吐窗口：{S/'fairness-effects.json'}。
以上为有限到达窗口/固定地图证据，不证明无限负载无饥饿、FIFO、有界全图等待或通道饱和容量；地面绕行不计入Tube吞吐。

回归、保护与收尾
两段各默认301、北桥501、南桥501，共6配对2606帧严格；每次构建和阶段回退均串行，下一阶段先验证前段程序与312项编译输入绑定。最终mi/sc/aw3/fm逐模式完整轨迹等于父批；4项既有349/350随机分歧、2020/2018与2219/2220时序差异保留。列车碰撞、碾压、重复失败及Z436/Z-193原版高差异常通过。
验收对照{pairs}配对{frames}帧（15正常回归配对、8原版行为边界配对），{strict}严格、{functional}既有局部功能差异；393216原版片段例另计。不宣称全游戏/完整视觉等价。父批无效目标、62,54起点未启动及构建重叠无效快照按prior-explorations.json继承，均不计当前成功覆盖；不要求逐BUG复刻。
5项社区固定版本/内容哈希继承；前批两份公开源码核对按哈希保留，不虚称本批重新下载。仅参考结构与定位，不套不同版本地址/规则、不导入第三方引擎、不上传私有工程。堆容量改进的7412预期差异/65541合成见证继承，不计新例，不保证最短路径。29非主入口/86原始入边证据继承，无新自然别名入口结论。
父代475项封存、315项独立基线、两段有效回退、改前探针/宿主、全部轨迹及原版异常保留。H盘20项输入、原game.exe/SAVE0029、原rules、旧手写引擎、Git配置/远端引用不变。
清理{clean['deleted_files']}项可重建对象/缓存及重复导出，{clean['deleted_bytes']}字节，{clean['protected_files']}项保护文件保持。本地提交，不推送。
复核：{R/'verify_final_movement_v67.py'}；提交收据：{S/'postcommit/git-local-commit.json'}。
整体现状与剩余：{progress_doc}。
""",encoding='utf-8',newline='\n')
groups=inventory['compiled_c_groups']
progress_doc.write_text(f"""当前进度与剩余内容（第六十六批，2026-10-25）

主线与口径
当前主线是原版RA2 1.006的C17/x86静态重编译与逐步可读化，不是把旧手写x64引擎的里程碑相加。旧项目、原始资源与旧程序继续保留。批次66不表示整机完成66%；没有足够完整的功能总清单与全覆盖证据，当前不给虚构百分比。

已经做到
1. 已有可构建、可运行并与锁定原版对照的C17/x86程序，复用原规则/美术与存档。固定seed12345、模拟帧发令、原版/C状态对照、只读观测、原版片段探针、分段回退、内容哈希和本地提交形成可持续验收链。
2. 可读移动服务已覆盖当前验证范围内的地面通行/对象分类、分层区域与局部路径搜索、堆/节点、平滑后处理、完成重建与队列消费、耗尽重试、等待/障碍释放、桥面层与Tube进入/出口/连接恢复，以及本批障碍响应和预算耗尽收尾。自然场景包含单向/反向/双向、桥隧、长等待与持续请求、碰撞/碾压等，但仍是有界证据。
3. 当前实际编译181个C、131个头文件，共312输入。其中gameplay {groups['ra2/src/gameplay']}个C、runtime {groups['ra2/src/runtime']}个C、生成重编译 {groups['ra2/src/recomp']}个C，其余为兼容/底层运行库。gameplay文件数不等于已完整验收的独立功能数。
4. 原lifting统计记录{inventory['historical_lift_stats']['lifted']}个入口；当前生成C定义计数{inventory['generated_function_definitions']}。这些多数仍是机械生成代码，不表示所有玩法已可读重建或全面验收。当前保留{inventory['unimplemented_guard_sites']}处未实现保护调用点（{inventory['unique_guard_targets']}个不同目标）；调用点数也不等于缺失功能数。
5. 本批23配对62273帧（19严格、4既有功能差异）、393216原版片段例通过。新增反向/竞争流8配对43208帧原版行为边界严格对照，未计全车到达成功；仅是本批增量，历史有效证据按哈希继承，未把重复运行累计成新覆盖。当前程序SHA-256：{digest}。

剩余主要内容
1. 移动域：更多地图、载具/移动类型、尺寸和桥层组合，更长的竞争负载与边界；按功能风险补充29个非主入口的剩余证据，不为穷尽别名而阻止本批交付。持续无限新请求下的公平性/饥饿、全局最短和自然容量饱和尚无证明，不能从有限场景外推。必要的优先级/退避/寻路改进需另有测量与回归。
2. 全局保护点：37处调用点分布于多个生成函数，包含地形析构、下拉列表构造等命名入口及无名入口，需按可达性/影响归类；它们不是37项完整缺失玩法，也不全属于移动。明细见progress-inventory.json。
3. 其他玩法域：战斗/武器弹道、伤害与死亡、生产建造、经济采矿、科技规则、AI/任务、战役触发与任务目标等仍需在本主线逐步可读化并进行系统级验收。它们在原版提升代码中存在，不能直接说未实现，也不能把存在生成C当成已完成验收。
4. 整机链路：普通用户启动/交互、菜单与游戏生命周期、保存/载入、完整战役和遭遇战的长期运行、视觉/音频与规则/美术资源调用一致性，尚未形成完整发布验收。旧手写引擎的相关成果不自动填补本主线证据。
5. 本批新增边界：反向12请求仅8辆精确到达，4辆请求后未运动；双向16请求13辆精确到达，3辆在目标附近停稳。这些与原版逐帧相同，不是本批C回归，也不作为全车恢复成功。下一步应先定位可达性/占位/原版停止规则，再决定是否改进恢复调度，当前未证明根因。
6. 其他已知边界：349/350随机首差及部分到达时序仅按功能效果接受，随机调用的全部因果链未证明；Z436/Z-193等原版异常、62,54原版/改前C未启动起点、历史失败输入都保留，不自动变成必须复刻或逐个修复的清单。

后续顺序
先按功能风险收口移动剩余清单，减少只有重复场景/重命名而无新增行为证据的轮次；再推进战斗/对象生命周期等相邻玩法的可读服务与原版对照。每批只扩展受影响行为，使用整体功能/效果边界，不以逐位或逐BUG穷举阻止交付。
本批详细报告：{report}
交接：{handoff}
可核对清单：{S/'progress-inventory.json'}
""",encoding='utf-8',newline='\n')
handoff.write_text(f"""当前正式66 / 验证67，2026-10-25。
父提交：{parent}；程序SHA-256：{digest}。
报告：{report}
当前进度与剩余：{progress_doc}
政策：{policy}；机制补充：{addendum}。

仅改ground_reaction/ground_recovery两处生产C，整理分派/对象攻击/重试出口、预算耗尽和共享恢复收尾；回调顺序、动态context/对象读取、返回/停止约定保持，无新FIFO/退避/路径算法。181C/312输入/37保护。
原版四reaction入口与两recovery段，共五收据393216唯一例；改前和两段后通过，重复不累计，ABI/控制字范围按各探针字段。
两张普通地图：反向12请求+3占道；桥隧双向8+8请求。所有起点/路点/目标先经原版地形检查；每图5401帧，正式/观测改前/最终共8配对43208帧严格。完整轨迹等于冻结基线；观察与正式生产记录逐模式一致；新增8配对为边界对照，不是全请求恢复成功。
{summary}
总23配对62273帧，19严格、4既有局部功能差异。无限负载无饥饿/FIFO/全图最短未证明。旧RNG、时序、高差和起点异常、失败输入及无效快照原地继承，不计当前新覆盖，不要求逐BUG复刻。
基线：{S/'baseline'}；有效回退：{S/'parts/reaction'}、{S/'parts/recovery'}；探针：{S/'baseline-probe'}；宿主：{S/'baseline-channel-observer'}；封存：{S/'final-source'}。
清理{clean['deleted_files']}项无用产物，本地提交，不推送。复核：{R/'verify_final_movement_v67.py'}。
下一批父证据显式指定movement-state-v67；优先按进度清单收口移动功能边界，再进入战斗/对象生命周期等相邻玩法，避免仅无限扩大相同交通配方。
""",encoding='utf-8',newline='\n')
lead=f'最新接续：第六十六批正式65 / 验证66已验收。\n交接：{handoff}\n政策：{policy}\n机制改进补充：{addendum}\nEXE：{digest}\n以下历史原地保留。\n\n'.encode('utf-8')
for name in ['交接文档-原版逆向与C重编译-20261020.txt','交接文档-新对话继续推进-20261022.txt']:
 p=P/name;p.write_bytes(lead+p.read_bytes())
p=P/'README.md';ls=p.read_bytes().splitlines(keepends=True);eol=b'\r\n' if ls[0].endswith(b'\r\n') else b'\n'
p.write_bytes('> 当前研究路线（2026-10-25）：原版1.006 C17/x86单位移动第六十六批已验收。反向/竞争桥隧交通与障碍恢复服务；[交接](交接文档-单位移动第六十六批正式验收-20261025.txt)、[当前进度和剩余内容](docs/当前进度与剩余内容-20261025-第六十六批.txt)。遵守整体功能与效果验收边界；以下旧手写引擎阶段不计入本主线完成度。'.encode('utf-8')+eol+b''.join(ls[1:]))
p=R/'ra2/src/gameplay/阅读说明-单位移动.txt';p.write_bytes(f'第六十六批（2026-10-25）\n障碍响应分派/攻击/重试出口、失败预算耗尽与共享恢复收尾；反向队列与双向桥隧竞争。181C/312输入/37保护，23配对62273帧，原版片段393216例。\n报告：{report}\n进度：{progress_doc}\n\n'.encode('utf-8')+p.read_bytes())
pointer=dict(passed=True,status='promoted',formal_baseline_generation=66,verification_round=67,validation=str(S/'validation.json'),exe_sha256=digest,sha256=digest,executable=str(R/'ra2/build-original-c/ra2.exe'),full_original_equivalence_verified=False,report=str(report),handoff=str(handoff),acceptance_policy=str(policy),pathfinding_policy_addendum=str(addendum),path_mechanism_identity_required=False,globally_shortest_paths_verified=False)
for name in ['latest-recovery.json','latest-state-comparison.json','latest-movement-candidate.json']:
 p=P/'reports'/name;x=read(p);x.update(pointer);x['current_batch']=dict(formal_generation=66,verification_round=67,accepted_game_pairs=pairs,accepted_frames=frames,native_cases=393216,native_groups=5,synthetic_cases=0,inherited_heap_improvement=True,new_traffic_recipes=2,positive_game_pairs=15,traffic_boundary_pairs=8,all_traffic_requests_exactly_arrived=False,production_c_sources=181,content_inputs=312,strict_all_frames_equal=False,accepted_baseline_variations=4,strict_game_pairs=strict,functional_game_pairs=functional,fifo_guarantee=False,unbounded_starvation_freedom_proved=False)
 p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
write(S/'remaining-work.json',dict(passed=True,bug_for_bug_required=False,path_mechanism_identity_required=False,globally_shortest_paths_verified=False,natural_alias_dispatch_required=False,community_references_available=True,remaining=['Broader maps, locomotors and longer competing traffic; measured queue priority/backoff if needed','Classify 37 remaining guard sites and validate affected reachable behavior','Other gameplay systems still largely generated C: combat/production/economy/AI/campaign logic','Full user lifecycle, save/load, visual/audio/resource and long campaign/skirmish acceptance','Retained original stationary start and RNG variations remain bounded references, not mandatory bug replication'],progress_report=str(progress_doc)))
for e in read(S/'checker-lineage.json')['entries']:assert e['final_derived_sha256']==sha(R/e['derived'])
paths={Path(p).relative_to(R).as_posix() for p in receipt['inputs']}
paths.update(['ra2/CMakeLists.txt','ra2/run_lift.py','ra2/tools/playtest.py','ra2/build-original-c/ra2.exe','ra2/build-original-c/source-content-receipt.json','ra2/src/gameplay/阅读说明-单位移动.txt','build-faithful.ps1','run_fixture_comparison.py','run_state_comparison.py','evidence/movement-state-v4/SOV01T-original.MAP','ra2/work/game/lift_stats.json'])
paths.update(p.relative_to(R).as_posix() for p in R.glob('*v67*') if p.is_file())
paths.update(p.relative_to(R).as_posix() for p in S.iterdir() if p.is_file() and p.suffix in ['.c','.h','.asm','.exe','.json'] and p.name not in ['source-manifest.json','document-manifest.json','validation.json','final-check.json'])
paths.update(p.relative_to(R).as_posix() for p in (S/'fixtures').iterdir() if p.is_file());manifest=[]
for rel in sorted(paths):
 d=S/'final-source'/rel;d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/rel,d);manifest.append(dict(path=rel,sha256=sha(d)))
write(S/'source-manifest.json',manifest)
docs=[P/'README.md',report,handoff,progress_doc,policy,addendum]+[P/n for n in ['交接文档-原版逆向与C重编译-20261020.txt','交接文档-新对话继续推进-20261022.txt']]+[P/'reports'/n for n in ['latest-recovery.json','latest-state-comparison.json','latest-movement-candidate.json']];documents=[]
for p in docs:
 d=S/'current-project'/p.relative_to(P);d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,d);documents.append(dict(path=p.relative_to(P).as_posix(),sha256=sha(d)))
write(S/'document-manifest.json',documents)
write(S/'validation.json',dict(**pointer,parent_commit=parent,state_schema=12,accepted_game_pairs=pairs,accepted_frames=frames,production_c_sources=181,content_inputs=312,unsupported_guards=37,native_cases=393216,probes=2,synthetic_cases=0,inherited_heap_improvement=True,new_traffic_recipes=2,new_traffic_pairs=8,new_traffic_frames=43208,capture_packet_cases_inherited=64,transport_packet_cases_inherited=128,accepted_inherited_variations=4,strict_game_pairs=strict,functional_game_pairs=functional,strict_all_frames_equal=False,source_files=len(manifest),finite_original_behavior_conformance=True,all_traffic_requests_exactly_arrived=False,positive_game_pairs=15,traffic_boundary_pairs=8,bug_for_bug_required=False,cleanup_performed_this_round=True,rollback_parts=['reaction','recovery'],excluded_rollback_dirs=[],fifo_guarantee=False,unbounded_starvation_freedom_proved=False,pushed=False))
write(S/'final-check.json',dict(passed=True,exe_sha256=digest,source_manifest_sha256=sha(S/'source-manifest.json'),document_manifest_sha256=sha(S/'document-manifest.json'),pushed=False))
print(dict(passed=True,generation=66,exe_sha256=digest,source_files=len(manifest),pairs=pairs,frames=frames,native_cases=393216,new_traffic_recipes=2))
