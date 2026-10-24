"""Promote generation40 after finite functional and real collision acceptance."""
from run_batch_v41 import R,P,S,O,read,write,sha
from pathlib import Path
import shutil,json
for name in ['native-gates.json','effects.json','collision-real-effects.json','bridge-cross-release-effects.json','preservation.json','alias-evidence-inheritance.json','cleanup.json','final-scene-matrix.json','observer-variation.json']:assert read(S/name)['passed'],name
matrix=read(S/'final-scene-matrix.json');assert matrix['production_frames']==5960 and matrix['observer_frames']==2004
digest=sha(R/'ra2/build-original-c/ra2.exe');assert read(S/'parts/advance/validation.json')['exe_sha256']==digest
clean=read(S/'cleanup.json');collision=read(S/'collision-real-effects.json')['scenes'];cycle=read(S/'native-prepare.json')
report=P/'docs/单位移动第四十批-Prepare周期与Advance接续及列车碾压实景-20261024.txt'
handoff=P/'交接文档-单位移动第四十批正式验收-20261024.txt';policy=P/'docs/项目目标与验收边界-20261024.txt'
details='\n'.join(name+'：生命变化'+str(x['health_changes'])+'；目标消失帧'+str(x['target_disappearance_frames'])+'；最终生命'+str(x['actor_final_health'])+'，位置'+str(x['final_actor_position']) for name,x in collision.items())
text=f'''单位移动第四十批（正式40 / 验证41），2026-10-24。
父提交：77e5905145e8a34a4eed21e486950a91fb0e3442。第三十九批353项封存已复核并原地保留。
程序：{R/'ra2/build-original-c/ra2.exe'}
SHA-256：{digest}

验收边界
继续遵守{policy}。目标为整体功能、效果、规则解读和美术资源调用一致；不要求逐个BUG复刻，不无限扩大逐帧矩阵。
本轮固定实现和代表场景，重要效果成立、受影响回归通过、基线回退可用即结束；未改变原版生产规则和美术资源。

实现
新增gameplay/ground_prepare_cycle.h/.c：统一Prepare入口、已有方向队列和需要重寻路时的转换。只有真正转入重试时，才从当前owner读取重试计时器和当前帧；路径裁剪/状态服务完成后的对象变化可见。
runtime/ground_prepare_bridge将主Prepare入口接入统一周期，保留原先单入口/重试适配用于原生段内来源与验证。生成外壳只有这一处主入口分派及三个结果接续增加；原生标签、指令注释、尾跳表和注册保留。
Advance的接续模板提交、刷新、存活/限制检查、候选格进入、速度恢复与旧方向出队收拢到commit_turn_segment，明确状态转换与服务边界。
Prepare路段的列车/碾压放行复用已有ra2_ground_template_gate，保留分类、类型及覆盖层查询顺序；普通Advance允许移动障碍接续，Prepare等待策略仍按既有不同语义处理。
173个生产C源、296项构建输入；新增一个业务C和一个头文件。37个未实现保护不变。比较器、记录器、schema12及原版固定镜像未改。

本轮实际验证
Prepare和Advance两部分，各3组代表场景：默认遭遇战301帧、南北桥上途中放行各501帧；每部分1303帧，各自保存源码/EXE回退。
最终六组受影响原版路径共393216例：Prepare入口、重试、组合周期各65536例；路段门槛、Advance转弯接续和跨格效果各65536例。组合周期是新增65536例，原来两个适配路径也继续验证。
最终正式程序10场5960帧、独立观察4场2004帧；连同两部分共20个通过验收的原版/C配对、10570帧。状态、普通命令、随机数逐模拟帧核对与差异定位自检通过。
另有基线探索4个配对2004帧：首对2场只证明对照一致，效果不合格；第二对2场确认真实碰撞/碾压。本轮实际执行24个游戏配对12574帧，探索与正式验收不混记。
固定seed12345，最多两条场景通道/4个游戏进程，所有构建串行。未重跑与本轮无关的历史大矩阵。

新实景：普通地图、完整独立规则和原生命令/脚本
使用原版提取的完整rules.ini作为独立场景输入，IsTrain绑定原生006DB049读取到type+AA0。仅在隔离游戏目录放置场景规则；H盘原始提取规则和生产资源不改。
列车：原生地图触发CreateTeam，脚本action3向waypoint99移动；不用玩家移动命令或强写路径。原版构造的同一桥层对象链上有两辆不可碾压载具及一名可碾步兵。列车撞掉两辆载具，自己200→160，步兵仍125，最后到达目标格。
碾压：Crusher车辆正常发令，消除桥上两名敌方步兵，生命保持200；两辆友方载具以普通命令占用出口并在210/300帧先后放行。车辆继续经过出口并抵达目标格；出口查询、持有和绕行与既有南北交会场景分别核对。
关闭IsTrain或Crusher的完整规则对照使用同一地图和原生脚本/命令；车辆生命保持200，对应目标保留。证明效果来自正常规则解读与游戏过程，而非直接调用碰撞入口或写结果。
{details}
独立观察版重跑列车、碾压与南北普通占用交通；观测版与正式程序状态及普通移动审计一致。列车/碾压证据本轮已包括真实运行，不再只有合成片段。
列车观察版在158/191/208帧各多一条stage16只读位置诊断记录：C观察器对复用的raw_position回调统一标记，而原生只在主采样位置读取点安装了该观测。501帧游戏状态、随机数、普通命令/移动审计以及其余诊断事件全部一致。严格比较报告仍为false且完整保留，另有functional-acceptance.json和observer-variation.json记录功能验收；未为追平诊断计数改游戏逻辑或比较器。
两项弯曲高差异常、受控隧道出口阻挡和重复重寻路失败纳入有限回归；诊断单位环与普通地图实景分开记录。

调查与保留
首次探索的目标在桥下，列车玩家Move被原版取消，因此没有碰撞效果；两个配对均一致仍不算效果通过。输入、日志和轨迹全部保留，调整后通过正确桥层与原生队伍脚本得到效果证据，未强造运行状态。
新增组合周期第一次原版探针在case724出现一个计时器中间字差异；服务序列与结果一致。原版入口位置查询输出位于frame+44，frame+48随后被重试计时器适配读取。已保留这个服务输出缓冲交接，业务层不解释此旧字段，也未为追逐它扩大实景矩阵。失败源码/探针/日志保留在investigations/prepare-cycle-01，修正记录prepare-boundary-resolution.json；现有和新增路径均通过。
原版4→6弯曲高差Z436停滞、7→4最终Z-193未完成继续保留记录；候选本轮同样表现。它们不是必须永远复刻的BUG要求。
29个非主副本的原始86条入边和前批自然观察沿用；本轮没有新增独立自然入口结论。主入口业务接续变化不删除原始段内入口，全部296项输入扫描未新增直接C调用引用。未以穷尽候选命中阻挡交付。
第三十九批封存、297项独立基线和两部分回退均保留；当前封存只包含实际构建内容、本轮配方及必要探针，不反复复制全部历史工具。
完成验证后按路径、类型和哈希白名单清理{clean['deleted_files']}个确认无用的中间文件/缓存，共{clean['deleted_bytes']}字节；{clean['protected_files']}个同目录非候选文件哈希保持一致。未递归、未强制删除；源文件、原始资源、存档、程序、轨迹、基线和回退保留。
H盘原版既有20项白名单、额外只读规则源及D盘原版程序/真实存档/旧引擎指纹均保持一致。

剩余工作
继续整理Prepare障碍、等待/失败后的后续状态与更多Advance边界；其他移动器、建筑/地形、毁桥等组合选择代表性实景补齐。当前不是完整可读地面移动或独立全游戏引擎。
非主C来源调查保持开放，仅在新证据或功能差异出现时扩展；不逐条包装所有未进入生成标签，也不追逐所有原版异常。旧主观百分比本轮未重新计算。
只读复核：{R/'verify_final_movement_v41.py'}。
本轮本地提交，不推送。提交身份见本地postcommit/git-local-commit.json。
'''
assert not report.exists() and not handoff.exists();report.write_text(text,encoding='utf-8',newline='\n')
handoff.write_text(f'''当前正式40 / 验证41，2026-10-24。
验收边界：{policy}
报告：{report}
程序SHA-256：{digest}
只读复核：{R/'verify_final_movement_v41.py'}
已接入Prepare入口到重试的完整周期；Advance接续提交已收拢，Prepare列车/碾压门槛共用业务接口。组合周期的旧输出缓冲交接已核实并保留。
两部分各3场1303帧；最终正式10场5960帧、观察4场2004帧；共20个验收配对10570帧。六组原版路径393216例，其中新增组合周期65536例。
本轮已取得列车真实撞掉两辆载具、自损40、保留可碾步兵的效果，以及Crusher消除两敌兵后经过占用出口的效果；两种规则关闭对照也已核对。
额外4个基线探索配对单独保留，首对未出现碰撞不能算效果通过。真实场景仅用普通地图/完整独立规则/原生命令与队伍脚本，不写碰撞结果或内部路径。
列车观察版只多3条stage16读位置诊断，游戏状态/普通命令/RNG及其余诊断一致；严格报告false保留，functional-acceptance和observer-variation记录通过。下一轮不要为此追平内部计数。
173个C源、296项构建内容、37个保护；原始标签、尾跳和注册保留。29候选来源调查沿用证据，没有新独立自然C命中声明。
基线：{S/'baseline'}；回退：{S/'parts'}；当前封存：{S/'final-source'}；父批封存原地保留。
下一批按功能单元推进Prepare后续状态与其他移动器/毁桥等代表场景，有限验收，保留原版异常；清理确认无用的文件/缓存，本地提交，不推送。
''',encoding='utf-8',newline='\n')
lead=f'''最新接续：第四十批已验收，正式40 / 验证41。
政策：{policy}
交接：{handoff}
程序SHA-256：{digest}
只读复核：{R/'verify_final_movement_v41.py'}
以下历史保留，以整体功能与效果一致的有限验收边界为准。

'''.encode('utf-8')
for name in ['交接文档-原版逆向与C重编译-20261020.txt','交接文档-新对话继续推进-20261022.txt']:
 p=P/name;p.write_bytes(lead+p.read_bytes())
p=P/'README.md';raw=p.read_bytes();lines=raw.splitlines(keepends=True);eol=b'\r\n' if lines[0].endswith(b'\r\n') else b'\n';p.write_bytes('> 当前研究路线（2026-10-24）：原版1.006 C17/x86单位移动第四十批已验收。Prepare周期、Advance接续及真实列车碰撞/碾压与桥上占用对照；[第四十批交接](交接文档-单位移动第四十批正式验收-20261024.txt)。继续遵守[整体功能与效果一致的验收边界](docs/项目目标与验收边界-20261024.txt)，保留基线、回退和原版异常。'.encode('utf-8')+eol+b''.join(lines[1:]))
p=R/'ra2/src/gameplay/阅读说明-单位移动.txt';p.write_bytes(f'''第四十批当前状态（2026-10-24）
ground_prepare_cycle把入口/已有路径/重试合并为业务周期，计时器与帧只在转入重试后读取；runtime保留位置服务的旧输出缓冲，避免跨状态交接丢失。
Advance的commit_turn_segment集中处理接续模板提交及刷新后的存活/候选格分流；Prepare路段共用模板列车/碾压放行规则，保留与Advance不同的移动障碍策略。
列车真实撞掉两辆车、自损40且同格步兵保留；Crusher真实消除两敌兵并继续经过占用出口。关闭对应规则标志的对照通过。均使用正常地图、完整独立规则、命令/队伍脚本。
20个验收配对10570帧、六组原版路径393216例；另4个基线探索单独保留。报告：{report}
仍按整体功能、效果、规则和资源调用一致验收，不要求逐BUG复刻或无限逐帧扩展。

'''.encode('utf-8')+p.read_bytes())
pointer=dict(passed=True,status='promoted',formal_baseline_generation=40,verification_round=41,validation=str(S/'validation.json'),exe_sha256=digest,sha256=digest,executable=str(R/'ra2/build-original-c/ra2.exe'),full_original_equivalence_verified=False,report=str(report),handoff=str(handoff),acceptance_policy=str(policy))
for name in ['latest-recovery.json','latest-state-comparison.json','latest-movement-candidate.json']:
 p=P/'reports'/name;x=read(p);x.update(pointer);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
write(S/'remaining-work.json',dict(passed=True,completed=['Combined Prepare cycle and deferred state/timer reads','Advance turn commit and shared train/crusher gate','Real train and infantry-crushing bridge cases with rule controls'],remaining=['Further Prepare obstacle/wait/failure followups and Advance boundaries','Other locomotors, buildings/terrain and bridge destruction scenes','Remaining engine subsystems and integration'],bug_for_bug_required=False,natural_alias_dispatch_required=False,percentage_reestimated=False))
receipt=read(R/'ra2/build-original-c/source-content-receipt.json');paths={Path(p).relative_to(R).as_posix() for p in receipt['inputs']}
paths.update(['ra2/CMakeLists.txt','ra2/run_lift.py','ra2/tools/playtest.py','ra2/build-original-c/ra2.exe','ra2/build-original-c/source-content-receipt.json','ra2/src/gameplay/阅读说明-单位移动.txt','build-faithful.ps1','run_fixture_comparison.py','run_state_comparison.py','evidence/movement-state-v4/SOV01T-original.MAP'])
paths.update(p.relative_to(R).as_posix() for p in R.glob('*v41*') if p.is_file());paths.update(p.relative_to(R).as_posix() for p in S.iterdir() if p.is_file() and p.suffix in ['.c','.h','.asm','.exe']);paths.update(p.relative_to(R).as_posix() for p in (S/'fixtures').iterdir() if p.is_file());paths.update((S/n).relative_to(R).as_posix() for n in ['bridge-cross-release-fixtures.json','collision-acceptance-fixtures.json','collision-fixtures.json','collision-fixtures-02.json','connection-fixture-build-arguments.json'])
manifest=[]
for rel in sorted(paths):
 d=S/'final-source'/rel;d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/rel,d);manifest.append(dict(path=rel,sha256=sha(d)))
write(S/'source-manifest.json',manifest)
docs=[P/'README.md',report,handoff,policy]+[P/n for n in ['交接文档-原版逆向与C重编译-20261020.txt','交接文档-新对话继续推进-20261022.txt']]+[P/'reports'/n for n in ['latest-recovery.json','latest-state-comparison.json','latest-movement-candidate.json']];documents=[]
for p in docs:
 d=S/'current-project'/p.relative_to(P);d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,d);documents.append(dict(path=p.relative_to(P).as_posix(),sha256=sha(d)))
write(S/'document-manifest.json',documents)
write(S/'validation.json',dict(**pointer,parent_commit=read(S/'vcs-context.json')['parent_commit'],state_schema=12,paired_scenes=10,paired_frames=5960,observer_scenes=4,observer_frames=2004,part_scenes=6,part_frames=2606,accepted_game_pairs=20,accepted_frames=10570,baseline_exploration_pairs=4,baseline_exploration_frames=2004,total_game_pairs_executed=24,total_frames_compared=12574,probes=6,native_cases=393216,new_cycle_cases=65536,source_files=len(manifest),production_c_sources=173,content_inputs=296,unsupported_guards=37,native_labels_and_tables_preserved=True,legal_alias_sources_inherited=29,new_alias_runtime_scenes=0,real_train_and_crush_effects=True,negative_rule_controls=True,strict_observer_event_equality=False,accepted_diagnostic_variations=1,observer_variation=str(S/'observer-variation.json'),bug_for_bug_required=False,finite_functional_conformance=True,cleanup_performed_this_round=True))
write(S/'final-check.json',dict(passed=True,exe_sha256=digest,source_files=len(manifest),report_sha256=sha(report),handoff_sha256=sha(handoff),policy_sha256=sha(policy),source_manifest_sha256=sha(S/'source-manifest.json'),document_manifest_sha256=sha(S/'document-manifest.json'),pushed=False))
print(dict(passed=True,generation=40,exe_sha256=digest,source_files=len(manifest),report=str(report)))
