"""Promote the finite functional batch, preserving exact build and rollback inputs."""
from run_batch_v43 import *
for n in ['native-gates.json','effects.json','preservation.json','alias-evidence-inheritance.json','cleanup.json','final-scene-matrix.json']:assert read(S/n)['passed'],n
receipt=read(R/'ra2/build-original-c/source-content-receipt.json');digest=sha(R/'ra2/build-original-c/ra2.exe');matrix=read(S/'final-scene-matrix.json');effects=read(S/'effects.json');clean=read(S/'cleanup.json');native=read(S/'native-gates.json')
assert read(S/'parts/process/validation.json')['exe_sha256']==digest
report=P/'docs/单位移动第四十二批-Prepare特殊阻挡与Process收尾及修桥绕行实景-20261024.txt';handoff=P/'交接文档-单位移动第四十二批正式验收-20261024.txt';policy=P/'docs/项目目标与验收边界-20261024.txt'
parts=[read(S/'parts'/n/'validation.json') for n in ['prepare','process']]
pairs=matrix['production_scenes']+matrix.get('observer_scenes',0)+sum(x['scene_count'] for x in parts);frames=matrix['production_frames']+matrix.get('observer_frames',0)+sum(x['frames'] for x in parts)
exploratory=[]
for folder in sorted(list((S/'runs').glob('baseline-*'))+[S/'runs/discover-repair']):
 x=read(folder/'comparison.json');exploratory.append(dict(tag=folder.name,passed=x['passed'],frames=x.get('comparison',{}).get('frames_compared',0)))
text=f'''单位移动第四十二批（正式42 / 验证43），2026-10-24。
父提交：{read(S/'vcs-context.json')['parent_commit']}。第四十一批403项封存已核对，当前301项独立基线原地保留。
程序：{R/'ra2/build-original-c/ra2.exe'}
SHA-256：{digest}
政策：{policy}

本轮范围与结束条件
继续以整体功能、效果、规则解读和美术资源调用一致为目标，不逐BUG复刻，也不无限扩大逐帧矩阵。完成本轮四个业务单元、代表效果和受影响回归，保留回退与差异后即提交。

实现
Prepare剩余的近目标失败停止分支与cloaked/temporary特殊阻挡，复用第四十一批的路段失效与目标取消/停止接口；保留递归重试、列车旁路、桥层通知和服务后的owner存活检查，不合并两次任务查询。
Process将新段和同帧接续的Prepare/Advance/存活/finish服务序列收拢到prepare_and_advance；同帧第二段继续传1，新段传0，避免重复累计速度。先前分支查询、目标同步、转向后刷新和无路径时停止速度保持原顺序。
Arrival将刷新后的可用性、取消目标与路径、停止Move任务、owner更新及存活分流集中到finish_after_refresh。Process和Arrival均复用已验证的有效路段失效规则，真实到达后的driving无条件清零仍保留。
只改ground_prepare.c、ground_special.c、ground_drive.c、ground_arrival.c。没有新增生产C或修改头文件/CMake；仍为174个C、298项编译输入、37个未实现保护。生成入口、runtime适配、生产比较器/记录器及schema12均未改。

本轮验证
Prepare和Process/Arrival两部分，各默认遭遇战301帧、南北桥上步兵车辆交会与占用出口各501帧，每部分1303帧，各自保存完整源码/EXE回退。
六组受影响原生路径共{native['cases']}例：Prepare入口/重试/组合周期各65536，特殊阻挡65536，Process32768，Arrival65536。另64例原版004B6170命令构造器核对全部111字节，验证捕获输入的目标UID位于0E、类型位于12。
最终正式程序{matrix['production_scenes']}场{matrix['production_frames']}帧；工程师正常命令/只读桥格宿主{matrix['observer_scenes']}场{matrix['observer_frames']}帧；连同两部分共{pairs}个通过功能验收的原版/C配对、{frames}帧。
普通状态、命令/移动审计、随机数按模拟帧核对；飞行单位一项严格差异明确保留，见下文。比较器差异定位和缺帧拒绝自检通过。最多两条游戏通道/四个游戏进程，构建串行；未重跑无关历史大矩阵。
另{len(exploratory)}个基线配对用于对象编号/配方资格与差异定位，和正式验收分开记；原始输入、程序身份、日志、轨迹均保留。

代表实景与效果
{json.dumps(effects['representative'],ensure_ascii=False,indent=2)}

工程师正常进入原版CABHUT维修屋：沿用原版SOV01T的58,73位置，目标为普通建筑对象。600帧提交Capture8正常MEGAMISSION，进入原有OutList后由原版/C原有任务执行修桥；未直接调用修桥/路径/结果函数，也未写桥梁标志或强造路段。
200帧桥中两格断口均为非桥；工程师消耗后900帧两格恢复，1000帧给后车重新发Move命令，随后跨桥抵达目标。只删除捕获命令的同图对照保留工程师、断口不恢复，后车仍无法越过。
独立功能验收宿主只增加已核对布局的正常捕获输入，及200/900帧只读桥格标志、900帧格目录；生产记录器未改变。当前修桥与对照的全部轨迹与基线同模式逐条一致。
毁桥绕行使用普通地图开辟的替代通道：前车触桥后下落移除，后车只有一次Move命令，自行离开60/61桥道，从替代通道绕过断口抵达原目标；没有路径、速度或对象链注入。
飞行移动器使用原版JUMPJET规则与资源，在断口上方飞过并到达目标格。没有声称本轮重写了完整Jumpjet/Ship等移动器。

差异与继承证据
Jumpjet在本轮生产改动前的基线即有小幅位置/朝向差异：最大世界坐标X1、Y22（22/256格，不足0.09格），朝向580/65536圈（约3.2度）；581/1001帧严格相等。严格comparison.json仍为false，功能验收另存functional-acceptance.json，比较器未放宽。
只有该飞行单位的两个水平坐标和两个朝向字段存在上述变化，Z、生命、任务、随机数、普通命令和其他对象/字段完全一致。当前原版与基线原版、当前C与基线C的全部轨迹记录分别逐条相同，证明没有被本轮整理扩大。只记录这项既有差异，不为追平瞬时浮点/转向数值无限扩展工作。
原版弯曲高差Z436停滞和Z-193未完成异常继续保留；当前有限回归表现一致，不作为永久照搬BUG的要求。真实列车碰撞与步兵碾压继续回归，关闭规则的负对照沿用前批证据。
29个非主C候选与86条原始入边沿用，全部298项输入未新增直接C调用引用；本轮没有新的独立合法自然入口结论，不强造入口凑覆盖。

保留与清理
父批403项封存、当前301项基线、两部分回退和基线功能宿主均保留。只封存当前实际构建输入、本轮工具、选用的17项历史场景输入及新增地图/探针，不再复制所有旧探索地图和旧代工具。
按路径/类型/哈希清理{clean['deleted_files']}个可重建中间文件或缓存，共{clean['deleted_bytes']}字节；{clean['protected_files']}个同目录非候选文件哈希一致。源文件、正式程序、原始资源、存档、轨迹、基线和回退保留。
原版EXE、真实SAVE0029、旧手写引擎、H盘既有20项白名单及只读提取规则指纹保持不变。生产规则和美术资源未改。

剩余内容
继续按功能单元整理其他生成状态入口、更多移动器和动态交通/修桥组合，以及规则和资源与其他引擎子系统的集成。当前仍非完整可读地面移动或独立全游戏引擎；单个代表场景通过不能推导全游戏等价或总体完成百分比。
保留有界自然入口待核和飞行细微差异，只有新功能证据或重要回归才扩展验证。
复核：{R/'verify_final_movement_v43.py'}。
本轮本地提交，不推送；提交身份见postcommit/git-local-commit.json。
'''
assert not report.exists() and not handoff.exists();report.write_text(text,encoding='utf-8',newline='\n')
handoff.write_text(f'''当前正式42 / 验证43，2026-10-24。
政策：{policy}
报告：{report}
程序SHA-256：{digest}
已整理Prepare近目标失败/特殊阻挡、Process新段与接续服务序列及Arrival刷新收尾；仅四个现有业务C改变。174个C、298项输入、37保护，生成入口/适配/生产记录器/比较器未改。
两部分各3场1303帧，有独立回退。正式与功能宿主共{pairs}个验收配对{frames}帧；六组原生路径{native['cases']}例，另64例原版命令构造器。
已取得工程师正常进入维修屋修桥、桥格恢复后车辆重新通行、无捕获命令负对照、毁桥后自然绕行、Jumpjet飞过断口的实景。
Jumpjet既有水平位置不足0.09格/朝向约3.2度差异保留，严格报告false与独立功能验收分开；当前各模式轨迹与基线分别逐条一致，不追逐瞬时数值完美相同。
原版两项高差异常、29候选来源调查和父批原始证据保留。只有受影响/新功能证据才扩大矩阵。
基线：{S/'baseline'}；回退：{S/'parts'}；基线功能宿主：{S/'baseline-observer'}；当前封存：{S/'final-source'}。
复核：{R/'verify_final_movement_v43.py'}。后续继续其他移动器/状态入口与全引擎集成；有限验收、清理可再生成缓存，本地提交不推送。
''',encoding='utf-8',newline='\n')
lead=f'最新接续：第四十二批正式42 / 验证43已验收。\n交接：{handoff}\n政策：{policy}\nEXE：{digest}\n以下历史原地保留。\n\n'.encode('utf-8')
for name in ['交接文档-原版逆向与C重编译-20261020.txt','交接文档-新对话继续推进-20261022.txt']:
 p=P/name;p.write_bytes(lead+p.read_bytes())
p=P/'README.md';raw=p.read_bytes();ls=raw.splitlines(keepends=True);eol=b'\r\n' if ls[0].endswith(b'\r\n') else b'\n';p.write_bytes('> 当前研究路线（2026-10-24）：原版1.006 C17/x86单位移动第四十二批已验收。Prepare特殊阻挡、Process/Arrival收尾及工程师修桥恢复通行/毁桥绕行代表实景；[第四十二批交接](交接文档-单位移动第四十二批正式验收-20261024.txt)。继续遵守[整体功能与效果一致的验收边界](docs/项目目标与验收边界-20261024.txt)，保留基线、回退和原版异常。'.encode('utf-8')+eol+b''.join(ls[1:]))
p=R/'ra2/src/gameplay/阅读说明-单位移动.txt';p.write_bytes(f'第四十二批（2026-10-24）\nPrepare特殊阻挡和近目标失败复用停止契约；Process统一新段/同帧接续服务顺序，Arrival集中刷新后收尾。正常命令修桥恢复通行、毁桥绕行和飞行跨断口效果已核对，飞行既有小差异另存功能验收。\n174个C、298项输入、37保护；{pairs}个验收配对{frames}帧；原生{native["cases"]}例。\n报告：{report}\n继续按整体功能/效果一致验收，不追逐逐BUG或无限内部计数一致。\n\n'.encode('utf-8')+p.read_bytes())
pointer=dict(passed=True,status='promoted',formal_baseline_generation=42,verification_round=43,validation=str(S/'validation.json'),exe_sha256=digest,sha256=digest,executable=str(R/'ra2/build-original-c/ra2.exe'),full_original_equivalence_verified=False,report=str(report),handoff=str(handoff),acceptance_policy=str(policy))
for n in ['latest-recovery.json','latest-state-comparison.json','latest-movement-candidate.json']:
 p=P/'reports'/n;x=read(p);x.update(pointer);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
write(S/'exploration-summary.json',dict(passed=True,results=exploratory,excluded_from_acceptance=True))
write(S/'remaining-work.json',dict(passed=True,bug_for_bug_required=False,natural_alias_dispatch_required=False,percentage_reestimated=False,remaining=['Other generated state entries and service boundaries','More locomotors and dynamic repair/traffic combinations','Other engine subsystems and integration']))
paths={Path(p).relative_to(R).as_posix() for p in receipt['inputs']}
paths.update(['ra2/CMakeLists.txt','ra2/run_lift.py','ra2/tools/playtest.py','ra2/build-original-c/ra2.exe','ra2/build-original-c/source-content-receipt.json','ra2/src/gameplay/阅读说明-单位移动.txt','build-faithful.ps1','run_fixture_comparison.py','run_state_comparison.py','evidence/movement-state-v4/SOV01T-original.MAP','make_elevated_tubes_v29.py'])
paths.update(p.relative_to(R).as_posix() for p in R.glob('*v43*') if p.is_file());paths.update(p.relative_to(R).as_posix() for p in S.iterdir() if p.is_file() and p.suffix in ['.c','.h','.asm','.exe']);paths.update(p.relative_to(R).as_posix() for p in (S/'fixtures').iterdir() if p.is_file())
paths.update(p.relative_to(R).as_posix() for p in S.glob('*fixtures*.json'))
manifest=[]
for rel in sorted(paths):
 d=S/'final-source'/rel;d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/rel,d);manifest.append(dict(path=rel,sha256=sha(d)))
write(S/'source-manifest.json',manifest)
docs=[P/'README.md',report,handoff,policy]+[P/n for n in ['交接文档-原版逆向与C重编译-20261020.txt','交接文档-新对话继续推进-20261022.txt']]+[P/'reports'/n for n in ['latest-recovery.json','latest-state-comparison.json','latest-movement-candidate.json']];documents=[]
for p in docs:
 d=S/'current-project'/p.relative_to(P);d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,d);documents.append(dict(path=p.relative_to(P).as_posix(),sha256=sha(d)))
write(S/'document-manifest.json',documents)
write(S/'validation.json',dict(**pointer,parent_commit=read(S/'vcs-context.json')['parent_commit'],state_schema=12,accepted_game_pairs=pairs,accepted_frames=frames,production_c_sources=174,content_inputs=298,unsupported_guards=37,native_cases=native['cases'],probes=native['groups'],capture_packet_cases=64,accepted_inherited_variations=1,strict_all_frames_equal=False,source_files=len(manifest),finite_functional_conformance=True,bug_for_bug_required=False,cleanup_performed_this_round=True,pushed=False))
write(S/'final-check.json',dict(passed=True,exe_sha256=digest,source_manifest_sha256=sha(S/'source-manifest.json'),document_manifest_sha256=sha(S/'document-manifest.json'),pushed=False))
print(dict(passed=True,generation=42,exe_sha256=digest,source_files=len(manifest),pairs=pairs,frames=frames))
