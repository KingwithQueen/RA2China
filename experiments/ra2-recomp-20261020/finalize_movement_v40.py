"""Promote generation39 with finite functional verification and compact rollback/archive."""
from run_batch_v40 import R,P,S,O,read,write,sha
from pathlib import Path
import shutil,json
for name in ['native-gates.json','effects.json','bridge-cross-release-effects.json','preservation.json','alias-evidence-inheritance.json','cleanup.json','final-scene-matrix.json']:assert read(S/name)['passed'],name
matrix=read(S/'final-scene-matrix.json');assert matrix['production_frames']==5459 and matrix['observer_frames']==1002
native=read(S/'native-advance.json');clean=read(S/'cleanup.json');digest=sha(R/'ra2/build-original-c/ra2.exe')
assert read(S/'parts/services/validation.json')['exe_sha256']==digest
investigation=S/'investigations/build-link-01'
write(S/'build-recovery.json',dict(passed=True,cause='New API name collided with existing ground_sampling.c symbol; only the new API was renamed.',game_runs_affected=0,original_failure_receipt_sha256=sha(investigation/'receipt.json'),link_error_summary_sha256=sha(investigation/'link-error.txt'),successful_retry_log_sha256=sha(S/'build-advance-retry.log'),final_build_log_sha256=sha(S/'build-services.log'),production_executable_sha256=digest))
report=P/'docs/单位移动第三十九批-跨格进入与列车碰撞及共享定位业务-20261024.txt'
handoff=P/'交接文档-单位移动第三十九批正式验收-20261024.txt'
policy=P/'docs/项目目标与验收边界-20261024.txt'
text=f'''单位移动第三十九批（正式39 / 验证40），2026-10-24。
父基线：4c674913e268521e323b3329f38677388b6595ab；第三十八批475项封存已复核并原地保留。
程序：{R/'ra2/build-original-c/ra2.exe'}
SHA-256：{digest}

本轮按功能单元推进
继续遵守{policy}：整体功能、效果、规则解读和美术资源调用一致，不要求逐个BUG复刻；逐帧对照是有边界的回归工具。
本轮没有继续为未观测到的内部副本逐条增加包装，而是把实际使用的跨格行为和共享出口收拢成可修改的业务接口。
新增gameplay/ground_cell_placement.h/.c，定义离格、定位、更新桥层、进入前处理、重新占格的有序服务流程。needs_leave区分已经离格的入口；进入前处理可以在移动单位失效后阻止后续占格。
Advance主采样和原有4A2586/4A2590共享出口均接入同一业务流程；调用方适配寄存器、旧内存布局及返回值，业务层不访问原版固定地址。
ground_advance新增四个业务接口：ra2_ground_enter_sample_cell、ra2_ground_advance_train_contact、ra2_ground_advance_overlay_contact、ra2_ground_advance_finish_sample。
列车处理先保存下一对象，再调用当前对象的类型与伤害服务，允许伤害移除当前链项；在进入前重新检查移动单位存活。地表碾压的开启、类型、覆盖层和减速规则沿用既有服务；没有合并具有副作用的查询。
这些变化是对已有行为的功能化整理，不代表新增游戏规则或已经完成全部移动器/碾压机制。

实际验收范围
跨格业务与共享服务出口两部分，各3组代表场景：默认遭遇战301帧、南北桥上途中放行各501帧；每部分1303帧，各保存独立源码/EXE回退。
最终受影响原版片段回归28组、1835008例。采样推进65536例中包含{native['multiple_chain_target_cases']}例多目标链处理、{native['removed_before_enter_cases']}例进入前停止后续占格、{native['damage_calls']}次伤害服务；完整有序服务参数、对象/局部状态与原版核对通过。
共享出口包含两种入口以及回调替换owner、格子、坐标、保存槽和桥层的情形；此前其余接续/返回回归也通过。
最终正式程序9场5459帧，独立观察2场1002帧；加上两部分6场2606帧，本轮共17个原版/C配对、9067帧，状态、命令与随机数逐模拟帧一致，差异定位自检通过。
桥上两向都有移动步兵与车辆的关系/几何查询、出口等待、绕行和主车途中放行；车辆与步兵到达目标格，生命值200/125。独立观察器与正式程序状态一致。
既有南北交会、敌对动态交通、受控隧道出口阻挡、重复寻路失败、两项弯曲高差异常纳入有限回归。
列车链伤害和对象移除的证据来自映射原版片段探针，不称为真实列车毁桥场景验收。隧道阻挡与重复失败中的诊断单位环也与普通桥上地图/命令分开记录。
规则、美术资源及比较器/状态记录器未改；本轮不是新的渲染、美术或全游戏验收。沿用C17/x86和schema12。

非主副本调查
本轮全部生成C、入口注册与跳转表字节不变，没有新增原生或非主入口。294项编译输入扫描未发现新增直接C调用引用。
29个候选、86条原始字节入边和前批6场自然观察原地保留；仍未证明独立非主C自然分派。
本轮未重跑与改动无关的29候选场景，不把继承证据算为新增实测；计算入口和未跑场景保持开放，不以穷尽独立副本命中阻挡交付。

构建、清理和保留
172个生产C源、294项构建输入；新增一个业务C和一个头文件。37个未实现保护不变，生成C和原始指令注释未改。
首次完整链接发现新接口与ground_sampling.c已有ra2_ground_finish_sample重名。只将新增接口改名为ra2_ground_advance_finish_sample，沿用已完成Ninja依赖重编译，成功链接并核对输入后才更新内容收据；失败源码和链接错误摘要保留于investigations/build-link-01，无游戏验证受影响。
当前封存只保存当前构建内容、本轮配方与必要探针，不重复复制历史整代工具；第三十八批封存、295项独立基线、两部分回退和此前原版异常均保留。
完成全部验证后，按确切路径/类型/哈希清单清理{clean['deleted_files']}个无用中间文件和缓存，共{clean['deleted_bytes']}字节；{clean['protected_files']}个同目录非候选文件哈希不变。包括失活探针.obj、可再生Python字节码、保留C源的临时difftest程序、一个与原始存档完全同哈希的独立临时副本。没有递归或强制删除。
未删除源文件、真实原始存档、正式/历史程序、轨迹、基线或回退。H盘原版仅核对既有20项白名单；D盘原始程序、存档和旧引擎指纹保持一致。
原版4→6弯曲高差Z436停滞、7→4最终Z-193未完成继续保留记录；候选当前表现一致，未来合理修正并不受逐BUG复刻要求限制。

剩余工作
继续按功能模块收拢Prepare/Advance/连接中的状态转换与服务边界；具体对象、移动器、建筑/地形、碾压及毁桥组合选取代表性实景补齐。
本轮使跨格与占格业务更易修改；完整地面移动、全游戏可读恢复、独立布局/移植、UI/渲染/音效/网络等仍未完成。旧主观百分比未重新计算。
下一批不必追逐所有未进入的生成标签或原版异常；只在新功能、新证据或重要差异出现时扩展矩阵。
复核：{R/'verify_final_movement_v40.py'}。
本轮本地提交，不推送；提交身份写入本地postcommit/git-local-commit.json。
'''
assert not report.exists() and not handoff.exists();report.write_text(text,encoding='utf-8',newline='\n')
handoff.write_text(f'''当前正式39 / 验证40，2026-10-24。
先读验收边界：{policy}
报告：{report}
程序SHA-256：{digest}
只读复核：{R/'verify_final_movement_v40.py'}
新增ground_cell_placement有序服务流程；Advance跨格业务和4A2586/4A2590出口共用。列车链、地表碾压、完成采样可单独修改。
两部分各3场1303帧；最终9场正式程序5459帧、观察2场1002帧；共17个原版/C配对9067帧，28组受影响探针1835008例通过。
172个C源、294项构建输入、37个保护；生成C和入口注册未改。29候选的静态来源与前批自然观察继承，未声称本轮重跑或证明独立自然C分派。
基线：{S/'baseline'}；两部分回退：{S/'parts'}；封存：{S/'final-source'}。父批封存原地保留。
原版异常保留为证据，不作逐BUG复刻要求；后续按功能单元推进、有限验收，及时清理可确认无用的文件/缓存。本地提交，不推送。
''',encoding='utf-8',newline='\n')
lead=f'''最新接续：第三十九批已验收，正式39 / 验证40。
政策：{policy}
交接：{handoff}
程序SHA-256：{digest}
只读复核：{R/'verify_final_movement_v40.py'}
以下历史保留，以整体功能与效果一致的有限验收边界为准。

'''.encode('utf-8')
for name in ['交接文档-原版逆向与C重编译-20261020.txt','交接文档-新对话继续推进-20261022.txt']:
 p=P/name;p.write_bytes(lead+p.read_bytes())
p=P/'README.md';raw=p.read_bytes();lines=raw.splitlines(keepends=True);eol=b'\r\n' if lines[0].endswith(b'\r\n') else b'\n';head='> 当前研究路线（2026-10-24）：原版1.006 C17/x86单位移动第三十九批已验收。跨格进入、列车链/地表碾压业务与共享定位流程；[第三十九批交接](交接文档-单位移动第三十九批正式验收-20261024.txt)。继续遵守[整体功能与效果一致的验收边界](docs/项目目标与验收边界-20261024.txt)，保留基线、回退和原版异常。';p.write_bytes(head.encode('utf-8')+eol+b''.join(lines[1:]))
p=R/'ra2/src/gameplay/阅读说明-单位移动.txt';p.write_bytes(f'''第三十九批当前状态（2026-10-24）
ground_cell_placement：leave/place/update_layer/before_enter/enter的顺序业务，已接入Advance和既有共享出口；before_enter失效时不继续占格。
ground_advance：enter_sample_cell、advance_train_contact、advance_overlay_contact、advance_finish_sample为可修改业务单元。对象链下一项必须在伤害服务前保存，类型/owner/桥层查询仍按原来的服务顺序。
两部分各3场1303帧；最终正式9场5459帧、观察2场1002帧；28组受影响探针通过。列车伤害/移除证据属于原版片段，不能代替毁桥真实实景。
报告：{report}
仍遵守整体功能、效果、规则和美术资源调用一致；不要求逐BUG复刻或无限逐帧扩展。下方历史表述以此为准。

'''.encode('utf-8')+p.read_bytes())
pointer=dict(passed=True,status='promoted',formal_baseline_generation=39,verification_round=40,validation=str(S/'validation.json'),exe_sha256=digest,sha256=digest,executable=str(R/'ra2/build-original-c/ra2.exe'),full_original_equivalence_verified=False,report=str(report),handoff=str(handoff),acceptance_policy=str(policy))
for name in ['latest-recovery.json','latest-state-comparison.json','latest-movement-candidate.json']:
 p=P/'reports'/name;x=read(p);x.update(pointer);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
write(S/'remaining-work.json',dict(passed=True,completed_functional_units=['Ordered cell-placement services shared across Advance and two existing exits','Sampled cell entry, train-chain contact, overlay contact and finishing step'],remaining=['Prepare/Advance/connection state consolidation','Representative locomotor/crushing/building/terrain/bridge destruction scenes','Other engine subsystem readability and integration'],bug_for_bug_required=False,natural_alias_dispatch_required=False,percentage_reestimated=False))
receipt=read(R/'ra2/build-original-c/source-content-receipt.json');paths={Path(p).relative_to(R).as_posix() for p in receipt['inputs']}
paths.update(['ra2/CMakeLists.txt','ra2/run_lift.py','ra2/tools/playtest.py','ra2/build-original-c/ra2.exe','ra2/build-original-c/source-content-receipt.json','ra2/src/gameplay/阅读说明-单位移动.txt','build-faithful.ps1','run_fixture_comparison.py','run_state_comparison.py'])
paths.update(p.relative_to(R).as_posix() for p in R.glob('*v40*') if p.is_file())
paths.update(p.relative_to(R).as_posix() for p in S.iterdir() if p.is_file() and p.suffix in ['.c','.h','.asm','.exe'])
paths.update(p.relative_to(R).as_posix() for p in (S/'fixtures').iterdir() if p.is_file())
paths.update((S/n).relative_to(R).as_posix() for n in ['bridge-cross-release-fixtures.json','connection-fixture-build-arguments.json'])
manifest=[]
for rel in sorted(paths):
 dest=S/'final-source'/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/rel,dest);manifest.append(dict(path=rel,sha256=sha(dest)))
write(S/'source-manifest.json',manifest)
docs=[P/'README.md',report,handoff,policy]+[P/n for n in ['交接文档-原版逆向与C重编译-20261020.txt','交接文档-新对话继续推进-20261022.txt']]+[P/'reports'/n for n in ['latest-recovery.json','latest-state-comparison.json','latest-movement-candidate.json']]
documents=[]
for p in docs:
 dest=S/'current-project'/p.relative_to(P);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest);documents.append(dict(path=p.relative_to(P).as_posix(),sha256=sha(dest)))
write(S/'document-manifest.json',documents)
write(S/'validation.json',dict(**pointer,parent_commit=read(S/'vcs-context.json')['parent_commit'],state_schema=12,paired_scenes=9,paired_frames=5459,observer_scenes=2,observer_frames=1002,part_scenes=6,part_frames=2606,total_game_pairs_executed=17,total_frames_compared=9067,probes=28,native_cases=1835008,source_files=len(manifest),production_c_sources=172,content_inputs=294,unsupported_guards=37,generated_C_unchanged=True,legal_alias_sources_inherited=29,new_alias_runtime_scenes=0,bug_for_bug_required=False,finite_functional_conformance=True,cleanup_performed_this_round=True))
write(S/'final-check.json',dict(passed=True,exe_sha256=digest,source_files=len(manifest),report_sha256=sha(report),handoff_sha256=sha(handoff),policy_sha256=sha(policy),source_manifest_sha256=sha(S/'source-manifest.json'),document_manifest_sha256=sha(S/'document-manifest.json'),pushed=False))
print(dict(passed=True,generation=39,exe_sha256=digest,source_files=len(manifest),report=str(report)))
