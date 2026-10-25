"""Promote queue-exhaustion retry/arrival services and distinct traffic channels."""
from run_batch_v62 import *
if '--freeze-lineage' in sys.argv:
 lineage=read(S/'checker-lineage.json')
 for e in lineage['entries']:
  e['final_derived_sha256']=sha(R/e['derived']);e['unchanged_after_initial_derivation']=e['final_derived_sha256']==e['derived_sha256']
 (S/'checker-lineage.json').write_text(json.dumps(lineage,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print('Current checker lineage frozen before cleanup.');raise SystemExit(0)
for name in ['native-gates.json','effects.json','traffic-effects.json','traffic-reissue-motion.json','channel-comparison.json','channel-land-proof.json','preservation.json','cleanup.json','final-scene-matrix.json','rng-functional-impact.json','rng-first-split-window.json','boundary-inheritance.json','service-boundaries.json','infrastructure-status.json','baseline-native-identity.json','community-reference-review.json','heap-improvement-inheritance.json','prior-traffic-inheritance.json']:
 assert read(S/name)['passed'],name
receipt=read(R/'ra2/build-original-c/source-content-receipt.json');digest=sha(R/'ra2/build-original-c/ra2.exe')
matrix=read(S/'final-scene-matrix.json');native=read(S/'native-gates.json');clean=read(S/'cleanup.json');traffic=read(S/'traffic-effects.json')
parts=[read(S/'parts'/n/'validation.json') for n in ['retry','arrival']];before=read(S/'traffic-baseline-scenes.json');assert parts[-1]['exe_sha256']==digest
pairs=sum(x['scene_count'] for x in parts)+len(matrix['results'])+len(before['results'])
frames=sum(x['frames'] for x in parts)+sum(x['frames'] for x in matrix['results']+before['results'])
strict=sum(x['scene_count'] for x in parts)+sum(x['strict_trace_equal'] for x in matrix['results']+before['results']);functional=pairs-strict
assert (pairs,frames,strict,functional)==(19,28669,15,4)
assert native['groups']==3 and native['cases']==229376
assert sorted(read(S/n)['cases'] for n in native['receipts'])==[32768,65536,131072]
refs=read(S/'community-reference-review.json');assert len(refs['sources'])==5 and sha(S/'community-reference-review.json')==sha(O/'community-reference-review.json')
parent=read(S/'vcs-context.json')['parent_commit'];report=P/'docs/单位移动第六十一批-队列耗尽重试到达与不同通道交通-20261025.txt';handoff=P/'交接文档-单位移动第六十一批正式验收-20261025.txt'
policy=P/'docs/项目目标与验收边界-20261024.txt';addendum=P/'docs/寻路机制改进验收补充-20261025.txt'
traffic_lines=[]
for tag,x in traffic['scenes'].items():
 assert x['per_mode_traces_equal_prechange'] and x['strict_trace_equal']
 m=x['modes']['original'];moving=sum(q['was_moving'] and q['old_goal_unfinished'] for q in m['moving_reissues'])
 windows=' / '.join(str(w['simultaneous_three_or_more_frames']) for w in m['activity_windows'])
 traffic_lines.append(f"{tag}：高度{m['expected_height']}；四窗至少三单位同时移动帧数{windows}；{moving}次改发前一帧有位移且旧目标未完成；{len(m['empty_arrival_reissues'])}次空队列到达后再发并回到Guard的见证。")
arrival=read(S/'part-arrival-arrival.json')
report.write_text(f'''单位移动第六十一批（正式61 / 验证62），2026-10-25。
父提交：{parent}。
程序：{R/'ra2/build-original-c/ra2.exe'}
SHA-256：{digest}
验收边界：{policy}
机制补充：{addendum}

范围
按整体功能、效果、规则和资源调用验收，不追求逐个BUG复刻，允许有证据支持的寻路机制改进。本批整理队列耗尽后的重试、空队列处理与到达衔接，生产仅改ground_drive.c、ground_prepare.c、ground_arrival.c。181C/312编译输入/37处未实现保护不变，头文件、CMake、规则/美术、生成入口/分发表、runtime桥接、schema12记录器和通用比较器未改。
前批路径完成/重建、结果消费、24槽提交和固定容量堆改进保持。本批未引入新的算法/容量变化；已有7412项预期堆差异、65541项合成见证按哈希继承，不计当前新门禁，不保证全图最短。

第一段retry：活动段耗尽与重试
resume_exhausted_segment保留先Advance(0)、再按返回/存活决定是否继续的顺序；路段未耗尽、停止且队首为空、特定owner标志等仍只finish_frame。需要新段时保留目标类别查询/目标同步，使用continuing=1进入prepare_and_advance，避免本帧再次累计速度；普通新段仍传0。
stop_if_already_arrived只归拢原来的目标格已在当前格及Guard位置已到目的地两种停止判断，不改变短路查询顺序或stop_navigation返回处理。转向刷新和任务等待仍按旧顺序执行。
handle_empty_queue在原有“不移动且队首-1”门禁之后运行：flag325清路段与速度，其余按目标存在性同步目的地，然后finish_frame；空队列不直接启动新段。目标拒绝分支仍先清路段，再执行Stop，不缓存回调前状态。
ground_prepare把计时通过后的延迟查询、重启计时、重建和失败后复核分离为restart_and_rebuild_path。计时器32位回绕、elapsed/remaining判断和准备入口源逻辑保留；delay先查、timer再重启、rebuild后才查owner/目标，services->context仍在原位置实时读取。失败后的距离阈值、两次任务查询、取消/停止和存活判断不合并。

第二段arrival：落位、层高与任务收尾
publish_arrived_segment先根据向零除256/16位格坐标比较决定relocate参数，再按回调后的状态废弃segment_end/driving，清selector和sample_index。
mark_reached_destination先查目标是否当前格，再读owner参考高度；之后才读destination.z。保留无符号差量/绝对值回绕和2*level_height回绕容差的严格小于比较，不改为<=。确认到达后清destination及路段状态。
finish_after_refresh及共享owner completion保持：刷新后再查可用性，必要时取消目标/路径并处理Move任务，再查询owner更新和存活；不提前缓存任务或owner状态。函数签名、布局、原版数值语义和运行时接续保持。

原版1.006验证
drive_process_probe采用已验v46原字节，32768例；prepare_probe采用v52原字节，entry与retry各65536例；arrival_probe采用v46原字节，65536例。合计229376例，改前、第一段后和第二段后均执行，相同输入重复不累计。原版状态、调用顺序及探针所检查的返回/寄存器/标志/栈局部量/控制字均通过；不同组的检查范围见各自字段，不宣称全ABI。
到达探针本轮继续到下一阶段{arrival['continued']}例、返回{arrival['returned']}例，均为合法出口分类。原探针源码/程序/header独立保留baseline-probe；既有构建配方经gameplay依赖闭包补足当前依赖，不修改探针桩或生产构建。其他移动片段及未观测自然入口不计本轮覆盖。

不同通道自然交通
平地岸边通道使用原地图字节，3TRUCKA+1E2在0高度执行四轮活动，并加入到达后再次发令。高架道路通道使用已验北向交通地图原字节，同样3TRUCKA+1E2，先等待/释放，再双向往返、改发及到达后再发；实际经过Road=1、基础层高4，单位高度416。两个配方均2401帧，规则、地形包和单位配置未改。
高架记录不作为新Bridge flag切换证明。基线初次检查漏列Road=1，实际高度始终416，原版/C原始比较已严格通过；原地形表与H盘原rules.ini的[Road]确认Foot/Wheel=100%。仅修正专用通道检查器，复用完整轨迹；没有重跑游戏、改生产/地图/规则或放宽通用比较器。证据见channel-land-proof.json及channel-comparison.json。
{chr(10).join(traffic_lines)}
空队列到达再发按改发前位置、空路径/selector和Guard核对；既有目标到达后再发新目标或同格目标均单列，不把全部见证写成同格再发。行进中未完成目标改发按前一帧真实位移判定。四个活动窗口均至少三单位同时移动>=8帧，四单位各有>=5帧真实移动；全程生命、合法通道/高度、路径方向缓冲、现有stage6结果、提交/执行事件、最终目标和Guard通过。
两个配方在改代码前由原版/父批程序运行，最终程序再各运行，共4配对9604帧，均严格；每种模式完整轨迹等于冻结基线。前批长交通按哈希保留不重计。使用正式程序、普通Move和既有只读观测，无状态/结果注入或新增生产钩子，不证明大规模交通、网络或所有层切换。

回归、社区与保护
两段各默认301、北桥501、南桥501帧，3配对1303帧严格。最终mi/sc/aw3/fm装卸和岸边场景完整轨迹等于父批本模式；旧货车2020/2018、步兵2219/2220、严格false及349/350随机首差窗口保留，不改种子/随机流/比较器。
列车碰撞、碾压、重复失败和弯曲高差严格通过；原版Z436停滞、Z-193未完成等异常输入/轨迹/基线保留，不要求逐BUG复刻。旧岸边失败、远目标、坡型8/飞机、碰撞负控制及29非主C/86入边按哈希继承，未全量重跑，无新自然非主入口结论。
继续使用父批已核对的5项固定提交/内容哈希：gagarin YR1.001结构与调用线索、EA旧Red Alert检查/发布组织、Phobos扩展定位。用于定位和服务组织，不直接套版本地址/规则或引入第三方引擎实现；原版1.006仍为对照依据，详见community-reference-review.json。
总{pairs}配对{frames}模拟帧，{strict}严格、{functional}既有局部功能差异通过。固定seed12345和模拟帧发令，构建串行，最多两条配对通道/四个游戏进程；映射片段、自然通道、独立观测宿主与继承证据分开。
父批417项封存、315项独立基线、两段回退、改前探针/宿主与两个通道基线保留。H盘20项原始输入、原版game.exe/SAVE0029、原规则、旧手写引擎、Git配置和远端引用不变。
逐路径/类型/哈希清理{clean['deleted_files']}项可重建文件/缓存，共{clean['deleted_bytes']}字节，同目录{clean['protected_files']}项保护文件哈希不变。保留源码、正式程序、资源、基线、回退、轨迹和原版异常。本地提交，不推送。
复核：{R/'verify_final_movement_v62.py'}；提交收据：{S/'postcommit/git-local-commit.json'}。
下一步按功能需要推进等待/障碍释放后的恢复衔接、更多层高/通道交互或有度量的寻路改进；其他子系统和完整视觉/资源验收未覆盖，不宣称全游戏等价。
''',encoding='utf-8',newline='\n')
handoff.write_text(f'''当前正式61 / 验证62，2026-10-25。
父提交：{parent}；程序SHA-256：{digest}。
政策：{policy}
机制补充：{addendum}
报告：{report}
ground_drive整理活动段耗尽、已到达停止、空队列处理，保留同帧接续1/新段0及回调后存活/状态查询。ground_prepare分离计时通过后的delay/timer/rebuild/失败复核，保留回绕和实时context。ground_arrival分离relocate后发布、严格层高到达判定与任务收尾，owner刷新/取消/存活顺序保持。只改3C，181C/312输入/37保护不变。
原版Drive32768、Prepare entry/retry各65536、Arrival65536，共229376例，改前和两段后通过，重复不累计。到达继续{arrival['continued']}、返回{arrival['returned']}，均合法出口；探针被检查ABI/状态/调用通过，不宣称全部ABI。
平地岸边0高度和高架道路416高度两个通道，各2401帧、四轮活动；3TRUCKA+1E2普通Move，无状态/结果注入或新生产钩子。高架实际Road=1/基础层高4，不作为新Bridge flag切换证明。检查器漏列Road已据原地形表和[Road] Foot/Wheel=100%纠正，原始比较严格通过、轨迹未重跑、规则/地图未改，见channel-land-proof.json。
改前/后4配对9604帧均严格，完整每模式轨迹等于冻结基线；平地/高架基线有9/4个空队列到达再发见证，最终统计详见traffic-effects/channel-comparison。全程生命、合法落格/高度、队列方向、stage6、最终目标/Guard及真实改发通过。
总19配对28669帧，15严格、4既有局部功能差异；mi/sc/aw3/fm旧时序、严格false、349/350窗口及Z436/Z-193原版异常保留；旧边界与29非主C/86入边按哈希继承。
前批完整服务和有证据的堆容量改进保持，7412预期差异/65541合成见证不计当前新覆盖。社区5项固定线索继续继承：{S/'community-reference-review.json'}，原版1.006仍为对照；允许机制改进，不保证全图最短。
基线：{S/'baseline'}；回退：{S/'parts'}；原版探针：{S/'baseline-probe'}；宿主：{S/'baseline-observer'}；通道改前记录：{S/'runs/b-traffic-channel-flat'}、{S/'runs/b-traffic-channel-deck'}；封存：{S/'final-source'}。
已哈希核对清理{clean['deleted_files']}项可重建文件；原始输入、资源、旧引擎和历史证据保留。本地提交，不推送。
下一步按功能需要推进等待/障碍释放后的恢复、更多层高与通道交互，或有证据的搜索改进；全游戏及完整视觉/资源验收仍未覆盖。
派生下一批须显式指定父证据movement-state-v62并保留导入校验。复核：{R/'verify_final_movement_v62.py'}。
''',encoding='utf-8',newline='\n')
lead=f'最新接续：第六十一批正式61 / 验证62已验收。\n交接：{handoff}\n政策：{policy}\n机制改进补充：{addendum}\nEXE：{digest}\n以下历史原地保留。\n\n'.encode('utf-8')
for name in ['交接文档-原版逆向与C重编译-20261020.txt','交接文档-新对话继续推进-20261022.txt']:
 p=P/name;p.write_bytes(lead+p.read_bytes())
p=P/'README.md';ls=p.read_bytes().splitlines(keepends=True);eol=b'\r\n' if ls[0].endswith(b'\r\n') else b'\n'
p.write_bytes('> 当前研究路线（2026-10-25）：原版1.006 C17/x86单位移动第六十一批已验收。队列耗尽后的重试/到达衔接及不同通道交通；[第六十一批交接](交接文档-单位移动第六十一批正式验收-20261025.txt)。遵守[整体功能与效果边界](docs/项目目标与验收边界-20261024.txt)和[机制改进补充](docs/寻路机制改进验收补充-20261025.txt)。'.encode('utf-8')+eol+b''.join(ls[1:]))
p=R/'ra2/src/gameplay/阅读说明-单位移动.txt';p.write_bytes(f'第六十一批（2026-10-25）\n队列耗尽/重试/到达衔接；平地与高架道路两个2401帧通道。181C/312输入/37保护，19配对28669帧，原版耗尽/重试/到达229376例。\n前批有证据的堆容量改进及全部原版差异、异常和基线回退保留。\n报告：{report}\n\n'.encode('utf-8')+p.read_bytes())
pointer=dict(passed=True,status='promoted',formal_baseline_generation=61,verification_round=62,validation=str(S/'validation.json'),exe_sha256=digest,sha256=digest,executable=str(R/'ra2/build-original-c/ra2.exe'),full_original_equivalence_verified=False,report=str(report),handoff=str(handoff),acceptance_policy=str(policy),pathfinding_policy_addendum=str(addendum),path_mechanism_identity_required=False,globally_shortest_paths_verified=False)
for name in ['latest-recovery.json','latest-state-comparison.json','latest-movement-candidate.json']:
 p=P/'reports'/name;x=read(p);x.update(pointer)
 x['current_batch']=dict(formal_generation=61,verification_round=62,accepted_game_pairs=pairs,accepted_frames=frames,native_cases=229376,native_groups=3,synthetic_cases=0,inherited_heap_improvement=True,new_traffic_recipes=2,production_c_sources=181,content_inputs=312,strict_all_frames_equal=False,accepted_baseline_variations=4,strict_game_pairs=strict,functional_game_pairs=functional)
 p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
write(S/'remaining-work.json',dict(passed=True,bug_for_bug_required=False,path_mechanism_identity_required=False,globally_shortest_paths_verified=False,natural_alias_dispatch_required=False,candidates_not_confirmed_failures=True,community_references_available=True,remaining=['Recovery after waiting/obstacle release and further height/channel interactions as functionally needed','Broader ordinary traffic and evidence-supported search improvements','Other engine subsystems and full visual/resource acceptance']))
for e in read(S/'checker-lineage.json')['entries']:assert e['final_derived_sha256']==sha(R/e['derived'])
paths={Path(p).relative_to(R).as_posix() for p in receipt['inputs']}
paths.update(['ra2/CMakeLists.txt','ra2/run_lift.py','ra2/tools/playtest.py','ra2/build-original-c/ra2.exe','ra2/build-original-c/source-content-receipt.json','ra2/src/gameplay/阅读说明-单位移动.txt','build-faithful.ps1','run_fixture_comparison.py','run_state_comparison.py','evidence/movement-state-v4/SOV01T-original.MAP'])
paths.update(p.relative_to(R).as_posix() for p in R.glob('*v62*') if p.is_file())
paths.update(p.relative_to(R).as_posix() for p in S.iterdir() if p.is_file() and p.suffix in ['.c','.h','.asm','.exe','.json'] and p.name not in ['source-manifest.json','document-manifest.json','validation.json','final-check.json'])
paths.update(p.relative_to(R).as_posix() for p in (S/'fixtures').iterdir() if p.is_file());manifest=[]
for rel in sorted(paths):
 d=S/'final-source'/rel;d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/rel,d);manifest.append(dict(path=rel,sha256=sha(d)))
write(S/'source-manifest.json',manifest)
docs=[P/'README.md',report,handoff,policy,addendum]+[P/n for n in ['交接文档-原版逆向与C重编译-20261020.txt','交接文档-新对话继续推进-20261022.txt']]+[P/'reports'/n for n in ['latest-recovery.json','latest-state-comparison.json','latest-movement-candidate.json']];documents=[]
for p in docs:
 d=S/'current-project'/p.relative_to(P);d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,d);documents.append(dict(path=p.relative_to(P).as_posix(),sha256=sha(d)))
write(S/'document-manifest.json',documents)
write(S/'validation.json',dict(**pointer,parent_commit=parent,state_schema=12,accepted_game_pairs=pairs,accepted_frames=frames,production_c_sources=181,content_inputs=312,unsupported_guards=37,native_cases=229376,probes=3,synthetic_cases=0,inherited_heap_improvement=True,new_traffic_recipes=2,new_traffic_pairs=4,new_traffic_frames=9604,capture_packet_cases_inherited=64,transport_packet_cases_inherited=128,accepted_inherited_variations=4,strict_game_pairs=strict,functional_game_pairs=functional,strict_all_frames_equal=False,source_files=len(manifest),finite_functional_conformance=True,bug_for_bug_required=False,cleanup_performed_this_round=True,pushed=False))
write(S/'final-check.json',dict(passed=True,exe_sha256=digest,source_manifest_sha256=sha(S/'source-manifest.json'),document_manifest_sha256=sha(S/'document-manifest.json'),pushed=False))
print(dict(passed=True,generation=61,exe_sha256=digest,source_files=len(manifest),pairs=pairs,frames=frames,native_cases=229376,new_traffic_recipes=2))
