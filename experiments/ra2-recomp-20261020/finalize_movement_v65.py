"""Promote Tube exit/connection recovery and finite per-vehicle queue traffic."""
from run_batch_v65 import *
if '--freeze-lineage' in sys.argv:
 lineage=read(S/'checker-lineage.json')
 for e in lineage['entries']:
  e['final_derived_sha256']=sha(R/e['derived']);e['unchanged_after_initial_derivation']=e['final_derived_sha256']==e['derived_sha256']
 (S/'checker-lineage.json').write_text(json.dumps(lineage,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print('Current checker lineage frozen before cleanup.');raise SystemExit(0)
for name in ['native-gates.json','effects.json','traffic-effects.json','mixed-recovery-effects.json','queue-recovery-effects.json','bridge-channel-effects.json','channel-comparison.json','traffic-event-linkage.json','channel-host-identity.json','current-explorations.json','preservation.json','cleanup.json','final-scene-matrix.json','rng-functional-impact.json','rng-first-split-window.json','boundary-inheritance.json','service-boundaries.json','infrastructure-status.json','baseline-native-identity.json','community-reference-review.json','heap-improvement-inheritance.json','prior-traffic-inheritance.json','prior-explorations.json','mixed-relocation-rle.json']:
 assert read(S/name)['passed'],name
receipt=read(R/'ra2/build-original-c/source-content-receipt.json');digest=sha(R/'ra2/build-original-c/ra2.exe')
matrix=read(S/'final-scene-matrix.json');native=read(S/'native-gates.json');clean=read(S/'cleanup.json');traffic=read(S/'traffic-effects.json')
parts=[read(S/'parts'/n/'validation.json') for n in ['exit','recovery']];before=read(S/'traffic-baseline-scenes.json');assert parts[-1]['exe_sha256']==digest
pairs=sum(x['scene_count'] for x in parts)+len(matrix['results'])+len(before['results'])
frames=sum(x['frames'] for x in parts)+sum(x['frames'] for x in matrix['results']+before['results'])
strict=sum(x['scene_count'] for x in parts)+sum(x['strict_trace_equal'] for x in matrix['results']+before['results']);functional=pairs-strict
assert (pairs,frames,strict,functional)==(23,47473,19,4)
assert native['groups']==6 and native['cases']==196608
assert sorted(read(S/n)['cases'] for n in native['receipts'])==[32768]*6
assert sha(S/'community-reference-review.json')==sha(O/'community-reference-review.json')
parent=read(S/'vcs-context.json')['parent_commit'];report=P/'docs/单位移动第六十四批-隧道出口恢复与桥隧队列交通-20261025.txt';handoff=P/'交接文档-单位移动第六十四批正式验收-20261025.txt'
policy=P/'docs/项目目标与验收边界-20261024.txt';addendum=P/'docs/寻路机制改进验收补充-20261025.txt'
recipes=read(S/'traffic-fixtures.json')['fixtures'];mixed=next(x for x in recipes if x['kind']=='mixed');queue=next(x for x in recipes if x['kind']=='queue')
queue_effect=read(S/'queue-recovery-effects.json')['scenes'][queue['observer_tag']]['original']['effects']
oldest=queue_effect['per_vehicle'][str(queue_effect['oldest_request_id'])]
mixed_effect=read(S/'mixed-recovery-effects.json')['scenes'][mixed['observer_tag']]['original']['effects']
report.write_text(f'''单位移动第六十四批（正式64 / 验证65），2026-10-25。
父提交：{parent}。
程序：{R/'ra2/build-original-c/ra2.exe'}
SHA-256：{digest}
验收边界：{policy}
机制补充：{addendum}

范围与服务
按整体功能、效果、规则和资源调用验收，不追求逐个BUG复刻，允许有证据支持的机制改进。本批生产仅改ground_tube_state.c、ground_landing.c、ground_failure.c；181C/312编译输入/37处未实现保护不变，头文件、构建清单、runtime桥接、生成入口/分发表、生产schema12记录器、通用比较器、规则与资源未改。
第一段exit：wait_for_occupied_exit把完整链快照、实时数量/类别查询与让路、阻塞速度、快照释放串成出口等待事务，仍先完成整条快照再调用让路；非类别1仍第二次查类别，数量仍可被回调改变，速度服务先于end_snapshot，返回值保留。
place_at_free_exit先落位再入格，之后restore_exit_navigation才查询目标是否出口格并按需请求自身让路，恢复任务、速度和后继连接朝向；保持入口捕获context，入格回调后的状态可见。路点对齐后重查结束标志的逻辑未改。
第二段recovery：admit_connection在leave/clear之后查连接索引和有效性，拒绝出口保持；成功先start_connection再设置approach。publish_connection_height依次查询当前/目标高度及duration，再用原数值规则计算和发布，不提前缓存owner或端点。
retry_failed_connection保持清路径、按计划重启计时、再准备的顺序；stop_failed_connection保持按计划清当前/保存路段再stop。clear_pending仍优先返回，七类失败入口的计划、截断/取消/低字节约定及捕获context不改。
本批无新增调度、路径容量或寻路算法变化；前批有证据的堆改进和7412预期差异/65541合成见证按哈希继承，不计当前新门禁，不保证全图最短。

原版1.006片段门禁
原字节tube-state v51出口/路点两组、remainder v50连接接纳/失败两组、progress v50未改动approach/continuation衔接两组，各32768，共196608例。改前和两段后均执行，重复不累计；未改动下游衔接门禁不虚称新增生产改动。
状态、回调值/顺序、返回与探针声明的寄存器/栈清理检查通过；控制字/全ABI不作超出字段的声明。浮点算法未改，前批数值验证按哈希保留。探针源码/header保持来源原字节，构建只补足现有gameplay传递依赖，baseline-probe与两段源/程序独立保留。

自然桥隧混合通道
{mixed['tag']}共3501帧，四辆普通TRUCKA。每辆先过原桥上层，再按普通Move路点经过同一图中双向弯曲Tubes，随后返回桥面并到达各自北向目标/Guard。不是在两个无关场景分别经过桥和隧道。
混合地图从已验桥下走廊出发，将已验平层十段Tube地形/覆盖局部平移[-8,-38]，入口/出口为60,76与70,76；只修改189个地形记录及对应覆盖区域、普通Units/Infantry/Tubes。原桥58..61、63..70范围覆盖字节及范围外覆盖保持；LZO/LCW往返校验、原版/C加载校准和完整移动均通过。无规则或全局美术资源变动，无原始路径/预算/运动状态注入。
每车有同一轨迹内的桥层标志、正向路由、反向路由和返桥先后见证：{mixed_effect}。

较大队列与有限饥饿恢复
{queue['tag']}共3601帧，12辆请求车辆加3辆普通Sleep出口占道车辆。最高actor ID收到第5帧最早请求，较低ID在100..450帧后到；占道车辆在1200/1300/1400帧分批Move释放。请求车辆没有收到重发目标来强迫恢复。
12辆全部保持生命、恢复并到达各自目标/Guard；其中{queue_effect['actual_tube_actors']}辆实际入隧道，{queue_effect['ground_bypass_actors']}辆普通地面绕行，出口终点静止等待峰值{queue_effect['peak_terminal_waiters']}辆。初始专用检查器把12辆请求都视为必经Tube，后据原版/C严格轨迹区分9辆入隧道与3辆绕行；复用原始轨迹，不修改生产/规则/地图或全局比较器，见queue-observation-review.json。
最早请求{queue_effect['oldest_request_id']}首次Tube进展{oldest['first_active_tube']}帧，出口连续静止{oldest['longest_terminal_wait']}帧；被{queue_effect['oldest_later_requests_exited_first']}个后到Tube请求先行通过，仍在{oldest['exit_publish_frame']}帧恢复出口发布，{oldest['arrival_frame']}帧到达。逐车请求、Tube或绕行分类、最大连续终点等待、出口发布、最终到达均单列，不以总体吞吐替代每车恢复。
此为有限到达序列中的长等待/被超越后恢复，不证明任意队长、持续无限新请求下无饥饿，也不作天然heap/vector容量饱和结论。

观测与成功验收
复用父批只读channel-observer字段，无新增游戏调用或原生钩子；每个新配方改前/最终各一组正式程序和一组独立观测。剔除fixture行后的全部生产记录逐模式完全相等，观测自身原版/C也严格通过；每种模式完整轨迹等于改前冻结数据。
两个配方与独立观测改前/后共8配对28408帧严格。全程生命、普通命令提交/执行、路径缓冲、stage6、最终目标与Guard通过。3次成功的0:1两帧actor校准仅用于绑定地图实际编号，单列不计自然交通；旧交通及其差异按哈希继承，不重计当前执行。
两段各默认301、北桥501、南桥501帧，共6配对2606帧严格。最终mi/sc/aw3/fm完整每模式轨迹等于父批，4项既有严格false、349/350随机首差窗口、原版/C货车2020/2018与步兵2219/2220时序保留。列车碰撞、碾压、重复失败及Z436/Z-193原版高差异常回归通过。
成功验收总{pairs}配对{frames}模拟帧，{strict}严格、{functional}既有局部功能差异。seed12345、模拟帧发令，构建串行、最多两条配对/四个游戏进程；不宣称全游戏或完整视觉资源等价。

失败候选与保护
远距离桥隧候选原版/C原始比较严格，但地面绕路未在下一订单前完成路点，实际没有Tube进展、最终目标未完成；两条5001帧轨迹、地图与命令保留，不计成功场景，也不归为已证实的原版Tube故障。近桥头首个literal LCW导出候选在原版/C加载时均失败；保留该地图、压缩前工具和错误，改用紧凑fill编码并约束压缩块长度后，同一局部组合通过原版/C加载和移动。离线往返通过不等于运行期接受；未据此修改游戏或资源。
两次0:0校准因最后帧必须为正数在模拟前被拒绝，原记录保留，修正为0:1。当前探索与检查器修正见current-explorations.json；父批长路径ra2.csf启动、范围校验、4→6停滞等全部按prior-explorations.json继承保留，不计当前新覆盖。
29非主C入口/86原始入边、旧岸边/坡型/飞机等边界按哈希保留，无新自然别名入口结论。继续使用已核对5项固定社区提交/内容哈希：gagarin的YR结构和桥层线索、EA旧Red Alert通行/发布组织、Phobos扩展定位。仅用于定位/组织，不套版本地址/规则或引入第三方引擎，不上传私有工程；原版1.006为对照。
父批{len(read(O/'source-manifest.json'))}项封存、315项独立基线、两段回退、改前探针/观测宿主及新交通基线保留。H盘20项原始输入、原版game.exe/SAVE0029、原rules和旧手写引擎、Git配置/远端引用不变。
按路径、类型、哈希与重解析点核对清理{clean['deleted_files']}项对象、缓存及重复导出，共{clean['deleted_bytes']}字节，{clean['protected_files']}项保护文件不变。正式程序、源、资源、基线、回退、轨迹及原版异常/失败候选保留。本地提交，不推送。
复核：{R/'verify_final_movement_v65.py'}；本地提交收据：{S/'postcommit/git-local-commit.json'}。
后续按功能需要研究持续新请求下的公平性、混合通道吞吐/饥饿边界及有度量的调度/寻路改进；当前无全图最优或无限负载活性保证。
''',encoding='utf-8',newline='\n')
handoff.write_text(f'''当前正式64 / 验证65，2026-10-25。
父提交：{parent}；程序SHA-256：{digest}。
报告：{report}
政策：{policy}
机制补充：{addendum}

ground_tube_state整理占用出口快照/让路/速度/释放事务及入格后任务恢复；ground_landing分离连接接纳和高度发布；ground_failure分离重试与停止衔接。保持实时回调顺序和捕获context，只有3C改动，181C/312输入/37保护不变。
原版Tube出口/路点、连接接纳/失败、未改approach/continuation共六组各32768，196608例，改前与两段后通过，重复不累计；ABI范围以各探针字段为准，无超范围控制字声明。
3501帧混合图：四车同一轨迹先后经过桥、正向Tube、反向Tube和返桥。桥头附近仅平移已验189格Tube地形/覆盖并使用普通Map/Move；原桥字节保持。3601帧队列：12请求、3占道车，9辆实际Tube、3辆地面绕行，峰值9辆终点等待；最早请求连续等待1239帧，被8个后到Tube请求超越后1511帧恢复出口、1884帧到达，12辆均最终到达/Guard。
只读观测与正式程序全部生产记录逐模式相同，改前/后8配对28408帧严格、完整每模式轨迹相等。总23配对47473帧，19严格、4既有局部功能差异；349/350、2020/2018、2219/2220、Z436/Z-193与原版失败边界保留。
远距候选未完成路点且未实际入Tube；第一局部地图导出在原版/C加载失败，紧凑LCW版本才通过；0:0校准参数错误也原地保留。queue检查器最初误把全部12请求视为Tube入队，已据原始轨迹分开9入Tube/3绕行；无生产/规则/比较器修改或该修正造成的游戏重跑。见current-explorations.json、queue-observation-review.json；父批探索按prior-explorations.json保留。
基线：{S/'baseline'}；回退：{S/'parts'}；探针：{S/'baseline-probe'}；宿主：{S/'baseline-channel-observer'}；改前新交通：{S/'traffic-baseline-scenes.json'}；封存：{S/'final-source'}。
堆改进、5项社区固定线索及旧负控制按哈希继承。允许有证据的机制改进，不要求逐BUG复刻；此次有限序列恢复不证明持续无限新请求下无饥饿。
清理{clean['deleted_files']}项对象、缓存及重复导出，保留原始输入、正式程序和历史证据。本地提交，不推送。
下一批显式指定父证据movement-state-v65并核对导入；可推进持续到达公平性、混合通道吞吐或有证据的调度/寻路改进。复核：{R/'verify_final_movement_v65.py'}。
''',encoding='utf-8',newline='\n')
lead=f'最新接续：第六十四批正式64 / 验证65已验收。\n交接：{handoff}\n政策：{policy}\n机制改进补充：{addendum}\nEXE：{digest}\n以下历史原地保留。\n\n'.encode('utf-8')
for name in ['交接文档-原版逆向与C重编译-20261020.txt','交接文档-新对话继续推进-20261022.txt']:
 p=P/name;p.write_bytes(lead+p.read_bytes())
p=P/'README.md';ls=p.read_bytes().splitlines(keepends=True);eol=b'\r\n' if ls[0].endswith(b'\r\n') else b'\n'
p.write_bytes('> 当前研究路线（2026-10-25）：原版1.006 C17/x86单位移动第六十四批已验收。隧道出口恢复、桥隧混合通道与较大队列逐车恢复；[第六十四批交接](交接文档-单位移动第六十四批正式验收-20261025.txt)。遵守[整体功能与效果边界](docs/项目目标与验收边界-20261024.txt)和[机制改进补充](docs/寻路机制改进验收补充-20261025.txt)。'.encode('utf-8')+eol+b''.join(ls[1:]))
p=R/'ra2/src/gameplay/阅读说明-单位移动.txt';p.write_bytes(f'第六十四批（2026-10-25）\n隧道出口/连接接纳与失败重试恢复；四车桥隧串行、12请求中9辆实际隧道出口排队及逐车恢复。181C/312输入/37保护，23配对47473帧，原版片段196608例。\n前批有证据的堆容量改进、原版差异/异常、基线和分段回退保留。\n报告：{report}\n\n'.encode('utf-8')+p.read_bytes())
pointer=dict(passed=True,status='promoted',formal_baseline_generation=64,verification_round=65,validation=str(S/'validation.json'),exe_sha256=digest,sha256=digest,executable=str(R/'ra2/build-original-c/ra2.exe'),full_original_equivalence_verified=False,report=str(report),handoff=str(handoff),acceptance_policy=str(policy),pathfinding_policy_addendum=str(addendum),path_mechanism_identity_required=False,globally_shortest_paths_verified=False)
for name in ['latest-recovery.json','latest-state-comparison.json','latest-movement-candidate.json']:
 p=P/'reports'/name;x=read(p);x.update(pointer)
 x['current_batch']=dict(formal_generation=64,verification_round=65,accepted_game_pairs=pairs,accepted_frames=frames,native_cases=196608,native_groups=6,synthetic_cases=0,inherited_heap_improvement=True,new_traffic_recipes=2,production_c_sources=181,content_inputs=312,strict_all_frames_equal=False,accepted_baseline_variations=4,strict_game_pairs=strict,functional_game_pairs=functional)
 p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
write(S/'remaining-work.json',dict(passed=True,bug_for_bug_required=False,path_mechanism_identity_required=False,globally_shortest_paths_verified=False,natural_alias_dispatch_required=False,candidates_not_confirmed_failures=True,community_references_available=True,remaining=['Continuous-arrival bridge/tube traffic and bounded-wait fairness under sustained demand','Measured evidence-supported queue/retry/search improvements when needed','Other engine subsystems and full visual/resource acceptance']))
for e in read(S/'checker-lineage.json')['entries']:assert e['final_derived_sha256']==sha(R/e['derived'])
paths={Path(p).relative_to(R).as_posix() for p in receipt['inputs']}
paths.update(['ra2/CMakeLists.txt','ra2/run_lift.py','ra2/tools/playtest.py','ra2/build-original-c/ra2.exe','ra2/build-original-c/source-content-receipt.json','ra2/src/gameplay/阅读说明-单位移动.txt','build-faithful.ps1','run_fixture_comparison.py','run_state_comparison.py','evidence/movement-state-v4/SOV01T-original.MAP'])
paths.update(p.relative_to(R).as_posix() for p in R.glob('*v65*') if p.is_file())
paths.update(p.relative_to(R).as_posix() for p in S.iterdir() if p.is_file() and p.suffix in ['.c','.h','.asm','.exe','.json'] and p.name not in ['source-manifest.json','document-manifest.json','validation.json','final-check.json'])
paths.update(p.relative_to(R).as_posix() for p in (S/'codec-revisions').iterdir() if p.is_file())
paths.update(p.relative_to(R).as_posix() for p in (S/'fixtures').iterdir() if p.is_file());manifest=[]
for rel in sorted(paths):
 d=S/'final-source'/rel;d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/rel,d);manifest.append(dict(path=rel,sha256=sha(d)))
write(S/'source-manifest.json',manifest)
docs=[P/'README.md',report,handoff,policy,addendum]+[P/n for n in ['交接文档-原版逆向与C重编译-20261020.txt','交接文档-新对话继续推进-20261022.txt']]+[P/'reports'/n for n in ['latest-recovery.json','latest-state-comparison.json','latest-movement-candidate.json']];documents=[]
for p in docs:
 d=S/'current-project'/p.relative_to(P);d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,d);documents.append(dict(path=p.relative_to(P).as_posix(),sha256=sha(d)))
write(S/'document-manifest.json',documents)
write(S/'validation.json',dict(**pointer,parent_commit=parent,state_schema=12,accepted_game_pairs=pairs,accepted_frames=frames,production_c_sources=181,content_inputs=312,unsupported_guards=37,native_cases=196608,probes=3,synthetic_cases=0,inherited_heap_improvement=True,new_traffic_recipes=2,new_traffic_pairs=8,new_traffic_frames=28408,capture_packet_cases_inherited=64,transport_packet_cases_inherited=128,accepted_inherited_variations=4,strict_game_pairs=strict,functional_game_pairs=functional,strict_all_frames_equal=False,source_files=len(manifest),finite_functional_conformance=True,bug_for_bug_required=False,cleanup_performed_this_round=True,pushed=False))
write(S/'final-check.json',dict(passed=True,exe_sha256=digest,source_manifest_sha256=sha(S/'source-manifest.json'),document_manifest_sha256=sha(S/'document-manifest.json'),pushed=False))
print(dict(passed=True,generation=64,exe_sha256=digest,source_files=len(manifest),pairs=pairs,frames=frames,native_cases=196608,new_traffic_recipes=2))
