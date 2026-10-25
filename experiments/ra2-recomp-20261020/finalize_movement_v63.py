"""Promote finite wait/release recovery services and observed ramp/crossroad traffic."""
from run_batch_v63 import *
if '--freeze-lineage' in sys.argv:
 lineage=read(S/'checker-lineage.json')
 for e in lineage['entries']:
  e['final_derived_sha256']=sha(R/e['derived']);e['unchanged_after_initial_derivation']=e['final_derived_sha256']==e['derived_sha256']
 (S/'checker-lineage.json').write_text(json.dumps(lineage,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print('Current checker lineage frozen before cleanup.');raise SystemExit(0)
for name in ['native-gates.json','effects.json','traffic-effects.json','traffic-reissue-motion.json','channel-comparison.json','channel-land-proof.json','wait-release-height-effects.json','bridge-surface-profile.json','preservation.json','cleanup.json','final-scene-matrix.json','rng-functional-impact.json','rng-first-split-window.json','boundary-inheritance.json','service-boundaries.json','infrastructure-status.json','baseline-native-identity.json','community-reference-review.json','heap-improvement-inheritance.json','prior-traffic-inheritance.json']:
 assert read(S/name)['passed'],name
receipt=read(R/'ra2/build-original-c/source-content-receipt.json');digest=sha(R/'ra2/build-original-c/ra2.exe')
matrix=read(S/'final-scene-matrix.json');native=read(S/'native-gates.json');clean=read(S/'cleanup.json');traffic=read(S/'traffic-effects.json')
parts=[read(S/'parts'/n/'validation.json') for n in ['wait','release']];before=read(S/'traffic-baseline-scenes.json');assert parts[-1]['exe_sha256']==digest
pairs=sum(x['scene_count'] for x in parts)+len(matrix['results'])+len(before['results'])
frames=sum(x['frames'] for x in parts)+sum(x['frames'] for x in matrix['results']+before['results'])
strict=sum(x['scene_count'] for x in parts)+sum(x['strict_trace_equal'] for x in matrix['results']+before['results']);functional=pairs-strict
assert (pairs,frames,strict,functional)==(19,31069,15,4)
assert native['groups']==5 and native['cases']==458752
assert sorted(read(S/n)['cases'] for n in native['receipts'])==[65536,65536,65536,131072,131072]
assert sha(S/'community-reference-review.json')==sha(O/'community-reference-review.json')
parent=read(S/'vcs-context.json')['parent_commit'];report=P/'docs/单位移动第六十二批-等待障碍恢复与层高通道交通-20261025.txt';handoff=P/'交接文档-单位移动第六十二批正式验收-20261025.txt'
policy=P/'docs/项目目标与验收边界-20261024.txt';addendum=P/'docs/寻路机制改进验收补充-20261025.txt'
lines=[]
for tag,x in traffic['scenes'].items():
 assert x['per_mode_traces_equal_prechange'] and x['strict_trace_equal']
 m=x['modes']['original'];r=read(S/'wait-release-height-effects.json')['scenes'][tag]['original']
 windows='/'.join(str(w['simultaneous_three_or_more_frames']) for w in m['activity_windows'])
 lines.append(f"{tag}：实测层高{m['observed_base_levels']}，Z范围{m['observed_height_range']}；四窗至少三单位同时移动帧数{windows}；等待{r['wait_frames']}帧；障碍首次移动{r['blocker_first_motion']}，主车跨越{r['car_cross_frame']}、到达{r['car_arrival_frame']}；近邻不同高度同时移动{r['nearby_different_height_moving_frames']}帧；空队列到达再发见证{len(m['empty_arrival_reissues'])}个。")
report.write_text(f'''单位移动第六十二批（正式62 / 验证63），2026-10-25。
父提交：{parent}。
程序：{R/'ra2/build-original-c/ra2.exe'}
SHA-256：{digest}
验收边界：{policy}
机制补充：{addendum}

范围与实现
按整体功能、效果、规则与资源调用验收，不追求逐个BUG复刻；允许有证据支持的机制改进。本批只改ground_wait.c和ground_obstacle.c，整理通行/等待与障碍释放后的恢复衔接。181C、312编译输入、37处未实现保护不变；头文件、构建清单、生成入口/分发表、runtime桥接、schema12记录器、通用比较器、规则和资源未改。
第一段wait：resolve_clear_terrain在通行成功后处理可碾覆盖及目标地形；保留先查overlay，再按passage分流，层高差>=2时沿用参考层/道路回退，普通分支重新查询level和land。clear_only仍绕过这些查询，Gate仍先请求开启再废弃路段。所有查询保留当时services->context。
start_traffic_wait_once只在未等待时写waiting与阻塞计时并通知start_wait，回调后的状态不覆盖。主入口先重试计时门禁，再按waiting及阻塞时限选mode1/2；保留32位回绕判断。rebuild_after_traffic_wait在重建之后构造统一出口服务，再复核owner、目标接纳、停止与重试；不提前缓存回调之前的对象、帧或目标。
第二段release：observe_neighbor_passage在地图边界检查后重读队首/朝向；整个障碍观察保留入口捕获的context。友军/列车过滤仍先于距离和严格层高容差判断。finish_near_allied_blocker先废弃段再查目标、取消/停止；只有未结束目标才通知桥层。publish_recovered_queue在障碍检查后重置失败预算10，再读取可能由回调改写的队首，返回原队列消费阶段。越界、方向8、Gate、失败重建和成功重建的出口保留。
ground_recovery现有失败预算、目标停止、存活、声音、关联对象通知与清段/selector收尾保持原字节，本轮重跑其原版对照，以核对恢复链出口；未虚称为新增生产改动。没有新增算法或容量变化，前批有证据的堆容量改进保留，不保证全图最短。

原版1.006片段验证
采用已核对原字节探针：wait v44的clearance、clear-only/invalidate、traffic-wait三组各65536；obstacle v53失败/成功重建各65536；recovery v53失败预算/共享收尾各65536。五个门禁组共458752例，改前、wait后、release后均执行，相同输入重复不累计。
各探针声明的状态、回调顺序、返回、寄存器/标志、栈局部量及控制字检查通过；recovery未声明控制字覆盖，不泛称全部ABI。源码、程序、header独立保留baseline-probe；构建仅补足现有gameplay依赖闭包，未改探针输入/桩或生产构建。其他移动入口不计本轮新增覆盖。

自然交通与实际层高交互
两个新配方使用既有北向交通地图原字节，3TRUCKA与1E2、普通Move事件。前段保留210/300帧分批释放障碍，主车只有5帧的一次发令，观察等待、邻道释放后绕行、跨越、主障碍释放及到达。后续三轮分别通过地图已有4/5层坡道、道路交叉口，在行进中改发，最终同格再发。每条3001帧；全部活动单位均有真实上坡和下坡，记录近邻不同高度同时移动；没有修改地形、规则或注入路径/移动状态。
{chr(10).join(lines)}
坡道实测Z416..520并包含中间高度，非仅两个固定高度的独立场景。Road=1和合法陆地据保留的原版地形表/[Road]规则校验；channel-land-proof.json是父批原字节继承，内含父批检查器纠正经过，该Road纠正没有在本批重做。本批检查器初次漏列桥面下的Rock=3基础地形，已按Cell bridge=1、基础层0和实测Z416进行专用分类，原版/C原始比较严格、原轨迹复用，未改地图/生产/规则；见bridge-surface-profile.json。此次不是新记录单位Bridge flag上下桥面切换的证明。
完整生命、合法地形/高度范围、每车路径缓冲、现有stage6结果、普通发令提交/执行、四个活动窗和最终目标/Guard均通过。改发按前两帧位置核对移动且旧目标未完成；空队列再发独立分类。等待/释放的自然观测不能证明每一次内部timer mode或死锁原因，映射片段门禁另列。
改代码前与最终程序各2配对，共4配对12004帧严格；各模式完整轨迹等于改前冻结基线。所有原版/C原始比较和负控制保留；前批平地/高架交通按哈希继承，不重计为当前执行。

回归与边界
两段各默认301、北桥501、南桥501帧，共6配对2606帧严格。最终mi/sc/aw3/fm装卸与岸边场景完整每模式轨迹等于父批；4项既有严格false、349/350随机首差窗口、原版/C货车2020/2018与步兵2219/2220时序保留。列车碰撞、碾压、重复失败和弯曲高差回归通过；Z436停滞与Z-193未完成等原版异常、失败地图、负控制保留，不要求逐BUG复刻。
29非主C入口/86原始入边及旧岸边、坡型/飞机等边界按哈希继承，未宣称重跑或新增自然别名入口。全部{pairs}配对{frames}模拟帧，{strict}严格、{functional}既有局部功能差异通过。seed12345、模拟帧发令；最多两条配对通道/四个游戏进程，构建串行。
社区5项固定提交/内容哈希线索原字节继承：gagarin YR1.001结构/调用、EA旧Red Alert检查/发布组织、Phobos扩展定位，仅用于定位与服务组织；不套版本地址/规则，不引入第三方引擎代码、不上传私有工程。原版1.006仍为依据：{S/'community-reference-review.json'}。
父批{len(read(O/'source-manifest.json'))}项封存、315项独立基线、两段回退、改前探针/宿主及两条自然交通基线保留。H盘20项原始输入、game.exe/SAVE0029、原rules、旧手写引擎、Git配置/远端引用不变。
按路径、类型、哈希及重解析点检查清理{clean['deleted_files']}项对象文件、缓存和重复导出，共{clean['deleted_bytes']}字节；保护清单{clean['protected_files']}项不变。其中重复lineage导出在确认独立保留副本后删除，见redundant-export-cleanup.json。源码、正式程序、资源、轨迹、基线、回退、异常保留。本地提交，不推送。
复核：{R/'verify_final_movement_v63.py'}；本地提交收据：{S/'postcommit/git-local-commit.json'}。
后续按功能需要扩展多层桥面/隧道交通、长时间拥堵恢复或有度量的搜索改进；当前不是全游戏、完整资源视觉或最优路径验收。
''',encoding='utf-8',newline='\n')
handoff.write_text(f'''当前正式62 / 验证63，2026-10-25。
父提交：{parent}；程序SHA-256：{digest}。
报告：{report}
政策：{policy}
机制补充：{addendum}

ground_wait完成通行地形、首次等待、计时重建与统一出口服务；ground_obstacle完成边界后实时方向、近目标停止与恢复队列发布服务。保留回调顺序、实时/捕获context边界、回绕计时及层高回退。只改2C，181C/312输入/37保护不变，runtime/生成入口/记录器/比较器/规则资源未改。
原版wait三相196608、obstacle两入口131072、未改动recovery两出口131072，共458752例，改前及两段后通过。五组，重复不累计，ABI/控制字范围以各探针字段为准。
两个3001帧普通交通配方先分批释放障碍，再通过既有4/5层坡道和交叉路口，实测Z416..520包含中间高度，全部活动单位有上下坡、近邻不同高度并行。四窗活动、行进改发、空队列再发、生命、路径、目标与Guard通过。不是新的Bridge flag切换证明，也不泛称内部每个等待分支自然覆盖。
总19配对31069帧，15严格、4既有局部功能差异；新交通改前/后4配对12004帧严格且完整每模式轨迹相等。既有349/350窗口、2020/2018和2219/2220时序、Z436/Z-193异常、旧失败地图与边界保留。堆改进和5项固定社区线索按哈希继承，不重计新门禁。
基线：{S/'baseline'}；回退：{S/'parts'}；探针：{S/'baseline-probe'}；宿主：{S/'baseline-observer'}；自然改前：{S/'runs/b-traffic-height-ramp'}、{S/'runs/b-traffic-height-crossroad'}；封存：{S/'final-source'}。
清理{clean['deleted_files']}项对象文件、缓存和独立留存后的重复导出；保护原始输入、正式程序与历史证据。本地提交，不推送。
后续按功能推进多层桥面/隧道交通、长时间拥堵恢复或有证据的寻路改进；全游戏/完整资源视觉/全图最优路径未验收。
派生下一批显式指定父证据movement-state-v63并核对导入。复核：{R/'verify_final_movement_v63.py'}。
''',encoding='utf-8',newline='\n')
lead=f'最新接续：第六十二批正式62 / 验证63已验收。\n交接：{handoff}\n政策：{policy}\n机制改进补充：{addendum}\nEXE：{digest}\n以下历史原地保留。\n\n'.encode('utf-8')
for name in ['交接文档-原版逆向与C重编译-20261020.txt','交接文档-新对话继续推进-20261022.txt']:
 p=P/name;p.write_bytes(lead+p.read_bytes())
p=P/'README.md';ls=p.read_bytes().splitlines(keepends=True);eol=b'\r\n' if ls[0].endswith(b'\r\n') else b'\n'
p.write_bytes('> 当前研究路线（2026-10-25）：原版1.006 C17/x86单位移动第六十二批已验收。等待/障碍释放恢复及坡道、交叉道路交通；[第六十二批交接](交接文档-单位移动第六十二批正式验收-20261025.txt)。遵守[整体功能与效果边界](docs/项目目标与验收边界-20261024.txt)和[机制改进补充](docs/寻路机制改进验收补充-20261025.txt)。'.encode('utf-8')+eol+b''.join(ls[1:]))
p=R/'ra2/src/gameplay/阅读说明-单位移动.txt';p.write_bytes(f'第六十二批（2026-10-25）\n等待/障碍释放恢复；两个3001帧坡道/交叉道路交通，真实4/5层与Z416..520。181C/312输入/37保护，19配对31069帧，原版片段458752例。\n前批有证据的堆容量改进、原版差异/异常、基线和分段回退保留。\n报告：{report}\n\n'.encode('utf-8')+p.read_bytes())
pointer=dict(passed=True,status='promoted',formal_baseline_generation=62,verification_round=63,validation=str(S/'validation.json'),exe_sha256=digest,sha256=digest,executable=str(R/'ra2/build-original-c/ra2.exe'),full_original_equivalence_verified=False,report=str(report),handoff=str(handoff),acceptance_policy=str(policy),pathfinding_policy_addendum=str(addendum),path_mechanism_identity_required=False,globally_shortest_paths_verified=False)
for name in ['latest-recovery.json','latest-state-comparison.json','latest-movement-candidate.json']:
 p=P/'reports'/name;x=read(p);x.update(pointer)
 x['current_batch']=dict(formal_generation=62,verification_round=63,accepted_game_pairs=pairs,accepted_frames=frames,native_cases=458752,native_groups=5,synthetic_cases=0,inherited_heap_improvement=True,new_traffic_recipes=2,production_c_sources=181,content_inputs=312,strict_all_frames_equal=False,accepted_baseline_variations=4,strict_game_pairs=strict,functional_game_pairs=functional)
 p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
write(S/'remaining-work.json',dict(passed=True,bug_for_bug_required=False,path_mechanism_identity_required=False,globally_shortest_paths_verified=False,natural_alias_dispatch_required=False,candidates_not_confirmed_failures=True,community_references_available=True,remaining=['Further bridge-layer/tunnel ordinary traffic as functionally needed','Long congestion recovery and measured evidence-supported search improvements','Other engine subsystems and full visual/resource acceptance']))
for e in read(S/'checker-lineage.json')['entries']:assert e['final_derived_sha256']==sha(R/e['derived'])
paths={Path(p).relative_to(R).as_posix() for p in receipt['inputs']}
paths.update(['ra2/CMakeLists.txt','ra2/run_lift.py','ra2/tools/playtest.py','ra2/build-original-c/ra2.exe','ra2/build-original-c/source-content-receipt.json','ra2/src/gameplay/阅读说明-单位移动.txt','build-faithful.ps1','run_fixture_comparison.py','run_state_comparison.py','evidence/movement-state-v4/SOV01T-original.MAP'])
paths.update(p.relative_to(R).as_posix() for p in R.glob('*v63*') if p.is_file())
paths.update(p.relative_to(R).as_posix() for p in S.iterdir() if p.is_file() and p.suffix in ['.c','.h','.asm','.exe','.json'] and p.name not in ['source-manifest.json','document-manifest.json','validation.json','final-check.json'])
paths.update(p.relative_to(R).as_posix() for p in (S/'fixtures').iterdir() if p.is_file());manifest=[]
for rel in sorted(paths):
 d=S/'final-source'/rel;d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/rel,d);manifest.append(dict(path=rel,sha256=sha(d)))
write(S/'source-manifest.json',manifest)
docs=[P/'README.md',report,handoff,policy,addendum]+[P/n for n in ['交接文档-原版逆向与C重编译-20261020.txt','交接文档-新对话继续推进-20261022.txt']]+[P/'reports'/n for n in ['latest-recovery.json','latest-state-comparison.json','latest-movement-candidate.json']];documents=[]
for p in docs:
 d=S/'current-project'/p.relative_to(P);d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,d);documents.append(dict(path=p.relative_to(P).as_posix(),sha256=sha(d)))
write(S/'document-manifest.json',documents)
write(S/'validation.json',dict(**pointer,parent_commit=parent,state_schema=12,accepted_game_pairs=pairs,accepted_frames=frames,production_c_sources=181,content_inputs=312,unsupported_guards=37,native_cases=458752,probes=3,synthetic_cases=0,inherited_heap_improvement=True,new_traffic_recipes=2,new_traffic_pairs=4,new_traffic_frames=12004,capture_packet_cases_inherited=64,transport_packet_cases_inherited=128,accepted_inherited_variations=4,strict_game_pairs=strict,functional_game_pairs=functional,strict_all_frames_equal=False,source_files=len(manifest),finite_functional_conformance=True,bug_for_bug_required=False,cleanup_performed_this_round=True,pushed=False))
write(S/'final-check.json',dict(passed=True,exe_sha256=digest,source_manifest_sha256=sha(S/'source-manifest.json'),document_manifest_sha256=sha(S/'document-manifest.json'),pushed=False))
print(dict(passed=True,generation=62,exe_sha256=digest,source_files=len(manifest),pairs=pairs,frames=frames,native_cases=458752,new_traffic_recipes=2))
