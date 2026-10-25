"""Formal67 / verification68: close movement risks and publish continuation-ready evidence."""
from run_batch_v68 import *
roll=read(S/'evidence-rollup.json');clean=read(S/'cleanup.json');source=read(S/'source-preservation.json');queue=read(S/'reachability-fairness.json');other=read(S/'other-movement-acceptance.json')
assert all(d['passed'] for d in [roll,clean,source,queue,other])
receipt=read(R/'ra2/build-original-c/source-content-receipt.json');digest=sha(R/'ra2/build-original-c/ra2.exe');assert digest==receipt['executable_sha256']==read(S/'parts/closeout/validation.json')['exe_sha256']
report=P/'docs/单位移动第六十七批-移动域收口-20261025.txt';handoff=P/'交接文档-单位移动第六十七批正式验收-20261025.txt';checklist=P/'docs/移动域收口清单-20261025.txt';progress=P/'docs/当前进度与剩余内容-20261025-第六十七批.txt'
for p in [report,handoff,checklist,progress]:assert not p.exists(),p
parent=read(S/'vcs-context.json')['parent_commit'];policy=P/'docs/项目目标与验收边界-20261024.txt'
summary=f"{roll['accepted_pairs']}配对、{roll['accepted_frames']}帧：{roll['strict_pairs']}严格，{roll['functional_pairs']}舰船既有差异按功能接受；630784原版片段例，6程序/9片段，重复运行不累计。"
report.write_text(f'''单位移动第六十七批：移动域收口（正式67 / 验证68），2026-10-25
父提交：{parent}
程序：{R/'ra2/build-original-c/ra2.exe'}
SHA-256：{digest}
验收边界：整体功能、规则解读和效果一致；允许有证据支持的机制改进，不以逐BUG或逐位复刻阻止交付。

本轮实际代码
1. ground_cell_services提供可用地图菱形的命名边界与坡面/层高调整；新的ground_map_bounds_bridge只处理1.006布局、备用格、寄存器/标志和ret 8，替换0055A660一个无别名的生成函数。规则没改，108个原版直接调用点的公共边界得到明确实现。
2. ground_failure_transition统一严格距离/两层高度停止条件和32位差值位模式；Prepare、障碍和Arrival调用它，保留查询与回调次序、实时状态和不同停止返回约定。
3. ground_collision复用既有occupation_route，去掉重复的占格前置决策；保留五个步兵子格、车辆位、自身排除、桥层、碾压/武器和友方查询顺序。宽布尔输入显式归一化，原版片段验证通过。
4. 实际182C、131头、313编译输入；改10个既有输入、新增1个运行适配C，CMake新增对应C17严格编译项。原版资源、记录器、比较器、规则和此前堆容量改进保持。

可达性收口
上一批四个原位请求不是已入队后的饥饿。地图width=55、LocalSize=2,5,51,89，可用左边要求y-x<51；63,114、63,116、64,116、65,116都不满足。它们有地形数据，仍不属于可接受目标。
原输入和四辆未运动轨迹原地保留。仅将四个目标改成66,110、67,112、67,116、68,118，不改起点、来车、占道车或释放时序：原版/改前C/当前C十二辆全部精确到达、存活并清空目标。末次请求{queue['last_request']}，最后到达{queue['last_arrival']}，最长请求到达间隔{queue['maximum_request_to_arrival']}帧。

占位与停止收口
双向场景的三辆近目标结果已区分：1023319/1023320的原目标格被占用，导航改选邻格并到达；1023321也先改选目标，后来重建失败时导航被清除。只看最终位置无法区分这些过程。
目标空闲控制能到达原格；目标占用时会改选邻格，任务完成后即使占位车离开也不擅自复活已完成命令，重新发Move后可到原格。CloseEnough=0控制仍保留原来的三个结果，故不把它们一概归因于CloseEnough；严格容差边界另有原版片段门禁。
实际Stop控制在移动中发Stop，队列和目标清空，200/300帧保持静止，350帧新Move后继续到达。Stop有排队/执行/完成证据，采样没有单独停留的Stop-entered帧，不能把缺这个瞬时状态误判为功能失败。

公平性边界
本轮证明有限、合法且已接受请求在指定持续来车/释放条件下全部完成，未证明全局FIFO、无限负载无饥饿或所有地图最短路。本轮没有引入无证据的优先级/退避/FIFO调度，也不把被拒绝目标或已完成/取消任务算作待恢复队列。
保留此前有限桥隧拥堵、吞吐、逆序出队和饥饿恢复证据；其覆盖范围按原收据继承，不重复加总。

其他移动代码与自然对照
6个真实规则单位HTNK、SAPC、DEST、E1、JUMPJET、CLEG，实际六种不同移动器，普通Move均到达请求格且存活；包括悬浮水上到岸。跳跃单位保留空中Move状态，悬浮保留垂直浮动。
舰船原版/改前C已有32帧XY差异，最大3世界单位（1格256），终点、生命和随机序列相同。对象/地形查询循环有一帧时序差，净多一次地形查询；当前C与改前C每一路完整轨迹相同。原始严格比较保留失败，功能验收单列，没有放宽比较器。
实际编译的109个命名移动文件、12个RTTI移动类（含基类）、37个全局保护调用点、29个非主内部入口已清点。37点/29入口没有新增或删除；别名所在生成块字节不变，不强造非法入口。全局保护调用点不等于37项移动缺失功能。
12个家族并非都完成可读重写：Fly、Mech、Tunnel、DropPod、Rocket等仍有原版提升实现，其完整玩法/接口验收随实际功能需求推进；不能把本轮六类实景外推成所有移动器、全部地图和整机等价。

验证与保留
{summary}
主控制矩阵改前/改后每一路完整记录一致；独立观测器与正式程序的所有生产记录一致。默认遭遇战、南北上下桥、列车/碾压、重复重建失败回归通过。既有RNG349/350、到达时序、高差异常、失败输入和无效历史快照原位保留，不要求逐个复刻。
原版20个H盘输入、D盘原game.exe/存档、旧手写x64程序和父封存均核对。社区固定源码线索按上一批哈希继承，本轮未重新下载，地址和规则仍以本机1.006为准。
初始其它移动地图的Infantry字段在Tag后错位，产生OnBridge=-1和人为上层起点；原输入/原版与改前C轨迹保留并排除，改正三行字段后用相同地形和命令重新对照。初始统计器把净多一次查询误当成只有少量记录差，以及Stop瞬时采样假设，均保留最初脚本与复核记录；没有因此更改生产代码、地图规则或原始比较器。
两次未成功编译和CMake布局断言没有产出有效候选；只保留成功构建后的closeout回退。最终构建源码/EXE绑定检查通过，没有边构建边封存。

保留位置：基线{S/'baseline'}；有效回退{S/'parts/closeout'}；改前探针{S/'baseline-probe'}；改前观测器{S/'baseline-observer'}；最终封存{S/'final-source'}。
清理{clean['deleted_files']}项、{clean['deleted_bytes']}字节可再生成产物，受保护文件清理前后不变。本地提交，不推送。
收口清单：{checklist}
交接：{handoff}
进度：{progress}
复核：{R/'verify_closeout_v68.py'}
''',encoding='utf-8',newline='\n')
checklist.write_text(f'''移动域收口清单，2026-10-25（正式67 / 验证68）

已收口的本轮功能风险
1. 地形存在与目标可达范围分开判断；四个越界目标有原版公式、原输入和合法目标控制，十二个合法请求完成。
2. 目标占位后的邻格改选、到达收尾、重建失败清导航分别有记录；空闲/占用/释放/重新发令控制闭环。
3. CloseEnough与高度严格边界共用命名规则，保留实时服务读取；实际Stop清导航并保持静止，新Move才能恢复。
4. 有限持续来车队列逐请求完成；合法活动请求与拒绝、改选、已完成和取消状态区分，不把后者误称饥饿。
5. 六个普通规则移动器有健康到格及前后对照；其余命名移动文件和RTTI家族有清单，原生成实现保留。
6. 默认/桥层/占格碾压/重复失败回归、原版片段门禁、原版/父/基线/回退/封存绑定、清理和本地提交复核闭环。

保留的验收边界
不承诺FIFO、无限负载无饥饿、全图最短、全部地图或所有单位组合覆盖。无自然触发证据的29个非主内部入口按既有政策有界保留，未删改其标签或注册。
37个全局保护点保留，不代表37项移动功能缺失。12类全部可读重写和全游戏等价没有宣称完成；6类自然测试与其它生成实现状态分别列出。
舰船3世界单位/32帧及查询循环时序差是改前已有且最终效果一致的有限差异，原始失败和每一路完整轨迹均保留。
过去的原版异常、高差、RNG、不可用起点、无效快照和本轮无效输入均保留，不自动转成逐BUG复刻清单。

结束条件
上述约定风险已有闭环证据，当前修改未引入新的功能差异；本轮移动域可以交付。后续仅因明确功能回归、实际未支持单位/地图或有测量收益的机制改进重开相应范围，不再为同一已解释边界无限扩大配方。
需要直接修改飞行/钻地/空投等未整理玩法时，先为相应生成实现建立有限对照，再可读化；这项保留不应伪装成已经重写。
明细：{S/'movement-code-inventory.json'}
报告：{report}
''',encoding='utf-8',newline='\n')
progress.write_text(f'''当前进度与剩余内容（第六十七批，2026-10-25）
当前C17/x86主线182C、131头、313编译输入；23117个原提升入口，74个gameplay C。计数不是功能完成率，旧手写x64阶段不合并计算。
已完成：地面移动的搜索/节点/路径处理/队列/桥隧/恢复服务及本轮可达性、占位、停止与有限公平性边界收口。{summary}
新增六类移动器普通实景健康到格；完整源码清单与12个移动类（含基类）保留状态已列出。其余生成移动器并非不存在，也不等于全部可读重写或全量验收。
剩余：战斗/弹道/伤害死亡和对象生命周期、建造经济科技、AI和战役触发/任务目标的逐步可读化和系统验收；菜单与普通用户交互、保存载入、长期战役/遭遇战、视听及资源调用整体验收；37个全局保护点按可达性/实际功能风险处理。飞行/钻地/空投等未整理移动器的完整可读化随对应玩法需求推进。
移动域后续重开条件：有实测功能回归、新单位/地图需求，或有证据的机制改进；不以逐BUG、全部别名或无限交通证明阻止当前交付。当前不提供虚构整体完成百分比。
收口清单：{checklist}
交接：{handoff}
''',encoding='utf-8',newline='\n')
handoff.write_text(f'''正式67 / 验证68，移动域收口，2026-10-25
父提交：{parent}
程序SHA-256：{digest}
报告：{report}
收口清单：{checklist}
进度：{progress}
{summary}
四个拒绝目标已定位为菱形地图边界，合法控制12/12精确到达；三个近目标结果分别定位为占位改选及后续重建清导航，不统归CloseEnough。实际Stop/保持静止/新Move闭环。六类移动器健康到格；舰船既有3世界单位/32帧及查询时序差按效果接受，原始比较不改。
182C/313输入/37全局保护，改10既有输入、加1适配C；无新FIFO或调度机制，无别名删除。109命名移动文件/12移动器家族已清点，并非全部移动类都可读重写。
基线：{S/'baseline'}
有效回退：{S/'parts/closeout'}
探针基线：{S/'baseline-probe'}
最终封存：{S/'final-source'}
复核：{R/'verify_closeout_v68.py'}
提交收据：{S/'postcommit/git-local-commit.json'}
保留全部原版、父档、异常与失败输入；清理{clean['deleted_files']}项，本地提交但不推送。
后续父证据指定movement-state-v68。先推进战斗/对象生命周期等实际功能；移动域仅按收口清单的实测风险重开，不重复扩大已经解释的相同交通配方。
''',encoding='utf-8',newline='\n')
root_names=['README.md','交接文档-原版逆向与C重编译-20261020.txt','交接文档-新对话继续推进-20261022.txt']+['reports/'+n for n in ['latest-recovery.json','latest-state-comparison.json','latest-movement-candidate.json']]
for name in root_names:
    p=P/name;assert git('show','HEAD:'+name)==p.read_bytes(),name
    q=S/'baseline-project'/name;q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q)
lead=f'最新接续：正式67 / 验证68，移动域边界收口已验收。\n交接：{handoff}\n清单：{checklist}\n程序：{digest}\n以下历史原地保留。\n\n'.encode('utf-8')
for name in root_names[1:3]:p=P/name;p.write_bytes(lead+p.read_bytes())
p=P/'README.md';lines=p.read_bytes().splitlines(keepends=True);eol=b'\r\n' if lines[0].endswith(b'\r\n') else b'\n'
p.write_bytes('> 当前研究路线（2026-10-25）：原版1.006 C17/x86第六十七批移动域收口已验收。可达性、占位、停止及有限公平性边界闭环；[交接](交接文档-单位移动第六十七批正式验收-20261025.txt)、[收口清单](docs/移动域收口清单-20261025.txt)、[进度](docs/当前进度与剩余内容-20261025-第六十七批.txt)。以下旧手写引擎阶段不计入本主线完成度。'.encode('utf-8')+eol+b''.join(lines[1:]))
p=R/'ra2/src/gameplay/阅读说明-单位移动.txt';p.write_bytes(f'第六十七批：移动域收口（2026-10-25）\n可用地图菱形/坡高、共用严格停止边界和占格决策；四个越界目标及三个近目标结果已解释，合法队列12/12，六类普通移动健康到格。182C/313输入/37全局保护。\n{summary}\n清单：{checklist}\n报告：{report}\n\n'.encode('utf-8')+p.read_bytes())
pointer=dict(passed=True,status='promoted',formal_baseline_generation=67,verification_round=68,validation=str(S/'validation.json'),exe_sha256=digest,sha256=digest,executable=str(R/'ra2/build-original-c/ra2.exe'),report=str(report),handoff=str(handoff),progress_report=str(progress),movement_closeout_checklist=str(checklist),full_original_equivalence_verified=False,scoped_movement_acceptance_closed=True,all_locomotors_readably_rewritten=False,acceptance_policy=str(policy),pathfinding_policy_addendum=str(P/'docs/寻路机制改进验收补充-20261025.txt'),path_mechanism_identity_required=False,globally_shortest_paths_verified=False)
batch=dict(formal_generation=67,verification_round=68,accepted_game_pairs=roll['accepted_pairs'],accepted_frames=roll['accepted_frames'],strict_game_pairs=roll['strict_pairs'],functional_game_pairs=roll['functional_pairs'],native_cases=630784,native_programs=6,native_groups=6,native_fragments=9,production_c_sources=182,content_inputs=313,unsupported_guards=37,inherited_heap_improvement=True,synthetic_cases=0,strict_all_frames_equal=False,fifo_guarantee=False,unbounded_starvation_freedom_proved=False,valid_queue_requests=12,valid_queue_exact_arrivals=12,natural_locomotors=6,all_traffic_requests_exactly_arrived=False,whole_game_acceptance=False)
for name in root_names[3:]:
    p=P/name;x=read(p);x.update(pointer);x['current_batch']=batch;p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
write(S/'remaining-work.json',dict(passed=True,scoped_movement_acceptance_closed=True,movement_reopen_conditions=['Measured functional regression','Actual new unit/map/locomotor requirements','Measured mechanism improvement'],remaining=['Systematic combat/object lifecycle/production/economy/AI/campaign acceptance','User lifecycle, saves, long games, visual/audio/resource release acceptance','Risk-based global guard work and unrefactored locomotors when touched'],fifo_proved=False,all_locomotors_readably_rewritten=False,bug_for_bug_required=False))
paths={Path(p).relative_to(R).as_posix() for p in receipt['inputs']}
paths.update(['ra2/CMakeLists.txt','ra2/build-original-c/ra2.exe','ra2/build-original-c/source-content-receipt.json','ra2/src/gameplay/阅读说明-单位移动.txt','build-faithful.ps1','run_fixture_comparison.py','run_state_comparison.py'])
paths.update(p.relative_to(R).as_posix() for p in R.glob('*v68*') if p.is_file())
paths.update(p.relative_to(R).as_posix() for p in S.iterdir() if p.is_file() and p.suffix in ['.c','.h','.exe','.json','.py'] and p.name not in ['source-manifest.json','document-manifest.json','validation.json','final-check.json'])
paths.update(p.relative_to(R).as_posix() for p in (S/'fixtures').iterdir() if p.is_file());manifest=[]
for rel in sorted(paths):
    p=S/'final-source'/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/rel,p);manifest.append(dict(path=rel,sha256=sha(p)))
write(S/'source-manifest.json',manifest)
docs=[P/n for n in root_names]+[report,handoff,checklist,progress,policy,P/'docs/寻路机制改进验收补充-20261025.txt'];documents=[]
for p in docs:
    q=S/'current-project'/p.relative_to(P);q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q);documents.append(dict(path=p.relative_to(P).as_posix(),sha256=sha(q)))
write(S/'document-manifest.json',documents)
write(S/'validation.json',dict(pointer|batch,parent_commit=parent,state_schema=12,source_files=len(manifest),rollback_parts=['closeout'],excluded_rollback_dirs=['explorations/layout-assertion'],protected_baseline_and_originals=True,cleanup_performed=True,pushed=False))
write(S/'final-check.json',dict(passed=True,exe_sha256=digest,source_manifest_sha256=sha(S/'source-manifest.json'),document_manifest_sha256=sha(S/'document-manifest.json'),pushed=False))
print(dict(passed=True,exe_sha256=digest,source_files=len(manifest),pairs=roll['accepted_pairs'],frames=roll['accepted_frames']))
