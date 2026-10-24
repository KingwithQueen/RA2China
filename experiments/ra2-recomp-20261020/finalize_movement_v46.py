"""Promote one finite batch with source, document and rollback identities."""
from run_batch_v46 import *
for name in ['native-gates.json','effects.json','preservation.json','alias-evidence-inheritance.json','cleanup.json','final-scene-matrix.json']:
 assert read(S/name)['passed'],name
receipt=read(R/'ra2/build-original-c/source-content-receipt.json');digest=sha(R/'ra2/build-original-c/ra2.exe')
matrix=read(S/'final-scene-matrix.json');effects=read(S/'effects.json');native=read(S/'native-gates.json');clean=read(S/'cleanup.json')
parts=[read(S/'parts'/n/'validation.json') for n in ['arrival','drive']]
assert parts[-1]['exe_sha256']==digest
pairs=sum(x['scene_count'] for x in parts)+len(matrix['results'])
frames=sum(x['frames'] for x in parts)+matrix['production_frames']+matrix['observer_frames']
strict=all(x['strict_trace_equal'] for x in matrix['results']);variations=effects['accepted_baseline_variations']
report=P/'docs/单位移动第四十五批-对象刷新与收尾服务边界及运输上下桥-20261024.txt'
handoff=P/'交接文档-单位移动第四十五批正式验收-20261024.txt';policy=P/'docs/项目目标与验收边界-20261024.txt'
rep=effects['representative'];transport=rep['bridge-transport'];hover=rep['hover-traffic']
text=f'''单位移动第四十五批（正式45 / 验证46），2026-10-24。
父提交：{read(S/'vcs-context.json')['parent_commit']}。第四十四批370项封存已逐项核对，本轮305项独立基线保留。
程序：{R/'ra2/build-original-c/ra2.exe'}
SHA-256：{digest}
验收边界：{policy}

实现与服务边界
以整体功能、效果、规则和资源解读一致为目标，不追求逐个BUG复刻。只对本批变化、代表效果及受影响回归做有限验收。
新增ground_owner_boundary.h/.c：刷新后实时检查可用性；到达后按原顺序取消目标/路径、读取有效任务、停止Move、更新对象，最后才查存活。显式返回CONTINUE/RETURN_FALSE/RETURN_TRUE，保留所有短路和服务副作用。
ground_arrival把原有刷新/任务收尾接入该服务边界，原先的位置落定、路段失效、目标与高差判断保持原顺序。不能在刷新前缓存可用性或任务；更新返回true时不新增存活查询。
ground_drive在原地转向结束后先清pending，再调用同一刷新/可用性边界；不可用时仍立即返回0，正常驾驶不套用到达阶段的取消目标、停止和更新策略。
177个生产C、304项编译内容输入、37个未实现保护；新增一C一头文件，另改arrival/drive业务C及CMake。生成入口、runtime适配、比较器、生产记录器/schema12、生产规则和美术资源不变。

原生片段与分部验收
到达收尾65536例、驾驶Process32768例，共98304例；服务调用次序、状态、返回/栈等按探针范围与原版核对。到达3937次继续、61599次返回。普通Enter/Unload构造器另128例，所有111字节与原版构造器相同；继承Capture64例证明不重复运行或计数。
到达与驾驶两部分各默认遭遇战301帧、南北桥上出口占用/车辆步兵交会各501帧，每部分3配对1303帧，并保存各自源码/工具/程序回退。
最终生产程序{matrix['production_scenes']}配对{matrix['production_frames']}帧、正常事件/只读观察功能宿主{matrix['observer_scenes']}配对{matrix['observer_frames']}帧；连同分部共{pairs}配对{frames}帧。其中气垫一组单列既有数值差异的功能验收，其余严格逐模拟帧相同。
三项选定动态场景的当前原版与C分别必须与自己的改动前完整记录逐条相同。固定seed12345；构建串行，最多两条配对通道/四个游戏进程，不把初始化或未达成探索计作正式功能通过。

运输、上下桥与动态交通实景
普通FV装载一名E2：正常Enter命令50帧，{transport['board_frame']}帧记录到乘员离开地面活动占位；载具400帧开始过桥，乘员保持装载。
载具桥层变化：{transport['carrier_bridge_transitions']}。这是桥层进入/离开验证，当前平齐桥头Z均416，不宣称验证了陡坡高度变化。
载具与对向步兵有{len(transport['simultaneous_bridge_motion_frames'])}帧同时在桥面移动。关系查询实际时点见effects.json；本配方没有两者都移动时的关系查询，不把同时运动当作该查询的证明。另有出口占位车辆，800帧正常Move、实际{transport['blocker_first_motion']}帧开始运动。
1200帧正常Unload，{transport['unload_frame']}帧乘员重新出现在出口地面；1450帧发往可通行桥面，{transport['passenger_first_motion']}帧开始独立运动，最终{transport['passenger_final']}且桥层标志为1。载具最后{transport['carrier_final']}，对向步兵最后{transport['opposing_infantry_final']}；载具200、乘员及对向步兵125生命保持不变。
负对照仅省去Unload及其后的乘员移动命令：1200帧之前状态逐帧一致，乘员到1900帧仍在装载状态，不能把停留的旧位置当作已卸载。
功能宿主只构造普通事件进入原有队列，另读步兵原始字节74/75/76/79/7A/7D与桥格。不直接调用装载、卸载、修桥、路径或落位结果，也不改写对象/桥层/速度。
任务号来自原版0x7CD774任务名表：Enter=7、Unload=16；构造器0x4B6170证明保存。Enter必须把载具作为destination写入+0x13/+0x17；Capture使用target +0x0E/+0x12，两者不能照搬。
早期把Enter放入target位置，原版转为攻击载具；输入、构造器检查、宿主和完整轨迹全部保留，不作为装载成功。正确装卸后的早期移动目标未达成，也保留原始轨迹；最终使用普通可通行桥面目标，没有调整规则或强制路径。
修正输入时业务第一部分已构建，因此专门从305项父批基线重编译旧arrival对象、移除新helper链接，其他业务仍为第四十四批，独立建立正确输入的改动前功能宿主。其程序/源/参数与身份清单保存在baseline/transport-observer，不把第一部分结果冒充父批基线。另已从父批arrival/drive源独立重建可重建回退程序，保留原资格宿主；该构建检查不计新增运行配对。

其他移动器、既有差异与原版异常
气垫/地面车/步兵混合绕行沿用第四十四批已证实可达配方，因Driver改变而重跑：共同水平移动{hover['horizontal_simultaneous_frames']}帧，车、气垫及步兵分别完成目标。没有把气垫悬浮升降当水平通行。
气垫原版/C的既有水平坐标、转向和地形查询时点差异保留：X13/Y21世界单位，方向5316/5324，计时88/4；严格comparison.json仍为false，局部功能验收要求当前各模式完整轨迹与本轮基线一致，其他状态、普通命令、地面单位、生命、规则值和随机数一致。没有修改通用比较器。初轮额外气垫占格标志时点观察也留存；最终运输专用观察只读取步兵字段。
两项原版高差异常Z436停滞、Z-193未完成继续保留，有限回归中当前一致，不自动变成永久BUG复刻要求。列车碰撞、步兵碾压和重复失败受影响回归已跑；规则关闭负对照继承既有证据，前批Jumpjet差异保留，不扩大无关矩阵。
29个非主C候选、86条原始入边沿用；当前304项输入扫描无新增直接C调用，标签和原始分发表保留，没有新增合法自然入口结论，不强造入口。

保留、清理与剩余范围
父批370项封存、本批305项基线、两部分回退、旧/新功能宿主、输入修正前探索、数值差异和原版异常保留。当前封存只含实际编译内容、当前工具、必要探针与有限配方。
清理{clean['deleted_files']}个路径/类型/哈希逐项核对的可重建中间文件或缓存，共{clean['deleted_bytes']}字节；同目录{clean['protected_files']}个非候选文件哈希不变。原始资源、源文件、存档、程序、轨迹和回退保留。
H盘20项原版输入、只读提取规则、原版EXE、SAVE0029、旧引擎及Git配置/远端引用不变。
本批只覆盖FV单步兵运输、当前平齐桥头的桥层转换和代表交通；载车运输、其他装卸地形/移动器、真正的坡面上下桥、剩余状态入口与其他引擎子系统仍需后续有界推进，不宣称全游戏等价或估算缺少可靠分母的总进度。
复核：{R/'verify_final_movement_v46.py'}。
本地提交，不推送；提交身份见{S/'postcommit/git-local-commit.json'}。
'''
assert not report.exists() and not handoff.exists();report.write_text(text,encoding='utf-8',newline='\n')
handoff.write_text(f'''当前正式45 / 验证46，2026-10-24。
政策：{policy}
报告：{report}
程序SHA-256：{digest}
新增共享对象刷新/到达收尾边界；Arrival保留取消/停止/更新次序，Driver只复用刷新后可用性检查，不混用后续策略。
177C/304输入/37保护；生成入口/runtime/生产记录器/比较器/规则与美术未改。
两部分各3配对1303帧并保存回退；正式矩阵共{pairs}配对{frames}帧，原生98304例，普通运输构造器另128例，Capture64证明只继承。
FV正常装载、桥层进入/离开、与步兵同桥动态交通、出口占位车离开、正常卸载及乘员独立返回桥面已实测；不卸载对照保持装载。平齐桥头Z416，不冒称陡坡测试。
Enter使用destination，与Capture的target不同；早期错误目标造成攻击、正确装卸后的未达成移动目标及初轮额外气垫观察均保留。
正确输入的父批业务宿主：{S/'baseline/transport-observer'}；初始宿主：{S/'baseline-observer'}。原版/C各自与正确输入基线完整记录相同。
气垫既有细微差异单列功能验收；严格false不改写，原版高差异常/旧Jumpjet差异和29候选来源调查保留，不追求逐BUG复刻。
基线：{S/'baseline'}；回退：{S/'parts'}；封存：{S/'final-source'}。
后续推进载车运输、其他移动器/装卸地形、真实坡面上下桥、剩余状态服务和其他子系统；有限功能验收、清理可重建缓存、本地提交不推送。
复核：{R/'verify_final_movement_v46.py'}。
''',encoding='utf-8',newline='\n')
lead=f'最新接续：第四十五批正式45 / 验证46已验收。\n交接：{handoff}\n政策：{policy}\nEXE：{digest}\n以下历史原地保留。\n\n'.encode('utf-8')
for name in ['交接文档-原版逆向与C重编译-20261020.txt','交接文档-新对话继续推进-20261022.txt']:
 p=P/name;p.write_bytes(lead+p.read_bytes())
p=P/'README.md';ls=p.read_bytes().splitlines(keepends=True);eol=b'\r\n' if ls[0].endswith(b'\r\n') else b'\n'
p.write_bytes('> 当前研究路线（2026-10-24）：原版1.006 C17/x86单位移动第四十五批已验收。对象刷新与收尾服务边界、FV装卸与桥层转换及代表交通；[第四十五批交接](交接文档-单位移动第四十五批正式验收-20261024.txt)。继续遵守[整体功能与效果一致的验收边界](docs/项目目标与验收边界-20261024.txt)，保留基线、回退和原版异常。'.encode('utf-8')+eol+b''.join(ls[1:]))
p=R/'ra2/src/gameplay/阅读说明-单位移动.txt'
p.write_bytes(f'第四十五批（2026-10-24）\n新增ground_owner_boundary，整理Arrival收尾与Driver转向结束的对象刷新/可用性边界，保留两者后续分流。\nFV普通装卸、桥层进入/离开及乘员独立返回桥面已实测；177C/304输入/37保护，{pairs}配对{frames}帧，原生98304例，运输构造器另128例。\n报告：{report}\n\n'.encode('utf-8')+p.read_bytes())
pointer=dict(passed=True,status='promoted',formal_baseline_generation=45,verification_round=46,validation=str(S/'validation.json'),exe_sha256=digest,sha256=digest,executable=str(R/'ra2/build-original-c/ra2.exe'),full_original_equivalence_verified=False,report=str(report),handoff=str(handoff),acceptance_policy=str(policy))
for name in ['latest-recovery.json','latest-state-comparison.json','latest-movement-candidate.json']:
 p=P/'reports'/name;x=read(p);x.update(pointer);x['current_batch']=dict(formal_generation=45,verification_round=46,accepted_game_pairs=pairs,accepted_frames=frames,native_cases=98304,production_c_sources=177,content_inputs=304,strict_all_frames_equal=strict,accepted_baseline_variations=variations);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
exploratory=[]
for folder in sorted((S/'runs').glob('b*')):
 if folder.is_dir() and (folder/'comparison.json').is_file():
  q=read(folder/'comparison.json');exploratory.append(dict(tag=folder.name,strict_passed=q['passed'],frames=q['comparison']['frames_compared'],selected=folder.name in [x['baseline_tag'] for x in read(S/'dynamic-fixtures.json')['fixtures']],counted_in_final_matrix=False))
write(S/'exploration-summary.json',dict(passed=True,results=exploratory,unqualified_transport_input_tags=['b-tr','b-tc'],initial_readonly_hover_flag_variation_tag='b-hv',all_original_reports_retained=True))
write(S/'remaining-work.json',dict(passed=True,bug_for_bug_required=False,natural_alias_dispatch_required=False,percentage_reestimated=False,remaining=['Other generated state entries and service boundaries','Vehicle cargo, other locomotors, unloading terrain and real bridge slopes','Other engine subsystems and integration']))
paths={Path(p).relative_to(R).as_posix() for p in receipt['inputs']}
paths.update(['ra2/CMakeLists.txt','ra2/run_lift.py','ra2/tools/playtest.py','ra2/build-original-c/ra2.exe','ra2/build-original-c/source-content-receipt.json','ra2/src/gameplay/阅读说明-单位移动.txt','build-faithful.ps1','run_fixture_comparison.py','run_state_comparison.py','evidence/movement-state-v4/SOV01T-original.MAP','evidence/movement-state-v46/service-boundaries.json'])
paths.update(p.relative_to(R).as_posix() for p in R.glob('*v46*') if p.is_file())
paths.update(p.relative_to(R).as_posix() for p in S.iterdir() if p.is_file() and p.suffix in ['.c','.h','.asm','.exe'])
paths.update(p.relative_to(R).as_posix() for p in (S/'fixtures').iterdir() if p.is_file())
paths.update(p.relative_to(R).as_posix() for p in S.glob('*fixtures*.json'))
paths.update((S/n).relative_to(R).as_posix() for n in ['transport-baseline-build-arguments.json','bridge-catalog-build-arguments.json','baseline-rebuild-support.json','mission-table-proof.json','transport-native-validation-current.json','native-gates.json'])
manifest=[]
for rel in sorted(paths):
 d=S/'final-source'/rel;d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/rel,d);manifest.append(dict(path=rel,sha256=sha(d)))
write(S/'source-manifest.json',manifest)
docs=[P/'README.md',report,handoff,policy]+[P/n for n in ['交接文档-原版逆向与C重编译-20261020.txt','交接文档-新对话继续推进-20261022.txt']]+[P/'reports'/n for n in ['latest-recovery.json','latest-state-comparison.json','latest-movement-candidate.json']]
documents=[]
for p in docs:
 d=S/'current-project'/p.relative_to(P);d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,d);documents.append(dict(path=p.relative_to(P).as_posix(),sha256=sha(d)))
write(S/'document-manifest.json',documents)
write(S/'validation.json',dict(**pointer,parent_commit=read(S/'vcs-context.json')['parent_commit'],state_schema=12,accepted_game_pairs=pairs,accepted_frames=frames,production_c_sources=177,content_inputs=304,unsupported_guards=37,native_cases=native['cases'],probes=native['groups'],capture_packet_cases_inherited=64,transport_native_packet_cases=128,accepted_inherited_variations=variations,strict_all_frames_equal=strict,source_files=len(manifest),finite_functional_conformance=True,bug_for_bug_required=False,cleanup_performed_this_round=True,pushed=False))
write(S/'final-check.json',dict(passed=True,exe_sha256=digest,source_manifest_sha256=sha(S/'source-manifest.json'),document_manifest_sha256=sha(S/'document-manifest.json'),pushed=False))
print(dict(passed=True,generation=45,exe_sha256=digest,source_files=len(manifest),pairs=pairs,frames=frames))
