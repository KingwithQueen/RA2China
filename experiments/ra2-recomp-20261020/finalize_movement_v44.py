"""Promote the finite functional batch, preserving exact build and rollback inputs."""
from run_batch_v44 import *
for n in ['native-gates.json','effects.json','preservation.json','alias-evidence-inheritance.json','cleanup.json','final-scene-matrix.json']:assert read(S/n)['passed'],n
receipt=read(R/'ra2/build-original-c/source-content-receipt.json');digest=sha(R/'ra2/build-original-c/ra2.exe');matrix=read(S/'final-scene-matrix.json');effects=read(S/'effects.json');clean=read(S/'cleanup.json');native=read(S/'native-gates.json')
assert read(S/'parts/turn/validation.json')['exe_sha256']==digest
report=P/'docs/单位移动第四十三批-重建结果与转弯服务边界及修桥动态交通-20261024.txt';handoff=P/'交接文档-单位移动第四十三批正式验收-20261024.txt';policy=P/'docs/项目目标与验收边界-20261024.txt'
parts=[read(S/'parts'/n/'validation.json') for n in ['rebuild','turn']]
pairs=matrix['production_scenes']+matrix.get('observer_scenes',0)+sum(x['scene_count'] for x in parts);frames=matrix['production_frames']+matrix.get('observer_frames',0)+sum(x['frames'] for x in parts)
exploratory=[]
for folder in sorted([p for p in (S/'runs').iterdir() if p.is_dir() and (p.name.startswith('baseline-') or p.name.startswith('b-'))]):
 x=read(folder/'comparison.json');exploratory.append(dict(tag=folder.name,passed=x['passed'],frames=x.get('comparison',{}).get('frames_compared',0)))
text=f'''单位移动第四十三批（正式43 / 验证44），2026-10-24。
父提交：{read(S/'vcs-context.json')['parent_commit']}。第四十二批368项封存已核对，当前301项独立基线保留。
程序：{R/'ra2/build-original-c/ra2.exe'}
SHA-256：{digest}
政策：{policy}

范围与实现
以整体功能、效果、规则及资源解读一致为验收边界，不要求逐BUG或无关瞬时数值完全相同。固定当前实现、代表效果与受影响回归，保留差异和回退后结束本批。
新增ground_rebuild_result.h/.c：集中重建后的owner存在、写aborted、目标接受和停止服务，返回READY/NO_OWNER/REJECTED。成功时是否复核owner由调用点明确指定。
ground_prepare_exit在非timer_only分支复核成功/失败重建的owner；拒绝直接退出，不重启短计时器。ground_followup成功时跳过owner复核；失败被拒绝并停止后仍重取第二方向，只有NO_OWNER才直接aborted。两个调用点的不同后续策略保留，未因共用服务而合并。
ground_turn的列车/碾压放行复用已有template_gate，保留类型与覆盖层查询短路顺序；停止候选复用已验证的路段失效与取消/停止导航。临时障碍停止失败后丢弃候选，隐形/完全阻挡则直接返回；递归重试和提交方向队列保持原分流。
175个生产C、300项编译输入，新增一C一头文件；仅另改prepare_exit、followup、turn三个业务C及CMake。生成入口、runtime适配、比较器、生产记录器/schema12和37个未实现保护不变。

验证
重建结果与Turn两部分，各默认遭遇战301帧、南北占用出口/步兵车辆交会各501帧，每部分1303帧，并各自保存源码/EXE回退。
四组受影响原生片段共262144例：Followup速度/候选两个阶段各65536，等待重建出口65536，Turn分类/停止/重试/提交65536；Turn包括3537例分类过程owner失效。服务次序、状态、返回/栈及相关x87边界均按探针已覆盖范围核对。正常Capture命令构造器64例证明沿用前批，源和探针程序哈希一致，本轮没有重复运行或混入新计数。
最终正式程序{matrix['production_scenes']}场{matrix['production_frames']}帧、正常命令/只读桥格功能宿主{matrix['observer_scenes']}场{matrix['observer_frames']}帧；连同两部分共{pairs}个功能验收配对、{frames}帧。气垫绕行有一项基线差异另存功能验收，其余代表矩阵按严格逐模拟帧核对。
固定seed12345，最多两条配对通道/四个游戏进程，所有构建串行。受控单位环只用于重复失败回归，与普通地图/正常命令实景分开。
另{len(exploratory)}个资格探索配对单独保留；初始化失败和未合格配方不计正式验收。没有为穷尽全部标签或追平瞬时数值扩大矩阵。

动态组合的真实效果
{json.dumps(effects['representative'],ensure_ascii=False,indent=2)}

修桥交通：普通地图中工程师正常进入维修屋修复断口；900帧桥格恢复、1800帧仍可通行。车辆重新发令后与反向步兵交会，并遇到两辆出口占位车；两车以1350/1450帧普通Move命令先后离开。静止气垫单位构成出口附近的另一种对象占位。保留断口、仅省去捕获命令的对照中，工程师仍在，车辆与步兵没有跨越断口。
毁桥绕行：同一普通地形替代通道上加入停放车辆、移动步兵和实际移动的LCRF气垫单位；主车只有一次Move命令，自行绕过断口及占位，最终完成经过出口的移动。气垫与步兵也到达各自目标区域。没有直接改写桥/路径、速度、对象链或最终结果。
功能宿主继承已核对的Capture8普通事件输入，只多一次1800帧只读桥格观察；生产记录器不改。所有新效果分别检查原版与C，且当前每个模式的动态场景轨迹须与本轮改动前对应基线逐条一致。

差异、探索与原版异常
气垫绕行在本轮源码改动前已出现水平坐标与转向状态差异；位置最大X13/Y21世界单位（不足0.09格），方向和转向计时具体最大值见functional-acceptance.json。地面车辆、步兵、生命、任务、桥格、随机数、普通命令及其余状态字段一致；仅该气垫单位的地形查询时点有变化，规则值计数一致。
严格comparison.json仍保留false；额外功能验收只允许已定位的六个气垫字段与其stage27地形观察变化，当前原版/C分别必须和本轮基线同模式全部记录逐条相同，不能扩大范围。没有修改通用比较器，也没有重写气垫移动器或追平既有转向振荡。前批Jumpjet差异原地保留，本轮不重跑其矩阵。
初轮气垫在修桥地图上的一条移动目标未达成，因此最终配方明确保留它作为静止占位；实际气垫移动效果由绕行配方验证。初轮停放车没有完成指定移动，最终配方也明确保留其静止占位，不把失败发令计作动态效果。
未修桥对照两次在较长运行标签下于ra2.csf初始化阶段退出，没有进入模拟；同一地图和命令改为短隔离目录后通过。日志、失败报告及输入全部保留，只记录观察与解决方式，不把未确定的根因归咎于游戏逻辑或修改原始资源。
原版两项弯曲高差异常Z436停滞、Z-193未完成仍保留，有限回归中当前表现一致，不作为永久逐BUG复刻要求。列车真实碰撞和步兵碾压继续回归，规则关闭负对照继承已验证历史。
29个非主C候选及86条原始入边沿用，全部300项输入扫描没有新增直接C调用；没有新的独立自然入口结论，不强造入口凑覆盖。

保留、清理与后续
父批368项封存、当前301项基线、两部分回退、基线功能宿主和全部探索/异常输入轨迹保留。本轮封存仅当前实际构建内容、当前配方、选用场景和必要探针。
清理{clean['deleted_files']}个路径/类型/哈希已核对的可重建中间文件或缓存，共{clean['deleted_bytes']}字节；{clean['protected_files']}个同目录非候选文件哈希不变。源文件、正式程序、原始资源/存档、轨迹和回退保留。
H盘20项原版输入、只读提取规则、原版EXE、真实SAVE0029和旧手写引擎指纹不变；生产规则及美术资源未改。
仍需推进其他状态入口、移动器及运输/上下桥等服务边界与其他引擎子系统集成；本批不是完整可读地面移动或全游戏等价。只在新功能证据、重要差异或回归出现时扩大有界验证，不估算总体百分比。
复核：{R/'verify_final_movement_v44.py'}。
本地提交，不推送；提交身份见postcommit/git-local-commit.json。
'''
assert not report.exists() and not handoff.exists();report.write_text(text,encoding='utf-8',newline='\n')
handoff.write_text(f'''当前正式43 / 验证44，2026-10-24。
政策：{policy}
报告：{report}
程序SHA-256：{digest}
新增共享重建结果，保留Prepare出口与Followup不同的owner复核及拒绝后接续策略；Turn复用类型放行与停止契约并保留重试/丢弃/提交分支。
175个C、300项输入、37保护；生成入口/适配/生产记录器/比较器未改。
两部分各3场1303帧，有独立回退；共{pairs}个功能配对{frames}帧，四组原生262144例。64例Capture构造器证明仅继承，未重复计入。
已验证修桥恢复后的步兵车辆交会、1350/1450出口占位车先后放行、静止气垫占位，以及毁桥绕行中车辆/步兵/移动气垫组合；无修桥命令负对照也已核对。
气垫水平坐标及转向/地形查询时点差异在本轮改动前已存在，严格报告false和功能验收分开保存；当前各模式完整轨迹分别与基线相同，未扩大差异或修改通用比较器。
两次长目录资源初始化失败在短运行目录复核通过，原始失败报告保留，根因未定。原版高差异常、前批Jumpjet差异和29候选来源调查均保留。
基线：{S/'baseline'}；回退：{S/'parts'}；基线功能宿主：{S/'baseline-observer'}；当前封存：{S/'final-source'}。
后续继续其他状态入口、移动器/运输/上下桥与全引擎集成；有限功能验收，清理可再生成缓存，本地提交不推送。
复核：{R/'verify_final_movement_v44.py'}。
''',encoding='utf-8',newline='\n')
lead=f'最新接续：第四十三批正式43 / 验证44已验收。\n交接：{handoff}\n政策：{policy}\nEXE：{digest}\n以下历史原地保留。\n\n'.encode('utf-8')
for name in ['交接文档-原版逆向与C重编译-20261020.txt','交接文档-新对话继续推进-20261022.txt']:
 p=P/name;p.write_bytes(lead+p.read_bytes())
p=P/'README.md';raw=p.read_bytes();ls=raw.splitlines(keepends=True);eol=b'\r\n' if ls[0].endswith(b'\r\n') else b'\n';p.write_bytes('> 当前研究路线（2026-10-24）：原版1.006 C17/x86单位移动第四十三批已验收。共享重建结果、转弯服务边界及修桥后交会/占位放行与混类绕行代表实景；[第四十三批交接](交接文档-单位移动第四十三批正式验收-20261024.txt)。继续遵守[整体功能与效果一致的验收边界](docs/项目目标与验收边界-20261024.txt)，保留基线、回退和原版异常。'.encode('utf-8')+eol+b''.join(ls[1:]))
p=R/'ra2/src/gameplay/阅读说明-单位移动.txt';p.write_bytes(f'第四十三批（2026-10-24）\n新增ground_rebuild_result，共用重建后的服务检查；Prepare与Followup的不同接续策略保留。Turn的分类放行、停止/重试/丢弃候选边界已整理。\n修桥后交会/占位车辆放行与混类绕行已实测；气垫既有差异另存功能验收，不追平瞬时数值。\n175个C、300项输入、37保护；{pairs}个功能配对{frames}帧，原生262144例。\n报告：{report}\n\n'.encode('utf-8')+p.read_bytes())
pointer=dict(passed=True,status='promoted',formal_baseline_generation=43,verification_round=44,validation=str(S/'validation.json'),exe_sha256=digest,sha256=digest,executable=str(R/'ra2/build-original-c/ra2.exe'),full_original_equivalence_verified=False,report=str(report),handoff=str(handoff),acceptance_policy=str(policy))
for n in ['latest-recovery.json','latest-state-comparison.json','latest-movement-candidate.json']:
 p=P/'reports'/n;x=read(p);x.update(pointer);x['current_batch']=dict(formal_generation=43,verification_round=44,accepted_game_pairs=pairs,accepted_frames=frames,native_cases=262144,production_c_sources=175,content_inputs=300,strict_all_frames_equal=False,accepted_baseline_variations=1);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
write(S/'exploration-summary.json',dict(passed=True,results=exploratory,excluded_from_acceptance=True))
write(S/'remaining-work.json',dict(passed=True,bug_for_bug_required=False,natural_alias_dispatch_required=False,percentage_reestimated=False,remaining=['Other generated state entries and service boundaries','More locomotors and dynamic repair/traffic combinations','Other engine subsystems and integration']))
paths={Path(p).relative_to(R).as_posix() for p in receipt['inputs']}
paths.update(['ra2/CMakeLists.txt','ra2/run_lift.py','ra2/tools/playtest.py','ra2/build-original-c/ra2.exe','ra2/build-original-c/source-content-receipt.json','ra2/src/gameplay/阅读说明-单位移动.txt','build-faithful.ps1','run_fixture_comparison.py','run_state_comparison.py','evidence/movement-state-v4/SOV01T-original.MAP'])
paths.update(p.relative_to(R).as_posix() for p in R.glob('*v44*') if p.is_file());paths.update(p.relative_to(R).as_posix() for p in S.iterdir() if p.is_file() and p.suffix in ['.c','.h','.asm','.exe']);paths.update(p.relative_to(R).as_posix() for p in (S/'fixtures').iterdir() if p.is_file())
paths.update(p.relative_to(R).as_posix() for p in S.glob('*fixtures*.json'))
manifest=[]
for rel in sorted(paths):
 d=S/'final-source'/rel;d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/rel,d);manifest.append(dict(path=rel,sha256=sha(d)))
write(S/'source-manifest.json',manifest)
docs=[P/'README.md',report,handoff,policy]+[P/n for n in ['交接文档-原版逆向与C重编译-20261020.txt','交接文档-新对话继续推进-20261022.txt']]+[P/'reports'/n for n in ['latest-recovery.json','latest-state-comparison.json','latest-movement-candidate.json']];documents=[]
for p in docs:
 d=S/'current-project'/p.relative_to(P);d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,d);documents.append(dict(path=p.relative_to(P).as_posix(),sha256=sha(d)))
write(S/'document-manifest.json',documents)
write(S/'validation.json',dict(**pointer,parent_commit=read(S/'vcs-context.json')['parent_commit'],state_schema=12,accepted_game_pairs=pairs,accepted_frames=frames,production_c_sources=175,content_inputs=300,unsupported_guards=37,native_cases=native['cases'],probes=native['groups'],capture_packet_cases_inherited=64,accepted_inherited_variations=1,strict_all_frames_equal=False,source_files=len(manifest),finite_functional_conformance=True,bug_for_bug_required=False,cleanup_performed_this_round=True,pushed=False))
write(S/'final-check.json',dict(passed=True,exe_sha256=digest,source_manifest_sha256=sha(S/'source-manifest.json'),document_manifest_sha256=sha(S/'document-manifest.json'),pushed=False))
print(dict(passed=True,generation=43,exe_sha256=digest,source_files=len(manifest),pairs=pairs,frames=frames))
