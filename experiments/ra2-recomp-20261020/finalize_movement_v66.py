"""Promote finite sustained-arrival fairness measurements and recovery scheduling services."""
from run_batch_v66 import *
if '--freeze-lineage' in sys.argv:
 lineage=read(S/'checker-lineage.json')
 for e in lineage['entries']:
  e['final_derived_sha256']=sha(R/e['derived']);e['unchanged_after_initial_derivation']=e['final_derived_sha256']==e['derived_sha256']
 (S/'checker-lineage.json').write_text(json.dumps(lineage,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print('Current checker lineage frozen before cleanup.');raise SystemExit(0)
required=['native-gates.json','effects.json','traffic-effects.json','fairness-effects.json','mixed-recovery-effects.json','queue-recovery-effects.json','bridge-channel-effects.json','channel-comparison.json','traffic-event-linkage.json','channel-host-identity.json','current-explorations.json','preservation.json','cleanup.json','final-scene-matrix.json','rng-functional-impact.json','rng-first-split-window.json','boundary-inheritance.json','service-boundaries.json','infrastructure-status.json','baseline-native-identity.json','community-reference-review.json','community-current-use.json','phase-overlap-review.json','heap-improvement-inheritance.json','prior-traffic-inheritance.json','prior-explorations.json','traffic-map-provenance.json','traffic-goal-terrain-validation.json','mixed-target-terrain-review.json','channel-observer-baseline-parity.json']
for name in required:assert read(S/name)['passed'],name
receipt=read(R/'ra2/build-original-c/source-content-receipt.json');digest=sha(R/'ra2/build-original-c/ra2.exe')
matrix=read(S/'final-scene-matrix.json');native=read(S/'native-gates.json');clean=read(S/'cleanup.json')
parts=[read(S/'parts'/n/'validation.json') for n in ['scheduling','publication']];before=read(S/'traffic-baseline-scenes.json');assert parts[-1]['exe_sha256']==digest
pairs=sum(x['scene_count'] for x in parts)+len(matrix['results'])+len(before['results'])
frames=sum(x['frames'] for x in parts)+sum(x['frames'] for x in matrix['results']+before['results'])
strict=sum(x['scene_count'] for x in parts)+sum(x['strict_trace_equal'] for x in matrix['results']+before['results']);functional=pairs-strict
assert (pairs,frames,strict,functional)==(23,78273,19,4)
assert native['groups']==5 and native['cases']==360448
assert sorted(read(S/n)['unique_cases'] for n in native['receipts'])==[32768,65536,65536,65536,131072]
parent=read(S/'vcs-context.json')['parent_commit'];report=P/'docs/单位移动第六十五批-持续来车公平性与桥隧恢复调度-20261025.txt';handoff=P/'交接文档-单位移动第六十五批正式验收-20261025.txt'
policy=P/'docs/项目目标与验收边界-20261024.txt';addendum=P/'docs/寻路机制改进验收补充-20261025.txt'
recipes=read(S/'traffic-fixtures.json')['fixtures'];measurements=[]
mixed_count=len(next(x['actor_ids'] for x in recipes if x['kind']=='mixed'));queue_tag=next(x['tag'] for x in recipes if x['kind']=='queue');mixed_tag=next(x['tag'] for x in recipes if x['kind']=='mixed');mixed_period=next(x['arrival_period'] for x in recipes if x['kind']=='mixed');mixed_end=next(x['arrival_end'] for x in recipes if x['kind']=='mixed');calibrations=len(read(S/'actor-catalog-validation.json')['catalogs'])
for item in recipes:
 effect=read(S/'fairness-effects.json')['scenes'][item['observer_tag']]['original']['effects'];old=effect['per_vehicle'][str(effect['oldest_request_id'])]
 measurements.append(dict(tag=item['tag'],kind=item['kind'],frames=item['last']+1,request_vehicles=len(item['actor_ids']),blockers=len(item['blocker_ids']),arrival_window=effect['arrival_window'],release_window=effect['blocker_release_window'],actual_tube_actors=effect['actual_tube_actors'],ground_bypass_actors=effect['ground_bypass_actors'],peak_waiters=effect['peak_terminal_waiters'],exits_during_arrivals=effect['tube_exits_during_arrivals'],oldest_id=effect['oldest_request_id'],oldest=old,oldest_exit_during_arrivals=effect['oldest_exit_during_arrivals'],maximum_request_to_exit=effect['maximum_request_to_exit'],maximum_terminal_wait=effect['maximum_terminal_wait'],exit_order_inversions=effect['request_exit_order_inversions'],last_goal_arrival=effect['last_goal_arrival'],post_release_exits_per_1000_frames=effect['post_release_tube_exits_per_1000_frames']))
summary=json.dumps(measurements,ensure_ascii=False,indent=2)
report.write_text(f'''单位移动第六十五批（正式65 / 验证66），2026-10-25。
父提交：{parent}。
程序：{R/'ra2/build-original-c/ra2.exe'}
SHA-256：{digest}
验收边界：{policy}
机制补充：{addendum}

范围与调度服务
继续按整体功能、效果、规则和资源调用验收，不追求逐个BUG复刻，允许有证据支持的机制改进。生产仅改ground_wait.c、ground_prepare_cycle.c、ground_prepare_exit.c；181C/312编译输入/37处未实现保护不变。头文件、构建清单、runtime桥接、生成入口/分发表、生产schema12记录器、通用比较器、规则与资源均未改。
第一段scheduling：traffic_rebuild_mode将短重试节流与长等待升级组成明确的调度选择。首次阻塞仍只启动一次等待，start_wait后不覆盖回调可改写的waiting/计时字段；当前帧查询后先判短计时器，未到期报告障碍；到期再按原有长计时器选择mode1或2。有符号回绕规则不变，不因后来车辆刷新既有车辆的等待起点。
schedule_empty_queue_retry仅在准备入口返回RETRY_PATH后读取当前对象重试计时器，再查询帧并进入原重试服务。原入口的已有路径、对象/任务短路和回调后的实时context保持；不提前读取或缓存services->prepare。
第二段publication：accept_rebuild_for_retry保留捕获context及重建后的owner/目的地接纳、取消/终止检查；timer_only跳过结果检查。publish_retry_deadline依次读取当前帧、换算延迟、重启计时器，保留延迟回调的控制字与对象副作用。每辆车独立节流和到期重试；本批没有新增全局FIFO、优先队列、路径算法、对象字段或内存预算。
前批有证据的堆容量改进及7412预期差异/65541合成见证按哈希继承，不计本批新门禁；不保证全图最短。

原版1.006片段门禁
wait v63原字节探针：clearance、clearance-tail、traffic-schedule各65536；prepare v62探针入口与重试各65536，合为一份131072收据；tube-state v51原字节出口32768。共三份探针源码、五组执行收据、六段片段门禁、360448唯一例，改前与两段后通过，重复不累计。clearance两组和Tube出口为未改动的相邻服务回归，不能虚称新增实现。
状态、回调参数/顺序、返回、探针声明的ABI与控制字字段通过；Tube出口探针的ABI范围仍按其自身字段，不把所有五组统一称为完整ABI或控制字证明。三份原字节源码与各自构建输入、改前可执行文件及两段回退独立保留。

持续到达与混合通道自然场景
{queue_tag}：24辆请求车及3辆普通Sleep出口占道车。最高actor ID最先在第5帧请求，其余车辆从100帧起每180帧请求，持续至4060；占道车辆2200/2300/2400帧普通Move分批释放。每车仅一份出口请求，未重发目标强迫恢复。
{mixed_tag}：{mixed_count}辆车在同一图中分批先过原桥、到达西侧普通路点，再从800帧起每{mixed_period}帧请求通过附近同一条弯曲Tube，持续至{mixed_end}；3辆普通Sleep出口占道车2600/2700/2800帧分批Move释放。每个实际Tube参与者均有同一轨迹中更早的桥层见证。桥面/接近路点是预先固定的行程命令，队列中的出口请求没有被重发替换。
两张输入仅替换父批已验地图的Units/Infantry段，其余字节保持，尤其原桥、局部189格合法Tube地形、紧凑LCW覆盖与Tubes记录不改。{calibrations}次成功的0:1两帧actor校准仅用于绑定实际编号，单列，不计自然交通帧。
24车运行7601帧，{mixed_count}车混合运行7201帧；正式程序和独立只读观测各在改前与最终执行一组，共8配对59208帧严格。保留每车请求、实际Tube或合法地面绕行分类、终点连续等待、出口发布、目标到达、被后来请求超越次数；另存100帧积压/最老等待年龄采样及500帧吞吐窗口。吞吐率明确使用“释放开始至观测结束”的固定窗口，包含尾部空闲，不冒充通道饱和容量。
实测汇总（原版/C一致）：
{summary}
完整逐车和分窗数据：{S/'fairness-effects.json'}。
已验证本次有限持续到达窗口中，新请求仍到达时通道能够服务，并且所有请求最终恢复。先进先出、任意队长、无限持续新请求下的无饥饿与有界等待均未证明；最早请求是否在来车结束前出隧道已单列，不能用其他车辆吞吐替代它。此次整理保留原调度机制，未将原版放行先后顺序静默替换为FIFO。

观测、回归与差异
复用父批只读桥层/Tube字段，不新增游戏函数调用或原生钩子。观测剔除fixture行后的所有生产记录逐模式与正式程序完全相等，全部当前完整每模式轨迹等于改前冻结数据；原版/C严格比较和负控制保持，未放宽通用比较器。
两段各默认301、北桥501、南桥501帧，共6配对2606帧严格。最终mi/sc/aw3/fm与父批完整逐模式轨迹相等，4项既有严格false、349/350随机首差窗口、原版/C货车2020/2018与步兵2219/2220时序保留。列车碰撞、碾压、重复失败及Z436/Z-193原版高差异常回归通过。
成功验收总{pairs}配对{frames}模拟帧，{strict}严格、{functional}既有局部功能差异。seed12345、模拟帧发令，构建串行，最多两条配对/四个游戏进程。不宣称全游戏、完整视觉资源或无限负载等价。
父批远距未完成行程、literal LCW加载失败、0:0校准错误、队列检查器9Tube/3绕行纠正及更早异常，全部按prior-explorations.json继承；没有重新归为本批成功覆盖。当前首个24车偏轴目标候选只有2辆实际入Tube、最早请求绕行。三个早期16车混合候选含岩石/水域目标，部分车辆未到达；原版/改前C原始轨迹均严格，但不计成功交通。早期曾把“前6辆通过、后续未完成”解读为负载边界，现已依据原版地形catalog撤回，不能据此声称通道容量或饥饿故障；见mixed-target-terrain-review.json。最终输入仅把全部普通中间/终点改为原版已核对的合法地面格，使用{mixed_period}帧间隔至{mixed_end}帧；所有旧地图、命令和完整轨迹保留。合法目标的16车版本仍有1辆在原版/改前C均停于初格62,54，原因未确认，不归因队列饥饿；该完整输入保留。正式混合配方删除这一初始对象，以{mixed_count}辆已观察到能移动的车重新执行，3辆占道车仍在；没有向队列请求车辆重发恢复命令。一次校准误携带超出0:1范围的命令，被两种模式在模拟前拒绝，改用清空命令的新tag成功，旧收据保留。见current-explorations.json、traffic-exclusions.json及traffic-goal-terrain-validation.json。

构建调度异常
第二段曾在第一段南桥场景退出前启动，链接因ra2.exe被占用失败，程序字节未被替换；第一段快照因此错收第三处未来源码。无效快照原字节留在parts/scheduling-overlap-invalid，按其存档构建收据与独立基线恢复唯一错配源码，核对全部312项输入及已执行程序/探针/轨迹身份后重建正式scheduling回退；没有重分类或重跑、没有增加验收计数。之后串行完成第二段，工具增加前段回退及编译输入检查。见phase-overlap-review.json。

社区线索、保护与收尾
已核对5项社区固定版本/内容哈希保持，其中gagarin FindPath包装与EA FINDPATH.CPP两份公开源码本批重新下载到内存核对，内容与锁定哈希相同，未写缓存。用其请求/检查/发布分层组织线索，不移植YR/旧RA地址、阈值或FIFO假设，不引入第三方引擎、不上传私有工程。原版1.006原字节与自然运行是本批对照依据。
29非主C入口/86原始入边、旧岸边/坡型/飞机及其他边界按哈希继承，无新自然别名入口结论。父批461项封存、315项独立基线、两段回退、改前探针/宿主及新交通基线保留。H盘20项原始输入、原版game.exe/SAVE0029、原rules和旧手写引擎、Git配置/远端引用保持不变。
按路径、类型、哈希与重解析点清理{clean['deleted_files']}项可再生成对象/缓存及重复导出，共{clean['deleted_bytes']}字节，{clean['protected_files']}项保护文件不变。正式程序、源、资源、基线、回退、轨迹及原版异常保留。本地提交，不推送。
复核：{R/'verify_final_movement_v66.py'}；本地提交收据：{S/'postcommit/git-local-commit.json'}。
下一步可研究不同负载/反向需求下的公平性界限与有测量依据的优先级或退避改进；本批不以追逐任意内部差异扩大验收范围。
''',encoding='utf-8',newline='\n')
handoff.write_text(f'''当前正式65 / 验证66，2026-10-25。
父提交：{parent}；程序SHA-256：{digest}。
报告：{report}
政策：{policy}
机制补充：{addendum}

生产仅改ground_wait、ground_prepare_cycle、ground_prepare_exit三处，整理短重试/长等待升级、队列耗尽后调度和重建后期限发布；保持原计时、实时context/回调顺序、owner/目的地接纳和控制字副作用。无新FIFO或路径机制。181C/312输入/37保护不变。
原版片段五份执行收据、六段共360448唯一例通过，改前与两段后重复不累计；当前ABI/控制字范围以每份探针字段为准。
24辆持续出口请求与3辆占道车运行7601帧；{mixed_count}辆先桥后Tube混合请求与3辆占道车运行7201帧。普通Move分批释放，队列请求未重发；新来车结束前的吞吐和最终逐车恢复分开计量。正式/观测改前及最终共8配对59208帧严格，总23配对78273帧，19严格、4既有功能差异。完整实测：{S/'fairness-effects.json'}。
{summary}
所有请求最终到达；有限持续来车窗口有实际出口吞吐。未证明无限持续到达下无饥饿、FIFO或任意负载有界等待，不将总吞吐当作最早请求恢复。
一次构建与前段场景重叠导致链接失败和源码快照错配；无效快照保留，按存档收据和独立基线重建正确回退并核对312输入，未增加测试计数。见phase-overlap-review.json。
旧349/350、2020/2018、2219/2220、Z436/Z-193以及失败候选/原版异常原地保留。两张新图只改Units/Infantry，原桥/Tube/覆盖保持。5项社区固定线索继承，2份公开源码重新核对哈希；无第三方引擎或私有上传。
基线：{S/'baseline'}；回退：{S/'parts'}（仅scheduling/publication，scheduling-overlap-invalid不用于回退）；探针：{S/'baseline-probe'}；宿主：{S/'baseline-channel-observer'}；新交通改前：{S/'traffic-baseline-scenes.json'}；封存：{S/'final-source'}。
清理{clean['deleted_files']}项无用产物，保护文件保持；本地提交，不推送。
下一批显式指定父证据movement-state-v66，可推进反向持续需求/不同负载的公平性界限或有证据的优先级/退避改进。复核：{R/'verify_final_movement_v66.py'}。
''',encoding='utf-8',newline='\n')
lead=f'最新接续：第六十五批正式65 / 验证66已验收。\n交接：{handoff}\n政策：{policy}\n机制改进补充：{addendum}\nEXE：{digest}\n以下历史原地保留。\n\n'.encode('utf-8')
for name in ['交接文档-原版逆向与C重编译-20261020.txt','交接文档-新对话继续推进-20261022.txt']:
 p=P/name;p.write_bytes(lead+p.read_bytes())
p=P/'README.md';ls=p.read_bytes().splitlines(keepends=True);eol=b'\r\n' if ls[0].endswith(b'\r\n') else b'\n'
p.write_bytes('> 当前研究路线（2026-10-25）：原版1.006 C17/x86单位移动第六十五批已验收。持续来车下的恢复调度、桥隧拥堵逐车公平性与吞吐；[第六十五批交接](交接文档-单位移动第六十五批正式验收-20261025.txt)。遵守[整体功能与效果边界](docs/项目目标与验收边界-20261024.txt)和[机制改进补充](docs/寻路机制改进验收补充-20261025.txt)。'.encode('utf-8')+eol+b''.join(ls[1:]))
p=R/'ra2/src/gameplay/阅读说明-单位移动.txt';p.write_bytes(f'第六十五批（2026-10-25）\n短重试/长等待升级、队列耗尽恢复调度和重建期限发布；24辆持续到达及{mixed_count}辆桥隧混合请求逐车恢复/吞吐。181C/312输入/37保护，23配对78273帧，原版片段360448例。\n有限来车恢复不证明无限负载无饥饿；基线/回退/原版差异与异常保留。\n报告：{report}\n\n'.encode('utf-8')+p.read_bytes())
pointer=dict(passed=True,status='promoted',formal_baseline_generation=65,verification_round=66,validation=str(S/'validation.json'),exe_sha256=digest,sha256=digest,executable=str(R/'ra2/build-original-c/ra2.exe'),full_original_equivalence_verified=False,report=str(report),handoff=str(handoff),acceptance_policy=str(policy),pathfinding_policy_addendum=str(addendum),path_mechanism_identity_required=False,globally_shortest_paths_verified=False)
for name in ['latest-recovery.json','latest-state-comparison.json','latest-movement-candidate.json']:
 p=P/'reports'/name;x=read(p);x.update(pointer);x['current_batch']=dict(formal_generation=65,verification_round=66,accepted_game_pairs=pairs,accepted_frames=frames,native_cases=360448,native_groups=5,synthetic_cases=0,inherited_heap_improvement=True,new_traffic_recipes=2,production_c_sources=181,content_inputs=312,strict_all_frames_equal=False,accepted_baseline_variations=4,strict_game_pairs=strict,functional_game_pairs=functional,fifo_guarantee=False,unbounded_starvation_freedom_proved=False)
 p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
write(S/'remaining-work.json',dict(passed=True,bug_for_bug_required=False,path_mechanism_identity_required=False,globally_shortest_paths_verified=False,natural_alias_dispatch_required=False,community_references_available=True,remaining=['Reverse and competing sustained demand with measured fairness boundaries','Optional investigation of the retained stationary original start at62,54; bug reproduction is not required','Evidence-supported queue priority or backoff changes when needed','Other engine subsystems and full visual/resource acceptance']))
for e in read(S/'checker-lineage.json')['entries']:assert e['final_derived_sha256']==sha(R/e['derived'])
paths={Path(p).relative_to(R).as_posix() for p in receipt['inputs']}
paths.update(['ra2/CMakeLists.txt','ra2/run_lift.py','ra2/tools/playtest.py','ra2/build-original-c/ra2.exe','ra2/build-original-c/source-content-receipt.json','ra2/src/gameplay/阅读说明-单位移动.txt','build-faithful.ps1','run_fixture_comparison.py','run_state_comparison.py','evidence/movement-state-v4/SOV01T-original.MAP'])
paths.update(p.relative_to(R).as_posix() for p in R.glob('*v66*') if p.is_file())
paths.update(p.relative_to(R).as_posix() for p in S.iterdir() if p.is_file() and p.suffix in ['.c','.h','.asm','.exe','.json'] and p.name not in ['source-manifest.json','document-manifest.json','validation.json','final-check.json'])
paths.update(p.relative_to(R).as_posix() for p in (S/'fixtures').iterdir() if p.is_file());manifest=[]
for rel in sorted(paths):
 d=S/'final-source'/rel;d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/rel,d);manifest.append(dict(path=rel,sha256=sha(d)))
write(S/'source-manifest.json',manifest)
docs=[P/'README.md',report,handoff,policy,addendum]+[P/n for n in ['交接文档-原版逆向与C重编译-20261020.txt','交接文档-新对话继续推进-20261022.txt']]+[P/'reports'/n for n in ['latest-recovery.json','latest-state-comparison.json','latest-movement-candidate.json']];documents=[]
for p in docs:
 d=S/'current-project'/p.relative_to(P);d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,d);documents.append(dict(path=p.relative_to(P).as_posix(),sha256=sha(d)))
write(S/'document-manifest.json',documents)
write(S/'validation.json',dict(**pointer,parent_commit=parent,state_schema=12,accepted_game_pairs=pairs,accepted_frames=frames,production_c_sources=181,content_inputs=312,unsupported_guards=37,native_cases=360448,probes=3,synthetic_cases=0,inherited_heap_improvement=True,new_traffic_recipes=2,new_traffic_pairs=8,new_traffic_frames=59208,capture_packet_cases_inherited=64,transport_packet_cases_inherited=128,accepted_inherited_variations=4,strict_game_pairs=strict,functional_game_pairs=functional,strict_all_frames_equal=False,source_files=len(manifest),finite_functional_conformance=True,bug_for_bug_required=False,cleanup_performed_this_round=True,rollback_parts=['scheduling','publication'],excluded_rollback_dirs=['scheduling-overlap-invalid'],fifo_guarantee=False,unbounded_starvation_freedom_proved=False,pushed=False))
write(S/'final-check.json',dict(passed=True,exe_sha256=digest,source_manifest_sha256=sha(S/'source-manifest.json'),document_manifest_sha256=sha(S/'document-manifest.json'),pushed=False))
print(dict(passed=True,generation=65,exe_sha256=digest,source_files=len(manifest),pairs=pairs,frames=frames,native_cases=360448,new_traffic_recipes=2))
