"""Promote batch48 finite effects with preserved diagnostics, baseline and rollbacks."""
from run_batch_v49 import *
for name in ['native-gates.json','effects.json','preservation.json','cleanup.json','final-scene-matrix.json','rng-provenance.json']:assert read(S/name)['passed'],name
receipt=read(R/'ra2/build-original-c/source-content-receipt.json');digest=sha(R/'ra2/build-original-c/ra2.exe')
matrix=read(S/'final-scene-matrix.json');effects=read(S/'effects.json');native=read(S/'native-gates.json');clean=read(S/'cleanup.json')
parts=[read(S/'parts'/n/'validation.json') for n in ['finish','landing']];assert parts[-1]['exe_sha256']==digest
pairs=sum(x['scene_count'] for x in parts)+len(matrix['results']);frames=sum(x['frames'] for x in parts)+matrix['production_frames']+matrix['observer_frames']
strict=all(x['strict_trace_equal'] for x in matrix['results']);variations=effects['accepted_baseline_variations'];assert strict and not variations
report=P/'docs/单位移动第四十八批-共享出口与连接边界及随机分流和坍塌交通-20261024.txt'
handoff=P/'交接文档-单位移动第四十八批正式验收-20261024.txt';policy=P/'docs/项目目标与验收边界-20261024.txt'
rep=effects['representative'];ru=rep['r2']['modes']['original'];nd=rep['nd']['modes']['original'];nu=rep['nu']['modes']['original'];ws=rep['ws']['modes']['original']
text=f'''单位移动第四十八批（正式48 / 验证49），2026-10-24。
父提交：{read(S/'vcs-context.json')['parent_commit']}。第四十七批392项封存逐项核对，本轮311项独立基线保留。
程序：{R/'ra2/build-original-c/ra2.exe'}
SHA-256：{digest}
政策：{policy}

实现与服务边界
以整体功能、效果、规则和资源解读一致为目标，不追求逐个BUG复刻。只固定本批实现和有限效果，不代表全游戏等价。
新增ground_exit_policy.h/.c，明确八类Prepare出口的清路径、启动重试、完成计时、递归、清段、清驾驶标记和目标取消计划。
ground_completion按原次序执行清路径→启动重试→计时尾→递归；递归出口立即返回。非递归清理后才查目标，强制取消入口短路目标查询。取消服务可改变owner，停止服务仍重读当前owner；目标停止及递归保留完整32位结果，普通停止只清低字节。
ground_landing保留已有模板早退、离格→清段→查连接→失败清理，以及启动连接→接近点→当前地面高度→目标高度/时长→完成连接的顺序。仅把32位回绕高差、向零整除及回绕加法放入共享函数，不缓存跨服务owner；保留非零时长和有效x86有符号商的调用约定。
180个生产C、310项编译内容、37个未实现保护。只另改ground_completion、ground_landing及CMake；生成入口/runtime适配/生产记录器schema12/通用比较器/生产规则和美术未改。
两组原版映射片段各32768例，共65536例；核对探针范围内的回调顺序、副作用、状态、结果和栈清理。运输128例、Capture64例按源/程序哈希继承，不重跑、不重复计数。
两部分各默认遭遇战301帧、南北桥交会及出口占位各501帧，每部分3配对1303帧，分别保留源码/工具/程序回退。

额外时序随机数分流
针对父批b3-dc建立独立只读诊断，生产随机函数、比较器和记录器不改，不重置随机状态。
首个随机快照分流仍是1029帧。同一LCRF（1023362）：原版1028帧仍为Move，经Foot virtual133的4C3945调用抽取[0,2]周期扰动；C1029帧已为Guard，经Foot virtual129抽取[0,2]。原生记录返回地址4C394A，C记录函数入口4C4660，不能当同类地址比较。
窗口原版345次、C344次实际抽取；按抽取顺序对齐的前344次索引和原始随机字完全相同。证据指向到达/任务服务调度改变抽样时点及分配，窗口内未发现生成算法自身不同的证据。
诊断主轨迹分别与旧样本全部前缀一致：到1045帧完整记录及1046帧入口快照相同。上游已有气垫到达数值差异和整段后续随机分配未穷尽，不宣称已修复或全尾段等价。严格false和原始轨迹保留，未计入正式严格通过。
首次短窗运行含未来命令，被输入检查拒绝，保留但排除；后续限窗命令成功。诊断文件/源码身份、调用清单及抽取顺序证据见rng-provenance.json。

新增代表实景
粗糙卸载r2：用普通地图记录换入原版land7平坦图块并保持可达平台高度；正常Enter装车。{ru['collapse_frame']}帧载货船水平移动时桥毁，{ru['trap_removed_frame']}帧触发车移除，{ru['drop_frame']}帧卸载。实际货车落格{ru['landing_cell']}、land={ru['landing_land']}，再Move到{ru['cargo_final']}。船300、货车和动态车200、步兵125生命保持。
邻近载具nd/nu：登陆艇[62,66]与桥上/下[61,66]受影响车辆水平相距256世界单位。货车正常装入；桥毁后船/货生命和装载状态保持至1300帧，步兵仍完成移动。
nd车辆初始Z0/下层，{nd['collapse_frame']}帧桥毁时当帧移除，不称作桥面坠落。
nu车辆普通Move从[61,62]驶入[61,66]，Z416/上层1；{nu['collapse_frame']}帧失桥层，连续下落，{nu['victim_removed_frame']}帧移除。最后存活生命仍200，只证明坠落/移除过程，不虚报扣血量。触发车另于1140帧移除。
坡型1 ws：取原版[51,32]普通坡面记录，东侧级5平台接级4。主车西向下坡入桥，900帧后返程东向上坡；520↔416，中间坡面分别{[len(x['samples']) for x in ws['ramps']]}帧，桥层0→1→0→1→0，最终回到{ws['end']}。含对向车、移动步兵及450帧释放的出口占位车。
四场均严格逐模拟帧一致；当前原版/C还各自等于改代码前完整轨迹。使用普通地图和正常命令，不调用破桥/伤害/装卸/落位或路径结果函数伪造效果。

回归、保留、清理与后续
最终生产{matrix['production_scenes']}配对{matrix['production_frames']}帧，独立普通事件/只读观察宿主{matrix['observer_scenes']}配对{matrix['observer_frames']}帧；含两部分共{pairs}配对{frames}帧，均严格相同，随机检查保持。实景最多两配对通道/四个游戏进程，固定seed12345。
列车碰撞、步兵碾压、重复失败及原版弯曲高差Z436停滞、Z-193未完成已有限回归并保留。受控单位环仅用于重复失败诊断，不将异常扩展为永久逐BUG要求。
初试ru在运行时实际落到清地land0，未计作粗糙卸载；改用原版[83,32]的稳定粗糙图块后另跑r2，按实际落格验收，原输入/轨迹保留。
b-nc移动运输初试虽然均移除受影响车辆并卸货，但登陆艇到达/返回位置和随机分配不同，输入和完整轨迹保留，未计正式通过；坍塌效果由nd/nu覆盖，粗糙卸载由r2独立覆盖。
29非主C候选/86原始入边的旧证据按哈希继承，当前310项输入扫描无新增直接C调用，原标签/分发表保留；没有新自然入口结论，不强造入口。
父批392项封存、本轮311项基线、两部分回退、改动前宿主、全部探索和原版异常保留。H盘20项原版输入、只读规则、原版EXE、SAVE0029、旧手写引擎及Git配置/远端引用不变。
清理{clean['deleted_files']}个逐路径/类型/哈希核对的可重建文件或缓存，共{clean['deleted_bytes']}字节；同目录{clean['protected_files']}个非候选文件哈希不变。源文件、正式程序、资源、轨迹、基线和回退保留。
剩余：未覆盖状态/服务、其他真实水岸装卸/移动器及坡型、其他引擎子系统。额外Hover到达误差和后续随机影响作为已知差异保留，仅在影响功能效果时有界推进。
复核：{R/'verify_final_movement_v49.py'}。本地提交不推送，收据：{S/'postcommit/git-local-commit.json'}。
'''
assert not report.exists() and not handoff.exists();report.write_text(text,encoding='utf-8',newline='\n')
handoff.write_text(f'''当前正式48 / 验证49，2026-10-24。
父提交：{read(S/'vcs-context.json')['parent_commit']}。
政策：{policy}
报告：{report}
程序SHA-256：{digest}
Prepare八类共享出口及Advance连接高度/服务边界完成；180C/310输入/37保护，生成入口/runtime/记录器/比较器/规则和美术未改。
两部分各3配对1303帧并保留回退；共{pairs}配对{frames}帧严格相同，原生65536例。运输128/Capture64例按哈希继承。
额外时序首处分流1029帧已定位同一登陆艇的到达/周期调用：原版1028帧Move的4C3945，C1029帧Guard的virtual129。前344次原始抽取字/索引序列相同；诊断主轨迹等于旧样本各自前缀。未修随机函数/强行同步，严格false保留，不计通过；上游气垫到达误差和全尾段分配仍为已知差异。
粗糙实际卸载land7、桥下当帧移除、桥上正常驶入后失层/坠落并于1139帧移除、相邻一格已载货登陆艇保持状态；坡型1西下/东上及桥交通完成。四场均等于改动前各自完整轨迹。
b-nc移动运输差异、无效短窗输入、父批异常及29候选调查保留，不强造自然入口，不追逐BUG一致。
基线：{S/'baseline'}；分部回退：{S/'parts'}；基线宿主：{S/'baseline-observer'}；封存：{S/'final-source'}。
后续：剩余状态/服务、其他真实水岸装卸/移动器/坡型、其他子系统，维持整体功能与效果一致的有限验收边界。
复核：{R/'verify_final_movement_v49.py'}。本地提交不推送。
''',encoding='utf-8',newline='\n')
lead=f'最新接续：第四十八批正式48 / 验证49已验收。\n交接：{handoff}\n政策：{policy}\nEXE：{digest}\n以下历史原地保留。\n\n'.encode('utf-8')
for name in ['交接文档-原版逆向与C重编译-20261020.txt','交接文档-新对话继续推进-20261022.txt']:
 p=P/name;p.write_bytes(lead+p.read_bytes())
p=P/'README.md';ls=p.read_bytes().splitlines(keepends=True);eol=b'\r\n' if ls[0].endswith(b'\r\n') else b'\n'
p.write_bytes('> 当前研究路线（2026-10-24）：原版1.006 C17/x86单位移动第四十八批已验收。Prepare出口/Advance连接、随机分流来源、粗糙卸载与坍塌及反向坡面；[第四十八批交接](交接文档-单位移动第四十八批正式验收-20261024.txt)。继续遵守[整体功能与效果一致的验收边界](docs/项目目标与验收边界-20261024.txt)。'.encode('utf-8')+eol+b''.join(ls[1:]))
p=R/'ra2/src/gameplay/阅读说明-单位移动.txt';p.write_bytes(f'第四十八批（2026-10-24）\n新增ground_exit_policy，整理Prepare出口和Advance连接高度服务；180C/310输入/37保护，{pairs}配对{frames}帧、原生65536例。\n额外随机分流定位到到达/任务周期，保留严格false，不改随机函数。\n报告：{report}\n\n'.encode('utf-8')+p.read_bytes())
pointer=dict(passed=True,status='promoted',formal_baseline_generation=48,verification_round=49,validation=str(S/'validation.json'),exe_sha256=digest,sha256=digest,executable=str(R/'ra2/build-original-c/ra2.exe'),full_original_equivalence_verified=False,report=str(report),handoff=str(handoff),acceptance_policy=str(policy))
for name in ['latest-recovery.json','latest-state-comparison.json','latest-movement-candidate.json']:
 p=P/'reports'/name;x=read(p);x.update(pointer);x['current_batch']=dict(formal_generation=48,verification_round=49,accepted_game_pairs=pairs,accepted_frames=frames,native_cases=65536,production_c_sources=180,content_inputs=310,strict_all_frames_equal=strict,accepted_baseline_variations=variations);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
write(S/'remaining-work.json',dict(passed=True,bug_for_bug_required=False,natural_alias_dispatch_required=False,percentage_reestimated=False,remaining=['Uncovered generated state/service entries','Other genuine water-shore unload, locomotors and ramps','Known Hover arrival/scheduling and later RNG assignment differences: finite effect-driven work only','Other engine subsystem integration']))
paths={Path(p).relative_to(R).as_posix() for p in receipt['inputs']}
paths.update(['ra2/CMakeLists.txt','ra2/run_lift.py','ra2/tools/playtest.py','ra2/build-original-c/ra2.exe','ra2/build-original-c/source-content-receipt.json','ra2/src/gameplay/阅读说明-单位移动.txt','build-faithful.ps1','run_fixture_comparison.py','run_state_comparison.py','evidence/movement-state-v4/SOV01T-original.MAP'])
paths.update(p.relative_to(R).as_posix() for p in R.glob('*v49*') if p.is_file())
paths.update(p.relative_to(R).as_posix() for p in S.iterdir() if p.is_file() and p.suffix in ['.c','.h','.asm','.exe'])
paths.update(p.relative_to(R).as_posix() for p in (S/'fixtures').iterdir() if p.is_file())
paths.update(p.relative_to(R).as_posix() for p in S.glob('*fixtures*.json'))
paths.update((S/n).relative_to(R).as_posix() for n in ['bridge-catalog-build-arguments.json','rng-build-arguments.json','rng-attribution-build-arguments.json','mission-table-proof.json','transport-native-validation-current.json','native-gates.json','service-boundaries.json','rng-provenance.json','excluded-near-transport.json','mixed-terrain-exploration.json','slope-details.json'])
manifest=[]
for rel in sorted(paths):
 d=S/'final-source'/rel;d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/rel,d);manifest.append(dict(path=rel,sha256=sha(d)))
write(S/'source-manifest.json',manifest)
docs=[P/'README.md',report,handoff,policy]+[P/n for n in ['交接文档-原版逆向与C重编译-20261020.txt','交接文档-新对话继续推进-20261022.txt']]+[P/'reports'/n for n in ['latest-recovery.json','latest-state-comparison.json','latest-movement-candidate.json']]
documents=[]
for p in docs:
 d=S/'current-project'/p.relative_to(P);d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,d);documents.append(dict(path=p.relative_to(P).as_posix(),sha256=sha(d)))
write(S/'document-manifest.json',documents)
write(S/'validation.json',dict(**pointer,parent_commit=read(S/'vcs-context.json')['parent_commit'],state_schema=12,accepted_game_pairs=pairs,accepted_frames=frames,production_c_sources=180,content_inputs=310,unsupported_guards=37,native_cases=native['cases'],probes=native['groups'],capture_packet_cases_inherited=64,transport_packet_cases_inherited=128,accepted_inherited_variations=variations,strict_all_frames_equal=strict,source_files=len(manifest),finite_functional_conformance=True,bug_for_bug_required=False,cleanup_performed_this_round=True,pushed=False))
write(S/'final-check.json',dict(passed=True,exe_sha256=digest,source_manifest_sha256=sha(S/'source-manifest.json'),document_manifest_sha256=sha(S/'document-manifest.json'),pushed=False))
print(dict(passed=True,generation=48,exe_sha256=digest,source_files=len(manifest),pairs=pairs,frames=frames))
