"""Promote result consumption, movement-queue handoff and longer ordinary traffic."""
from run_batch_v61 import *
if '--freeze-lineage' in sys.argv:
 lineage=read(S/'checker-lineage.json')
 for e in lineage['entries']:
  e['final_derived_sha256']=sha(R/e['derived']);e['unchanged_after_initial_derivation']=e['final_derived_sha256']==e['derived_sha256']
 (S/'checker-lineage.json').write_text(json.dumps(lineage,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print('Current checker lineage frozen before cleanup.');raise SystemExit(0)
for name in ['native-gates.json','effects.json','traffic-effects.json','traffic-reissue-motion.json','preservation.json','cleanup.json','final-scene-matrix.json','rng-functional-impact.json','rng-first-split-window.json','boundary-inheritance.json','service-boundaries.json','infrastructure-status.json','baseline-native-identity.json','community-reference-review.json','heap-improvement-inheritance.json','short-traffic-inheritance.json']:
 assert read(S/name)['passed'],name
receipt=read(R/'ra2/build-original-c/source-content-receipt.json');digest=sha(R/'ra2/build-original-c/ra2.exe')
matrix=read(S/'final-scene-matrix.json');native=read(S/'native-gates.json');clean=read(S/'cleanup.json');traffic=read(S/'traffic-effects.json')
parts=[read(S/'parts'/n/'validation.json') for n in ['consumer','queue']];before=read(S/'traffic-baseline-scenes.json');assert parts[-1]['exe_sha256']==digest
pairs=sum(x['scene_count'] for x in parts)+len(matrix['results'])+len(before['results'])
frames=sum(x['frames'] for x in parts)+sum(x['frames'] for x in matrix['results']+before['results'])
strict=sum(x['scene_count'] for x in parts)+sum(x['strict_trace_equal'] for x in matrix['results']+before['results']);functional=pairs-strict
assert (pairs,frames,strict,functional)==(19,28669,15,4)
assert native['groups']==3 and native['cases']==196608 and all(read(S/n)['cases']==65536 for n in native['receipts'])
refs=read(S/'community-reference-review.json');assert len(refs['sources'])==5 and sha(S/'community-reference-review.json')==sha(O/'community-reference-review.json')
parent=read(S/'vcs-context.json')['parent_commit'];report=P/'docs/单位移动第六十批-路径消费队列衔接与长交通-20261025.txt';handoff=P/'交接文档-单位移动第六十批正式验收-20261025.txt'
policy=P/'docs/项目目标与验收边界-20261024.txt';addendum=P/'docs/寻路机制改进验收补充-20261025.txt'
traffic_lines=[]
for tag,x in traffic['scenes'].items():
 assert x['per_mode_traces_equal_prechange'] and x['strict_trace_equal']
 m=x['modes']['original'];moving=sum(q['was_moving'] and q['old_goal_unfinished'] for q in m['moving_reissues'])
 windows='；'.join(f"{w['window'][0]}..{w['window'][1]}帧中至少三单位同时移动{w['simultaneous_three_or_more_frames']}帧" for w in m['activity_windows'])
 traffic_lines.append(f"{tag}：全程至少三单位同时移动{m['simultaneous_three_or_more_frames']}帧，近距离同时运动{m['nearby_simultaneous_motion_frames']}帧（平面最大轴差<=768）；{moving}次改发前一帧有位移且旧目标未完成。活动分窗：{windows}。")
report.write_text(f'''单位移动第六十批（正式60 / 验证61），2026-10-25。
父提交：{parent}。
程序：{R/'ra2/build-original-c/ra2.exe'}
SHA-256：{digest}
验收边界：{policy}
寻路机制改进补充：{addendum}

范围与结果
按整体功能、效果、规则与资源调用验收，不追求逐个BUG复刻，允许有证据支持的寻路机制改进。本批整理ground_followup的路径结果消费和ground_template的24槽方向队列/路段提交，补充两个2401帧、四轮实际移动的长交通变体。仅改2个生产C文件；181C/312编译输入/37处未实现保护不变。头文件、CMake、规则/美术、生成入口/分发表、runtime桥接、schema12记录器和通用比较器未改。
前批完成/重建服务、共享ground_rebuild_result策略、堆满保留较低priority候选和节点服务保持。当前没有新的算法或容量变化，不把既有7412项预期差异或65541项合成见证计入本批新门禁，也不声称自然场景已触发堆满改善或普遍最短路径。

第一部分consumer：缺方向后的结果消费
候选准备后先读第二方向；非-1直接返回，缺方向且距离<=512时仍走force_straight。consume_followup_rebuild分离远目标的train查询、重建、共享返回策略和方向重取。
传入候选准备之前取得的context，不能在回调后重新取services->context。train仍先于重建查询，检查服务表在重建后构造；成功重建以check_success=0进入共享策略，按原约定略过owner复核。失败后owner不存在则写aborted并返回；目标拒绝会停止导航，但该入口随后仍重新读取第二方向。没有把它合并成Prepare失败出口的直接返回，也不增加预算、方向缓存或提前读取。
速度准备函数和共享ground_rebuild_result/Prepare策略源字节未改。函数签名、Ra2FollowupResult布局及运行时接续地址保持。

第二部分queue：24槽方向消费与路段提交
consume_direction_queue把普通弹出和保留队列区分：普通入口按原顺序移动23槽，尾值改-1；保留入口不移动前23槽，但仍把指定terminal_direction写入第23槽。返回的实际尾值继续用于失败回退，不扩大缓冲或改变方向规则。
prepare_segment_publication依次按向零除256/16位截断写目标格、清sound_pending、置sample_index=0；旧segment_end非invalid时才置invalid并清driving，已经invalid的旧段不额外清driving。
随后仍调用原有segment admission，保留候选发布、accepts_owner、flag76、start/存活复核的次序。成功开始直接返回；其余结果由reject_queued_segment依次写selector、队首和零速度，不加新owner门禁、不提前清目标。模板选择、方向归一化、表查询和准入服务源字节未改。

原版1.006门禁
followup_probe.c使用已验v44原字节，phase1共65536例；template_probe.c使用已验v45原字节，phase1普通弹出和phase2保留队列各65536例。合计196608例，改动前、第一段后和第二段后均执行，不把重复输入累计成589824个新用例。原探针代码、程序与header独立保留baseline-probe。
比较原版映射片段的状态/方向缓冲、返回与接续、有序服务调用、活跃栈局部量、被检查ABI和控制字，有限输入均通过。probe依赖从已验v44/v45构建配方出发，按现有gameplay定义解析闭包；仅补既有bridge_plane/segment_admission等依赖，不修改生产构建或探针桩。构建计划与来源哈希单独留存。
速度phase0、模板选择phase0/3/4、其他Prepare/转向片段未重跑，不计本批覆盖；片段桩不证明全部ABI、任意回调或所有自然入口。

更长的自然交通
traffic-long-cross和traffic-long-convoy在父批两个901帧配方上扩展至2401帧；地图字节、地形包、规则与原始单位配置不变。3辆TRUCKA和1名E2使用普通Move事件，初始交错/错峰后，在550、1100、1650附近再次发令和中途改发；最后留出到达与Guard稳定检查时间。
每个配方检查四个活动窗口0..500、550..1050、1100..1600、1650..2250：各窗口至少三单位同时移动>=8帧，四个单位各有>=5帧真实位移。持续活动和关键改发的实际统计如下：
{chr(10).join(traffic_lines)}
改发状态直接比较前两帧位置并与旧目标核对；无位移或已到达旧目标的改发单列，不算行进中未完成目标改发。每个普通命令的提交格、event_frame/单位/任务执行均核对。全程生命、合法陆地/零层高、车辆非空路径缓冲、现有stage6结果、最终格和Guard均通过。
两配方在改生产代码前由原版与父批正式程序各运行，再由最终程序各运行，均严格通过；每模式完整轨迹等于本轮冻结基线。2个长配方改前/后共4配对9604帧，不写成4个独立新场景。前批两个短配方按哈希保留，不重复计覆盖。使用正式生产程序和既有只读观测，无状态/路径结果注入或新增生产钩子；不证明大规模交通、锁步网络或全图最优。

既有回归与原版异常
两段各默认301、北桥501、南桥501帧，3配对1303帧全部严格。最终mi/sc/aw3/fm装卸和岸边交通完整轨迹等于父批本模式；旧货车原版2020/C2018、步兵原版2219/C2220等差异和通用严格false保留。随机首差仍mi/sc/aw3第349帧、fm第350帧，仅只读窗口，不改种子/随机流或比较器。
列车碰撞、碾压、重复寻路失败和弯曲高差严格通过；原版Z436停滞、Z-193未完成等异常输入/轨迹/基线保留，不转成必须逐BUG复刻。旧岸边失败、远目标、坡型8/飞机及碰撞负控制按boundary-inheritance.json继承，未全量重跑；29非主C/86入边按哈希继承，无新自然非主入口结论。

社区线索与保护
继续继承父批已核对的5项固定提交/内容哈希：gagarin YR1.001 AStar/FootClass结构和调用线索、EA旧Red Alert候选检查与成功发布组织、Phobos引擎扩展定位。它们用于定位和服务命名；未引入第三方引擎实现、不直接套不同版本地址/规则，原版1.006仍是对照依据。详见community-reference-review.json。
总{pairs}配对{frames}模拟帧，{strict}严格、{functional}既有局部功能差异通过；固定seed12345和模拟帧发令，构建串行，最多两条配对通道/四个游戏进程。原版片段、普通交通、既有独立观测宿主和继承证据分开记载。
父批412项封存、315项独立基线、两段回退、改前探针/宿主、长交通完整基线保留。H盘20项原始输入、原版game.exe/SAVE0029、原规则、旧手写引擎、Git配置及远端引用不变。
逐路径/类型/哈希清理{clean['deleted_files']}项可重建文件/缓存，共{clean['deleted_bytes']}字节，同目录{clean['protected_files']}项保护文件哈希不变。源码、正式程序、资源、基线、回退、轨迹与原版异常保留。本地提交，不推送。
复核：{R/'verify_final_movement_v61.py'}；提交收据：{S/'postcommit/git-local-commit.json'}。
下一步按功能需要检查队列耗尽后的重试/到达衔接及不同通道交通，或有度量支持的寻路改进；其他引擎子系统与完整视觉/资源调用验收仍未覆盖，不宣称全游戏等价。
''',encoding='utf-8',newline='\n')
handoff.write_text(f'''当前正式60 / 验证61，2026-10-25。
父提交：{parent}；程序SHA-256：{digest}。
政策：{policy}
机制补充：{addendum}
报告：{report}
ground_followup分离缺方向的远目标重建结果消费，保留候选准备前context、train先查、成功略过owner复核、无owner中止、拒绝后仍重取方向。ground_template分离24槽弹出/保留、目标格与计数发布、准入后回退；旧invalid段不额外清driving，尾值沿用原策略。只改2C，181C/312输入/37保护不变，前批共享结果策略、完成重建及堆容量改进保持。
原版消费phase1/队列弹出phase1/保留phase2各65536，共196608例；改前和两段后通过，重复不累计。原始探针固定来源v44 followup/v45 template，现有gameplay依赖闭包有独立构建收据；未改探针桩或生产构建。不计速度、其他模板选择和全部ABI覆盖。
两个长交通变体均2401帧，继承原地图/规则，四轮实际发令；四个活动窗口均满足并行移动，关键改发按前一帧真实位移判定。3TRUCKA+1E2普通Move，最终目标/Guard、生命、合法落格、路径缓冲及现有stage6结果通过。改前/后4配对9604帧均严格，完整每模式轨迹等于冻结基线。短901帧配方按哈希保留，无状态/结果注入或新生产钩子。
总19配对28669帧，15严格、4沿用局部功能差异；mi/sc/aw3/fm旧严格false、1/2帧时序、349/350随机窗口及Z436/Z-193原版异常保留。29非主C/86入边和旧边界按哈希继承。
社区5项固定来源及原版1.006对照继续使用：{S/'community-reference-review.json'}。前批7412预期堆差异及65541合成见证按哈希继承，不计本批新用例；允许有证据的机制改进，不保证全图最短。
基线：{S/'baseline'}；回退：{S/'parts'}；原版探针：{S/'baseline-probe'}；宿主：{S/'baseline-observer'}；长交通改前记录：{S/'runs/b-traffic-long-cross'}、{S/'runs/b-traffic-long-convoy'}；封存：{S/'final-source'}。
已核对哈希清理{clean['deleted_files']}项可重建文件；原始资源、旧引擎、基线回退和全部历史证据保留。本地提交，不推送。
下一步按功能需要推进队列耗尽后的重试/到达衔接及不同通道交通，或有证据的搜索改进；全游戏及完整视觉/资源验收未覆盖。
派生后续工具须显式指定父证据movement-state-v61并保留导入校验。复核：{R/'verify_final_movement_v61.py'}。
''',encoding='utf-8',newline='\n')
lead=f'最新接续：第六十批正式60 / 验证61已验收。\n交接：{handoff}\n政策：{policy}\n机制改进补充：{addendum}\nEXE：{digest}\n以下历史原地保留。\n\n'.encode('utf-8')
for name in ['交接文档-原版逆向与C重编译-20261020.txt','交接文档-新对话继续推进-20261022.txt']:
 p=P/name;p.write_bytes(lead+p.read_bytes())
p=P/'README.md';ls=p.read_bytes().splitlines(keepends=True);eol=b'\r\n' if ls[0].endswith(b'\r\n') else b'\n'
p.write_bytes('> 当前研究路线（2026-10-25）：原版1.006 C17/x86单位移动第六十批已验收。路径结果消费、方向队列衔接与长交通；[第六十批交接](交接文档-单位移动第六十批正式验收-20261025.txt)。遵守[整体功能与效果边界](docs/项目目标与验收边界-20261024.txt)和[机制改进补充](docs/寻路机制改进验收补充-20261025.txt)。'.encode('utf-8')+eol+b''.join(ls[1:]))
p=R/'ra2/src/gameplay/阅读说明-单位移动.txt';p.write_bytes(f'第六十批（2026-10-25）\n缺方向结果消费、24槽队列及路段提交；两个2401帧四轮活动的长交通变体。181C/312输入/37保护，19配对28669帧，原版消费/队列196608例。\n前批有证据的堆容量改进及全部原版差异、异常和基线回退保留。\n报告：{report}\n\n'.encode('utf-8')+p.read_bytes())
pointer=dict(passed=True,status='promoted',formal_baseline_generation=60,verification_round=61,validation=str(S/'validation.json'),exe_sha256=digest,sha256=digest,executable=str(R/'ra2/build-original-c/ra2.exe'),full_original_equivalence_verified=False,report=str(report),handoff=str(handoff),acceptance_policy=str(policy),pathfinding_policy_addendum=str(addendum),path_mechanism_identity_required=False,globally_shortest_paths_verified=False)
for name in ['latest-recovery.json','latest-state-comparison.json','latest-movement-candidate.json']:
 p=P/'reports'/name;x=read(p);x.update(pointer)
 x['current_batch']=dict(formal_generation=60,verification_round=61,accepted_game_pairs=pairs,accepted_frames=frames,native_cases=196608,native_groups=3,synthetic_cases=0,inherited_heap_improvement=True,new_traffic_recipes=2,production_c_sources=181,content_inputs=312,strict_all_frames_equal=False,accepted_baseline_variations=4,strict_game_pairs=strict,functional_game_pairs=functional)
 p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
write(S/'remaining-work.json',dict(passed=True,bug_for_bug_required=False,path_mechanism_identity_required=False,globally_shortest_paths_verified=False,natural_alias_dispatch_required=False,candidates_not_confirmed_failures=True,community_references_available=True,remaining=['Queue exhaustion, retry/arrival integration and different traffic channels as functionally needed','Broader ordinary traffic and evidence-supported search improvements','Other engine subsystems and full visual/resource acceptance']))
for e in read(S/'checker-lineage.json')['entries']:assert e['final_derived_sha256']==sha(R/e['derived'])
paths={Path(p).relative_to(R).as_posix() for p in receipt['inputs']}
paths.update(['ra2/CMakeLists.txt','ra2/run_lift.py','ra2/tools/playtest.py','ra2/build-original-c/ra2.exe','ra2/build-original-c/source-content-receipt.json','ra2/src/gameplay/阅读说明-单位移动.txt','build-faithful.ps1','run_fixture_comparison.py','run_state_comparison.py','evidence/movement-state-v4/SOV01T-original.MAP'])
paths.update(p.relative_to(R).as_posix() for p in R.glob('*v61*') if p.is_file())
paths.update(p.relative_to(R).as_posix() for p in S.iterdir() if p.is_file() and p.suffix in ['.c','.h','.asm','.exe','.json'] and p.name not in ['source-manifest.json','document-manifest.json','validation.json','final-check.json'])
paths.update(p.relative_to(R).as_posix() for p in (S/'fixtures').iterdir() if p.is_file());manifest=[]
for rel in sorted(paths):
 d=S/'final-source'/rel;d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/rel,d);manifest.append(dict(path=rel,sha256=sha(d)))
write(S/'source-manifest.json',manifest)
docs=[P/'README.md',report,handoff,policy,addendum]+[P/n for n in ['交接文档-原版逆向与C重编译-20261020.txt','交接文档-新对话继续推进-20261022.txt']]+[P/'reports'/n for n in ['latest-recovery.json','latest-state-comparison.json','latest-movement-candidate.json']];documents=[]
for p in docs:
 d=S/'current-project'/p.relative_to(P);d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,d);documents.append(dict(path=p.relative_to(P).as_posix(),sha256=sha(d)))
write(S/'document-manifest.json',documents)
write(S/'validation.json',dict(**pointer,parent_commit=parent,state_schema=12,accepted_game_pairs=pairs,accepted_frames=frames,production_c_sources=181,content_inputs=312,unsupported_guards=37,native_cases=196608,probes=3,synthetic_cases=0,inherited_heap_improvement=True,new_traffic_recipes=2,new_traffic_pairs=4,new_traffic_frames=9604,capture_packet_cases_inherited=64,transport_packet_cases_inherited=128,accepted_inherited_variations=4,strict_game_pairs=strict,functional_game_pairs=functional,strict_all_frames_equal=False,source_files=len(manifest),finite_functional_conformance=True,bug_for_bug_required=False,cleanup_performed_this_round=True,pushed=False))
write(S/'final-check.json',dict(passed=True,exe_sha256=digest,source_manifest_sha256=sha(S/'source-manifest.json'),document_manifest_sha256=sha(S/'document-manifest.json'),pushed=False))
print(dict(passed=True,generation=60,exe_sha256=digest,source_files=len(manifest),pairs=pairs,frames=frames,native_cases=196608,new_traffic_recipes=2))
