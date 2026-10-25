"""Promote bridge layers/channel handoff and finite natural traffic evidence."""
from run_batch_v64 import *
if '--freeze-lineage' in sys.argv:
 lineage=read(S/'checker-lineage.json')
 for e in lineage['entries']:
  e['final_derived_sha256']=sha(R/e['derived']);e['unchanged_after_initial_derivation']=e['final_derived_sha256']==e['derived_sha256']
 (S/'checker-lineage.json').write_text(json.dumps(lineage,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print('Current checker lineage frozen before cleanup.');raise SystemExit(0)
for name in ['native-gates.json','effects.json','traffic-effects.json','bridge-channel-effects.json','channel-comparison.json','traffic-event-linkage.json','channel-host-identity.json','current-explorations.json','preservation.json','cleanup.json','final-scene-matrix.json','rng-functional-impact.json','rng-first-split-window.json','boundary-inheritance.json','service-boundaries.json','infrastructure-status.json','baseline-native-identity.json','community-reference-review.json','heap-improvement-inheritance.json','prior-traffic-inheritance.json']:
 assert read(S/name)['passed'],name
receipt=read(R/'ra2/build-original-c/source-content-receipt.json');digest=sha(R/'ra2/build-original-c/ra2.exe')
matrix=read(S/'final-scene-matrix.json');native=read(S/'native-gates.json');clean=read(S/'cleanup.json');traffic=read(S/'traffic-effects.json')
parts=[read(S/'parts'/n/'validation.json') for n in ['bridge','channel']];before=read(S/'traffic-baseline-scenes.json');assert parts[-1]['exe_sha256']==digest
pairs=sum(x['scene_count'] for x in parts)+len(matrix['results'])+len(before['results'])
frames=sum(x['frames'] for x in parts)+sum(x['frames'] for x in matrix['results']+before['results'])
strict=sum(x['scene_count'] for x in parts)+sum(x['strict_trace_equal'] for x in matrix['results']+before['results']);functional=pairs-strict
assert (pairs,frames,strict,functional)==(23,40673,19,4)
assert native['groups']==6 and native['cases']==491520
assert sorted(read(S/n)['cases'] for n in native['receipts'])==[32768,65536,65536,65536,131072,131072]
assert sha(S/'community-reference-review.json')==sha(O/'community-reference-review.json')
parent=read(S/'vcs-context.json')['parent_commit'];report=P/'docs/单位移动第六十三批-桥面层切换与隧道拥堵交通-20261025.txt';handoff=P/'交接文档-单位移动第六十三批正式验收-20261025.txt'
policy=P/'docs/项目目标与验收边界-20261024.txt';addendum=P/'docs/寻路机制改进验收补充-20261025.txt'
lines=[]
for tag,x in traffic['scenes'].items():
 assert x['per_mode_traces_equal_prechange'] and x['strict_trace_equal']
 m=x['modes']['original'];lines.append(f"{tag}：最终目标/Guard、生命、事件、路径均通过；至少两单位同时移动{m['simultaneous_two_or_more_frames']}帧；效果{m['effects']}。")
report.write_text(f'''单位移动第六十三批（正式63 / 验证64），2026-10-25。
父提交：{parent}。
程序：{R/'ra2/build-original-c/ra2.exe'}
SHA-256：{digest}
验收边界：{policy}
机制补充：{addendum}

范围与服务
按整体功能、效果、规则和资源调用验收，不追求逐个BUG复刻，允许有证据支持的机制改进。本批生产仅改ground_bridge_plane.c、ground_segment.c、ground_tube_travel.c；181C/312编译输入/37处未实现保护不变。头文件、构建清单、runtime桥接、生成入口/分发表、生产schema12记录器、通用比较器、规则和资源未改。
第一段bridge：enter_upper_bridge先按无符号32位回绕匹配上下四级高度，再查下一格桥标志并写上层；leave_upper_bridge在可能写回之后重新查询下一格和前一格标志，独立决定离桥，不改成else，不预读缓存。
resolve_segment_surface保留第一候选点、当前格、owner桥层、第二候选点、下一格、再次owner标志的原顺序；不合并两次候选点查询。wait_for_segment_permission按owner许可、目标格、闸门许可、当前朝向、转向的原顺序决定等待；通过后才分类、做列车/碾压门禁。Segment入口捕获context，门禁适配器继续在原时点读取services->context；回调对状态和输出的改写仍可见。
第二段channel：resolve_tube_rise在路由/端点服务之后依次查询入口高度、出口高度、段数，保留32位回绕差、非零段数64位除法和零段数回退；入口distance/select_route/heading/speed/endpoints顺序保持。隧道水平推进、查表与x87精度/舍入/转换控制字原算法不变。本批没有新增算法或容量改变；前批有证据的堆改进及7412预期差异/65541合成见证按哈希继承，不计当前新门禁，不保证全图最短。

原版1.006片段门禁
采用原字节overlap v51的早/晚桥层两组各65536、segment v42路段65536、travel v38入口32768及剩余/普通推进各131072，六组共491520例，改前和两段后均执行，重复不累计。
状态、回调值/顺序、原栈清理以及各探针声明的寄存器、标志、局部量和控制字检查通过，范围以各自字段为准，不泛称全ABI。补足overlap原配方的remaining_return_cases.h及现有gameplay传递依赖；探针C/header保持来源原字节，未修改桩或生产构建。baseline-probe与两段源/程序独立保留。

自然交通与观测
traffic-two-plane：使用前期合法桥下走廊，桥覆盖/地形不变，仅换普通Units/Infantry布置；两辆上层货车、两辆下层货车及两步兵相向往返四轮，共2401帧。直接读取正式记录器已有owner_flags_74_79，原版两上层车各8次0/1切换，下层车始终0；桥上Z416、桥下Z0，有210帧近邻两层同时移动。以单位标志及实际通过为证，不仅依据地图桥标志；不宣称堆叠三层桥面。
traffic-long-block：三辆普通Sleep车辆占住三格桥出口，1200/1300/1400帧分批Move释放，主车在200..1199连续1000帧静止且保留Move目标。阻车首次移动1230/1330/1430，主车1336帧自主恢复，早于1500帧普通同目标再发，随后继续往返、最终到达。总3601帧。此等待期间stage8入口和navigation等待标志均为0：这是静止友军阻塞/相邻格复核下的长期拥堵，不计作TrafficWait mode1/2新增自然覆盖。
traffic-tu：四辆普通货车在既有平层双向十段弯曲Tubes内分批出发、反向和往返，共2401帧。生产路径自然出现方向8；独立只读观测记录route/waypoint、段数、入口/出口和approach，要求每车两路由、至少六种中间路点，实际通过而非普通地面绕行。没有动态构造出口车、原始运动/路径/预算注入或新增生产钩子。
{chr(10).join(lines)}
新channel-observer只在既有隔离记录器快照后读取Tube字段，与当前正式对象链接；不调用新游戏函数、不改原生入口或路径。改前/最终各一次，逐模式剔除新增fixture记录后的全部生产观测完全相等；其自身原版/C严格比较及冻结改前轨迹也通过。原bridge-catalog观测宿主继续用于既有装卸回归，与新只读观测分开。
三个配方改前/后各3组生产与1组独立观测，共8配对21608帧严格；完整每模式轨迹等于冻结基线。全程生命、命令提交/执行、路径缓冲、已有stage6、最终目标与Guard通过。旧坡道/道路交通按哈希继承，不重计当前执行。

探索、启动问题与原版异常
首次较长标签Tubes候选中，原版跑完2401帧但4→6层cardinal路线停滞，三次C/观测启动在加载ra2.csf前失败，不能归为移动首差。资源MIX哈希与成功场景相同；游戏根路径ANSI长度128的原版运行成功，131/137/140的三个启动失败。
保留上述地图、原版轨迹、全部false比较及命令。使用同资源/地图/seed和短标签、仅保留<=600帧订单，补跑601帧原版/C严格对照，原版前601帧与长标签逐状态相等，双方重现停滞；这支持路径长度相关的启动问题判断，尚未定位原版具体缓冲区。一次缩短范围但未同步移除后续订单的启动参数校验错误也原地保留，未进入模拟。短标签配方完成游戏启动；生产、资源与通用比较器未为此修改。
失败候选和601帧异常对照不计成功自然交通，见current-explorations.json；后续改用已验平层弯曲Tubes并验证实际路点。既有Z436停滞、Z-193未完成、岸边/碰撞负控制等异常和边界继续保留，不要求逐BUG复刻。

回归、社区与保护
两段各默认301、北桥501、南桥501帧，共6配对2606帧严格。最终mi/sc/aw3/fm装卸/岸边完整每模式轨迹等于父批；4项既有严格false、349/350随机首差窗口、原版/C货车2020/2018和步兵2219/2220时序保留。列车碰撞、碾压、重复失败及弯曲高差原版异常回归通过。29非主C入口/86原始入边、旧岸边和坡型/飞机边界按哈希继承，无新增自然别名入口结论。
当前成功验收{pairs}配对{frames}模拟帧，{strict}严格、{functional}既有局部功能差异；另有601帧严格异常对照单列。seed12345、模拟帧发令，构建串行、最多两条配对/四个游戏进程。
继续参考父批5项固定提交/内容哈希：gagarin YR1.001结构与桥层调用、EA旧Red Alert通行/结果组织、Phobos扩展定位。仅作定位和组织线索，不移植版本地址/规则或第三方引擎实现，不上传私有工程；原版1.006为依据，见community-reference-review.json。
父批{len(read(O/'source-manifest.json'))}项封存、315项独立基线、两段回退、改前探针/两个观测宿主和三种新交通基线保留。H盘20项原始输入、原版game.exe/SAVE0029、原rules和旧手写引擎、Git配置/远端引用不变。
按路径/类型/哈希和重解析点检查清理{clean['deleted_files']}项对象、缓存与重复导出，共{clean['deleted_bytes']}字节，{clean['protected_files']}项保护文件不变；独立保留初始lineage后删除重复导出。正式程序、源、资源、轨迹、基线、回退、失败与原版异常保留。本地提交，不推送。
复核：{R/'verify_final_movement_v64.py'}；本地提交收据：{S/'postcommit/git-local-commit.json'}。
后续按功能需要扩展桥/隧道混合交通、更大队列/饥饿恢复或有度量的搜索改进；当前不是全游戏、完整资源视觉或全图最优路径验收。
''',encoding='utf-8',newline='\n')
handoff.write_text(f'''当前正式63 / 验证64，2026-10-25。
父提交：{parent}；程序SHA-256：{digest}。
报告：{report}
政策：{policy}
机制补充：{addendum}

ground_bridge_plane整理独立入桥/离桥服务，保持写回后重读标志；ground_segment分开桥层/候选解析与闸门/朝向等待，保持捕获context和重复查询；ground_tube_travel分离路由后的两端高度/段数衔接。只改3C，181C/312输入/37保护不变，无新算法/规则/资源或生产记录器改动。
原版早/晚桥层各65536、路段65536、Tube入口32768、剩余/普通推进各131072，共491520例，改前和两段后通过；六组重复不累计，ABI/控制字范围以各探针字段为准。
新自然交通：2401帧双层桥面（上车各8次层切换、下车保持下层、210帧两层近邻并行）；3601帧长拥堵（1000帧静止保留Move，1336帧自主恢复，早于1500再发令）；2401帧四车双向弯曲Tubes（方向8和实际路由/路点进展）。只读channel-observer逐模式与正式程序完整生产观测相等；不把长期静止阻塞计为stage8等待模式入口，也不宣称三层堆叠桥。
总23配对40673帧，19严格、4既有局部功能差异；新三配方及Tube独立观测改前/后8配对21608帧严格，完整每模式轨迹相等。既有349/350、2020/2018、2219/2220、Z436/Z-193和旧失败边界保留。
较长路径标签下3次ra2.csf启动失败与一份原版4→6层cardinal停滞轨迹原地保留；短标签同地图601帧原版/C严格重现停滞，原版前缀相等，单列不计成功自然交通。原因支持路径长度相关，未定位具体原版缓冲区；另保留一次范围/订单参数校验错误。见current-explorations.json。
基线：{S/'baseline'}；回退：{S/'parts'}；探针：{S/'baseline-probe'}；旧宿主：{S/'baseline-observer'}；新宿主：{S/'baseline-channel-observer'}；新场景改前：{S/'traffic-baseline-scenes.json'}；封存：{S/'final-source'}。
前批堆改进和5项固定社区线索按哈希继承；原版1.006为准，允许有证据的机制改进，不保证全图最短。
已核对清理{clean['deleted_files']}项对象、缓存及重复导出；保护原始输入、正式程序和全部历史证据。本地提交，不推送。
下一步按功能需要推进混合桥/隧道、更大队列与饥饿恢复、或有证据的搜索改进；全游戏/完整资源视觉未验收。
下一批显式指定父证据movement-state-v64并核对导入。复核：{R/'verify_final_movement_v64.py'}。
''',encoding='utf-8',newline='\n')
lead=f'最新接续：第六十三批正式63 / 验证64已验收。\n交接：{handoff}\n政策：{policy}\n机制改进补充：{addendum}\nEXE：{digest}\n以下历史原地保留。\n\n'.encode('utf-8')
for name in ['交接文档-原版逆向与C重编译-20261020.txt','交接文档-新对话继续推进-20261022.txt']:
 p=P/name;p.write_bytes(lead+p.read_bytes())
p=P/'README.md';ls=p.read_bytes().splitlines(keepends=True);eol=b'\r\n' if ls[0].endswith(b'\r\n') else b'\n'
p.write_bytes('> 当前研究路线（2026-10-25）：原版1.006 C17/x86单位移动第六十三批已验收。桥面层切换、通道衔接与双层桥面/隧道拥堵交通；[第六十三批交接](交接文档-单位移动第六十三批正式验收-20261025.txt)。遵守[整体功能与效果边界](docs/项目目标与验收边界-20261024.txt)和[机制改进补充](docs/寻路机制改进验收补充-20261025.txt)。'.encode('utf-8')+eol+b''.join(ls[1:]))
p=R/'ra2/src/gameplay/阅读说明-单位移动.txt';p.write_bytes(f'第六十三批（2026-10-25）\n桥面层切换/路段及隧道入口衔接；双层桥面、双向隧道与1000帧拥堵自动恢复交通。181C/312输入/37保护，23配对40673帧，原版片段491520例。\n前批有证据的堆容量改进、原版差异/异常、基线和分段回退保留。\n报告：{report}\n\n'.encode('utf-8')+p.read_bytes())
pointer=dict(passed=True,status='promoted',formal_baseline_generation=63,verification_round=64,validation=str(S/'validation.json'),exe_sha256=digest,sha256=digest,executable=str(R/'ra2/build-original-c/ra2.exe'),full_original_equivalence_verified=False,report=str(report),handoff=str(handoff),acceptance_policy=str(policy),pathfinding_policy_addendum=str(addendum),path_mechanism_identity_required=False,globally_shortest_paths_verified=False)
for name in ['latest-recovery.json','latest-state-comparison.json','latest-movement-candidate.json']:
 p=P/'reports'/name;x=read(p);x.update(pointer)
 x['current_batch']=dict(formal_generation=63,verification_round=64,accepted_game_pairs=pairs,accepted_frames=frames,native_cases=491520,native_groups=6,synthetic_cases=0,inherited_heap_improvement=True,new_traffic_recipes=3,production_c_sources=181,content_inputs=312,strict_all_frames_equal=False,accepted_baseline_variations=4,strict_game_pairs=strict,functional_game_pairs=functional)
 p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
write(S/'remaining-work.json',dict(passed=True,bug_for_bug_required=False,path_mechanism_identity_required=False,globally_shortest_paths_verified=False,natural_alias_dispatch_required=False,candidates_not_confirmed_failures=True,community_references_available=True,remaining=['Further multi-unit bridge/tube interaction and starvation/long-queue recovery as functionally needed','Long congestion recovery and measured evidence-supported search improvements','Other engine subsystems and full visual/resource acceptance']))
for e in read(S/'checker-lineage.json')['entries']:assert e['final_derived_sha256']==sha(R/e['derived'])
paths={Path(p).relative_to(R).as_posix() for p in receipt['inputs']}
paths.update(['ra2/CMakeLists.txt','ra2/run_lift.py','ra2/tools/playtest.py','ra2/build-original-c/ra2.exe','ra2/build-original-c/source-content-receipt.json','ra2/src/gameplay/阅读说明-单位移动.txt','build-faithful.ps1','run_fixture_comparison.py','run_state_comparison.py','evidence/movement-state-v4/SOV01T-original.MAP'])
paths.update(p.relative_to(R).as_posix() for p in R.glob('*v64*') if p.is_file())
paths.update(p.relative_to(R).as_posix() for p in S.iterdir() if p.is_file() and p.suffix in ['.c','.h','.asm','.exe','.json'] and p.name not in ['source-manifest.json','document-manifest.json','validation.json','final-check.json'])
paths.update(p.relative_to(R).as_posix() for p in (S/'fixtures').iterdir() if p.is_file());manifest=[]
for rel in sorted(paths):
 d=S/'final-source'/rel;d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/rel,d);manifest.append(dict(path=rel,sha256=sha(d)))
write(S/'source-manifest.json',manifest)
docs=[P/'README.md',report,handoff,policy,addendum]+[P/n for n in ['交接文档-原版逆向与C重编译-20261020.txt','交接文档-新对话继续推进-20261022.txt']]+[P/'reports'/n for n in ['latest-recovery.json','latest-state-comparison.json','latest-movement-candidate.json']];documents=[]
for p in docs:
 d=S/'current-project'/p.relative_to(P);d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,d);documents.append(dict(path=p.relative_to(P).as_posix(),sha256=sha(d)))
write(S/'document-manifest.json',documents)
write(S/'validation.json',dict(**pointer,parent_commit=parent,state_schema=12,accepted_game_pairs=pairs,accepted_frames=frames,production_c_sources=181,content_inputs=312,unsupported_guards=37,native_cases=491520,probes=3,synthetic_cases=0,inherited_heap_improvement=True,new_traffic_recipes=3,new_traffic_pairs=8,new_traffic_frames=21608,capture_packet_cases_inherited=64,transport_packet_cases_inherited=128,accepted_inherited_variations=4,strict_game_pairs=strict,functional_game_pairs=functional,strict_all_frames_equal=False,source_files=len(manifest),finite_functional_conformance=True,bug_for_bug_required=False,cleanup_performed_this_round=True,pushed=False))
write(S/'final-check.json',dict(passed=True,exe_sha256=digest,source_manifest_sha256=sha(S/'source-manifest.json'),document_manifest_sha256=sha(S/'document-manifest.json'),pushed=False))
print(dict(passed=True,generation=63,exe_sha256=digest,source_files=len(manifest),pairs=pairs,frames=frames,native_cases=491520,new_traffic_recipes=3))
