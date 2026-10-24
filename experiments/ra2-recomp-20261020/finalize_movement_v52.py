"""Promote formal batch51 with bounded services, coast effects and preserved evidence."""
from run_batch_v52 import *
for name in ['native-gates.json','effects.json','preservation.json','cleanup.json','final-scene-matrix.json','rng-functional-impact.json','rng-first-split-window.json']:assert read(S/name)['passed'],name
receipt=read(R/'ra2/build-original-c/source-content-receipt.json');digest=sha(R/'ra2/build-original-c/ra2.exe')
matrix=read(S/'final-scene-matrix.json');effects=read(S/'effects.json');native=read(S/'native-gates.json');clean=read(S/'cleanup.json')
parts=[read(S/'parts'/n/'validation.json') for n in ['prepare','advance']];assert parts[-1]['exe_sha256']==digest
pairs=sum(x['scene_count'] for x in parts)+len(matrix['results']);frames=sum(x['frames'] for x in parts)+matrix['production_frames']+matrix['observer_frames']
strict_pairs=sum(x['scene_count'] for x in parts)+sum(x['strict_trace_equal'] for x in matrix['results']);variations=effects['accepted_baseline_variations'];assert variations==2 and pairs==14 and frames==17164 and strict_pairs==12
report=P/'docs/单位移动第五十一批-Prepare重试与Advance采样及水岸交通-20261024.txt';handoff=P/'交接文档-单位移动第五十一批正式验收-20261024.txt';policy=P/'docs/项目目标与验收边界-20261024.txt'
ww=effects['representative']['ww']['effect_modes'];js=effects['representative']['js']['effect_modes'];rng=read(S/'rng-functional-impact.json')
text=f'''单位移动第五十一批（正式51 / 验证52），2026-10-24。
父提交：{read(S/'vcs-context.json')['parent_commit']}。第五十批403项封存已逐项核对；本轮315项独立基线保留。
程序：{R/'ra2/build-original-c/ra2.exe'}
SHA-256：{digest}
政策：{policy}

实现与服务边界
遵守整体功能、效果、规则与资源解读一致，不追求逐个BUG复刻。只整理ground_prepare.c、ground_advance.c，保持181个生产C、312项编译内容、37个未实现保护；未增加生产文件或修改CMake。
Prepare入口防护之后，将已有路径的类别判断、距离裁剪和路径头重读集中为prepare_queued_path。类别1/15的两次短路查询保留；裁剪服务之后再读实际路径头，不缓存服务前的值。
重试阶段保持计时器就绪→延迟查询→重启计时器→重建路径。只有重建失败才进入finish_failed_rebuild，按原顺序查所属对象、目标接受情况、可能已被服务改变的无效目标、近目标距离和任务，随后取消目标、停止导航并判断对象生死。任务2/11的两次查询保留，成功重建不走失败服务。
Advance将前一采样格解析与当前采样位置变换分开。先处理标记/清旗，查前一索引，走当前格或前一样本变换；然后重新查当前索引、读取当前样本并变换，保留变换对样本方向的修改，清Z后才读原始位置、判是否跨格。跨格放置/桥层/列车伤害/存活/登记/覆盖层和末尾朝向服务次序保持；入口绑定context一次的方式不变。
未改生成标签/分发表、runtime适配、生产记录器schema12、通用比较器、随机算法、规则或美术。29非主C候选/86原始入边按哈希继承，312项输入扫描无新直接C调用；未冒称新自然入口或自然隧道共享出口覆盖。

分部分验证与回退
Prepare原版片段入口65536、重试65536，共131072例；Advance原版片段65536例；本轮196608个不同用例输入，核对探针覆盖的状态、服务调用、ABI/栈、控制字和分支结果。重跑不重复计数，片段证明不等于自然场景覆盖。
两个部分各默认301帧、北桥501帧、南桥501帧，共3配对1303帧，均严格通过并保留源码/工具/程序回退。运输构造128与Capture64例按哈希继承，未重跑或当作新增例数。

真实水岸：载车时的水上卸载请求与岸边占用
ww保留原水面/沙滩/陆地记录和第五十批普通初始对象位置，只增加700帧Unload事件。两模式700帧均在真实水格[129,103]提交并执行事件，货车在700..899帧保持装载；不把事件执行冒称直接卸载服务的返回结果。
返岸后首次1404帧才卸下。原落点[138,101]仍被交通车占用，实际选合法陆格[139,102]。占位车1500帧第一条移动命令未产生位移，2250帧换目标、2261帧实际离开；第二轮3004帧在已空的[138,101]卸下。
原版两轮装/卸{[(c['board_frame'],c['drop_frame']) for c in ww['original']['cycles']]}，C版{[(c['board_frame'],c['drop_frame']) for c in ww['generated-c']['cycles']]}；第二次装车有32帧原有差异，首次过水样本数与瞬时子格也有差异，严格false保留。两轮载员保持、真实水面/沙滩经过、落格、最终目标和生命结果一致。
最终运输船[138,102]、货车[139,104]、舰船[130,106]、普通步兵[140,100]、传送步兵[138,105]、占位车[138,104]；参与对象生命全程保持。当前每种模式分别逐条等于改代码前该模式的完整轨迹。

其他移动器与动态交通
js以第五十批SHAD/E2海岸地图为底，只将DEST换成SUB、CLEG换成JUMPJET，保留原地形和规则。SUB不创建驱逐舰的ASW子对象，已用0..2帧短窗口确认对象编号变化，再发正常目标和登载/卸载事件。
SHAD/E2两轮77/2004、2353/3504装/卸，落格均[138,102]，E2随后到[140,104]；潜艇水路到[130,96]，普通步兵到[140,100]，飞行步兵到[138,105]，生命全程保持。船、飞行载具、地面步兵和飞行步兵按不同具体对象解释，不能用同一任务编号替代真实装载/移动效果。
飞行步兵原规则Locomotor为Jumpjet、JumpjetHeight500、JumpjetClimb20；两模式均有3676帧高度>=450，峰值585、最终500。原版/C移动中的高空样本分别{js['original']['jumpjet_infantry']['moving_airborne_frames']}/{js['generated-c']['jumpjet_infantry']['moving_airborne_frames']}，最终任务仍为2；只称到达目标格并悬停，不称Guard结束或精确落到请求点。SUB的记录Z0不被当成潜航深度；生产schema未新增步兵移动器指针，规则GUID与可观察位置/类别分开记录。
两轮空运实际过水时点、瞬时高度、飞行步兵朝向等旧差异保留；当前原版/C各自完整轨迹等于改动前本模式轨迹，有限功能验收通过。

随机数分流的功能边界
ww/js首个随机快照差异分别{rng['new_variants']['ww']['rng_first_different_frame']}/{rng['new_variants']['js']['rng_first_different_frame']}帧。每场只读一个首差前后各8帧窗口，并记录参与对象位置/任务/朝向/生命的首差；见rng-first-split-window.json。快照差异不等于定位某次随机调用因果，未宣称原始发生器或具体调用来源已证明。
两场舰船在348/439帧已出现任务字段差异，早于随机快照首差349/440；首差时ww两项随机索引各差1、js各差3，不当作实际调用次数证明，也未把快照差异当作所有运动差异的起因。参与对象的生命字段全程无差异。
全程生命、两轮载员、合法落点、岸边占用释放、最终目标与悬停效果另行检查。分流在本轮改动前已存在，重构后未改变各模式完整轨迹；原规则/生成算法/随机种子未改，未添加随机调用钩子、重置或追平随机流，未放宽通用比较器。
旧1029/349分析及第五十批飞机/旧坡图控制按哈希继承，不计本轮新实测。后续只有出现功能影响才扩展，未推及战斗随机分配或全游戏等价。

验收、异常与保留
含两部分共{pairs}组配对{frames}模拟帧，{strict_pairs}严格、{variations}按上述局部功能通过。最终生产{matrix['production_scenes']}配对{matrix['production_frames']}帧、事件/只读宿主{matrix['observer_scenes']}配对{matrix['observer_frames']}帧。固定seed12345，最多两条配对通道/四个游戏进程，构建串行。
坡型8独立模块主车完成桥道往返、级4/5/6与车兵交通绕行；历史地图接桥受阻原因未定位，原有控制证据原位继承，不继续无功能目标地追查。受影响列车碰撞、碾压、重复失败、弯曲高差Z436停滞/Z-193未完成已有限回归；负对照继承旧证据，原版异常不自动变成必须复刻要求。
第一次短身份窗口0..2帧结束后，比较包装器要求900帧才输出的地形目录而失败；两个游戏轨迹保留，未计正式配对。随后不请求地形目录的同范围确认严格通过，亦不计正式配对。没有因该采集错误重跑长场景或修改生产记录器。
父批403项封存、本轮315项基线、两部分回退、改动前宿主、完整原版/C轨迹和原版异常保留；H盘20项输入、原规则、原版EXE/SAVE0029、旧手写引擎、Git配置与远端引用均不变。
清理{clean['deleted_files']}个逐路径/类型/哈希核对的可重建文件或缓存，共{clean['deleted_bytes']}字节；同目录{clean['protected_files']}项非候选哈希不变。源文件、正式程序、资源、轨迹、基线与回退保留。
后续候选按功能需要推进：ground_obstacle的友军阻挡近目标/桥层通知，ground_path_prepare的桥层高度/朝向邻格排除/根节点，ground_recovery的失败预算/音效/关联对象通知；这些是待整理候选，不代表当前已发现功能失败。实景可补岸边所有合法落点占用后的等待释放、多载员卸载顺序和其他地形。js飞行步兵任务2保留，不因未变成Guard而默认当作必须修复的BUG。
剩余还有其他引擎子系统。本批为游戏逻辑和代表状态验证，不等同完整图像/资源调用或全游戏验收。
复核：{R/'verify_final_movement_v52.py'}。本地提交不推送，收据：{S/'postcommit/git-local-commit.json'}。
'''
assert not report.exists() and not handoff.exists();report.write_text(text,encoding='utf-8',newline='\n')
handoff.write_text(f'''当前正式51 / 验证52，2026-10-24。
父提交：{read(S/'vcs-context.json')['parent_commit']}。
政策：{policy}
报告：{report}
程序SHA-256：{digest}
只整理ground_prepare与ground_advance，181C/312输入/37保护，无新增生产文件或CMake改动。Prepare分已有路径/失败重建后续；Advance分前样本/重读当前样本，服务副作用及状态顺序保留。
196608原生片段用例（Prepare131072、Advance65536），两部分各3组1303帧；合计{pairs}组{frames}帧，12严格、2局部功能通过。运输128/Capture64继承，不重复计数。
ww在700帧真实水格[129,103]执行卸载事件但载员保持，返岸1404帧才卸；原落点占用改选[139,102]，交通车2261帧实际离开，第二卸3004帧回到[138,101]。第二次装车原版1923/C1955帧差异保留。
js的SUB/JUMPJET替换按正常地图记录，编号先短窗口确认；SHAD/E2两轮77/2004、2353/3504，潜艇、普通/飞行步兵目标格成立，生命保持。飞行步兵最终500高度、任务2悬停，峰值585；不称Guard完成，不把潜艇Z0当潜航深度。
ww/js随机快照首差349/440，固定17帧窗口及有限功能核查；各模式当前完整轨迹等于其改动前轨迹，严格false保留，不追平随机数或逐BUG复刻。
坡型8独立往返与列车/碾压/重复失败/高差异常有限回归；旧坡图原因、旧飞机/随机诊断等按哈希继承。29非主C/86入边继承，无新自然入口结论。
基线：{S/'baseline'}；回退：{S/'parts'}；改动前宿主：{S/'baseline-observer'}；封存：{S/'final-source'}。
下一步可按功能需要整理ground_obstacle友军阻挡/桥层通知、ground_path_prepare桥层/朝向排除/根节点、ground_recovery失败预算/音效/关联对象通知；再补全合法卸载点占用后的等待释放、多载员卸载顺序。它们是待整理候选，不是已确认失败；其他引擎子系统仍在范围外。沿用整体功能/效果一致的有限验收，保留原版异常。
复核：{R/'verify_final_movement_v52.py'}。本地提交不推送。
''',encoding='utf-8',newline='\n')
lead=f'最新接续：第五十一批正式51 / 验证52已验收。\n交接：{handoff}\n政策：{policy}\nEXE：{digest}\n以下历史原地保留。\n\n'.encode('utf-8')
for name in ['交接文档-原版逆向与C重编译-20261020.txt','交接文档-新对话继续推进-20261022.txt']:
 p=P/name;p.write_bytes(lead+p.read_bytes())
p=P/'README.md';ls=p.read_bytes().splitlines(keepends=True);eol=b'\r\n' if ls[0].endswith(b'\r\n') else b'\n'
p.write_bytes('> 当前研究路线（2026-10-24）：原版1.006 C17/x86单位移动第五十一批已验收。Prepare重试/Advance采样服务、水上卸载请求及飞行步兵/潜艇交通；[第五十一批交接](交接文档-单位移动第五十一批正式验收-20261024.txt)。继续遵守[整体功能与效果一致的验收边界](docs/项目目标与验收边界-20261024.txt)。'.encode('utf-8')+eol+b''.join(ls[1:]))
p=R/'ra2/src/gameplay/阅读说明-单位移动.txt';p.write_bytes(f'第五十一批（2026-10-24）\nPrepare重试/Advance采样服务，181C/312输入/37保护，{pairs}组{frames}帧、196608原生片段例。\n水上卸载请求保持装载、岸边占用替代落格及飞行步兵/潜艇交通按冻结基线和功能通过；保留严格false及随机差异。\n报告：{report}\n\n'.encode('utf-8')+p.read_bytes())
pointer=dict(passed=True,status='promoted',formal_baseline_generation=51,verification_round=52,validation=str(S/'validation.json'),exe_sha256=digest,sha256=digest,executable=str(R/'ra2/build-original-c/ra2.exe'),full_original_equivalence_verified=False,report=str(report),handoff=str(handoff),acceptance_policy=str(policy))
for name in ['latest-recovery.json','latest-state-comparison.json','latest-movement-candidate.json']:
 p=P/'reports'/name;x=read(p);x.update(pointer);x['current_batch']=dict(formal_generation=51,verification_round=52,accepted_game_pairs=pairs,accepted_frames=frames,native_cases=196608,production_c_sources=181,content_inputs=312,strict_all_frames_equal=False,accepted_baseline_variations=variations,strict_game_pairs=strict_pairs,functional_game_pairs=variations);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
write(S/'remaining-work.json',dict(passed=True,bug_for_bug_required=False,natural_alias_dispatch_required=False,percentage_reestimated=False,old_corner_followup_only_for_functional_need=True,rng_exact_call_source_proved=False,candidates_not_confirmed_failures=True,remaining=['ground_obstacle: allied blocker proximity, height and bridge-layer notifications','ground_path_prepare: bridge height, facing exclusions and root service','ground_recovery: failure budget, sound and linked object callbacks','All legal unload cells occupied, wait/release and multiple passenger order','Other engine subsystems and full visual/resource acceptance']))
paths={Path(p).relative_to(R).as_posix() for p in receipt['inputs']}
paths.update(['ra2/CMakeLists.txt','ra2/run_lift.py','ra2/tools/playtest.py','ra2/build-original-c/ra2.exe','ra2/build-original-c/source-content-receipt.json','ra2/src/gameplay/阅读说明-单位移动.txt','build-faithful.ps1','run_fixture_comparison.py','run_state_comparison.py','evidence/movement-state-v4/SOV01T-original.MAP'])
paths.update(p.relative_to(R).as_posix() for p in R.glob('*v52*') if p.is_file())
paths.update(p.relative_to(R).as_posix() for p in S.iterdir() if p.is_file() and p.suffix in ['.c','.h','.asm','.exe','.json'] and p.name not in ['source-manifest.json','document-manifest.json','validation.json','final-check.json'])
paths.update(p.relative_to(R).as_posix() for p in (S/'fixtures').iterdir() if p.is_file())
manifest=[]
for rel in sorted(paths):
 d=S/'final-source'/rel;d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/rel,d);manifest.append(dict(path=rel,sha256=sha(d)))
write(S/'source-manifest.json',manifest)
docs=[P/'README.md',report,handoff,policy]+[P/n for n in ['交接文档-原版逆向与C重编译-20261020.txt','交接文档-新对话继续推进-20261022.txt']]+[P/'reports'/n for n in ['latest-recovery.json','latest-state-comparison.json','latest-movement-candidate.json']]
documents=[]
for p in docs:
 d=S/'current-project'/p.relative_to(P);d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,d);documents.append(dict(path=p.relative_to(P).as_posix(),sha256=sha(d)))
write(S/'document-manifest.json',documents)
write(S/'validation.json',dict(**pointer,parent_commit=read(S/'vcs-context.json')['parent_commit'],state_schema=12,accepted_game_pairs=pairs,accepted_frames=frames,production_c_sources=181,content_inputs=312,unsupported_guards=37,native_cases=native['cases'],probes=native['groups'],capture_packet_cases_inherited=64,transport_packet_cases_inherited=128,accepted_inherited_variations=variations,strict_all_frames_equal=False,source_files=len(manifest),finite_functional_conformance=True,bug_for_bug_required=False,cleanup_performed_this_round=True,pushed=False))
write(S/'final-check.json',dict(passed=True,exe_sha256=digest,source_manifest_sha256=sha(S/'source-manifest.json'),document_manifest_sha256=sha(S/'document-manifest.json'),pushed=False))
print(dict(passed=True,generation=51,exe_sha256=digest,source_files=len(manifest),pairs=pairs,frames=frames))
