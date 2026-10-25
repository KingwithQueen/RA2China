"""Promote completion/reconstruction services and two ordinary traffic recipes."""
from run_batch_v60 import *
if '--freeze-lineage' in sys.argv:
 lineage=read(S/'checker-lineage.json')
 for e in lineage['entries']:
  e['final_derived_sha256']=sha(R/e['derived']);e['unchanged_after_initial_derivation']=e['final_derived_sha256']==e['derived_sha256']
 (S/'checker-lineage.json').write_text(json.dumps(lineage,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print('Current checker lineage frozen before cleanup.');raise SystemExit(0)
for name in ['native-gates.json','effects.json','traffic-effects.json','traffic-reissue-motion.json','preservation.json','cleanup.json','final-scene-matrix.json','rng-functional-impact.json','rng-first-split-window.json','boundary-inheritance.json','service-boundaries.json','infrastructure-status.json','baseline-native-identity.json','community-reference-review.json','heap-improvement-inheritance.json','environment-note.json']:
 assert read(S/name)['passed'],name
receipt=read(R/'ra2/build-original-c/source-content-receipt.json');digest=sha(R/'ra2/build-original-c/ra2.exe')
matrix=read(S/'final-scene-matrix.json');native=read(S/'native-gates.json');clean=read(S/'cleanup.json');traffic=read(S/'traffic-effects.json')
parts=[read(S/'parts'/n/'validation.json') for n in ['completion','rebuild']];before=read(S/'traffic-baseline-scenes.json');assert parts[-1]['exe_sha256']==digest
pairs=sum(x['scene_count'] for x in parts)+len(matrix['results'])+len(before['results'])
frames=sum(x['frames'] for x in parts)+sum(x['frames'] for x in matrix['results']+before['results'])
strict=sum(x['scene_count'] for x in parts)+sum(x['strict_trace_equal'] for x in matrix['results']+before['results']);functional=pairs-strict
assert (pairs,frames,strict,functional)==(19,22669,15,4)
assert native['groups']==2 and native['cases']==24576
c=read(S/'part-rebuild-completion.json');r=read(S/'part-rebuild-rebuild.json');assert (c['cases'],r['cases'])==(8192,16384)
refs=read(S/'community-reference-review.json');assert len(refs['sources'])==5 and sha(S/'community-reference-review.json')==sha(O/'community-reference-review.json')
parent=read(S/'vcs-context.json')['parent_commit'];report=P/'docs/单位移动第五十九批-路径完成重建与自然交通-20261025.txt';handoff=P/'交接文档-单位移动第五十九批正式验收-20261025.txt'
policy=P/'docs/项目目标与验收边界-20261024.txt';addendum=P/'docs/寻路机制改进验收补充-20261025.txt'
traffic_lines=[]
for tag,x in traffic['scenes'].items():
 assert x['per_mode_traces_equal_prechange'] and x['strict_trace_equal']
 m=x['modes']['original'];moving=sum(q['was_moving'] and q['old_goal_unfinished'] for q in m['moving_reissues'])
 traffic_lines.append(f"{tag}：至少三单位同时移动{m['simultaneous_three_or_more_frames']}帧、两单位同时移动且平面最大轴差不超过3格{m['nearby_simultaneous_motion_frames']}帧；{moving}次改发前仍在移动且旧目标未完成。所有最终目标/Guard、生命和合法落格通过；程序每模式完整轨迹等于本轮改动前基线。")
report.write_text(f'''单位移动第五十九批（正式59 / 验证60），2026-10-25。
父提交：{parent}。
程序：{R/'ra2/build-original-c/ra2.exe'}
SHA-256：{digest}
验收边界：{policy}
寻路机制改进授权补充：{addendum}

范围与结果
按整体功能、效果、规则与资源调用验收，不追求逐个BUG复刻，允许有证据支持的寻路机制改进。完成ground_path_completion和ground_path_rebuild的服务整理，新增两个普通交通配方。生产仅改两个C文件；181C/312编译输入/37处未实现保护不变，头文件、CMake、规则/美术、生成入口/分发表、runtime桥接、schema12记录器及通用比较器未改。
父批固定容量满堆保留较低priority候选的机制与节点服务逐字节保留，本轮不新增算法或内存预算变化。父批7412项有意差异和65541项合成见证按哈希继承，不计入本轮新门禁；不声称本轮自然场景触发了堆满改进或普遍最短路径。

第一部分completion：完成门禁与服务发布
can_publish_path明确原有可发布条件：READY、expanded不恰等于10000、current非空、expanded不恰等于expansion_limit、节点长度至少2。两项上限仍为相等判断，不改成>=；空节点检查和上限检查仍先于长度读取。
INVALID_CELL和ALREADY_THERE保留直接空返回，不进入障碍恢复。rebuild_and_finalize依次调用重建、平滑、后处理；重建返回NULL仍按原样把NULL传给后两项服务。所有回调结束后才重新读取共享obstacle_mode，按当时值恢复临时障碍；不提前缓存该标志，也不增加新的错误出口。

第二部分rebuild：元数据、父链和方向发布
initialize_result按原顺序写score截断、length、方向/层高指针、reserved=0、scratch=(0,0)，x87兼容截断保持。reconstruct_steps从终点父链反向填槽：层高先取父链；依次调用读格服务读取父点、子点，写方向后才分别推进child和parent。direction_between只分离既有32位差量及3x3表查询，非相邻格仍写方向8，交由特殊连接处理。
最后重新读取end->path_length写末槽-1，再重新读根格写start，最后将零score改为1；不复用此前的读格结果，也不填写末尾未定义层高槽。合法父链和输出容量仍由调用者提供，没有增加截断、猜测容量、路径合法化或新规则。

原版1.006片段对照
完成阶段沿用未改字节的path_local_probe.c phase3，覆盖原版0x427CBB/0x427D1F/0x427D2E等返回路径，共8192例；{c['successes']}非空返回、{c['failures_or_zero_prefix']}空返回。空返回包含合法早退/门禁与重建桩返回NULL，不当作测试失败。上下文、完整缓冲、返回值、有序回调及原版栈清理一致；累计比较{c['event_words_compared']}个事件字，不能当作同数量服务调用。后处理修改共享障碍标志的情况已包含。
重建沿用path_lifecycle_probe.c phase2，原版0x428370共16384例，长度1..127，含相邻/非相邻父链、层高、负分/分数截断/零分修正。路径描述中的层高缓冲指针归一到原版固定地址后比较，两个实际完整缓冲另行逐字节核对。运行时一次性注册/销毁桥接保持原样，片段不证明全部ABI或所有自然入口。
合计{native['cases']}例，两组输入在改动前和两段后均重跑，不累计成三倍覆盖；原版探针、程序和header独立保留在baseline-probe。prepare/区域发布及局部转弯的其他phase未重跑，不计本批覆盖。

新增自然交通
traffic-cross与traffic-convoy共两个新配方，地图字节直接继承此前核对的coast-sc.MAP，未修改原地形/规则/单位配置。三辆TRUCKA和一名E2使用普通Move事件；其余初始单位沿用原地图配置。使用正式生产程序及原有只读层高/地形目录/移动观测，无内存状态注入、路径结果注入或新增生产钩子。
第一配方近距离交错并改发目标；第二配方错峰出发、折返，再改发尚未到达目标的车辆。第220帧前8帧该车无位移，不把这一次写成行进中改发。实际行进未完成目标改发的数量按记录列出：
{chr(10).join(traffic_lines)}
改生产代码前，原版与父批正式程序各执行两配方，均900+1帧严格通过；最终程序再次执行，两配方均严格通过。两配方改前/后共4配对3604帧，不写成4个独立新场景。检查每个普通命令的提交格、执行event_frame/单位/任务，车辆非空路径方向缓冲、现有stage6返回观测、四单位全程生命/陆地/零层高及最终目标。观测到正常路径消费，不据此宣称所有内部完成/重建分支、锁步网络或全图交通已覆盖。

既有回归、原版异常与社区参考
两段各默认遭遇战301、北桥501、南桥501帧，均3配对1303帧严格。最终重新运行mi/sc/aw3/fm装卸和岸边交通，四种模式的完整轨迹分别等于父批冻结基线。旧mi货车原版2020/C2018、fm步兵原版2219/C2220、严格比较false及随机首差保留；仍为mi/sc/aw3第349帧、fm第350帧，只读前后8帧，不改种子/随机流或比较规则。
列车碰撞、碾压、重复寻路失败及弯曲高差严格通过；原版Z436停滞、Z-193未完成等异常输入/轨迹/基线保留，不要求逐BUG复刻。旧未合格岸边、远目标、坡型8/飞机和碰撞负控制按boundary-inheritance.json继承，未全量重跑。29非主C/86入边按哈希继承，无新增自然非主入口结论。
社区5项固定提交和内容哈希逐字节继承community-reference-review.json：gagarin YR1.001的AStar/FootClass结构与调用线索、EA旧Red Alert的检查后优化发布组织、Phobos扩展定位。未移入第三方引擎代码，不直接套其他版本地址/规则；原版1.006片段和功能对照仍为依据。原版EA/社区源码的结构线索用于分清重建、平滑及最终发布，不作为本项目同版映射证明。

总验收、回退与清理
共{pairs}配对{frames}模拟帧，{strict}严格、{functional}沿用局部功能差异通过；固定seed12345及按模拟帧发令，构建串行，最多两条配对通道/四个游戏进程。新交通使用生产程序，装卸四场使用既有独立事件/只读观测宿主；证据范围分开。
父批409项封存、315项独立生产基线、两段回退、改动前原版探针/宿主及两套新交通完整基线保留。H盘20项输入、原版game.exe/SAVE0029、原规则、旧手写引擎、Git配置和远端引用不变。新增检查器初次误读execute的cell字段，按原schema的event_frame匹配修正，提交格单独严格核对；复用完整轨迹，未重跑或改变游戏输入，详见environment-note.json。
清理{clean['deleted_files']}项可重建中间文件/缓存，共{clean['deleted_bytes']}字节，同目录{clean['protected_files']}项非候选哈希不变。源码、正式程序、资源、基线、回退、轨迹和原版异常保留。只本地提交，不推送。
复核：{R/'verify_final_movement_v60.py'}；提交收据：{S/'postcommit/git-local-commit.json'}。
下一步按功能需要检查路径结果消费/移动队列衔接及更长交通压力，或有度量支持的搜索改进；其他子系统与完整视觉/资源调用验收仍未覆盖，不宣称全游戏等价或普遍最短。
''',encoding='utf-8',newline='\n')
handoff.write_text(f'''当前正式59 / 验证60，2026-10-25。
父提交：{parent}；程序SHA-256：{digest}。
政策：{policy}
机制改进补充：{addendum}
报告：{report}
完成ground_path_completion的发布门禁、重建/平滑/后处理顺序、回调后障碍恢复；ground_path_rebuild的元数据初始化、逆向父链、方向8、终止槽与根点发布。只改2C，181C/312输入/37保护不变。
原版完成8192、重建16384，共24576例，改前和两段后通过；重复输入不累加。完成{c['successes']}非空/{c['failures_or_zero_prefix']}空返回，NULL重建仍调用后两项服务、后处理可改障碍标志；重建缓冲指针归一后比描述并逐字节比实际缓冲，不宣称全部ABI。
新增traffic-cross/traffic-convoy，原地图字节与规则不变，3TRUCKA+1E2普通Move，含真实交错和未完成目标时改发。各900+1帧，改前/后4配对3604帧，均严格通过；两配方分别116/186帧至少3单位同时移动、各3次真实行进未完成目标改发。第220帧前8帧车辆无位移，不算行进改发。最终目标/Guard、全程生命、合法陆地和零高度通过，完整每模式轨迹等于改前基线；无状态/路径注入或新生产钩子。
总19配对22669帧，15严格、4既有局部功能差异。mi/sc/aw3/fm严格false、1/2帧旧时序、349/350随机窗口及Z436/Z-193原版异常保留。29非主C/86入边与旧边界按哈希继承。
前批堆满较低分候选改进与节点服务字节不变，7412预期差异及65541合成见证按哈希继承，不是本轮新覆盖。允许有证据的机制改进，不要求逐BUG相同，不保证全图最短。
社区5项固定参考继续继承：{S/'community-reference-review.json'}；不直接套YR地址/规则或移入第三方引擎代码，原版1.006为对照依据。
基线：{S/'baseline'}；两段回退：{S/'parts'}；原版探针：{S/'baseline-probe'}；旧宿主：{S/'baseline-observer'}；新交通基线：{S/'runs/b-traffic-cross'}、{S/'runs/b-traffic-convoy'}；封存：{S/'final-source'}。
已逐路径哈希清理{clean['deleted_files']}项可重建文件；原始输入、资源、旧引擎和历史证据保留。检查器字段修正详见environment-note.json，原始轨迹未重跑。
下一步按功能需要衔接路径结果消费/移动队列及更长自然交通，或有度量支持的搜索改进；全游戏及完整视觉/资源验收未覆盖。
派生后续工具须显式使用父证据movement-state-v60并保留导入校验。复核：{R/'verify_final_movement_v60.py'}。本地提交，不推送。
''',encoding='utf-8',newline='\n')
lead=f'最新接续：第五十九批正式59 / 验证60已验收。\n交接：{handoff}\n政策：{policy}\n机制改进补充：{addendum}\nEXE：{digest}\n以下历史原地保留。\n\n'.encode('utf-8')
for name in ['交接文档-原版逆向与C重编译-20261020.txt','交接文档-新对话继续推进-20261022.txt']:
 p=P/name;p.write_bytes(lead+p.read_bytes())
p=P/'README.md';ls=p.read_bytes().splitlines(keepends=True);eol=b'\r\n' if ls[0].endswith(b'\r\n') else b'\n'
p.write_bytes('> 当前研究路线（2026-10-25）：原版1.006 C17/x86单位移动第五十九批已验收。路径完成与重建服务、两项新增自然交通；[第五十九批交接](交接文档-单位移动第五十九批正式验收-20261025.txt)。遵守[整体功能与效果边界](docs/项目目标与验收边界-20261024.txt)和[机制改进补充](docs/寻路机制改进验收补充-20261025.txt)。'.encode('utf-8')+eol+b''.join(ls[1:]))
p=R/'ra2/src/gameplay/阅读说明-单位移动.txt';p.write_bytes(f'第五十九批（2026-10-25）\n完成门禁、重建与最终发布；新增原地图普通交通两配方。181C/312输入/37保护，19配对22669帧，原版完成/重建24576例。\n前批有证据的堆容量改进及全部原版差异、异常和基线回退保留。\n报告：{report}\n\n'.encode('utf-8')+p.read_bytes())
pointer=dict(passed=True,status='promoted',formal_baseline_generation=59,verification_round=60,validation=str(S/'validation.json'),exe_sha256=digest,sha256=digest,executable=str(R/'ra2/build-original-c/ra2.exe'),full_original_equivalence_verified=False,report=str(report),handoff=str(handoff),acceptance_policy=str(policy),pathfinding_policy_addendum=str(addendum),path_mechanism_identity_required=False,globally_shortest_paths_verified=False)
for name in ['latest-recovery.json','latest-state-comparison.json','latest-movement-candidate.json']:
 p=P/'reports'/name;x=read(p);x.update(pointer)
 x['current_batch']=dict(formal_generation=59,verification_round=60,accepted_game_pairs=pairs,accepted_frames=frames,native_cases=24576,native_groups=2,synthetic_cases=0,inherited_heap_improvement=True,new_traffic_recipes=2,production_c_sources=181,content_inputs=312,strict_all_frames_equal=False,accepted_baseline_variations=4,strict_game_pairs=strict,functional_game_pairs=functional)
 p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
write(S/'remaining-work.json',dict(passed=True,bug_for_bug_required=False,path_mechanism_identity_required=False,globally_shortest_paths_verified=False,natural_alias_dispatch_required=False,candidates_not_confirmed_failures=True,community_references_available=True,remaining=['Path-result consumer and movement-queue integration as functionally needed','Longer ordinary traffic and evidence-supported search improvements','Other engine subsystems and full visual/resource acceptance']))
for e in read(S/'checker-lineage.json')['entries']:assert e['final_derived_sha256']==sha(R/e['derived'])
paths={Path(p).relative_to(R).as_posix() for p in receipt['inputs']}
paths.update(['ra2/CMakeLists.txt','ra2/run_lift.py','ra2/tools/playtest.py','ra2/build-original-c/ra2.exe','ra2/build-original-c/source-content-receipt.json','ra2/src/gameplay/阅读说明-单位移动.txt','build-faithful.ps1','run_fixture_comparison.py','run_state_comparison.py','evidence/movement-state-v4/SOV01T-original.MAP'])
paths.update(p.relative_to(R).as_posix() for p in R.glob('*v60*') if p.is_file())
paths.update(p.relative_to(R).as_posix() for p in S.iterdir() if p.is_file() and p.suffix in ['.c','.h','.asm','.exe','.json'] and p.name not in ['source-manifest.json','document-manifest.json','validation.json','final-check.json'])
paths.update(p.relative_to(R).as_posix() for p in (S/'fixtures').iterdir() if p.is_file());manifest=[]
for rel in sorted(paths):
 d=S/'final-source'/rel;d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/rel,d);manifest.append(dict(path=rel,sha256=sha(d)))
write(S/'source-manifest.json',manifest)
docs=[P/'README.md',report,handoff,policy,addendum]+[P/n for n in ['交接文档-原版逆向与C重编译-20261020.txt','交接文档-新对话继续推进-20261022.txt']]+[P/'reports'/n for n in ['latest-recovery.json','latest-state-comparison.json','latest-movement-candidate.json']];documents=[]
for p in docs:
 d=S/'current-project'/p.relative_to(P);d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,d);documents.append(dict(path=p.relative_to(P).as_posix(),sha256=sha(d)))
write(S/'document-manifest.json',documents)
write(S/'validation.json',dict(**pointer,parent_commit=parent,state_schema=12,accepted_game_pairs=pairs,accepted_frames=frames,production_c_sources=181,content_inputs=312,unsupported_guards=37,native_cases=24576,probes=2,synthetic_cases=0,inherited_heap_improvement=True,new_traffic_recipes=2,new_traffic_pairs=4,new_traffic_frames=3604,capture_packet_cases_inherited=64,transport_packet_cases_inherited=128,accepted_inherited_variations=4,strict_game_pairs=strict,functional_game_pairs=functional,strict_all_frames_equal=False,source_files=len(manifest),finite_functional_conformance=True,bug_for_bug_required=False,cleanup_performed_this_round=True,pushed=False))
write(S/'final-check.json',dict(passed=True,exe_sha256=digest,source_manifest_sha256=sha(S/'source-manifest.json'),document_manifest_sha256=sha(S/'document-manifest.json'),pushed=False))
print(dict(passed=True,generation=59,exe_sha256=digest,source_files=len(manifest),pairs=pairs,frames=frames,native_cases=24576,new_traffic_recipes=2))
