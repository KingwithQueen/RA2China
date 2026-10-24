"""Promote a finite functional-conformance batch, retaining parent archives in place."""
from run_batch_v39 import R,P,S,O,read,write,sha
from pathlib import Path
import shutil,json
names=['native-gates.json','effects.json','bridge-cross-release-effects.json','alias-natural-scenes.json','internal-alias-sources.json','preservation.json','cleanup.json','final-scene-matrix.json']
for name in names:assert read(S/name)['passed'],name
native=read(S/'native-gates.json');matrix=read(S/'final-scene-matrix.json');aliases=read(S/'alias-natural-scenes.json');clean=read(S/'cleanup.json')
precheck=S/'investigations/cleanup-precheck-01/receipt.json';assert read(precheck)['files_deleted']==0
write(S/'cleanup-precheck-recovery.json',dict(passed=True,precheck_receipt=str(precheck),precheck_sha256=sha(precheck),failed_precheck_deleted_files=0,all_scenes_completed_before_successful_cleanup=True,successful_cleanup_sha256=sha(S/'cleanup.json')))
assert native['groups']==41 and native['new_cases']==327680
assert matrix['production_scenes']==9 and matrix['production_frames']==5459 and matrix['observer_frames']==4008
assert not aliases['natural_entry_candidates']
digest=sha(R/'ra2/build-original-c/ra2.exe');assert digest==read(S/'parts/returns/validation.json')['exe_sha256']
report=P/'docs/单位移动第三十八批-采样目标接续与桥上途中放行组合-20261024.txt'
handoff=P/'交接文档-单位移动第三十八批正式验收-20261024.txt'
policy=P/'docs/项目目标与验收边界-20261024.txt';assert policy.exists()
bridges=read(S/'bridge-cross-release-effects.json')['scenes']
summary='\n'.join(f"{name}：关系/几何查询帧{[q['frame'] for q in x['query_samples']]}，出口等待{x['wait_range']}，绕行{x['detour_frames']}帧，跨出口{x['cross_frame']}，首次到目标格{x['arrival_frame']}；占位车发令/实际移动"+str([(m['order_frame'],m['first_actual_motion_frame']) for m in x['blocker_motion']]) for name,x in bridges.items())
text=f'''单位移动第三十八批正式验收（正式38 / 验证39）
日期：2026-10-24。代码父提交：65ffecb844c08b0dbc5d46c53b7646635572c108。
程序：{R/'ra2/build-original-c/ra2.exe'}
SHA-256：{digest}

本轮验收边界
以相同功能、效果、规则解读和资源调用为目标，不要求bug-to-bug完美复刻。逐帧对照用于发现有意义的差异；确认本轮功能并跑完受影响回归即可交付，不无限扩大矩阵。
政策原文落实：{policy}。这一边界优先于下面历史文档中“完全等价/必须保留每个异常”的旧表述。
本轮未引入主动修复原版BUG或规则、美术资源变更。所跑场景恰好逐帧一致，不表示日后必须保持每一帧、每个内部寄存器或原版BUG一致。

已完成的实现
4A2326：12段载入采样/哨兵接续；先读取样本再写回局部坐标，选择继续采样或结束落点。
4A24A2：12段当前位置/前一格/目标选择；坐标读取与写回相邻，处理进度<=3与后续主分支。
4A2528：13段当前位置和目标格比较；复用已有纯C格坐标算法，保留符号坐标解释及同格/跨格结果。
703A3B：3段已经返回武器持有槽的对象分类；空槽和弹头标志决定阻挡/继续。复用原有具体对象分类，不重复查询武器服务。
4A2590：13段定位—桥层—重新占格出口；与此前离格出口共用后半段，已经完成的离格服务不重复调用。定位回调后重新读取格子、桥层、当前对象；返回过程沿用原适配。
改动编译输入仅4项：recomp_0010.c、recomp_0046.c、ground_joint_bridge.c、ground_objects_bridge.c。171个C源、292项构建内容、37个未实现保护不变。
原生标签、跳转尾表、原指令注释与入口注册保留；0010保留LF、0046保留CRLF。比较器、状态记录器与schema12未改。

本轮实际执行的验证
模板、对象分类、服务出口每部分各3场：默认遭遇战301帧、南北桥组合各501帧，合计每部分1303帧；各有独立源码/EXE回退和清单。
最终受影响边界回归41组、2686976例，其中新增5组327680例。含旧的离格出口与武器分类回归、空武器槽、别名局部坐标、带修改副作用的回调。
最终正式程序9场5459帧；独立观察2场1002帧；29个非主候选分组观察6场3006帧。最终共17个原版/C配对；连同三部分共26个配对、13376帧。均通过逐模拟帧状态、命令、随机数核对和差异定位自检。
本轮固定seed12345；最多两条场景通道、4个游戏进程，所有编译器串行。没有把旧126组/71场49241帧历史矩阵写成本轮重跑结果。
旧完整矩阵留在{O}，已复核其6328项封存、正式37身份，沿用未受影响部分的证据。

桥上新增组合的实际效果
普通地图和正常命令：移动E2与车辆对向交会、两格出口占用、相邻车道先移动，主车道在主车途中放行；主车只发一次移动命令，不写路径/对象链/桥层或移动状态。
{summary}
两向都观测到移动中的步兵关系和几何查询、近出口等待、绕行、相邻车移动期间主车绕行；主出口实际移动发生在跨出口之后、抵达目标之前。步兵和主车最终都到目标格，生命值保持125/200。
独立观察版与正式程序状态、普通命令及移动审计一致。
已有南北交会、敌对动态交通、受控隧道出口阻挡、重复寻路失败及两种弯曲高差异常纳入代表性回归。
隧道阻挡/重复失败使用已有诊断单位环，属于受控障碍试验，不称为未经干预的自然对局；桥上新增组合完全使用普通地图和命令。

29个非主C副本
静态来源仍为29个候选、86条原始字节核对的入边、3个主入口对照；未发现直接原生CALL、非代码区地址字面量或直接C调用引用。
6场交替南北的普通桥上途中放行实景分组配置全部29个候选；主入口阳性对照均出现，未观测到独立非主C首次分派。
原生函数内部跳转是合法自然来源；它不等于通过单独生成的C副本分派。计算目标、运行时指针和未跑场景未被排除；记录为有边界的开放项，不阻挡整体功能交付，不再以穷尽29种独立命中为完工条件。

保留、清理与回退
第三十七批完整封存原地保留；另存361项构建/程序及探针回退，旧文档与阅读说明保留。三部分回退各322/323/327项。
本轮封存当前构建输入、当前工具和配方；不再次复制全部历史6328项。旧封存和调查证据未删除。
按哈希白名单删除{clean['deleted_files']}个根目录可再生.obj，共{clean['deleted_bytes']}字节；{clean['protected_files']}个同目录非候选文件前后哈希一致。未递归、未强制删除，无源文件、程序、轨迹、基线或回退删除。
首次清理预检遇到仍在写入的观察日志而停止，未删除文件；记录保留于investigations/cleanup-precheck-01，全部场景结束后重新生成清单并清理通过。
H盘原版1.006仅核对既有20项白名单；D盘原始EXE、真实存档和旧引擎指纹保持一致。不扩大为整个H盘都已验收。
两项原版异常记录继续保留：4→6弯曲高差最终Z436停滞，7→4最终Z-193未完成。候选当前同样表现；它们是已知问题证据，不是必须永远复刻的BUG要求。

剩余工作与下一批边界
继续以可修改的功能单元整理Advance/Prepare及连接状态机，减少生成外壳；优先处理能影响规则/效果的分支和服务，不逐条包装所有不可达旧指令。
具体对象分类还需扩展碾压、建筑/地形、桥梁破坏、其他移动器与带对象失效/替换的服务组合；选择有限、代表性的效果验收。
更广的战役/遭遇战集成、渲染/音效/UI、存读档/网络和移植仍属后续；当前不是完整独立可读引擎。37个保护尚存。
非主副本来源调查保留清单，只有新证据或功能差异出现时再扩展。以前76%/22%及8–15批是旧定义的历史主观估算，本轮未据新边界重新量化，不将它当当前完成比例。

复核入口：{R/'verify_final_movement_v39.py'}。
本轮只做本地提交，不推送。提交完成后的Git身份见evidence/movement-state-v39/postcommit/git-local-commit.json。
'''
assert not report.exists() and not handoff.exists();report.write_text(text,encoding='utf-8',newline='\n')
handoff.write_text(f'''当前正式基线38 / 验证39，2026-10-24。
先读：{policy}
验收与接续报告：{report}
程序SHA-256：{digest}
只读核对：{R/'verify_final_movement_v39.py'}
基线：{S/'baseline'}；三部分回退：{S/'parts'}；当前封存：{S/'final-source'}。
父批完整封存仍在：{O/'final-source'}。
三个优先入口4A2326/4A24A2/4A2528、703A3B分类和4A2590服务出口本轮已完成。
每部分3场1303帧；最终9场正式程序5459帧、8场观察4008帧；41组受影响探针，其中5组新增327680例。旧大矩阵沿用证据，未重复计数。
下一批按功能单元收拢剩余Advance/Prepare及对象/移动器服务，选有限场景验证规则和效果。29个副本未观测到独立自然C入口，不以穷尽这些命中或复刻原版BUG作为完工条件。
保留原版异常、旧调查、基线和回退；及时删除已验证可重建的编译中间文件。本地提交，不推送。
''',encoding='utf-8',newline='\n')
lead=f'''最新接续：第三十八批已验收，正式38 / 验证39。
先读验收边界：{policy}
交接：{handoff}
程序SHA-256：{digest}
只读核对：{R/'verify_final_movement_v39.py'}
以功能/效果/规则/资源整体一致为目标；逐帧比较有边界，不要求BUG逐个复刻。下列历史描述以此为准。

'''
for name in ['交接文档-原版逆向与C重编译-20261020.txt','交接文档-新对话继续推进-20261022.txt']:
 p=P/name;p.write_bytes(lead.encode('utf-8')+p.read_bytes())
p=P/'README.md';lines=p.read_text(encoding='utf-8').splitlines(keepends=True);lines[0]='> 当前研究路线（2026-10-24）：原版1.006 C17/x86单位移动第三十八批已验收。4A2326/4A24A2/4A2528接续、对象分类与定位占格出口；采用[整体功能一致的验收边界](docs/项目目标与验收边界-20261024.txt)，完成有限逐帧对照与受影响回归。入口为[第三十八批交接](交接文档-单位移动第三十八批正式验收-20261024.txt)。基线、回退、原版异常保留。\n';p.write_text(''.join(lines),encoding='utf-8',newline='\n')
p=R/'ra2/src/gameplay/阅读说明-单位移动.txt';p.write_bytes(f'''第三十八批当前状态（2026-10-24）
4A2326/4A24A2/4A2528、703A3B与4A2590已整理；每部分3场1303帧，最终正式9场5459帧，观察8场4008帧，受影响探针41组。
本项目追求相同功能、效果、规则解读及资源调用；不要求BUG逐个复刻。逐帧比较用于定位有意义差异，未受影响矩阵可沿用；有解释的原版BUG修复可另行验收。此边界优先于下方历史中的严格等价措辞。
报告：{report}
政策：{policy}

'''.encode('utf-8')+p.read_bytes())
pointer=dict(passed=True,status='promoted',formal_baseline_generation=38,verification_round=39,validation=str(S/'validation.json'),exe_sha256=digest,executable=str(R/'ra2/build-original-c/ra2.exe'),full_original_equivalence_verified=False,report=str(report),handoff=str(handoff),acceptance_policy=str(policy))
for name in ['latest-recovery.json','latest-state-comparison.json','latest-movement-candidate.json']:
 (P/'reports'/name).write_text(json.dumps(pointer,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
write(S/'remaining-work.json',dict(passed=True,completed_entries=['004A2326','004A24A2','004A2528','00703A3B','004A2590'],alias_investigation_open=True,natural_aliases_required_for_completion=False,bug_for_bug_required=False,remaining=['Functional consolidation of Advance/Prepare/connection state machines','Concrete crushing/building/terrain/bridge destruction and locomotor/service combinations','Wider campaign/skirmish integration and other engine subsystems'],unsupported_guards=37,percentage_reestimated=False,historical_estimates_not_current=True))
receipt=read(R/'ra2/build-original-c/source-content-receipt.json');paths={Path(p).relative_to(R).as_posix() for p in receipt['inputs']}
paths.update(['ra2/build-original-c/ra2.exe','ra2/build-original-c/source-content-receipt.json','ra2/CMakeLists.txt','ra2/run_lift.py','ra2/tools/playtest.py','ra2/src/gameplay/阅读说明-单位移动.txt','run_fixture_comparison.py','run_state_comparison.py','build-faithful.ps1'])
paths.update(p.relative_to(R).as_posix() for p in R.glob('*v39*') if p.is_file())
paths.update(p.relative_to(R).as_posix() for p in S.iterdir() if p.is_file() and p.suffix in ['.c','.h','.asm'])
paths.update(p.relative_to(R).as_posix() for p in (S/'fixtures').iterdir() if p.is_file())
paths.update((S/name).relative_to(R).as_posix() for name in ['bridge-cross-release-fixtures.json','connection-fixture-build-arguments.json','connection-fixture-probe.exe','overlap_probe.exe','objects_probe.exe'])
manifest=[]
for rel in sorted(paths):
 dest=S/'final-source'/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/rel,dest);manifest.append(dict(path=rel,sha256=sha(dest)))
write(S/'source-manifest.json',manifest)
docs=[P/'README.md',policy,report,handoff]+[P/n for n in ['交接文档-原版逆向与C重编译-20261020.txt','交接文档-新对话继续推进-20261022.txt']]+[P/'reports'/n for n in ['latest-recovery.json','latest-state-comparison.json','latest-movement-candidate.json']]
doc_manifest=[]
for p in docs:
 dest=S/'current-project'/p.relative_to(P);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest);doc_manifest.append(dict(path=p.relative_to(P).as_posix(),sha256=sha(dest)))
write(S/'document-manifest.json',doc_manifest)
write(S/'validation.json',dict(**pointer,parent_commit=read(S/'vcs-context.json')['parent_commit'],sha256=digest,state_schema=12,paired_scenes=9,paired_frames=5459,observer_scenes=8,observer_frames=4008,part_scenes=9,part_frames=3909,total_game_pairs_executed=26,total_frames_compared=13376,probes=41,native_cases=2686976,new_fragment_cases=327680,source_files=len(manifest),production_c_sources=171,content_inputs=292,unsupported_guards=37,legal_alias_sources_examined=29,nonprimary_overlapping_adapter_naturally_observed=False,bug_for_bug_required=False,finite_functional_conformance=True,cleanup_performed_this_round=True,accepted_parent_archive_retained=True))
write(S/'final-check.json',dict(passed=True,exe_sha256=digest,source_files=len(manifest),report_sha256=sha(report),handoff_sha256=sha(handoff),policy_sha256=sha(policy),source_manifest_sha256=sha(S/'source-manifest.json'),document_manifest_sha256=sha(S/'document-manifest.json'),pushed=False))
print(dict(passed=True,generation=38,exe_sha256=digest,source_files=len(manifest),report=str(report)),flush=True)
