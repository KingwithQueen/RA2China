"""Promote the finite functional batch, preserving exact build and rollback inputs."""
from run_batch_v42 import *
for n in ['native-gates.json','effects.json','preservation.json','alias-evidence-inheritance.json','cleanup.json','final-scene-matrix.json']:assert read(S/n)['passed'],n
receipt=read(R/'ra2/build-original-c/source-content-receipt.json');digest=sha(R/'ra2/build-original-c/ra2.exe');matrix=read(S/'final-scene-matrix.json');effects=read(S/'effects.json');clean=read(S/'cleanup.json');native=read(S/'native-gates.json')
assert read(S/'parts/advance/validation.json')['exe_sha256']==digest
report=P/'docs/单位移动第四十一批-障碍等待失败收尾与其他移动器及毁桥实景-20261024.txt';handoff=P/'交接文档-单位移动第四十一批正式验收-20261024.txt';policy=P/'docs/项目目标与验收边界-20261024.txt'
parts=[read(S/'parts'/n/'validation.json') for n in ['prepare','advance']]
pairs=matrix['production_scenes']+matrix.get('observer_scenes',0)+sum(x['scene_count'] for x in parts);frames=matrix['production_frames']+matrix.get('observer_frames',0)+sum(x['frames'] for x in parts)
exploratory=[]
for folder in sorted(list((S/'runs').glob('baseline-*'))+[S/'runs/bridge-destroy']):
 x=read(folder/'comparison.json');exploratory.append(dict(tag=folder.name,passed=x['passed'],frames=x.get('comparison',{}).get('frames_compared',0)))
text=f'''单位移动第四十一批（正式41 / 验证42），2026-10-24。
父提交：{read(S/'vcs-context.json')['parent_commit']}。第四十批379项封存和当前独立299项基线已核对保留。
程序：{R/'ra2/build-original-c/ra2.exe'}
SHA-256：{digest}
验收政策：{policy}

实现与服务边界
新增ground_failure_transition.h/.c，统一“仅对有效路段清除终点与driving”和“按实时目标取消/停止导航”的状态转换。Prepare障碍接近终点、阻挡反应、失败预算耗尽三处复用；保持无目标时停止服务返回值不参与成功判定，有目标时取消服务先于停止服务。
失败停止后仍重新查询owner存活；提示音、关联对象通知和最终selector/flag收尾保留原来顺序，服务可以修改对象/状态。保留原本终点已无效时不额外改driving的边界，未重解释为新的游戏规则。
等待路径重建之后，复用ground_prepare_after_rebuild出口；先检查当前owner及失败时的目标接受结果，再重新读取当前帧、延迟并启动短重试计时器。等待长计时器仍决定模式1/2，未被共享出口合并。
Advance转弯接续复用相同路段失效接口；保留模板提交、刷新、存活/限制检查、候选进入、恢复速度与移除旧方向的先后次序。
174个生产C、298项编译内容输入，37个未实现保护。生成C、runtime适配、比较器、schema12记录器均未改；原生标签、尾跳、注册表和既有入口全部保留。

有限验证
两部分各默认遭遇战301帧、南北占用出口/步兵车辆交会各501帧，每部分1303帧，分别封存源码和EXE回退。
受影响原生路径{native['groups']}组、{native['cases']}例，涵盖障碍/反应、失败预算与共同收尾、清障/等待、Prepare入口与重试周期、Advance接续和采样效果。每份记录标明实际探针程序与验证时源码身份；合成原生片段与普通地图实景分开记。
最终正式程序{matrix['production_scenes']}场{matrix['production_frames']}帧、只读桥格观察{matrix.get('observer_scenes',0)}场{matrix.get('observer_frames',0)}帧；连同部分验收共{pairs}个通过的原版/C配对、{frames}个模拟帧。状态、普通命令与移动审计、随机数逐帧一致，差异定位/缺帧拒绝自检通过。
本轮额外探索{len(exploratory)}个配对：详情见exploration-summary.json。对象编号、阻挡摆放和触发参数不合格的探索保留，不计正式验收。
最多两条游戏通道/四个游戏进程，构建串行。固定范围达到代表效果后结束，未扩张为穷尽全标签/全组合验证。

代表效果（原版与C分别核对）
{json.dumps(effects['representative'],ensure_ascii=False,indent=2)}

真实列车碰撞、碾压与桥上占用出口继续有限回归；弯曲高差Z436停滞与Z-193未完成异常记录保留。本轮不要求永久逐BUG复刻。
新增的桥格观察程序只将既有只读格目录输出推迟到第200帧：检查的12个桥格中，66行两格在毁桥场景由桥变为非桥，旁边10格保留桥面，完整桥对照12格仍为桥；原版/C目录一致，观察版全部轨迹记录与正式程序逐条一致。生产记录器和schema未改。
第四十批内部观察器的三条stage16诊断数量差异及功能验收沿用原始证据，本轮没有重跑该旧内部观察矩阵，也未为追平计数改游戏逻辑。
毁桥使用原版任务地图同样的EnteredBy国家参数13和正常桥格CellTag/DestroyAttached动作32；单位未直接关联销毁标签，也未写桥/单位状态。原版原生006B1592/006B15A8调用Map桥毁坏服务00569090。早期EnteredBy=0场景不触发，严格对照通过仍不算毁桥效果；该报告完整保留并从正式矩阵移除。
29个非主C候选及86条原始入边调查沿用；全部当前输入未出现新增直接C调用，不宣称取得新的独立合法自然入口。不以穷尽候选命中作为交付条件。

保留与清理
第四十批封存、当前299项基线、两部分回退、所有探索/异常输入与轨迹保留；原版程序、真实存档、旧引擎、H盘20项原版资源及只读提取规则指纹保持一致。
按路径、类型、哈希清理{clean['deleted_files']}个可重建中间文件/缓存，{clean['deleted_bytes']}字节；同目录{clean['protected_files']}个非候选文件哈希不变。未递归/强制删除，未删除源文件、正式程序、基线、回退、轨迹和原始素材。

剩余工作
当前并非完整可读地面移动或独立全游戏引擎。继续按功能单元整理尚留生成外壳的状态分支、更多移动器与损坏/修复桥和动态交通组合；规则解析、资源使用和其他子系统的集成仍需后续推进。
原版异常和29个候选来源仅在出现新功能证据时扩展，不无限穷举。总体百分比不能由本轮移动样例覆盖率推算，本轮不重新估计全项目完成率。
只读复核：{R/'verify_final_movement_v42.py'}。
本地提交，不推送；提交身份见postcommit/git-local-commit.json。
'''
assert not report.exists() and not handoff.exists();report.write_text(text,encoding='utf-8',newline='\n')
handoff.write_text(f'''当前正式41 / 验证42，2026-10-24。
政策：{policy}
报告：{report}
EXE SHA-256：{digest}
统一Prepare障碍/反应/失败收尾，等待重建复用服务出口，Advance接续复用路段失效边界。
174个C、298项输入、37保护；生成外壳/适配/比较器/记录器未改。
验收{pairs}个配对{frames}帧；原生{native['groups']}组{native['cases']}例。新增其他移动器、建筑地形及毁桥代表效果见effects.json；无效果探索保留且不计验收。
基线：{S/'baseline'}；回退：{S/'parts'}；封存：{S/'final-source'}。
原版高差异常、前批观察诊断差异和29候选来源调查保留，未把逐BUG/穷举自然入口作为验收门槛。
复核：{R/'verify_final_movement_v42.py'}。下一批继续功能边界/其他子系统集成，有限代表实景与受影响回归，本地提交不推送。
''',encoding='utf-8',newline='\n')
lead=f'最新接续：第四十一批正式41 / 验证42已验收。\n交接：{handoff}\n政策：{policy}\nEXE：{digest}\n以下历史原地保留。\n\n'.encode('utf-8')
for name in ['交接文档-原版逆向与C重编译-20261020.txt','交接文档-新对话继续推进-20261022.txt']:
 p=P/name;p.write_bytes(lead+p.read_bytes())
p=P/'README.md';raw=p.read_bytes();ls=raw.splitlines(keepends=True);eol=b'\r\n' if ls[0].endswith(b'\r\n') else b'\n';p.write_bytes('> 当前研究路线（2026-10-24）：原版1.006 C17/x86单位移动第四十一批已验收。障碍、等待和失败收尾及其他移动器/建筑地形/毁桥代表实景；[第四十一批交接](交接文档-单位移动第四十一批正式验收-20261024.txt)。继续遵守[整体功能与效果一致的验收边界](docs/项目目标与验收边界-20261024.txt)，保留基线、回退和原版异常。'.encode('utf-8')+eol+b''.join(ls[1:]))
p=R/'ra2/src/gameplay/阅读说明-单位移动.txt';p.write_bytes(f'第四十一批（2026-10-24）\nground_failure_transition统一障碍/失败停止与有效路段清除；ground_wait复用重建后的共享服务出口，Advance接续共用失效边界。\n174个C、298项输入、37保护；{pairs}个验收配对{frames}帧；原生{native["cases"]}例。\n报告：{report}\n继续按整体功能/效果一致验收，不追逐逐BUG或无限内部计数一致。\n\n'.encode('utf-8')+p.read_bytes())
pointer=dict(passed=True,status='promoted',formal_baseline_generation=41,verification_round=42,validation=str(S/'validation.json'),exe_sha256=digest,sha256=digest,executable=str(R/'ra2/build-original-c/ra2.exe'),full_original_equivalence_verified=False,report=str(report),handoff=str(handoff),acceptance_policy=str(policy))
for n in ['latest-recovery.json','latest-state-comparison.json','latest-movement-candidate.json']:
 p=P/'reports'/n;x=read(p);x.update(pointer);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
write(S/'exploration-summary.json',dict(passed=True,results=exploratory,excluded_from_acceptance=True))
write(S/'remaining-work.json',dict(passed=True,bug_for_bug_required=False,natural_alias_dispatch_required=False,percentage_reestimated=False,remaining=['Generated state branches and service boundaries','More locomotors, bridge damage/repair and dynamic traffic combinations','Other engine subsystems and integration']))
paths={Path(p).relative_to(R).as_posix() for p in receipt['inputs']}
paths.update(['ra2/CMakeLists.txt','ra2/run_lift.py','ra2/tools/playtest.py','ra2/build-original-c/ra2.exe','ra2/build-original-c/source-content-receipt.json','ra2/src/gameplay/阅读说明-单位移动.txt','build-faithful.ps1','run_fixture_comparison.py','run_state_comparison.py','evidence/movement-state-v4/SOV01T-original.MAP'])
paths.update(p.relative_to(R).as_posix() for p in R.glob('*v42*') if p.is_file());paths.update(p.relative_to(R).as_posix() for p in S.iterdir() if p.is_file() and p.suffix in ['.c','.h','.asm','.exe']);paths.update(p.relative_to(R).as_posix() for p in (S/'fixtures').iterdir() if p.is_file())
paths.update(p.relative_to(R).as_posix() for p in S.glob('*fixtures*.json'))
manifest=[]
for rel in sorted(paths):
 d=S/'final-source'/rel;d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/rel,d);manifest.append(dict(path=rel,sha256=sha(d)))
write(S/'source-manifest.json',manifest)
docs=[P/'README.md',report,handoff,policy]+[P/n for n in ['交接文档-原版逆向与C重编译-20261020.txt','交接文档-新对话继续推进-20261022.txt']]+[P/'reports'/n for n in ['latest-recovery.json','latest-state-comparison.json','latest-movement-candidate.json']];documents=[]
for p in docs:
 d=S/'current-project'/p.relative_to(P);d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,d);documents.append(dict(path=p.relative_to(P).as_posix(),sha256=sha(d)))
write(S/'document-manifest.json',documents)
write(S/'validation.json',dict(**pointer,parent_commit=read(S/'vcs-context.json')['parent_commit'],state_schema=12,accepted_game_pairs=pairs,accepted_frames=frames,production_c_sources=174,content_inputs=298,unsupported_guards=37,native_cases=native['cases'],probes=native['groups'],source_files=len(manifest),finite_functional_conformance=True,bug_for_bug_required=False,cleanup_performed_this_round=True,pushed=False))
write(S/'final-check.json',dict(passed=True,exe_sha256=digest,source_manifest_sha256=sha(S/'source-manifest.json'),document_manifest_sha256=sha(S/'document-manifest.json'),pushed=False))
print(dict(passed=True,generation=41,exe_sha256=digest,source_files=len(manifest),pairs=pairs,frames=frames))
